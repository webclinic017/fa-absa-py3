""" Compiled: 2010-08-18 19:45:48 """

"""----------------------------------------------------------------------------
MODULE
    FExeAssPerform - Module that executes ExerciseAssign.

    (c) Copyright 2004 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module executes the Exercise/Assign procedure based on the
    parameters passed from the scripts FExerciseAssign or FManualExercise.

----------------------------------------------------------------------------"""
#Import builtin modules

import ael, acm
import FBDPCommon
import FBDPRollback
import ArenaFunctionBridge
import FBDPCalculatePosition
from FBDPCommon import Summary
import FBDPString
logme = FBDPString.logme

import FBDPInstrument

# Attempt to get FBDPHook.exercise_trade hook and FBDPHook.additional_excercise_trades
exercise_trade_hook = None
additional_excercise_trades_hook = None
try:
    import FBDPHook
    reload(FBDPHook)
    exercise_trade_hook = FBDPHook.exercise_trade
except:
    logme('No FBDPHook.exercise_trade hook.', 'DEBUG')
try:
    import FBDPHook
    reload(FBDPHook)
    additional_excercise_trades_hook = FBDPHook.additional_excercise_trades
except:
    logme('No FBDPHook.additional_excercise_trades hook.', 'DEBUG')




#------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------
TRADE_TIME=(21*60*60)-1           # 20:59:59 seconds today
abandon_types=['Option', 'Warrant', 'Future/Forward', 'Bond']

def perform_exercise_assign(args):
    FBDPCommon.callSelectionHook(args, 'trades', 'exercise_assign_selection')
    e = Exercise('Exercise Assign', args['Testmode'], args)
    e.perform()
    e.end()

class Exercise(FBDPRollback.RollbackWrapper):
    def readArguments(self):
        if self.ael_variables_dict.has_key('actions_for_trades'):
            logme ("Found 'actions_for_trades' in ael_variables.", "DEBUG")
            # Turn the parameter (a string) back into a real dictionary.
            self.actionsForTrades = eval(self.ael_variables_dict['actions_for_trades'])
        else:
            logme ("Failed to find 'actions_for_trades' in ael_variables -- this is a problem if you are running FManualExercise.", "DEBUG")
            self.actionsForTrades = None
        self.doExeAssign = self.ael_variables_dict['DoExeAss']
        self.doAbandon = self.ael_variables_dict['DoAbandon']
        self.mode = self.ael_variables_dict['mode']
        self.settlePrice = self.ael_variables_dict['settle_price']
        self.settleMarket = self.ael_variables_dict['settlemarket']
        self.givenTradeIds = self.ael_variables_dict['trades']

    def getPositions(self):
        positions = {}
        for tradeId in self.givenTradeIds:
            t = ael.Trade[tradeId]
            ins = t.insaddr
            port = t.prfnbr
            if not positions.has_key(ins):
                positions[ins] = [port]
            else:
                if positions[ins].count(port) == 0:
                    positions[ins].append(port)
        return positions
    
    def perform(self):
        self.insDates = {}
        
        # read given arguments
        self.readArguments()
        
        # Populate instrument dictionary with traded portfolios
        positions = self.getPositions()
        
        #positioning after hook recalculate_position
        hookArguments = {}
        try:
            from FBDPHook import recalculate_position
            hookArguments = self.ael_variables_dict
        except:
            pass

        trade_cutoff_date = ael.date_today()
        for (ins, portfolios) in positions.items():
            manualAction = self.getManualOverride(ins)
            insIsBarrier = isBarrier(ins)
            if hookArguments:
                portfolios = []
            calcPositions = FBDPCalculatePosition.calculatePosition(ins, 
                                        end_date = trade_cutoff_date,
                                        portfolio = portfolios,
                                        hookArguments = hookArguments)
            for pos in calcPositions:
                calcTrades = pos[0]
                dependTrades = pos[1]
                port = calcTrades[0].prfnbr
                posName ="[%s:%s]" % (port and port.prfid or 'None', ins.insid)
                if len(calcTrades) > 1:
                    useCurrencyDependency = True
                else:
                    useCurrencyDependency = False
                for trd in calcTrades:
                    depTrade = None
                    if trd.trdnbr > 0:
                        depTrade = trd
                    else:
                        if useCurrencyDependency:
                            for t in dependTrades:
                                if t.curr == trd.curr:
                                    depTrade = t
                                    break
                        if not depTrade:
                            depTrade = dependTrades[0]
                    self.adjustPosition(ins, trd, depTrade, posName, manualAction, insIsBarrier)

    def adjustPosition(self, ins, trd, dependent_, posName, manualAction, insIsBarrier):
        logme('- '*23, 'DEBUG')
        logme('Processing %s' % ins.insid, 'DEBUG')
        self.insIsBarrier = insIsBarrier
        ignoreMsg = self.checkTradePosition(ins, trd, posName, manualAction, insIsBarrier)
        if ignoreMsg:
            Summary().ignore(Summary().POSITION, Summary().action, ignoreMsg, posName)
            return
        
        date = self.getDate(ins)

        useTheorValue = 0
        insIsEuropeanSwaption = insIsSwaption(ins) and ins.exercise_type == 'European'
        if insIsEuropeanSwaption:
            useTheorValue = 1
            i = acm.FInstrument[ins.insid]
            calcSpace = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
            theor = i.Calculation().TheoreticalValue(calcSpace)
            settle = theor.Value().Number()                
        elif self.settlePrice: #Find settle price:
            settle = float(self.settlePrice.replace(',', '.'))
        else:
            priceCurr = ins.instype not in ('Future/Forward') and ins.strike_curr or None
            settleIns = ins.instype in ('Future/Forward') and ins or ins.und_insaddr
            settle = settleIns and FBDPInstrument.find_settle_price(ins, settleIns, date, priceCurr, self.settleMarket)
            if not settle:
                if manualAction:
                    msg = 'MANUALLY OVERRIDING: No settle price for underlying'
                    Summary().warning(Summary().POSITION, Summary().action, msg, posName)
                else:
                    msg = 'No settle price for underlying'
                    Summary().ignore(Summary().POSITION, Summary().action, msg, posName)
                    return
            
        if not useTheorValue:
            logme('Will use settle price: %s' % settle, "DEBUG")

        if ins.instype == 'Future/Forward':
            return self.abandon(ins, 
                    trd, 
                    date, 
                    settle, 
                    mode=self.mode,
                    name=posName)
        
        # Barrier Options
        if insIsBarrier:
            (errMsg, type) = self.checkBarrierOption(ins, posName, manualAction)
            if errMsg:
                args = [Summary().POSITION, Summary().action, errMsg, posName]
                if type == 'fail':
                    Summary().fail(*args)
                else:
                    Summary().ignore(*args)
                return

        # Check if derivative is in-the-money.
        InTheMoney = 0
        strike_price = convert_price_to_und_or_strike_quotation(ins, ins.strike_price, 1)            
        if insIsEuropeanSwaption:
            if settle:
                InTheMoney = 1
        
        elif (ins.call_option == 1 and strike_price < settle) or \
           (ins.call_option == 0 and strike_price > settle):
            # ExeAss = 1 => in-the-money
            InTheMoney = 1 
        
        ExeAss = 0 
        Abandon = 0

        actionFromInTheMoney = True
        # If the user has changed the default value 'Normal' value 
        # of the 'Action' column in the Trade Sheet, 
        # always do what the user says, period.
        if manualAction in ['Exercise', 'Abandon', 'Skip']:
            actionFromInTheMoney = False
            logme('Manual override for %s: %s.' % (trd.trdnbr, manualAction))
            # For 'Skip'  keep ExeAss=0 and Abandon=0
            if manualAction == 'Exercise':
                ExeAss = 1
            if manualAction == 'Abandon':
                Abandon = 1
        # If the value of the 'Action' column is not set or is 'Normal,'
        # always perform normal processing.
        elif insIsBarrier:
            exotic = ins.exotics()[0]
            if exotic.barrier_option_type in ('Double Out', 'Down & Out', 'Up & Out') and exotic.barrier_crossed_status == 'Confirmed' or \
                exotic.barrier_option_type in ('Double In', 'Down & In', 'Up & In') and exotic.barrier_crossed_status == 'Confirmed' and not InTheMoney or \
                exotic.barrier_option_type in ('Double In', 'Down & In', 'Up & In') and exotic.barrier_crossed_status == 'None':
                Abandon = 1
                actionFromInTheMoney = False
            elif ins.digital:
                ExeAss = 1
                actionFromInTheMoney = False
        
        if actionFromInTheMoney:
            if InTheMoney:
                if self.doExeAssign:
                    ExeAss = 1
                else:
                    self.debugLogInOrOutTheMoney('In', ins, posName)
                    msg = 'Script executed with "Exercise ITM Normal Trades" untoggled'
                    Summary().ignore(Summary().POSITION, Summary().action, msg, posName)
                    return
            else:
                if self.doAbandon:
                    Abandon = 1
                else:
                    self.debugLogInOrOutTheMoney('Out-Of', ins, posName)
                    msg = 'Script executed with "Abandon OTM and ATM Normal Trades" untoggled'
                    Summary().ignore(Summary().POSITION, Summary().action, msg, posName)
                    return  
                    
        self.abandon(ins,
                    trd,
                    date,
                    settle,
                    exeass=ExeAss,
                    mode=self.mode,
                    aba=Abandon,
                    dependent=dependent_,
                    name=posName,
                    insIsBarrier=insIsBarrier)

    def checkTradePosition(self, ins, trd, posName, manualAction, insIsBarrier):
        if trd.quantity == 0:
            if manualAction:
                Summary().warning(Summary().POSITION, Summary().action, 'MANUALLY OVERRIDING: Zero position', '%s' %posName)
            else:
                return 'Zero position'
                
        if not ins.instype in ['Option', 'Warrant', 'Future/Forward']:
            logme('Instrument %s has the unsupported instrument type %s.' % (ins.insid, ins.instype))
            return 'Unsupported instrument type %s' % ins.instype
        
        if ins.settlement == 'Physical Delivery':
            if ins.und_insaddr.generic:
                if manualAction:
                    msg = 'MANUALLY OVERRIDING: Physical delivery of generic underlying is not supported %s' % (ins.insid)
                    Summary().warning(Summary().POSITION, Summary().action, msg, posName)
                else:
                    msg = 'Physical delivery of generic underlying is not supported %s' % (ins.insid)
                    return msg
            if ins.und_insaddr.notional and not ins.und_insaddr.und_insaddr:
                if manualAction:
                    msg = 'MANUALLY OVERRIDING: No CTD selected.'
                    Summary().warning(Summary().POSITION, Summary().action, msg, posName)
                else:
                    return 'No CTD selected.'
        # European options can not be processed early, except for barriers
        if ins.exercise_type=='European' and ins.exp_day>ael.date_today() and not insIsBarrier:
            if manualAction:
                msg = 'MANUALLY OVERRIDING: European option with Expiry > Today'
                Summary().warning(Summary().POSITION, Summary().action, msg, posName)
            else:
                return 'European option with Expiry > Today'

    def checkBarrierOption(self, ins, posName, manualAction):
        include = 0
        exotic = ins.exotics()[0]
        if exotic.barrier_crossed_status == 'Crossed' and not manualAction:
            msg = 'Barrier Crossed but not yet Confirmed. Change the trade(s) to Confirmed and resubmit:' 
            msg +=  "'%s'."  % ins.insid
            logme(msg, 'ERROR')
            msg = 'Change the trade(s) to Confirmed and resubmit.'
            return (msg, 'fail')
        
        # include all knocked barriers, but not the european
        if exotic.barrier_crossed_status == 'Confirmed' and not ins.exercise_type=='European':
            include = 1
        # include all expired options
        if ins.exp_day <= ael.date_today():
            include = 1                
        # include knocked-out barriers. They should be abandoned.
        if exotic.barrier_option_type in ('Double Out', 'Down & Out', 'Up & Out') and \
            exotic.barrier_crossed_status == 'Confirmed':
            include = 1
        # Include knocked in Digital Barriers, they should be exercised.
        # Except Digital Barrier & Strike European. It becomes Digital Strike European, thus wait until expiry.
        elif exotic.barrier_option_type in ('Double In', 'Down & In', 'Up & In') and \
            ins.digital and exotic.barrier_crossed_status == 'Confirmed' and \
            not exotic.digital_barrier_type == 'Barrier & Strike': 
            include = 1
        elif ins.exercise_type=='European' and ins.exp_day > ael.date_today():
            include = 0
        if include == 0:
            if manualAction:
                msg = 'MANUALLY OVERRIDING: European barrier option with Expiry > Today'
                Summary().warning(Summary().POSITION, Summary().action, msg, posName)
            else:
                msg = 'European barrier option with Expiry > Today'
                return (msg, 'ignore')
        return (None, None)

    def abandon(self, ins, cp, d1, price, exeass=0, mode='Strike', aba=1, dependent=None, name=None, insIsBarrier=False):
        """Close/Abandon/Exercise/Assign a position. For future/forward a price can be given"""
        if ins.instype not in abandon_types:
            logme("To Exercise/Assign/Abandon/Close positions in instruments with instype %s is not supported" % \
                ins.instype, 'WARNING')
            return
        #trade_by_trade = cp.trdnbr > 0 and dependent and dependent.trdnbr == cp.trdnbr
        exp_day=exp_day_to_date(ins)
        n=0
        originalTradePrice = cp.price
        rebate_at_expiry = 0
        t=cp.new()
        for p in t.payments():
            p.delete()
        t.quantity = -t.quantity
        t.curr = t.insaddr.curr
        if t.quantity == 0.0:
            logme('Skipping zero position: ' + name, 'DEBUG')
            return
        if ins.instype == 'Future/Forward':
            t.type = 'Closing'
            summaryType = Summary().CLOSE
        elif exeass == 0:
            t.type = 'Abandon'
            summaryType = Summary().ABANDON
            if aba == 0:
                return
        elif t.quantity < 0:
            t.type = 'Exercise'
            summaryType = Summary().EXERCISE
        else:
            t.type = 'Assign'
            summaryType = Summary().ASSIGN

        create_payment = 0
        pay=None
        
        # Link exercise, and delivery trades
        # by setting their contract trade numbers equal to (one of) the original trade number,
        # in order to enable multiple original trades to be closed 
        # by one exercise trade.
        if dependent:
            t.contract_trdnbr = dependent.trdnbr
            t.connected_trdnbr = None
        else:
            logme("Not linking original, exercise, and delivery trades due to null original.", "WARNING")
        
        if price==None:
            price=suggest_abandon_price(ins, exp_day)
        if ins.instype in ['Option', 'Warrant']:

            from FBDPCommon import create_price, create_quotetype_price   
            strike_price = convert_price_to_und_or_strike_quotation(ins, ins.strike_price, 1)
            if ins.und_instype == 'Curr' and ins.digital:
                t.price = 0.0
                if exeass == 1:
                    if ins.settlement== 'Physical Delivery' and ins.und_instype == 'Curr':
                        paycurr = ins.und_insaddr.insaddr
                    else:
                        paycurr =ins.strike_curr.insaddr
                    
                    create_payment = 1
                    pay = ael.Payment.new(t)
                    pay.curr = paycurr 
                    pay.type = "Cash"
                    pay.amount = -t.quantity * t.insaddr.contr_size
                    if ins.pay_offset_method == 'Business Days':
                        d2 = d1.add_banking_day(pay.curr, ins.pay_day_offset)
                    elif  ins.pay_offset_method == 'Calendar Days':
                        d2 = d1.add_days(ins.pay_day_offset)
                    pay.payday = d2
            elif ins.und_instype == 'Curr' and not ins.digital and not insIsBarrier and ins.settlement=='Cash'                  and exeass ==1:
                t.price = 0.0
                pay = create_fx_vanilla_cash_payment(ins, t, price, d1)
            elif t.type == 'Abandon' or (mode == 'Strike' and ins.settlement == 'Physical Delivery'):
                t.price = 0.0
            elif ins.digital and not insIsBarrier and ins.settlement=='Cash':
                #plain digital without barrier or , cash settle
                t.price = 0.0
                create_payment = 1
                pay = ael.Payment.new(t)
                pay.curr = ins.strike_curr.insaddr
                pay.type = "Cash"
                pay.amount = -t.quantity * t.insaddr.contr_size
                if ins.pay_offset_method == 'Business Days':
                    d2 = d1.add_banking_day(pay.curr, ins.pay_day_offset)
                elif  ins.pay_offset_method == 'Calendar Days':
                    d2 = d1.add_days(ins.pay_day_offset)
                pay.payday = d2
            elif ins.und_instype == 'Curr':
                t.price = 0.0
            else:
                if ins.digital and not insIsBarrier and ins.settlement!='Cash':
                    #plain digital without barrier, physical settle but zero price when exercised.
                    cash_price = 0.0 
                else:
                    cash_price = create_price(ins.und_insaddr, price - strike_price)
                if (not ins.curr.insaddr == ins.strike_curr.insaddr):
                    if (ins.und_instype == 'Curr' and ins.curr.insaddr == ins.und_insaddr.insaddr):
                        if not price == 0.0:
                            cash_price = cash_price / price
                    else:
                        exch = ArenaFunctionBridge.fx_rate(ins.strike_curr.insid, ins.curr.insid, None)
                        cash_price = cash_price * exch
              
                if not ins.call_option:
                    cash_price = - cash_price

                t.price = create_quotetype_price(ins, cash_price)
            
            # barriers
            if insIsBarrier:
                exotic = ins.exotics()[0]
                self.debugLogBarrier(t, ins, exotic, insIsBarrier)
                
                if not ins.digital and rebate_payment_should_be_created(ins, exotic, price, strike_price):
                    create_payment = 1
                    if ins.digital:
                        t.price = 0.0
                    if ins.settlement=='Cash' or (not ins.digital and ins.settlement=='Physical Delivery'):
                        #On non-digital barrier when physical settlement, if abandon then pay actual cash rebate.                 
                        if ins.rebate  != 0.0:    
                            pay = ael.Payment.new(t)
                            pay.curr = ins.strike_curr.insaddr
                            pay.type = "Cash"
                            pay.amount = -ins.rebate*t.quantity*ins.contr_size
                            rebate_at_expiry = exotic.barrier_rebate_on_expiry
        else:
            if t.insaddr.instype == 'Future/Forward' and t.insaddr.und_instype == 'Curr' and \
                t.insaddr.paytype == 'Forward' and t.insaddr.settlement == 'Cash':
                t.reference_price =price
            else:
                t.price = price
            
        t.time = d1.to_time() + TRADE_TIME - 2 # So you can abandon and Clear
        if rebate_at_expiry:
            addFromDate = ins.exp_day
        else:
            addFromDate = d1
        if ins.pay_offset_method == 'Business Days':
            d2 = addFromDate.add_banking_day(ins.strike_curr, ins.pay_day_offset)
        elif  ins.pay_offset_method == 'Calendar Days':
            d2 = addFromDate.add_days(ins.pay_day_offset)
        if insIsBarrier:
            if create_payment == 1 and pay:
                pay.payday = d2
        t.value_day = t.acquire_day = d2
        
        #Create physical trade if derivative is in the money:
        t_und = None

        if t.insaddr.settlement == 'Physical Delivery' \
            and (exeass == 1 or ins.instype == 'Future/Forward') and not t.insaddr.digital:
            if (ins.instype == 'Option' and ins.und_instype == 'Curr' and not ins.digital): 
                und_price = 0.0
                if ins.digital:#4.1 und price and und premium zero for digitals
                    pass
                elif mode == 'Strike':
                    und_price = t.insaddr.strike_price
                elif mode == 'Market':
                    und_price = price
                    und_price = convert_price_to_und_or_strike_quotation(t.insaddr, und_price, 0)
                else:
                    logme('No physical trade price available!', 'ERROR')
                t_und = t.generate_delivery_trade_for_fxoption(und_price)#revise: t_und.q=f(cs).
                cs = t.insaddr.phys_contr_size
                cs_und = t_und.insaddr.contr_size
                if cs == 0:
                    cs = t.insaddr.contr_size
                if ins.digital or t.insaddr.call_option == 1:
                    t_und.quantity = -t.quantity * cs
                else:
                    t_und.quantity = t.quantity * cs

                acm_und_trade=acm.FTrade[t_und.trdnbr];
                acm_und_trade.CLS(acm_und_trade.CheckCLSEligible() )
            else:
                t_und = copyTrade(t)
                t_und.insaddr = t.insaddr.und_insaddr
                t_und.curr = t.insaddr.strike_curr 
                t_und.value_day = t_und.acquire_day = d2
                if t_und.insaddr.notional:
                    t_und.insaddr = t.insaddr.und_insaddr.und_insaddr

            if mode == 'Strike':
                if ins.digital:
                    pass
                elif (abs(ins.phys_contr_size) > 0.000001 and \
                abs(ins.phys_contr_size - ins.contr_size) > 0.000001):
                    # p never committed ???
                    p = create_excess_payment(ins, t_und, price)

            t_und.contract_trdnbr = t.contract_trdnbr
            t_und.connected_trdnbr = None
            cs = t.insaddr.phys_contr_size
            cs_und = t_und.insaddr.contr_size
            if cs == 0:
                cs = t.insaddr.contr_size
            if not (ins.instype == 'Option' and ins.und_instype == 'Curr'):
                if ins.digital or t.insaddr.call_option == 1:
                    t_und.quantity = -t.quantity * cs
                else:
                    t_und.quantity = t.quantity * cs
    
            if ins.instype == 'Future/Forward':
                t_und.quantity = -t.quantity * cs
                t_und.price = t.price
                
                # Forwards in Strike mode + Physical delivery should buy the underlying with 
                # original trade price of the Forward. 
                if t.insaddr.paytype == 'Forward' and mode == 'Strike':
                    t_und.price = originalTradePrice
                    t.price = originalTradePrice

                
                if t_und.insaddr.instype == 'Bond':
                    t_und.quantity = -t.quantity * cs / cs_und
                    conv_factor = 1.0
                    del_link = ael.DeliverableLink.read('owner_insaddr.insaddr = %d \
                    and member_insaddr.insaddr = %d' % (ins.und_insaddr.insaddr, t_und.insaddr.insaddr))
                    if del_link:
                        conv_factor = del_link.conversion_factor
                    t_und.price = t_und.price * conv_factor
                    # p_und never committed ???
                    p_und = create_accrued_payment(t_und)
            elif not (ins.instype == 'Option' and ins.und_instype == 'Curr'):
                if mode == 'Strike':
                    t_und.price = t.insaddr.strike_price
                elif mode == 'Market':
                    t_und.price = price
                    t_und.price = convert_price_to_und_or_strike_quotation(t.insaddr, t_und.price, 0)
                else:
                    logme('No physical trade price available!', 'ERROR')
                
            if exercise_trade_hook:
                t_und = exercise_trade_hook(ins, t_und)
            t_und.premium = FBDPCommon.calculate_premium(t_und)
            self.add_trade(t_und)
            n += 1
            
        if exercise_trade_hook:
            t = exercise_trade_hook(ins, t.new())
            
        if ins.paytype == 'Future':
            t.premium = 0.0    
        else: 
            t.premium = FBDPCommon.calculate_premium(t)            

        self.add_trade(t)
        if create_payment == 1 and pay:
            logme("trade payment. %s" %(pay.pp()), 'DEBUG')
        Summary().ok(Summary().POSITION, summaryType)

        if n == 0:
            logme("No underlying trade done.", 'DEBUG')
        ael.poll()
        hook = additional_excercise_trades_hook
        if hook:
            add_trades = hook(t.new(), t_und and t_und.new(), price, self.ael_variables_dict)
            if add_trades:
                logme("Adding %s extra trades from 'additional_excercise_trades' hook." % len(add_trades), "DEBUG")
                self.beginTransaction()
                for trade in add_trades:
                    self.add_trade(trade)
                try:
                    self.commitTransaction()
                except Exception, e:
                    self.abortTransaction()
                    logme("Could not commit trades defined in additional_excercise_trades hook.", "ERROR")
                    raise e
        ael.poll()

    # Return the manually defined exercise or abandon action, 
    # if any, or None otherwise.
    def getManualOverride(self, ins):
        if self.actionsForTrades:
            for t in ins.trades():
                if t.trdnbr in self.actionsForTrades:
                    action = self.actionsForTrades[t.trdnbr]
                    logme('Found %s: %s.' % (t.trdnbr, action), 'DEBUG')
                    if action == 'Exercise' or action == 'Abandon':
                        return action
        return None
    
    def getDate(self, ins):
        import time
        if self.insDates.has_key(ins.insid):
            return self.insDates[ins.insid]
        elif ins.exp_day and ins.exp_day <= ael.date_today():
            date = ins.exp_day
        elif self.insIsBarrier and ins.exotics()[0].barrier_crossed_status == 'Confirmed' and \
            ins.exotics()[0].barrier_rebate_on_expiry:
            date = ins.exp_day
        else: 
            date = ael.date_today()
        t = ael.date(time.strftime('%Y %m %d', time.localtime(ins.exp_time)))
        if t <= date and t > ael.date('1970-01-02'):
            date = t
        self.insDates[ins.insid] = date
        return date
    
    def debugLogBarrier(self, t, ins, exotic, insIsBarrier):
        msg = 'Settlement %s |digital %s |barrier %s |dbtype %s |crossed %s |btype %s' \
            % (t.insaddr.settlement, \
               ins.digital, \
               insIsBarrier, \
               exotic.digital_barrier_type, \
               exotic.barrier_crossed_status, \
               exotic.barrier_option_type)
        logme (msg, 'DEBUG')
        
    def debugLogInOrOutTheMoney(self, inOut, ins, posName):
        msg = "\nPosition %s skipped." %posName
        if inOut == 'In':
            param = 'Exercise ITM'
        else:
            param = 'Abandon OTM and ATM'
        msg += "\nReason: instrument %s is %s-The-Money" %(ins.insid, inOut)
        msg += " and the '%s Normal Trades'-parameter is untoggled." %param
        logme (msg, 'DEBUG')

#___end class Exercise___

# Function for converting the exp_day to true exp_day
def exp_day_to_date(ins):
    a_day=24*60*60
    if ins.exp_time > a_day and ins.exp_time < 2 * a_day:
        return ins.exp_day.add_days(-1)
    else:
        return ins.exp_day

# function returns one if instrument is a barrier option, else zero
def isBarrier(ins):
    if ins.record_type == 'Instrument' and \
        ins.instype == 'Option' and \
        ins.exotic_type == 'Other' and \
        ins.exotics() and \
        ins.exotics()[0] and \
        ins.exotics()[0].barrier_option_type != 'None':
            return 1
    return 0

# Function returns 1 if instrument is a swaption, otherwise 0
def insIsSwaption(ins):
    if ins.record_type == 'Instrument' and \
        ins.instype == 'Option' and \
        ins.und_insaddr.instype == 'Swap':
            return 1
    return 0

def suggest_abandon_price(ins, date=None):
    if not date:
        try:
            date=exp_day_to_date(ins)
        except:
            date=ael.date_today()
    if ins.instype in ['Option', 'Warrant']:
        return 0.0
    elif ins.instype == 'Future/Forward':
        settle_price = FBDPInstrument.find_price(ins, date, settlement_market='SETTLEMENT')
        if not settle_price:
            raise 'No settlement price found for %s on date %s' % (ins.insid, date)
        return settle_price
    elif ins.instype == 'Bond':
        return 100.0
    else:
        return 0.0

def rebate_payment_should_be_created(ins, exotic, price, strike_price):
    isOutBarrier = exotic.barrier_option_type in ('Double Out', 'Down & Out', 'Up & Out')
    digital_type = exotic.digital_barrier_type
    crossed = exotic.barrier_crossed_status
    call = ins.call_option
    diff = price - strike_price
    if ins.digital and (isOutBarrier and crossed == 'None' or not isOutBarrier and crossed == 'Confirmed'):
        if digital_type == 'Barrier' or (call and diff > 0) or (not call and diff < 0):
            return True
    elif not ins.digital and (isOutBarrier and crossed == 'Confirmed' or not isOutBarrier and crossed == 'None'):
        return True
    return False

# function returns the price converted to either the underlying quotation or
# the strike quotation
def convert_price_to_und_or_strike_quotation(ins, price, convert_to_und_quotation):  
    if ((ins.record_type == 'Instrument') and ins.und_insaddr):
        if (ins.und_insaddr.quotation_seqnbr and 
            ins.strike_quotation_seqnbr and 
            ins.strike_quotation_seqnbr != ins.und_insaddr.quotation_seqnbr):
                instr = acm.FInstrument[ins.insaddr]
                und_instr = acm.FInstrument[ins.und_insaddr.insaddr]
                date_today = acm.Time().DateToday()
                #doubleCast = acm.GetFunction('double', 1)
                denom_func = acm.GetFunction('denominatedvalue', 4)
                denom_val = denom_func(price, ins.und_insaddr.insid, None, ael.date_today())
                
                if (convert_to_und_quotation == 1):
                    to_quotation = und_instr.Quotation()
                    from_quotation = instr.StrikeQuotation()
                else:
                    from_quotation = und_instr.Quotation()
                    to_quotation = instr.StrikeQuotation()

                lprice_denom_val = instr.QuoteToQuote(denom_val, date_today,
                                                      None, from_quotation,
                                                      to_quotation)
                lprice=lprice_denom_val.Number()

                return lprice

    return price

def copyTrade(t):
    d = fieldsFromTemplate(t, exclude=('trdnbr',))
    t = ael.Trade.new(t.insaddr)
    for key, value in d.items():
        setattr(t, key, value)
    return t

def fieldsFromTemplate(t, exclude=()):
    d = {}
    for c in t.columns():
        if c not in exclude:
            try:
                d[c] = getattr(t, c)
            except AttributeError:
                logme(c, "ERROR")
    return d

def create_accrued_payment(t):
    accrued = ArenaFunctionBridge.instrument_accrued_interest(t.insaddr, t.value_day) * t.quantity
    p = ael.Payment.new(t)
    p.payday = t.value_day
    p.amount = -float(accrued)
    p.curr = t.curr
    p.type = 'Cash'
    p.ptynbr = t.counterparty_ptynbr
    p.text = 'Accrued Interest'
    p.valid_from = ael.date_from_time(t.time)

    s = 'Created Accrued Interest Payment: %f, %s' % (p.amount, p.curr.insid)
    logme(s, 'DEBUG')
    return p

def create_excess_payment(ins, t_und, settle):
    if not (ins.instype == 'Option'):
        s = 'Trying to create Exercise Payment for %s: %s.\
        Excess payments can only be created for Options.'\
        % (ins.instype, ins.insid)
        logme(s, 'ERROR')
        logme(None, 'ABORT')
        raise RuntimeError

    excess_lots = ins.contr_size - ins.phys_contr_size
    strike_price = convert_price_to_und_or_strike_quotation(ins, ins.strike_price, 1)
    if ins.call_option == 1:
        trade_price = FBDPCommon.create_quotetype_price(ins, settle - strike_price)
    else:
        trade_price = FBDPCommon.create_quotetype_price(ins, strike_price - settle)

    premium = ArenaFunctionBridge.trade_premium_from_quote(t_und.trdnbr, trade_price, t_und.acquire_day)
    pmnt_amount = premium * excess_lots 

    p = ael.Payment.new(t_und)
    p.payday    = ael.date(ArenaFunctionBridge.trade_spot_date(t_und.trdnbr, ael.date_from_time(t_und.time)))
    p.amount    = float(pmnt_amount)
    p.curr      = t_und.curr
    p.type      = 'Exercise Cash'
    p.ptynbr    = t_und.counterparty_ptynbr
    p.valid_from = ael.date_from_time(t_und.time)

    s = 'Created Exercise Payment: %f\nCurr: %s' % (p.amount,
        p.curr.insid)
    logme(s)
    return p

# ------------------------------------------------------------------
# Functions below called by FSetFinalExercisePrices
# ------------------------------------------------------------------

# Select all trades with trade type set to
# Exercise, Assign or Closing where trade time equals the input date
def get_trades(exer_date):
    exer_date = ael.date(str(exer_date))
    exer_trades = []
    all_trades = ael.Trade.select()
    for t in all_trades:
        if t.time > 0 and ael.date_from_time(t.time) == exer_date:
            if t.type in ('Exercise', 'Assign') and t.insaddr.instype in ('Option', 'Warrant'):
                pass
            elif t.type == 'Closing' and t.insaddr.instype == 'Future/Forward' and t.insaddr.settlement == 'Cash':
                pass
            else:
                continue
            exer_trades.append(t)
            logme('Will update trade %s in %s.' % (t.trdnbr, t.insaddr.insid))
    return exer_trades

# Find the physical delivery trade corresponding to the exercise trade
def get_physical_trade(t_exer):
    if not t_exer.insaddr.und_insaddr:
        return None
    ins = ael.Instrument.read('insaddr=%d'
                              %(t_exer.insaddr.insaddr))
    is_strike_quotation_different = 0
    if (ins.und_insaddr.quotation_seqnbr and ins.strike_quotation_seqnbr and 
        ins.strike_quotation_seqnbr != ins.und_insaddr.quotation_seqnbr):
        is_strike_quotation_different = 1

    und = ael.Instrument.read('insaddr=%d'
                              %(t_exer.insaddr.und_insaddr.insaddr))
    pr_trades = ael.Trade.select('contract_trdnbr=%d' %(t_exer.contract_trdnbr))
    for t in pr_trades:
        if t.insaddr.insaddr == und.insaddr:
            return t
        elif (is_strike_quotation_different and (t.curr.insaddr == und.insaddr)):
            return t


# Update the payment of type Exercise Cash or create it if it doesn't exist
def update_exercise_payment(t_exer, settle, mode, TestMode):
    found = 0
    excess_lots = t_exer.insaddr.contr_size - t_exer.insaddr.phys_contr_size

    if t_exer.insaddr.instype == 'Option': 
        strike_price = convert_price_to_und_or_strike_quotation(t_exer.insaddr, t_exer.insaddr.strike_price, 1)
        if t_exer.insaddr.call_option == 1:
            trade_price = FBDPCommon.create_quotetype_price(t_exer.insaddr, \
                          settle - strike_price)
        else:
            trade_price = FBDPCommon.create_quotetype_price(t_exer.insaddr, \
                          strike_price - settle)
    else:
        trade_price = settle

    premium = ArenaFunctionBridge.trade_premium_from_quote(t_exer.trdnbr, trade_price, t_exer.acquire_day)
    new_amount = premium * excess_lots / t_exer.insaddr.contr_size
    payments = ael.Payment.select('trdnbr=%d' %(t_exer.trdnbr))
    
    for p in payments:

        if (p.type == 'Exercise Cash' and mode == 'Strike'):
            found=1
            payment_clone = p.clone()
            payment_clone.amount = new_amount
            if not TestMode:
                payment_clone.commit()

    t_exer_clone = t_exer.clone()
    payments_clone = t_exer_clone.payments()

    for p in payments_clone:
        if (p.type == 'Exercise Cash' and mode == 'Market'):
            found=1
            p.delete()

    if not TestMode:
        t_exer_clone.commit()


    if not found and mode == 'Strike':
        t_exer_clone        = t_exer.clone()
        new_payment         = ael.Payment.new(t_exer_clone)
        new_payment.ptynbr  = t_exer.counterparty_ptynbr
        new_payment.type    = 'Exercise Cash'
        new_payment.amount  = new_amount
        new_payment.curr    = t_exer.insaddr.curr
        new_payment.payday  = ArenaFunctionBridge.trade_spot_date(t_exer.trdnbr, ael.date_from_time(t_exer.time))
    if not TestMode:
        t_exer_clone.commit()



"""----------------------------------------------------------------------------
FUNCTION
    set_final_settle_prices(pr_trades, exer_date, mode)

DESCRIPTION
    Sets the final settlement price in all exercising derivatives trades,
    and potential corresponding physical delivery trades, done on the
    specified date.

    Cash settled instruments: Read the price on the SETTLEMENT market
    first. If there is no such price, read the settle price from the
    market on which the trade was done. Set the price of the closing
    derivative trade to the difference between the settle price and the
    strike and change the premium accordingly.

    Physical settled instruments: Either the physical trade is done to
    market, in which case the exercise trade should carry the difference
    between strike and the settlement price, or the physical trade is done
    to the strike in which case the exercise trade should get the price
    and premium zero.

ARGUMENTS
    The function takes the following arguments:
    1) trades - The Exercise trades found in get_trades().
    2) exer_date - Only Exercised trades done on this date are handled,
       i.e. the trade time of the trade with type Exercise, Assign or
       Abandon should equal this date. The settlement prices should also
       have been entered on this date.
    3) mode - This could either be set to Strike or to Market. This
       depends on whether the physical delivery trade is done to the
       strike price or to market price.
----------------------------------------------------------------------------"""

def set_final_settle_prices(pr_trades, exer_date, mode, TestMode):
    if not pr_trades:
        logme('No Exercise/Assign trades made on date %s' % exer_date, 'WARNING')
        return

    for t in pr_trades:
        ins = t.insaddr
        priceCurr = ins.instype in ('Option', 'Warrant') and ins.strike_curr or None
        settle_price = FBDPInstrument.find_settle_price(ins, ins.und_insaddr,
                                                 exer_date,
                                                 priceCurr,
                                                 "SETTLEMENT")

        if not settle_price:
            logme('Will skip trade %s since there is no price for this instrument %s.' % (t.trdnbr, ins.insid))
            continue
        
        strike_price = convert_price_to_und_or_strike_quotation(ins, ins.strike_price, 1)
        
        if ins.settlement == 'Cash':
            if ins.call_option:
                p_der = FBDPCommon.create_quotetype_price(ins,\
                        settle_price - strike_price)
            elif ins.instype == 'Future/Forward':
                p_der = settle_price
            else:
                p_der = FBDPCommon.create_quotetype_price(ins,\
                        strike_price - settle_price)

        else:  #Physical settlement
            p_phys = 0.0 #price to be set in the physical trade
            t_phys = get_physical_trade(t)
            if not t_phys:
                logme('Physical settlement trade does not exist for trade %d.'\
                      % t.trdnbr)
                continue
            if mode == 'Market':
                p_phys = settle_price
                if ins.instype == 'Option':
                    p_phys = settle_price
                    if ins.call_option:
                        p_der = FBDPCommon.create_quotetype_price(ins, \
                                settle_price - strike_price)
                    else:
                        p_der = FBDPCommon.create_quotetype_price(ins,\
                                strike_price - settle_price)
                else: #Future
                    p_der = settle_price

            else: #Physical is done to the strike price (Strike mode)
                p_der = 0.0
                if ins.instype == 'Option':
                    p_phys = ins.strike_price
                else: #Future
                    p_phys = settle_price
                    
                if (abs(ins.phys_contr_size) > 0.000001 and \
                abs(ins.phys_contr_size - ins.contr_size) > 0.000001):
                    update_exercise_payment(t, settle_price, mode, TestMode)
                
                phys_clone = t_phys.clone()
                phys_clone.price = p_phys
                if (ins.instype == 'Option' and ins.und_instype == 'Curr'): 
                    phys_clone.fx_update_non_dealt_amount(p_phys)
                else:
                    phys_clone.premium = \
                        ArenaFunctionBridge.trade_premium_from_quote(phys_clone.trdnbr, p_phys, phys_clone.acquire_day)
                if not TestMode:
                    phys_clone.commit()

        der_clone = t.clone()
        der_clone.price = p_der
        der_clone.premium = ArenaFunctionBridge.trade_premium_from_quote(der_clone.trdnbr, p_der, t.acquire_day)
        
        if not TestMode:
            der_clone.commit()
        ael.poll
        
def create_fx_vanilla_cash_payment(ins, t_und, settle, d1):
    if not (ins.instype == 'Option'):
        s = 'Trying to create Exercise Payment for %s: %s.\
        Excess payments can only be created for Options.'\
        % (ins.instype, ins.insid)
        logme(s, 'ERROR')
        logme(None, 'ABORT')
        raise RuntimeError
    if ins.add_info('Settlement_Curr'):
        cashCurr = ael.Instrument[ins.add_info('Settlement_Curr')]
        strike_price = convert_price_to_und_or_strike_quotation(ins, ins.strike_price, 1)
        if ins.call_option == 1:
            trade_price = FBDPCommon.create_quotetype_price(ins, settle - strike_price)
        else:
            trade_price = FBDPCommon.create_quotetype_price(ins, strike_price - settle)

        pmnt_amount = ArenaFunctionBridge.trade_premium_from_quote(t_und.trdnbr, trade_price, t_und.acquire_day)
        
        if cashCurr != ins.strike_curr:
            pmnt_amount= pmnt_amount/float(settle)
            

        p = ael.Payment.new(t_und)
        if ins.pay_offset_method == 'Business Days':
            d2 = d1.add_banking_day(cashCurr, ins.pay_day_offset)
        elif  ins.pay_offset_method == 'Calendar Days':
            d2 = d1.add_days(ins.pay_day_offset)
        
        p.payday    = d2
        p.amount    = float(pmnt_amount)
        p.curr      = cashCurr
        p.type      = 'Cash'
        p.ptynbr    = t_und.counterparty_ptynbr
        p.valid_from = ael.date_from_time(t_und.time)

        s = 'Created Exercise Payment for Cash Settled Vanilla: %f\nCurr: %s' % (p.amount,
            p.curr.insid)
        logme(s)
        return p
