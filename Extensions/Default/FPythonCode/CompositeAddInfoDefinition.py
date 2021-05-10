import acm
from DealPackageDevKit import CompositeAttributeDefinition, AttributeDialog, Action, Object, ReturnDomainDecorator, Str, DealPackageChoiceListSource

class AddInfoDefinition(CompositeAttributeDefinition):
    def OnInit(self, obj, **kwargs):
        self._obj = obj
        self._selectedSpec = acm.FAdditionalInfoSpec()
        self._editValueChoices = acm.FArray()
        
    def Attributes(self):
        return { 'addInfoSpecs'         : Object( label='Additional Infos',
                                                  objMapping=self._obj+'.AddInfoSpecs',
                                                  columns=[{'methodChain': 'FieldName',      'label': 'Name'}],
                                                  onSelectionChanged=self.UniqueCallback('@SetSelectedSpec'),
                                                  dialog=AttributeDialog( label='Set Value', 
                                                                          customPanes=self.UniqueCallback('@SetAddInfoDialogCustomPanes'))),
                 'addInfos'             : Object( label='Values',
                                                  objMapping=self._obj+'.AddInfos',
                                                  columns=[{'methodChain': 'AddInf.FieldName',      'label': 'Additional Info'},
                                                           {'methodChain': 'FieldValue',            'label': 'Value'}],
                                                  onSelectionChanged=self.UniqueCallback('@SetSelectedAddInfo'),
                                                  dialog=AttributeDialog( label='Set Value', 
                                                                          customPanes=self.UniqueCallback('@SetAddInfoDialogCustomPanes'))),
                 'selectedFieldName'    : Object( label='Spec',
                                                  objMapping=self.UniqueCallback('SelectedSpec')+'.FieldName',
                                                  enabled=False),
                 'selectedDataTypeGroup': Object( label='Group',
                                                  objMapping=self.UniqueCallback('SelectedSpec')+'.DataTypeGroup',
                                                  choiceListSource=None,
                                                  enabled=False),
                 'selectedDataDomain'   : Object( label='Type',
                                                  objMapping=self.UniqueCallback('SelectedSpec')+'.DataDomain',
                                                  choiceListSource=None,
                                                  enabled=False),
                 'editValue'            : Object( label='Value',
                                                  objMapping=self.UniqueCallback('EditValue'),
                                                  width=50),
                 'editValueChoices'     : Object( label='Choices',
                                                  objMapping=self.UniqueCallback('EditValueChoices'),
                                                  columns=[{'methodChain': 'Value',      'label': 'Name'}],
                                                  onSelectionChanged=self.UniqueCallback('@SetSelectedEditValue'),
                                                  visible=self.UniqueCallback('@EditValueChoicesVisible'))
               }
    
    # Visible callbacks 
    def EditValueChoicesVisible(self, attributeName):
        return len(self.EditValueChoices()) > 0
    
    # OnSelctionChanged callbacks     
    def SetSelectedSpec(self, attrName, selectedSpec):
        self._selectedSpec = selectedSpec
        self.UpdateEditValueChoices()
        
    def SetSelectedAddInfo(self, attrName, selectedAddInfo):
        self._selectedSpec = selectedAddInfo and selectedAddInfo.AddInf()
        self.UpdateEditValueChoices()
        
    def SetSelectedEditValue(self, attrName, selectedEditValue):
        self.editValue = selectedEditValue.Name() if hasattr(selectedEditValue, 'Name') else selectedEditValue
     
    # Util
    def SelectedSpec(self):
        return self._selectedSpec
        
    def UpdateEditValueChoices(self):
        self._editValueChoices.Clear()
        choices = []
        if self.SelectedSpec():
            domain = self.SelectedSpec().DataDomain()
            if hasattr(domain, 'Choices') and len(domain.Choices()):
                choices = domain.Choices().split('\n')
            elif hasattr(domain, 'InstancesKindOf'):
                choices = domain.InstancesKindOf()
            self._editValueChoices.AddAll(choices)
    
    @ReturnDomainDecorator('FArray')
    def EditValueChoices(self, value = '*Reading*'):
        if value == '*Reading*':
            return self._editValueChoices
            
    @ReturnDomainDecorator('string')
    def EditValue(self, value = '*Reading*'):
        if self.SelectedSpec():
            if value == '*Reading*':
                value = self.Object().AddInfoValue(self.SelectedSpec())
                return value.Name() if hasattr(value, 'Name') else value
            else:
                self.Object().AddInfoValue(self.SelectedSpec(), value)
            
    def Object(self):
        return self.GetMethod(self._obj)()
    
    def GetLayout(self):
        return self.UniqueLayout(
                    """
                    hbox(;
                        addInfoSpecs;
                        addInfos;
                    );
                    """
                )
                
    def SetAddInfoDialogCustomPanes(self, attrName):
        layout = self.UniqueLayout(
                    """
                    selectedFieldName;
                    selectedDataTypeGroup;
                    selectedDataDomain;
                    editValue;
                    editValueChoices;
                    """
                )
        return [{'Edit Value' : layout}]
