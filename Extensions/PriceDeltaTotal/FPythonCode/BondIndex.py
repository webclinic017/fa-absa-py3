''' Calculate the value of a bond index according to the BEASSA Total Return Indices 2000 documentation 
    which can be found at: http://www.bondexchange.co.za/besa/view/besa/en/page44998
    
    Paul Jacot-Guillarmod, 2009/08/12
'''

import acm, ael, csv, string, time
from at_time import acm_datetime
from at_type_helpers import to_ael

# Used to convert the KFactor for storing in the time series (10**18)
KFactor_Multiplier = float(1000000000000000000)
calc_space_collection = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def first_weekday_of_month(month_date, day):
    ''' Returns the date of the first week day (specified by day) of the month in month_date
        e.g. To get the first Thursday of a given month:
        first_weekday_of_month(ael.date(2009-07-15), 'Thu') = 2009-07-02
    '''
    week_days = {'Mon':1, 'Tue':2, 'Wed':3, 'Thu':4, 'Fri':5, 'Sat':6, 'Sun':7}
    first_day = month_date.first_day_of_month()
    num_days = (week_days[day] - first_day.day_of_week()) % 7
    
    return first_day.add_days(num_days)
    
def rebasing_day(method='Next', input_date=ael.date_today()):
    ''' Returns the next or previous rebasing day in relation to the input_date.  The rebasing day is the first 
        Thursday of every month adjusted to the preceding banking day in the case of public holidays.
        
        method is either Previous or Next
    ''' 
    first_day = input_date.first_day_of_month()
    rebase_day = first_weekday_of_month(first_day, 'Thu').adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding')
    
    if input_date <= rebase_day and method == 'Next':
        return rebase_day
    elif input_date > rebase_day and method == 'Next':
        return first_weekday_of_month(first_day.add_months(1), 'Thu').adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding')
    elif input_date < rebase_day and method == 'Previous':
        return first_weekday_of_month(first_day.add_months(-1), 'Thu').adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding')
    elif input_date >= rebase_day and method == 'Previous':
        return rebase_day

def triple_to_date(t):
    ''' Converts an integer triple [yyyy, mm, dd] to an ael date
    '''
    return ael.date('-'.join([string.zfill(s, 2) for s in t]))

def ncd(bnd, settlement_day):
    ''' Returns the next coupon date for a given bond and settlement date
    '''
    return min([cf.end_day for cf in ael.Instrument[bnd].cash_flows() if cf.type == 'Fixed Rate' and cf.end_day > settlement_day])
    
def ex_cpn_day(bnd, settlement_day):
    ''' Returns the ex coupon date for a given bond and settlement date
    '''
    myBnd = ael.Instrument[bnd]
    next_coup = ncd(bnd, settlement_day)
    
    if myBnd.ex_coup_method == 'Calendar Days':
        return next_coup.add_period('-' + ael.Instrument[bnd].ex_coup_period)
        
    elif myBnd.ex_coup_method == 'Business Days':
        return next_coup.add_period('-' + ael.Instrument[bnd].ex_coup_period).adjust_to_banking_day(ael.Instrument['ZAR'])
        
    elif myBnd.ex_coup_method == 'AdditionalInfo':
        # Find the relevent date by looking at the difference between the months of the ncd and ex coupon days mod 12.  The reason for 
        # using mod 12 arithmetic is that we want the difference between December (12th month) and January (1st month) to be 1
        ex_day_list = [ael.date_from_string(myBnd.add_info('ExCoup1')).to_ymd(), ael.date_from_string(myBnd.add_info('ExCoup2')).to_ymd()]
        ncd_trip = next_coup.to_ymd()
        ncd_month = ncd_trip[1]
        
        if (ncd_month - ex_day_list[0][1]) % 12 < (ncd_month - ex_day_list[1][1]) % 12:
            ex_day = ex_day_list[0]
        else:
            ex_day = ex_day_list[1]
            
        # Adjust the year of ex_day by checking for the case where next_coup is at the beginning of a year and the ex_day is 
        # at the end of the previous year.
        if ex_day[1] <= ncd_month:
            return triple_to_date([ncd_trip[0], ex_day[1], ex_day[2]])
        else:
            return triple_to_date([ncd_trip[0]-1, ex_day[1], ex_day[2]])
    
def Cit_plus_inc(bnd, value_day, inc):
    ''' If inc = 0 then return the next coupon date <= value_day
        If inc != 0 then return the coupon date inc number of 
        periods before or after the next coupon date
    '''
    date_list = [cf.end_day for cf in ael.Instrument[bnd].cash_flows() if cf.type == 'Fixed Rate']
    date_list.sort()
    for i, d in enumerate(date_list):
        if d >= value_day:
            if i+inc > len(date_list)-1:
                return max(date_list)
            elif i+inc < 0:
                return min(date_list)
            else:
                return date_list[i+inc] 

def getKFactor(i, t):
    ''' Return a KFactor for a specified instrument and date.  The KFactors are stored as a time series called KFactor which is linked to
        the instrument.
    '''
    for ts in i.time_series():
        if ts.day == t and ts.ts_specnbr.field_name == 'KFactor':
            return ts.value/KFactor_Multiplier
            
def bond_index_calculations(ins, bond_weights, t, s, user_input='No', input_file='F:\\Albi Yields.csv'):
    ''' Return a dictionary of dictionaries containing the values of all intermediate calculations as 
        specified by the BEASSA Total Return Indices 2000 documentation 
    '''
    
    prev_weight_change = rebasing_day('Previous', t)
    todays_kfactor = getKFactor(ins, t)

    if user_input == 'Yes':
        user_Yit = {}
        user_Pit = {}
        try:
            reader = csv.reader(open(input_file, "rb"))
            for row in reader:
                user_Yit[row[0]] = float(row[1])
                user_Pit[row[0]] = float(row[2])
        except:
            print 'Error: Problem reading user input at the following path: ' + input_file
            raise
            
    # Get the previous set of weights 
    prev_index = ael.Instrument[ins.add_info('Previous_Index')]
    previous_weights = {}
    for c in prev_index.combination_links():
        previous_weights[c.member_insaddr.insid] = int(c.weight)
    
    # Used for finding the last day of a bonds ex-coupon period
    t_prev = t.add_banking_day(ael.Instrument['ZAR'], -1)
    s_prev = t_prev.add_banking_day(ael.Instrument['ZAR'], 3)
    
    bond_calcs = {'Bt':0.0, 'Ct':0.0, 'Cmit':{}, 'Cit':{}, 'Cpit':{}, 'Yit':{}, 'Pit':{}, 'gi':{}, 'Hit':{}, 'Dit':{}, 'Nit':{}, 'Nitp':{}, 'Xit':{}, 'Vit':{}, 'Rit':{}}
    for b in bond_weights.keys():
        if user_input == 'Yes':
            try:
                bond_calcs['Yit'][b] = user_Yit[b]
                bond_calcs['Pit'][b] = user_Pit[b]
            except KeyError:
                print 'Error: Could not find ' + b + ' in user input file.'
                raise
        else:
            #bond_calcs['Yit'][b] = ael.Instrument[b].spot_price()
            #bond_calcs['Pit'][b] = ael.Instrument[b].dirty_from_yield()
            instr = acm.FInstrument[b]
            bond_calcs['Yit'][b] = instr.Calculation().TheoreticalPrice(calc_space_collection).Value().Number()
            credit_basket_ref = instr.CreditReference() if instr.IsCreditBasket() else None
            
            leg_infos = []
            static_leg_informations = []

            for leg in instr.Legs():
                leg_infos.append(leg.LegInformation(acm_datetime('Today')))
                static_leg_informations.append(leg.StaticLegInformation(instr, acm_datetime('Today'), credit_basket_ref))
                
            bond_calcs['Pit'][b] = instr.QuoteToQuote(
                acm.DenominatedValue(instr.Calculation().TheoreticalPrice(calc_space_collection).Value().Number(), 'Price', acm_datetime('today')),
                acm_datetime('today'),
                leg_infos,
                static_leg_informations,
                'Yield',
                'Pct of Nominal',
            ).Value().Number()
            
        bond_calcs['Cmit'][b] = Cit_plus_inc(b, t, -1)
        bond_calcs['Cit'][b] = Cit_plus_inc(b, t, 0)
        bond_calcs['Cpit'][b] = Cit_plus_inc(b, t, 1)
        bond_calcs['gi'][b] = ael.Instrument[b].legs()[0].fixed_rate
        
        if bond_calcs['Cit'][b] >= s:
            bond_calcs['Hit'][b] = float(t.days_between(s)) / bond_calcs['Cmit'][b].days_between(bond_calcs['Cit'][b])
        else:
            bond_calcs['Hit'][b] = float(s.days_between(bond_calcs['Cit'][b])) / bond_calcs['Cpit'][b].days_between(bond_calcs['Cit'][b]) \
                    + float(bond_calcs['Cit'][b].days_between(t)) / bond_calcs['Cit'][b].days_between(bond_calcs['Cmit'][b])
            
        bond_calcs['Dit'][b] = (1/(1 + bond_calcs['Yit'][b]/float(200)))**bond_calcs['Hit'][b]
        bond_calcs['Nit'][b] = todays_kfactor*bond_weights[b]
        
        # Check to see if the bond is in its ex-period
        ex_coupon_day = ex_cpn_day(b, t)
        if (ex_coupon_day <= s <= bond_calcs['Cit'][b]) or (s_prev < bond_calcs['Cit'][b] and s >= bond_calcs['Cit'][b]):
            # Get the first day of the ex coupon period
            first_day = ex_coupon_day.add_banking_day(ael.Instrument['ZAR'], -3)
            
            # Check to see if the indexes weights were rebased in the bonds ex-period
            if first_day <= prev_weight_change <= bond_calcs['Cit'][b]:
                # Check to see if the bond was in the previous set of instruments making up the index
                if b in previous_weights.keys():
                    bond_calcs['Nitp'][b] = getKFactor(ins, first_day)*previous_weights[b]
                else:
                    bond_calcs['Nitp'][b] = 0.0
            else:
                bond_calcs['Nitp'][b] = getKFactor(ins, first_day)*bond_weights[b]
        else:
            bond_calcs['Nitp'][b] = 0.0
            
        bond_calcs['Xit'][b] = bond_calcs['gi'][b]*bond_calcs['Nitp'][b]/200
        
        bond_calcs['Vit'][b] = bond_calcs['Xit'][b]*bond_calcs['Dit'][b]*(1/(1 + bond_calcs['Yit'][b]/float(200))) \
                **(max(float(s.days_between(bond_calcs['Cit'][b])), 0.0) / bond_calcs['Cmit'][b].days_between(bond_calcs['Cit'][b]))
        
        if s_prev < bond_calcs['Cit'][b] and s >= bond_calcs['Cit'][b]:
            bond_calcs['Rit'][b] = bond_calcs['Vit'][b]
        else:
            bond_calcs['Rit'][b] = 0.0
        
        bond_calcs['Bt'] += bond_calcs['Nit'][b]*bond_calcs['Pit'][b]*bond_calcs['Dit'][b]/100
        bond_calcs['Ct'] += bond_calcs['Vit'][b]
        
    return bond_calcs
    
def bond_index_calculations_theor(ins, bond_weights, t, s, theoretical_prices, user_input='No', input_file='F:\\Albi Yields.csv'):
    ''' Return a dictionary of dictionaries containing the values of all intermediate calculations as 
        specified by the BEASSA Total Return Indices 2000 documentation 
    '''
    
    prev_weight_change = rebasing_day('Previous', t)
    todays_kfactor = getKFactor(ins, t)

    if user_input == 'Yes':
        user_Yit = {}
        user_Pit = {}
        try:
            reader = csv.reader(open(input_file, "rb"))
            for row in reader:
                user_Yit[row[0]] = float(row[1])
                user_Pit[row[0]] = float(row[2])
        except:
            print 'Error: Problem reading user input at the following path: ' + input_file
            raise
            
    # Get the previous set of weights 
    prev_index = ael.Instrument[ins.add_info('Previous_Index')]
    previous_weights = {}
    for c in prev_index.combination_links():
        previous_weights[c.member_insaddr.insid] = int(c.weight)
    
    # Used for finding the last day of a bonds ex-coupon period
    t_prev = t.add_banking_day(ael.Instrument['ZAR'], -1)
    s_prev = t_prev.add_banking_day(ael.Instrument['ZAR'], 3)
    
    bond_calcs = {'Bt':0.0, 'Ct':0.0, 'Cmit':{}, 'Cit':{}, 'Cpit':{}, 'Yit':{}, 'Pit':{}, 'gi':{}, 'Hit':{}, 'Dit':{}, 'Nit':{}, 'Nitp':{}, 'Xit':{}, 'Vit':{}, 'Rit':{}}
    for b in bond_weights.keys():
        if user_input == 'Yes':
            try:
                bond_calcs['Yit'][b] = user_Yit[b]
                bond_calcs['Pit'][b] = user_Pit[b]
            except KeyError:
                print 'Error: Could not find ' + b + ' in user input file.'
                raise
        else:
            #bond_calcs['Yit'][b] = ael.Instrument[b].spot_price()
            #bond_calcs['Pit'][b] = ael.Instrument[b].dirty_from_yield()
            instr = acm.FInstrument[b]
            bond_calcs['Yit'][b] = theoretical_prices[b].Number()
            credit_basket_ref = instr.CreditReference() if instr.IsCreditBasket() else None
            
            leg_infos = []
            static_leg_informations = []

            for leg in instr.Legs():
                leg_infos.append(leg.LegInformation(acm_datetime('Today')))
                static_leg_informations.append(leg.StaticLegInformation(instr, acm_datetime('Today'), credit_basket_ref))
                
            bond_calcs['Pit'][b] = instr.QuoteToQuote(
                acm.DenominatedValue(theoretical_prices[b].Number(), 'Price', acm_datetime('today')),
                acm_datetime('today'),
                leg_infos,
                static_leg_informations,
                'Yield',
                'Pct of Nominal'
            ).Value().Number()
            
        bond_calcs['Cmit'][b] = Cit_plus_inc(b, t, -1)
        bond_calcs['Cit'][b] = Cit_plus_inc(b, t, 0)
        bond_calcs['Cpit'][b] = Cit_plus_inc(b, t, 1)
        bond_calcs['gi'][b] = ael.Instrument[b].legs()[0].fixed_rate
        
        if bond_calcs['Cit'][b] >= s:
            bond_calcs['Hit'][b] = float(t.days_between(s)) / bond_calcs['Cmit'][b].days_between(bond_calcs['Cit'][b])
        else:
            bond_calcs['Hit'][b] = float(s.days_between(bond_calcs['Cit'][b])) / bond_calcs['Cpit'][b].days_between(bond_calcs['Cit'][b]) \
                    + float(bond_calcs['Cit'][b].days_between(t)) / bond_calcs['Cit'][b].days_between(bond_calcs['Cmit'][b])
            
        bond_calcs['Dit'][b] = (1/(1 + bond_calcs['Yit'][b]/float(200)))**bond_calcs['Hit'][b]
        bond_calcs['Nit'][b] = todays_kfactor*bond_weights[b]
        
        # Check to see if the bond is in its ex-period
        ex_coupon_day = ex_cpn_day(b, t)
        if (ex_coupon_day <= s <= bond_calcs['Cit'][b]) or (s_prev < bond_calcs['Cit'][b] and s >= bond_calcs['Cit'][b]):
            # Get the first day of the ex coupon period
            first_day = ex_coupon_day.add_banking_day(ael.Instrument['ZAR'], -3)
            
            # Check to see if the indexes weights were rebased in the bonds ex-period
            if first_day <= prev_weight_change <= bond_calcs['Cit'][b]:
            
                # Check to see if the bond was in the previous set of instruments making up the index
                if b in previous_weights.keys():
                    bond_calcs['Nitp'][b] = getKFactor(ins, first_day)*previous_weights[b]
                else:
                    bond_calcs['Nitp'][b] = 0.0
            else:
                bond_calcs['Nitp'][b] = getKFactor(ins, first_day)*bond_weights[b]
        else:
            bond_calcs['Nitp'][b] = 0.0
            
        bond_calcs['Xit'][b] = bond_calcs['gi'][b]*bond_calcs['Nitp'][b]/200
        
        bond_calcs['Vit'][b] = bond_calcs['Xit'][b]*bond_calcs['Dit'][b]*(1/(1 + bond_calcs['Yit'][b]/float(200))) \
                **(max(float(s.days_between(bond_calcs['Cit'][b])), 0.0) / bond_calcs['Cmit'][b].days_between(bond_calcs['Cit'][b]))
        
        if s_prev < bond_calcs['Cit'][b] and s >= bond_calcs['Cit'][b]:
            bond_calcs['Rit'][b] = bond_calcs['Vit'][b]
        else:
            bond_calcs['Rit'][b] = 0.0
        
        bond_calcs['Bt'] += bond_calcs['Nit'][b]*bond_calcs['Pit'][b]*bond_calcs['Dit'][b]/100
        bond_calcs['Ct'] += bond_calcs['Vit'][b]
        
    return bond_calcs
    

def index_value(bond_index, theoretical_prices, instruments):
    ''' Calculate the value of a bond_index
    '''
  
    # Get the weights 
    
    bond_index = to_ael(bond_index)
    weights = {}
    for c in bond_index.combination_links():
        weights[c.member_insaddr.insid] = int(c.weight)
        
    theoretical_values = {}
    for instrument, price in zip(instruments, theoretical_prices):
        theoretical_values[to_ael(instrument).insid] = price
    
    # value day and settlement day
    vd = ael.date_today()
    sd = vd.adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding').add_banking_day(ael.Instrument['ZAR'], 3)
    
    # Get all the intermediate calculations needed for calculating the final value of the index
    index_calcs = bond_index_calculations_theor(bond_index, weights, vd, sd, theoretical_values)
    return round(index_calcs['Bt'] + index_calcs['Ct'], 3)

def calculate_kfactor(bond_index, user_input='No', input_file='F:\\Albi Yields.csv'):
    ''' Return tomorrows K-Factor for a given bond index
    '''
    K_numerator = K_denominator = 0.0
    
    # value day and settlement day
    vd = ael.date_today()
    sd = vd.adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding').add_banking_day(ael.Instrument['ZAR'], 3)
    
    # Get the weight change date for the bond index
    weight_change_date = rebasing_day('Next', vd)
    
    # Get the weights of the current instrument
    weights = {}
    for c in bond_index.combination_links():
        weights[c.member_insaddr.insid] = int(c.weight)
    
    # Check to see if the next set of weights need to be used
    if vd == weight_change_date:
        next_index = ael.Instrument[bond_index.add_info('Next_Index')]
        new_weights = {}
        for c in next_index.combination_links():
            new_weights[c.member_insaddr.insid] = int(c.weight)
    else:
        new_weights = weights.copy()
    
    # Calculations for the current set of weights
    index_calcs = bond_index_calculations(bond_index, weights, vd, sd, user_input, input_file)
    
    # Calculations for the next set of weights
    next_index_calcs = bond_index_calculations(bond_index, new_weights, vd, sd, user_input, input_file)
    
    # Calculate K_numerator using current weights and underlying instruments
    for b in weights.keys():
        K_numerator += index_calcs['Nit'][b]*index_calcs['Pit'][b]*index_calcs['Dit'][b]/100 + index_calcs['Rit'][b]
        
    # Calculate K_denominator using the new weights and underlying instruments
    for b in new_weights.keys():
        K_denominator += new_weights[b]*next_index_calcs['Pit'][b]*next_index_calcs['Dit'][b]/100
        
    return K_numerator/K_denominator

def change_weights(ins, copy_ins):
    ''' Replace the underlying instruments and weights in ins with the underlying instruments and weights in copy_ins
    '''
    
    new_weights = {}
    for c in copy_ins.combination_links():
        new_weights[c.member_insaddr.insid] = int(c.weight)
    
    try:
        ins_clone = ins.clone()
        for c in ins_clone.combination_links():
            c.delete()
        
        for b in new_weights.keys():
            new_cl = ael.CombinationLink.new(ins_clone)
            new_cl.member_insaddr = ael.Instrument[b]
            new_cl.weight = new_weights[b]
        ins_clone.commit()
    except:
        ael.log("Error: Could not copy weights from " + copy_ins.insid + " to " + ins.insid)
        
def generate_kfactor(bond_index, offset=1):
    ''' Rebases the bond index by calculating tomorrows K-Factor and changing the weights if today
        is the next weight change date.
        
        offset is either 0 or 1 and handles the case in the expiry months where todays k-factor gets 
        overwritten at 12h00 and is replaced by a new k-factor for the second half of the day.
    '''
    
    New_K = calculate_kfactor(bond_index)
    New_K_date = ael.date_today().add_days(offset)
    
    for ts in bond_index.time_series():
        if ts.day == New_K_date and ts.ts_specnbr.field_name == 'KFactor':
            new_ts = ts.clone()
            break
    else:
        new_ts = ael.TimeSeries.new()
        
    new_ts.value = round(New_K*KFactor_Multiplier, 0)
    new_ts.day = New_K_date
    new_ts.ts_specnbr = ael.TimeSeriesSpec['KFactor'].specnbr
    new_ts.recaddr = bond_index.insaddr
    try:
        new_ts.commit()
    except:
        ael.log("Error: Could not commit new K-Factor for " + bond_index.insid)

def rebase_instruments(bond_index):
    ''' Rebases a bond index.  This script needs to get run twice a day at 12h00 and 16h30.  On the rebasing day of an
        expiry month the instrument will get rebased at 12h00 and at 21h00, all other days rebasing will only take 
        place at 21h00
    '''

    # Rebasing time is 12h00 for expiry months
    expiry_months = (2, 5, 8, 11)
    expiry_time = time.strptime('13:00:00', '%H:%M:%S')
    expiry = (expiry_time.tm_hour, expiry_time.tm_min)
    
    time_now = time.localtime()
    todays_month = time_now.tm_mon
    now = (time_now.tm_hour, time_now.tm_min)
    
    if ael.date_today() == rebasing_day('Next'):     
        if now < expiry and todays_month in expiry_months:
            generate_kfactor(bond_index, 0)
            change_weights(ael.Instrument[bond_index.add_info('Previous_Index')], bond_index)
            change_weights(bond_index, ael.Instrument[bond_index.add_info('Next_Index')])
        elif now > expiry and todays_month in expiry_months:
            generate_kfactor(bond_index, 1)
        elif now > expiry and todays_month not in expiry_months:
            generate_kfactor(bond_index, 1)
            change_weights(ael.Instrument[bond_index.add_info('Previous_Index')], bond_index)
            change_weights(bond_index, ael.Instrument[bond_index.add_info('Next_Index')])
    else:
        if now > expiry:
            generate_kfactor(bond_index, 1)

def update_bond_index_price(ins):
    ''' Over-writes the spot price of an ETF with the theor price of the underlying bond index. 
    '''
    
    bond_index = ins.und_insaddr
    ins_theor = index_value(bond_index)
    
    ins_spot = ael.Price.read(('insaddr = %d and curr = %d and ptynbr = %d') \
    % (ins.insaddr, ins.curr.insaddr, ael.Party['SPOT'].ptynbr))
    
    if ins_spot:
        p_clone = ins_spot.clone()
    else:
        p_clone = ael.Price.new()
    
    try:
        p_clone.insaddr = ins.insaddr
        p_clone.curr = ins.curr
        p_clone.ptynbr = ael.Party['SPOT'].ptynbr
        p_clone.day = ael.date_today()
        p_clone.bid = ins_theor
        p_clone.ask = ins_theor
        p_clone.last = ins_theor
        p_clone.settle = ins_theor
        p_clone.commit()
    except:
        ael.log('Error: Could not copy a new spot price for ' + ins)

def calculation_report(bond_index, user_input='No', input_file='F:\\Albi Yields.csv'):
    ''' Print out all the intermediate results used in calculating the value of the given bond index
    '''
   
    # Get the weights 
    weights = {}
    for c in bond_index.combination_links():
        weights[c.member_insaddr.insid] = int(c.weight)
    
    # value day and settlement day
    vd = ael.date_today()
    sd = vd.adjust_to_banking_day(ael.Instrument['ZAR'], 'Preceding').add_banking_day(ael.Instrument['ZAR'], 3)
    
    # Get all the intermediate calculations needed for calculating the value of the index
    index_calcs = bond_index_calculations(bond_index, weights, vd, sd, user_input, input_file)
    
    # Generate an ouput table
    output = [['Bond', 'Weight', 'ExCouponDay', 'C_minus_it', 'C_it', 'C_plus_it', 'Y_it', 'H_it', 'D_it', 'N_it', 'N_itp', 'P_it', 'g_i', 'X_it', 'V_it', 'R_it']]
    for b in weights.keys():
        row = [b, weights[b], ex_cpn_day(b, vd), index_calcs['Cmit'][b], index_calcs['Cit'][b], index_calcs['Cpit'][b], \
            index_calcs['Yit'][b], index_calcs['Hit'][b], index_calcs['Dit'][b], index_calcs['Nit'][b], index_calcs['Nitp'][b], \
            index_calcs['Pit'][b], index_calcs['gi'][b], index_calcs['Xit'][b], index_calcs['Vit'][b], index_calcs['Rit'][b]]
        output.append(row)
        
    # Find the maximum width of the columns in the output table, so that the table can be printed neatly
    # zip(*output) transposes output
    column_widths = []
    for row in zip(*output):
        column_widths.append(max([len(str(v)) for v in row]))
    
    # Print bond index meta-data
    print ''
    print 'Instrument:', bond_index.insid
    print 'Value Day (t):', vd
    print 'Settlement Day (s):', sd
    print 'Previous weight change date:', rebasing_day('Previous', vd)
    print 'Next weight change date:', rebasing_day('Next', vd)
    print 'B_t:', index_calcs['Bt']
    print 'C_t:', index_calcs['Ct']
    print 'V_t:', round(index_calcs['Bt'] + index_calcs['Ct'], 3)
    print 'Todays K-factor:', getKFactor(bond_index, vd)
    print 'Tomorrows K-factor:', calculate_kfactor(bond_index, user_input, input_file)
    print ''
    
    # Print the output table with columns formatted to a uniform width
    for row in output:
        print ' '.join([str(val).ljust(column_widths[i]) for (i, val) in enumerate(row)])
    
def test():
    tic = time.time()
    test_bond = ael.Instrument['ZAR/ALBI_TEST']
    
    print 'Executing index_value()...'
    print 'Value = ', index_value(test_bond)
    print ''
    
    print 'Executing calculation_report()...'
    calculation_report(test_bond, 'No', input_file)
    
    print ''
    print 'Execution time:', time.time() - tic
    print ''

'''
import profile, __main__
__main__.test = test
profile.run('test()')
'''

