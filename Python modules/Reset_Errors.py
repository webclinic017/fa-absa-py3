'''
This Python script produces a reset exceptions report which is used by Middle Office in conjunction with a file that is managed by them
and a script which filters out known reset exceptions.

Purpose                 :[Initial deployment]
Department and Desk     :[Middle Office]
Requester               :[Pedro de Moura]
Developer               :[Willie van der Bank]
CR Number               :[237787 2012-06-08]
'''

import acm, ael

today = ael.date_today()
stoday = today.to_string('%Y-%m-%d')

#==========================================================================================================
def GenStrFromList(delim, list):
    s = ''
    k = 0
    cnt = len(list)

    for o in list:
        k += 1
        if k < cnt:
            s = s + str(o) + delim
        else:
            s = s + str(o) + '\n'

    return s

#==========================================================================================================
def roundex(v):
    return float(str(v))

#==========================================================================================================
def CheckResetBizDay(dt, fleg):
    ret = 0

    cal1 = fleg.ResetCalendar()
    cal2 = fleg.Reset2Calendar()
    cal3 = fleg.Reset3Calendar()
    cal4 = fleg.Reset4Calendar()
    cal5 = fleg.Reset5Calendar()

    if cal1:
        ret = ret or cal1.IsNonBankingDay(cal2, cal3, dt)

    if cal4:
        ret = ret or cal4.IsNonBankingDay(cal5, cal5, dt)

    return ret

#==========================================================================================================
def check_used_v_expected(rst, endcpi, cpi_rebase_dt):
    ret_scale = rst.ResetType() in ['Return', 'Nominal Scaling']
    zero_val = rst.FixingValue() == 0 and rst.FixingValue2() == 0

    retfin = {}

    dt = ael.date(rst.Day())
    sdt = dt.to_string('%Y-%m-%d')

    fltref1 = rst.Leg().FloatRateReference()
    fltref2 = rst.Leg().FloatRateReference2()

    fltref_id = fltref1_id = fltref2_id = ''

    if fltref1:
        fltref1_id = fltref1.Name()
        fltref_id = fltref1.Name()

    if fltref2:
        fltref2_id = fltref2.Name()
        fltref_id += ' | ' + fltref2.Name()

    #------------------------------------------------------------------------------------------------
    # check for missing resets
    ret = []

    if zero_val and dt <= today:
        ret.append( [fltref_id, sdt, rst.ResetType(), '' ] )

    if len(ret) > 0:
        retfin['MISSING RESET'] = ret


    #------------------------------------------------------------------------------------------------
    # check for actual v expected
    if  not ret_scale and not zero_val:
        ret = []

        if dt <= today:
            act1 = rst.FixingValue()
            act2 = rst.FixingValue2()

            expected1 = expected2 = 0

            if fltref1:
                expected1 = roundex(fltref1.UsedPrice(dt, None, None))

                if abs(expected1 - act1) > 1e-6:
                    det = str(act1) + '% v ' + str(expected1) + '%'
                    ret.append( [fltref1_id, sdt, rst.ResetType(), det] )

            if fltref2:
                expected2 = roundex(fltref2.UsedPrice(dt, None, None))

                if abs(expected2 - act2) > 1e-6:
                    det = str(act2) + '% v ' + str(expected2) + '%'
                    ret.append( [fltref2_id, sdt, rst.ResetType(), det] )

        if len(ret) > 0:
            retfin['USED V ACTUAL'] = ret


    #------------------------------------------------------------------------------------------------
    # check for non-zero future resets
    ret = []

    if dt > today and not zero_val and not ret_scale:
        ret.append( [fltref_id, sdt, rst.ResetType(), '' ] )

    if len(ret) > 0:
        retfin['FUTURE NON-ZERO'] = ret

    #------------------------------------------------------------------------------------------------
    # check for zero read-time
    ret = []

    if rst.ReadTime() == 0:
        ret.append( [fltref_id, sdt, rst.ResetType(), '' ] )

    if len(ret) > 0:
        retfin['NON-ZERO READ TIME'] = ret

    #------------------------------------------------------------------------------------------------
    # check for non-biz reset days
    ret = []

    leg = rst.Leg()

    ishol = CheckResetBizDay(dt, leg)

    if ishol:
        ret.append( [fltref_id, sdt, rst.ResetType(), '' ] )

    if len(ret) > 0:
        if dt < today:
            retfin['NON-BUSINESS DAY RESET-PAST'] = ret
        else:
            retfin['NON-BUSINESS DAY RESET-FUTURE'] = ret

    #------------------------------------------------------------------------------------------------
    # check for CPI used v expected
    ret = []
    if ret_scale and rst.Leg().IndexRef() and rst.Leg().IndexRef().Name() == 'SACPI':
        inscpi = ael.Instrument['SACPI']
        indxval = inscpi.cpi_reference(dt)
        indxval = round(indxval, 5)
        fixval = rst.FixingValue()
        if dt <= endcpi:
            if dt < cpi_rebase_dt:
                fixval = round(fixval, 5)
                if fixval <> indxval:
                    det = str(fixval) + ' v ' + str(indxval)
                    ret.append( ['SACPI', sdt, rst.ResetType(), det] )
            else:
                if fixval <> indxval:
                    det = str(fixval) + ' v ' + str(indxval)
                    ret.append( ['SACPI', sdt, rst.ResetType(), det] )
        else:
            if fixval <> 0:
                det = str(fixval) + ' v 0'
                ret.append( [fltref_id, sdt, rst.ResetType(), det] )
                #print rst.Instrument().Name(),'\t',rst.FixingValue(),'\t',indxval,'\t',endcpi,'\t',ael.date(rst.Day())

    if len(ret) > 0:
        if dt < today:
            retfin['CPI RESET - PAST'] = ret
        else:
            retfin['CPI RESET - FUTURE'] = ret

    return retfin

#==========================================================================================================

def get_all_ins(ins, ret):

    ret.append(ins)

    if ins.InsType() in ['Combination']:
        cboinslst = ins.Instruments()

        for cboins in cboinslst:
            ret.append(cboins)

    und = ins.Underlying()

    if und:
        get_all_ins(und, ret)

#==========================================================================================================

def get_exception_resets(dict):

    sfexl = dict['exceptpath']
    exl = []
    fexl = open(sfexl, 'r')
    try:
        s = fexl.readline()
        s = fexl.readline()
        delim = ','
        while s <> '':
            ln = s.split(delim)
            ent = []
            ent.append(ln[0])
            ent.append(ln[1])
            ent.append(ln[2])

            rdt = ael.date(ln[3])
            ent.append(rdt.to_string('%Y-%m-%d'))

            ent.append(ln[4])
            ent.append(ln[5])
            ent.append(ln[6])
            ent.append(int(ln[7]))
            ent.append(ln[8])

            sl = len(ln[9])
            if ln[9][sl-1:sl] == '\n':
                ent.append(ln[9][0:sl-1])
            else:
                ent.append(ln[9])
            exl.append(ent)
            s = fexl.readline()
        fexl.close()
    except Exception, e:
        fexl.close()
        print 'Error in creating exclusions list:', e

    return exl

#==========================================================================================================

def get_endcpi():
    cpi_ins = ael.Instrument['SACPI']
    cpi_prc = ael.Price.select('insaddr = ' + str(cpi_ins.insaddr))

    maxdt = ael.date('2010-01-01')
    for p in cpi_prc:
        if p.day.day_of_month() == 01:
            fdt = p.day.add_months(4)
            if fdt > maxdt:
                maxdt = fdt

    return maxdt

#==========================================================================================================
def filters():
    filters = []
    for f in ael.TradeFilter:
        filters.append(f.fltid)
    filters.sort()
    return filters

ael_variables = [('outpath', 'Output Path', 'string', ['Y:\\Jhb\\Official\\PCG Middle Office\\Reset Reports\\'], 'Y:\\Jhb\\Official\\PCG Middle Office\\Reset Reports\\', 1, 0, 'Enter only full path of file, not filename.'),
                 ('outname', 'File Name', 'string', ['Reset_Errors.tab'], 'Reset_Errors.tab', 1, 0, 'Enter only filename, not path of file.'),
                 ('exceptpath', 'Exception Path', 'string', ['Y:\\Jhb\\Official\\PCG Middle Office\\Reset Reports\\reset_exceptions.csv'], 'Y:\\Jhb\\Official\\PCG Middle Office\\Reset Reports\\reset_exceptions.csv', 0, 0, 'Enter full path and filename.'),
                 ('filter', 'Trade Filter', 'string', filters(), 'MO_ResetErrorRTB', 1)]

def ael_main(dict):

    sfout = dict['outpath'] + dict['outname']

    dat = {}
    tf = acm.FTradeSelection[dict['filter']]
    trds = tf.Trades()
    cnt = len(trds)
    n = 0

    print 'Retrieving resets'

    for trd in trds:
        n += 1
        if n % 1000 == 0:
            print n, ' | ', cnt

        trdnbr = trd.Oid()

        inslst = []
        ins = trd.Instrument()

        isCall = ins.OpenEnd() == 'Open End' and ins.InsType() in ['Deposit']

        if not isCall:
            get_all_ins(ins, inslst)

        for ins in inslst:
            legs = ins.Legs()

            for leg in legs:
                fltref1 = leg.FloatRateReference()
                fltref2 = leg.FloatRateReference2()
                indref = leg.IndexRef()
                if indref <> None:
                    indref = indref.Name()

                if fltref1 or fltref2 or indref == 'SACPI':
                    cfs = leg.CashFlows()

                    for cf in cfs:
                        if ael.date(cf.PayDate() ) > today:
                            rsts = cf.Resets()

                            if len(rsts) > 0:
                                if not dat.has_key(trdnbr):
                                    dat[trdnbr] = []
                                dat[trdnbr].extend(rsts)


    trds = dat.keys()
    trds.sort()

    cnt = len(trds)
    n = 0

    out = []
    endcpi = get_endcpi()
    cpi_rebase_dt = ael.date('2013-04-01')

    print 'Checking for exceptions'

    for trdnbr in trds:
        trd = acm.FTrade[trdnbr]

        n += 1
        if n % 500 == 0:
            print n, ' | ', cnt

        for rst in dat[trdnbr]:
            checks = check_used_v_expected(rst, endcpi, cpi_rebase_dt)

            ckeys = checks.keys()
            ckeys.sort()

            for check in ckeys:
                c = checks[check]
                area = trd.Portfolio().add_info('Parent_Portfolio')
                ins = rst.Leg().Instrument()
                portid = trd.Portfolio().Name()

                for itm in c:
                    lst = [check, area]
                    lst.extend(itm)
                    lst.append(ins.InsType() )
                    lst.append(trdnbr )
                    lst.append(portid)
                    lst.append(ins.Name() )
                    lst.append(rst.Oid())
                    out.append(lst)

    fout = open(sfout, 'w')
    try:
        itm = ['Check', 'Area', 'Index', 'ResetDay', 'ResetType', 'Detail', 'InsType', 'TrdNbr', 'PortId', 'Insid', 'ResetNumber ']
        hdr = GenStrFromList('\t', itm)
        fout.write(hdr)

        #exl = get_exception_resets(dict)

        out.sort()
        for itm in out:
            #if itm not in exl:
            s = GenStrFromList('\t', itm)
            fout.write(s)

        fout.close()
    except Exception, e:
        fout.close()
        print 'Error in creating exceptions file:', e

    ael.log('Wrote secondary output to::: ' + sfout)

