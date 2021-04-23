import acm
import FUxCore
import FUxUtils

_resultKey = acm.FSymbol('Mid')
_resultCostFunctionKey = acm.FSymbol('CostFunctionColumns')
_resultTargetColumnKey = acm.FSymbol('TargetColumnCreator')
_resultFunctionColumnKey = acm.FSymbol('FunctionColumnCreator')
_resultDerivativesAspectKey = acm.FSymbol('DerivativesAspect')
    
'''Select Cost functions Main Dlialog'''

class FCustomSelectCostFunctionDialog(FUxCore.LayoutDialog):

    _btnAddTargetColumnId = "btnAddTargetColumn"
    _inputTargetColumnId = "inputTargetColumn"
    _btnAddFunctionColumnId = "btnAddFunctionColumn"
    _inputFunctionColumnId = "inputFunctionColumn"
    
    def __init__(self, shell, initDict):
        self._shell = shell    
        self._resultDictionary = initDict.Clone() if initDict else acm.FDictionary()
    
    def HandleApply(self):
        return self._resultDictionary
           
    def HandleCreate(self, dlg, layout):
        self._fuxDlg = dlg
        self._layout = layout
        self._btnAddTargetColumn = layout.GetControl(self._btnAddTargetColumnId)
        self._inputTargetColumn = layout.GetControl(self._inputTargetColumnId)
        self._btnAddFunctionColumn = layout.GetControl(self._btnAddFunctionColumnId)
        self._inputFunctionColumnId = layout.GetControl(self._inputFunctionColumnId)
        
        self._inputTargetColumn.Editable(False)
        self._inputFunctionColumnId.Editable(False)
        
        self._btnAddTargetColumn.AddCallback('Activate',  self._OnTargetColumnClicked, None)
        self._btnAddFunctionColumn.AddCallback('Activate', self._OnFunctionColumnClicked, None)
        
        self.Populate()
        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()

        b.BeginVertBox()
        b.  BeginVertBox('Invisible')
        b.    BeginHorzBox()
        b.      AddInput(self._inputTargetColumnId, "Target Column")
        b.      AddButton(self._btnAddTargetColumnId, "...", False, True)
        b.    EndBox()
        b.    BeginHorzBox()
        b.      AddInput(self._inputFunctionColumnId, "Function Column")
        b.      AddButton(self._btnAddFunctionColumnId, "...", False, True)
        b.    EndBox()
        b.  EndBox()
        b.  BeginVertBox('Invisible')
        b.    BeginHorzBox()
        b.      AddSpace(100);
        b.      AddFill()
        b.      AddButton("ok", "OK")
        b.      AddButton("cancel", "Cancel")
        b.    EndBox()
        b.  EndBox()
        b.EndBox()
        return b
        
    def Populate(self):
        return None
        
    def UpdateControls(self):
        self._inputTargetColumn.SetData(self._resultDictionary.At(_resultTargetColumnKey))
        self._inputFunctionColumnId.SetData(self._resultDictionary.At(_resultFunctionColumnKey))
        
    def _ShowSelectColumnsDlg(self, type):
        sheetDefinition = acm.Sheet.GetSheetDefinition(acm.FPortfolioSheet)
        gridBuilder = sheetDefinition.CreateGridBuilder(False)
        
        result = acm.UX().Dialogs().SelectOneColumn(self._shell, acm.FPortfolioSheet, gridBuilder, acm.GetDefaultContext())
        
        return result
        
    def _OnTargetColumnClicked(self, ud, cd):
        result = self._ShowSelectColumnsDlg("");
        if result is not None:
            self._resultDictionary.AtPut(_resultTargetColumnKey, result)
            self.UpdateControls()

    def _OnFunctionColumnClicked(self, ud, cd):
        result = self._ShowSelectColumnsDlg("");
        if result is not None:
            self._resultDictionary.AtPut(_resultFunctionColumnKey, result)
            self.UpdateControls()

def UnpackStoredCalibrationParametersByName(initDict):
    resultMidDict = initDict.At(_resultKey)
    return resultMidDict.At(_resultCostFunctionKey), resultMidDict.At(_resultDerivativesAspectKey)
    
def PackStoredCalibrationParametersByName(costFunctionDict):
    resultMidDict = acm.FDictionary()
    resultMidDict.AtPut(_resultCostFunctionKey, costFunctionDict)
    resultMidDict.AtPut(_resultDerivativesAspectKey, None)
    
    resultDict = acm.FDictionary()
    resultDict.AtPut(_resultKey, resultMidDict)
    
    return resultDict
    
def GetColumns():
    
    result = acm.FArray()
    context = acm.GetDefaultContext()
    
    targetColumns = context.GetAllExtensions(acm.FColumnDefinition, acm.FTradingSheet, True, True, "sheet columns", "calibrationtarget")
    functionColumns = context.GetAllExtensions(acm.FColumnDefinition, acm.FTradingSheet, True, True, "sheet columns", "calibrationfunction")
    
    result.AddAll(targetColumns).AddAll(functionColumns)
    
    return result

def ael_custom_dialog_show(shell, params):

    result = None
    #columns = GetColumns()

    initData = FUxUtils.UnpackInitialData(params)
    
    costFunctionColumns = None
    derivativesAspect = None
    
    if initData:
        costFunctionColumns, derivativesAspect = UnpackStoredCalibrationParametersByName(initData)
    else:
        costFunctionColumns = acm.FDictionary()
        
    customDlg = FCustomSelectCostFunctionDialog(shell, costFunctionColumns)
    costFunctionDict = acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)
    
    if costFunctionDict is None:
        result = initData
    else:    
        result = PackStoredCalibrationParametersByName(costFunctionDict)
    
    return result
  
def ael_custom_dialog_main( parameters, dictExtra ):
    
    #Unpack Filter parameters
    columnsCreatorsDictionary, derivativesAspect = UnpackStoredCalibrationParametersByName(parameters)
    
    return [columnsCreatorsDictionary, derivativesAspect]
