"""----------------------------------------------------------------------------
PROJECT                 :   SBL ACS Migration
PURPOSE                 :   Generate security loan trade messages to be sent
                            to Global One
DEPATMENT AND DESK      :   Prime Services, Securities Lending
REQUESTER               :   Linda Breytenbach
DEVELOPER               :   Anil Parbhoo
CR NUMBER               :   701495

HISTORY
===============================================================================
Date       Change no Developer              Description
-------------------------------------------------------------------------------
2010-10-15 450056    Paul Jacot-Guillarmod  Initial Implementation
2010-10-19 468027    Francois Truter        Updated settlement date and trade
                                            date mappings for full returns
2010-10-19 468171    Francois Truter        Added confirmation reports
2011-01-06 531986    Francois Truter        Added check for 2 timstamps
2011-04-07 634517    Rohan vd Walt          Do not exclude VAT from fee when
                                            VAT checkbox isn't checked.
                                            Added MinimumFeeValue
                                            to upload file.
2011-07-07 701495    Anil Parbhoo           pass the bond AIP to G1
                                            in the case where the underlying
                                            to the security loan is a bond
                                            or an indexed linked bond
2011-11-01 816158    Rohan vd Walt          Trade Category
2012-10-16 533770    Anwar Banoo            Removed the restriction
                                            of only sending a trade
                                            down to g1 twice
2013-05-09 999016    Peter Basista          Feed SL Dividend Factor
                                            to Global One.
2014-05-06 1798994	 Manan Ghosh			Removed the condition the to filter out trades with mirror trades due to
											due to enhancement in trade booking for SBL desk
2018-10-02 CHG1001031614  O. Bahounek       Convert trade numbers to HEX numbers 8 chars long.
                                            G1 accepts only 8 chars numbers (should change in future).
2020-01-06 CHG0073632    Sihle Gaxa         Change SL_SWIFT flag from instrument to trade
----------------------------------------------------------------------------"""

import os

import acm

import FRunScriptGUI
import sl_functions
from PS_BrokerFeesRates import get_vat_for_date
from sl_global_one_upload_file import GlobalOneStatus
from sl_global_one_upload_file import GlUploadFile
from sl_global_one_upload_file import LenderModuleTrade
from sl_global_one_upload_file import PostingType
from sl_global_one_upload_file import ReturnUpdateFlag
from sl_global_one_upload_file import SecurityCodeType
from sl_global_one_upload_file import TransactionType

CALENDAR = acm.FCalendar['ZAR Johannesburg']


def get_hex_len8_nbr(nbr):
    """Return 8 chars long hex number"""
    h1 = hex(nbr)  # "0x1234567"
    h2 = h1[2:]  # "1234567"  
    if len(h2) == 7:
        h2 = "0" + h2  # "01234567"
    return h2.upper()


def process_trade_nbr(trdnbr):
    if len(str(trdnbr)) > 8:
        trdnbr = get_hex_len8_nbr(trdnbr)
    return str(trdnbr)


def isParentOfPartialReturn(trade):
    instrument = trade.Instrument()
    if (instrument.OpenEnd() == 'Terminated') and (
            trade.Oid() < trade.ConnectedTrdnbr()):
        return True
    else:
        return False

def isPartialReturn(trade):
    return trade.SLPartialReturnIsPartOfChain()

def isFullReturn(trade):
    instrument = trade.Instrument()
    if (instrument.OpenEnd() == 'Terminated') and (
            trade.Oid() >= trade.ConnectedTrdnbr()):
        return True
    else:
        return False

def getRecordType(trade):
    instrument = trade.Instrument()

    if not trade.SLGlobalOneTimeStampExists():
        if isPartialReturn(trade):
            recordType = 'PartialReturn'
        else:
            recordType = 'Insert'

    elif (trade.SLGlobalOneTimeStamp() <
            max(instrument.UpdateTime(), trade.UpdateTime())):
        if isFullReturn(trade):
            recordType = 'FullReturn'
        else:
            recordType = None
    else:
        recordType = None

    return recordType

def ReturnedQuantity(trade):
    instrument = trade.Instrument()
    parentTrade = trade.TrxTrade()
    parentInstrument = parentTrade.Instrument()
    parentQuantity = abs(round(sl_functions.underlying_quantity(
        parentTrade.Quantity(), parentInstrument)))
    childQuantity = abs(round(sl_functions.underlying_quantity(
        trade.Quantity(), instrument)))
    return parentQuantity - childQuantity


def FullReturnQuantity(trade):
    return abs(round(sl_functions.underlying_quantity(
        trade.Quantity(), trade.Instrument())))


def FormatInstrumentName(name):
    """ Strip away 'ZAR/' from the instrument name to return the JSE ticker.
    """
    return name[4:]

def SetRecordFields(record, trade, recordType, fund, lenderRecord='No'):

    instrument = trade.Instrument()
    leg = instrument.Legs().At(0)
    underlying = instrument.Underlying()
    quantity = abs(round(sl_functions.underlying_quantity(trade.Quantity(),
        instrument)))

    if (instrument.Underlying().InsType()== 'Bond' or
            instrument.Underlying().InsType()== 'IndexLinkedBond'):
        price = trade.AllInPrice()
    else:
        price = instrument.RefPrice()


    value = quantity * price * underlying.Quotation().QuotationFactor()

    if recordType == 'Amend':
        record.TransactionType.Value(TransactionType.Trade)
        record.Status.Value(GlobalOneStatus.Amended)

    elif recordType == 'Insert':
        record.TransactionType.Value(TransactionType.Trade)
        record.Status.Value(GlobalOneStatus.New)

    elif recordType == 'PartialReturn':
        record.TransactionType.Value(TransactionType.Return)
        record.Status.Value(GlobalOneStatus.New)
        record.ReturnUpdateFlag.Value(ReturnUpdateFlag.DefaultFromParent)
        quantity = ReturnedQuantity(trade)
        record.Quantity.Value(quantity)
        record.TradeDate.Value(trade.TradeTime(), '%Y-%m-%d %H:%M:%S')
        record.SecuritySettlementDueDate.Value(instrument.StartDate(),
            '%Y-%m-%d')
        return

    elif recordType == 'FullReturn':
        try:
            custom_trade_date = trade.AdditionalInfo().SL_CustomTradeDate()
        except Exception as ex:
            custom_trade_date = None
            print("Trade {0} has a problematic Custom Return Date: {1}".format(trade.Oid(), str(ex)))

        if custom_trade_date:
            custom_trade_date = acm.Time().DateFromTime(custom_trade_date)
        else:
            custom_trade_date = acm.Time().DateNow()
        
        record.ReturnUpdateFlag.Value(ReturnUpdateFlag.DefaultFromParent)
        record.Quantity.Value(FullReturnQuantity(trade))
        record.TransactionType.Value(TransactionType.Return)
        record.Status.Value(GlobalOneStatus.New)
        record.TradeDate.Value(min(custom_trade_date,
            CALENDAR.AdjustBankingDays(instrument.EndDate(), -1)), '%Y-%m-%d')
        record.SecuritySettlementDueDate.Value(instrument.EndDate(),
            '%Y-%m-%d')
        return

    isin = underlying.Isin()
    if isin:
        record.SecurityCodeType.Value(SecurityCodeType.ISIN)
        record.IsinCode.Value(isin)
    else:
        underlyingName = FormatInstrumentName(underlying.Name())
        record.SecurityCodeType.Value(SecurityCodeType.Ticker)
        record.IsinCode.Value(underlyingName)

    record.Quantity.Value(quantity)
    record.LoanPrice.Value(price)
    record.LoanValue.Value(value)

    #Don't set minimum fee on lender record
    if lenderRecord != 'Yes':
        record.MinimumFee.Value(instrument.add_info('SL_Minimum_Fee'))
        record.MinimumFeeType.Value('F')
        record.MinimumFeeValue.Value(instrument.add_info('SL_Minimum_Fee'))

    record.Currency.Value(instrument.Currency().Name())
    record.SecuritySettlementDueDate.Value(instrument.StartDate(), '%Y-%m-%d')
    #test for SWIFT add_info field
    if (trade.add_info('SL_SWIFT') == 'SWIFT' or
            (not (trade.add_info('SL_SWIFT')))):
        record.SecuritySettlementMode.Value('SWIFT')
    else:
        record.SecuritySettlementMode.Value('DOM')

    record.TradeDate.Value(trade.TradeTime(), '%Y-%m-%d %H:%M:%S')
    record.TradeTime.Value(trade.TradeTime(), '%Y-%m-%d %H:%M:%S')

    if fund:
        record.LenderModuleTrade.Value(LenderModuleTrade.ManualValidation)
        record.FundCode1.Value(fund)
        record.FundLocation1.Value('000')
        record.Fund1Quantity.Value(quantity)
        record.Fund1Value.Value(value)

    # ABITFA-1684: Pushing the dividend percentage to Global One.
    try:
        sl_dividend_factor = float(instrument.add_info('SL_Dividend_Factor'))
        if sl_dividend_factor != 1:
            record.NetDividendPercentage.Value(sl_dividend_factor * 100)
    except RuntimeError as instance:
        log.Information("Additional info 'SL_Dividend_Factor' is missing "
            "on the instrument %(instrument)s. Assuming that its value is 1.\n"
            "More detailed explanation: %(instance)s\n" %
            {'instrument': instrument.Name(), 'instance': instance})

def isValidUpload(trade):
    """ Make sure that the trade is meant to be sent to Global One
    """
    # ABITFA-1572 - remove the restriction that forces only two instances
    # of a trade to feed down to global 1.
    # only the check is being removed - the warning will still come through
    # on the user log window.
    #if trade.SLGlobalOneTimeStampCount() >= 2:
    #    return False
    instrument = trade.Instrument()
    if (instrument.add_info('SL_ExternalInternal') == 'Internal' ):
        return False
    elif (not(trade.add_info('SL_G1Counterparty1') and
            trade.add_info('SL_G1Counterparty2'))):
        return False
    else:
        return True

def getTradeCategory(trade):
    """
    (if rolling period 1d) = MD - Mark Daily:
    Trade to be M-T-M daily on or after settlement date is reached.
    (if rolling period 1w and rolling base day is Monday) MM - Mark Monday:
    Trade to be M-T-M weekly every Monday on or after
    settlement date is reached. If Monday is a holiday
    then the trade will be M-T-M on the following Friday.
    (if rolling period 1w and rolling base day is Friday) MF - Mark Friday:
    Trade to be M-T-M weekly every Friday after on or settlement date
    is reached. If Friday is a holiday then the trade will be M-T-M
    on the following Monday.
    """
    nst = acm.Time()
    rollingPeriod = trade.Instrument().PayLeg().RollingPeriod()
    if str(rollingPeriod).upper() == '1D':
        return 'MD'     #MARK DAILY
    elif str(rollingPeriod).upper() == '1W':
        rollingBase = trade.Instrument().PayLeg().RollingPeriodBase()
        dow = nst.DayOfWeek(rollingBase)
        if dow == 'Monday':
            return 'MM'
        elif dow == 'Friday':
            return 'MF'
    return None

def getPartyCode(party, partyType):

    if partyType == 'Fund':
        parties = acm.FChoiceList.Select("name = 'GlobalOneFunds'")[0]
    elif partyType == 'Borrower':
        parties = acm.FChoiceList.Select("name = 'GlobalOneBorrowers'")[0]
    elif partyType == 'Lender':
        parties = acm.FChoiceList.Select("name = 'GlobalOneLenders'")[0]

    if parties:
        for item in parties.Choices():
            if item.Name() == party:
                return item.Description()

    if partyType != "Fund":
        FAParty = acm.FParty[party]
        if FAParty:
            return FAParty.AdditionalInfo().SL_G1PartyCode()

    return None


def excludeVat(_value, instrument, for_date):
    if instrument.AdditionalInfo().SL_VAT():
        vat_rate = get_vat_for_date(for_date)
        return float(_value) / vat_rate
    else:
        return _value


def is_finder_applicable(cpty_code):
    return not (cpty_code == 'ABS401' or cpty_code == 'ABS402')


def get_finder_code(finder_name):
    if not finder_name:
        return None
    finder_chlist = sl_functions.FINDER_CHLIST
    choice_list = acm.FChoiceList.Select01(
        'name="%s" and list="MASTER"' % finder_chlist,
        'Choice list %s does not exist.' % finder_chlist)
    for item in choice_list.Choices():
        if finder_name == item.Name():
            return item.Description()
    return None


def add_finder_code_and_fee(record, trade):
    finder_fee = trade.add_info('SL_G1FinderRate')
    finder_code = get_finder_code(trade.add_info('SL_G1FinderCode'))
    if finder_code:
        record.FinderLocBankFee.Value(finder_fee)
        record.FinderLocBankCode.Value(finder_code)
    return record


def GenerateReport(trades, filepath, backupDir, confirmationsDir, parameters):
    """ Generate a Global One trade report
    """

    report = GlUploadFile()
    for trade in trades:
        if isValidUpload(trade):
            recordType = getRecordType(trade)
            if recordType:
                fundCode = getPartyCode(trade.add_info('SL_G1Counterparty2'),
                    'Fund')
                instrument = trade.Instrument()
                leg = instrument.Legs().At(0)
                if fundCode:
                    record = report.CreateRecord(trade)
                    if trade.SLPartialReturnIsPartOfChain():
                        firstTrade = trade.SLPartialReturnFirstTrade()
                        tradeNumber = firstTrade.Oid()
                    else:
                        tradeNumber = trade.Oid()
                    tradeNumberLinkRef = process_trade_nbr(tradeNumber)
                    
                    record.OwnContractReference.Value(tradeNumber)
                    record.InterestRate.Value(excludeVat(leg.FixedRate(),
                        instrument, trade.ValueDay()))
                    record.PostingType.Value(PostingType.Loan)
                    borrower = getPartyCode(trade.add_info(
                        'SL_G1Counterparty1'), 'Borrower')
                    record.CounterpartyCode.Value(borrower)
                    record.LinkReference.Value(tradeNumberLinkRef)
                    if is_finder_applicable(borrower):
                        record = add_finder_code_and_fee(record, trade)

                    SetRecordFields(record, trade, recordType, fundCode)
                else:
                    if trade.SLPartialReturnIsPartOfChain():
                        firstTrade = trade.SLPartialReturnFirstTrade()
                        tradeNumber = firstTrade.Oid()
                    else:
                        tradeNumber = trade.Oid()
                    tradeNumberLinkRef = process_trade_nbr(tradeNumber)

                    # Create borrower record
                    record1 = report.CreateRecord(trade)
                    record1.OwnContractReference.Value(str(tradeNumber)+'B')
                    record1.PostingType.Value(PostingType.Loan)
                    record1.InterestRate.Value(excludeVat(leg.FixedRate(),
                        instrument, trade.ValueDay()))
                    borrower = getPartyCode(trade.add_info('SL_G1Counterparty1'),
                        'Borrower')
                    record1.CounterpartyCode.Value(borrower)
                    record1.LinkReference.Value(tradeNumberLinkRef)
                    if parameters['tradeCategory'] == 'Yes':
                        record1.TradeCategory.Value(getTradeCategory(trade))
                    if is_finder_applicable(borrower):
                        record1 = add_finder_code_and_fee(record1, trade)

                    SetRecordFields(record1, trade, recordType, None)

                    # Create lender record
                    record2 = report.CreateRecord(trade)
                    record2.OwnContractReference.Value(str(tradeNumber)+'L')
                    record2.PostingType.Value(PostingType.Borrow)
                    lenderFee = trade.add_info('SL_G1Fee2')
                    if not lenderFee:
                        lenderFee = leg.FixedRate()
                    record2.InterestRate.Value(excludeVat(lenderFee,
                        instrument, trade.ValueDay()))
                    lender = getPartyCode(trade.add_info('SL_G1Counterparty2'),
                        'Lender')
                    record2.CounterpartyCode.Value(lender)
                    record2.LinkReference.Value(tradeNumberLinkRef)
                    if parameters['tradeCategory'] == 'Yes':
                        record2.TradeCategory.Value(getTradeCategory(trade))
                    if is_finder_applicable(lender):
                        record2 = add_finder_code_and_fee(record2, trade)

                    SetRecordFields(record2, trade, recordType, None,
                        lenderRecord = 'Yes')

    filename = report.Filename
    fullPath = os.path.join(filepath, filename)
    backupPath = os.path.join(backupDir, filename)

    if report.WriteFile(fullPath, backupPath):
        print('Completed successfully.')
        if confirmationsDir:
            report.WriteConfirmationReport(confirmationsDir)
    else:
        raise RuntimeError("Errors occurred. Check error file")

backupSelection = FRunScriptGUI.DirectorySelection()
backupSelection.SelectedDirectory('Y:\\Jhb\Prime Services FO\\'
    '1. Equity Finance\\1. SBL\\SBL\\ACS Migration\\Global One Backup Files')

outputSelection = FRunScriptGUI.DirectorySelection()
outputSelection.SelectedDirectory('\\\\jhbdsm020000050\\Uploads\\')

confirmationsSelection = FRunScriptGUI.DirectorySelection()

trade_key = '0'
folder_key = '1'
backup_folder_key = '2'
confirmations_folder_key = '3'

# Variable Name, Display Name, Type, Candidate Values,
# Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [[trade_key, 'Trades Selection', 'FTrade', None,
        None, 0, 1, 'Global One trade selection.', None, 1],
    [backup_folder_key, 'Backup Folder', backupSelection, None,
        backupSelection, 1, 1, 'Backup Folder', None, 1],
    [folder_key, 'Global One Folder', outputSelection, None,
        outputSelection, 1, 1, 'Global One Output Folder', None, 1],
    [confirmations_folder_key, 'Confirmation Report Folder',
        confirmationsSelection, None, confirmationsSelection, 0, 1,
        'Folder where confirmation reports will be generated.', None, 1],
    ['tradeCategory', 'Populate Trade Category_Settings', 'string',
        ['No', 'Yes'], 'Yes', 1, 0,
        'Populates the trade category field in the upload file if Yes',
        None, 1]]

def ael_main(parameters):
    trades = parameters[trade_key]
    path = parameters[folder_key].SelectedDirectory().Text()
    backup_path = parameters[backup_folder_key].SelectedDirectory().Text()
    confirmations_path = parameters[
        confirmations_folder_key].SelectedDirectory().Text()
    GenerateReport(trades, path, backup_path, confirmations_path, parameters)
