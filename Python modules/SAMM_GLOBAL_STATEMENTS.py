"""
History
=======

2017-05-24 Vojtech Sidorin  FAU-938 Update dependency on elementtree.
"""

import ael, acm

import sys, string

from xml.etree.ElementTree import Element, SubElement, XML, tostring, ElementTree

def Connect(ADSIPandPORT, UserName, Password):
    #print ael.is_connected()
    #print 'Connecting to: ' + ADSIPandPORT + ' UID=' + UserName + ' PWD=' + Password
    #print ael.is_connected()
    acm.Connect( ADSIPandPORT, UserName, Password, "")
    print ael.is_connected()
#    ael.connect( ADSIPandPORT , UserName , Password)
    #print acm.IsConnected()
    return 1

def Disconnect():
    acm.Disconnect()
    return 1

def caRedemption(ins):
    balance=0.0
    legs = ins.Legs()
    if not legs:
        return balance
    leg=legs.At(0) # only 1 leg for CallAccount
    if not leg:
        return balance
    cashflows=leg.CashFlows()
    if not cashflows:
        return balance
    trades = ins.Trades()
    if not trades:
        return balance
    sign = trades.At(0).Quantity()
        
    cf1=None
    
    for cf in cashflows:
        if cf.CashFlowType() == 'Redemption Amount':
            cf1 = cf
            break

    if cf1:
        balance += cf1.ProjectedCashFlow(0, cf1.EndDate())
    
    return balance * (1) * sign #opposite sign to redemption cashflow

def get_statement_XML(ins,startd, endd,type,page, recs,*rest):
    t = ins.trades()[0]
    status = 'SUCCESS'
    outfile = ''
    error = 0
     
    
    #=======Header========#
    DOC = Element("RESPONSE")
    STAT = SubElement(DOC, "STATEMENT")
    
# ========================================================================================
#       CUSTOMER CONTACT DETAILS 
# ======================================================================================== 
    
    p = t.counterparty_ptynbr
    CNAM = p.fullname
    CACC = str(ins.insid[0:18])
    CNAM = CNAM.replace('&', '&amp;') + ' (' + t.add_info('Account_Name').replace('&', '&amp;') + ')'
    ACC = SubElement(STAT, "ACCOUNT", No = CACC, Name = CNAM)
        
   
# ========================================================================================
#                       SETUP 
# ========================================================================================
    legs = t.insaddr.legs()
    leg = legs[0]
    cashflows = legs[0].cash_flows()
    ins = t.insaddr
    daysx  = []
    daysy =[]
    dict_movement = {}
    movement = []
    OpeningBalance = 0.00
    total_interest = 0.00
    total_debits = 0.00
    total_credits = 0.00
    opening_int = 0.00
    today = ael.date_today()
    intbal =0
    ss = 'm'
    mx = 0
    dict_fixed= {}
    i1 = 0
    reinv = 0
    #All Movement and Interest Dates
    for cf in cashflows:
        if leg.reinvest == 0:
            if cf.type ==  'Interest Reinvestment' and cf.pay_day >= startd: 
                reinv = 1
                
    for cf in cashflows:
        
        if cf.type in ('Fixed Amount', 'Interest Reinvestment', 'Call Fixed Rate Adjustable', 'Fixed Rate Adjustable'): 
            if cf.pay_day not in daysx:
                daysx.append(cf.pay_day)
            if cf.type == 'Fixed Amount' and cf.start_day:
                if cf.start_day not in daysx:
                    daysx.append(cf.start_day)
            
    daysx.sort()
    
       
    #MOVEMENTS
    for cfday in daysx:
        for cf in cashflows:
            if  cf.pay_day  == cfday :
                if cf.type in ('Fixed Amount', 'Interest Reinvestment') and abs(cf.projected_cf()*t.quantity) > 0.005 :
                    if cf.type == 'Fixed Amount':
                            if cf.start_day:
                                cft = cf.start_day
                            else:
                                cft = cfday
                    else:
                        cft = cfday
                    if cf.type == 'Fixed Amount':
                        ss = 'm'
                    else:
                        ss = 'r'                
                
                    if (cf.pay_day >= startd and cf.pay_day <= endd) or (cf.start_day >= startd and cf.pay_day >= startd):
                        
                        if cf.type == 'Fixed Amount':
                            if cf.start_day:
                                
                                if cf.start_day >= startd and cf.start_day <= endd:
                                    
                                    s1 = []
                                    s1.append(cf.start_day) #start day is the effective day
                                    s1.append(ael.date_from_time(cf.creat_time))
                                    s1.append(str(cf.cfwnbr))
                                    val = round(cf.projected_cf() * t.quantity, 2)
                                    if val > 0:
                                        s1.append('Backdated Transfer In')
                                    else:
                                        s1.append('Backdated Transfer Out')
                                    s1.append(val)
                                    s1.append(1)
                                    movement.append(s1)
                                    
                                    if cf.projected_cf()*t.quantity< 0:
                                        total_debits = total_debits + val
                                    else:
                                        total_credits = total_credits + val
                                    #print 'here', cft
                                    
                            else:
                                s1 =[]
                                s1.append(str(cf.pay_day))
                                s1.append(ael.date_from_time(cf.creat_time))
                                s1.append(str(cf.cfwnbr))
                                val = round(cf.projected_cf() * t.quantity, 2)
                                if val > 0:
                                    s1.append('Transfer In')
                                else:
                                    s1.append('Transfer Out')
                                s1.append(val)
                                s1.append(1)
                                movement.append(s1)
                                if cf.projected_cf()*t.quantity< 0:
                                    total_debits = total_debits + val
                                else:
                                    total_credits = total_credits + val

                        else:
                            s1 =[]
                            s1.append(str(cf.pay_day))
                            s1.append(ael.date_from_time(cf.creat_time))
                            s1.append(str(cf.cfwnbr))
                            s1.append('Interest Reinvestment')
                            s1.append(round(cf.projected_cf() * t.quantity, 2))
                            s1.append(1)
                            movement.append(s1)
                            #print cf.pp()
                            if cf.projected_cf()*t.quantity< 0:
                                total_debits = total_debits + round(cf.projected_cf()*t.quantity, 2)
                            else:
                                total_credits = total_credits + round(cf.projected_cf()*t.quantity, 2)
                    
                    if str(cft) in dict_movement.keys():
                        dict_movement[str(cft)].append([ss, round(cf.projected_cf()*t.quantity, 2)])
                    else:
                        dict_movement[str(cft)] = [[ss, round(cf.projected_cf()*t.quantity, 2)]]
            

                if cf.type == 'Call Fixed Rate Adjustable' and (cf.pay_day >= startd and cf.pay_day <= endd): #and leg.reinvest == 0:# and reinv == 0):
                    if cf.pay_day != ael.date_today():
                        
                        int_set = round(cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* t.quantity, 2)
                        val = 0
                        if reinv ==1 or leg.reinvest == 1:
                            if cf.end_day != cf.pay_day:
                                val = get_cf(ins, cf.pay_day) + get_cf(ins, cf.end_day)
                            else:
                                val = get_cf(ins, cf.pay_day)
                        
                        if cf.end_day <= startd and int_set!=0:
                            i1 = i1 + int_set
                        if int_set !=0 and val == 0:
                            s1 =[]
                            s1.append(str(cf.pay_day))
                            s1.append(ael.date_from_time(cf.creat_time))
                            s1.append(str(cf.cfwnbr))
                            s1.append('Interest Settlement')
                            s1.append(int_set* t.quantity)
                                                              
                            
                            s1.append(0)
                            movement.append(s1)
                            
                            if int_set < 0:
                                total_debits = total_debits + int_set
                            else:
                                total_credits = total_credits + int_set
                                
                            if str(cfday) in dict_movement.keys():
                                dict_movement[str(cfday)].append(['i', int_set])
                            else:
                                dict_movement[str(cfday)] = [['i', int_set]]
                                
                          
                    
                if cf.type == 'Call Fixed Rate Adjustable' and (leg.reinvest == 0): #and cf.pay_day > endd:
                    
                    if cf.end_day <= startd and cf.pay_day > endd:
                        
                        int_set = round(cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* t.quantity, 2)
                        mx =  mx + int_set
                            
                if cf.type == 'Fixed Rate Adjustable' and (cf.pay_day >= startd and cf.pay_day <= endd):# and (leg.reinvest == 0):
                    int_set = round(cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* t.quantity, 2)
                    val = 0
                    if reinv ==1 or leg.reinvest == 1:
                        if cf.end_day != cf.pay_day:
                            val = get_cf(ins, cf.pay_day) + get_cf(ins, cf.end_day)
                        else:
                            val = get_cf(ins, cf.pay_day)
                            
                    if cf.end_day <= startd and int_set!=0:
                            i1 = i1 + int_set
                            
                    if int_set !=0 and val == 0:
                        s1 =[]
                        s1.append(str(cf.pay_day))
                        s1.append(ael.date_from_time(cf.creat_time))
                        s1.append(str(cf.cfwnbr))
                        s1.append('Backdated Interest Settlement')
                        s1.append(int_set* t.quantity)
                                                          
                        
                        s1.append(0)
                        movement.append(s1)
                        
                        if int_set < 0:
                            total_debits = total_debits + int_set
                        else:
                            total_credits = total_credits + int_set
                            
                        if str(cfday) in dict_movement.keys():
                            dict_movement[str(cfday)].append(['i', int_set])
                        else:
                            dict_movement[str(cfday)] = [['i', int_set]]
                                
                                
                if cf.type == 'Fixed Rate Adjustable' and (leg.reinvest == 0) and (cf.end_day <= startd and cf.pay_day> endd):
                    int_set = round(cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* t.quantity, 2)
                    if str(cf.end_day) in dict_fixed.keys():
                            dict_fixed[str(cf.end_day)].append(['i', int_set])
                    else:
                        dict_fixed[str(cf.end_day)] = [['i', int_set]]
                        

                      
    movement.sort(lambda x, y: cmp(ael.date(x[0]), ael.date(y[0])))
    
    #RESETS
    dict_reset = {}   
    for c in cashflows:
        if c.type == 'Call Fixed Rate Adjustable':
            for r in c.resets():
                d1 = r.start_day
                while d1 < r.end_day:
                    
                    if str(d1) in dict_reset.keys():
                        dict_reset[str(d1)] = dict_reset[str(d1)] + r.value
                    else:   
                        dict_reset[str(d1)] =  r.value
                    d1 = d1.add_days(1)
    
    interest = []
    total = 0
    reset_rate = 0
    sd = startd
    if len(daysx) > 0:
        sd1 = daysx[0]
    else:
        sd1 = sd
    ed = endd
    mov1 = 0
    mov = 0
    bal =0
    total_interest = 0.00
    ClosingBalance = 0.00
    OpeningBalance = 0
    m1 = 0
   
    while sd1 < startd:
        if str(sd1) in  dict_movement.keys():
            for mov in  dict_movement[str(sd1)]:
                if mov[0] in ('m', 'r'):
                    m1 = mov[1] + m1
                
        sd1 = sd1.add_days(1)
    OpeningBalance = m1 
    bal = m1 
    set =0
    due = 0
    acc =0
    val = 0
    
    for days in  dict_movement.keys():
        for mov in dict_movement[days]:
            if mov[0] in ('m', 'r'):
                ClosingBalance = mov[1] + ClosingBalance
    
    for days in  dict_fixed.keys():
       if ael.date(days).add_days(-1) <= startd:
            for mov in  dict_fixed[days]:
                val = mov[1] + val
            
    
    acc = leg.interest_accrued(leg.start_day, startd, 'ZAR')*t.quantity *(-1)
    
    total = -1*(i1 + val + mx) + acc
    
#===========================================================================================
#                                       DAILY INTEREST
#===========================================================================================

    if type == 'I':
        while sd <= ed:
            intbal = 0
            day1 = sd
            day2 = sd.add_days(1)
            sd = day2
            l2 =[]
            intbal = 0        
            
            if str(day1) in  dict_movement.keys():
                mov1 = 0
                for mov in  dict_movement[str(day1)]:
                    
                    if mov[0] in ('m', 'r'):
                        mov1 = mov[1] + mov1
                    if mov[0] =='i':
                        intbal = intbal + mov[1]
                    if mov[0] =='r': #and day1 != startd:
                        intbal = intbal + (mov[1])*(-1)
                        #print day1, 'int bal r' ,  intbal, mov[1]
                    
                       
            else:
                mov1 =   0
                        
            int_set = legs[0].interest_settled(day1, day2, 'ZAR')
            int_acc = legs[0].interest_accrued(day1, day2, 'ZAR')
            int_due = legs[0].interest_due(day1, day2, 'ZAR')
                   
            tot = (int_set + int_acc + int_due)*t.quantity *-1
            total_interest = tot + total_interest
            bal = bal + mov1
            total = total + tot + intbal
            intbal = 0
            if tot !=0 and total !=0:
                l2.append(day1.to_string('%Y/%m/%d'))
                l2.append(tot)
                try:
                    reset_rate = dict_reset[str(day1)]
                except:
                    
                    pass
                l2.append(reset_rate)
                
                l2.append(total)
                l2.append(bal)
                
                interest.append(l2)
                acc =0
    else:
        total_interest = total_accrued(leg, startd, endd, t.quantity)#, round(total_interest,2)
    
    
    
# ========================================================================================
#       HEADER 2
# ======================================================================================== 
 
    if type == 'S':
        trec = len(movement)
    if type == 'I':
        trec = len(interest)
       
    HEADER = SubElement(ACC, "HEADER")
    SubElement(HEADER, "SDATE").text = str(startd)
    SubElement(HEADER, "EDATE").text = str(endd)
    SubElement(HEADER, "PNUM").text = str(page)
    SubElement(HEADER, "PSIZE").text = str(recs)
    SubElement(HEADER, "TREC").text = str(trec)
       
    rstart = page*recs + 1
    if (type == 'I' and rstart > len(interest)) or (type == 'S' and rstart > len(movement)):
        error = 1
    rend = rstart + recs -1
    #print 'page',page, 'rec', recs, 'start', rstart, 'rend', rend
#=========================================================================================        
#                       XML
#=========================================================================================    


    # SUMMARY
    # =========
    
    
    OB = str(round(OpeningBalance, 2))
    TC = str(round(total_credits, 2))
    TD = str(round(total_debits, 2))
    TI = str(round(total_interest, 2))
    CB = str(round(ClosingBalance, 2))
    
    ACCSUM = SubElement(ACC, "ACCSUM")
    SubElement(ACCSUM, "OBAL").text = OB
    SubElement(ACCSUM, "TCRED").text = TC
    SubElement(ACCSUM, "TDEB").text = TD
    SubElement(ACCSUM, "TINT").text = TI
    SubElement(ACCSUM, "CBAL").text = CB
    
    sum1 = OpeningBalance

    # MOVEMENTS
    # =========
    pcount = 1
    if type == 'S': 
        YOURTRANS = SubElement(ACC, "YOURTRANS")
            
        for x in movement:
            output=''
            if x[5] == 1:
                sum1 = sum1 + x[4]
            if pcount >=rstart and pcount <= rend:           
                TA = str(round(x[4], 2))
                S = str(round(sum1, 2))
                TRANS = SubElement(YOURTRANS, "TRANS")
                SubElement(TRANS, "VDAT").text = ael.date(x[0]).to_string('%Y/%m/%d')
                SubElement(TRANS, "PDAT").text = ael.date(x[1]).to_string('%Y/%m/%d')
                SubElement(TRANS, "DLNO").text = str(x[2])
                SubElement(TRANS, "CDES").text = str(x[3])
                SubElement(TRANS, "CREF").text = str(x[2])
                SubElement(TRANS, "TAMT").text = TA
                SubElement(TRANS, "TABAL").text = S
            pcount += 1
                    
    # INTEREST
    # ========
    if type == 'I': 
        INTEREST = SubElement(ACC, "INTEREST")
        
        rcount = 1
        
        for x in interest:
            output=''
            if pcount >=rstart and pcount <= rend:     
                IA = str(round(x[1], 2))
                IB = str(round(x[3], 2))
                AB = str(round(x[4], 2))
                INTLIN = SubElement(INTEREST, "INTLIN")
                SubElement(INTLIN, "VDAT").text = str(x[0])
                SubElement(INTLIN, "IAMNT").text = IA
                SubElement(INTLIN, "IRATE").text = str(x[2])
                SubElement(INTLIN, "IBAL").text = IB
                SubElement(INTLIN, "ABAL").text = AB
            
            pcount += 1   
        

   
    #xmloutFile = "C:\\STAT_RESxxx.xml"
    
    #ElementTree(DOC).write(xmloutFile,encoding='utf-8')
    return tostring(DOC)




def get_cf(ins, d):
    val = 0
    for cf in ins.legs()[0].cash_flows():
        if cf.type == 'Interest Reinvestment' and cf.pay_day == d:
            val = val + cf.projected_cf()
    return val 

def total_accrued(leg, d1, d2, quantity):
    day1 = d1
    day2 = day1.add_days(1)
    tot = 0
    while day2 <= d2:
        
        int_set = leg.interest_settled(day1, day2, 'ZAR')
        int_acc = leg.interest_accrued(day1, day2, 'ZAR')
        int_due = leg.interest_due(day1, day2, 'ZAR')
               
        tot = tot + (int_set + int_acc + int_due)*quantity *-1
        day1 = day2
        day2 = day2.add_days(1)
    return tot

def get_balance(xelem):
    errort = ''
    RESPONSE = Element("RESPONSE")
    BALANCE = SubElement(RESPONSE, "BALANCE")
    flag = 0
    for element in xelem.getiterator("REQUEST"):
        for x in element.getiterator():
            if x.tag == "ACCOUNT":
                try:
                    i =  x.attrib[str('No')]
                    try:
                       ins = acm.FInstrument[i]
                       t = ins.Trades().At(0)
                       val = str(round(caRedemption(ins)*t.Quantity(), 2))
                       flag = 1
                    except:
                        name = i
                        flag = 0
                        errort = 'Invalid Account'
                        
                except:
                    flag = 0
                    name = 'INVALID'
                    errort = 'NO ACCOUNT NUMBER'
                    
                if flag == 1: 
                    name = ins.Name()
                    ACCOUNT = SubElement(BALANCE, "ACCOUNT", No = name)
                    SubElement(ACCOUNT, "BAL").text = val
                else:
                    
                    ACCOUNT = SubElement(BALANCE, "ACCOUNT", No = name)
                    SubElement(ACCOUNT, "ERROR").text  = errort
    #xmloutFile = "C:\\BAL_RESPXX.xml"
    
    #ElementTree(RESPONSE).write(xmloutFile,encoding='utf-8')    
    return tostring(RESPONSE)

def get_param(e, name):
    #print 'params'
    for element in e.getiterator("REQUEST"):
        for x in element.getiterator():
            if x.tag == name:
                return x.text
                
def get_attrib(e):
    for element in e.getiterator("REQUEST"):
        for x in element.getiterator():
            if x.tag == "ACCOUNT":
                return  x.attrib[str('No')]
    
def MAIN(string):
    elem = XML(string)
    
    if get_param(elem, "REQUEST_TYPE") == 'Balance':
        
        return get_balance(elem)
    elif get_param(elem, "REQUEST_TYPE") == 'Statement':
        
        try:
            
            ins = ael.Instrument[get_attrib(elem)]
            if ins == None:
                return ('<ERROR>') +  'INVALID ACCOUNT NUMBER' +  ('</ERROR>\n')
        except:
            return ('<ERROR>') +  'INVALID ACCOUNT NUMBER' +  ('</ERROR>\n')
       
        try:
            sd = ael.date(get_param(elem, "SDATE"))
            if sd > ael.date_today():
                return ('<ERROR>') +  'INVALID START DATE' +  ('</ERROR>\n')
            globalStart = ael.date('01/03/2008')
            if sd < globalStart:
                sd = globalStart
        except:
            return ('<ERROR>') +  'INVALID START DATE' +  ('</ERROR>\n')
            
        try:
            ed = ael.date(get_param(elem, "EDATE"))
            if ed > ael.date_today():
                ed = ael.date_today()
            if sd > ed:
                return ('<ERROR>') +  'INVALID DATE RANGE' +  ('</ERROR>\n')
        except:
            return ('<ERROR>') +  'INVALID END DATE' +  ('</ERROR>\n')
            
        t1 = get_param(elem, "STATEMENTDATA")
        t2 = get_param(elem, "INTERESTDATA")
	  
        if t1 == 'Y':
            t = 'S'
	  
        elif t2 == 'Y':
            t = 'I'	  
        else:
            return ('<ERROR>') +  'INVALID REQUEST' +  ('</ERROR>\n')
        
        try:
            page = int(get_param(elem, "PAGE"))
        except:
            return ('<ERROR>') +  'INVALID PAGE REQUEST' +  ('</ERROR>\n')
        
        try:
            rec = int(get_param(elem, "PAGESIZE"))
        except:
            return ('<ERROR>') +  'INVALID PAGING RECORD REQUEST' +  ('</ERROR>\n')
        
        return  get_statement_XML(ins, sd, ed, t, page, rec)
    else:
        return ('<ERROR>') +  'INVALID REQUEST TYPE' +  ('</ERROR>\n')
        
s1 = '<REQUEST><REQUEST_TYPE>Statement</REQUEST_TYPE><ACCOUNT No="030270-ZAR-2203-01"><SDATE>2008-04-01</SDATE><EDATE>2008-05-27</EDATE><STATEMENTDATA>N</STATEMENTDATA><INTERESTDATA>Y</INTERESTDATA><PAGE>0</PAGE><PAGESIZE>100</PAGESIZE></ACCOUNT></REQUEST>'

#http://s094apl101033:6540/scripts/aorta.dll/?IXMLAction=urn:S094APL101033.ambext2.dev&IXML=<Envelope><callAELFunction><AELFunctionCall><FunctionName>MAIN</FunctionName><Params><REQUEST><REQUEST_TYPE>Statement</REQUEST_TYPE><ACCOUNT%20No="012394823094-01"><SDATE>2008-02-01</SDATE><EDATE>2008-05-02</EDATE><STATEMENTDATA>Y</STATEMENTDATA><INTERESTDATA>N</INTERESTDATA><PAGE>0</PAGE><PAGESIZE>100</PAGESIZE></ACCOUNT></REQUEST></Params></AELFunctionCall></callAELFunction></Envelope>

print MAIN(s1)

