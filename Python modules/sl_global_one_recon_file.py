"""-----------------------------------------------------------------------------
PURPOSE                 :  Creates a CSV report that is used by Intellimatch to
                           reconcile the Security Loan trades to Global One
DEPATMENT AND DESK      :  Prime Services Ops, Securities Lending
REQUESTER               :  Alistar Lawrence, Gasant Thulsie
DEVELOPER               :  Francois Truter
CR NUMBER               :  645661
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-08 593059    		Francois Truter            Initial Implementation
2011-04-04 645661    		Francois Truter            Added trade filter as input
2011-12-01 846490    		Rohan van der Walt         Update to correctly get G1Code from FParty if addinfo isnt in choicelist
2012-02-16 880858    		Jaysen Naicker	           Add columns Trade status and L/B
2012-04-20 CHNG0000144653	Jaysen Naicker	           Add column Current Trade Number and rounded Lender fee to 3 decimal places
2012-11-14 CHNG0000610025   Pavel Saparov              Removing condition to exclude Bonds and Index Linked Bonds for ABSA SECURITIES LENDING
2013-02-27 830992			Ntuthuko Matthews		   Added a _getAllInPrice function to be used when creating the report.
2013-04-18 000000           Edmundo Chissungo          Added additional fields to output file, nominal value as per cash flow table, LENDER FEE EXCL VAT and BORROWER FEE EXCL VAT
2016-08-16 3881184          Libor Svoboda              Use SPOT price for instruments with ETF underlyings.
2019-06-10 CHG1001877373    Marian Zdrazil             Adding 3 columns to the report: ref value, portfolio, mirror ref + use reference price for all instruments
2019-10-16 FAPE-85          Marian Zdrazil             Removing the _Ext_ task running temporarily in parallel to an old task - renaming task/TF/ASQL
"""

import acm
import csv
import sl_functions
import os
import time
import FRunScriptGUI
import ael
from PS_BrokerFeesRates import get_vat_for_date

space = acm.FCalculationSpaceCollection().GetSpace("FMoneyFlowSheet", acm.GetDefaultContext())


def _substringAfterLast(string, char):
    array = string.split(char)
    length = len(array)
    if length > 0:
        return array[length - 1]
    else:
        return ''


def _getCodeFromChoiceList(value):
    if not value:
        return None
    choiceList = None

    type = value[0]
    if type == 'F':
        choiceList = acm.FChoiceList.Select01("name = 'GlobalOneFunds'",
                                              'More than one choicelist returned for GlobalOneFunds')
    elif type == 'B':
        choiceList = acm.FChoiceList.Select01("name = 'GlobalOneBorrowers'",
                                              'More than one choicelist returned for GlobalOneBorrowers')
    elif type == 'L':
        choiceList = acm.FChoiceList.Select01("name = 'GlobalOneLenders'",
                                              'More than one choicelist returned for GlobalOneLenders')

    if choiceList:
        for item in choiceList.Choices():
            if item.Name() == value:
                return item.Description()
    else:
        FAParty = acm.FParty[value]
        if FAParty:
            return FAParty.AdditionalInfo().SL_G1PartyCode()
    return None


def _getMtmPrice(underlying, date):
    CALENDAR = acm.FCalendar['ZAR Johannesburg']
    mtm_date = sl_functions.GetMtMDate(date)
    if underlying.InsType() in ('Bond', 'IndexLinkedBond'):
        bond_mtm_price = underlying.UsedPrice(mtm_date, 'ZAR', 'SPOT_BESA')
        price = sl_functions.YTM_To_Price(underlying,
                                          CALENDAR.AdjustBankingDays(mtm_date, underlying.SpotBankingDaysOffset()),
                                          bond_mtm_price, True)
    elif underlying.InsType() == 'ETF':
        price = underlying.UsedPrice(mtm_date, 'ZAR', 'SPOT')
    else:
        price = underlying.MtMPrice(mtm_date, underlying.Currency(), 0)

    return price


def _getPrice(instrument, underlying):
    TODAY = acm.Time().DateNow()
    if instrument.AdditionalInfo().SL_CFD():
        price = _getMtmPrice(underlying, TODAY)
    else:
        price = instrument.RefPrice()

    return price * underlying.Quotation().QuotationFactor()


def _getNominal(trade):
    value = 0.00
    i = trade.Instrument()
    csc = acm.FStandardCalculationsSpaceCollection()

    tag = acm.CreateEBTag()
    for l in i.Legs():
        for cf in l.CashFlows():
            if cf.CashFlowType() in ['Fixed Rate', 'Fixed Rate Adjustable']:
                if (cf.StartDate() <= acm.Time().DateToday() <= cf.EndDate()):
                    value = cf.Calculation().Nominal(csc, trade, trade.Currency()).Number()
    return value


def _getAllInPrice(trade, underlying):
    instrument = trade.Instrument()

    TODAY = acm.Time().DateNow()
    if instrument.AdditionalInfo().SL_CFD() is not None:
        if underlying.InsType() in ['Bond', 'IndexLinkedBond']:
            return instrument.RefPrice()
    if instrument.AdditionalInfo().SL_CFD():
        price = _getMtmPrice(underlying, TODAY)
    else:
        price = trade.AllInPrice()

    return price * underlying.Quotation().QuotationFactor()


def _isNumber(object):
    try:
        if object != object:
            isNumber = False
        else:
            object = float(object)
            isNumber = True
    except:
        isNumber = False

    return isNumber


def _getFilepath(directory):
    return os.path.join(directory, 'ABCAP_FA_SBLRecon_Ext_%s.csv' % time.strftime('%Y%m%d%H%M%S'))


def WriteTrades(trades, filepath):
    dateFormatter = acm.FDateFormatter('dateFormatter')
    dateFormatter.FormatDefinition('%Y-%m-%d')
    with open(filepath, 'w') as csvFile:
        writer = csv.writer(csvFile, lineterminator='\n')
        writer.writerow([
            'Trade Number',
            'Trade Date',
            'Security Code',
            'Security ISIN',
            'Borrower Code',
            'Lender Code',
            'Lender Fee',
            'Quantity',
            'Rate',
            'Price',
            'VAT',
            'Trade status',
            'L/B',
            'Current Trade Number',
            'Lender Rate Excl Vat',
            'Borrower Rate Excl Vat',
            'Ref Value',
            'Portfolio',
            'Mirror Ref'
        ])

        today = acm.Time().DateNow()
        for trade in trades:
            vat_rate = get_vat_for_date(acm.Time().DateNow())
            instrument = trade.Instrument()
            underlying = instrument.Underlying()
            tradeAdditionalInfo = trade.AdditionalInfo()
            firstTrade = trade.SLPartialReturnFirstTrade() if trade.SLPartialReturnIsPartOfChain() else trade
            LorB = 'Lender' if trade.Quantity() < 0 else 'Borrower'

            if instrument.Legs()[0].event_date('LastEndDay') <= today and instrument.OpenEnd() == 'Terminated':
                pass
            else:

                lU = 0.000
                if _isNumber(tradeAdditionalInfo.SL_G1Fee2()) and instrument.AdditionalInfo().SL_VAT():
                    lU = '%.3f' % (tradeAdditionalInfo.SL_G1Fee2() / vat_rate)
                else:
                    lU = tradeAdditionalInfo.SL_G1Fee2()

                if trade.MirrorTrade():
                    mirrorRef = trade.MirrorTrade().Oid()
                else:
                    mirrorRef = ""

                writer.writerow([
                    firstTrade.Oid(),
                    dateFormatter.Format(firstTrade.Instrument().StartDate()),
                    _substringAfterLast(underlying.Name(), '/'),
                    underlying.Isin(),
                    _getCodeFromChoiceList(tradeAdditionalInfo.SL_G1Counterparty1()),
                    _getCodeFromChoiceList(tradeAdditionalInfo.SL_G1Counterparty2()),
                    '%.3f' % tradeAdditionalInfo.SL_G1Fee2() if _isNumber(tradeAdditionalInfo.SL_G1Fee2()) else None,
                    '%.0f' % abs(trade.QuantityInUnderlying()),
                    '%.3f' % instrument.Legs()[0].FixedRate(),
                    '%.2f' % _getAllInPrice(trade, underlying),
                    instrument.AdditionalInfo().SL_VAT(),
                    trade.Status(),
                    LorB,
                    trade.Oid(),
                    lU,
                    '%.3f' % (instrument.Legs()[0].FixedRate() / vat_rate if instrument.AdditionalInfo().SL_VAT() else
                              instrument.Legs()[0].FixedRate()),
                    '%.2f' % _getNominal(trade),
                    trade.Portfolio().Name(),
                    mirrorRef
                ])


tradeFilterSelectKey = 'TRADE_FILTER_SELECT'
prevTradeFilterSelect = True
tradeFilterKey = 'TRADE_FILTER'

tradeSelectionSelectKey = 'TRADE_SELECTION_SELECT'
prevTradeSelectionSelect = False
tradeSelectionKey = 'TRADE_SELECTION'

outputDirectoryKey = 'OUTPUT_DIRECTORY'
outputSelection = FRunScriptGUI.DirectorySelection()

boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()
boolDictDisplay.sort()

ael_gui_parameters = {
    'windowCaption': 'SL Global One Recon File'
}


def select_cb(index, fieldValues):
    global prevTradeFilterSelect
    global prevTradeSelectionSelect

    tradeFilterSelected = boolDict[fieldValues[0]]
    tradeSelectionSelected = boolDict[fieldValues[2]]

    if prevTradeFilterSelect != tradeFilterSelected:
        prevTradeFilterSelect = tradeFilterSelected
        tradeSelectionSelected = prevTradeSelectionSelect = not tradeFilterSelected
        fieldValues[2] = 'No' if tradeFilterSelected else 'Yes'

    elif prevTradeSelectionSelect != tradeSelectionSelected:
        prevTradeSelectionSelect = tradeSelectionSelected
        tradeFilterSelected = prevTradeFilterSelect = not tradeSelectionSelected
        fieldValues[0] = 'No' if tradeSelectionSelected else 'Yes'

    ael_variables[1][9] = tradeFilterSelected
    ael_variables[1][5] = tradeFilterSelected
    ael_variables[3][9] = tradeSelectionSelected
    ael_variables[3][5] = tradeSelectionSelected

    return fieldValues


# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [tradeFilterSelectKey, 'Use Trade Filter', 'string', boolDictDisplay, 'Yes', 1, 0,
     'Run report from the selected Trade Filter?', select_cb, 1],
    [tradeFilterKey, 'Trade Filter', 'FTradeSelection', None, None, 0, 1,
     'Trades Filter to be written to the recon file.', None, 1],
    [tradeSelectionSelectKey, 'Use Trade Selection', 'string', boolDictDisplay, 'No', 1, 0,
     'Run the report from the selected Trade Selection or Query Folder?', select_cb, 1],
    [tradeSelectionKey, 'Trade Selection', 'FTrade', None, None, 0, 1, 'Trades to be written to the recon file.', None,
     1],
    [outputDirectoryKey, 'Output Directory', outputSelection, None, outputSelection, 1, 1,
     'Directory where the file will be created.', None, 1]
]


def _raiseError(message):
    func = acm.GetFunction('msgBox', 3)
    func('Error', message, 0)


def ael_main(parameters):
    try:
        trades = None

        tradeFilterSelected = boolDict[parameters[tradeFilterSelectKey]]
        if tradeFilterSelected:
            tradeFilter = parameters[tradeFilterKey]
            if not tradeFilter:
                _raiseError('Please supply a value for mandatory parameter Trade Filter.')
                return
            tradeFilter = tradeFilter[0]
            trades = tradeFilter.Trades()
        else:
            trades = parameters[tradeSelectionKey]
            if not trades:
                print('No trades selected to report')

        outputDirectory = parameters[outputDirectoryKey]

        filepath = _getFilepath(outputDirectory.SelectedDirectory().Text())
        WriteTrades(trades, filepath)
        print('Wrote secondary output to:::' + filepath)
    except Exception, ex:
        print('Error while creating trade report for Global One recon:', str(ex))
