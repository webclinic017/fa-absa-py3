"""Generate report with top 20 SARB rates.

This script generates a report with the top 20 SARB rates, plus additional
related reports.

Department: Treasury
Requester:  Shira Zadikov
Revised by: Mike Schaefer


History
=======

2014-11-11 Fancy Dire/Bhavnisha Sarawan ABITFA-1451/CHNG0003118255: Initial implementation.
2016-02-17 Vojtech Sidorin              ABITFA-4025: Fix calculating the top 20 rates; improve coding style.
"""

import time
from itertools import groupby
from operator import itemgetter
import csv

import acm
import ael

import at
import at_calculation_space as acs


ael_variables = at.ael_variables.AelVariableHandler()
ael_variables.add_input_file(
        name='inputFile',
        label='Input File',
        mandatory=1,
        default='Party_Definition_codes.csv'
        )
ael_variables.add_directory(
        name='inputPath',
        label='Input Path',
        mandatory=1,
        default='/apps/frontnt/REPORTS/BackOffice/Atlas-End-Of-Day/SABOR/'
        )
ael_variables.add_directory(
        name='outputPath',
        label='Output Path',
        mandatory=1,
        default='/services/frontnt/Task/'
        )
ael_variables.add(
        name='counterparties',
        label='Counterparties',
        mandatory=1,
        default=','.join([
            'AFRICAN BANK LTD',
            'BIDVEST BANK LTD',
            'CAPITEC BANK LIMITED',
            'FIRSTRAND BANK LTD',
            'GRINDROD BANK LTD',
            'INVESTEC BANK LTD',
            'NEDBANK LIMITED',
            'SASFIN BANK LTD',
            'STANDARD BANK SA',
            'UBANK LTD',
            'ALBARAKA BANK LTD',
            'HABIB OVERSEAS BANK',
            'HBZ BANK LIMITED',
            'MERCANTILE  BANK LTD',
            'THE SA BANK OF ATHENS',
            'CITIBANK NA SOUTH AFRICA BRANCH',
            'BANK OF BARODA LTD',
            'BANK OF CHINA LTD',
            'BANK OF INDIA',
            'BNP PARIBAS SA FRANCE',
            'BNP PARIBAS SA LONDON',
            'CHINA CONSTRUCTION BANK CORPORATION',
            'CITIBANK NA',
            'DEUTSCHE BANK AG JHB',
            'HSBC BANK PLC JOHANNESBURG',
            'JP MORGAN CHASE BANK JOHANNESBURG',
            'SOCIETE GENERALE JOHANNESBURG',
            'STANDARD CHARTERED JOHANNESBURG',
            'STATE BANK OF INDIA',
            'STANDARD CHARTERED BANK JOHANNESBU',
            ]),
        collection=acm.FParty.Select('type = "Counterparty"'),
        multiple=1
        )
ael_variables.add(
        name='portfolios',
        label='Portfolios',
        mandatory=1,
        default=','.join([
            'Call_2474',
            'Call_7744 CRP Dp DBN',
            'Call_5617 CIB Dp CAPE',
            'Call_5616 CIB Dp DBN',
            'Call_5615 CIB Dp GTNG',
            'Call_5615 DP PRETORIA',
            'Call_7744 CRP Dp CAPE',
            'Call_7744 CRP Dp GAUTENG',
            'Call_7744',
            ]),
        collection=acm.FPhysicalPortfolio.Select(''),
        multiple=1
        )
ael_variables.add(
        name='interbank_portfolios',
        label='Interbank Portfolios',
        mandatory=1,
        default='LIABILITIES 2474',
        collection=acm.FPhysicalPortfolio.Select(''),
        multiple=1
        )
ael_variables.add(
        name='interbankLimit',
        label='Interbank Limit (millions)',
        mandatory=1,
        default=1
        )
ael_variables.add(
        name='tradeStatuses',
        label='Trade Statuses',
        mandatory=1,
        default=','.join([
            'FO Confirmed',
            'BO Confirmed',
            'BO-BO Confirmed',
            ]),
        collection=acm.FEnumeration["enum(TradeStatus)"].Enumerators(),
        multiple=1
        )
ael_variables.add(
        name='currentTrades',
        label='Current Trades Expire:',
        mandatory=1,
        default='Today',
        collection=["Today", "Tomorrow"],
        multiple=0,
        alt="Morning runs: expire today. Afternoon: expire tomorrow."
        )


def log(msg):
    print("%s - %s" %(time.strftime("%Y-%m-%d %H:%M:%S"), msg))


def _group_by_party_code(trades):
    """Group trades by party code.

    Generator that groups trades by the party code, and computes the weighted
    rate (weighted by the balance) and the total balance.  The weighted rate is
    rounded to 3 decimal places.

    Arguments:
    trades -- iterable of (rate, party_code, balance, trade_oid)

    Yields: party code, weighted rate, total balance
    """
    # Sort the trades so that groupby works as expected.
    sorted_trades = sorted(trades, key=itemgetter(1))
    for party_code, party_trades in groupby(sorted_trades, key=itemgetter(1)):
        total_balance = 0.
        weighted_sum = 0.
        for trade in party_trades:
            total_balance += trade[2]
            weighted_sum += trade[0]*trade[2]
        weighted_rate = round(weighted_sum/total_balance, 3)
        yield party_code, weighted_rate, total_balance


def _format_asql_list(iterable):
    """Format iterable into ASQL list ready for direct use in query.

    >>> trade_statuses = ["Simulated", "Void", "FO Confirmed"]
    >>> _format_asql_list(trade_statuses)
    "('Simulated','Void','FO Confirmed')"
    """
    quoted = ["'{0}'".format(i) for i in iterable]
    return "({0})".format(",".join(quoted))


def _get_call_trades(portfolios, trade_statuses):
    """Get relevant call trades."""
    query = """
        SELECT
            t.trdnbr
        FROM
            Trade t,
            Party pty,
            Portfolio prf,
            Instrument i,
            AdditionalInfoSpec ais,
            AdditionalInfo ai
        WHERE
            pty.ptynbr = t.counterparty_ptynbr
            and prf.prfnbr = t.prfnbr
            and t.insaddr = i.insaddr
            and i.instype = 'Deposit'
            and t.status in {trade_statuses}
            and prf.prfid in {portfolios}
            and t.trdnbr = ai.recaddr
            and ais.field_name = 'Funding Instype'
            and ai.addinf_specnbr = ais.specnbr
            and ai.value in (
                'Call Deposit NonDTI',
                'Call Deposit DTI',
                'Call Loan DTI',
                'Call Loan NonDTI'
                )
        """.format(
                trade_statuses=_format_asql_list(trade_statuses),
                portfolios=_format_asql_list(portfolios)
                )
    call_trades = ael.asql(query)[1][0]
    log("%s call trade(s) selected." %len(call_trades))
    return call_trades


def _get_other_trades(interbank_portfolios, counterparties, trade_statuses):
    """Get other relevant (non-call) trades."""
    query = """
        SELECT
            t.trdnbr
        FROM
            Trade t,
            Party pty,
            Portfolio prf,
            Instrument i
        WHERE
            pty.ptynbr = t.counterparty_ptynbr
            and prf.prfnbr = t.prfnbr
            and t.insaddr = i.insaddr
            and i.instype = 'Deposit'
            and t.status in {trade_statuses}
            and prf.prfid in {portfolios}
            and pty.ptyid in {counterparties}
        """.format(
                trade_statuses=_format_asql_list(trade_statuses),
                portfolios=_format_asql_list(interbank_portfolios),
                counterparties=_format_asql_list(counterparties)
                )
    other_trades = ael.asql(query)[1][0]
    log("%s other trade(s) selected." %len(other_trades))
    return other_trades


def _faQuery(partyDictn, portfolios, counterparties, interbank_portfolios,
            interbank_limit, tradeStatuses, currentTrades):
    '''
    This method extracts the trades based on a filter
    and calculates the Balance and retrieves the Rate
    '''
    today = acm.Time.DateToday()
    # Cater for tasks which are run early in the morning, assuming that
    #   trades expiring later in the day are still current. Alternatively,
    #   tasks which run in the afternoon assume that trades expiring on the
    #   day of execution are NOT current.
    if (currentTrades == "Tomorrow"):
        today = acm.Time.DateAddDelta(today, 0, 0, 1)
    ZAR_calendar = acm.FCalendar['ZAR Johannesburg']
    prevBusDay = ZAR_calendar.AdjustBankingDays(today, -1)
    usedPrice = acm.FInstrument['ZAR-REPO'].UsedPrice(prevBusDay, None, None)
    call_trades = _get_call_trades(portfolios, tradeStatuses)
    other_trades = _get_other_trades(interbank_portfolios,
        counterparties, tradeStatuses)
    all_trades = call_trades + other_trades
    missingData = acm.FDictionary()
    faDictn = acm.FDictionary()
    interBank_fund_nonrepo = acm.FDictionary()
    interBank_fund_repo = acm.FDictionary()
    interBank_lend_nonrepo = acm.FDictionary()
    interBank_lend_repo = acm.FDictionary()
    rateException = acm.FDictionary()

    for trade in all_trades:
        t = acm.FTrade[trade[0]]
        ins = t.Instrument()
        amountBalance = _getAmountBalance(ins, t, prevBusDay)

        if amountBalance != 0:
            faList = []
            partyName = t.Counterparty().StringKey()
            trade_portfolio = t.Portfolio().Name()
            isTrading = not(t.Counterparty().NotTrading())
            currentRate = _getCurrentRate(ins, t, prevBusDay)

            # Checking if the Rate is lower or above the Repo rate by 50 basis points
            if ((currentRate < (usedPrice - 0.5)) or (currentRate > (usedPrice + 0.5))) \
                and (abs(amountBalance) >= 50e6) \
                and (trade_portfolio not in interbank_portfolios) \
                and t.AdditionalInfo().Funding_Instype() in ['Call Deposit NonDTI', 'Call Deposit DTI']:
                rateDiff = currentRate - usedPrice
                rateException[t.Oid()] = [t.Oid(), partyName, currentRate, abs(amountBalance), usedPrice, rateDiff]

            if partyName in partyDictn \
                and isTrading \
                and trade_portfolio not in interbank_portfolios \
                and not t.Counterparty().Name().startswith("SARB") \
                and (t.Counterparty().Name() not in counterparties) \
                and t.AdditionalInfo().Funding_Instype() in ['Call Deposit NonDTI', 'Call Deposit DTI']:
                faList = [abs(amountBalance), currentRate, partyDictn[partyName]]
                faDictn[t.Oid()] = faList

            elif (abs(amountBalance) >= interbank_limit) \
                and not t.Counterparty().Name().startswith("SARB") \
                and t.Counterparty().Name() in counterparties:
                start_date = ins.StartDate()
                end_date = ins.EndDate()
                end_less_start = ZAR_calendar.BankingDaysBetween(end_date, start_date)
                end_less_today = ZAR_calendar.BankingDaysBetween(today, end_date)
                overnight_trade = (end_less_start == 1)
                current_trade = (end_less_today == 0)

                # Select current overnight/weekend trades only:
                if (overnight_trade and current_trade) or (ins.OpenEnd() == 'Open End'):
                    call_float_spread = currentRate - usedPrice
                    # Funding at other than repo
                    if (amountBalance >= 0 and call_float_spread != 0):
                        interBank_fund_nonrepo[t.Oid()] = [t.Oid(), partyName, currentRate, abs(amountBalance)]
                    # Funding at repo
                    elif (amountBalance >= 0 and call_float_spread == 0):
                        interBank_fund_repo[t.Oid()] = [t.Oid(), partyName, currentRate, abs(amountBalance)]
                    # Lending at other than repo
                    elif (amountBalance < 0 and call_float_spread != 0):
                        interBank_lend_nonrepo[t.Oid()] = [t.Oid(), partyName, currentRate, abs(amountBalance)]
                    # Lending at repo
                    else:
                        interBank_lend_repo[t.Oid()] = [t.Oid(), partyName, currentRate, abs(amountBalance)]

            #amountBalance >= 1e3 Eliminates trades with nominal values close to zero
            if partyName not in partyDictn \
                and isTrading \
                and (abs(amountBalance) >= 1e3) \
                and (trade_portfolio not in interbank_portfolios) \
                and t.AdditionalInfo().Funding_Instype() in ['Call Deposit NonDTI', 'Call Deposit DTI']:
                    missingData[t.Oid()] = [t.Oid(), partyName, currentRate, abs(amountBalance)]

    return faDictn, missingData, interBank_fund_nonrepo, rateException, \
            interBank_fund_repo, interBank_lend_nonrepo, interBank_lend_repo


def _getCurrentRate(ins, t, prevBusDay):
    if ins.OpenEnd() == 'Open End':
        currentRate = _getColumn(t, 'PS Current Rate')
    elif ins.Legs()[0].LegType() == 'Fixed':
        currentRate = ins.Legs()[0].FixedRate()
    elif ins.Legs()[0].LegType() == 'Float':
        currentRate = ins.Legs()[0].Spread() + \
            ins.Legs()[0].FloatRateReference().UsedPrice(prevBusDay, None, None)
    return currentRate


def _getAmountBalance(ins, t, prevBusDay):
    if ins.OpenEnd() == 'Open End':
        amountBalance = _getColumn(t, 'PS Deposit Balance')
    else:
        amountBalance = t.Premium()
    return amountBalance


def _getColumn(trade, column):
    value = acs.calculate_value('FPortfolioSheet', trade, column)
    if hasattr(value, 'Number'):
        value = value.Number()
    return value


def _rateDictn(mergedDictn):
    '''
    Returns a dictionary with Rate as a key and Party code, Balance and
    Trade number as the value list.
    '''

    listTemp = []
    for trd in mergedDictn.Keys():  # t.Oid()
        if mergedDictn[trd].Size() == 3:
            rate = mergedDictn[trd][1]  # rate
            # Create a tuple with (Rate, Party, Balance, TradeID)
            listTemp.append(tuple([rate, mergedDictn[trd][2], mergedDictn[trd][0], trd]))
    return listTemp


def _sumBalances(ratesDictn, outputFileNew):
    '''
    Sum the balance for the same party in each rate and remove the balances
    below 50m
    '''
    ptyTradeDict = {}

    for trd in ratesDictn:
        ptyTradeDict.setdefault(trd[1], []).append(trd[3])  # {Cntpty# -->[t.oid, t.oid,t.oid ....]}

    tempFinal = []

    for party_code, weighted_rate, total in _group_by_party_code(ratesDictn):
        if total >= 5e7:
            tempFinal.append((weighted_rate, party_code, total, ptyTradeDict[party_code]))

    # Sort the finalList in decending order by Rate and Balance
    finalList = sorted(tempFinal, key=itemgetter(0, 2), reverse=True)

    outfile = open(outputFileNew, 'w')
    outfile.write('\nAll the trades with rates 4.8 and above \n')
    outfile.write('%s, %s, %s, %s\n' % ('Rate', 'Party number', 'Balance', 'Trade_ID'))

    #  Printing all Parties where the rate is Greater than 4.7
    for rate in finalList:
        if rate[0] >= 4.8:
            outfile.write('%s, %s, %s, %s\n' % (rate[0], rate[1], rate[2], rate[3]))
    outfile.close()
    return finalList


def _missingPartyCode(temp_dict, missingData):
    '''
    This method checks if all the trades with missing party codes
    would have been in the Top20, and keeps them in the dictionary
    to be reported to business.
    '''
    keyList = sorted(temp_dict)
    missingDataSize = missingData.Size()

    if missingDataSize > 0:
        for i in missingData.Keys():
            # comparing the lowest rate to the rates of the missing data
            if missingData[i][2] < keyList[0][0]:
                del missingData[i]
    return missingData


def _workOutRate(Top20):
    '''
    Work out the rate based on the Top 20
    '''
    sumTotal = 0.0
    rateTotal = 0.0

    for key in Top20:
        sumTotal += key[2]
        rateTotal += (key[2] * (key[0]/100))
    if sumTotal != 0:
        rate = round((rateTotal/sumTotal)*100, 4)
    else:
        sumTotal = 0
        rateTotal = 0
        rate = 0
    return sumTotal, rateTotal, rate


def _createDataFile(rate, missingData, missingPartyCode, Top20, outputFile):
    '''
    This method will  create a file with the Top20 rates and the missing
    party codes for business to update.
    '''
    outfile = open(outputFile, 'w')

    outfile.write('The top 20 accounts used to calculate Weighted average: \n')
    outfile.write('%s, %s, %s, %s, %s\n' % ('\t', 'Party Name', 'Rate', 'Summed Balance', 'R mil'))

    countTop20 = 1
    for rateKey in Top20:
        amountMil = round(rateKey[2]/1000000, 0)
        line = '%s, %s, %s, %s, %s\n' % (countTop20, rateKey[1], rateKey[0], rateKey[2], amountMil)
        print(line)
        outfile.write(line)
        countTop20 += 1

    amountMil = round(rate[0]/1000000)
    line = '%s, %s, %s, %s, %s\n' % ('\t', 'Weighted Average', rate[2], rate[0], amountMil)
    print(line)
    outfile.write(line)

    outfile.write('\nThese trades do not have a counterparty code defined \n')
    outfile.write('%s, %s, %s, %s\n' % ('Trade Number', 'Party Name', 'Rate', 'Nominal'))
    for key in missingData.Keys():
        outfile.write('%s, %s, %s, %s\n' % (key, missingData[key][1], missingData[key][2], missingData[key][3]))

    if missingPartyCode.Size() > 0:
        outfile.write('\nThese trades should have been included in the top20 trades \n')
        outfile.write('%s, %s, %s, %s\n' % ('Trade Number', 'Party Name', 'Rate', 'Nominal'))
        for key in missingPartyCode.Keys():
            if missingPartyCode[key][3] >= 5e7:
                outfile.write('%s, %s, %s, %s\n' % (key, missingPartyCode[key][1], missingPartyCode[key][2], missingPartyCode[key][3]))
    else:
        outfile.write('\nNo missing trade information belongs in the top20 \n')
    outfile.close()


def _import_party_codes(filename):
    """Import party codes from a csv file.

    Expecting a header row, then each line should contain Party Name and Party
    Code.
    """
    party_names_codes = {}
    with open(filename, "rb") as f:
        reader = csv.reader(f)
        reader.next()  # Skip first (header) line.
        for line in reader:
            if len(line) != 2:
                msg = ("File '{0}': Unexpected line {1}. Expecting two values "
                       "separated by a comma: Party Name, Party Code."
                       .format(filename, reader.line_num))
                log(msg)
                raise Exception(msg)
            party_name = line[0].strip()
            party_code = line[1].strip()
            if (party_name in party_names_codes and
                    party_code != party_names_codes[party_name]):
                # Redefined party code.
                msg = ("Warning: File '{0}': Code for party '{1}' redefined "
                       "on line {2}."
                       .format(filename, party_name, reader.line_num))
                log(msg)
                party_names_codes[party_name] = party_code
            else:
                party_names_codes[party_name] = party_code
    return party_names_codes


def _exportFile(data, exportFile, weighted_rate, section, excep=0):
    '''
    This method is used to export the Interbank trades for business to check.
    '''

    with open(exportFile, 'a') as outfile:
        # Writing the column headers
        if excep == 1:
            outline = 'Trade Number, Party Name, Rate, Amount, Repo Rate, Difference\n'
        else:
            outline = 'Trade Number, Party Name, Rate, Amount\n'

        outfile.writelines(outline)
        outfile.writelines(section)
        for key in data.Keys():
            if excep == 1:
                outline = '%s, %s, %s, %s, %s, %s\n' % (key, data[key][1], data[key][2], data[key][3], data[key][4], data[key][5])
            else:
                outline = '%s, %s, %s, %s\n' % (key, data[key][1], data[key][2], data[key][3])
            outfile.writelines(outline)
        if weighted_rate:
            outline = '%s, %s, %s\n' % ('\t', 'Weighted Average', weighted_rate)
            outfile.writelines(outline)
        outfile.writelines('\t,\t,\t,\t\n')

def _interbankTop20(input_dict):
    '''
    Change the format of the input dictionary (faDictn) so that the existing function (_workOutRate)
        can be used to calculate the weighted average for SARB_Interbank.
    '''
    interbank_list = []
    for key in input_dict:
        if input_dict[key][2]:
            interbank_tuple = (abs(input_dict[key][2]), input_dict[key][1], input_dict[key][3], [key])
        else:
            interbank_tuple = (0, input_dict[key][1], input_dict[key][3], [key])
        interbank_list.append(interbank_tuple)
    return _workOutRate(interbank_list)


def ael_main(parameter):
    inputFile = parameter['inputPath'].AsString() + parameter['inputFile'].AsString()
    outputFile = parameter['outputPath'].AsString() + 'SARB_Top20_Rate.csv'
    outputFileNew = parameter['outputPath'].AsString() + 'SARB_AllData.csv'
    interBankFile = parameter['outputPath'].AsString() + 'SARB_Interbank.csv'
    rateExcepFile = parameter['outputPath'].AsString() + 'SARB_Exceptions.csv'
    counterparties = list(parameter['counterparties'])
    portfolios = list(parameter['portfolios'])
    tradeStatuses = list(parameter['tradeStatuses'])
    interbank_portfolios = list(parameter['interbank_portfolios'])
    currentTrades = parameter['currentTrades']
    interbank_limit = int(parameter['interbankLimit'])
    # Limit is in millions:
    interbank_limit *= 1e6

    log('Start SARB Top20 Selection\n')

    # Import the Party three letter codes and create a dict
    partyDictn = _import_party_codes(inputFile)
    log('Party Codes Imported...\n')

    # Use the filter to pull trade details
    # Return faDictn, missingData, interBank_fund_nonrepo, rateException, \
    #        interBank_fund_repo, interBank_lend_nonrepo, interBank_lend_repo
    faDictn = _faQuery(partyDictn, portfolios, counterparties, \
                    interbank_portfolios, interbank_limit, \
                    tradeStatuses, currentTrades)
    log('Trades Retrieved...\n')

    # Save the dictionary with rate as a key, and party and balance as the values
    ratesDictn = _rateDictn(faDictn[0])
    log('Rates saved to Dictionary...\n')

    # Sum the balance for the same party in each rate and remove the balances below 50m
    summedBalances = _sumBalances(ratesDictn, outputFileNew)

    # Select the top 20
    Top20 = summedBalances[:20]
    log('Retrieved the Top20...\n')

    missingPartyCode = _missingPartyCode(Top20, faDictn[1])

    # Export the InterBank trades
    if faDictn[2]:
        sumTotal, rateTotal, rate = _interbankTop20(faDictn[2])
        section = 'Bank funding from:(other than @ repo)\n'
        _exportFile(faDictn[2], interBankFile, rate, section) # Funding at other than repo
        sumTotal, rateTotal, rate = _interbankTop20(faDictn[4])
        section = 'Bank funding from:(@ repo)\n'
        _exportFile(faDictn[4], interBankFile, rate, section) # Funding at repo
        sumTotal, rateTotal, rate = _interbankTop20(faDictn[5])
        section = 'Bank lending to:(other than @ repo)\n'
        _exportFile(faDictn[5], interBankFile, rate, section) # Lending at other than repo
        sumTotal, rateTotal, rate = _interbankTop20(faDictn[6])
        section = 'Bank lending to:(@ repo)\n'
        _exportFile(faDictn[6], interBankFile, rate, section) # Lending at repo
    else:
        _exportFile(faDictn[2], interBankFile, 0, '')

    # Export the Repo Rate Exceptions
    section = ''
    _exportFile(faDictn[3], rateExcepFile, None, section, excep=1)

    # Work out the rate for submission
    rate = _workOutRate(Top20)

    _createDataFile(rate, faDictn[1], missingPartyCode, Top20, outputFile)

    log('\nSARB Top20 Selection Completed...\n')
    log('Wrote secondary output for Top20 to: %s' % outputFile)
    log('Wrote secondary output for Interbank trades to: %s' % interBankFile)
    log('Wrote secondary output for Repo Rate Exceptions to: %s' % rateExcepFile)
    log('Wrote secondary output for All trades to: %s' % outputFileNew)
