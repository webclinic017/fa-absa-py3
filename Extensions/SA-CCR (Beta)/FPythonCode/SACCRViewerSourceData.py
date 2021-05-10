
import acm

import SACCRAggregationManager

class SourceData( object ):
    #------------------------------------------------------------------------------
    def __init__( self, sourceObject ):
        self.m_sourceData = []
        self.m_aggregationManager = None
        
        if sourceObject:
            self.SetSourceData( sourceObject )
        
        self.AggregateSourceData()
    
    #------------------------------------------------------------------------------
    def GetSourceData( self ):
        return self.m_sourceData
        
    #------------------------------------------------------------------------------
    def GetAggregatedData( self, groupingAttributes ):
        return self.m_aggregationManager.GetAggregatedValue(*groupingAttributes)
    
    #------------------------------------------------------------------------------
    def AggregateSourceData( self ):
        self.m_aggregationManager = SACCRAggregationManager.SACCRAggregationManager(self.m_sourceData)
    
    #------------------------------------------------------------------------------
    def SetSourceData( self, sourceObject ):
        calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
        top_node = calc_space.InsertItem( sourceObject )
        calc_space.Refresh()
        calc = calc_space.CreateCalculation(top_node, "SACCR Aggregation Values")
        
        self.m_sourceData = calc.Value()

#------------------------------------------------------------------------------
def GetValuesForColumns(sourceObject, columns):
    calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet')
    top_node = calc_space.InsertItem(sourceObject)
    calc_space.Refresh()
    
    iterator = calc_space.RowTreeIterator()
    iterator.Find(sourceObject)
    
    return dict((col, calc_space.CalculateValue(iterator.Tree(), col)) for col in columns)
