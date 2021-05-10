"""
    MODULE
     Module containing the Python hooks that are called when a state transition takes place on an object created with
    the GenericMandatesAuthorization state machine definition.

    The context parameter is an instance of FBusinessProcessCallbackContext

    Conditions return True or False

    Name convention is
    'condition_' + 'entry_'/'exit_' + 'state_' + state name in lowercase and underscore

     The authorization process for mandates deal with the authorization processes (approval) for creating and updating
     mandates.

     The state chart models the authorization process as a single, non terminating business process associated with a
     mandate.

     There are two flows a creation and update flow. Creation occurs only once and update can occur zero or many times.
     The creation flow allows the mandate to be enabled after it is created. The update flow allows a mandate to be
     updated when changes are requested.

     Authorizer groups are used to control the authorization process. A Authorizer group is a collection of user(s) that
     can provide authorization on behave of a particular group. The membership is determined using certain functions.
     The set of membership functions can modified as required.

     A key component in the authorization state chart is the Authorization Stage states. These states act as checkpoints
     during an authorization flow.

     There are two type of modes that control the behaviour of the authorization stages. Global and Local. Global sees
     all the authorizer groups pooled into one global authorization pool. Local sees authorizer groups associated with
     with each authorizer stage.

     The authorizer groups that can authorize in these two different modes can be established via the FParameters.
     Likewise the mode can also be set via the FParameters.
    
    AUTHOR
    
    
    DATE CREATED
        
"""

import acm

from GenericMandatesAuthorizationCore import isUpdateAuthorization, \
    getNewMandatePropertiesFromBusinessProcess, getMandateFromMandateTextObject, \
    areNewMandatePropertiesSetForBusinessProcess, GetAuthGroup
from GenericMandatesLogger import getLogger
from ABSAMailer import GetAfricaSupervisorGroupEmails, GetMandatedTradersEmails, GetProductSupervisorsEmails, \
    SendMandateAuthorizedMail, SendMandateCreatedMail, SendMandateAmendedMail, SendMandateRejectedMail
from GenericMandatesDefinition import Mandate
from GenericMandatesUtils import GetMandateSettingsParam


def _GetLoggedOnUser():
    return acm.FACMServer().User().Name()  # pylint: disable=no-member


def _CopySteps(context, additional_params_to_add_in_diary = None):
    """
    Copy the Parameters from one Business Process Step to the next when a state transition takes place.
    :param context: FBusinessProcessCallbackContext
    """
    try:
        if context.CurrentStep().IsInfant() is False:
            getLogger().debug('[STATE] Copy states')
            steps = context.CurrentStep().BusinessProcess().Steps()

            sourceStep = context.CurrentStep()
            sourceDiary = sourceStep.DiaryEntry()

            # Copy notes
            notes = sourceDiary.Notes()
            if notes:
                for note in notes:
                    context.AddNote('%s\n' % note)

            # Copy parameters
            parameters = sourceDiary.Parameters()
            contextTargetParameters = context.Parameters()
            keys = parameters.Keys()
            if keys:
                for key in keys:
                    getLogger().debug('Field: %s %s => %s' % (key, parameters[key], contextTargetParameters[key]))
                    contextTargetParameters[key] = parameters[key]

            # Add additional params passed into the function
            if additional_params_to_add_in_diary:
                for key in additional_params_to_add_in_diary:
                    contextTargetParameters[key] = additional_params_to_add_in_diary[key]

    except Exception as e:
        getLogger().error('[ERROR] Exception Occurred: %s' % e)


def CreateOrigName(tempQfName):
    return '%s%s' % (tempQfName[:8], tempQfName[13:])


def CopyQueryFolderToOriginal(tempQfName):
    """
    Create a copy of the query folder. If a query folder with the target name already exists, it will be deleted.
    :param tempQfName: FStoredASQLQuery
    :return: FStoredASQLQuery
    """
    originalQfName = CreateOrigName(tempQfName)
    tempQf = acm.FStoredASQLQuery[tempQfName]  # pylint: disable=no-member
    # originalQf = acm.FStoredASQLQuery[originalQfName]

    # Apply changes from temporary Query Folder to original Query Folder
    clone = tempQf.Clone()
    clone.Name(originalQfName)

    # Remove existing query folders with the same name
    existing = acm.FStoredASQLQuery.Select('name="%s"' % originalQfName)  # pylint: disable=no-member
    for queryFolder in existing:
        queryFolder.Delete()

    # Commit the temp query folder to replace the original one
    clone.Commit()
    return clone


#FBusinessProcessCallbackContext callback handlers:
#-----------------------------------------------------------------------------------
# The context parameter is an instance of FBusinessProcessCallbackContext

# Conditions return True or False
#
# Name convention is
# 'condition_' + 'entry_'/'exit_' + 'state_' + state name in lowercase and underscore
#-----------------------------------------------------------------------------------
def on_entry_state_authorization_stage_1(context):
    """
    Product Supervisor authorization stage
    :param context:
    :return: bool
    """    
    _CopySteps(context)
    return True


def on_entry_state_rejected(context):
    disableMail = False
    _CopySteps(context)
    contextTarget = context.Parameters()
    if 'Mandate Change Reason' in contextTarget.Keys():
        reason = contextTarget['Mandate Change Reason']
        
        if 'Recertification of mandate.' in reason:
            disableMail = True
        
    textObject = context.Subject()
    limit = acm.FLimit[textObject.Name()]
    if limit and disableMail is False:
        mandate = Mandate(limit)
        mailTo = GetAfricaSupervisorGroupEmails()
        
        SendMandateRejectedMail(mandate, mailTo, 'Front Arena - Mandates')
    else:
        getLogger().debug('Mailing disabled for this step. Not sending mail')
    return True


def on_entry_state_authorized(context):

    try:
        # add the authoriser details to the business process diary
        # and copy params from previous step onto the 'to' step.
        authoriser_params = {}
        authoriser_params['Authorizer Group'] = GetAuthGroup()
        authoriser_params['Authorizer'] = _GetLoggedOnUser()

        _CopySteps(context, authoriser_params)

    except Exception as e:
        getLogger().error('[ERROR] Exception Occurred: %s' % e)


def on_entry_state_active(context):
    """
    Authorized state on entry function. Handles the updating of the mandate in the following 3 cases:
    Creation request - Set as active only
    Activation request - Set as active and updates mandate
    Update request - Update mandate
    :param context: FBusinessProcessCallbackContext
    :return:
    """
    getLogger().debug("on_entry_state_active() executing")

    # Copy parameters between business process steps
    _CopySteps(context)
        
    businessProcess = context.CurrentStep().BusinessProcess()
    oldMandate = context.Subject()
    areNewMandateParametersSet = areNewMandatePropertiesSetForBusinessProcess(businessProcess)

    # If update authorization
    if isUpdateAuthorization(businessProcess):
        getLogger().debug("Update existing mandate authorization")

        # If the new mandate properties are set and if the subject is a text object
        if areNewMandateParametersSet and oldMandate.IsKindOf(acm.FCustomTextObject):  # pylint: disable=no-member
            getLogger().debug("Mandate '%s' authorization complete. Updating mandate..." % oldMandate.Name())
            try:
                # Get current mandate
                currentMandate = getMandateFromMandateTextObject(oldMandate)

                # Get new mandate properties to update current mandate with
                mandateTarget, mandateType, queryFolders, blocking, active, reason = getNewMandatePropertiesFromBusinessProcess(
                    businessProcess)

                # Copy temporary query folders to original ones
                # updatedQueryFolders = [CopyQueryFolderToOriginal(queryFolder.Name()) for queryFolder in queryFolders]
                updatedQueryFolders = queryFolders

                # Update current mandate with the new mandate properties
                getLogger().debug('Updating Auth Timestamp on Mandate')
                currentMandate.SetAuthTime(acm.Time.TimeNow())  # pylint: disable=no-member
                currentMandate.SetAuthUser(acm.User().Name())  # pylint: disable=no-member
                currentMandate.SetEntity(mandateTarget)
                currentMandate.SetType(mandateType)
                currentMandate.SetBlocking(blocking)
                currentMandate.SetMandateAsActive() if active is True else currentMandate.SetMandateAsInactive()
                currentMandate.ClearAcceptedTraders()

                currentMandate.UnlinkQueryFolders()
                for folder in updatedQueryFolders:
                    currentMandate.LinkQueryFolder(folder)

                # Save all changes to mandate
                currentMandate.Commit()

                # Apply mandate to Limit
                currentMandate.ApplyMandateToLimit()
                
                # Send e-mail notification to Africa Supervisor Group & Mandated Traders
                getLogger().info('Send notification e-mail to Africa Supervisor group & Mandated Traders')
                mailTo = GetAfricaSupervisorGroupEmails()
                mailTo += GetMandatedTradersEmails(currentMandate)
                mailTo += GetProductSupervisorsEmails(currentMandate)
                SendMandateAmendedMail(currentMandate, mailTo, 'Front Arena - Mandates')
                getLogger().info('e-mails sent')

            except Exception as e:
                # Errors will move the state chart into and exception state. So the authorizer group should be removed
                # to allow reverting
                getLogger().error('-'*60)
                import sys
                import traceback
                traceback.print_exc(file=sys.stdout)
                getLogger().error('-'*60)

                raise e
        else:
            raise Exception("New mandate properties not found")

    # If creation/activation authorization
    else:
        getLogger().debug("New mandate authorization")
        try:
            # Get mandate object in question
            currentMandate = getMandateFromMandateTextObject(oldMandate)
            getLogger().debug("New mandate parameters are set")

            # Get new mandate properties to update current mandate with
            mandateTarget, mandateType, queryFolders, blocking, active, reason = getNewMandatePropertiesFromBusinessProcess(
                businessProcess)

            # Copy temporary copy folders to originals
            # updatedQueryFolders = [CopyQueryFolderToOriginal(queryFolder.Name()) for queryFolder in queryFolders]
            updatedQueryFolders = queryFolders

            # Update mandate properties and commit changes
            getLogger().debug('Updating Auth Timestamp on Mandate')
            currentMandate.SetAuthTime(acm.Time.TimeNow())  # pylint: disable=no-member
            currentMandate.SetAuthUser(acm.User().Name())  # pylint: disable=no-member
            currentMandate.SetEntity(mandateTarget)
            currentMandate.SetType(mandateType)
            currentMandate.SetBlocking(blocking)
            currentMandate.SetMandateAsActive() if active is True else currentMandate.SetMandateAsInactive()

            currentMandate.UnlinkQueryFolders()
            for folder in updatedQueryFolders:
                currentMandate.LinkQueryFolder(folder)

            # Save changes to mandate
            currentMandate.Commit()

            # Apply mandate to limit
            currentMandate.ApplyMandateToLimit()

            # Send e-mail notification to Africa Supervisor Group & Mandated Traders
            getLogger().info('Send notification e-mail to Africa Supervisor group & Mandated Traders')
            mailTo = GetAfricaSupervisorGroupEmails()
            mailTo += GetMandatedTradersEmails(currentMandate)
            mailTo += GetProductSupervisorsEmails(currentMandate)
            SendMandateAmendedMail(currentMandate, mailTo, 'Front Arena - Mandates')
            getLogger().info('e-mails sent')
            
        except Exception as e:
            message = "Error: Failed to make mandate '%s' active. Due to exception %s" % (oldMandate.Name(), e.message)
            # Errors will move the state chart into and exception state. So the authorizer group should be removed
            # to allow reverting
            getLogger().error('-'*60)
            import sys
            import traceback
            getLogger().error('%s' % message)
            traceback.print_exc(file=sys.stdout)
            getLogger().error('-'*60)
            raise e
