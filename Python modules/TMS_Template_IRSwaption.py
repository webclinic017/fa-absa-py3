'''------------------------------------------------------------------------------
Create Date:    2008-06-03

Developer:      Neil Retief

Description:    TMS Template for IR Swaptions

---------------------------------------------------------------------------------'''

import ael, amb, time, datetime, TMS_Functions, SAGEN_Resets, SAGEN_Cashflows

#Template for IRSwaption in TMS

def IRSwaption_Message(ent_op, entity_addr):

    #Get the trade object
    TObject = ael.Trade[(int)(entity_addr)]
    
    #Get the instrument object
    IObject = ael.Instrument[TObject.insaddr.insaddr]
    #Get the underlying instrument object
    if IObject.und_instype != 'None':
        Und_IObject = ael.Instrument[TObject.insaddr.und_insaddr.insaddr]
    else:
        Und_IObject = ''
    
    #For the IRSwaption the Leg will be on the underlying instrument
    if IObject.und_instype != 'None':
        LObject = ael.Leg.select('insaddr=%d'%Und_IObject.insaddr)
    else:
        LObject = ael.Leg.select('insaddr=%d'%IObject.insaddr)
        
    #Check the operation to send the correct message header
    if ent_op == 'UPDATE_TRADE':# and TObject.optional_key:
        #create the message header
        message = amb.mbf_start_message(None, "UPDATE_TRADE", "1.0", None, "AMBA_TMS")
    else:
        message = amb.mbf_start_message(None, "INSERT_TRADE", "1.0", None, "AMBA_TMS")
            
    #Get the current date
    DateToday = TMS_Functions.Date()
    
    #Create the first list = TRADE along with all TRADE attributes
    Trade_msg = message.mbf_start_list("TRADE")
    Trade_msg.mbf_add_int("TrdNbr", TObject.trdnbr)
    #Add the Deal ID if one exists
    if TObject.trx_trdnbr:
        Trade_msg.mbf_add_int("DealID", TObject.trx_trdnbr)
    Trade_msg.mbf_add_int("Version_Id", TObject.version_id)
    Trade_msg.mbf_add_string("Time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TObject.time)))
    Trade_msg.mbf_add_string("Creat_Time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TObject.creat_time)))
    Trade_msg.mbf_add_string("Updat_Time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TObject.updat_time)))
    Trade_msg.mbf_add_string("Type", TObject.type)
    Trade_msg.mbf_add_string("TradeUpdateUser", TMS_Functions.Get_BarCap_User_ID(TObject.updat_usrnbr))
    Trade_msg.mbf_add_string("Status", TObject.status)
    Trade_msg.mbf_add_string("Trader", TMS_Functions.Get_BarCap_User_ID(TObject.trader_usrnbr))
    Trade_msg.mbf_add_string("CP", TMS_Functions.Get_BarCap_SDS_ID(TObject.counterparty_ptynbr))
    Trade_msg.mbf_add_string("TradeCurr", TObject.display_id('curr'))
    Trade_msg.mbf_add_double("Quantity", TObject.quantity)
    Trade_msg.mbf_add_double("TradeNominal", TObject.nominal_amount())
    
    #Pass both the Portfolio name as well as the SMS Book ID
    Trade_msg.mbf_add_string("Portfolio", TObject.display_id('prfnbr'))
    Trade_msg.mbf_add_string("Book_ID", TMS_Functions.Get_BarCap_Book_ID(TObject.prfnbr))
    Trade_msg.mbf_add_string("Strategy_Book", TMS_Functions.Get_BarCap_Strategy_Book_Name(TObject.prfnbr))
    Trade_msg.mbf_add_string("Strategy_Book_ID", TMS_Functions.Get_BarCap_Strategy_Book_ID(TObject.prfnbr))
    Trade_msg.mbf_add_string("Acquirer", TMS_Functions.Get_BarCap_SDS_ID(TObject.acquirer_ptynbr))
    Trade_msg.mbf_add_double("Fee", TObject.fee)
    
    #This part will get the broker linked to the additional payment of type Broker Fee if the broker on the face of the trade is blank
    #---------------------------------------------------------------------------------------------------------------------------------
    list=[]
    for P in TObject.payments():
        if P.type == 'Broker Fee':
            PayM = (P.type, P.ptynbr)
            list.append(PayM)
    
    list.sort()
    if TObject.broker_ptynbr:
        Trade_msg.mbf_add_string("Broker", TMS_Functions.Get_BarCap_SDS_ID(TObject.broker_ptynbr))
    else:
        if list:
            Trade_msg.mbf_add_string("Broker", TMS_Functions.Get_BarCap_SDS_ID(list[0][1]))
        else:
            Trade_msg.mbf_add_string("Broker", '0')
    #This part will get the broker linked to the additional payment of type Broker Fee if the broker on the face of the trade is blank
    #---------------------------------------------------------------------------------------------------------------------------------

    Trade_msg.mbf_add_double("Premium", TObject.premium)
    Trade_msg.mbf_add_string("Value_Day", TObject.value_day.to_string('%Y-%m-%d'))
    
    #Create the second list - INSTRUMENT along with all relevant INSTRUMENT attributes
    #Instrument will be a child of Trade
    Inst_msg = Trade_msg.mbf_start_list("INSTRUMENT")
    Inst_msg.mbf_add_string("InsID", IObject.insid)
    Inst_msg.mbf_add_string("Instype", IObject.instype)
    Inst_msg.mbf_add_string("Und_Instype", Und_IObject.instype)
    Inst_msg.mbf_add_int("version_id", IObject.version_id)
    Inst_msg.mbf_add_string("exercise_type", IObject.exercise_type)
    Inst_msg.mbf_add_string("settlement", IObject.settlement)
    Inst_msg.mbf_add_string("updat_time", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(IObject.updat_time)))
    Inst_msg.mbf_add_string("UpdateUser", TMS_Functions.Get_BarCap_User_ID(IObject.updat_usrnbr))
    Inst_msg.mbf_add_int("otc", IObject.otc)
    #Inst_msg.mbf_add_int("call_option",IObject.call_option)
    Inst_msg.mbf_add_double("contr_size", IObject.contr_size)
    Inst_msg.mbf_add_string("exp_day", IObject.exp_day.to_string('%Y-%m-%d'))
    Inst_msg.mbf_add_string("exp_time", time.strftime("%H:%M:%S", time.localtime(IObject.exp_time)))
    Inst_msg.mbf_add_string("Curr", IObject.display_id('curr'))
    
    #Calculate the Global Reset day - it will either be the current reset day or the next reset day
    #If the underlying exist - based on the underlying, otherwise, main instrument
    if IObject.und_instype != 'None':
        Inst_msg.mbf_add_string("Global_Reset_Day", TMS_Functions.Get_Global_Reset_Day(Und_IObject.insaddr, DateToday))
    else:
        Inst_msg.mbf_add_string("Global_Reset_Day", TMS_Functions.Get_Global_Reset_Day(IObject.insaddr, DateToday))


    #Get all the exercise events if the trade is a Bermudan Swaption
    if IObject.exercise_type == 'Bermudan':
        Events = []
        for e in IObject.exercise_events():
            Events_Tuple = (e.day, e)
            Events.append(Events_Tuple)
    
        Events.sort()
        
        for e in Events:
            events = e[1]
            Events_msg = Inst_msg.mbf_start_list("EXERCISE_EVENTS")
            Events_msg.mbf_add_string("Exp_Day", events.day.to_string('%Y-%m-%d'))
            Events_msg.mbf_add_string("Notice_Day", events.notice_day.to_string('%Y-%m-%d'))    
    
            #End reset list
            Events_msg.mbf_end_list()
        
        
    #Create the third list - LEG
    #Create a list object with the legs in so that legs can be sorted on type
    Legs = []
    
    for l in LObject:
        L_Tuple = (l.type, l)
        Legs.append(L_Tuple)

    #Sort the cashflows
    Legs.sort()
    
    
    #Leg will be a child of Instrument
    for Leg in Legs:
        l = Leg[1]
        #Start list
        Leg_msg = Inst_msg.mbf_start_list("LEG")
        
        #Include for all legs of the instrument
        Leg_msg.mbf_add_string("L_Curr", l.display_id('curr'))    
        Leg_msg.mbf_add_string("Type", l.type)
        Leg_msg.mbf_add_string("start_day", l.start_day.to_string('%Y-%m-%d'))
        Leg_msg.mbf_add_string("end_day", l.end_day.to_string('%Y-%m-%d'))    
        
        #----------------------------------------------------------
        #Create an if statement to get the value of pay and receive
        #Get the current or next cashflow number so that the projected cashflow amount can be obtained

        #if ((IObject.call_option == 0 and l.type == 'Float') or (IObject.call_option == 1 and l.type == 'Fixed')):
        #if ((l.payleg == 1 and TObject.quantity > 0) or (l.payleg == 0 and TObject.quantity < 0)):
        #Get a list of all the cashflows for pay and receive calcs.

        #----------------------------------------------------------
        #Get the value of the current cashflows projected cashflow
        CFS = []
        
        for c in l.cash_flows():
            CF_Tuple = (c.pay_day, c.end_day, c)
            CFS.append(CF_Tuple)

        #Sort the cashflows
        CFS.sort()
        
        #Add all relevant columns for CashFlows
        count = 0
        
        while count < 1:
            cf = CFS[count][2]
    
            count = count + 1
            
            if (TObject.quantity * cf.projected_cf()) < 0:
                PayRec = 'Yes'
            else:
                PayRec = 'No'
                
            Leg_msg.mbf_add_string("payleg", PayRec)
        #----------------------------------------------------------
        '''        
        if l.payleg == 1:
            PayRec = 'Yes'
        else:
            PayRec = 'No'
                
        Leg_msg.mbf_add_string("payleg",PayRec)
        '''
        #-------------------------------------------------------------------------
        #Create an if statement to check whether nominal will be paid at the start
        if l.nominal_at_start == 1:
            NomAtStart = 'Yes'
        else:
            NomAtStart = 'No'
        Leg_msg.mbf_add_string("nominal_at_start", NomAtStart)
        #-------------------------------------------------------------------------
        #-----------------------------------------------------------------------
        #Create an if statement to check whether nominal will be paid at the end
        if l.nominal_at_end == 1:
            NomAtEnd = 'Yes'
        else:
            NomAtEnd = 'No'
        Leg_msg.mbf_add_string("nominal_at_end", NomAtEnd)
        #-----------------------------------------------------------------------
        Leg_msg.mbf_add_int("rolling_period.count", getattr(l, 'rolling_period.count'))
        Leg_msg.mbf_add_string("rolling_period.unit", getattr(l, 'rolling_period.unit'))
        Leg_msg.mbf_add_string("pay_day_method", l.pay_day_method)
        Leg_msg.mbf_add_int("pay_day_offset.count", getattr(l, 'pay_day_offset.count'))
        Leg_msg.mbf_add_string("daycount_method", l.daycount_method)
        Leg_msg.mbf_add_string("LegStartDayOfMonth", l.start_day.to_string('%d'))
        Leg_msg.mbf_add_string("LegEndDayOfMonth", l.end_day.to_string('%d'))
        Leg_msg.mbf_add_string("PayCal", TMS_Functions.Get_BarCap_Calendar(l.display_id('pay_calnbr'), l.display_id('pay2_calnbr'), l.display_id('pay3_calnbr'), l.display_id('pay4_calnbr'), l.display_id('pay5_calnbr')))
        Leg_msg.mbf_add_string("LegFloatRate", l.display_id('float_rate'))
        
        #Reset Day Method
        if l.reset_day_method:
            Leg_msg.mbf_add_string("reset_day_method", l.reset_day_method)
        else:
            Leg_msg.mbf_add_string("reset_day_method", '')
            
        #Get the Leg nominal
        Leg_msg.mbf_add_double("LegNominal", TObject.quantity * IObject.contr_size * l.nominal_factor)
    
        if l.type == 'Float':
            if l.spread != 'None':
                Leg_msg.mbf_add_double("Spread", l.spread/100)
            else:
                Leg_msg.mbf_add_double("Spread", 0)
                
            Leg_msg.mbf_add_int("reset_period_count", getattr(l, 'reset_period.count'))    
            Leg_msg.mbf_add_string("reset_period_unit", getattr(l, 'reset_period.unit'))
            
            #Get the list of Reset Calendars
            Leg_msg.mbf_add_string("ResetCal", TMS_Functions.Get_BarCap_Calendar(l.display_id('reset_calnbr'), l.display_id('reset2_calnbr'), l.display_id('reset3_calnbr'), l.display_id('reset4_calnbr'), l.display_id('reset5_calnbr')))
            Leg_msg.mbf_add_double("AccruedIncluded", l.accrued_included)
            Leg_msg.mbf_add_int("reset_day_offset", l.reset_day_offset)
            Leg_msg.mbf_add_int("reset_in_arrear", l.reset_in_arrear)
    
        if l.type == 'Fixed':
            Leg_msg.mbf_add_double("fixed_rate", l.fixed_rate)
        

        #Build a list of cashflows so that the cashflows can be sorted on pay_day
        CFS = []
        
        for c in l.cash_flows():
            CF_Tuple = (c.pay_day, c.end_day, c)
            CFS.append(CF_Tuple)

        #Sort the cashflows
        CFS.sort()
        
        #Add all relevant columns for CashFlows
        for c in CFS:
            cf = c[2]
            
            if cf.type != 'Fixed Amount':
                #Start cashflow list
                
                CF_msg = Leg_msg.mbf_start_list("CASHFLOW")
                
                CF_msg.mbf_add_string("start_day", cf.start_day.to_string('%Y-%m-%d'))
                CF_msg.mbf_add_string("end_day", cf.end_day.to_string('%Y-%m-%d'))
                CF_msg.mbf_add_string("pay_day", cf.pay_day.to_string('%Y-%m-%d'))
                #------------------------------------------
                #Pass the cashflow rate only for fixed legs
                if l.type == 'Fixed':
                    CF_msg.mbf_add_double("CFRate", cf.rate)
                #------------------------------------------
                CF_msg.mbf_add_double("CFNominal", TObject.quantity * IObject.contr_size * cf.nominal_factor)
                #------------------------------------------------------
                #Pass the projected cashflow amount only for float legs
                if l.type == 'Float':
                    if cf.spread != 'None':
                        CF_msg.mbf_add_double("spread", cf.spread/100)
                    else:
                        CF_msg.mbf_add_double("spread", 0)
                #------------------------------------------------------
                
                #End cashflow list
                CF_msg.mbf_end_list()
                
                #Add all relevant columns for resets
                for r in cf.resets():
                    #Start reset list
                    R_msg = CF_msg.mbf_start_list("RESET")
                    
                    if r.day.to_string('%Y-%m-%d') <= DateToday:
                        R_msg.mbf_add_double("fixing_rate", r.value)
                    else:
                        R_msg.mbf_add_double("fixing_rate", 0)

                    R_msg.mbf_add_string("day", r.day.to_string('%Y-%m-%d'))
                    R_msg.mbf_add_string("start_day", r.start_day.to_string('%Y-%m-%d'))
                    R_msg.mbf_add_string("end_day", r.end_day.to_string('%Y-%m-%d'))
                    R_msg.mbf_add_string("ResetDayOfMonth", r.day.to_string('%d'))
                    
                    #End reset list
                    R_msg.mbf_end_list()
        
    #Add child under TRADE for all fees applicable on the day
    #Send through a list of the applicable payments on the trade
    #If a premium exists - send it through
    if TObject.premium:
        F_msg = Trade_msg.mbf_start_list("FEES")
        F_msg.mbf_add_string("FEE_DATE", TObject.value_day.to_string('%Y-%m-%d'))
        F_msg.mbf_add_double("FEE_AMOUNT", TObject.premium)
        F_msg.mbf_add_string("FEE_TYPE", 'Premium')
        F_msg.mbf_end_list()

    #If a brokerage exists - send it through
    if TObject.fee:
        if IObject.exercise_type == 'European':
            Type = TObject.fee
        else:
            Type = 'Premium'
            
        F_msg = Trade_msg.mbf_start_list("FEES")
        F_msg.mbf_add_string("FEE_DATE", TObject.value_day.to_string('%Y-%m-%d'))
        F_msg.mbf_add_double("FEE_AMOUNT", Type)
        F_msg.mbf_add_string("FEE_TYPE", Type)
        F_msg.mbf_end_list()

    for p in TObject.payments():
        if IObject.exercise_type == 'European':
            Type = p.type
        else:
            Type = 'Premium'

        F_msg = Trade_msg.mbf_start_list("FEES")
        F_msg.mbf_add_string("FEE_DATE", p.payday.to_string('%Y-%m-%d'))
        F_msg.mbf_add_double("FEE_AMOUNT", p.amount)
        F_msg.mbf_add_string("FEE_TYPE", Type)
        F_msg.mbf_end_list()
        
    
    Trade_msg.mbf_end_list()
    Inst_msg.mbf_end_list()
    Leg_msg.mbf_end_list()
    
    #End the message and assign to variable
    FinalMsg = message.mbf_end_message()
        
    return FinalMsg
