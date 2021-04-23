import PaceVariantTools as VariantTools

def ToUnicode(inputString):
    return str(inputString, 'cp1251')

def AssignVariantValue(target, source, valueMethod ):
    valueMethod(target, source)

def AssignString(target, source ):
    VariantTools.AssignString(target, ToUnicode(source) )

def AssignDouble(target, source ):
    VariantTools.AssignDouble(target, source )

def AssignBool(target, source ):
    VariantTools.AssignBool(target, source )
    
def AssignInt32(target, source ):
    VariantTools.AssignInt32(target, source )

def AssignInt64(target, source ):
    VariantTools.AssignInt64(target, source )



class LookupServicePluginBase(object):

    def InitializePlugin(self):
        raise StandardError( "LookupServicePluginBase: Plugin provider is missing method: InitializePlugin.")
        
    def GetPluginName(self):
        raise StandardError( "LookupServicePluginBase: Plugin provider is missing method: GetPluginName.")
    
    def GetProviders(self):
        raise StandardError( "LookupServicePluginBase: Plugin provider is missing method: GetProviders.")
        
class LookupServicePluginProviderBase(object):

    def GetTableName(self):
        raise StandardError( "LookupServicePluginProviderBase: Plugin provider is missing method: GetTableName.")
        
    def LookupTableObject(self, providedAttributes):
        tableRow = None
        usedIndexAttribute = None
        raise StandardError( "LookupServicePluginProviderBase: Plugin provider is missing method: LookupTableObject.")
        return tableRow, usedIndexAttribute      

    def BuildResult(self, definition, tableRow, usedAttribute): 
        keyValues = []        
        raise StandardError( "LookupServicePluginProviderBase: Plugin provider is missing method: BuildResult.")
        return keyValues
