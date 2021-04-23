from __future__ import print_function
import acm, FVaRFileParsing
 
import FUxCore
import RiskFactorUtils
from RiskFactorUtils import s_supportedRiskFactorMappingTypes

s_supportedRiskFactorMappingTypes = sorted(s_supportedRiskFactorMappingTypes, key=str.lower, reverse=False)

s_empty = '    '
s_defaultDisplayTypes = acm.FEnumeration['eShiftDisplayType'].Enumerators()

FILE_TYPES = ("Text Files (*.txt)|*.txt|"
                "All Files (*.*)|*.*")


def ReallyStartDialog(shell, params):
    builder = CreateLayout()
    initialData = params.At('initialData')

    customDlg = RiskScenarioFromFileDialog(initialData)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg )
      

def OnRiskFactorSetupChanged(self, cd):
    riskFactorSetup = self.m_riskFactorSetup.GetData()
    self.PopulateRiskFactorSetupAttribute(riskFactorSetup)
    self.m_riskFactorCollectionAttributeValue.Enabled( False )
    self.m_riskFactorCollectionAttributeValue.SetData('')
    
def OnRiskFactorSetupAttributeChanged(self, cd):
    riskFactorAttribute = self.m_riskFactorCollectionAttribute.GetData()
    self.PopulateRiskFactorSetupAttributeValue(riskFactorAttribute)
    
    if not (riskFactorAttribute is None or riskFactorAttribute == s_empty):
        insertionItem = self.m_riskFactorCollectionAttributeValue.GetItemAt(0)
        
        if riskFactorAttribute == 'Name':
            insertionItem = sorted(self.m_riskFactorSetup.GetData().RiskFactorCollections())[0] #always the first risk factor collection.

        self.m_riskFactorCollectionAttributeValue.SetData(insertionItem)      
        self.m_riskFactorCollectionAttributeValue.Enabled( True )

def OnFileNameClicked(self, cd):
    selection = acm.FFileSelection()
    selection.FileFilter = FILE_TYPES
    isSelected = acm.UX().Dialogs().BrowseForFile(self.m_fuxDlg.Shell(), selection)
    
    if isSelected:
        self.m_filePath.SetData(selection.SelectedFile())
    
def OnNameChanged(self, cd):
    if not self.m_nameEdit.GetData():
        self.m_ok.Enabled(False)
    else:
        self.m_ok.Enabled(True)

class RiskScenarioFromFileDialog (FUxCore.LayoutDialog):
    def __init__(self, initialData):
        self.m_initialData = initialData
        self.m_riskFactorCollectionAttribute = None
        self.m_riskFactorCollectionAttributeValue = None
        self.m_okBtn = None
        self.m_nameEdit = None
        self.m_fuxDlg = None
        self.m_dispType = None
        self.m_riskFactorSetup = None
        self.m_scenarioFile = None
        self.m_colStart = None
        self.m_colEnd = None
        self.m_colDelimiter = None
        self.m_commentChar = None
        self.m_fileName = None
        self.m_filePath = None
        
    def HandleApply( self ):
        data = {}
        scenDict = {}
        
        data['Name'] = self.m_nameEdit.GetData()
        data['ShiftDisplayType'] = self.m_dispType.GetData()
        
        scenDict['riskFactorSetup'] = self.m_riskFactorSetup.GetData()
        scenDict['Attribute'] = self.m_riskFactorCollectionAttribute.GetData()
        scenDict['Value'] = self.m_riskFactorCollectionAttributeValue.GetData()
        scenDict['file'] = self.m_filePath.GetData()
        scenDict['startIndex'] = self.m_colStart.GetData()
        scenDict['endIndex'] = self.m_colEnd.GetData()
        scenDict['delimiterChar'] = self.m_colDelimiter.GetData()
        scenDict['commentChar'] = self.m_commentChar.GetData()
        
        data['Parameters'] = scenDict
        
        validInput, msg = self.Validate()
        
        if not validInput:
            acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), msg)
            
        return data if validInput else None
    
    def Validate( self ):
    
        validInput = True
        msg = ''
        npfi = 'not properly filled in.'
        
        if validInput and not self.m_nameEdit.GetData():
            validInput = False
            msg = 'Name field ' + npfi
        elif validInput and not self.m_dispType.GetData():
            validInput = False
            msg = 'Display type ' + npfi
        elif validInput and not self.m_riskFactorSetup.GetData():
            validInput = False
            msg = 'Risk Factor Setup ' + npfi
        elif validInput and (not self.m_filePath.GetData() or self.m_filePath.GetData() == '' ):
            validInput = False
            msg = 'Scenario File ' + npfi
        elif validInput and not(self.m_colStart.GetData() and self.m_colEnd.GetData()) : 
            validInput = False
            msg = 'Column End or Column Start ' + npfi
        elif validInput and not(self.m_colDelimiter.GetData() and self.m_commentChar.GetData()):
            validInput = False
            msg = 'Column Delimiter or Comment Character ' + npfi
        elif validInput and (self.m_colStart.GetData() or self.m_colEnd.GetData()):
            validInput, msg = self.ControlStartAndEndIndex()
        
        if validInput and msg == '' and (self.m_colDelimiter.GetData() or self.m_commentChar.GetData()) :
            validInput, msg = self.ControlChararacterInput()

        return validInput, msg
    
    def ControlChararacterInput(self):
        validInput = True
        msg = ''
        if not (len(self.m_colDelimiter.GetData()) == 1 and len(self.m_commentChar.GetData()) == 1):
            validInput = False
            msg = 'Comment Character and Column Delimiter fields must contain one character.'
            
        return validInput, msg
    
    def ControlStartAndEndIndex(self):
        validInput = True
        msg = ''
        try:
            start = self.m_colStart.GetData()
            end = self.m_colEnd.GetData()
            int(start)
            int(end)
            if start > end:
                validInput = False
                msg = 'Column Start field input must be less than or equal to Column End field input.'
        except:
            validInput = False
            msg = 'Column Start and Column End fields must have integer input.'
        
        return validInput, msg
            
            
    def PopulateRiskFactorSetupAttributeValue(self, riskFactorAttribute): 
        collectionAttributeValues = []
        riskFactorSetup = self.m_riskFactorSetup.GetData()
        
        if riskFactorAttribute == s_empty:
            OnRiskFactorSetupChanged(self, 5)
            return
        elif riskFactorAttribute == 'Name' :
            for collection in riskFactorSetup.RiskFactorCollections():
                collectionAttributeValues.append(collection)
     
        elif riskFactorAttribute == 'Risk Factor Type':
            collectionAttributeValues = s_supportedRiskFactorMappingTypes
        elif acm.FAdditionalInfoSpec[riskFactorAttribute] and str(acm.FAdditionalInfoSpec[riskFactorAttribute].ClassName()) == 'FAdditionalInfoSpec':
            if acm.FAdditionalInfoSpec[riskFactorAttribute].DataDomain().IsEnum():
                collectionAttributeValues = acm.FAdditionalInfoSpec[riskFactorAttribute].DataDomain().Enumerators()
            else:
                for collection in riskFactorSetup.RiskFactorCollections():
                    if collection.add_info(acm.FAdditionalInfoSpec[riskFactorAttribute].Value()) not in collectionAttributeValues:
                        collectionAttributeValues.append(str(collection.add_info(acm.FAdditionalInfoSpec[riskFactorAttribute].Value())))

        self.m_riskFactorCollectionAttributeValue.Clear()
        collectionAttributeValues = sorted(collectionAttributeValues)
        '''
        use populate to insert instances, 
        AddItem to insert string representation of instance
        '''
        if riskFactorAttribute == 'Name':
            self.m_riskFactorCollectionAttributeValue.Populate(collectionAttributeValues)
        else:
            for s in collectionAttributeValues:
                self.m_riskFactorCollectionAttributeValue.AddItem(s) 

    def PopulateRiskFactorSetupAttribute(self, riskFactorSetup) :
        self.m_riskFactorCollectionAttribute.Clear()
        self.m_riskFactorCollectionAttribute.AddItem(s_empty)
        self.m_riskFactorCollectionAttribute.AddItem('Name')
        self.m_riskFactorCollectionAttribute.AddItem('Risk Factor Type')
        
        collectionAttributes = []
        for item in RiskFactorUtils.GetAddInfoSpecsFromRiskFactorSetup(riskFactorSetup, 'RiskFactorCollection', False):
            collectionAttributes.append(item)
        
        collectionAttributes = sorted(collectionAttributes)
        
        for item in collectionAttributes: 
            self.m_riskFactorCollectionAttribute.AddItem(item)
        
        self.m_riskFactorCollectionAttribute.SetData(s_empty)

    def PopulateData(self):
        riskFactorSetups = acm.FRiskFactorSetup.Select('')
        self.m_riskFactorSetup.Populate(riskFactorSetups)
        for s in s_defaultDisplayTypes:
            self.m_dispType.AddItem(s)
        
        initialName = self.m_initialData.At('Name')
        initialShiftDisplayType = self.m_initialData.At('ShiftDisplayType')
        initialParams = self.m_initialData.At('Parameters')
  
        self.m_nameEdit.SetData(initialName)
        self.m_dispType.SetData(initialShiftDisplayType)     
        
        if initialParams :
            riskFactorSetup = initialParams['riskFactorSetup']   
            self.m_riskFactorSetup.SetData(riskFactorSetup)
            if riskFactorSetup:
                self.PopulateRiskFactorSetupAttribute(riskFactorSetup)
                
                riskFactorAttribute = initialParams['Attribute']
                if not riskFactorAttribute == s_empty and self.m_riskFactorCollectionAttribute.ItemExists(riskFactorAttribute):
                    self.m_riskFactorCollectionAttribute.SetData(riskFactorAttribute)
                    self.PopulateRiskFactorSetupAttributeValue(riskFactorAttribute)
                    self.m_riskFactorCollectionAttributeValue.SetData(initialParams['Value'])
                    self.m_riskFactorCollectionAttributeValue.Enabled( True )
                
            self.m_filePath.SetData(initialParams['file'])
            self.m_colStart.SetData(initialParams['startIndex'])
            self.m_colEnd.SetData(initialParams['endIndex'])
            specHeader = acm.Risk().MappedRiskFactorSpecHeader().Parameter()
            if initialParams['delimiterChar']:
                self.m_colDelimiter.SetData(initialParams['delimiterChar'])
            else:
                self.m_colDelimiter.SetData(specHeader.DelimiterChar())
                
            if initialParams['commentChar']:
                self.m_commentChar.SetData(initialParams['commentChar'])
            else: 
                self.m_commentChar.SetData(specHeader.CommentChar())
                
        else :
            self.m_colDelimiter.SetData(',')
            self.m_commentChar.SetData('*')
        
            self.m_dispType.SetData(s_defaultDisplayTypes[0])
            
            self.m_colStart.SetData(0)
            self.m_colEnd.SetData(0)

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Scenario Editor')
        self.m_nameEdit = layout.GetControl("name")
        self.m_dispType = layout.GetControl("defaultDispType")
        self.m_riskFactorSetup = layout.GetControl('riskFactorSetup')
        self.m_colStart = layout.GetControl('colStart')
        self.m_colEnd = layout.GetControl('colEnd')
        self.m_colDelimiter = layout.GetControl('colDelimiter')
        self.m_commentChar = layout.GetControl('commentChar')
        self.m_riskFactorCollectionAttribute = layout.GetControl('riskFactorSetupAttribute')
        self.m_riskFactorCollectionAttributeValue = layout.GetControl('riskFactorSetupAttributeValue')
        self.m_fileName = layout.GetControl('fileName')
        self.m_filePath = layout.GetControl('filePath')
        self.m_ok = layout.GetControl('ok')
        
        self.m_nameEdit.Enabled(self.m_initialData.At('AllowChangeName'))

        layout.GetControl('filePath').ToolTip('The name or path to an external scenario file.')
        layout.GetControl('riskFactorSetup').ToolTip('The Risk Factor Setup, repository for the Risk Factors.')
        layout.GetControl('riskFactorSetupAttribute').ToolTip('The Risk Factor Collection attribute.')
        layout.GetControl('riskFactorSetupAttributeValue').ToolTip('The Risk Factor Collection attribute value.')
        layout.GetControl('colStart').ToolTip('The starting column used in the external scenario file.')
        layout.GetControl('colEnd').ToolTip('The ending column used in the external scenario file.')
        layout.GetControl('colDelimiter').ToolTip('The column delimiter character used in the external scenario file.')
        layout.GetControl('commentChar').ToolTip('The comment character used in the external scenario file.')

        self.m_riskFactorCollectionAttributeValue.Enabled( False )

        self.m_riskFactorSetup.AddCallback('Changed', OnRiskFactorSetupChanged, self) 
        self.m_riskFactorCollectionAttribute.AddCallback('Changed', OnRiskFactorSetupAttributeChanged, self) 
        self.m_fileName.AddCallback('Activate', OnFileNameClicked, self)
        self.m_nameEdit.AddCallback('Changed', OnNameChanged, self)
        
        self.PopulateData()

def FilteredRiskFactorCollections(scenDict):
    searchKeys = ['Attribute', 'Value']
    if scenDict and not all(elem in list(scenDict.Keys()) for elem in searchKeys):
        #Legacy setup, will use all collections present.
        if scenDict.HasKey('riskFactorSetup'):
            return scenDict['riskFactorSetup'].RiskFactorCollections()
                
        #Setup without risk factor setup, should never happen.
        raise Exception('Risk Factor Setup not found.')

    collectionsList = []
    filterAttribute = scenDict['Attribute']
    filterValue = scenDict['Value']
    
    if filterAttribute == 'Name':
        for col in scenDict['riskFactorSetup'].RiskFactorCollections():
            if col == filterValue:
                collectionsList = [col]
                break
    else:
        for collection in scenDict['riskFactorSetup'].RiskFactorCollections():
            if filterAttribute == 'Risk Factor Type':
                if collection.RiskFactorType() == filterValue:
                    collectionsList.append(collection)
            elif filterAttribute == s_empty or (collection.add_info(filterAttribute) == filterValue):
                collectionsList.append(collection)
                
    return collectionsList

def CreateLayout():
    b = acm.FUxLayoutBuilder()
    b.BeginVertBox('None')
    b.  AddInput('name', 'Name')
    b.  AddOption('defaultDispType', 'Default Display Type')
    b.  BeginVertBox('EtchedIn', '')
    b.    BeginHorzBox('None')
    b.      AddOption('riskFactorSetup', 'Risk Factor Setup*:')
    b.    EndBox()
    b.    BeginHorzBox('None')
    b.      AddOption('riskFactorSetupAttribute', 'Attribute:')
    b.    EndBox()
    b.    BeginHorzBox('None')
    b.      AddOption('riskFactorSetupAttributeValue', 'Value:')
    b.    EndBox()
    b.  EndBox()
    b.  BeginVertBox('EtchedIn', '')
    b.    BeginHorzBox('None')
    b.      AddInput('filePath', 'Scenario File*:')
    b.      AddButton('fileName', '...', False, True)
    b.    EndBox()
    b.    AddInput('colStart', 'Column Start*:')
    b.    AddInput('colEnd', 'Column End*:')
    b.    AddInput('colDelimiter', 'Column Delimiter*:')
    b.    AddInput('commentChar', 'Comment Character*:')
    b.  EndBox()
    b.  BeginHorzBox('None')
    b.    AddSpace(200)
    b.    AddFill()
    b.    AddButton('ok', 'OK')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    b.EndBox()
    return b
    
def CreateScenario(scenDict, dictExtra) :
    delimiterChar = scenDict['delimiterChar']
    commentChar = scenDict['commentChar'] 
    scenarioFile = scenDict['file']
    startIndex = scenDict['startIndex'] 
    endIndex = scenDict['endIndex']
    riskFactorSetup = scenDict['riskFactorSetup']
    
    if delimiterChar and commentChar:
        fileData = FVaRFileParsing.create_scenario_file_data(scenarioFile, delimiterChar, commentChar)
    else:
        #Backwards compatibility, using Risk Factor Spec Header
        if not scenarioFile:
            raise Exception('Scenario File Not found.')
        fileData = FVaRFileParsing.scenario_file_data(scenarioFile)
        
    if not riskFactorSetup:
            raise Exception('Risk Factor Setup not found.')
            
    collectionsList = FilteredRiskFactorCollections(scenDict)

    dateToday = acm.Time().DateNow()
    if not fileData:
        print ('No file found! ', file)
    else:
        riskFactorCreatorCache = acm.RiskFactor.CreatorCache()
        if not startIndex or startIndex < 0:
            startIndex = 0
        if not endIndex or endIndex < 0:
            endIndex = 0
        if endIndex < startIndex:
            raise Exception('Column End < Column Start')

        scenarioBuilder = acm.FScenarioBuilder()
        riskFactors = []
        for collection in collectionsList:
            for riskFactorInstance in collection.RiskFactorInstances():
                externalId = acm.FSymbol(acm.RiskFactor.RiskFactorExternalId(riskFactorInstance))
                if fileData.HasKey(externalId):
                    riskFactors.append(acm.RiskFactor.RiskFactorFromRiskFactorInstance(riskFactorInstance, externalId, riskFactorCreatorCache, dateToday))

        if len(riskFactors):
            scenario = scenarioBuilder.CreateScenario(riskFactors, fileData, startIndex, endIndex)
            print ('Created scenario resulting in ' +  str(len(riskFactors)) + ' risk factors.')
        else:
            scenario = scenarioBuilder.CreateScenario()
            scenarioBuilder.CreateScenarioDimension(scenario)
            print ('Empty scenario created, no risk factors found.')
            
    return scenario
    

def ael_custom_dialog_show(shell, params):
    return ReallyStartDialog(shell, params)
    
    
def ael_custom_dialog_main(parameters, dictExtra):
    return CreateScenario(parameters, dictExtra)

