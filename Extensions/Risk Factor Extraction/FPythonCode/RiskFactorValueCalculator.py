import acm
import FExportCalculatedValuesWriterCommon


class RiskFactorValueCalculator(object):
    
    def __init__( self, riskFactorSetups ):
        self.m_setups = riskFactorSetups
        self.m_cs = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FRiskFactorSheet')
        
    def _positionInfoId( self, riskFactorSetup, riskFactorInstance ):
        return riskFactorSetup.Name() + "|" + riskFactorInstance.StringKey()
        
    def Columns(self):
        return [(FExportCalculatedValuesWriterCommon.ColumnInformation( name = 'Risk Factor Value', columnID = 'Risk Factor Value', columnPartNames = [None], isDynamic = False, scenarioInformation = None, vectorInformation = None ), 'Risk Factor Value')]
        
    def RootPositions(self):
        for setup in self.m_setups:
            yield ( FExportCalculatedValuesWriterCommon.RootPositionInformation( name = setup.Name(), acmDomainName = "FRiskFactorSetup" ), setup.Name() )
        
    def Positions(self):
        for setup in self.m_setups:
            for riskFactorCollection in setup.RiskFactorCollections():
                for instance in riskFactorCollection.RiskFactorInstances():
                    yield ( FExportCalculatedValuesWriterCommon.PositionInformation( rootPositionInformationID = setup.Name(), parentInfoID = None, name = self._positionInfoId( setup, instance ), acmDomainName = "FRiskFactorInstance", dimensionName = None ), self._positionInfoId( setup, instance ) )
            
    def Values( self ):
        for setup in self.m_setups:
            for riskFactorCollection in setup.RiskFactorCollections():
                for instance in riskFactorCollection.RiskFactorInstances():
                    value = self.m_cs.CalculateValue( instance, "Risk Factor Value" )
                    yield ( self._positionInfoId( setup, instance ), "Risk Factor Value", [FExportCalculatedValuesWriterCommon.CalculationInformation( projectionCoordinates = [], values = value )] )
                
