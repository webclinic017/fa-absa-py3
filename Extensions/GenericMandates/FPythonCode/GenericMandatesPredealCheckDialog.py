"""
Module containing most of the logic executed when a pre-deal check dialog is displayed to the trader.
"""

import acm
import FLimitMonitor  # pylint: disable=import-error
import FUxCore  # pylint: disable=import-error

from GenericMandatesLogger import getLogger
from GenericMandatesDefinition import Mandate
from GenericMandatesConstants import MANDATE_ALLOWED_TEXT, MANDATE_NOT_ALLOWED_TEXT, MANDATE_NOT_FOUND_TEXT
from GenericMandatesUtils import GetMandateSettingsParam, GetDefaultLimitsColumns, GetFailType, GetLimits, \
    GetReadOnlyLimitsColumns
from GenericMandatesViolation import CreateViolation
from GenericMandatesTreeView import CreateTreeViewDialogLayout, DialogTreeView


STATE_MAP = {"Breached": "Trade Not Allowed",
             "Warning": "Trade Not Allowed",
             "Active": "Trade Allowed",
             "Ready": "???",
             "No Mandate Found": "No Mandate Found"}

context = acm.GetDefaultContext()  # pylint: disable=no-member
calcSpace = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')  # pylint: disable=no-member


class MandateSelectMandateTypesDialog(object, FUxCore.LayoutDialog):
    """
    This is the dialog that pops up where the user is able to choose which mandate types to "test". The user can
    select which mandates using checkboxes for each one. By default all the checkboxes are checked.
    """
    def __init__(self, modified_trade, shell, mandateTypes):
        """
        Constructor
        :param modified_trade: FTrade
        :param shell: FUxShell
        :param mandateTypes: array
        """
        self._shell = shell
        self._modified_trade = modified_trade
        self._dialog = None
        self._mandateTypes = mandateTypes
        self._checkBoxes = {}

    def CreateLayout(self):
        """
        Create the layout for pre-deal check GUI.
        :return: FUxLayoutBuilder
        """
        getLogger().debug("CreateLayout() executing")

        b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
        b.BeginVertBox('None')
        b.  BeginVertBox('EtchedIn', 'Select mandate types:')

        for mandateType in self._mandateTypes:
            # Remove "-" and " " characters from name
            checkBoxName = mandateType.replace("-", "")
            checkBoxName = "chk%s" % checkBoxName.replace(" ", "")

            # Save Mandate type details in dictionary
            self._checkBoxes[checkBoxName] = [mandateType, None]
            b.      AddCheckbox(checkBoxName, mandateType)

        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

    def HandleCreate(self, dialog, layout):
        """
        GUI creation handler.
        :param dialog: FUxLayoutBuilder
        :param layout:
        """
        getLogger().debug("HandleCreate() executing")
        self._dialog = dialog
        ctrl = layout.GetControl

        for checkBoxName in self._checkBoxes.keys():
            self._checkBoxes[checkBoxName][1] = ctrl(checkBoxName)
            self._checkBoxes[checkBoxName][1].Checked(True)

    def HandleApply(self):
        """
        Dialog Handle Apply handler.
        :return: bool
        """
        getLogger().debug("HandleApply() executing ...")
        limits = []
        allLimits = GetLimits(self._modified_trade)

        for limit in allLimits:
            spec = limit.LimitSpecification().Name()
            for checkBoxName in self._checkBoxes.keys():
                checkBoxCtrl = self._checkBoxes[checkBoxName][1]
                limitSpec = self._checkBoxes[checkBoxName][0]
                if checkBoxCtrl.Checked() is True and spec == limitSpec:
                    limits.append(limit)

        dialog = MandateCheckDialogBase(self._modified_trade, limits, 0, self._shell, True)
        # pylint: disable=no-member
        acm.UX().Dialogs().ShowCustomDialogModal(self._shell, dialog.CreateLayout(), dialog)
        return True


class MandateCheckDialogBase(object, FUxCore.LayoutDialog):
    """
    Pre-deal check GUI
    """
    def __init__(self, modifiedTrade, limitsList, tradeOptionalKey, shell, readOnly):
        self._dialog = None
        self._shell = shell
        self._btnAcceptMandatesCtrl = None
        self._btnDetailCtrl = None
        self._btnOkCtrl = None
        self._btnCancelCtrl = None
        self._limits = None
        self._limitSheet = None
        self._edtSummary = None
        self._allMandateDetailDict = acm.FDictionary()  # pylint: disable=no-member
        self._updatedStates = {}
        self._modifiedTrade = modifiedTrade
        self._tradeOptionalKey = tradeOptionalKey
        self._limitsList = limitsList
        self._mandates = []
        self._mandatoryMandateMissing = []
        self.overallBlock = False

        self._blockPreDealCheck = None

        self._listOfMandates = []
        self._columnHeadings = ["", "Checked Attribute", "Comparator", "Checked Value"]
        self._defaultStyle = {'background': 'white', 'color': 'black', 'style': 'regular', 'size': 8}
        self._instructionTxt = 'Instruction text'
        self._rowHeight = []

        # Specify the styles for the cells
        self._styleFailed = {'background': 'red', 'color': 'white', 'style': 'regular', 'size': 8}
        self._styleWarning = {'background': 'orange', 'color': 'white', 'style': 'italic', 'size': 8}

        self._readOnly = readOnly
        self._SetupMandates()

    def _SetupMandates(self):
        """
        Load all the mandate objects using the list of limits passed to the class.
        """
        for limit in self._limitsList:
            mandate = Mandate(limit)
            self._mandates.append(mandate)

    def _AllMandatesAccepted(self, user):
        """
        Check if all the mandates have been accepted by the trader.
        :param user:
        :return:
        """
        if self._mandates:
            for mandate in self._mandates:
                if mandate.IsAcceptedByTrader(user) is False:
                    return False
        return True

    def __AcceptAllMandates(self, user):
        """
        Accept all outstanding mandates for trader.
        :param user: FUser
        """
        if self._mandates:
            for mandate in self._mandates:
                if mandate.IsAcceptedByTrader(user) is False:
                    mandate.AddAcceptedTrader(user)
                    mandate.Commit()
                    getLogger().debug('Accepted mandate (%s) .' % mandate.Name())
                else:
                    getLogger().debug('Mandate has previously been accepted (%s)' % mandate.Name())

    def HandleApply(self):
        """
        Dialog Handle Apply handler.
        :return: bool
        """
        getLogger().debug("HandleApply() executing")
        if not self.__CheckComment():
            # Does not return anything, so _dialog stays open, check comment does a popup
            getLogger().debug("Dialog stays open")
        else:
            for limit in self._limitsList:
                specName = limit.LimitSpecification().Name()
                mandate = self._allMandateDetailDict.At(specName)
                # if mandate.behaviour[limit.Oid()][0] == 2:
                
                # Check if mandate is non-blocking only
                if mandate.GetBehaviour()[0] == 2:
                    breachComment = self.__GetCellValue(limit, 'Mandate Fail Comment').Value()
                    violation = CreateViolation(limit,
                                                self._modifiedTrade,
                                                self._tradeOptionalKey,
                                                specName,
                                                mandate.Entity(),
                                                'mandateVersion',
                                                self._modifiedTrade.VersionId(),
                                                breachComment)
                    if violation:
                        violation.AddAdditionalTradeParams(self._modifiedTrade)

                    getLogger().debug('-----------created violation: %s' % str(violation))
            return True

    def CreateLayout(self):
        """
        Creating the layout.
        :return: FUxLayoutBuilder
        """
        getLogger().debug('CreateLayout() executing ..')
        limitSheetWidth = 1325 if self._readOnly is False else 950

        b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
        b.BeginVertBox()
        b.  BeginVertBox('EtchedIn', 'Mandates')
        b.    BeginVertBox()
        b.      AddCustom('limits', 'sheet.FLimitSheet', limitSheetWidth, 150)
        b.    EndBox()
        b.    AddSeparator()
        b.  EndBox()

        b.  BeginHorzBox()
        b.    AddButton('detail', 'Mandate Detail')
        b.    AddFill()
        b.    AddButton('btnAccept', 'Accept Mandates')
        b.    AddButton('ok', 'Continue')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()

        b.EndBox()

        return b

    def HandleCreate(self, dialog, layout):
        """
        GUI creation handler
        :param dialog:
        :param layout:
        """
        getLogger().debug('HandleCreate() executing ..')
        self._dialog = dialog
        self._dialog.Caption('Mandates - ' + self._GetTradeDescription())

        ctrl = layout.GetControl
        self._btnAcceptMandatesCtrl = ctrl('btnAccept')
        self._btnAcceptMandatesCtrl.AddCallback("Activate", self._OnClickAcceptMandates, None)
        self._btnDetailCtrl = ctrl('detail')
        self._btnOkCtrl = ctrl('ok')
        self._btnCancelCtrl = ctrl('cancel')
        self._btnDetailCtrl.AddCallback("Activate", self.__OnDetailClickedHandler, 'AAA')
        self._limitSheet = ctrl('limits').GetCustomControl()

        self.__LoadMandatesIntoPreDealCheck()
        self.__InitialiseLimits()
        self.__InitialiseLimitSheet()
        self.__CalculateLimitValues()
        self.__UpdateColumnComment()
        self.__UpdateButtons()
        self.__UpdateDialog()

    def HandleCancel(self):
        """
        Dialog Handle Cancel handler.
        :return: bool
        """
        getLogger().debug('Cancel Clicked')

        if self._readOnly is False:
            for limit in self._limitsList:
                specName = limit.LimitSpecification().Name()
                mandate = self._allMandateDetailDict.At(specName)
                breachComment = 'Trader blocked from booking trade.'
                violation = CreateViolation(limit,
                                            self._modifiedTrade,
                                            self._tradeOptionalKey,
                                            specName,
                                            mandate.Entity(),
                                            '',
                                            self._modifiedTrade.VersionId(),
                                            breachComment)
                if violation:
                    violation.AddAdditionalTradeParams(self._modifiedTrade)
                getLogger().debug('Created violation: %s' % str(violation))
        return True
    
    def HandleDestroy(self):
        """
        Dialog handle destroy handler
        :return: bool
        """
        getLogger().debug('Handle Destroy')

    def __MessageBoxYesNo(self, title, message):
        """
        Display a dialog showing a message with a 'Yes' and a 'No' button.
        :param title: string - Title of the dialog
        :param message: string - Message of the dialog
        :return: boolean
        """
        answer = acm.UX().Dialogs().MessageBoxYesNo(self._shell, title, message)  # pylint: disable=no-member
        if answer == 'Button1':
            return True
        return False

# Methods to initialise, populate and also simulate values in the the LimitsSheet:
# =============================================================================================

    def __CheckComment(self):
        """
        Retrieve the comment entered by the user.
        :return: bool
        """
        for limit in self._limitsList:
            mandate = self._allMandateDetailDict.At(limit.LimitSpecification().Name())
            # if mandate.behaviour[limit.Oid()][0] == 2:
            if mandate.GetBehaviour()[0] == 2:
                cellValue = self.__GetCellValue(limit, 'Mandate Fail Comment').Value()
                # if cellValue == '' or cellValue == mandate.behaviour[limit.Oid()][1]:
                if cellValue == '' or cellValue == mandate.GetBehaviour()[1]:
                    shell = acm.UX().SessionManager().Shell()  # pylint: disable=no-member
                    msg = 'Please enter a reason for each Mandate Violation that requires a comment'
                    acm.UX().Dialogs().MessageBoxInformation(shell, msg)  # pylint: disable=no-member
                    return False
        return True

    def __LoadMandatesIntoPreDealCheck(self):
        """
        All limits passed to the dialog are filtered and then added to the pre-deal check.

        (1) Limits without a mandate are removed from the check.
        (2) A check is performed to check if all mandatory mandates are passed to the pre-deal check.
        """

        getLogger().debug("__LoadMandatesIntoPreDealCheck() executing")
        atLeastOneCommentRequired = False

        for limit in self._limitsList:
            limitSpecName = limit.LimitSpecification().Name()
            getLogger().debug("Limit specification: %s" % limitSpecName)

            mandate = self._allMandateDetailDict[limitSpecName]

            if not mandate:
                mandate = Mandate(limit)

            if mandate:
                getLogger().debug("Adding limit to pre-deal check (%s - %s)" % (limitSpecName, limit.Oid()))
                behaviour = mandate.GetBehaviour()

                if behaviour[0] == 3:                       # Breach and block
                    self.overallBlock = True
                if behaviour[0] == 2:                       # Comment allowed
                    atLeastOneCommentRequired = True

                self._allMandateDetailDict.AtPut(limitSpecName, mandate)
            else:
                # Removing a limit if there is no mandate found for the limit. If the mandate was
                # mandatory that will block based on below code.
                mandatoryMandateTypes = GetMandateSettingsParam("Mandatory Mandate Types").split(",")
                mandatoryMandateTypes = list(filter(None, mandatoryMandateTypes))
                if limitSpecName not in mandatoryMandateTypes:
                    getLogger().debug("Removing limit with spec %s (%s) from check." % (limitSpecName, limit.Oid()))
                    self._limitsList.Remove(limit)

        # self.overallBlock = overallBlock
        self.atLeastOneCommentRequired = atLeastOneCommentRequired

        # Check for mandatory mandates
        getLogger().debug("All mandates applicable: %s" % self._allMandateDetailDict.Keys())
        mandatoryMandateTypes = GetMandateSettingsParam("Mandatory Mandate Types").split(", ")
        mandatoryMandateTypes = list(filter(None, mandatoryMandateTypes))
        applicableMandateTypes = self._allMandateDetailDict.Keys()
        for mandatoryMandateType in mandatoryMandateTypes:
            if mandatoryMandateType not in applicableMandateTypes:
                self._mandatoryMandateMissing.append(mandatoryMandateType)
                getLogger().info("Mandatory mandate missing (%s)." % mandatoryMandateType)

    def __InitialiseLimits(self):
        """
        Create FASQLQueryFolder that will be used to populate the limits in the limit sheet that is displayed in the
        pre-deal check window.
        """
        getLogger().debug("__InitialiseLimits() executing")

        self._limits = acm.FASQLQueryFolder()  # pylint: disable=no-member
        self._limits.Name(self._GetTradeDescription())
        query = acm.CreateFASQLQuery('FLimit', 'OR')  # pylint: disable=no-member

        for limit in self._limitsList:
            getLogger().debug('Add limit to query: %s' % limit.Oid())
            query.AddOpNode('OR')
            query.AddAttrNode('Oid', 'EQUAL', limit.Oid())

        if not query.AsqlNodes():
            # No limits to display
            query.AddOpNode('AND')
            query.AddAttrNode('Oid', 'EQUAL', -1)

        self._limits.AsqlQuery(query)

    def __InitialiseLimitSheet(self):
        """
        Set up the columns that will be displayed in the pre-deal check's limit sheet. Populate the limit sheet
        with the temporary query folder.
        """
        getLogger().debug("__InitialiseLimitSheet() executing")

        # Clear the limit sheet columns
        columns = self._limitSheet.ColumnCreators()
        columns.Clear()

        # Populate the limit sheet columns
        extContext = acm.GetDefaultContext()  # pylint: disable=no-member

        if self._readOnly is True:
            defaultColumns = acm.GetColumnCreators(GetReadOnlyLimitsColumns(), extContext)  # pylint: disable=no-member
        else:
            defaultColumns = acm.GetColumnCreators(GetDefaultLimitsColumns(), extContext)  # pylint: disable=no-member

        for i in range(defaultColumns.Size()):
            columns.Add(defaultColumns.At(i))

        # Insert the query folder into the limit sheet
        self._limitSheet.InsertObject(self._limits, 'IOAP_LAST')
        self._limitSheet.PrivateTestSyncSheetContents()

    def __UpdateLimitState(self, checkResult):
        """
        Update the limit state for a specific limit after the limit has been checked on a simulated column.
        :param checkResult: FLimitMonitor.LimitCheckResult
        """
        getLogger().debug("__UpdateLimitState() executing")

        allowedMap = {1: MANDATE_ALLOWED_TEXT, 0: MANDATE_NOT_ALLOWED_TEXT, -1: MANDATE_NOT_FOUND_TEXT}
        limit = checkResult.Limit
        checkedValue = checkResult.CheckedValue
        stateAfter = checkResult.StateAfter

        if checkedValue == -1:
            # Override this limit state to distinguish between breached and missing mandates.
            # stateAfter = 'No Mandate Found'
            stateAfter = MANDATE_NOT_FOUND_TEXT

        # Update simulated column values
        stateMapped = STATE_MAP[stateAfter]
        failType = GetFailType(limit)
        self.__SetCellSimulatedValue(limit, 'Limit Current State', stateMapped)
        self.__SetCellSimulatedValue(limit, 'Mandate Fail Type', failType)

        self._updatedStates[limit] = checkedValue

        mandate = self._allMandateDetailDict.At(limit.LimitSpecification().Name())
        mandate.SimulatedCheckValue(allowedMap[checkedValue])

    def __CalculateLimitValues(self):
        """
        Calculate the simulated values for all the limits in the pre-deal check.
        """
        getLogger().debug("__CalculateLimitValues() executing")
        calcToStringMapping = {MANDATE_NOT_FOUND_TEXT: -1, MANDATE_NOT_ALLOWED_TEXT: 0, MANDATE_ALLOWED_TEXT: 1}

        for limit in self._limitsList:
            getLogger().debug('Checking Limit (%s)' % limit.Name())
            # Calculate the checked value using the _modifiedTrade object
            target = limit.LimitTarget()
            calcSpec = target.CalculationSpecification()
            columnId = calcSpec.ColumnName()
            calc = calcSpace.CreateCalculation(self._modifiedTrade, columnId)

            # Check the limit result on the calculated column
            getLogger().debug('Check limit result on column')
            res = FLimitMonitor.LimitCheckResult()
            res.Limit = limit
            res.StateBefore = 'Ready'
            res.CheckedValue = calcToStringMapping[calc.Value()]

            # Set the checked limit state
            getLogger().debug('Set the checked limit state')
            cls = FLimitMonitor.FMonitoredLimit
            cls._SetCheckedLimitState(res)  # pylint: disable=protected-access
            if res:
                self.__UpdateLimitState(res)

    def __SetCellSimulatedValue(self, limit, columnId, value):
        """
        Update the contents of a specific cell with the value passed in the "value" parameter. Column ID is the column
        ID of the specific cell and limit is the specific limit.
        :param limit: FLimit
        :param columnId: string
        :param value: string
        """
        getLogger().debug('__SetCellSimulatedValue() executing ..')
        try:
            if self._limitSheet.GridColumnIterator():
                cell = self.__GetCellValue(limit, columnId)
                evaluator = cell.Evaluator() if cell else None
                if evaluator:
                    if value is not None:
                        evaluator.Simulate(value, False)
                    else:
                        evaluator.RemoveSimulation()
        except Exception as e:
            getLogger().error('Exception error: %s' % e)

    def __GetCellValue(self, limit, columnId):
        """
        Get the value contained in a specific cell. The row is specified using the limit and the column is specified
        using the column ID.
        :param limit: FLimit
        :param columnId: string
        :return: string
        """
        getLogger().debug('__GetCellValue() executing ..')
        columnIter = self._limitSheet.GridColumnIterator()
        while columnIter:
            columnName = str(columnIter.GridColumn().ColumnId()) if columnIter.GridColumn() else None
            if columnName == columnId:
                break
            columnIter.Next()
        if columnIter:
            rowIter = self._limitSheet.RowTreeIterator(False)
            rowIter = rowIter.Find(limit) if rowIter else None
            if rowIter:
                return self._limitSheet.GetCell(rowIter, columnIter)
        return None

    def _GetTradeDescription(self):
        return self._modifiedTrade.Instrument().Name() + ' ' + self._modifiedTrade.StringKey()

    def _OnClickAcceptMandates(self, arg1, arg2):
        """
        On Click event handler for the "Accept Mandates" button.
        :param arg1:
        :param arg2:
        """
        getLogger().debug("_OnClickAcceptMandates() executing ..")
        del arg1
        del arg2

        msg = "By clicking yes you agree to the mandates. Are you sure you agree?"
        if self.__MessageBoxYesNo("Question", msg) is True:
            self.__AcceptAllMandates(acm.User())  # pylint: disable=no-member

            self.__UpdateButtons()
            # self._btnOkCtrl.Enabled(True)
            # self._btnCancelCtrl.Enabled(True)
            # self._btnAcceptMandatesCtrl.Enabled(False)

    def __OnDetailClickedHandler(self, arg1, arg2):
        """
        Event handler for the on-click event when the user clicks on the "Details" button on the pre-deal check
        dialog.
        :param arg1:
        :param arg2:
        """
        del arg1
        del arg2

        queryFolders = []
        getLogger().debug("__OnDetailClickedHandler() executing")
        self.__LoadMandates()

        # Loop through mandates
        for mandateCount in range(0, len(self._listOfMandates)):
            mandate = self._listOfMandates[mandateCount]

            # Check if the mandate failed
            queries = mandate.QueryFolders()
            # Check which queries in the mandate failed
            for query in queries:
                queryFolder = acm.FStoredASQLQuery[query]  # pylint: disable=no-member
                queryFolders.append(queryFolder)

        treeViewBuilder = CreateTreeViewDialogLayout()
        treeViewDialog = DialogTreeView(self._modifiedTrade, queryFolders)
        # pylint: disable=no-member
        acm.UX().Dialogs().ShowCustomDialogModal(acm.UX().SessionManager().Shell(), treeViewBuilder, treeViewDialog)

    def __LoadMandates(self):
        self._listOfMandates = []
        for applicableLimit in self._limitsList:
            self._listOfMandates.append(Mandate(applicableLimit))

    def __IsBlockingMandateBreached(self):
        """
        Check if a blocking mandate is breaching.
        :return: bool
        """
        if not self._blockPreDealCheck:
            self._blockPreDealCheck = False
            for limitSpecName in self._allMandateDetailDict:
                mandate = self._allMandateDetailDict.At(limitSpecName)
                if mandate.GetBehaviour()[0] == 3:
                    self._blockPreDealCheck = True
                    return True
        else:
            return self._blockPreDealCheck
        return False

    def __AllMandatesPass(self):
        """
        Check if all the mandates are passing.
        :return: bool
        """
        for limitSpecName in self._allMandateDetailDict:
            mandate = self._allMandateDetailDict.At(limitSpecName)
            if mandate.GetBehaviour()[0] != 4:
                return False
        return True

    def __UpdateColumnComment(self):
        """
        Update the "Mandate Fail Comment" column values to display the correct messages for each limit.
        """
        getLogger().debug('__UpdateColumnContent() executing ..')
        if self._readOnly is False:
            getLogger().debug("__UpdateColumnComment() executing")

            for limitSpecName in self._allMandateDetailDict:
                mandate = self._allMandateDetailDict.At(limitSpecName)
                if len(self._mandatoryMandateMissing) != 0:
                    behaviour = 'Mandatory mandate missing %s.  Blocking trade' % self._mandatoryMandateMissing
                elif self.__IsBlockingMandateBreached() is True:
                    behaviour = 'At least 1 blocking mandate failed. Blocking trade'
                else:
                    behaviour = mandate.GetBehaviour()[1]

                # pylint: disable=no-member
                self.__SetCellSimulatedValue(acm.FLimit[mandate.LimitOid()], 'Mandate Fail Comment', behaviour)

    def __UpdateButtons(self):
        """
        Update the "Continue" button on the dialog to enable it or disable it. This will enable or block a user from
        saving a trade.
        """
        getLogger().debug("__UpdateButtons() executing")

        # Check if Mandates have been accepted
        if self._AllMandatesAccepted(acm.User()) is False:  # pylint: disable=no-member
            getLogger().debug('All Mandates have not been accepted')
            self._btnAcceptMandatesCtrl.Enabled(True)
            self._btnOkCtrl.Enabled(False)

            if self.overallBlock is True or len(self._mandatoryMandateMissing) != 0 or self._blockPreDealCheck is True:
                getLogger().debug('A Blocking mandate has been breached')
                self._btnOkCtrl.Visible(False)
            else:
                getLogger().debug('No blocking mandate has been breached.')
                self._btnOkCtrl.Visible(True)
        else:
            getLogger().debug('All Mandates have been accepted')
            self._btnAcceptMandatesCtrl.Enabled(False)
            self._btnCancelCtrl.Visible(True)
            self._btnCancelCtrl.Enabled(True)

            if self.overallBlock is True or len(self._mandatoryMandateMissing) != 0 or self._blockPreDealCheck is True:
                getLogger().debug('A blocking mandate has been breached')
                self._btnOkCtrl.Enabled(False)
                self._btnOkCtrl.Visible(False)
                self._btnCancelCtrl.Label('OK')
                self._btnCancelCtrl.ForceRedraw()
            else:
                getLogger().debug('No blocking mandate has been breached')
                self._btnOkCtrl.Enabled(True)

    def __UpdateDialog(self):
        """
        Hide the dialog if all the mandates have passed AND this behaviour has been enabled in GenericMandatesSettings
        in the FParameters.
        """
        getLogger().debug("__UpdateDialog() executing")
        if self._AllMandatesAccepted(acm.User()) is True:  # pylint: disable=no-member
            getLogger().debug('All trader mandates have been accepted.')
            if GetMandateSettingsParam("DisplayPreDealCheckIfAllMandatesPass") == "False":
                getLogger().debug("DisplayPreDealCheckIfAllMandatesPass enabled")
                if self.__AllMandatesPass() is True and self._readOnly is False:
                    getLogger().debug("DisplayPreDealCheckIfAllMandatesPass enabled - Closing pre-deal check dialog")
                    self._dialog.CloseDialogOK()
        else:
            getLogger().debug('All trader mandates have NOT been accepted.')

        # Read only mode - when user is testing trade against limit (simulation)
        if self._readOnly is True:
            self._btnOkCtrl.Enabled(False)
            self._btnOkCtrl.Visible(False)
