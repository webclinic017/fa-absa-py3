"""
This module is only accessed from the Menu Extension(s).

All the functions in this module are the entry points executed from FMenuExtensions.

---------------------------------------------------------------------------------------------------
28-08-2018      Jaysen Naicker          amend method ApproveMandateMenuItem to update limit when mandate is updated
"""

import acm
import FUxCore  # pylint: disable=import-error

from GenericMandatesLogger import getLogger
from GenericMandatesCreateMandateGUI import DialogEditMandate
from GenericMandatesDefinition import Mandate, GetMandateTypes, GetAllMandateLimitOids
from GenericMandatesPredealCheckDialog import MandateSelectMandateTypesDialog
from GenericMandatesAuthorizationCore import EVENT_PARAMETER_REJECTION_REASON, EVENT_PARAMETER_REJECTION_USER, \
    loadMandateCustomTextObject, getNewMandatePropertiesFromBusinessProcess, isUpdateAuthorization, \
    extractParametersDictionaryFromFParameters, EXTENSION_CONTEXT_NAME, FPARAMETER_MANDATE_AUTHORIZATION_PARAMETERS
from GenericMandatesAuthorizationStateChart import StateChartAuthorizationProcess
from GenericMandatesAuthorizationApi import requestMandateUpdateAuthorization
from GenericMandatesTreeViewCompare import DialogTreeViewCompare, CreateTreeViewDialogLayout
from GenericMandatesAuthorizationLocal import localAuthoriseMandateWithCurrentUser, \
    localFindAuthorizationStageAuthorizerGroupMap
from GenericMandatesAuthorizationCore import AUTHORIZATION_MODE_LOCAL
from GenericMandatesUtils import GetMandateSettingsParam


def OnCreateMenuViewMandate(eii):
    """
    Executed when the menu item "View Mandate" is created.
    :param eii: FExtensionInvokationInfo
    :return: FExtensionInvokationInfo
    """
    del eii
    getLogger().debug("OnCreateMenuViewMandate() executed")
    

def OnClickMenuViewMandate(eii):
    """
    Executed when the user clicks on the "View Mandate" menu button. The edit mandate dialog is then displayed to the
    user.
    :param eii: FExtensionInvokationInfo
    """
    getLogger().debug("OnClickMenuViewMandate() executed")
    opsManager = eii.ExtensionObject()

    if not opsManager.Class() == acm.FBackOfficeManagerFrame:  # pylint: disable=no-member
        return

    # Get limit from selected cell
    sheet = opsManager.ActiveSheet()
    if sheet:
        selection = sheet.Selection()
        selectedCell = selection.SelectedCell()
        selectedObject = selectedCell.BusinessObject()
        mandate = None

        # Load mandate
        if "RecordType" in dir(selectedObject):
            if selectedObject.RecordType() == "Limit":
                # Limit Sheet
                mandate = Mandate(selectedObject)
            if selectedObject.RecordType() == "BusinessProcess":

                if selectedObject.Subject_type() == "TextObject":
                    # Business Process Sheet (Authorizations)
                    limit = acm.FLimit[selectedObject.Subject().Name()]  # pylint: disable=no-member
                    mandate = Mandate(limit)
                elif selectedObject.Subject_type() == "Limit":
                    # Business Process Sheet (Violations)
                    mandate = Mandate(selectedObject.Subject())

            limit = acm.FLimit[selectedObject.Name()]  # pylint: disable=no-member
            if limit:
                mandate = Mandate(limit)

            # Display dialog
            dialog = DialogEditMandate(mandate)
            # pylint: disable=no-member
            acm.UX().Dialogs().ShowCustomDialogModal(acm.UX().SessionManager().Shell(), dialog.CreateLayout(), dialog)


def OnClickTestTradeOnMandate(eii):
    """
    :param eii: FExtensionInvokationInfo
    :return:
    """
    originalTrader = None
    modified_trade = eii.ExtensionObject().EditTrade()
    modified_trade.Touch()
    
    # If logged in user is not the same as trader
    if modified_trade.Trader().Name() != acm.User().Name():
        originalTrader = modified_trade.Trader()
        modified_trade.Trader(acm.User())

    # pylint: disable=no-member
    shell = acm.UX().SessionManager().Shell()
    mandateTypes = GetMandateTypes()

    # Check mandate types
    dialog = MandateSelectMandateTypesDialog(modified_trade, shell, mandateTypes)
    acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog)

    # If logged in user is not the same as trader
    if originalTrader:
        modified_trade.Trader(originalTrader)
    

def OnClickMenuViewBreachedMandate(eii):
    """
    Executed when the user clicks on the "View Mandate" menu button. The edit mandate dialog is then displayed to the
    user.
    :param eii: FExtensionInvokationInfo
    """
    getLogger().debug("OnClickMenuViewBreachedMandate() executed")
    opsManager = eii.ExtensionObject()

    if not opsManager.Class() == acm.FBackOfficeManagerFrame:  # pylint: disable=no-member
        return

    # Get business process from selected cell
    sheet = opsManager.ActiveSheet()
    if sheet:
        selection = sheet.Selection()
        selectedCell = selection.SelectedCell()
        process = selectedCell.BusinessObject()


def OnClickViewHistoricalTrade(bp):
    """
    This method is executed when the user clicks on the "Mandates / View Trade" button. It will display an instrument
    dialog of the trade stored in the business process with the specific historical version number stored in transaction
    history.
    :param eii: FExtensionInvokationInfo
    :return:
    """
    getLogger().debug("GetHistoricalTrade() executed")

    # Get the optional key & trade version of the trade stored in the business process
    optionalKey = bp.CurrentStep().DiaryEntry().Parameters().At('TradeOptionalKey')
    version = bp.CurrentStep().DiaryEntry().Parameters().At('TradeVersion')
    trade = acm.FTrade.Select01('optionalKey="%s"' % optionalKey, "No trade exists for optional key (%s)" % optionalKey)

    # Retrieve the historical trade and view using the instrument dialog
    tradeNumber = trade.Oid()

    # Retrieve historical trade using AMBA message stored in Text Object
    from GenericMandatesViolation import GetTradeFromViolation
    trade, ins = GetTradeFromViolation(bp)
    del ins
    acm.StartApplication("Instrument Definition", trade)  # pylint: disable=no-member
    return None


class ViewTradeMenuItem(FUxCore.MenuItem):
    """
    MenuItem on Business Process Sheet used to view a historical version of a specific breached mandate.
    """
    def __init__(self, extObj):
        self._frame = extObj
        self._bp = None
        self._shell = self._frame.Shell()
        self.SetUp()

    def SetUp(self):
        """
        Setting up the menu.
        """
        getLogger().debug("SetUp() executed")
        opsManager = self._frame
        if not opsManager.Class() == acm.FBackOfficeManagerFrame:  # pylint: disable=no-member
            return

        # Get business process from selected cell
        sheet = opsManager.ActiveSheet()
        if sheet:
            selection = sheet.Selection()
            if not sheet.Selection() or not sheet.Selection().SelectedCell():
                return  
            selectedCell = selection.SelectedCell()
            self._bp = selectedCell.BusinessObject()

    def Invoke(self, eii):
        """
        OnClick method that executes when the menu item is clicked.
        :param eii: FExtensionInvokationInfo
        """
        del eii
        OnClickViewHistoricalTrade(self._bp)

    def Applicable(self):
        """
        Method that returns a boolean indicating if the item should be visible or not.
        :return: bool
        """
        if 'StateChart' in dir(self._bp):
            if self._bp.StateChart().Name() == 'GenericMandates_ViolationStates':
                return True
        return False

    def _IsUserAllowedToAuthorise(self):
        """
        Generic authorization stage state exit condition function. This functions checks if the user can authorize
        :return: Boolean
        """
        getLogger().debug('Executing - IsUserAllowedToAuthorise()')

        parameter = extractParametersDictionaryFromFParameters(EXTENSION_CONTEXT_NAME,
                                                               FPARAMETER_MANDATE_AUTHORIZATION_PARAMETERS)
        mode = parameter['AuthorizationMode']
        stageNumber = int(self._bp.CurrentStep().State().Name()[-1:])
        doesUserHavePermission = False

        if mode == AUTHORIZATION_MODE_LOCAL:
            getLogger().debug('SEQUENTIAL Authorization mode')
            doesUserHavePermission = localAuthoriseMandateWithCurrentUser(stageNumber)
            authMap = localFindAuthorizationStageAuthorizerGroupMap(EXTENSION_CONTEXT_NAME, stageNumber)
        else:
            getLogger().debug('NONSEQUENTIAL Authorization mode')

            # Retrieve a list of groups (states) already authorized
            from GenericMandatesAuthorizationGlobal import IsUserAllowedToAuthorise
            doesUserHavePermission, authMaps = IsUserAllowedToAuthorise(self._bp)

        if doesUserHavePermission is not True:
            doesUserHavePermission = "You do not have the necessary permissions to approve/deny mandates."
        return doesUserHavePermission

    def _ShowMessageBoxInformation(self, message):
        """
        Display a dialog with a message and a single 'OK' button.
        :param message: string - Message to display
        :return: None
        """
        acm.UX().Dialogs().MessageBoxInformation(self._shell, message)  # pylint: disable=no-member


class ApproveMandateMenuItem(ViewTradeMenuItem):
    """
    MenuItem on Business Process Sheet used to view a historical version of a specific breached mandate.
    """
    def _Approve(self):
        """
        Approve the mandate.
        """
        self._bp.HandleEvent(StateChartAuthorizationProcess.EVENT_APPROVE)
        self._bp.Commit()
        
        # update limit details to be in line with the manade changes.
        limitOid = self._bp.Subject().Name()
        limit = acm.FLimit[limitOid]
        mandate = Mandate(limit)
        limit.Name(mandate.Name())
        limit.LimitTarget().TemplatePath(self._bp.CurrentStep().DiaryEntry().Parameters()['Mandate target'])
        limit.Commit()
        
    def Invoke(self, eii):
        """
        OnClick method that executes when the menu item is clicked.
        :param eii: FExtensionInvokationInfo
        """
        del eii

        if self._IsUserAllowedToAuthorise() is True:
            self._Approve()
        else:
            getLogger().debug("Not allowed to authorise.")
            self._ShowMessageBoxInformation(self._IsUserAllowedToAuthorise())

    def Enabled(self):
        """
        Enable or disable menu item.
        :return: bool
        """
        validEvents = self._bp.CurrentStep().ValidEvents()
        for validEvent in validEvents:
            if 'Approve' in validEvent.Name():
                return True
        return False

    def Applicable(self):
        """
        Method that returns a boolean indicating if the item should be visible or not.
        :return: bool
        """
        if 'StateChart' in dir(self._bp):
            if self._bp.StateChart().Name() == StateChartAuthorizationProcess.NAME:
                return True
        return False


class DenyMandateMenuItem(ViewTradeMenuItem):
    """
    MenuItem on Business Process Sheet used to view a historical version of a specific breached mandate.
    """
    def _Deny(self, eii):
        """
        Deny the mandate. This method captures the reason why the user denied / rejected the specific mandate. It
        pops up a display prompting the user to capture a comment.
        :param eii: FExtensionInvokationInfo
        """
        shell = eii.Parameter('shell')
        dialogCaption = "Capture rejection reason"
        initialComment = "My reason for rejecting the authorization process."
        reason = acm.UX().Dialogs().GetTextInput(shell, dialogCaption, initialComment)  # pylint: disable=no-member

        if reason and len(reason) > 0:
            # A reason was supplied
            parameters = acm.FDictionary()  # pylint: disable=no-member
            parameters.AtPut(EVENT_PARAMETER_REJECTION_REASON, reason)
            # pylint: disable=no-member
            parameters.AtPut(EVENT_PARAMETER_REJECTION_USER, acm.FACMServer().User().Name())

            self._bp.HandleEvent(StateChartAuthorizationProcess.EVENT_DENY, parameters)
            self._bp.Commit()
        elif reason and len(reason) == 0:
            # No reason was supplied - display a notification
            # pylint: disable=no-member
            acm.UX().Dialogs().MessageBoxInformation(shell, 'No reason was supplied. The Authorization will not be '
                                                            'rejected. \nPlease try again.')

    def Invoke(self, eii):
        """
        OnClick method that executes when the menu item is clicked.
        :param eii: FExtensionInvokationInfo
        """
        if self._IsUserAllowedToAuthorise() is True:
            self._Deny(eii)
        else:
            getLogger().debug("Not allowed to authorise.")
            self._ShowMessageBoxInformation(self._IsUserAllowedToAuthorise())

    def Enabled(self):
        """
        Enable or disable the menu item.
        :return: bool
        """
        from GenericMandatesConstants import OPERATION_AUTHORIZE
        # pylint: disable=no-member
        if acm.User().IsAllowed(OPERATION_AUTHORIZE, 'Operation'):
            validEvents = self._bp.CurrentStep().ValidEvents()
            for validEvent in validEvents:
                if 'Reject' in validEvent.Name():
                    return True
        return False

    def Applicable(self):
        """
        Method that returns a boolean indicating if the item should be visible or not.
        :return: bool
        """
        if 'StateChart' in dir(self._bp):
            if self._bp.StateChart().Name() == StateChartAuthorizationProcess.NAME:
                return True
        return False


class ApplyMandateMenuItem(ViewTradeMenuItem):
    """
    MenuItem on Business Process Sheet used to view a historical version of a specific breached mandate.
    """
    def _Apply(self):
        """
        Approve the mandate.
        """
        self._bp.HandleEvent(StateChartAuthorizationProcess.EVENT_SAVE_MANDATE)
        self._bp.Commit()
        

    def Invoke(self, eii):
        """
        OnClick method that executes when the menu item is clicked.
        :param eii: FExtensionInvokationInfo
        """
        del eii
        self._Apply()

    def Enabled(self):
        """
        Enable or disable menu item.
        :return: bool
        """
        from GenericMandatesConstants import OPERATION_SAVE, FPARAM_LIMIT_OWNER

        # Check if logged on user is the System User (ATS user)
        # pylint: disable=no-member
        if acm.User().Name() == str(GetMandateSettingsParam(FPARAM_LIMIT_OWNER)):
            if acm.User().IsAllowed(OPERATION_SAVE, 'Operation'):
                validEvents = self._bp.CurrentStep().ValidEvents()
                for validEvent in validEvents:
                    if StateChartAuthorizationProcess.EVENT_SAVE_MANDATE in validEvent.Name():
                        return True
        return False

    def Applicable(self):
        """
        Method that returns a boolean indicating if the item should be visible or not.
        :return: bool
        """
        if 'StateChart' in dir(self._bp):
            if self._bp.StateChart().Name() == StateChartAuthorizationProcess.NAME:
                return True
        return False


class StatusMandateMenuItem(FUxCore.MenuItem):
    """
    MenuItem on Business Process Sheet used to view a historical version of a specific breached mandate.
    """
    def __init__(self, extObj):
        self._frame = extObj
        self._limit = None
        self._mandate = None
        self.__shell = self._frame.Shell()
        self.SetUp()

    def SetUp(self):
        """
        Setting up the menu.
        """
        getLogger().debug("Status Menu Item - SetUp() executed")
        opsManager = self._frame

        if not opsManager.Class() == acm.FBackOfficeManagerFrame:  # pylint: disable=no-member
            getLogger().debug('Not a Back Office worksheet.')
            return

        # Get limit from selected cell
        sheet = opsManager.ActiveSheet()
        if not sheet:
            return
          
        selection = sheet.Selection()
        selectedCell = selection.SelectedCell()
        self._limit = selectedCell.BusinessObject()

        # Load mandate
        if "RecordType" in dir(self._limit):
            if self._limit.RecordType() == "Limit":
                self._mandate = Mandate(self._limit)
            else:
                getLogger().debug('Not a Limit object in selected row. Type: %s' % self._limit.RecordType())
        else:
            getLogger().debug('Not a Limit object in selected row. No RecordType method.')

    def ToggleMandate(self, enable):
        """
        Toggle the enabled state of the mandate (limit).
        :param enable: bool
        """
        msg = "Are you sure you want to enable / disable this Mandate? \n\nThis will follow the same authorization " \
              "process as updating mandates."
        if self._MessageBoxYesNo("Question", msg) is True:
            getLogger().debug('Disable mandate (%s)' % self._mandate.LimitOid())

            reason = self._MessageBoxPromptText('Reason for toggling Mandate', 'This is the reason for requesting the '
                                                                               'change.')
            if reason and len(reason) > 0:
                mandateTextObject = loadMandateCustomTextObject(self._mandate.LimitOid())
                requestMandateUpdateAuthorization(mandateTextObject, '%s' % self._mandate.Entity(),
                                                  self._mandate.Type(), self._mandate.QueryFoldersObj(),
                                                  self._mandate.IsBlocking(), enable, reason)
            else:
                getLogger().info('No reason supplied')
                self._ShowMessageBoxInformation('The mandate will not be toggled. No reason was supplied to attach '
                                                'to the authorization process.\n\nPlease try again and supply a '
                                                'reason.')

    def RenewMandate(self):
        """
        Renew a mandate - kick off the renewal process for a mandate. This will disable and enable a mandate.
        """
        msg = "Are you sure you want to recertify this Mandate? \n\nThis will follow the same authorization " \
              "process as updating mandates."
        if self._MessageBoxYesNo("Question", msg) is True:
            getLogger().debug('Recertify mandate (%s)' % self._mandate.LimitOid())

            reason = 'Recertification of mandate.'
            mandateTextObject = loadMandateCustomTextObject(self._mandate.LimitOid())
            requestMandateUpdateAuthorization(mandateTextObject, '%s' % self._mandate.Entity(),
                                              self._mandate.Type(), self._mandate.QueryFoldersObj(),
                                              self._mandate.IsBlocking(), False, reason)
            requestMandateUpdateAuthorization(mandateTextObject, '%s' % self._mandate.Entity(),
                                              self._mandate.Type(), self._mandate.QueryFoldersObj(),
                                              self._mandate.IsBlocking(), True, reason)

    def _MessageBoxYesNo(self, title, message):
        """
        Display a dialog showing a message with a 'Yes' and a 'No' button.
        :param title: string - Title of the dialog
        :param message: string - Message of the dialog
        :return: boolean
        """
        answer = acm.UX().Dialogs().MessageBoxYesNo(self._frame.Shell(), title, message)  # pylint: disable=no-member
        if answer == 'Button1':
            return True
        return False

    def _MessageBoxPromptText(self, caption, initialText):
        """
        Display a dialog prompting the user to type in a reason for requesting a Mandate change.
        :param caption:
        :param initialText:
        :return: string
        """
        msg = acm.UX().Dialogs().GetTextInput(self.__shell, caption, initialText)  # pylint: disable=no-member
        if msg:
            # Check if the user clicked on Cancel
            return msg

    def _ShowMessageBoxInformation(self, message):
        """
        Display a dialog with a message and a single 'OK' button.
        :param message: string - Message to display
        :return: None
        """
        acm.UX().Dialogs().MessageBoxInformation(self.__shell, message)  # pylint: disable=no-member


class DisableMandateMenuItem(StatusMandateMenuItem):
    """
    MenuItem on Business Process Sheet used to view a historical version of a specific breached mandate.
    """
    def Invoke(self, eii):
        """
        OnClick method that executes when the menu item is clicked.
        :param eii: FExtensionInvokationInfo
        """
        del eii

        self.ToggleMandate(False)

    def Enabled(self):
        """
        Method that returns a boolean indicating if the item should be visible or not.
        :return: bool
        """
        from GenericMandatesConstants import OPERATION_MODIFY
        if acm.User().IsAllowed(OPERATION_MODIFY, 'Operation'):  # pylint: disable=no-member
            if self._mandate:
                return True if self._mandate.Status() == 'active' else False
        else:
            return False


class EnableMandateMenuItem(StatusMandateMenuItem):
    """
    MenuItem on Business Process Sheet used to view a historical version of a specific breached mandate.
    """
    def Invoke(self, eii):
        """
        OnClick method that executes when the menu item is clicked.
        :param eii: FExtensionInvokationInfo
        """
        del eii
        self.ToggleMandate(True)

    def Enabled(self):
        """
        Method that returns a boolean indicating if the item should be visible or not.
        :return: bool
        """
        from GenericMandatesConstants import OPERATION_MODIFY
        if acm.User().IsAllowed(OPERATION_MODIFY, 'Operation'):  # pylint: disable=no-member
            if self._mandate:
                return True if self._mandate.Status() == "inactive" else False
        else:
            return False


class RenewMandateMenuItem(StatusMandateMenuItem):
    """
    MenuItem on Business Process Sheet used to renew a mandate.
    """
    def Invoke(self, eii):
        """
        OnClick method that executes when the menu item is clicked.
        :param eii: FExtensionInvokationInfo
        """
        del eii
        self.RenewMandate()

    def Enabled(self):
        """
        Method that returns a boolean indicating if the item should be visible or not.
        :return: bool
        """
        from GenericMandatesConstants import OPERATION_MODIFY
        if acm.User().IsAllowed(OPERATION_MODIFY, 'Operation'):  # pylint: disable=no-member
            if self._mandate:
                return True if self._mandate.Status() == 'active' else False
        else:
            return False


class ViewProposedChangesMenuItem(ViewTradeMenuItem):
    """
    MenuItem on Business Process Sheet used to view a historical version of a specific breached mandate.
    """
    def _Apply(self):
        """
        Approve the mandate.
        """
        getLogger().debug('ViewProposedChangesMenuItem - _Apply()')

        # Retrieve Mandate / Limit ID
        limitOid = self._bp.Subject().Name()

        # Retrieve existing mandate properties
        mandate = Mandate(acm.FLimit[limitOid])  # pylint: disable=no-member
        existing = {'Blocking': mandate.IsBlocking(),
                    'Entity': mandate.Entity(),
                    'Entity Type': mandate.Type(),
                    'Active': True if mandate.Status() == 'active' else False,
                    'queries': mandate.QueryFoldersObj()}

        # Retrieve proposed mandate properties
        mandateProperties = getNewMandatePropertiesFromBusinessProcess(self._bp)

        proposed = {'Blocking': mandateProperties[3],
                    'Entity': mandateProperties[0],
                    'Entity Type': mandateProperties[1],
                    'Active': mandateProperties[4],
                    'queries': mandateProperties[2]}

        # Display dialog
        comment = mandateProperties[5]
        builder = CreateTreeViewDialogLayout()
        readOnly = self._IsUserAllowedToAuthorise() != True
        customDlg = DialogTreeViewCompare(existing, proposed, self._bp, comment, readOnly)
        acm.UX().Dialogs().ShowCustomDialogModal(self._shell, builder, customDlg)  # pylint: disable=no-member

    def Invoke(self, eii):
        """
        OnClick method that executes when the menu item is clicked.
        :param eii: FExtensionInvokationInfo
        """
        self._shell = eii.Parameter('shell')
        self._Apply()

    def Enabled(self):
        """
        Enable or disable menu item.
        :return: bool
        """
        if isUpdateAuthorization(self._bp) is True:
            validEvents = self._bp.CurrentStep().ValidEvents()
            for validEvent in validEvents:
                if 'Reject' in validEvent.Name():
                    return True
        return False

    def Applicable(self):
        """
        Method that returns a boolean indicating if the item should be visible or not.
        :return: bool
        """
        if 'StateChart' in dir(self._bp):
            if self._bp.StateChart().Name() == StateChartAuthorizationProcess.NAME:
                validEvents = self._bp.CurrentStep().ValidEvents()
                setA = {'Reject', 'Approve'}
                setB = {event.Name() for event in validEvents}
                if setA <= setB:
                    return True
        return False


def CreateViewTradeMenuItem(eii):
    """
    Return invocation object.
    :param eii: FExtensionInvokationInfo
    :return: FExtensionInvokationInfo
    """
    return ViewTradeMenuItem(eii)


def OnClickSearch(eii):
    """
    On Click event handler for the search button.
    :param eii: FExtensionInvokationInfo
    """
    # pylint: disable=no-member
    del eii
    getLogger().info('__OnClickSearch() executing')
    mandateNames = acm.FArray()
    limitOids = GetAllMandateLimitOids()

    for limitOid in limitOids:
        limit = acm.FLimit[limitOid]
        if limit:
            mandateNames.Add(limit.Name())

    selected = acm.UX().Dialogs().SelectObject(acm.UX().SessionManager().Shell(),
                                               "Select mandate",
                                               "Mandate description",
                                               mandateNames,
                                               "A")
    if selected:
        mandate = Mandate(acm.FLimit[selected])
        # Display mandate
        dialog = DialogEditMandate(mandate)
        acm.UX().Dialogs().ShowCustomDialogModal(acm.UX().SessionManager().Shell(), dialog.CreateLayout(), dialog)
