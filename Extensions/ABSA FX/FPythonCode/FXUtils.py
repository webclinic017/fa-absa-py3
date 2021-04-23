'''================================================================================================
================================================================================================'''
import acm
'''================================================================================================
================================================================================================'''
def CreateMirrorTrade(original_trade,mirror_portfolio,contactref = 0,your_ref = ''):
    mirror = original_trade.Clone() 
    mirror.Portfolio( mirror_portfolio )
    mirror.Acquirer( original_trade.Counterparty() )
    mirror.Counterparty( original_trade.Acquirer() )
    mirror.Quantity( -original_trade.Quantity() )
    mirror.Premium( -original_trade.Premium() )
    mirror.MirrorTrade( original_trade )
    mirror.TradeProcess( original_trade.TradeProcess() )
    mirror.ContractTrdnbr( contactref )
    mirror.YourRef( your_ref )
    return mirror
'''================================================================================================
================================================================================================'''
def PrettyPrint(trade):
    print '--------------------------------------------------------'
    print 'CurrencyPair         = ', trade.CurrencyPair().Name() 
    print 'ValueDay             = ', trade.ValueDay()
    print 'Portfolio            = ', trade.Portfolio().Name()
    print 'MirrorPortfolio      = ', trade.MirrorPortfolio().Name()        
    print 'CounterParty         = ', trade.Counterparty().Name()
    print 'Acquirer             = ', trade.Acquirer().Name()
    print 'Quantity             = ', trade.Quantity()
    print 'Price                = ', trade.Price()
    print 'Premium              = ', trade.Premium()
    print 'Status               = ', trade.Status()
    print 'Number               = ', trade.Oid()
    print 'Time                 = ', trade.TradeTime()
    print 'Text1                = ', trade.Text1()
    print '--------------------------------------------------------'    
'''================================================================================================
================================================================================================'''
def CreatRollBackData(rollbackSpec, trade):
    rbd = acm.FRollbackData()
    rbd.Attributes('{}') 
    rbd.Entity('ael.Trade['+str(trade.Oid())+']')
    rbd.Operation('Create')
    rbd.RollbackSpec(rollbackSpec)
    return rbd 
'''================================================================================================
================================================================================================'''
def CreateRollBackSpec(description):
    rs = acm.FRollbackSpec()
    rs.Name(description + ' ' + acm.Time.TimeNow())
    rs.Commit()
    return rs    
'''================================================================================================
================================================================================================'''
def CreateNamedParam(vector, currency ):
    param = acm.FNamedParameters();
    param.AddParameter('currency', acm.FCurrency[currency])
    vector.Add( param )    
'''================================================================================================
================================================================================================'''
def RunTest(dict):
    currencyPair = acm.FCurrencyPair[dict['CP']]
    valueDay = currencyPair.SpotDate( acm.Time.TimeNow() ) if dict['VD'] == 'SPOT' else acm.Time.DateAdjustPeriod( acm.Time.TimeNow(), dict['VD'] )
    trade = acm.FTrade()
    trade.RegisterInStorage()
    trade.TradeTime( acm.Time.TimeNow() )
    trade.AcquireDay(  valueDay )
    trade.ValueDay ( trade.AcquireDay() )
    trade.Instrument( currencyPair.Currency1() )
    trade.Currency( currencyPair.Currency2() )
    trade.Acquirer( dict['AC'] )
    trade.Counterparty( dict['CY'] )
    trade.Portfolio( dict['PF'] )
    trade.Trader( dict['TR'] )
    trade.Price( 11.1 )
    trade.ReferencePrice( 11)
    trade.Quantity( 100 )
    trade.UpdatePremium( True )
    trade.BaseCostDirty(dict['BC'])
    trade.TradeProcess( dict['TP'])
    trade.OptionalKey( '{0}|{1}|{0}'.format(acm.Time.TimeOnlyMs().replace(':', ''), dict['SR']))
    trade.Status("Simulated")
    #CommitInTransaction([near,far])
    route(trade, dict['AI'], False)
    #find_routing_instruction(trade)
'''================================================================================================
================================================================================================'''
def CommitInTransaction(objects):
    try:
        acm.BeginTransaction()
        [object.Commit() for object in objects]
        acm.CommitTransaction()
    except Exception, error:
        print ('Aborting Transaction for object {0}').format(str(error)) 
        acm.AbortTransaction()
'''================================================================================================
================================================================================================'''
