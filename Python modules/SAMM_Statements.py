import ael, acm, random
from zak_funcs import formnum
from xml.etree.ElementTree import Element, SubElement, dump, XML, tostring, ElementTree, parse

'''
Purpose                       :  Change Contact details,Updated contact info., Added the check for contact rule event choicelist.
Department and Desk           :  PCG OPERATIONS,
Requester                     :  Bernie Franke ,Chantal Nicholson, Sylvia Ackerman, Heinrich Cronje
Developer                     :  Ickin Vural,Willie van der Bank, Zaakirah kajee, Heinrich Cronje, Anwar Banoo, Jan Sinkora, Gabriel Marko
CR Number                     :  209946, 368883, 392806, 430054, 575272, 438949, XXXXXX, ABITFA-3945
Date                          :  13/07/2010, 2010-08-05, 2010-09-14, 2011-02-15, 2012-09-07, 2012-11-14, 2016-06-01
'''

def GenStatementXML(t,startd, endd, CPRINT,CFAX, CEMAIL, freq,con,path,*rest):
    """
    Generates the statement XML.

    If the CPRINT flag is set to 1, this returns 'FAIL' or a XML object, which need to be further handled.
    If the CPRINT flag is set to 0, this returns 'FAIL' or 'SUCCESS' and has a side-effect (creates the file)

    """
    newdate = ael.date_today().to_string('%Y%m%d')
    s =  str(freq) + '_' + str(t.insaddr.insid[0:18]) + '_' + newdate+ '_'+ str(int(random.random()*1000)) +'.xml'
    name = path + '//Input' + s

    if CPRINT == 1:

        STAT = Element("STATEMENT")

    else:
        DOC = Element("DOC")
        STAT = SubElement(DOC, "STATEMENT")


    if endd > ael.date_today():
        endd = ael.date_today()


# ========================================================================================
#       CONTACT DETAILS
# ========================================================================================

    CUST = SubElement(STAT, "CUSTLIN1")
    SubElement(CUST, "BNAM").text ='ABSA CAPITAL'
    SubElement(CUST, "BAD1").text ='PRIVATE BAG X10056'
    SubElement(CUST, "BAD2").text ='SANDTON'
    SubElement(CUST, "BAD3").text ='SOUTH AFRICA'
    SubElement(CUST, "BAD4").text ='2146'
    SubElement(CUST, "BTEL").text ='011 895 6734/6741'
    SubElement(CUST, "BFAX").text ='PRODUCT CONTROL GROUP'
    SubElement(CUST, "BCON").text ='Client Services (tmscs@barclayscapital.com)'

    SubElement(STAT, "MSG").text = 'Absa Capital has moved 15 ALICE LANE, SANDTON, 2196. Please make note of our new contact details for traders is: (011) 895 5521/5522. '


# ========================================================================================
#       CUSTOMER CONTACT DETAILS
# ========================================================================================

    p = t.counterparty_ptynbr
    CNAM = p.fullname + ' ' + p.fullname2
    PRINT = 'FAX'
    flag = 0
    check = 0
    l1 = []
    ctot=[]
    if CPRINT == 1:
        c1 = []
        c1.append('PRINT')
        c1.append('TMSCS')
        ctot.append(c1)

    if con != 0:
        c = ael.Contact[con]

        Fax = c.fax
        Attention = c.attention
        if c.address:
            l1.append(c.address.replace('&', '&amp;'))

        if c.address2:
            l1.append(c.address2.replace('&', '&amp;'))

        if c.city:
            l1.append(c.city.replace('&', '&amp;'))

        if c.zipcode:
            l1.append(c.zipcode)

        if c.country:
            l1.append(c.country.replace('&', '&amp;'))

        if CFAX ==1 and c.fax:
            c1 = []
            c1.append('FAX')
            c1.append(c.fax.replace('+27', '0'))
            ctot.append(c1)
            CFAX = 0
        if CEMAIL ==1 and c.email:
            c1 = []
            c1.append('EMAIL')
            c1.append(c.email)
            ctot.append(c1)
            CEMAIL = 0
    else:

        Fax = p.fax
        Attention = p.attention
        if p.address:
            l1.append(p.address.replace('&', '&amp;'))

        if p.address2:
            l1.append(p.address2.replace('&', '&amp;'))

        if p.city:
            l1.append(p.city.replace('&', '&amp;'))

        if p.zipcode:
            l1.append(p.zipcode)

        if p.country:
            l1.append(p.country.replace('&', '&amp;'))

        if CFAX ==1 and p.fax:
            c1 = []
            c1.append('FAX')
            c1.append(p.fax.replace('+27', '0'))
            ctot.append(c1)
            CFAX = 0
        if CEMAIL ==1 and p.email:
            c1 = []
            c1.append('EMAIL')
            c1.append(p.email)
            ctot.append(c1)
            CEMAIL = 0



    CACC = str(t.insaddr.insid[0:18])
    CNAM = CNAM.replace('&', '&amp;')

    CUST1 = SubElement(STAT, "CUSTLIN2")
    SubElement(CUST1, "CNAM").text =CNAM
    SubElement(CUST1, "CACC").text =CACC

    ind = 1
    for x in l1:
        field = "CADD" + str(ind)
        SubElement(CUST1, field).text = x
        ind = ind +1


    ind = 1
    COM = SubElement(STAT, "COMM")
    for x in ctot:
        fielda = "CTYPE" + str(ind)
        fieldb = "CDEST" + str(ind)
        SubElement(COM, fielda).text = x[0]
        SubElement(COM, fieldb).text = x[1]
        ind = ind +1

# ========================================================================================
#       HEADER 2
# ========================================================================================

    month = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    sy, sm, sd = startd.to_ymd()
    ey, em, ed = endd.to_ymd()



    if p.attention:
        ATT = 'Attention:' + Attention
    else:
        ATT = 'Attention: To whom it may concern'
    ins = t.add_info('Funding Instype')
    H1 = ins
    H2 = str(sd) + ' ' + month[sm] + ' ' + str(sy) + ' to ' + str(ed) + ' ' + month[em] + ' ' + str(ey)


    HEAD2 = SubElement(STAT, "header2")
    SubElement(HEAD2, "ATT").text = str(ATT)
    SubElement(HEAD2, "H1").text = H1
    SubElement(HEAD2, "H2").text = H2
    SubElement(HEAD2, "CDATE").text = str(endd)

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
                                    s1.append(cf.start_day)
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

                            if cf.projected_cf()*t.quantity< 0:
                                total_debits = total_debits + cf.projected_cf()*t.quantity
                            else:
                                total_credits = total_credits + cf.projected_cf()*t.quantity

                    if str(cft) in dict_movement.keys():
                        dict_movement[str(cft)].append([ss, cf.projected_cf()*t.quantity])
                    else:
                        dict_movement[str(cft)] = [[ss, cf.projected_cf()*t.quantity]]


                if cf.type == 'Call Fixed Rate Adjustable' and (cf.pay_day >= startd and cf.pay_day <= endd):
                    if cf.pay_day != ael.date_today():

                        int_set = cf.interest_settled(cf.start_day, cf.end_day, t.curr.insid)* t.quantity
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



                if cf.type == 'Call Fixed Rate Adjustable' and (leg.reinvest == 0):

                    if cf.end_day <= startd and cf.pay_day > endd:

                        int_set = cf.interest_settled(cf.start_day, cf.end_day, t.curr.insid)* t.quantity
                        mx =  mx + int_set

                if cf.type == 'Fixed Rate Adjustable' and (cf.pay_day >= startd and cf.pay_day <= endd):
                    int_set = cf.interest_settled(cf.start_day, cf.end_day, t.curr.insid)* t.quantity
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
                    int_set = cf.interest_settled(cf.start_day, cf.end_day, t.curr.insid)* t.quantity
                    if str(cf.end_day) in dict_fixed.keys():
                            dict_fixed[str(cf.end_day)].append(['i', int_set])
                    else:
                        dict_fixed[str(cf.end_day)] = [['i', int_set]]

    movement.sort(lambda x, y: cmp(ael.date(x[0]), ael.date(y[0])))


    #RESETS
    #======

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

    acc = leg.interest_accrued(leg.start_day, startd, t.curr.insid)*t.quantity *(-1)
    total = -1*(i1 + val + mx) + acc

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
                if mov[0] =='r':
                    intbal = intbal + (mov[1])*(-1)


        else:
            mov1 =   0

        int_set = legs[0].interest_settled(day1, day2, legs[0].curr.insid)
        int_acc = legs[0].interest_accrued(day1, day2, legs[0].curr.insid)

        tot = (int_set + int_acc )*t.quantity *-1
        total_interest = tot + total_interest
        bal = bal + mov1
        total = total + tot + intbal
        intbal = 0

        if tot !=0 or total !=0:
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


    ClosingBalance = bal


#=========================================================================================
#                       XML
#=========================================================================================
    #check if opening and closing balance is 0
    if round(OpeningBalance) == 0 and round(total_credits) == 0 and round(total_debits) == 0 and round(total_interest) == 0 and round(ClosingBalance) == 0:
        #print 'Trade ',t.trdnbr,' have 0 opening and closing balance with no movements during period: ',startd,' - ',endd
        return 'FAIL'


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


    SubElement(STAT, "YourTrans")
    sum1 = OpeningBalance

    # MOVEMENTS
    # =========

    TRANS = SubElement(STAT, "TRANLIN")
    SubElement(TRANS, "VDAT").text = startd.to_string('%Y/%m/%d')
    SubElement(TRANS, "PDAT").text = ""
    SubElement(TRANS, "DLNO").text = ""
    SubElement(TRANS, "CDES").text = "Balance Brought Forward"
    SubElement(TRANS, "TAMT").text = OB
    SubElement(TRANS, "TABAL").text = OB

    for x in movement:

        if x[5] == 1:
            sum1 = sum1 + x[4]


        TA = formnum(x[4])
        S =  formnum(sum1)


        TRANS = SubElement(STAT, "TRANLIN")
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

        INTLIN = SubElement(STAT, "INTLIN")
        SubElement(INTLIN, "VDAT").text = str(x[0])
        SubElement(INTLIN, "IAMNT").text = formnum(x[1])
        SubElement(INTLIN, "IRATE").text = str(x[2])
        SubElement(INTLIN, "IBAL").text = formnum(x[3])
        SubElement(INTLIN, "ABAL").text = formnum(x[4])

    #Footer
    #======


    if CPRINT == 1:
        return STAT

    else:
        #moved the file creation to end so that it will not create the file if the balances is zero
        try:
            xmloutFile=open(name, 'w')
            ElementTree(DOC).write(xmloutFile, encoding='utf-8')
        except:
            print "can't open {0}".format(name)
            raise Exception("can't open {0}".format(name))

        return 'SUCCESS'

#=================================================================================================================
#=================================================================================================================

def get_cf(ins, d):
    val = 0
    for cf in ins.legs()[0].cash_flows():
        if cf.type == 'Interest Reinvestment' and cf.pay_day == d:
            val = val + cf.projected_cf()
    return val

def GEN_STATEMENTS(tf, path):
    global printflag
    printflag = 0
    DOC = Element("DOC")
    newdate = ael.date_today().to_string('%Y%m%d')
    fname = "Print_Statements_" + newdate + ".xml"
    name = path + '//Print_Input/' + fname
    dict_days = {'Monday': 1 , 'Tuesday':2, 'Wednesday':3, 'Thursday':4, 'Friday':5}
    today = ael.date_today().add_days(-1)
    yesterday = today.add_days(-1)
    fdm = today.first_day_of_month()
    ldm = today.add_months(1).first_day_of_month().add_days(-1)
    week = today.day_of_week()

    trade_errors = []
    for t in tf.trades():
        p = t.counterparty_ptynbr
        cts = p.contacts()
        comm = ''
        for c in cts:
            # for all contacts of the counterparty of the trade
            for r in c.rules():
                if (r.event_chlnbr and r.instype == t.insaddr.instype
                    and r.event_chlnbr.entry == 'Money Market'):
                    freq = c.add_info('Comm Freq')
                    if freq:
                        # build a list of dictionaries
                        # 'params': list of parameters for the GenStatementXML function
                        # 'callback' (ptional): a callback function that get one parameter: the result of the generating function
                        statement_params = []

                        if (freq.find('Daily') >= 0 or freq.find('All') >= 0):
                            comm = str(c.add_info('Comm Type - Daily'))

                            if (comm.find('Fax')>= 0 or comm.find('All') >= 0):
                                statement_params.append({'params': [t, fdm, today, 0, 1, 0, '/DAILY', c.seqnbr, path]})
                            if (comm.find('Email')>= 0 or comm.find('All') >= 0):
                                statement_params.append({'params': [t, fdm, today, 0, 0, 1, '/DAILY', c.seqnbr, path]})



                        if freq.find('Weekly') >= 0 or freq.find('All') >= 0:

                            try:
                                dict_days[str(c.add_info('Comm Freq - Weekly'))]
                                if dict_days[str(c.add_info('Comm Freq - Weekly'))] == week:
                                    comm = str(c.add_info('Comm Type - Weekly'))
                                    if (comm.find('Fax')>= 0 or comm.find('All') >= 0):
                                        statement_params.append({'params': [t, today.add_days(-6), today, 0, 1, 0, '/WEEKLY', c.seqnbr, path]})
                                    if (comm.find('Email')>= 0 or comm.find('All') >= 0):
                                        statement_params.append({'params':[t, today.add_days(-6), today, 0, 0, 1, '/WEEKLY', c.seqnbr, path]})
                            except:
                                pass

                        if freq.find('Monthly') >= 0 or freq.find('All') >= 0:

                            comm = str(c.add_info('Comm Type - Monthly'))
                            if (comm.find('Print') >= 0 or comm.find('All') >= 0):
                                if today == fdm:
                                    # callback function
                                    def check_tag(tag):
                                        if tag != 'FAIL':
                                            DOC.append(tag)
                                            printflag = 1

                                    statement_params.append({'params': [t, today.add_months(-1), today, 1, 0, 0, '/MONTHLY', c.seqnbr, name, path],
                                                             'callback': check_tag})

                            mfreq = str(c.add_info('Comm Freq - Monthly'))
                            if  (mfreq == 'First Of Month') and (today == fdm):

                                if (comm.find('Fax') >= 0 or comm.find('All') >= 0):
                                    statement_params.append({'params': [t, today.add_months(-1), today.add_days(-1), 0, 1, 0, '/MONTHLY', c.seqnbr, path]})
                                if (comm.find('Email') >= 0 or comm.find('All') >= 0):
                                    statement_params.append({'params': [t, today.add_months(-1), today.add_days(-1), 0, 0, 1, '/MONTHLY', c.seqnbr, path]})


                            elif (mfreq == 'End Of Month') and today == ldm:

                                if (comm.find('Fax') >= 0 or comm.find('All') >= 0):
                                    statement_params.append({'params': [t, ldm.first_day_of_month(), ldm, 0, 1, 0, '/MONTHLY', c.seqnbr, path]})
                                if (comm.find('Email') >= 0 or comm.find('All') >= 0):
                                    statement_params.append({'params': [t, ldm.first_day_of_month(), ldm, 0, 0, 1, '/MONTHLY', c.seqnbr, path]})

                            else:
                                if (mfreq != 'None') and str(today.to_ymd()[2]) == (mfreq):
                                    if (comm.find('Fax') >= 0 or comm.find('All') >= 0):
                                        statement_params.append({'params': [t, today.add_months(-1), today.add_days(-1), 0, 1, 0, '/MONTHLY', c.seqnbr, path]})
                                    if (comm.find('Email') >= 0 or comm.find('All') >= 0):
                                        statement_params.append({'params': [t, today.add_months(-1), today.add_days(-1), 0, 0, 1, '/MONTHLY', c.seqnbr, path]})

                        # generate the reports, use callbacks when defined
                        for param_dict in statement_params:
                            params = param_dict['params']

                            try:
                                result = GenStatementXML(*params)
                                if result == 'FAIL':
                                    # if the report failed, it should still show
                                    # as successfull for RTB
                                    pass

                                if 'callback' in param_dict:
                                    # a callback has been set, let it react to the result
                                    callback = param_set['callback']
                                    callback(result)
                            except Exception, e:
                                error_str = 'trdnbr {0}: {1}'.format(t.trdnbr, e)
                                trade_errors.append(error_str)
                        break
    if printflag == 1:
        xmloutFile = name
        ElementTree(DOC).write(xmloutFile, encoding='utf-8')

    return trade_errors

ael_gui_parameters = { 'windowCaption':'SAMM Money Market Statements'}

ael_variables = [['TradeFilter', 'Trade Filter: ', 'FTradeSelection', acm.FTradeSelection.Select(''), None, 1, 1],
                    ['Path', 'Output Path', 'string', None, None, 1, 0]]

def ael_main(dict):

    success = True
    for trdf in  dict['TradeFilter']:
        try:
            tf = ael.TradeFilter[trdf.Name()]
            errors = GEN_STATEMENTS(tf, dict['Path'])
            if errors:
                error = "ERROR: SAMM_Statements - trade filter {0} had errors on these trades: ".format(trdf.Name())
                error += "\n".join(errors)
                ael.log(error)
                success = False
        except Exception, e:
            error = 'ERROR: SAMM_Statements - did not run for trade filter: {0} (error: {1})'.format(trdf.Name(), e)
            ael.log(error)
            success = False

    if success:
        print "success"
'''
TODAY = acm.Time().DateToday()
FIRSTOFMONTH = acm.Time().FirstDayOfMonth(TODAY)
startd          = ael.date(FIRSTOFMONTH)
endd            = ael.date(TODAY)

print GenStatementXML(ael.Trade[16297756],startd,endd,1,0,0,'Daily',0,'F:\\Cogito\\',None)
'''
