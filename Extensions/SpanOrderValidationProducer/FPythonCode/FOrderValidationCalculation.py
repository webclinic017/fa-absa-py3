from __future__ import print_function
""" Compiled: 2015-09-23 14:33:50 """

import acm
import GetShortSellPortfolios
import time
import thread
import os



# #############################################################################################################
#
# Singleton class for producer requesting portfolio and order data for a specified portfolio
#


class Space:
    def __init__(self):
        self._portfolios = {}
        self._lastUpdate = 0
        
        self._space = acm.Calculations().CreateCalculationSpace( acm.GetDefaultContext(), 'FPortfolioSheet' )
# Should not allow any other class direct access to the calc-space - to be able to guard the space from operations when something is already pending (e g reentrancy of PACE)
        self._producers = []
        self._stats = {}
        #thread.start_new_thread( self.LogStats, () )
        
        self._pendingCalcs = set()
        self._pendingOrders = set()
        self._updatingCalcs = False

    '''
    def AddStats(self, prf, name, t):
        if prf:
            return # Skip portfolio level logging
        prf = prf or '<Space>'
        stats = self._stats.setdefault( prf, {} )
        current = stats.setdefault( name, 0 )
        stats[ name ] = current + t
        
    def LogStats(self):
        def TS():
            return time.strftime( '%Y-%m-%d %H:%M:%S', time.localtime() )
            
        def Log(text, ts):
            d = ts.split()[ 0 ]
            f = open( 'Statistics_%s_%i.log' % ( d, os.getpid() ), 'a' )
            f.write( text + '\n' )
            f.close()
            
        def Sort(a, b):
            ka, va = a
            kb, vb = b
            if ka > kb: return 1
            if ka < kb: return -1
            return 0            
        
        Log( '\n\n%s *** Started statistics logger thread ***\n' % ( TS() ), TS() )
        
        while 1:
            time.sleep( 60 )
            t = TS()
            plog = '\n'.join( [ '%s %s: %s' % ( t, p.__class__.__name__, p._stats ) for p in self._producers ] )
            slog = '\n'.join( [ '%s %s: %s' % ( t, prf, stats ) for prf, stats in sorted( self._stats.iteritems(), Sort ) ] )
            
            Log( plog, t )
            Log( slog, t )
    '''
            
    def FlagPortfolioForRecalculation(self, prf, reason):
        self._pendingCalcs.add( prf )
            
    def FlagPortfolioForRecalculationOrderId(self, prf, reason):
        self._pendingOrders.add( prf )
        self.FlagPortfolioForRecalculation( prf, reason )
            
    def GetPortfolio(self, prf, ssl):
        # prf is an acm.FPortfolio, ssl is an already created FOrderValidationCalculation.Portfolio
        return self._portfolios.setdefault( prf, Portfolio( self, prf, ssl ) )
        
    def GetShortSellLimitPortfolio(self, prf, positionColumnIds):
        # sslPrf below is an acm.FPortfolio, but we are returning an FOrderValidationCalculation.Portfolio
        sslPrf = GetShortSellPortfolios.GetShortSellLimitCheckPortfolio( prf )
        if sslPrf and sslPrf != prf:
            return self.HandleRequest( sslPrf, [], positionColumnIds, False )
        else:
            return None
        
    def HandleRequest(self, prf, portfolioColumnIds = [], positionColumnIds = [], includeOrders = True):
        ssl = self.GetShortSellLimitPortfolio( prf, positionColumnIds )
        portfolio = self.GetPortfolio( prf, ssl )
        portfolio.Tree().AddColumns( portfolioColumnIds, positionColumnIds )
        portfolio.Tree().Initialize()
        portfolio.Orders().Initialize( includeOrders )
        self.DoRefresh()
        self.ManageCalculations( [ portfolio ] )
        return portfolio

    def InsertItem(self, item):
        return self._space.InsertItem( item )

    def CreateCalculation(self, item, id, cb):
        try:
            return Calculation( self._space.CreateCalculation( item, id ), id, cb, exception = None )
        except Exception as ex:
            return Calculation( None, id, cb, exception = ex )

    def DoRefresh(self):
        self._space.Refresh() # When run in local scope, must do this to be notified of any inserted or removed rows
        
    def ManageCalculations(self, portfolios):
        for portfolio in portfolios:
            portfolio.Tree().ManageCalculations()
            
    def GetNextPortfolioSet(self, prfSet):
        # Get all pending items - could possibly change to get an optimal slice if performance could be improved
        try:
            return [ self._portfolios[ prf ] for prf in prfSet ]
        finally:
            prfSet.clear()
            
    def GetUpdatedCalulcations(self, portfolios = None, updatedOnly = True):
        now = time.time()
        
        if updatedOnly and now > self._lastUpdate + 60 * 60:
            updatedOnly = False
            self._lastUpdate = now
            
        self.DoRefresh()

        portfolios = portfolios or self.GetNextPortfolioSet( self._pendingCalcs  )
        
        self.ManageCalculations( portfolios )
        
        updated = {}
        for portfolio in portfolios:
            updated[ portfolio.Key() ] = portfolio.GetUpdatedValues( updatedOnly )
            
        if updatedOnly == False:
            self._lastUpdate = time.time()
        
        return updated
            
    def GetUpdatedOrders(self, portfolios = None):
        portfolios = portfolios or self.GetNextPortfolioSet( self._pendingOrders )
  
        updated = {}
        for portfolio in portfolios: 
            updated[ portfolio.Key() ] = portfolio.GetUpdatedOrders()
        
        return updated
        


Space.Instance = Space()


# #############################################################################################################
#
# Order handling
#




class OrderInfo:
    def __init__(self):
        self._qty = 0.0
        self._ids = {}
        self._updated = False

    def InsertOrder(self, order):
        qty = order.Quantity()
        self._qty += qty
        self._ids[ order.OrderId() ] = qty
        self._updated = True

    def RemoveOrder(self, order):
        oid = order.OrderId()
        if oid in self._ids:
            self._qty -= self._ids.pop( oid )
            self._updated = True

    def Update(self):
        try:
            return self._updated
        finally:
            self._updated = False

    def Current(self):
        return self._qty


class OrderInfoPair:
    def __init__(self, key):
        self._key = key
        self._ois = { True : OrderInfo(), False : OrderInfo() }

    def Key(self):
        return self._key

    def OrderInfo(self, bs):
        return self._ois[ bs ]

    def Update(self):
        return True in [ oi.Update() for oi in self._ois.values() ]

        
class OrderId:        
    def __init__(self, key):
        self._key = key
        self._versions = []
        
    def Key(self):
        return self._key

    def AddVersion(self, order, state):
        self._versions.append( ( state, ( order.Text2(), order.Quantity() ) ) )
        
    def GetVersions(self):
        try:
            return self._versions
        finally:
            self._versions = []

    def Update(self):
        return len( self._versions ) > 0
        

class PortfolioOrders:
    def __init__(self, space, prf):
        self._space = space
        self._prf = prf
        self._selections = []
        self._all_order_info_pairs = {}
        self._all_order_ids = {}
        self._updated_order_ids = {}

    def Initialize(self, includeOrders):
        if includeOrders and self._selections == []:
            if self._prf.Compound():
                portfolios = self._prf.AllPhysicalPortfolios()
            else:
                portfolios = [ self._prf ]
            self._selections = [ acm.FActiveOrder.Select( "portfolio='%s'" % prf.Name() ) for prf in portfolios ]
            for selection in self._selections:
                selection.AddDependent( self )
                for order in selection:
                    self._OnInsert( order )

    def RemoveOrders(self):
        for selection in self._selections:
            selection.RemoveDependent( self )

    def Rows(self):
        return self._all_order_info_pairs.values()
        
    def Ids(self):
        return self._all_order_ids.values()

    def UpdatedIds(self):
        return self._updated_order_ids.values()
        
    def _PrintRowInfo(self, text, oip):
        print ('  %s %s %f/%f' % ( text, oip.Key(), oip.OrderInfo( True ).Current(), oip.OrderInfo( False ).Current() ))

    def _GetOrderInfoPair(self, order):
        key = order.Instrument()
        return self._all_order_info_pairs.setdefault( key, OrderInfoPair( key ) )

    def _OnInsert(self, order):
        oip = self._GetOrderInfoPair( order )
        oi = oip.OrderInfo( order.Quantity() >= 0 )
        oi.RemoveOrder( order ) # Remove order to decrease total quantity with the old qty value...
        oi.InsertOrder( order ) # ... then add it and increase total quantity with the new value
        id = order.OrderId()
        self._all_order_ids.setdefault( id, OrderId( id ) ).AddVersion( order, state = True )
        self._updated_order_ids[ id ] = self._all_order_ids[ id ]

    def _OnRemove(self, order):
        oip = self._GetOrderInfoPair( order )
        oi = oip.OrderInfo( order.Quantity() >= 0 )
        oi.RemoveOrder( order )
        id = order.OrderId()
        self._all_order_ids.setdefault( id, OrderId( id ) ).AddVersion( order, state = False )
        self._updated_order_ids[ id ] = self._all_order_ids[ id ]

    def GetOrderInfoPairFromKey(self, key, default):
        return self._all_order_info_pairs.get( key, default )

    def ServerUpdate(self, sender, aspect, param):
        if aspect.AsString() in [ 'insert', 'update' ]:
            self._OnInsert( param )
        elif aspect.AsString() == 'remove':
            self._OnRemove( param )
        self._space.FlagPortfolioForRecalculationOrderId( self._prf, 'Order' )


# #############################################################################################################
#
# Calculated values handling
#



class Calculation:
    def __init__(self, calculation, id, cb, exception):
        self._calculation = calculation
        self._id = id
        self._cb = cb
        self._exception = exception
        self._current = None
        self._isUpdate = True
        if not self._exception:
            self._calculation.AddDependent( self )
        cb( self ) # Make sure it is evaluated first time

    def Id(self):
        return self._id

    def Update(self):
        previous = self._current
        if self._exception:
            self._current = self._exception
        else:
            try:
                self._current = self._calculation.Value()
            except:
                self._current = None

        self._isUpdate = False
        return previous != self._current

    def Current(self):
        return self._current
        
    def IsUpdated(self):
        return self._isUpdate

    def Unsubscribe(self):
        if not self._exception:
            self._calculation.RemoveDependent( self )
            self._calculation = None #

    def ServerUpdate(self, sender, aspect, param):
        self._isUpdate = True
        self._cb( self )



STATE_ACTIVE = 1
STATE_INSERT = 2
STATE_DELETE = 4

class PortfolioRow:
    def __init__(self, space, prf, columnIds, item, key, state = STATE_INSERT):
        self._space = space
        self._prf = prf
        self._item = item
        self._key = key
        self._state = state
        self._columnIds = columnIds
        self._all_calculations = {}
        
    def AddColumns(self, columnIds):
        self._columnIds.update( columnIds )

    def SetFlag(self, bit):
        self._state |= bit

    def RemoveFlag(self, bit):
        if self._state & bit:
            self._state ^= bit

    def State(self):
        return self._state

    def Key(self):
        return self._key

    def MarkForInsertion(self, item):
        self._item = item
        self.SetFlag( STATE_INSERT )

    def MarkForDeletion(self):
        self.SetFlag( STATE_DELETE )
        self.RemoveFlag( STATE_INSERT )

    def Insert(self):
        self.AddCalculations()
        self.SetFlag( STATE_ACTIVE )
        self.RemoveFlag( STATE_INSERT )

    def Delete(self):
        self.RemoveCalculations()
        self.RemoveFlag( STATE_ACTIVE )
        self.RemoveFlag( STATE_DELETE )

    def ManageSweepDone(self):
        self.RemoveFlag( STATE_INSERT )
        self.RemoveFlag( STATE_DELETE )

    def Update(self, updatedOnly):
        return [ True for calculation in self._all_calculations.values() if (calculation.IsUpdated() and calculation.Update()) ] != []

    def AddCalculations(self):
        for id in self._columnIds:
            if not id in self._all_calculations:
                self._all_calculations[ id ] = self._space.CreateCalculation( item = self._item, id = id, cb = self.OnCalculationUpdate )

    def RemoveCalculations(self):
        for calculation in self._all_calculations.values():
            calculation.Unsubscribe()
        self._all_calculations.clear()

    def OnCalculationUpdate(self, calc):
        self._space.FlagPortfolioForRecalculation( self._prf, 'Calculation/' + calc.Id() )

    def Current(self):
        return dict( [ [ key, calc.Current() ] for key, calc in self._all_calculations.iteritems() ]  )



class PortfolioTree:
    def __init__(self, space, prf):
        self._space = space
        self._prf = prf
        self._portfolioColumnIds = set()
        self._positionColumnIds = set()
        self._proxy = None
        self._rows = {}
        self._rowsPrf = {} # Holds single item, but has the same format as rows to share the same interfacing
        #self._orders = PortfolioOrders( prf )
        self._updated = False
        
    def Initialize(self):
        if self._proxy == None:
            self._proxy = self._space.InsertItem( self._prf )
            self._proxy.AddDependent( self )
            self._rowsPrf[ self._prf ] = PortfolioRow( self._space, self._prf, self._portfolioColumnIds, self._proxy, self._prf ) # Created with INSERT state for later processing

    def AddColumns(self, portfolioColumnIds, positionColumnIds):
        self._portfolioColumnIds.update( portfolioColumnIds )
        self._positionColumnIds.update( positionColumnIds )

        for key, row in self._rowsPrf.iteritems():
            row.AddColumns( self._portfolioColumnIds )
            row.AddCalculations()
            
        for key, row in self._rows.iteritems():
            row.AddColumns( self._positionColumnIds )
            row.AddCalculations()

    def Rows(self):
        return self._rows.values()

    def PortfolioRows(self):
        return self._rowsPrf.values()
        
    def GetRowFromKey(self, key, default):
        row = self._rows.get( key, self._rowsPrf.get( key, None ) ) # Get value from rows or portfolio rows, or default
        if row and row.State() & STATE_ACTIVE:
            return row
        else:
            return default

    def Columns(self):
        return self._portfolioColumnIds

    def RowColumns(self):
        return self._positionColumnIds

    def _PrintRowInfo(self, row, text):
        print ('  %s %s/%s/%s' % ( text, self._prf.Name(), row.Key().Name(), row.Current() ))

    def ManageCalculations(self):
        if not self._updated:
            return
            
        for row in self._rowsPrf.values() + self._rows.values(): # Must iterate over values(), not iteritems(), to avoid exception due to changes in the _rows dictionary
            state = row.State()

            if state & STATE_DELETE and state & STATE_ACTIVE:
                row.Delete() # Does not remove the row from self._rows, but closes any open calculation subscriptions
                state = row.State() # Must get state again since it was changed...

            if state & STATE_INSERT and not state & STATE_ACTIVE:
                row.Insert()

            row.ManageSweepDone() # Removes any STATE_INSERT or STATE_DELETE flags
            
        self._updated = False

    def GetKeyFromItem(self, item):
        return item.Instrument() # Only single instrument and trade rows in this implementation (no grouping)

    def _OnInsert(self, treeProxy):
        item = treeProxy.Item()
        key = self.GetKeyFromItem( item )
        row = self._rows.setdefault( key, PortfolioRow( self._space, self._prf, self._positionColumnIds, treeProxy, key ) ) # Initially created with INSERT state for later processing
        if not row.State() & STATE_INSERT:
            row.MarkForInsertion( treeProxy )

    def _OnRemove(self, treeProxy):
        item = treeProxy.Item()
        key = self.GetKeyFromItem( item )
        if key in self._rows:
            row = self._rows[ key ]
            row.MarkForDeletion() # Changes the state of the row for later processing

    def ServerUpdate(self, sender, aspect, param):
        if sender == self._proxy:
            if aspect.AsString() == 'Insert':
                self._OnInsert(param)
            elif aspect.AsString() == 'Remove':
                self._OnRemove(param)
            self._updated = True
            self._space.FlagPortfolioForRecalculation( self._prf, 'Tree' )

    def __repr__(self):
        return 'Portfolio %s' % ( self._prf.Name() )



class Portfolio:
    def __init__(self, space, prf, ssl):
        self._prf = prf # an acm.FPortfolio
        self._tree = PortfolioTree( space, prf )
        self._orders = PortfolioOrders( space, prf )
        self._ssl = ssl or self # If no ShortSellLimit portfolio is provided, use current portfolio instead (to simplify code/minimize changes in this class)
        
    def Key(self):
        return self._prf

    def Tree(self):
        return self._tree

    def Orders(self):
        return self._orders
        
    def GetUpdatedValues(self, updatedOnly):
        updated = {}
        s = { row.Key() for row in self._ssl.Tree().Rows() if row.Update(updatedOnly) or updatedOnly == False }
        p = { row.Key() for row in self._tree.PortfolioRows() if row.Update(updatedOnly) or updatedOnly == False }
        t = { row.Key() for row in self._tree.Rows() if row.Update(updatedOnly) or updatedOnly == False }
        o = { row.Key() for row in self._orders.Rows() if row.Update() or updatedOnly == False }
        u = t.union( o ).union( s ).union( p )
        
        for key in u:
            if key.Oid() < 0:
                continue
                
            row = self._tree.GetRowFromKey( key, None )
            ssl = self._ssl.Tree().GetRowFromKey( key, None )
            oip = self._orders.GetOrderInfoPairFromKey( key, None )
            
            updated[ key ] = ( row, ssl, oip )
        
        return updated
        
    def GetUpdatedOrders(self):
        updated = {}
        for oid in self.Orders().UpdatedIds():
            if oid.Update():
                updated[ oid.Key() ] = oid.GetVersions() # also clears the updates
        return updated
