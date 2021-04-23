"""-----------------------------------------------------------------------
MODULE
    SAEQ_QuantDividends

HISTORY
         When: 	    CR Number:                  Who:	  					   What:  	     Requestor:
    2012-03-05         C127111       Nidheesh Sharma	  Fixed bug - output contained duplicate entries	Kiribakka Tendo
    2012-02-07         C774583       Jan Sinkora          Fixed bug - output contained duplicate entries	Kiribakka Tendo
-----------------------------------------------------------------------"""

import ael, string

def Instrument():
    Instrument=['Future/Forward', 'Option']
    Instrument.sort()
    return Instrument

def Port():
    Port=[]
    for p in ael.Portfolio:
        Port.append(p.prfid)
    Port.sort()
    return Port

def Filter():
    Filter=[]
    for f in ael.TradeFilter:
        Filter.append(f.fltid)
    Filter.sort()
    return Filter

def Index():
    Index=[]
    for i in ael.Instrument.select('instype = "EquityIndex"'):
        Index.append(i.insid)
    Index.sort()
    return Index

def ael_main(ael_dict):

    Instrument = ael_dict["Instrument"]
    Port = ael_dict["Port"]
    Filter = ael_dict["Filter"]
    Index = ael_dict["Index"]
    StartDate = ael_dict["StartDate"]
    Server = ael_dict["Server"]

    tel=0

    if len(Port) != 0:
        np = Numberp(Instrument, Port)
        for u in np:

            tel += 1
            Quantify(Instrument, Index, StartDate, Server, Port, Filter, tel, np)

    elif len(Filter) != 0:

        nf = Numberf(Instrument, Filter)

        for f in nf:

            tel += 1
            Quantify(Instrument, Index, StartDate, Server, Port, Filter, tel, nf)
    else:
        print 'You need to choose a Portfolio or a TradeFilter'

ael_variables = [('Instrument', 'Instrument', 'string', Instrument(), '', 1, 1),
                 ('Port', 'Port', 'string', Port(), '', 0, 1),
                 ('Filter', 'Filter', 'string', Filter(), '', 0, 1),
                 ('Index', 'Index', 'string', Index(), 'ZAR/ALSI', 1, 1),
                 ('StartDate', 'StartDate', 'date', None, ael.date_today(), 1),
                 ('Server', 'Server', 'string', None, 'C:\\', 1)]

def Numberp(Instrument,Port,*rest):

    ExpList=[]
    for prt in Port:
        Prtf = ael.Portfolio[prt]

        for t in Prtf.trades():

            ins = t.insaddr

            if ins.instype in Instrument and ins.exp_day >= ael.date_today():
                if ins.exp_day not in ExpList:
                    ExpList.append(ins.exp_day)
    ExpList.sort()
    return ExpList

def Numberf(Instrument,Filter,*rest):

    ExpList=[]
    today = ael.date_today()
    for fl in Filter:
        fltr = ael.TradeFilter[fl]

        for t in fltr.trades():

            ins = t.insaddr

            if ins.instype in Instrument and ins.exp_day >= today:
                if ins.exp_day not in ExpList:
                    ExpList.append(ins.exp_day)
    ExpList.sort()
    return ExpList

def Quantify(Instrument,Index,StartDate,Server,Port,Filter,tel,EXPLISTS,*rest):

    Global=[]
    Global1=[]
    ConsList=[]


    teller = tel - 1
    StartDate = ael.date(StartDate)
    EndDate = ael.date(EXPLISTS[teller])

    for i in Index:

        ins = ael.Instrument[i]
        y       = ins.used_repo_curve()
        factor  = ins.index_factor
        curr    = ael.Instrument[ins.curr.insid]

        SpotDays = ins.spot_banking_days_offset

        EndSpot = EndDate.add_banking_day(curr, SpotDays)
        StartSpot = StartDate.add_banking_day(curr, SpotDays)
        link = ins.combination_links()

        for lnk in link.members():

            con = lnk.member_insaddr
            ConsList.append(con.insid)

            strm = ael.DividendStream.select('insaddr = "%d"' %(con.insaddr))

            for st in strm:
                # only get the primary stream
                if st.name[-3:] == con.insid[-3:]:
                    for est in st.estimates():
                        day = est.ex_div_day.add_banking_day(curr, -1)
                        if day >= StartDate:
                            if day < EndDate:
                                list1=[]

                                list1.append(StartDate)             #StartDate
                                list1.append(EndDate)               #EndDate
                                list1.append(i)                     #Index
                                list1.append(con.insid)             #Constituent
                                list1.append(est.ex_div_day)        #ExDivDay
                                list1.append(est.pay_day)           #PayDay
                                list1.append(est.dividend)          #Dividend

                                wght = lnk.weight

                                DiscountFactor1 = y.yc_rate(StartDate, est.pay_day, 'Simple', 'Act/365', 'Discount')
                                DiscountFactor2 = y.yc_rate(StartDate, EndSpot, 'Simple', 'Act/365', 'Discount')
                                DiscountFactor3 = y.yc_rate(StartSpot, EndSpot, 'Simple', 'Act/365', 'Discount')
                                IndexPoints = (wght/factor)*est.dividend

                                list1.append(IndexPoints)                  #IndexPoints

                                DivFV = (IndexPoints * (DiscountFactor1/DiscountFactor2))
                                DivPV = DivFV * DiscountFactor3

                                list1.append(DivPV)                        #DivPV

                                if list1 not in Global:             #preventing duplicates
                                    Global.append(list1)


    Global.sort()

    if teller == 0:
        outfile1 = Server + 'DivS_' + StartDate.to_string('%Y%m%d') + '.csv'
        report1 = open(outfile1, 'w')

        Headers=[]

        Headers = ['StartDate', 'Expiry', 'Instrument', 'Constituent', 'ExDivDay', 'PayDate', 'Dividend', 'IndexPoints', 'DivPv']
        for i in Headers:

            report1.write((str)(i))
            report1.write(',')
        report1.write('\n')
        report1.close()

    outfile2 = Server + 'DivS_' + StartDate.to_string('%Y%m%d') + '.csv'
    report2 = open(outfile2, 'a')

    for lsts in Global:

        for ls in lsts:

            report2.write((str)(ls))
            report2.write(',')
        report2.write('\n')

    strms = ael.DividendStream.select()
    listr=[]

    for st in strms.members():
        length = len(st.name)
        ins = st.insaddr
        inst = st.insaddr.insid
        curr = ael.Instrument[ins.curr.insid]

        if length == 3:

            if inst not in ConsList:

                ins = ael.Instrument[inst]
                SpotDays = ins.spot_banking_days_offset
                EndSpot = EndDate.add_banking_day(curr, SpotDays)
                StartSpot = StartDate.add_banking_day(curr, SpotDays)

                for est in st.estimates():
                    day = est.ex_div_day.add_banking_day(curr, -1)
                    if day >= StartDate:
                        if day < EndDate:

                            listo=[]
                            listo.append(StartDate)             #StartDate
                            listo.append(EndDate)               #EndDate
                            listo.append('Stock')               #Index
                            listo.append(ins.insid)             #Constituent
                            listo.append(est.ex_div_day)        #ExDivDay
                            listo.append(est.pay_day)           #PayDay
                            listo.append(est.dividend)          #Dividend

                            listo.append('NoIndexPoints')       #IndexPoints

                            y = ins.used_repo_curve()
                            DiscountFactor1 = y.yc_rate(StartDate, est.pay_day, 'Simple', 'Act/365', 'Discount')
                            DiscountFactor2 = y.yc_rate(StartDate, EndSpot, 'Simple', 'Act/365', 'Discount')
                            DiscountFactor3 = y.yc_rate(StartSpot, EndSpot, 'Simple', 'Act/365', 'Discount')

                            dividend = est.dividend

                            DivFV = (dividend * (DiscountFactor1/DiscountFactor2))
                            DivPV = DivFV * DiscountFactor3

                            listo.append(DivPV)                        #DivPV

                            Global1.append(listo)


    Global1.sort()

    Blank=[]
    for b in Blank:
        report2.write(b)
        report2.write('\n')


    for lsts in Global1:

        for ls in lsts:

            report2.write((str)(ls))
            report2.write(',')
        report2.write('\n')
    report2.close()

    print'Success'
    print 'The file has been saved at:' + Server + 'DivS_' + StartDate.to_string('%Y%m%d') + '.csv'
    return


