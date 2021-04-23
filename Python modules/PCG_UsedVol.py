# Purpose                       :  Listens to a set of predefined trades and stores the volatility at FO Confirmed.
# Department and Desk           :  PCG
# Requester                     :  Palesa Mkhabele
# Developer                     :  Bhavnisha Sarawan
# CR Number                     :  C595780

import acm

VOL_ADDINFO = 'VolFOConfirmed'

class SheetCalcSpace( object ):
    CALC_SPACE = acm.FCalculationSpace('FTradeSheet')
    @classmethod
    def get_column_calc( cls, obj, column_id ):
        calc = SheetCalcSpace.CALC_SPACE.CreateCalculation( obj, column_id )
        return calc
        
def Vol(t,column, *rest):
    Value = 0
    try:
        calc  = SheetCalcSpace.get_column_calc(t, column)
        Value = calc.Value()
    except:
        print 'Error calculating volatility'
    return Value
    
def ParVol(t,column, *rest):
    Value = 0
    try:
        calc  = SheetCalcSpace.get_column_calc(t, column)
        Value = calc.Value().Number()
    except Exception, e:
        #print 'Error calculating volatility', e
        Value = calc.Value()
    return Value

class TradeUpdateHandler:

    #Generic function to add and amend Additional Info fields on any entity through ACM

    def set_AdditionalInfoValue(self, entity, addInfoName, value):
        if entity.add_info(addInfoName) == '':
            addInfo = acm.FAdditionalInfo()
            addInfo.Recaddr(entity.Oid())
            addInfo.AddInf(acm.FAdditionalInfoSpec[addInfoName])
            addInfo.Value(value)
            try:
                addInfo.Commit()
            except Exception, e:
                print 'Commit failed', e
        else:
            addInfo = acm.FAdditionalInfo.Select('recaddr = %i' %entity.Oid())
            for i in addInfo:
                if i.AddInf().Name() == addInfoName:
                    try:
                        i.Value(value)
                        i.Commit()
                    except Exception, e:
                        print 'Commit failed', e
                    break

    def ServerUpdate(self, sender, action, t):
        print action, 'action'
        if action.Text() == 'insert':
            if t.Instrument().InsType() == 'Option':
                vol = Vol(t, 'Portfolio Volatility')*100
                print vol
            else:
                vol = ParVol(t, 'Portfolio Par Volatility')*100
                print vol
            self.set_AdditionalInfoValue(t, VOL_ADDINFO, vol)
            
            print 'done'

def start():        
    u = TradeUpdateHandler()
    trade = acm.FTradeSelection['PCG_UsedVol1'].Trades()
    trade.AddDependent(u)
    trade2 = acm.FTradeSelection['PCG_UsedVol2'].Trades()
    trade2.AddDependent(u)
    print "started"
    
def stop():    
    trade = acm.FTradeSelection['PCG_UsedVol1'].Trades()
    for dependent in trade.Dependents():
        trade.RemoveDependent(dependent)
    
    trade2 = acm.FTradeSelection['PCG_UsedVol2'].Trades()
    for dependent in trade2.Dependents():
        trade2.RemoveDependent(dependent)
    print "stopped"
    
#stop()
#start()


