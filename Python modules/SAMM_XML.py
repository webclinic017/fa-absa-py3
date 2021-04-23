"""
History
=======

2017-05-24 Vojtech Sidorin  FAU-938 Update dependency on elementtree.
"""

import ael, os, FInstrumentCACashflow, acm
from xml.etree.ElementTree import Element, SubElement, ElementTree
from zak_funcs import formnum

def StatementXML(t,startd, endd,name ,*rest):
    status = 'SUCCESS'
        
    #=======Header========#
    
    DOC = Element("DOC")
    STAT = SubElement(DOC, "STATEMENT")
    

# ========================================================================================
#       CUSTOMER CONTACT DETAILS 
# ======================================================================================== 
    
    p = t.counterparty_ptynbr
    CNAM = p.fullname
    CACC = str(t.insaddr.insid[0:18])
    CNAM = CNAM.replace('&', '&amp;') + ' (' + t.add_info('Account_Name').replace('&', '&amp;') + ')'
    
    CUSTLIN2 = SubElement(STAT, "CUSTLIN2")
    SubElement(CUSTLIN2, "CNAM").text = CNAM
    SubElement(CUSTLIN2, "CACC").text = CACC

# ========================================================================================
#       HEADER 2
# ======================================================================================== 
 
    month = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    sy, sm, sd = startd.to_ymd()
    ey, em, ed = endd.to_ymd()
        
    H1 = t.add_info('Funding Instype')
    H2 = str(sd) + ' ' + month[sm] + ' ' + str(sy) + ' to ' + str(ed) + ' ' + month[em] + ' ' + str(ey)
    
    header2 = SubElement(STAT, "header2")
    SubElement(header2, "H1").text = H1
    SubElement(header2, "H2").text = H2
    SubElement(header2, "CDATE").text = str(endd)
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
                                    val = cf.projected_cf() * t.quantity
                                    if val > 0:
                                        s1.append('Backdated Transfer In')
                                    else:
                                        s1.append('Backdated Transfer Out')
                                    s1.append(val)
                                    s1.append(1)
                                    movement.append(s1)
                                    
                                    if cf.projected_cf()*t.quantity< 0:
                                        total_debits = total_debits + cf.projected_cf()*t.quantity
                                    else:
                                        total_credits = total_credits + cf.projected_cf()*t.quantity
                                    #print 'here', cft
                                    
                            else:
                                s1 =[]
                                s1.append(str(cf.pay_day))
                                s1.append(ael.date_from_time(cf.creat_time))
                                s1.append(str(cf.cfwnbr))
                                val = cf.projected_cf() * t.quantity
                                if val > 0:
                                    s1.append('Transfer In')
                                else:
                                    s1.append('Transfer Out')
                                s1.append(val)
                                s1.append(1)
                                movement.append(s1)
                                if cf.projected_cf()*t.quantity< 0:
                                    total_debits = total_debits + cf.projected_cf()*t.quantity
                                else:
                                    total_credits = total_credits + cf.projected_cf()*t.quantity

                        else:
                            s1 =[]
                            s1.append(str(cf.pay_day))
                            s1.append(ael.date_from_time(cf.creat_time))
                            s1.append(str(cf.cfwnbr))
                            s1.append('Interest Reinvestment')
                            s1.append(cf.projected_cf() * t.quantity)
                            s1.append(1)
                            movement.append(s1)
                            #print cf.pp()
                            if cf.projected_cf()*t.quantity< 0:
                                total_debits = total_debits + cf.projected_cf()*t.quantity
                            else:
                                total_credits = total_credits + cf.projected_cf()*t.quantity
                    
                    if str(cft) in dict_movement.keys():
                        dict_movement[str(cft)].append([ss, cf.projected_cf()*t.quantity])
                    else:
                        dict_movement[str(cft)] = [[ss, cf.projected_cf()*t.quantity]]
            

                if cf.type == 'Call Fixed Rate Adjustable' and (cf.pay_day >= startd and cf.pay_day <= endd): #and leg.reinvest == 0:# and reinv == 0):
                    if cf.pay_day != ael.date_today():
                        
                        int_set = cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* t.quantity
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
                                                              
                            
                                #print 'cfra normal',cf.cfwnbr, intbal, int_set, i1
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
                        
                        int_set = cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* t.quantity
                        mx =  mx + int_set
                        #print 'cfra',cf.cfwnbr, int_set, mx    
    
                if cf.type == 'Fixed Rate Adjustable' and (cf.pay_day >= startd and cf.pay_day <= endd):# and (leg.reinvest == 0):
                    int_set = cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* t.quantity
                    val = 0
                    if reinv ==1 or leg.reinvest == 1:
                        if cf.end_day != cf.pay_day:
                            val = get_cf(ins, cf.pay_day) + get_cf(ins, cf.end_day)
                        else:
                            val = get_cf(ins, cf.pay_day)
                            
                    if cf.end_day <= startd and int_set!=0:
                            i1 = i1 + int_set
                            
                    if int_set !=0 and val == 0:
                        #print 'fixed rate adjustable', cf.interest_settled(cf.start_day, cf.end_day,'ZAR')* t.quantity
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
                    #print cf.end_day
                    int_set = cf.interest_settled(cf.start_day, cf.end_day, 'ZAR')* t.quantity
                    if str(cf.end_day) in dict_fixed.keys():
                            dict_fixed[str(cf.end_day)].append(['i', int_set])
                    else:
                        dict_fixed[str(cf.end_day)] = [['i', int_set]]
                        

                      
    movement.sort(lambda x, y: cmp(ael.date(x[0]), ael.date(y[0])))
    
    #print dict_movement
    #RESETS
    dict_reset = {}   
    for c in cashflows:
        if c.type == 'Call Fixed Rate Adjustable':
            for r in c.resets():
                d1 = r.start_day
                while d1 < r.end_day:
                    
                    if str(d1) in dict_reset.keys():
                        #print'before', d1, dict_reset[str(d1)], r.value
                        dict_reset[str(d1)] = dict_reset[str(d1)] + r.value
                        #print'after', d1, dict_reset[str(d1)], r.value
                    else:   
                        dict_reset[str(d1)] =  r.value
                    d1 = d1.add_days(1)
    #print dict_reset            
                        
    
#===========================================================================================
#                                       DAILY INTEREST
#===========================================================================================

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
    
    for days in  dict_fixed.keys():
       if ael.date(days).add_days(-1) <= startd:
            for mov in  dict_fixed[days]:
                val = mov[1] + val
            
    acc = leg.interest_accrued(leg.start_day, startd, 'ZAR')*t.quantity *(-1)
    
    total = -1*(i1 + val + mx) + acc
    #print 'opening bal', total, 'mx', mx, 'acc', acc,'val',val, 'i1 : ',i1  
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
                    #print day1,'int bal i ' ,  intbal, mov[1]
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
        total = total + tot + intbal #+ acc #+ test
        
        intbal = 0
        if tot !=0 or total !=0:
            l2.append(day1.to_string('%Y/%m/%d'))
            l2.append(tot)
            try:
                reset_rate = dict_reset[str(day1)]
            except:
                
                pass
            l2.append(reset_rate)
            #print day1, ':   total' , total , 'intbal', intbal,'set, acc, due', round(int_set,2), round(int_acc,2), round(int_due,2),'acc', acc
            
            l2.append(total)
            l2.append(bal)
            
            interest.append(l2)
            acc =0
            
    
    #total_interest = accrued(leg,endd.first_day_of_month().add_days(-1), endd)*t.quantity *-1#(int_set + int_acc + int_due)*t.quantity *-1 + mx
    ClosingBalance = bal
    #print t.insaddr.insid, OpeningBalance, reset_rate    
    #for cf in cashflows:
    #    if cf.type == 'Call Fixed Rate Adjustable' and (cf.pay_day == today or cf.pay_day == today.add_days(1)):
    #        if abs(round(total,2)) - abs(round(cf.interest_settled(cf.start_day, cf.end_day,'ZAR')*t.quantity *-1,2)) > 1:
    #            print 'INTEREST DISCREPENCY: ', reinv,  startd, t.trdnbr , t.insaddr.insid,round(total,2) - round(cf.interest_settled(cf.start_day, cf.end_day,'ZAR')*t.quantity *-1,2), round(total,2), round(cf.interest_settled(cf.start_day, cf.end_day,'ZAR')*t.quantity *-1,2)
    ains = acm.FInstrument[t.insaddr.insid]
    trd = acm.FTrade[t.trdnbr]
    #print trd
    #if abs(round(FInstrumentCACashflow.caRedemption(ains)*-1,2) - round(ClosingBalance,2)) > 0.01:
    #    print 'ACCOUNT DISCREPENCY: ', ains.Name(),reinv, 'redemption', round(FInstrumentCACashflow.caRedemption(ains)*-1,2),'closing',  round(ClosingBalance,2)
    #else:
            #    print total, cf.interest_settled(cf.start_day, cf.end_day,'ZAR')* t.quantity
    #print p.ptyid, total_interest, mx
#=========================================================================================        
#                       XML
#=========================================================================================    

    # SUMMARY
    # =========
    
    OB = formnum(OpeningBalance)
    TC =  formnum(total_credits)
    TD =  formnum(total_debits)
    TI = formnum(total_interest)
    CB =  formnum(ClosingBalance)
    
    ACCSUM = SubElement(STAT, "ACCSUM")
    SubElement(ACCSUM, "OBAL").text = OB
    SubElement(ACCSUM, "TCRED").text = TC
    SubElement(ACCSUM, "TDEB").text = TD
    SubElement(ACCSUM, "TINT").text = TI
    SubElement(ACCSUM, "CBAL").text = CB
    
    sum1 = OpeningBalance

    # MOVEMENTS
    # =========
    
   
    YourTrans = SubElement(STAT, "YourTrans")
    TRANS = SubElement(YourTrans, "TRANLIN")
    SubElement(TRANS, "VDAT").text = startd.to_string('%Y/%m/%d')
    SubElement(TRANS, "PDAT").text = "-"
    SubElement(TRANS, "DLNO").text = "-"
    SubElement(TRANS, "CDES").text = "Balance Brought Forward"
    SubElement(TRANS, "TAMT").text = OB
    SubElement(TRANS, "TABAL").text = OB
    
       
    for x in movement:
        output=''
        if x[5] == 1:
            sum1 = sum1 + x[4]
        
        
        TA = formnum(x[4])
        S =  formnum(sum1)
        
        TRANS = SubElement(YourTrans, "TRANLIN")
        SubElement(TRANS, "VDAT").text = ael.date(x[0]).to_string('%Y/%m/%d')
        SubElement(TRANS, "PDAT").text = ael.date(x[1]).to_string('%Y/%m/%d')
        SubElement(TRANS, "DLNO").text = str(x[2])
        SubElement(TRANS, "CDES").text = str(x[3])
        SubElement(TRANS, "CREF").text = str(x[2])
        SubElement(TRANS, "TAMT").text = TA
        SubElement(TRANS, "TABAL").text = S
        
        
    # INTEREST
    # ========
    
    INTEREST = SubElement(STAT, "INTEREST")
    
    for x in interest:
        output=''
        
        IA = formnum(x[1])
        IB = formnum(x[3])
        AB = formnum(x[4])
        
        INTLIN = SubElement(INTEREST, "INTLIN")
        SubElement(INTLIN, "VDAT").text = str(x[0])
        SubElement(INTLIN, "IAMNT").text = IA
        SubElement(INTLIN, "IRATE").text = str(x[2])
        SubElement(INTLIN, "IBAL").text = IB
        SubElement(INTLIN, "ABAL").text = AB
        
     
    #Footer
    #======
    
    #"C:\\CALL_ACCOUNT_STATEMENT.xml"  
    #print name
    xmloutFile = open(str(name), 'w')
    #xmloutFile.write('<?xml-stylesheet type="text/xsl" href="\\\\v036syb004001\\Atlas-End-Of-Day\\MoneyMarketStatements\\XSL\\newform.xsl"?>\n')
    xmloutFile.write('<?xml-stylesheet type="text/xsl" href="Y:\\Jhb\\Arena\\Data\\Money Markets Statements\\XSL\\newform.xsl"?>\n')
    ElementTree(DOC).write(xmloutFile, encoding='utf-8')
    os.startfile(str(name))
    return status
    
   
def get_cf(ins, d):
    val = 0
    for cf in ins.legs()[0].cash_flows():
        if cf.type == 'Interest Reinvestment' and cf.pay_day == d:
            val = val + cf.projected_cf()
    return val    


'''
select ael_s(t, 'aa.test', @Start_Date{Today}, @End_Date{Today}) 
from trade t,
instrument i
where i.insaddr =t.insaddr
and i.insid = @Ins{;Instrument.insid where instype = 'Deposit'}
'''
#instrs = ['137976-ZAR-2205-03','747360-ZAR-2203-01','528042-ZAR-3203-01','620104-ZAR-2203-01','528703-ZAR-2203-01','519140-ZAR-2201-01','527101-ZAR-2201-02','346593-ZAR-2201-01','613968-ZAR-2201-01','526632-ZAR-2231-21','526632-ZAR-2231-23']
'''instrs = ['137976-ZAR-2205-03','528042-ZAR-3203-01']
d1 = ael.date('01/02/2008')
d2 = ael.date_today()#('02/04/2008')
for i in instrs:
    ins = ael.Instrument[i]
    print '\n\n', ins.insid, ins.legs()[0].reinvest
    t = ins.trades()[0]
    print ins.legs()[0].interest_accrued(t.insaddr.legs()[0].start_day, d1)
    print ins.legs()[0].interest_accrued(t.insaddr.legs()[0].start_day, d1.add_days(-1))
    #print  t.insaddr.legs()[0].interest_accrued(t.insaddr.legs()[0].start_day, d1)
    StatementXML(t,d1, d2)'''


#tf = ael.TradeFilter['Call_All_Trades']
#Y = tf.trades()
#flag =0
#d1 = ael.date('01/04/2008')
#d2 = ael.date('01/03/2008')'''
#d2 = ael.date_today()#('02/04/2008')
#print 'DATE: ', d1, d2
#for x in Y:
#    flag = 0
#    ins = x.insaddr
    #if ins.legs()[0].reinvest == 0:
#    for cf in ins.legs()[0].cash_flows():
#        if cf.type == 'Fixed Rate Adjustable' : #'Interest Reinvestment' and abs(cf.projected_cf()) > 1:
                #print cf.creat_usrnbr.userid
#                flag = flag + 1
#    if flag >0:
#        print x.trdnbr, x.add_info('Funding Instype')
    #t = x# ael.Trade[x]
    #p = t.counterparty_ptynbr
    #cts = p.contacts()
    #flag = 0   
    #if flag < 10:
#    StatementXML(x,d1, d2,'C://')
    #    flag = flag +1
#d1 = ael.date('01/02/2008')
#d2 = ael.date_today()#('02/04/2008')
'''
print 'DATE: ', d1, d2
for x in Y:
    #t = x# ael.Trade[x]
    #p = t.counterparty_ptynbr
    #cts = p.contacts()
    #flag = 0   
    StatementXML(x,d1, d2)'''
    #                        flag =1
    #if flag == 0:                    
    #    print p.ptyid, ',', t.trdnbr#c.fullname,',', r.event_chlnbr.entry#, c.add_info('Comm Freq')'''
