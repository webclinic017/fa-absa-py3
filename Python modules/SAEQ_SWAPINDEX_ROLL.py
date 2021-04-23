import acm, re, ael
import NamespaceTimeFunctions

'''
Date                    : 2010-04-14, 2011-01-25, 2011-02-02
Purpose                 : -For EquityIndices consisting of only one swap, update all these swaps
                          so that the swaps start date and duration corresponds to the EquityIndex's naming convention.
                          -The Fixed rate on the swap must also be set equal to the par rate.
                          -These should only be updated on the last business day of the month.
                          -e.g.
                              SWAP_3Y5Y (EquityIndex)
                                  the underlying swap must be adjusted so that start date is 3 years in the future,
                                  and the swap duration must be 5 years.
                              SWAP_3M12Y will indicate the underlying swap starts in 3 Months and lasts for 12 Years
                              SWAP_10Y will indicate the underlying swap starts on the last business day of the current month
                              and lasts for 10 Years
                          -For FRA Indexes the rolling will be done on the 15th of February, May, August and November
Department and Desk     : Equity
Requester               : Shameer Sukha
Developer               : Rohan van der Walt, Herman Hoon
CR Number               : (ABITFA-110), 554580, 563721
'''

def parse(eqIdx):
    '''
    Returns dictionary containg forward start and duration of underlying FRA details
    '''
    result = {'fwd':0, 'fwdType':'0', 'dur':0, 'durType':'0'}
    spec = eqIdx.Name().split('_')[-1]
    fwdStartDurationPattern = r'([\d]+)([ymYM])([\d]+)([ymYM])'
    DurationPattern = r'([\d]+)([ymYM])'
    myMatch = re.match(fwdStartDurationPattern, spec)
    if myMatch:
        result['fwdType'] = myMatch.group(2)
        result['durType'] = myMatch.group(4)
        result['fwd'] = int(myMatch.group(1))
        result['dur'] = int(myMatch.group(3))
    else:
        myMatch = re.match(DurationPattern, spec)
        if myMatch:
            result['durType'] = myMatch.group(2)
            result['dur'] = int(myMatch.group(1))
        else:
            raise Exception('ERROR: Spec not understood: ' + str(spec))
    return result


def updateFRAs(equityInx, forced, today):
    nst = acm.Time()
    cal = acm.FCalendar['ZAR Johannesburg']

    if forced != 'Yes':
        today = nst.DateNow()

    todayYmd = nst.DateToYMD(today)
    todayYear = todayYmd[0]
    todayMonth = todayYmd[1]
    todayDay = todayYmd[2]

    # February, May, August, November
    validMonths = [2, 5, 8, 11]
    validDay = 15

    if todayMonth in validMonths:
        # create rolling dates
        rollingDate = nst.DateFromYMD(todayYear, todayMonth, validDay)
        adjRollingDate = cal.ModifyDate(cal, cal, rollingDate, 'Preceding')
        if todayDay == validDay:
            acm.Log('Adjused Rolling Date: %s' % (adjRollingDate))
        if today == adjRollingDate:
            print 'Using', adjRollingDate, 'as base date'
            calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
            rate = None
            FRA = None
            try:
                FRA = equityInx.Instruments()[0]
                print "Starting:", equityInx.Name(), FRA.Name()
                spec = parse(equityInx)
                startDate = cal.ModifyDate(cal, cal, NamespaceTimeFunctions.DateAddDeltaType(None, adjRollingDate, spec['fwd'], spec['fwdType']), 'Mod. Following')
                endDate = cal.ModifyDate(cal, cal, NamespaceTimeFunctions.DateAddDeltaType(None, startDate, spec['dur'], spec['durType']), 'Mod. Following')

                myClone = FRA.Clone()
                for leg in myClone.Legs():
                    leg.StartDate(startDate)
                    leg.EndDate(endDate)
                    leg.GenerateCashFlows(0)
                FRA.Apply(myClone)
                FRA.Commit()

                rate = FRA.Calculation().ParRate(calc_space)
                print " Par Rate:", rate
                if hasattr(rate, 'Number'):
                    rate = rate.Number()
                theleg = FRA.FirstFloatLeg()
                myLeg = theleg.Clone()
                myLeg.FixedRate(rate * 100)
                myLeg.GenerateCashFlows(0)
                theleg.Apply(myLeg)
                theleg.Commit()

            except Exception, e:
                print '\nFAILED:', equityInx.Name() if FRA else 'Could not find IRSwap', "Par Rate:", rate, '\nError Message:', e
            print 'Done'
            print " <--Finished"


def updateSwaps(equityInx, forced=False):
    '''
    forced = False -> will only update if today is last business day of month.
    forced = True -> will use last business day of previous month to update swaps.
    '''
    nst = acm.Time()
    baseDate = nst.DateNow()
    if forced == 'Yes':
        baseDate = NamespaceTimeFunctions.GetLastBusinessDayOfMonth(None, nst.DateAddDelta(baseDate, 0, -1, 0))
    if baseDate == NamespaceTimeFunctions.GetLastBusinessDayOfMonth(None, baseDate):
        print 'Using', baseDate, 'as base date'
        calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        rate = None
        IRSwap = None
        try:
            IRSwap = equityInx.Instruments()[0]
            print "Starting:", equityInx.Name(), IRSwap.Name(),
            spec = parse(equityInx)
            start = NamespaceTimeFunctions.DateAddDeltaType(None, baseDate, spec['fwd'], spec['fwdType'])
            end = NamespaceTimeFunctions.DateAddDeltaType(None, start, spec['dur'], spec['durType'])
            myClone = IRSwap.Clone()
            for leg in myClone.Legs():
                leg.StartDate(start)
                leg.EndDate(end)
                leg.RollingPeriodBase(start)
                leg.GenerateCashFlows(0)
            IRSwap.Apply(myClone)
            IRSwap.Commit()
            rate = IRSwap.Calculation().ParRate(calc_space)
            print " Par Rate:", rate
            if hasattr(rate, 'Number'):
                rate = rate.Number()
            theleg = IRSwap.FirstFixedLeg()
            myLeg = theleg.Clone()
            myLeg.FixedRate(rate * 100)
            myLeg.GenerateCashFlows(0)
            theleg.Apply(myLeg)
            theleg.Commit()
            print " <--Finished"
        except Exception, e:
            print '\nFAILED:', equityInx.Name(), IRSwap.Name() if IRSwap else 'Could not find IRSwap', "Par Rate:", rate, '\nError Message:', e
        print 'Done'


def cbForced(index, fieldValues):
    ael_variables[2][9] = fieldValues[index] == 'Yes'
    return fieldValues

def listOfInstruments():
    query = acm.CreateFASQLQuery('FIndex', 'AND')
    op = query.AddOpNode('AND')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', '.*_([0-9]+[y,m,Y,M])+')
    return query.Select()


INCEPTION = ael.date('1970-01-01')
TODAY = ael.date_today()
FIRSTOFYEAR = TODAY.first_day_of_year()
FIRSTOFMONTH = TODAY.first_day_of_month()
PREVBUSDAY = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
TWOBUSDAYSAGO = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)
TWODAYSAGO = TODAY.add_days(-2)
YESTERDAY = TODAY.add_days(-1)

ReportDateList = {'Inception':INCEPTION.to_string(ael.DATE_ISO), \
                    'First Of Year':FIRSTOFYEAR.to_string(ael.DATE_ISO), \
                    'First Of Month':FIRSTOFMONTH.to_string(ael.DATE_ISO), \
                    'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO), \
                    'TwoBusinessDaysAgo':TWOBUSDAYSAGO.to_string(ael.DATE_ISO), \
                    'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO),
                    'Yesterday':YESTERDAY.to_string(ael.DATE_ISO),
                    'Today':TODAY.to_string(ael.DATE_ISO)}

ael_variables = [['Instruments', 'Instruments', acm.FEquityIndex, listOfInstruments(), None, 1, 1, 'All indexes to roll', None, 1],
                 ['forced', 'Force run', 'string', ['No', 'Yes'], 'Yes', 1, 0, 'Force this script to run. For SWAP Indeces it will use the last business day of the previous month as base date', cbForced, 1],
                 ['date', 'Date of run', 'string', ReportDateList.keys(), TODAY.to_string(ael.DATE_ISO), 0, 0, 'For FRA Indeces force the script to run on this specific date.', None, 1]]

ael_gui_parameters = { 'windowCaption':'Swap Index Rolling'}

def ael_main(dict):
    # if dict['date']
    for ins in dict['Instruments']:
        name = ins.Name().split('_')[0]
        if name == 'ZAR/SWAP':
            updateSwaps(ins, forced=dict['forced'])
        else:
            updateFRAs(ins, dict['forced'], dict['date'])

    print "Completed Successfully ::"
