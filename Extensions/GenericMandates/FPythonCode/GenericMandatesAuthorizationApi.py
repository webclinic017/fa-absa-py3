import acm

from GenericMandatesAuthorizationCore import isStateNameThatOfAuthorisationStage, extractAuthorisationStageNumber, \
    getNumberOfAuthorizationStages, getCurrentStateName, setMandatePropertiesInEventParameters, \
    isUpdateAuthorization, isAuthorizationAuthorized, isAuthorizationRejected, \
    isAuthorizationError
from GenericMandatesAuthorizationStateChart import StateChartAuthorizationProcess
from GenericMandatesLogger import getLogger
from GenericMandatesAuthorizationCore import EVENT_PARAMETER_REJECTION_REASON, EVENT_PARAMETER_REJECTION_USER
from GenericMandatesDefinition import Mandate


def getAuthorizationBusinessProcessForMandate(mandateTextObject):
    """
    Get the authorization business process for the mandate text object
    :param mandateTextObject: FPersistentTextObject
    :return: FBusinessProcess
    """
    stateChart = acm.FStateChart[StateChartAuthorizationProcess.NAME]

    if stateChart:
        businessProcesses = acm.BusinessProcess.FindBySubjectAndStateChart(mandateTextObject, stateChart)

        getLogger().debug("Business process %s" % businessProcesses)
        if len(businessProcesses) > 0:
            return businessProcesses[0]

    return None


def requestMandateCreationAuthorization(mandateTextObject, entityType, folders, blocking, entity, reason,
                                        mandateName, description):
    """
    Requests that the authorization business process is created for the mandate and that it is moved into activation.
    This should be called only once per mandate
    :param mandateTextObject: FPersistentTextObject
    :param entityType:
    :param folders:
    :param blocking:
    :param entity:
    :param reason:
    :param mandateName:
    :param description:

    :return: True if request was successful else false
    """
    # pylint: disable=no-member
    # Get the state chart for mandate authorization
    stateChart = acm.FStateChart[StateChartAuthorizationProcess.NAME]

    # If it exists
    if stateChart:
        businessProcess = getAuthorizationBusinessProcessForMandate(mandateTextObject)
        if not businessProcess:
            getLogger().debug("Requesting creation authorization for mandate %s" % entity)
            # Initialize a new authorization business process for the mandate
            businessProcess = acm.BusinessProcess.InitializeProcess(mandateTextObject, stateChart)
            bpParameters = acm.FDictionary()
            setMandatePropertiesInEventParameters(bpParameters, entity, entityType, folders, blocking, True, reason)
            businessProcess.Commit()

            limit = acm.FLimit[mandateTextObject.Name()]
            mandate = Mandate(limit)

            folderNames = [qf.Name() for qf in folders]
            folderNames = ",".join(folderNames)
            mandate.SetProposed(True, entityType, entity, folderNames, mandateName, blocking, description)
            mandate.Commit()
            mandate.ApplyEntityToLimit()

            # Trigger create event
            businessProcess.HandleEvent(StateChartAuthorizationProcess.EVENT_CREATE, bpParameters)
            businessProcess.HandleEvent(StateChartAuthorizationProcess.EVENT_APPROVE, bpParameters)

            # Persist triggered event
            businessProcess.Commit()
            # If business process in error state
            if isAuthorizationError(businessProcess):
                getLogger().error("Error: Unknown error occurred in business process")
                getLogger().debug("Removing business process")
                # businessProcess.Delete()
                return False
            else:
                msg = "Creating authorization request for mandate %s was successful" % mandateTextObject.Name()
                getLogger().debug(msg)
                return True

        else:
            getLogger().error("Business process already exists for mandate %s" % mandateTextObject.Name())
            return False
    else:
        getLogger().error("State chart does not exist. Could not generate authorization business process.")
        return False


def MoveToRejectedState(bp):
    """
    Moves the current state of the business process to Rejected. This is only executed half-way through an authorization
    process if the user amends the mandate before the authorization process has completed 100 %.
    :param bp: FBusinessProcess
    :return:
    """
    params = acm.FDictionary()  # pylint: disable=no-member
    params.AtPut(EVENT_PARAMETER_REJECTION_USER, acm.FACMServer().User().Name())  # pylint: disable=no-member
    params.AtPut(EVENT_PARAMETER_REJECTION_REASON, 'User changed the mandate definition before the authorization '
                                                   'request was completed.')
    bp.HandleEvent(StateChartAuthorizationProcess.EVENT_DENY, params)
    # Persist triggered event
    bp.Commit()


def requestMandateUpdateAuthorization(mandateTextObject, mandateTarget, mandateType, queryFolders, blocking, active, reason):
    """
    Requests that the authorization business process enters a update approval flow. And stores the parameters in
    the event parameters for later usage if the updated is authorized.
    :param mandateTextObject: FPersistentTextObject
    :param mandateTarget: string
    :param mandateType: string
    :param queryFolders: list
    :param blocking: boolean
    :param active:
    :param reason:
    :return: True if request was successful else false
    """
    getLogger().debug("requestMandateUpdateAuthorization() executing")

    # Get the state chart for mandate authorization
    businessProcess = getAuthorizationBusinessProcessForMandate(mandateTextObject)
    if businessProcess:
        getLogger().debug("Requesting update authorization for mandate %s" % mandateTextObject.Name())
        allowedStates = [StateChartAuthorizationProcess.STATE_REJECTED, StateChartAuthorizationProcess.STATE_APPLY]
        # mandateStatus = getMandateFromMandateTextObject(mandateTextObject).Status()

        # Check if the Authorization Process is currently half-way through and cancel (Reject) it
        if getCurrentStateName(businessProcess) not in allowedStates:
            MoveToRejectedState(businessProcess)

            # TODO: Delete existing temp query folders

        if getCurrentStateName(businessProcess) in allowedStates:
            parameters = acm.FDictionary()  # pylint: disable=no-member
            setMandatePropertiesInEventParameters(parameters, mandateTarget, mandateType, queryFolders, blocking,
                                                  active, reason)

            # Trigger a submit update event
            businessProcess.HandleEvent(StateChartAuthorizationProcess.EVENT_SUBMIT_UPDATE, parameters)
            businessProcess.HandleEvent(StateChartAuthorizationProcess.EVENT_APPROVE, parameters)

            # Persist triggered event
            businessProcess.Commit()

            # If business process in error state
            if isAuthorizationError(businessProcess):
                errorMsg = "Error: Unknown error occurred in business process"
                getLogger().error(errorMsg)
                # Reverting from error
                businessProcess.HandleEvent(StateChartAuthorizationProcess.EVENT_REVERT)
                # Persist triggered event
                businessProcess.Commit()
                return errorMsg
            else:
                msg = "Update authorization request for mandate %s was successful" % mandateTextObject.Name()
                getLogger().debug(msg)
                return True

        else:
            errorMsg = "Error: Update cannot be requested since not in rejected/authorized state and/or mandate is " \
                       "inactive"
            getLogger().error(errorMsg)
            return errorMsg
    else:
        errorMsg = "Error: Business process does not exist for mandate %s" % mandateTextObject.Name()
        getLogger().error(errorMsg)
        return errorMsg


def getMandateAuthorizationStatus(mandate):
    """
    Query the change approval status of the mandate
    :param mandate: the mandate who needs to be queried. FPersistentTextObject
    :return: a status string if the business process exists else None
    """
    getLogger().debug("getMandateAuthorizationStatus() executing")

    acm.PollAllEvents()  # pylint: disable=no-member
    businessProcess = getAuthorizationBusinessProcessForMandate(mandate)
    # If the business process exists
    if businessProcess:
        # Get current state name
        currentStateName = getCurrentStateName(businessProcess)

        # Determine the number of approvals
        if isStateNameThatOfAuthorisationStage(currentStateName):
            approvalCounts = extractAuthorisationStageNumber(currentStateName) - 1
        else:
            approvalCounts = 0

        # Determine authorization flow
        # If the authorization flow is an update authorization
        if isUpdateAuthorization(businessProcess):
            changeType = "Mandate update request"
        else:
            changeType = "Mandate activation request"

        # Determine the status of the authorization
        if isAuthorizationAuthorized(businessProcess):
            state = " was authorized."
        elif isAuthorizationRejected(businessProcess):
            state = " was rejected."
        else:
            state = " is awaiting authorisation. %s/%s approvals received." % (approvalCounts,
                                                                               getNumberOfAuthorizationStages())

        return "%s%s (Business process '%s')" % (changeType, state, businessProcess.Oid())

    else:
        return None
