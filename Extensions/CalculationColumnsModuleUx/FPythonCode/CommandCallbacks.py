
import acm

from MeasureSpecificationGenerator import Contributor

import DisplayCurrencyParameterization
import VectorContributorDialog
import VectorDimensionSelectDialog

def DimensionParameterization( dimension ):
    if dimension[acm.FSymbol("Type")]:
        if str( dimension[acm.FSymbol("Type")] ) == "Bucket":
            return "Bucket"
        if dimension[acm.FSymbol("VectorTypes")]:
            return str(dimension[acm.FSymbol("VectorTypes")])
        if dimension[acm.FSymbol("VectorParameterGUIDefinition")]:
            return str(dimension[acm.FSymbol("VectorParameterGUIDefinition")])
    return None

def DimensionsHaveSameCoordinates( dimension1, dimension2 ):
    if not dimension2:
        return True
    if DimensionParameterization( dimension1 ) and DimensionParameterization( dimension2 ):
        return DimensionParameterization( dimension1 ) == DimensionParameterization( dimension2 )
    return True

def DimensionsFromColumnId( columnId, namesAndDimensions ):
    liveColDef = acm.Risk.CreateLiveColumnDefinition( columnId, acm.ExtensionTools().GetDefaultContext().Name() )
    if liveColDef.OptionalDimensionDefinitionsByLogicalName():
        for logicalName in liveColDef.OptionalDimensionDefinitionsByLogicalName():
            currentDimension = namesAndDimensions[str(logicalName)]
            if DimensionsHaveSameCoordinates( liveColDef.OptionalDimensionDefinitionsByLogicalName()[logicalName], currentDimension ):
                namesAndDimensions[str(logicalName)] = liveColDef.OptionalDimensionDefinitionsByLogicalName()[logicalName]

customContributorTemplates = {
    "FRTB SA" : ["FRTBMeasureContributorDialog", "FRTBMeasureSpecificationGenerator"],
    "Risk Factor Delta" : ["RiskFactorDeltaContributorDialog", "RiskFactorDeltaSpecificationGenerator"],
    "Display Currencies" : ["DisplayCurrencyContributorDialog", "DisplayCurrencyContributorGenerator"]
    }

class Column( object ):

    @staticmethod
    def Enabled( self, ud ):
        return True

    @staticmethod
    def ShowDialog( self, contributorType = None, source = None):
        sheetDefinition = acm.Sheet.GetSheetDefinition(acm.FPortfolioSheet)
        gridBuilder = sheetDefinition.CreateGridBuilder(False)
        creators = acm.FColumnCreators()
        creators = acm.UX().Dialogs().SelectColumns(self.m_shell, creators, acm.FPortfolioSheet, 'positionsheet')
        return [creators.At(i) for i in range(creators.Size())]

    @staticmethod
    def ContributorsFromSource( columnCreator ):
        contributors = []
        columnContributor = Contributor(acm.FDictionary())
        columnContributor.m_type = "Column"
        columnContributor.m_displayName = columnCreator.Template().ColumnName()
        columnContributor.m_columnId = columnCreator.Template().ColumnId()
        contributors.append( columnContributor )
        
        if columnCreator.Configuration():
            contributor = Contributor(acm.FDictionary())
            contributor.m_type = "Parameters"
            contributor.m_parameters = columnCreator.Configuration().ParamDict()['columnParameters']
            contributors.append( contributor )
            
        liveColDef = columnCreator.Template().LiveColumnDefinition()
        if liveColDef.DimensionDefinitions():
            contributor = Contributor(acm.FDictionary())
            contributor.m_type = "Vector"
            contributor.m_vectors = []
            
            for dimDefLogicalName in liveColDef.DimensionDefinitionsByLogicalName().Keys():
                dimDef = liveColDef.DimensionDefinitionsByLogicalName()[ dimDefLogicalName ]
                dimensionParameterization = DimensionParameterization( dimDef )
                coordinatesSource = None
                if dimensionParameterization:
                    coordinatesSource = columnCreator.ConfiguredVectorSource()
                vectorConfig = acm.FDictionary()
                vectorConfig["logicalDimensionName"]  = str(dimDefLogicalName)
                vectorConfig["coordinatesParams"] = coordinatesSource
                contributor.m_vectors.append( vectorConfig )
                contributor.m_displayName = dimDefLogicalName
            contributors.append( contributor )

        return contributors
  
class Parameter( object ):
        
    @staticmethod
    def Enabled( self, ud ):
        return self.ValidParameterNamesForSelection() is not None

    @staticmethod
    def ShowDialog( self, contributorType, source ):
        validParameterNames = self.ValidParameterNamesForSelection()
        
        params = acm.FDictionary()
        params[acm.FSymbol( 'columnParameters' )] = acm.FArray()
        for paramName in validParameterNames:
            paramDef = acm.ExtensionTools().GetDefaultContext().GetExtension( acm.FColumnParameterDefinition, acm.FObject, paramName ).Value()
            params[acm.FSymbol( 'columnParameters' )].Add( paramDef )
        params[ acm.FSymbol('columnParameterNamesAndInitialValues') ] = source
        params[ acm.FSymbol( 'enableLabelInput' ) ] = False
        dlg = DisplayCurrencyParameterization.DisplayCurrencyParameterizationDialog( params )

        paramCreatorConfig = acm.UX().Dialogs().ShowCustomDialogModal( self.m_shell, dlg.CreateLayout(), dlg)
        return paramCreatorConfig and [paramCreatorConfig] or []

    @staticmethod
    def ContributorsFromSource( paramCreatorConfig ):
        contributor = Contributor( acm.FDictionary() )
        contributor.m_displayName = str(paramCreatorConfig['columnCreatorConfiguration'].ParamDict()['columnName'])
        contributor.m_parameters = paramCreatorConfig['columnCreatorConfiguration'].ParamDict()['columnParameters']
        contributor.m_type = "Parameters"
        return [contributor]
    
    @staticmethod
    def SourceFromContributor( contributor ):
        return contributor.m_parameters
        
class Scenario( object ):

    @staticmethod
    def Enabled( self, ud ):
        return True

    @staticmethod
    def ShowDialog( self, contributorType, source ):
    
        def LogicalDimensionNames( dimensionDefintion ):
            defaultExtName = dimDef[ acm.FSymbol("DefaultExternalName") ]
            prefixes = ["", "Cross "]
            return [acm.FSymbol( prefix + str(defaultExtName) ) for prefix in prefixes]
            
        scenario = acm.UX().Dialogs().SelectScenario( self.m_shell, source )
        if scenario:
            groupsByScenarioId = scenario.DynamicDimensionGroups()
            vectorConfigs = []
            for scenarioId in groupsByScenarioId:
                for group in groupsByScenarioId[scenarioId]:
                    namesAndDimensions = acm.FDictionary()
                    dimDefs = acm.ExtensionTools().GetDefaultContext().GetAllExtensions(
                        acm.FColumnDimensionDefinition,
                        acm.FObject,
                        False,
                        True,
                        'position sheet dimensions',
                        group,
                        True
                    )
                    for dimDef in dimDefs:
                        if not namesAndDimensions:
                            namesAndDimensions = acm.FDictionary()
                        for extName in LogicalDimensionNames( dimDef ):
                            if namesAndDimensions[extName]:
                                namesAndDimensions[extName].Add( dimDef )
                            else:
                                namesAndDimensions[extName] = acm.FArray()
                                namesAndDimensions[extName].Add( dimDef )
                    dlg = VectorDimensionSelectDialog.VectorDimensionSelectDialog(
                        namesAndDimensions,
                        None
                    )
                    vectorConfig = acm.UX().Dialogs().ShowCustomDialogModal(
                        self.m_shell, 
                        dlg.CreateLayout(),
                        dlg
                    )
                    if vectorConfig:
                        receivers = acm.FArray()
                        receivers.Add( scenarioId )
                        vectorConfig["receivers"] = receivers
                        vectorConfigs.append( vectorConfig )
            return [(scenario, vectorConfigs)]
        return scenario and [(scenario, [])] or None

    @staticmethod
    def ContributorsFromSource( scenarioAndVectorConfigs ):
        contributor = Contributor(acm.FDictionary())
        scenario = scenarioAndVectorConfigs[0]
        contributor.m_displayName = scenario.Name()
        contributor.m_scenario = scenario.ScenarioStorage()
        contributor.m_type = "Scenario"
        
        contributors = [contributor]

        vectorConfigs = scenarioAndVectorConfigs[1]
        for vectorConfig in vectorConfigs:
            contributor = Contributor(acm.FDictionary())
            contributor.m_type = "Vector"
            contributor.m_displayName = acm.FSymbol(str(vectorConfig["logicalDimensionName"]) + " [" + scenario.Name() + "]")
            contributor.m_vectors = [vectorConfig]
            contributors.append( contributor )
        return contributors
        
    @staticmethod
    def SourceFromContributor( contributor ):
        return contributor.m_scenario
        
class Vector( object ):
        
    @staticmethod
    def Enabled( self, ud ):
        validDimensions = self.ValidDimensionForSelection()
        return len(validDimensions) > 0

    @staticmethod
    def ShowDialog( self, contributorType, source ):
        namesAndDimensions = self.ValidDimensionForSelection()
        dlg = VectorContributorDialog.AddVectorContributorDialog( self.m_shell, namesAndDimensions, source )
       
        vectorConfig = acm.UX().Dialogs().ShowCustomDialogModal( self.m_shell, 
            dlg.CreateLayout(),
            dlg
            )
        return vectorConfig and [vectorConfig] or None

    @staticmethod
    def ContributorsFromSource( vectorConfig ):
        contributor = Contributor( acm.FDictionary() )
        contributor.m_displayName = vectorConfig["name"]

        if not contributor.m_displayName :
            contributor.m_displayName = vectorConfig["logicalDimensionName"]

        coordinatesParams = vectorConfig['coordinatesParams']
        if coordinatesParams :
            name = coordinatesParams.Name()
            if name and name != 'nil':
                contributor.m_displayName += ': ' + name

        contributor.m_vectors = [vectorConfig]
        contributor.m_type = "Vector"
        return [contributor]
        
    @staticmethod
    def SourceFromContributor( contributor ):
        return contributor.m_vectors[0]

class Custom( object ):
    
    @staticmethod
    def Enabled( self, ud ):
        generatorModule = __import__( customContributorTemplates[ud][1] )
        enabled = generatorModule.DefinesColumn()
        if not enabled and self.SelectionDefinesColumns():
            enabled = not generatorModule.DefinesColumn()
        return enabled    

    @staticmethod
    def ShowDialog( self, contributorType, dlgParams ):
        dialogModuleName = customContributorTemplates[contributorType][0]
        
        module = __import__(dialogModuleName)

        if not dlgParams:
            dlgParams = acm.FDictionary()
            dlgParams["name"] = contributorType

        dlg = module.Create( dlgParams )
            
        dlgParams = acm.UX().Dialogs().ShowCustomDialogModal(
            self.m_shell, 
            dlg.CreateLayout(),
            dlg
        )
        if dlgParams:
            params = acm.FDictionary()
            params["parameters"] = dlgParams
            params["customType"] = contributorType
        
            return [params]
            
        return None

    @staticmethod
    def ContributorsFromSource( params ):
        customContributor = acm.FDictionary()
        customContributor[ "customTemplateName" ] = customContributorTemplates[ params["customType"] ][1]
        customContributor[ "parameters" ] = params["parameters"]
    
        contributor = Contributor(acm.FDictionary())
        contributor.m_type = params["customType"]
        contributor.m_displayName = params["customType"]
        contributor.m_columnName = params["parameters"]["columnName"]
        contributor.m_customContributor = customContributor
        return [contributor]
        
    @staticmethod
    def SourceFromContributor( contributor ):
        params = contributor.m_customContributor["parameters"].Clone()
        return params
