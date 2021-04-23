""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLInsDefLimitCheckPanel.py"
from __future__ import print_function
import acm
import FUxCore
from FACLArMLResponse import FACLArMLResponse
from FACLFilterQuery import DefaultFilterCallbacks, FACLFilterQuery
from FACLParameters import PrimeSettings, CommonSettings
import FACLMessageRouter
import FACLArMLMessageBuilder
import FACLAttributeMapper
import FACLTradeActionUtils
import datetime
import FACLUtils
import traceback
import math

ICON_NONE = ''
ICON_OK = 'Check'
ICON_VIOLATION = 'Warning'
ICON_ERROR = 'Error'
ICON_CHECK = 'Refresh'
ICON_INIT_FAILED = 'Warning'

class FACLInsDefLimitCheckLogic():
    def __init__(self, msgRouter, msgBuilder, responseBuilder):
        self._msgRouter = msgRouter
        self._msgBuilder = msgBuilder
        self._responseBuilder = responseBuilder
        
    def AvailabilityCheck(self, trade, mapper, statusCB):
        try:            
            params = mapper.MapAttributes(trade)
            avilabilityArML = self._msgBuilder.CreateRequestDealAvailability(params)
            toReturn = self._fetchDetails(trade, avilabilityArML, statusCB)
        except Exception as e:
            print(traceback.format_exc())
            msg = 'Error: %s' % e
            statusCB(msg, ICON_ERROR)
            headline = msg
            details = ''
            toReturn = headline, details, None
            
        return toReturn
    
    def TrialCheck(self, trade, mapper, isNewTrade, statusCB):
        try:
            params = mapper.MapAttributes(trade)
            trialArML = None
            
            if isNewTrade:
                trialArML = self._msgBuilder.CreateAddTrialCheck(params)
            else:
                trialArML = self._msgBuilder.CreateModifyTrialCheck(params)
            
            toReturn = self._fetchDetails(trade, trialArML, statusCB)
        except Exception as e:
            print(traceback.format_exc())
            msg = 'Error: %s' % e
            statusCB(msg, ICON_ERROR)
            headline = msg
            details = ''
            toReturn = headline, details, None

        return toReturn
        
    # e2e_* methods are for backwards compatibility to allow integration tests to run properly.
    def e2e_AvailabilityCheck(self, trade, referenceTrade, mapper, statusCB):
        return self.AvailabilityCheck(self, trade, mapper, statusCB)
        
    def e2e_TrialCheck(self, trade, referenceTrade, mapper, isNewTrade, statusCB):
        return self.TrialCheck(self, trade, mapper, isNewTrade, statusCB)
    
    def _fetchDetails(self, trade, armlMsg, statusCB):
        details = None
        headline = None
        response = None
        try:
            FACLUtils.ensureConnectedToAMB(PrimeSettings.ambUser, PrimeSettings.ambPassword, PrimeSettings.ambAddress)
            responseArML = self._msgRouter.RouteMessagePersistentWithReply(trade, armlMsg)
            response = self._responseBuilder(responseArML)
            headline = response.Headline()
            details = ''
            
            if response.ExceptionOccurred():
                icon = ICON_ERROR
            elif response.LimitOk():
                icon = ICON_OK
            elif response.AvailabilityOk():
                icon = ICON_OK
            else:
                icon = ICON_VIOLATION
        except Exception as e:
            print(traceback.format_exc())
            icon = ICON_ERROR
            msg = 'Error: %s' % e
            headline = msg
            details = ''

        statusCB(headline, icon)
        
        return headline, details, response
    
class FACLInsDefDetailsDialog(FUxCore.LayoutTabbedDialog):
    def __init__(self, shell):
        self._ux_dlg = None
        self._ux_headline = None
        self._ux_details = None
        self._response = None
        self._headline = None
        self._detailed_description = None
        self._ux_ok = None
        self._shell = shell
        self._graphData = None
        self._limitOptionData = None
        self._graph_available = False

    def HandleApply( self, *args ):
        return True

    def HandleCreate(self, dlg, layout):
        response = self._response
        
        self._ux_dlg = dlg
        self._ux_dlg.Caption('ACL Details')
        
        self._createTopLayout(dlg)
        self._createTabs(dlg)
        self._ux_ok = layout.GetControl('ok')
    
    def _createTopLayout(self, dlg):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        self.  _createHeadlineLayout(b)
        self.  _createErrorsLayout(b)
        self.  _createViolationsLayout(b)
        self.  _createPotentialViolationsLayout(b)
        b.EndBox()
        layout = dlg.AddTopLayout( "Top", b )
        
        self._initTopLayout(layout)
    
    def _createTabs(self, dlg):    
        if not self._response:
            return
        
        self._createGraphsTab(dlg)
        self._createDataPointsTab(dlg)
        self._createAvailabilityResultsTab(dlg)
        
        self._initTabs()
                
    def _createGraphsTab(self, dlg):
        if self._response.GraphData():
            b = acm.FUxLayoutBuilder()
            b.  BeginVertBox('None')
            b.    AddOption('LimitOption', 'Limit Profile')
            b.    Add2DChart('LimitGraph', 600, 300)            
            b.  EndBox()
            layout = dlg.AddPane( 'Graphs', b )
            
            try:
                self._ux_limit_option = layout.GetControl('LimitOption')
                self._ux_limit_option.AddCallback('Changed', self._limitOptionChanged, self._ux_limit_option)
                self._ux_graph  = layout.GetControl('LimitGraph')
            except:
                pass
                
    def _createDataPointsTab(self, dlg):
        if self._response.GraphData():
            b = acm.FUxLayoutBuilder()
            b.  BeginVertBox('None')
            b.    AddOption('LimitOption', 'Limit Profile')
            b.    AddList('pointList', 8)
            b.  EndBox()
            layout = dlg.AddPane( 'Data Points', b )
            
            try:
                self._ux_limit_option2 = layout.GetControl('LimitOption')
                self._ux_limit_option2.AddCallback('Changed', self._limitOptionChanged, self._ux_limit_option2)
                self._pointList = layout.GetControl('pointList')
            except Exception as e:
                pass
                
    def _createAvailabilityResultsTab(self, dlg):
        if self._response.AvailabilityContents():
            b = acm.FUxLayoutBuilder()
            b.  BeginVertBox('None')
            b.    AddInput('counterparty', 'Counterparty')
            b.    AddTree('availabilityResultsTree', 600, 120)
            b.  EndBox()
            layout = dlg.AddPane( 'Availability Results', b )
            
            try:
                availabilityResultsTree = layout.GetControl('availabilityResultsTree')
                self._buildTree(availabilityResultsTree, self._response.AvailabilityContents())
                counterpartyCtrl = layout.GetControl('counterparty')
                counterpartyCtrl.SetData(self._response.Counterparty())
                counterpartyCtrl.Editable(False)
            except:
                pass
                
    def _createHeadlineLayout(self, b):
        b.  BeginHorzBox('None')
        b.      AddIcon('StatusIcon')
        b.      AddLabel('LimitHeadline', '', 500)
        b.  EndBox()
                
    def _createErrorsLayout(self, b):
        if self._response.ExceptionContents():
            b.  BeginVertBox('EtchedIn', 'Errors')
            b.    AddList('errorsList', 4)
            b.  EndBox()
            
    def _createViolationsLayout(self, b):
        if self._response.ViolationContents():
            b.  BeginVertBox('EtchedIn', 'Violations')
            b.    AddList('violationsList', 4)
            b.  EndBox()
                
    def _createPotentialViolationsLayout(self, b):
        if self._response.AvailabilityViolationContents():
            b.  BeginVertBox('EtchedIn', 'Potential Violations')
            b.    AddList('availabilityViolationsList', 4)
            b.  EndBox()
            
    def _initTopLayout(self, layout):
        icon = layout.GetControl('StatusIcon')
        if self._response:
            if self._response.ExceptionOccurred():
                icon.SetData(ICON_ERROR)
            elif self._response.AvailabilityOk():
                icon.SetData(ICON_OK)
            elif self._response.LimitOk():
                icon.SetData(ICON_OK)
            else:
                icon.SetData(ICON_VIOLATION)
        else:
            icon.SetData(ICON_ERROR)
            
        self._ux_headline = layout.GetControl('LimitHeadline')
        self._ux_headline.SetFont('Segoe UI Semibold', 11, False, False)
        self._ux_headline.SetData(self._headline)
        self._ux_headline.ForceRedraw()
        
        try:
            errorsList = layout.GetControl('errorsList')
            self._buildList(errorsList, self._response.ExceptionContents())
        except:
            pass
            
        try:
            violationsList = layout.GetControl('violationsList')
            self._buildList(violationsList, self._response.ViolationContents())
        except:
            pass
            
        try:
            availabilityViolationsList = layout.GetControl('availabilityViolationsList')
            self._buildList(availabilityViolationsList, self._response.AvailabilityViolationContents())
        except:
            pass
    
    def _initTabs(self):
        try:
            self._populateLimitOption()
            self._buildGraph()
            self._populateDataPointsTable(True)
        except:
            pass

    def _buildList(self, listControl, contents):
        listControl.ShowColumnHeaders()

        for i, header in enumerate(contents[0]):
            listControl.AddColumn(header, -1, '')

        root = listControl.GetRootItem()
        for row in contents[1:]:
            item = root.AddChild()
            for i, col in enumerate(row):
                item.Label(col, i)

        for i in range(listControl.ColumnCount()):
            listControl.AdjustColumnWidthToFitItems(i)    

    def _buildTree(self, treeControl, contents):
        treeControl.ShowColumnHeaders()
        icon = 'Ball'
        
        treeControl.ColumnLabel(0, contents[0][0])
        for i, header in enumerate(contents[0][1:]):
            treeControl.AddColumn(header, 70)
        treeControl.ColumnWidth(0, 300)    

        root = treeControl.GetRootItem()
        
        for error in contents[1:]:
            item = root.AddChild()
            if type(error[-1]) == list:
                for i, e in enumerate(error[:-1]):
                    item.Label(e, i)
                    item.Icon(icon, icon)
                for el in error[-1]:
                    subItem = item.AddChild()
                    for i, e in enumerate(el):
                        subItem.Label(e, i)
                        subItem.Icon(icon, icon)
                item.Expand()
            else:
                for i, e in enumerate(error):
                    item.Label(e, i)
                    item.Icon(icon, icon)

    def CreateLayout(self, response):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')

        self.CreateLayoutCustomPane(b)
        b.EndBox()
        return b
    
    def CreateLayoutCustomPane(self, b):
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'Close')
        b.  EndBox()

    def ShowDetailsDialog(self, headline, details, response):
        self._headline = headline
        self._detailed_description = details
        self._response = response
        if response:
            self._graphData = response.GraphData()
        else:
            self._graphData = {}
        builder = self.CreateLayout(response)
        return acm.UX().Dialogs().ShowCustomDialogModal(self._shell, builder, self)

    def _limitOptionChanged(self, arg = 0, arg2 = 0):
        limitOption = arg.GetData()
        self._ux_limit_option.SetData(limitOption)
        self._ux_limit_option2.SetData(limitOption)
        self._buildGraph()
        self._populateDataPointsTable(False)

    def _populateLimitOption(self):
        if not self._graphData:
            return
        
        defaultValue = None
        limitOptionValues = []
        for item in self._graphData.values():
            name = item['name']
            limitOptionValues.append(name)
            if item['is_limit_violated'] and not defaultValue:
                defaultValue = name
                    
        limitOptionValues.sort()
        for name in limitOptionValues:
            self._ux_limit_option.AddItem(name)
            self._ux_limit_option2.AddItem(name)
            
        if defaultValue == None and len(limitOptionValues) > 0:
            defaultValue = limitOptionValues[0]
            
        self._ux_limit_option.SetData(defaultValue)
        self._ux_limit_option2.SetData(defaultValue)
    
    def _selectedGraphData(self):
        measure = self._ux_limit_option.GetData()
        data = None
        for key in self._graphData.keys():
            if self._graphData[key]['name'] == measure:                
                data = self._graphData[key]
        return data
        
    def _populateDataPointsTable(self, includeHeader):
        selectedGraphData = self._selectedGraphData() 
    
        if not selectedGraphData: 
            return

        pointList = self._pointList
        pointList.RemoveAllItems()

        table = [['Date', 'Pre Deal', 'Post Deal', 'Deal Effect', 'Limit']] if includeHeader else [[]]
        table.extend(selectedGraphData['rows'])            
        
        self._buildList(pointList, table)        
        
    def _buildGraph(self):    
        selectedGraphData = self._selectedGraphData()    
        if not selectedGraphData: 
            return
            
        graph = self._ux_graph
        graph.ClearChart()
        graph.ShowLegend(True)        
        
        #Set the titles of the axis
        units = ['', '(tens)', '(hundreds)', '(thousands)', '(ten thousands)', '(hundred thousands)', '(millions)', '(ten millions)', '(hundred millions)']
        scalingFactor = 1.0 / CommonSettings.scalingFactor
        scalingFactorText = units[int(math.log10(scalingFactor))]
        graph.SetAxisTitles("", "%s %s" % (selectedGraphData['currency'], scalingFactorText))
        #Add a callback method to supply x and y values.
        graph.XValuesEventHandler().Add(self._getXValues, None)
        graph.YValuesEventHandler().Add(self._getYValues, None)

        xvalues = selectedGraphData['x_values']
        # Add three main series
        series = graph.AddSeries('StepLine', len(xvalues), acm.UX().Colors().Create(200, 0, 0), 'Limit')        
        series.SetBorderWidth(3)
        series.Populate(xvalues)        
        series = graph.AddSeries('StepLine', len(xvalues), acm.UX().Colors().Create(0, 170, 0), 'Pre Deal')        
        series.Populate(xvalues)        
        series.SetBorderWidth(3)
        series = graph.AddSeries('StepLine', len(xvalues), acm.UX().Colors().Create(0, 255, 0), 'Deal (+)')        
        series.Populate(xvalues)                        
        series.SetBorderWidth(3)
        series = graph.AddSeries('StepLine', len(xvalues), acm.UX().Colors().Create(85, 200, 255), 'Deal (-)')        
        series.Populate(xvalues)                        
        series.SetBorderWidth(3)

        formatter = acm.FDateTimeFormatter('DateOnly')
        graph.SetAxisLabelFormatter('XAxis', formatter)
        graph.BaseXAxisLabelsOnSeries(series)
        graph.ShowInteractionControls(True)
    
    def _getXValues(self, args, _):
        xValue = args.At('object')        
        return xValue
        
    def _getYValues(self, args, _):
        try:
            selectedGraphData = self._selectedGraphData()    
            if not selectedGraphData: 
                return
                
            xValue = args.At('object')
            series_idx = args.At('seriesIndex')

            y_data = selectedGraphData['y_series_values'][series_idx ]
            return y_data[ args.At('objectIndex') ]
        except Exception as err: 
            traceback.print_exc()

class FACLInsDefLimitCheckPanel(FUxCore.LayoutPanel):
    def __init__(self, insDefApp, logic, detailsDialog, shell, status, enabled, queryName):
        self._logic = logic
        self._insDefApp = insDefApp
        self._detailsDialog = detailsDialog
        self._shell = shell
        self._details = None
        self._headline = None
        self._status = status
        self._response = None
        self._icon = ''
        self._enabled = enabled
        self._faclFilter = self._createFACLFilter(queryName)
        self._isUpdatePossible = False
        self._trialcheckEnabled = False
        self._uxTrialCheck = None
        self._uxAvailCheck = None
        self._uxDetails = None
        self._uxStatusIcon = None
        self._uxStatusLabel = None
        
        self._tradeAction = None # if the trade is part of an ongoing trade action, the panel will be disabled
        
    def HandleApply( self, *args ):
        return True
        
    def HandleCreate( self ):
    
        self._tradeAction = FACLTradeActionUtils.is_trade_part_of_trade_action( self._insDefApp )

        layout = self.SetLayout( self.CreateLayout() )
        self._uxTrialCheck = layout.GetControl('trialCheck')
        self._uxTrialCheck.AddCallback( "Activate", self._OnTrialCheckClicked, self )
        self._uxTrialCheck.Enabled(self._enabled and not self._tradeAction)
        self._uxAvailCheck = layout.GetControl('availCheck')
        self._uxAvailCheck.AddCallback( "Activate", self._OnAvailabilityCheckClicked, self )
        self._uxAvailCheck.Enabled(self._enabled and not self._tradeAction)
        self._uxDetails = layout.GetControl('details')
        self._uxDetails.AddCallback( "Activate", self._OnDetailsClicked, self )
        self._uxDetails.Enabled(self._enabled and not self._tradeAction)
        self._uxStatusIcon = layout.GetControl('StatusIcon')
        if self._enabled:
            self._uxStatusIcon.SetData(ICON_NONE)
        else:
            self._uxStatusIcon.SetData(ICON_INIT_FAILED)
        self._uxStatusLabel = layout.GetControl('StatusLabel')
        self._uxStatusLabel.SetData(self._status)
        
        self._insDefApp.EditTrade().AddDependent(self)
        self._insDefApp.EditInstrument().AddDependent(self)
        self.UpdateControls()
        
    def ServerUpdate(self, sender, aspect, parameter ):
        if str(aspect) == str('ContentsChanged'):
            self._details = None
            self._status = ''
            self._icon = ICON_NONE
        elif str(aspect) == str('delete'):
            self._details = None
            self._status = ''
            self._icon = ICON_NONE
            sender.RemoveDependent(self)
            self._insDefApp.EditTrade().AddDependent(self)
            self._insDefApp.EditInstrument().AddDependent(self)
        
        if str(aspect) != 'update':
            self.UpdateControls()
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddSpace(1)
        b.  BeginHorzBox()
        b.  AddSpace(1)
        
        b.BeginVertBox()        
        b.  BeginHorzBox()
        b.    AddButton('trialCheck', 'Trial Check')
        b.    AddButton('availCheck', 'Availability')
        b.    AddFill()
        b.    AddButton('details', 'Details')
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn', 'Response')
        b.    AddIcon('StatusIcon')
        b.    AddLabel('StatusLabel', '', 300)
        b.    AddFill()
        b.  EndBox()
        b.EndBox()
        
        b.AddSpace(1)
        b.EndBox()
        b.EndBox()
        return b
    
    def UpdateControls(self):
        if self._tradeAction and self._insDefApp.OriginalTrade():
            # the unsaved trade is part of a trade action, now the trade has been saved
            self._tradeAction = False
            
        if self._enabled and not self._tradeAction:
            self._runFACLFilter()
            self._uxTrialCheck.Enabled(self._trialcheckEnabled)
            self._uxAvailCheck.Enabled(self._trialcheckEnabled)
            self._uxDetails.Enabled(self._response is not None)

            self._uxStatusLabel.SetData(self._status)
            self._uxStatusLabel.ForceRedraw()

            self._uxStatusIcon.SetData(self._icon)
        
        
    def _UpdateStatus(self, statusStr, icon = ICON_NONE):
        self._status = statusStr
        self._icon = icon
        self.UpdateControls()
        
    def _OnTrialCheckClicked(self, _att1, _att2):
        if self._isUpdatePossible:
            msg = 'Do you want to trial check a new trade or an updated trade?'
            checkType = acm.UX().Dialogs().MessageBox(self._shell, 'Message', msg, 'New Trade', 'Update Trade', None, 'Button1', 'Button3')
            if checkType == 'Button1':
                isNewTrade = True
            elif checkType == 'Button2':
                isNewTrade = False
            else: # dialog closed with [x]
                return
        else:
            isNewTrade = True

        self._UpdateStatus('Performing Trial Check...', ICON_CHECK)
        trade = FACLUtils.faclObjectFromInsDef(self._insDefApp)
        mapper = FACLAttributeMapper.FACLAttributeMapper()
        
        if trade.Instrument().InsType() == 'Deposit':
            mapper = CallDepositFixAttributeMapper(mapper, self._insDefApp)
        
        self._headline, self._details, self._response = self._logic.TrialCheck(trade, mapper, isNewTrade, self._UpdateStatus)
        self.UpdateControls()
        
        if self._response and not self._response.LimitOk():
            self._OnDetailsClicked(None, None)
            
    def _runFACLFilter(self):
        previousEditObject = self._insDefApp.OriginalTrade()
        if previousEditObject and previousEditObject.IsFxSwapNearLeg():
            previousFaclEditObject = acm.FX.GetSwapFarTrade(previousEditObject)
        else:
            previousFaclEditObject = previousEditObject
            
        currentFaclEditObject = FACLUtils.faclObjectFromInsDef(self._insDefApp)

        # Callback updates things
        self._faclFilter.EvaluateQuery(previousFaclEditObject, currentFaclEditObject)
    
    def _faclFilterCallBack(self, acrStatus, isUpdatePossible, trailcheckEnabled):
        # TODO clear previous trial check result on acrStatus = Exclude?
        self._isUpdatePossible = isUpdatePossible
        self._trialcheckEnabled = trailcheckEnabled
        
    def _createFACLFilter(self, queryName):
        callBack = InsDefFilterCallbacks(self._faclFilterCallBack)
        return FACLFilterQuery(queryName, callBack)
    
    def _OnAvailabilityCheckClicked(self, _att1, _att2):
        self._UpdateStatus('Performing Availability Check...', ICON_CHECK)
        trade = FACLUtils.faclObjectFromInsDef(self._insDefApp)
        mapper = FACLAttributeMapper.FACLAttributeMapper()
        self._headline, self._details, self._response = self._logic.AvailabilityCheck(trade, mapper, self._UpdateStatus)
        self.UpdateControls()
        
        if self._response and not self._response.AvailabilityOk():
            self._OnDetailsClicked(None, None)
        
    def _OnDetailsClicked(self, _att1, _att2):
        self._detailsDialog.ShowDetailsDialog(self._headline, self._details, self._response)
        

class InsDefFilterCallbacks(DefaultFilterCallbacks):
    def __init__(self, callback):
        self._callback = callback
    
    def OnIncludeToInclude(self, *params):
        self._callback('Include', True, True)
    
    def OnIncludeToExclude(self, *params):
        self._callback('Exclude', False, False)
    
    def OnExcludeToInclude(self, *params):
        self._callback('Include', False, True)
    
    def OnExcludeToExclude(self, *params):
        self._callback('Exclude', False, False)


class CallDepositFixAttributeMapper:

    def __init__(self, delegateMapper, insdef):
        self._delegateMapper = delegateMapper
        self._insdef          = insdef

    def MapAttributes(self, trade):
        attrs = self._delegateMapper.MapAttributes(trade)
        newAmount = self.GetInitialBalanceFromUI(attrs.get('Amount'))
        if newAmount:
            attrs['Amount'] = newAmount
        
        return attrs          

    def GetInitialBalanceFromUI(self, mappedAmount):
        numberStr = mappedAmount
        if str(self._insdef.ClassName()) == 'CInsDef_CALL_DEPOSIT':
            if not self._insdef.OriginalInstrument():
                # find the initial balance for an unsaved Call Deposit/Loan
                amount = self._insdef.GetFieldValue('ins_initial_balance')
                if amount:
                    aclScalingFactor = CommonSettings.scalingFactor
                    number = abs(acm.FNumFormatter('').Parse(amount)) * aclScalingFactor
                    numberStr = str(number)

        return numberStr
    
def OnCreate(eii):
    basicApp = eii.ExtensionObject()
    try:
        from FACLParameters import PrimeSettings, CommonSettings
        senderMBName = PrimeSettings.senderMBName
        senderSource = PrimeSettings.senderSource
        timeout = PrimeSettings.timeoutForReplyInSeconds
        receiverMBName = PrimeSettings.receiverMBName
        queryName = CommonSettings.tradeFilterQuery
        FACLUtils.ensureConnectedToAMB(PrimeSettings.ambUser, PrimeSettings.ambPassword, PrimeSettings.ambAddress)
        status = ''
        enabled = True
        
        excludeInsDefClassList = []
        for className in PrimeSettings.excludeInsDef:
            excludeInsDefClassList.append( eval( "acm." + className ) )
        if basicApp.Class() in excludeInsDefClassList:
            return
            
    except Exception as e:
        print(e)
        senderMBName = ''
        senderSource = ''
        timeout = 10
        receiverMBName = ''
        queryName = None
        status = 'Initialization failed. See log for details.'
        enabled = False

    msgRouter = FACLMessageRouter.FACLMessageRouter(senderMBName, senderSource, timeout, receiverMBName, None, 1)
    msgBuilder = FACLArMLMessageBuilder.FACLArMLMessageBuilder()
    responseBuilder = FACLArMLResponse

    logic = FACLInsDefLimitCheckLogic(msgRouter, msgBuilder, responseBuilder)
    insDefApp = eii.ExtensionObject()
    shell = eii.Parameter('shell')
    detailsDialog = FACLInsDefDetailsDialog(shell)
    limitCheckPanel = FACLInsDefLimitCheckPanel(insDefApp, logic, detailsDialog, shell, status, enabled, queryName)
    basicApp.CreateCustomDockWindow(limitCheckPanel, 'FACLInsDefLimitCheckPanel', 'Credit Limits', 'Bottom')
