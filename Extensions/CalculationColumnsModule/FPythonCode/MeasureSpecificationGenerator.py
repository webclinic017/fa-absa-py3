
import acm

class Contributor(object):
    
    def __init__( self, sourceDictionary ):
        self.m_type = sourceDictionary["type"]
        self.m_displayName = sourceDictionary["displayName"]
        self.m_scenario = sourceDictionary["scenario"]
        self.m_parameters = sourceDictionary["parameters"]
        self.m_columnId = sourceDictionary["columnId"]
        self.m_customContributor = sourceDictionary["customContributor"]
        self.m_vectors = sourceDictionary["vectors"]
        self.m_columnName = sourceDictionary["columnName"]
        
    def AsDictionary(self):
        d = {"displayName" : self.m_displayName, "type" : self.m_type }
        if self.m_scenario:
            d["scenario"] = self.m_scenario
        if self.m_parameters:
            d["parameters"] = self.m_parameters
        if self.m_columnId:
            d["columnId"] = self.m_columnId
        if self.m_customContributor:
            d["customContributor"] = self.m_customContributor.Clone()
        if self.m_vectors:
            d["vectors"] = []
            for vector in self.m_vectors:
                d["vectors"].append( vector.Clone() )
        if self.m_columnName:
            d["columnName"] = self.m_columnName
        return d
        
    def DefinesColumns( self ):
        if self.m_columnId:
            return True
        if self.m_customContributor:
            module = __import__( self.m_customContributor["customTemplateName"] )
            return module.DefinesColumn()
        return False
        
    def AsMeasureSpecificationComponents(self):
        if self.m_customContributor:
            module = __import__( self.m_customContributor["customTemplateName"] )
            #backwards compatibility
            self.m_customContributor["parameters"]["name"] = str(self.m_displayName)
            if self.m_columnName:
                self.m_customContributor["parameters"]["columnName"] = str(self.m_columnName)
            return module.Generate( self.m_customContributor["parameters"] )
            
        msc = MeasureSpecificationComponents()
        if self.m_scenario:
            msc.m_scenarios = [self.m_scenario]
        if self.m_parameters:
            msc.m_parameters = [acm.Sheet().Column().ConfigurationFromColumnParameterDefinitionNamesAndValues( self.m_parameters, None)]
        if self.m_columnId:
            msc.m_columnId = self.m_columnId
            msc.m_columnName = self.m_displayName
        if self.m_columnName:
            msc.m_columnName = self.m_columnName
        if self.m_vectors:
            msc.m_vectors = self.m_vectors
        return [msc]
        
class MeasureSpecificationComponents(object):
    def __init__(self):
        self.m_scenarios = None
        self.m_parameters = None
        self.m_columnId = None
        self.m_vectors = None
        self.m_columnName = None
        
    def UniqueId( self, idPrefix ):
        id = ""
        if idPrefix:
            id = idPrefix + "."
        id += self.Name()
        return id
    
    def Name( self ):
        if self.m_columnName:
            id = str( self.m_columnName )
        else:
            id = str( self.m_columnId )
        return id
        
    def Merge( self, other ):
        if other.m_scenarios:
            if not self.m_scenarios:
                self.m_scenarios = []
            self.m_scenarios.extend( other.m_scenarios )
        if other.m_parameters:
            if not self.m_parameters:
                self.m_parameters = []
            self.m_parameters.extend( other.m_parameters )
        if other.m_columnId:
            self.m_columnId = other.m_columnId
        if other.m_columnName:
            if self.m_columnName:
                self.m_columnName += "." + other.m_columnName
            else:
                self.m_columnName = other.m_columnName
        if other.m_vectors:
            if not self.m_vectors:
                self.m_vectors = []
            self.m_vectors.extend( other.m_vectors )
        
    def CreateVectorConfigurationParameters( self ):
        assert( self.m_columnId )

        def MergeVectorConfiguration( target, source ):
            if target:
                for key in source:
                    if "receivers" == key:
                        tt = target[key]
                        if tt:
                            target[key].AddAll( source[key] )
                        else:
                            target[key] = source[key]
                    else:
                        target[key] = source[key]
            else:
                target = source
            return target
            
        createParams = acm.FDictionary()
        dimensions = acm.FArray()
        createParams[ "dimensions" ] = dimensions
        
        vectors = acm.FOrderedDictionary()
        for v in self.m_vectors:
            logicalDimensionName = acm.FSymbol( v["logicalDimensionName"] )
            vectors[ logicalDimensionName ] = MergeVectorConfiguration( vectors[ logicalDimensionName ], v )
            """
            if vectors[ logicalDimensionName ]:
                vectors[ logicalDimensionName ].AddAll( v )
            else:
                vectors[ logicalDimensionName ] = v
            """
            
        usedExternalIds = set()
        if self.m_columnId:
            dimDefByLogicalName = None

            liveColDef = acm.Risk.CreateLiveColumnDefinition( self.m_columnId, acm.ExtensionTools().GetDefaultContext().Name() )
            dimDefByLogicalName = liveColDef.DimensionDefinitionsByLogicalName()
            if not dimDefByLogicalName:
                dimDefByLogicalName = acm.FOrderedDictionary()
            if liveColDef.OptionalDimensionDefinitionsByLogicalName():
                dimDefByLogicalName.AddAll(  liveColDef.OptionalDimensionDefinitionsByLogicalName() )
            
            for logicalName in dimDefByLogicalName:
                vConfig = vectors[logicalName]
                if vConfig:
                    dimData = acm.FDictionary()
                    dimData["externalId"] = logicalName
                    dimData["dimDefName"] = dimDefByLogicalName[logicalName].Name()
                    if vConfig["receivers"]:
                        dimData["receivers"] = vConfig["receivers"]
                    if vConfig["coordinatesParams"]:
                        dimData["coordinatesParams"] = vConfig["coordinatesParams"]
                    dimensions.Add( dimData )
                    usedExternalIds.add( logicalName )
            
        for logicalName in vectors:
            if not logicalName in usedExternalIds:
                usedExternalIds.add( logicalName )
                vConfig = vectors[ logicalName ]
                dimData = acm.FDictionary()
                dimData["externalId"] = vConfig["logicalDimensionName"]
                dimData["dimDefName"] = vConfig["dimDefName"]
                if vConfig["receivers"]:
                    dimData["receivers"] = vConfig["receivers"]
                dimensions.Add( dimData )
            
        return createParams
        
    def ToMeasureSpecification( self, idPrefix ):
        try:
            if not self.m_columnId:
                return None
            paramConfig = None
            if self.m_parameters:
                for cConfig in self.m_parameters:
                    if not paramConfig:
                        paramConfig = cConfig
                    paramConfig = paramConfig.Merge( cConfig )

            vectorConfiguration = None
            if self.m_vectors:
                createParams = self.CreateVectorConfigurationParameters()
                vectorConfiguration = acm.Risk().CreateDynamicVectorConfiguration( acm.ExtensionTools().GetDefaultContext().Name(), 'VectorConfiguration', createParams )
                paramConfig = acm.Sheet().Column().ConfigurationFromVectorConfiguration( vectorConfiguration, paramConfig )

            scenarios = []
            if self.m_scenarios:
                for scenario in self.m_scenarios:
                    scenarios.append( scenario.Scenario() )

            return acm.Risk().CreateMeasureSpecification(
                    self.UniqueId( idPrefix ), 
                    self.Name(),
                    self.m_columnId,
                    acm.ExtensionTools().GetDefaultContext().Name(),
                    scenarios, 
                    paramConfig
                )
        except Exception, e:
            print(e.message)
            return None

def MeasureSpecificationsFromContributors( idPrefix, contributors ):
    mss = []
    if contributors and len(contributors) > 0:
        mSpecs = contributors[0].AsMeasureSpecificationComponents()
        for c in contributors[1:]:
            oldSpecs = list(mSpecs)
            mSpecs = []
            newSpecs = c.AsMeasureSpecificationComponents()
            for spec in oldSpecs:
                for new in newSpecs:
                    newSpec = MeasureSpecificationComponents()
                    newSpec.Merge( spec )
                    newSpec.Merge( new )
                    mSpecs.append( newSpec )
        
        for ss in mSpecs:
            mSpec = ss.ToMeasureSpecification(idPrefix)
            if mSpec:
                mss.append( mSpec )
    return mss

def GenerateDo( idPrefix, params, contributors, ids, specs ):
    contributor = params['contributor']
    if contributor:
        contributors.append( Contributor( contributor ) )
    if params['children']:
        for child in params['children']:
            GenerateDo( idPrefix, child, contributors, ids, specs )
            contributors.pop()
    else:
        for spec in MeasureSpecificationsFromContributors( idPrefix, contributors ):
            if spec.UniqueId() in ids:
                print("spec with id " + spec.UniqueId() + " already generated.")
            else:
                specs.append( spec )
                ids.Add( spec.UniqueId() )
        
def Generate( params, ids ):
    specs = []
    if params:
        tree = params['tree']
        idPrefix = params['idPrefix']
        GenerateDo( idPrefix, tree, [], ids, specs )
    return specs
