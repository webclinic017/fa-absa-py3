import AttributeMetaData
import copy
    
DEFAULT_ATTR_MAKER = AttributeMetaData.AttributeMetaData
attrCallbackMakerMap = {
    'action':                      AttributeMetaData.ActionAttribute,
    'actionList':                  AttributeMetaData.ActionListAttribute,
    'addNewItem':                  AttributeMetaData.AddNewListItemAttribute,
    'alignment':                   AttributeMetaData.AlignmentAttribute,
    'backgroundColor':             AttributeMetaData.ColorAttribute,
    'calcConfiguration':           AttributeMetaData.CalcConfigurationAttribute,
    'calcMapping':                 AttributeMetaData.NoPreArgsAttribute,
    'checkedItems':                AttributeMetaData.GetInfoAttribute,
    'choiceListSource':            AttributeMetaData.ChoiceListSourceAttribute,
    'columns':                     AttributeMetaData.ColumnsAttribute,
    'dialog':                      AttributeMetaData.GetInfoAttribute,
    'domain':                      AttributeMetaData.DomainAttribute,
    'editable':                    AttributeMetaData.EditableAttribute,
    'elementDomain':               AttributeMetaData.ElementDomainAttribute,
    'enabled':                     AttributeMetaData.BoolAttributeTrue,
    'formatter':                   AttributeMetaData.FormatterAttribute,
    'hasChoiceListSource':         AttributeMetaData.HasChoiceListSourceAttribute,
    'height':                      AttributeMetaData.WidthAttribute,
    'initialFocus':                AttributeMetaData.BoolAttributeFalse,
    'isCalculationSimulated':       AttributeMetaData.IsCalculationSimulatedAttribute,
    'label':                       AttributeMetaData.LabelAttribute,
    'labelColor':                  AttributeMetaData.LabelColorAttribute,
    'labelFont':                   AttributeMetaData.FontAttribute,
    'mandatory':                   AttributeMetaData.MandatoryAttribute,
    'maxHeight':                   AttributeMetaData.WidthAttribute,
    'maxWidth':                    AttributeMetaData.WidthAttribute,
    'name':                        AttributeMetaData.TraitNameAttribute,
    'noDealPackageRefreshOnChange': AttributeMetaData.NoDealPackageRefreshOnChangeAttribute,
    'onChanged':                   AttributeMetaData.OnChangedAttribute,
    'onDoubleClick':               AttributeMetaData.UxInteractionAttribute,
    'onItemCheckStateChanged':     AttributeMetaData.UxInteractionAttribute,
    'onRightClick':                AttributeMetaData.UxInteractionAttribute,
    'onSelectionChanged':          AttributeMetaData.UxInteractionAttribute,
    'isPassword':                  AttributeMetaData.BoolAttributeFalse,
    'sortIndexCallback':           AttributeMetaData.UxNonInteractionAttribute,
    'recreateCalcSpaceOnChange':    AttributeMetaData.RecreateCalcSpaceOnChangeAttribute,
    'showDropDownOnKeyDown':       AttributeMetaData.BoolAttributeFalse,
    'silent':                      AttributeMetaData.BoolAttributeFalse,
    'sizeToFit':                   AttributeMetaData.BoolAttributeFalse,
    'solverParameter':             AttributeMetaData.SolverParameterAttribute,
    'solverTopValue':              AttributeMetaData.SolverTopValueAttribute,
    'tabStop':                     AttributeMetaData.BoolAttributeTrue,
    'textColor':                   AttributeMetaData.ColorAttribute,
    'textFont':                    AttributeMetaData.FontAttribute,
    'tick':                         AttributeMetaData.TickAttribute,
    'toolTip':                     AttributeMetaData.ToolTipAttribute,
    'transform':                   AttributeMetaData.TransformAttribute,
    'type':                        AttributeMetaData.TraitTypeAttribute,
    'validate':                    AttributeMetaData.ValidateAttribute,
    'validateMapping':             AttributeMetaData.BoolAttributeTrue,
    'valuationDetails':            AttributeMetaData.BoolAttributeTrue,
    'vertical':                    AttributeMetaData.BoolAttributeTrue,
    'visible':                     AttributeMetaData.BoolAttributeTrue,
    'width':                       AttributeMetaData.WidthAttribute,
}

def AttributeMetaDataKeys():
    return attrCallbackMakerMap.keys()
    
def ValidAttributeMetaDataKeys():
    validKeys = attrCallbackMakerMap.keys()
    validKeys.append('objMapping')
    validKeys.append('attributeMapping')    
    return validKeys

def MetaDataMergePossible(metaDataKey):
    if metaDataKey in ValidAttributeMetaDataKeys():
        if metaDataKey in ('objMapping', 'attributeMapping'):
            return True
        else:
            return attrCallbackMakerMap[metaDataKey].SupportsCallableMultiMethodChain()
    else:
        return False
    
class AttributeMetaDataFactory(object):
    def __init__(self, definition):
        self._definition = definition
        
    def CreateMetaData(self, attribute, metaName):
        plainMetaValues = self._definition.complete_trait_metadata(attribute.get_name(), metaName)
        previous = None
        for plainMetaValue in plainMetaValues:
            if isinstance(plainMetaValue, AttributeMetaData.AttributeMetaData):
                toReturn = copy.copy(plainMetaValue)
            else:
                toReturn = attrCallbackMakerMap.get(metaName, DEFAULT_ATTR_MAKER )(plainMetaValue)
            self.__InitMetaData(toReturn, attribute, metaName, previous)
            previous = toReturn
        return toReturn
    
    def __InitMetaData(self, metaData, attribute, metaName, previous):
        metaData.SetDpDef(self._definition)
        metaData.SetTrait( attribute )
        metaData.SetAttributeName( metaName )
        if previous:
            metaData.SetPreviousCallback(previous.Callback())
