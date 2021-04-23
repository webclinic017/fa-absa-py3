
'''
Purpose                 : Market Risk feed files
Department and Desk     : IT
Requester:              : Natalie Austin
Developer               : Douglas Finkel
CR Number               : 264536,278978, 644358

Description             : Remove time zero cashflows from structured instruments
2015/11/25              : Brendan Bosman - MINT 412, MINT 416, MINT 417
'''

import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []

def get_StrCfCrvIndexXREF(l, cf):
    StrCfCrvIndexXREF  = ''
    float_rate = getattr(l, 'float_rate')
    cfspread = getattr(cf, 'spread')
    rtype = getattr(l, 'reset_type')
    lrp = getattr(l, 'reset_period')

    if float_rate:
        output = float_rate.insid
        if cfspread != 0 and rtype == 'Compound':
            StrCfCrvIndexXREF = 'SCI_' + output + '_' + str(
                getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(
                getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(
                l.reset_day_method)+MR_MainFunctions.CompoundConvention(cfspread, rtype, lrp)
        else:
            StrCfCrvIndexXREF = 'SCI_' + output + '_' + str(
                getattr(l, 'reset_type')) + '_' + str(getattr(l, 'reset_period.count')) + str(
                getattr(l, 'reset_period.unit')) + '_' + str(l.reset_day_offset) + str(
                l.reset_day_method)+MR_MainFunctions.CompoundConvention(cfspread, rtype, lrp)

    return StrCfCrvIndexXREF

def get_StrCfCoupRatePERD(l, cf):
    result  = ''
    float_rate = getattr(l, 'float_rate')
    cfspread = getattr(cf, 'spread')
    rtype = getattr(l, 'reset_type')
    lrp = getattr(l, 'reset_period')

    if float_rate:
        output = float_rate.insid
        if cfspread != 0 and rtype == 'Compound':
            result = MR_MainFunctions.DatePeriodUnit(lrp)
        else:
            result = 'simple'

    return result

# OPENFILE ##########################################################################################################

def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName

    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')

    outfile.close()
    outfileP.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):


    #DateValueDay = acm.GetFunction('DateValueDay',0)
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName

    Instrument = acm.FInstrument[i.insaddr]
#    Trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()

    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record

        BASFLAG             =       'BAS'
        HeaderName          =       'IRS Structured Instrument'
        OBJECT              =       'Structured InstrumentSPEC'
        TYPE                =       'Structured Instrument'

        NAME                =       MR_MainFunctions.NameFix(i.insid)

        if i.instype in ('Cap', 'Floor'):
            IDENTIFIER = 'insaddr_'+str(i.insaddr)+ '_CFEdited'
        else:
            IDENTIFIER = 'insaddr_'+str(i.insaddr)

        CurrencyCAL         =       ''
        CurrencyDAYC        =       ''
        CurrencyPERD        =       ''

        try:
            CurrencyUNIT        =       Instrument.Currency().Name()
        except:
            CurrencyUNIT        =       ''

        try:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       Instrument.MappedDiscountLink().Value().Link().YieldCurveComponent().Name()

        InitialIndxLvlFUNC  =       ''
        InitialIndxLvlUNIT  =       ''
        InitialIndxLvlVAL   =       '0'
        InitialIndxLvlSTRG  =       ''

        TheoModelXREF       =       'General Structured Instrument'
        MarketModelXREF     =       ''
        FairValueModelXREF  =       ''

        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, InitialIndxLvlFUNC, InitialIndxLvlUNIT, InitialIndxLvlVAL, InitialIndxLvlSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF))

        #Rollover record
        BASFLAG	                =	'rm_ro'
        HeaderName	        =	'IRS Structured Instrument : Structured CashFlow'
        ATTRIBUTE	        =	'Structured CashFlow'
        OBJECT	                =	'Structured InstrumentSPEC'

        Legs = i.legs()
        for l in Legs:

            StrCfCapMatDATE     =       ''
            StrCfCoupFctrNB     =       ''
            StrCfCoupRateCAL    =       ''
            StrCfCoupRateDAYC   =       ''
            StrCfCoupRatePERD   =       ''
            StrCfCoupRateVAL    =       ''
            StrCfCrvIndexXREF   =       ''
            StrCfCurRateVAL     =       ''
            StrCfDiscENUM       =       ''
            StrCfFwdEndDATE     =       ''
            StrCfFwdStartDATE   =       ''
            StrCfHidOddCpFLAG   =       ''
            StrCfInstrFctrVAL   =       ''
            StrCfInstrSprdVAL   =       ''
            StrCfPayCAL         =       ''
            StrCfPayDATE        =       ''
            StrCfPayDAYC        =       ''
            StrCfPayFctrVAL     =       ''
            StrCfPayPERD        =       ''
            StrCfPayTYPE        =       ''
            StrCfPayUNIT        =       ''
            StrCfPayVAL         =       ''
            StrCfProcXREF       =       ''
            StrCfProratedFLAG   =       ''
            StrCfRealEndDATE    =       ''
            StrCfRealStartDATE  =       ''
            StrCfRstDateDATE    =       ''
            StrCfTheoEndDATE    =       ''
            StrCfTheoStartDATE  =       ''

            for cf in l.cash_flows():

                # calc = cf.Calculation()
                StrCfCapMatDATE		=       ''
                StrCfCoupFctrNB		=       ''
                StrCfCoupRateCAL	=       ''
                StrCfCoupRateDAYC	=       ''
                StrCfCoupRatePERD	=       ''
                StrCfCoupRateVAL	=       ''
                StrCfCrvIndexXREF	=       ''
                StrCfCurRateVAL		=       ''
                StrCfDiscENUM		=       ''
                StrCfFwdEndDATE		=       ''
                StrCfFwdStartDATE	=       ''
                StrCfHidOddCpFLAG	=       ''
                StrCfInstrFctrVAL	=       ''
                StrCfInstrSprdVAL	=       ''
                StrCfPayCAL	        =       ''
                StrCfPayDATE        	=       ''
                StrCfPayUNIT        	=       ''
                StrCfPayDAYC        	=       ''
                StrCfPayFctrVAL     	=       ''
                StrCfPayPERD        	=       ''
                StrCfPayTYPE        	=       str(cf.type) + '/' + str(i.instype)
                StrCfPayVAL	        =       ''
                StrCfProcXREF       	=       ''
                StrCfProratedFLAG	=       ''
                StrCfRealEndDATE	=       ''
                StrCfRealStartDATE	=       ''
                StrCfRstDateDATE	=       ''
                StrCfTheoEndDATE	=       ''
                StrCfTheoStartDATE	=       ''

                if MR_MainFunctions.Datefix(cf.pay_day) > MR_MainFunctions.Datefix(ael.date_today()) and MR_MainFunctions.Datefix(cf.pay_day) != '':
                    if cf.type == 'Fixed Amount':

                        StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                        StrCfPayTYPE        =       'Notional'
                        StrCfPayUNIT        =       l.curr.insid

                        StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                        StrCfCrvIndexXREF   = 	    ''

                    elif cf.type == 'Float Rate':
                        try:
                            for reset in cf.resets():

                                StrCfCoupFctrNB     =       '0'
                                StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.daycount_method)
                                StrCfCoupRatePERD   =       get_StrCfCoupRatePERD(l, cf)
                                StrCfCoupRateVAL    =       str(cf.spread)

                                StrCfCrvIndexXREF  = get_StrCfCrvIndexXREF(l, cf)

                                StrCfCurRateVAL     =       str(reset.value / 100)
                                StrCfDiscENUM       =       'In Fine'

                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))
                                StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(cf.start_day)) #MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(cf.start_day))

                                StrCfHidOddCpFLAG   =       'FALSE'

                                StrCfInstrFctrVAL   =       '1'
                                if cf.float_rate_factor == '0':
                                    StrCfPayFctrVAL   =       ''
                                else:
                                    StrCfPayFctrVAL   = cf.float_rate_factor

                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.curr.insid

                                StrCfPayVAL         =       cf.nominal_amount()    # calc.Nominal(CalcSpace(cs), Trade).Number()
                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                                StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))

                        except:
                            for reset in cf.resets():
                                StrCfCoupFctrNB     =       '0'
                                StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.daycount_method)
                                StrCfCoupRatePERD   =       get_StrCfCoupRatePERD(l, cf)
                                StrCfCoupRateVAL    =       str(cf.spread)

                                StrCfCrvIndexXREF  = get_StrCfCrvIndexXREF(l, cf)

                                StrCfCurRateVAL     =       str(reset.value / 100)
                                StrCfDiscENUM       =       'In Fine'
                                StrCfFwdEndDATE     =       MR_MainFunctions.Datefix(str(cf.end_day))

                                StrCfFwdStartDATE   =       MR_MainFunctions.Datefix(str(cf.start_day)) #MR_MainFunctions.Datefix(str(cf.start_day))
                                StrCfHidOddCpFLAG   =       'FALSE'

                                StrCfInstrFctrVAL   =       '1'
                                if cf.float_rate_factor == '0':
                                    StrCfPayFctrVAL   =       ''
                                else:
                                    StrCfPayFctrVAL   = cf.float_rate_factor

                                StrCfInstrSprdVAL   =       '0'
                                StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                                StrCfPayTYPE        =       'Float'
                                StrCfPayUNIT        =       l.curr.insid

                                StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor    # calc.Nominal(CalcSpace(cs), Trade).Number()
                                StrCfProratedFLAG   =       'TRUE'
                                StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                                StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))

                                StrCfRstDateDATE    =       MR_MainFunctions.Datefix(str(cf.start_day))


                    elif cf.type not in ('Caplet', 'Digital Caplet', 'Digital Floorlet', 'Floorlet'):

                            StrCfCoupFctrNB     =       '0'
                            StrCfCoupRateCAL    =       ''
                            StrCfCoupRateDAYC   =       MR_MainFunctions.DayCountFix(l.daycount_method)
                            StrCfCoupRatePERD   =       'simple'
                            StrCfCoupRateVAL    =       str(cf.rate)
                            StrCfHidOddCpFLAG   =       'FALSE'
                            StrCfPayDATE        =       MR_MainFunctions.Datefix(str(cf.pay_day))
                            StrCfPayTYPE        =       'Fixed'
                            StrCfPayUNIT        =       l.curr.insid
                            StrCfPayVAL         =       cf.nominal_amount() # PayRecSign*i.contr_size*cf.nominal_factor
                            StrCfProratedFLAG   =       'TRUE'
                            StrCfRealEndDATE    =       MR_MainFunctions.Datefix(str(cf.end_day))
                            StrCfRealStartDATE  =       MR_MainFunctions.Datefix(str(cf.start_day))

                    if StrCfPayVAL != 0.0 and StrCfPayVAL != '':
                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, ATTRIBUTE, OBJECT, StrCfCapMatDATE, StrCfCoupFctrNB, StrCfCoupRateCAL, StrCfCoupRateDAYC, StrCfCoupRatePERD, StrCfCoupRateVAL, StrCfCrvIndexXREF, StrCfCurRateVAL, StrCfDiscENUM, StrCfFwdEndDATE, StrCfFwdStartDATE, StrCfHidOddCpFLAG, StrCfInstrFctrVAL, StrCfInstrSprdVAL, StrCfPayCAL, StrCfPayDATE, StrCfPayDAYC, StrCfPayFctrVAL, StrCfPayPERD, StrCfPayTYPE, StrCfPayUNIT, StrCfPayVAL, StrCfProcXREF, StrCfProratedFLAG, StrCfRealEndDATE, StrCfRealStartDATE, StrCfRstDateDATE, StrCfTheoEndDATE, StrCfTheoStartDATE))
        outfile.close()

    return i.insid

# WRITE - FILE ######################################################################################################



