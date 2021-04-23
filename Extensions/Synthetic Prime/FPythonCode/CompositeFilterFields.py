import acm
import re
from collections import OrderedDict
from DealPackageDevKit import CompositeAttributeDefinition, AttributeDialog, Action, Object

class FilterFields(CompositeAttributeDefinition):
    def OnInit(self, **kwargs):
        self._attrDict = OrderedDict()
        
    def Attributes(self):
        i = 0
        for lbl, field in self.GetFilterFields().items():
            self._attrDict[field[0].lower() + field[1:]] = Object( label = lbl, 
                                                              objMapping = field
                                                              );
            i += 1
        return self._attrDict
    
    def GetFilterFields(self):
        filterFields = {}
        filterMaps = acm.DealCapturing.CreatePrfSwapFilterMaps()
        for filterMap in filterMaps:
            label = str(filterMap.First())
            criteriaPair = filterMap.Second()
            filterField = str(criteriaPair.First())
            filterField = re.sub(r'(\.Name$)|(\.Oid$)', '', filterField)
            filterFields[label] = filterField
        return filterFields
        
    def GetLayout(self):
        layout = 'vbox{;'
        for k in self._attrDict:
            layout += k + ';'
        layout += '};'
        return self.UniqueLayout(layout)
    
    def TabVisible(self, *args):
        return len(self._attrDict) > 0
    
