"""----------------------------------------------------------------------------------------
MODULE
     FSaveVolatility - Defines menu extensions for saving volatility via the 
                       trading manager.
    
     This module saves or recalculates the implied volatility from the Trading Manager.
     If the instrument is not defined as benchmark option it will be added to the structure.
     Given that the instruments coordinates (optMat, strike)  doesn't conflict 
     with an existing benchmark in the structure.
----------------------------------------------------------------------------------------"""

import acm
import FLogger

logger = FLogger.FLogger( 'Volatility' )

class InvalidRowObjectError( Exception ): pass

class VolatilityStructureUpdater( object ):

    @classmethod
    def get_identity_spread_point( cls, vol_structure, instrument, match_und_mat ):
        for p in vol_structure.Points():
            insIsGeneric = instrument.Generic()
            insIsCall = instrument.IsCall()
            pointIsGeneric = p.IsGenericExpiry()
            pointIsCall = p.Call()
            matchingGeneric = (insIsGeneric and pointIsGeneric) or ((not insIsGeneric) and (not pointIsGeneric))
            matchingCallPut = (insIsCall and pointIsCall) or ((not insIsCall) and (not pointIsCall))
            if matchingGeneric and matchingCallPut and p.Strike() == instrument.StrikePrice() and p.ActualExpiryDay() == instrument.ExpiryDateOnly():
                if match_und_mat:
                    underlying = instrument.Underlying()
                    if underlying:
                        undIsGeneric = underlying.Generic()
                        pointUndMatIsGeneric = p.IsGenericUnderlyingMaturity()
                        if p.ActualUnderlyingMaturityDay() == instrument.ActualUnderlyingMaturityDay():
                            if undIsGeneric and pointUndMatIsGeneric:
                                return p
                            if (not undIsGeneric) and (not pointUndMatIsGeneric):
                                return p
                else:
                    return p
        return None
    
    @classmethod
    def get_identity_point( cls, vol_structure, instrument ):
        for p in vol_structure.Points():
            if p.Benchmark() == instrument:
                return p
        return None
        
    @classmethod
    def get_matching_point( cls, vol_structure, instrument ):
        for p in vol_structure.Points():
            if p.Benchmark() and p.Benchmark().StrikePrice() == instrument.StrikePrice() and p.Benchmark().ExpiryDateOnly() == instrument.ExpiryDateOnly():
                return p
        return None
    
    @classmethod
    def get_point( cls, vol_structure, instrument, match_exact=False ):
        point = cls.get_identity_point( vol_structure, instrument ) 
        if not point and not match_exact:
            if vol_structure.IsSpreadStructure():
                point = cls.get_identity_spread_point( vol_structure, instrument, True )
                if not point:
                    point = cls.get_identity_spread_point( vol_structure, instrument, False )
            else:
                point = cls.get_matching_point( vol_structure, instrument )
        return point
    
    @classmethod    
    def create_point( cls, instrument, vol_structure, new_vol ):
        try:
            point = acm.FVolatilityPoint() 
            point.Structure( vol_structure )
            point.Benchmark( instrument )     
            point.Volatility( new_vol )
            point.Commit() 
            logger.LOG( "Created new point in volatility surface < %s > for instrument < %s > with volatility < %s >", vol_structure.Name(), instrument.Name(), new_vol  )
        except RuntimeError as err:
            logger.LOG( "Failed to create point in volatility surface < %s > for instrument < %s >", vol_structure.Name(), instrument.Name(), exc_info=True )

    @classmethod
    def update_point( cls, instrument, vol_structure, new_vol, create_new=True, match_exact=False ):
        if not isinstance( new_vol, float ):
            logger.ELOG( "Invalid volatility value < %s > of type < %s >!", new_vol, type( new_vol ) )
        else:
            if cls.get_point( vol_structure, instrument, match_exact ):
                try:
                    vol_structure_c = vol_structure.Clone()
                    point_c = cls.get_point( vol_structure_c, instrument, match_exact )
                    if vol_structure.IsSpreadStructure():
                        point_c.VolatilityTotal( new_vol )	
                    else:
                        point_c.Volatility( new_vol )	
                    vol_structure.Apply( vol_structure_c )
                    vol_structure.Commit()
                    logger.LOG( "Updated volatility surface < %s > for instrument < %s > with volatility < %s >", vol_structure.Name(), instrument.Name(), new_vol  )
                except RuntimeError as err:
                    logger.LOG( "Failed to updated volatility surface < %s > for instrument < %s >", vol_structure.Name(), instrument.Name(), exc_info=True )
            else:
                if create_new:
                    if vol_structure.IsSpreadStructure():
                        logger.LOG( "No suitable point found on spread volatility surface < %s > for instrument < %s >, please create a suitable point manually", vol_structure.Name(), instrument.Name(), exc_info=True )
                    else:
                        cls.create_point( instrument, vol_structure, new_vol )
    
    @classmethod
    def update_vol_of_vol( cls, vol_structure, new_value ):
        try:
            vol_structure.VolOfVol( new_value )
            vol_structure.Commit()
            logger.LOG( "Updated VofVol in structure < %s > with value < %s >", vol_structure.Name(), new_value )
        except RuntimeError, err:
            logger.ELOG( "Failed to update VofVol in structure < %s >", vol_structure.Name(), exc_info=True )
            
    @classmethod
    def update_speed_of_mean_reversion( cls, vol_structure, new_value ):
        try:
            vol_structure.SpeedOfMeanReversion( new_value )
            vol_structure.Commit()
            logger.LOG( "Updated SpeedOfMeanReversion in structure < %s > with value < %s >", vol_structure.Name(), new_value )
        except RuntimeError as err:
            logger.ELOG( "Failed to update SpeedOfMeanReversion in structure < %s >", vol_structure.Name(), exc_info=True )
            
    @classmethod
    def update_long_term_mean_vol( cls, vol_structure, new_value ):
        try:
            vol_structure.LongTermMeanVol( new_value )
            vol_structure.Commit()
            logger.LOG( "Updated LongTermMeanVol in structure < %s > with value < %s >", vol_structure.Name(), new_value )
        except RuntimeError as err:
            logger.ELOG( "Failed to update LongTermMeanVol in structure < %s >", vol_structure.Name(), exc_info=True )
        
class VolatilitySelectionMgr( object ):
    
    PORT_VOLA                   = "Portfolio Volatility"
    PORT_VOLA_CALL              = "Portfolio Volatility /Call"
    PORT_VOLA_PUT               = "Portfolio Volatility /Put"
    PORT_VOLA_VOLA              = "Portfolio Volatility of Volatility"
    PORT_MEAN_REVERSION         = "Portfolio Speed Of Mean Reversion"
    PORT_LONG_TERM_VOLA         = "Portfolio Long Term Volatility"
    
    COLUMNS                     = [ PORT_VOLA, PORT_VOLA_CALL, PORT_VOLA_PUT, PORT_VOLA_VOLA, PORT_MEAN_REVERSION, PORT_LONG_TERM_VOLA ]
    SC_CALC_SPACE               = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
    
    @classmethod
    def supported_column( cls, column_id ):
        return column_id in cls.COLUMNS
    
    @classmethod    
    def get_cell_info( cls, cell ):
        column = cell.Column()
        column_id = str(column.ColumnId())
        context = column.Context().Name()
        row = cell.RowObject()
        if hasattr( row, "Instrument" ):
            rowObject = row
        else:
            raise InvalidRowObjectError( "Invalid row object" )
        return column, column_id, context, rowObject
    
    @classmethod
    def is_point_column( cls, column_id ):
        return  column_id in [ cls.PORT_VOLA, cls.PORT_VOLA_CALL, cls.PORT_VOLA_PUT ]
    
    @classmethod
    def update_structure( cls, vol_structure, column_id, new_value ):
        if column_id == cls.PORT_VOLA_VOLA:
            VolatilityStructureUpdater.update_vol_of_vol( vol_structure, new_value )
                
        elif column_id == cls.PORT_MEAN_REVERSION:
            VolatilityStructureUpdater.update_speed_of_mean_reversion( vol_structure, new_value )
            
        elif column_id == cls.PORT_LONG_TERM_VOLA:
            VolatilityStructureUpdater.update_long_term_mean_vol( vol_structure, new_value )
    
    @classmethod
    def get_new_volatility( cls, instrument, cell, recalc ):
        if recalc:
            try:
                new_vol = instrument.Calculation().ImpliedVolatility( cls.SC_CALC_SPACE )
            except:
                logger.LOG( "Could not recalculate new volatility point for < %s > due to no market price or implied volatility could not be calculated. ", instrument.Name())
        else:
            new_vol = cell.Evaluator().Value() 
        return new_vol    
        
    @classmethod    
    def update_volatility_cell( cls, cell, recalc):
        try:
            column, column_id, context, rowObject = cls.get_cell_info( cell )
        except InvalidRowObjectError as err:
            return 
       
        try:
            instrument = rowObject.Instrument()
            value = acm.GetCalculatedValueFromString(rowObject, cell.Column().Context(), 'volatilityStructureName', cell.Tag())
            vola_name = str(value.Value())
            vol_structure = acm.FVolatilityStructure[vola_name] 
            if not vol_structure: 
                vol_structure = instrument.MappedVolatilityLink().Link().VolatilityStructure() 
        except: 
            vol_structure = instrument.MappedVolatilityLink().Link().VolatilityStructure() 
        
        if not cls.supported_column( column_id ):
            logger.LOG( "Column < %s > is not supported.", column_id )
        elif recalc and not cls.is_point_column( column_id ):
            logger.LOG( "Column < %s > does not support recalculation.", column_id )
        elif cls.is_point_column( column_id ):
            new_vol = cls.get_new_volatility( instrument, cell, recalc )
            VolatilityStructureUpdater.update_point( instrument, vol_structure, new_vol )  
        else:
            cls.update_structure( vol_structure, column_id, cell.Evaluator().Value() )
        return 
    
    @classmethod    
    def update_volatility_range( cls, invokationInfo, recalc ):
        try:
            for cell in invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedCells():
                cls.update_volatility_cell( cell, recalc )
        except:
            logger.LOG( "Recalculate Volatility can not be performed from this sheet.")
            
def save_volatility( invokationInfo ):
    VolatilitySelectionMgr.update_volatility_range( invokationInfo, recalc=False )

def recalc_implied_volatility( invokationInfo ):
    VolatilitySelectionMgr.update_volatility_range( invokationInfo, recalc=True )




