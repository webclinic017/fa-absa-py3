import acm
import FUxCore
import FUxUtils

_resultKey = acm.FSymbol('filterColumn')
    
'''Select Column Dialog'''

class FCustomSelectColumnDialog(FUxCore.LayoutDialog):

    _inputColumnId = "inputColumn"
    _btnAddColumnId = "btnAddColumn"
    
    def __init__(self, shell, result):
        self._shell = shell
        self._result = result
    
    def HandleApply(self):
        return self._result
           
    def HandleCreate(self, dlg, layout):
        self._fuxDlg = dlg
        self._layout = layout
        
        self._inputColumn = layout.GetControl(self._inputColumnId)
        self._inputColumn.Editable(False)
        self._btnAddColumn = layout.GetControl(self._btnAddColumnId)
        self._btnAddColumn.ToolTip('Select column. If there is an error in the selected column, the instrument or orderbook will be filtered out.')
        self._btnAddColumn.AddCallback('Activate',  self._OnColumnClicked, None)
        
        self.Populate()
        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        b.    BeginHorzBox()
        b.      AddInput(self._inputColumnId, "Column")
        b.      AddButton(self._btnAddColumnId, "...", False, True)
        b.    EndBox()
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.    BeginHorzBox()
        b.      AddSpace(60);
        b.      AddFill()
        b.      AddButton("ok", "OK")
        b.      AddButton("cancel", "Cancel")
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b
        
    def Populate(self):
        pass
        
    def UpdateControls(self):
        self._inputColumn.SetData(self._result)
        
    def _ShowSelectColumnsDlg(self, type):
        sheetDefinition = acm.Sheet.GetSheetDefinition(acm.FPortfolioSheet)
        gridBuilder = sheetDefinition.CreateGridBuilder(False)
        result = acm.UX().Dialogs().SelectOneColumn(self._shell, acm.FPortfolioSheet, gridBuilder, acm.GetDefaultContext())
        return result
        
    def _OnColumnClicked(self, ud, cd):
        result = self._ShowSelectColumnsDlg("");
        if result is not None:
            self._result = result
            self.UpdateControls()
            
def UnpackStoredCalibrationFilterParameterByName(initData):
    if initData:
        return initData.At(_resultKey)
    else:
        return None
    
def PackStoredCalibrationFilterParameterByName(result):
    resultDict = acm.FDictionary()
    resultDict.AtPut(_resultKey, result)
    return resultDict
    
def ael_custom_dialog_show(shell, params):
    initData = FUxUtils.UnpackInitialData(params)
    filterParameter = UnpackStoredCalibrationFilterParameterByName(initData);
    
    customDlg = FCustomSelectColumnDialog(shell, filterParameter)
    response = acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)
    
    if response is None:
        response = filterParameter;
    result = PackStoredCalibrationFilterParameterByName(response)
    return result


def ael_custom_dialog_main(parameters, dictExtra):
    #Unpack Filter parameters
    #No parameters used, hence nothing to unpack.
    columnCreator = parameters[_resultKey]
    
    #Unpack extra provided data for filter functions
    eii = dictExtra.At('customData')
    dict = eii.ExtensionObject()
    calibrationRowObjects = dict.At('calibrationRowObjects')
    
    calibrationCostFunctionsResult = dict.At('calibrationCostFunctionsResult')
    
    if columnCreator is None:
        return [calibrationCostFunctionsResult]
    
    calculationConfiguration = acm.Sheet().Column().CalculationSpecificationForColumn(columnCreator).Configuration()
    calibrationCostFunctionsResultDict = calibrationCostFunctionsResult.Results()

    for calibrationRowObject in calibrationRowObjects:
        calibrationCostFunctionResult = calibrationCostFunctionsResultDict.At(calibrationRowObject.Id())

        #Only possible to filter if calibrationRowObject has an instrument
        if not calibrationCostFunctionResult.Filtered() and calibrationRowObject.Instrument():
            try:
                calc = calibrationRowObject.Calculation(columnCreator.ColumnId(), calculationConfiguration)
                calc.Value()
            except Exception as e:
                calibrationCostFunctionResult.FilterReason("No " + columnCreator.ColumnId() + " Exist")  
    
    return [calibrationCostFunctionsResult]
