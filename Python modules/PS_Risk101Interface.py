"""-----------------------------------------------------------------------
MODULE
    PS_Risk101Interface

DESCRIPTION
    Date                : 2011-07-05
    Purpose             : Risk101 Interface Files
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Paul Jacot-Guillarmod, Francois Truter, Herman Hoon
    CR Number           : 703542
    
HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2011-07-05 703542       Herman Hoon    Initial Implementation
2011-07-08 707977       Herman Hoon    Updated instrument type mappings
2011-07-15 713436       Herman Hoon    Updated mappings for Swaps and FRAs
2011-07-18 715943       Herman Hoon    Updated the mapping for FRNs
2011-08-22 746446       Herman Hoon    Updated to remove the PS_Risk101Timestamp add info updating
2011-12-01 851050       Herman Hoon    Updated to include new mappings.
ENDDESCRIPTION
-----------------------------------------------------------------------"""

from gen_delimited_record import StringField
from gen_delimited_record import DoubleField
from gen_delimited_record import ListField
from gen_delimited_record import DayField
from gen_delimited_record import MonthField
from gen_delimited_record import YearField
from gen_delimited_record import HourField
from gen_delimited_record import MinuteField
from gen_delimited_record import YesNoField
from gen_delimited_record import IntegerField
from gen_delimited_record import Record
import acm

NEWLINE = '\n'

class Risk101SettlementTerms():
    
    PREVIOUS_BUSINESS_DAY = 'PBD'
    SAME_BUSINESS_DAY = 'T+0'
    NEXT_BUSINESS_DAY = 'NBD'
    T_PLUS_0 = 'T+0'
    T_PLUS_1 = 'T+1'
    T_PLUS_2 = 'T+2'
    T_PLUS_3 = 'T+3'
    T_PLUS_4 = 'T+4'
    T_PLUS_5 = 'T+5'
    SECOND_THURSDAY = '2TH'
    
    @staticmethod
    def TranslateFromSpotDays(days):
        if days == 0:
            return Risk101SettlementTerms.T_PLUS_0
        elif days == 1:
            return Risk101SettlementTerms.T_PLUS_1
        elif days == 2:
            return Risk101SettlementTerms.T_PLUS_2
        elif days == 3:
            return Risk101SettlementTerms.T_PLUS_3
        elif days == 4:
            return Risk101SettlementTerms.T_PLUS_4
        elif days == 5:
            return Risk101SettlementTerms.T_PLUS_5
        else:
            return ''

class Risk101InstrumentTypes():
    
    BOND_SPOT = 'B1'
    BOND_SPOT_OPTION = 'B2'
    BOND_FUTURE = 'B3'
    BOND_OTC_FUTURE_OPTION = 'B4'
    BOND_MARGINED_FUTURE_OPTION = 'B6'
    EQUITY_SPOT = 'E1'
    EQUITY_SPOT_OPTION = 'E2'
    EQUITY_FUTURE = 'E3'
    EQUITY_OTC_FUTURE_OPTION = 'E4'
    EQUITY_MARGINED_SPOT_OPTION = 'E5'
    EQUITY_MARGINED_FUTURE_OPTION = 'E6'
    INDEX_SPOT = 'I1'
    INDEX_SPOT_OPTION = 'I2'
    INDEX_FUTURE = 'I3'
    INDEX_OTC_FUTURE_OPTION = 'I4'
    INDEX_MARGINED_SPOT_OPTION = 'I5'
    INDEX_MARGINED_FUTURE_OPTION = 'I6'
    COMMODITY_SPOT = 'C1'
    COMMODITY_SPOT_OPTION = 'C2'
    COMMODITY_FUTURE = 'C3'
    COMMODITY_OTC_FUTURE_OPTION = 'C4'
    COMMODITY_MARGINED_FUTURE_OPTION = 'C6'
    CARBON_PERMIT_SPOT = 'X1'
    CARBON_PERMIT_SPOT_OPTION = 'X2'
    CARBON_PERMIT = 'X3'
    CARBON_PERMIT_OTC_OPTION = 'X4'
    CARBON_PERMIT_MARGINED_OPTION = 'X6'
    MMKT_SPOT_DISCOUNT_INSTRUMENT = 'D1'
    MMKT_SPOT_EFFECTIVE_INSTRUMENT = 'F1'
    LINKED_BOND_SPOT = 'L1'
    LINKED_BOND_SPOT_OPTION = 'L2'
    CASH = 'M1'
    CASH_FIXED_DEPOSIT = 'M3'
    NCD_WITH_COUPON = 'N1'
    NCD_WITH_COUPON_OPTION = 'N2'
    TRADEABLE_FOREX_SPOT = 'U1'
    TRADEABLE_FOREX_SPOT_OPTION = 'U2'
    TRADEABLE_FOREX_FUTURE = 'U3'
    TRADEABLE_FOREX_OTC_FUTURE_OPTION = 'U4'
    TRADEABLE_FOREX_MARGINED_FUTURE_OPTION = 'U6'
    FRA = 'R1'
    CAP_FLOOR_OR_COLLAR = 'R2'
    SWAP = 'S1'
    SWAPTION = 'S2'
    ANNUITY_CASH_FLOW = 'A1'
    CREDIT_DEFAULT_SWAP = 'T1'
    VARIANCE_SWAP = 'V1'
    VARIANCE_FUTURE = 'V3'
    
    DEFAULT_INS_TYPE = EQUITY_SPOT

    #KEY = (INSTRUMENT TYPE, UNDERLYING TYPE, UNDERLYING UNDERLYING TYPE, OTC, PAY TYPE)
    INSTRUMENT_MAP = {
        ('Stock', None, None, False, 'Spot') :    EQUITY_SPOT ,
        ('Future/Forward', 'Stock', None, False, 'Future') :    EQUITY_FUTURE ,
        ('Future/Forward', 'Stock', None, False, 'Forward') :    EQUITY_FUTURE ,
        ('Future/Forward', 'Stock', None, True, 'Future') :    EQUITY_FUTURE ,
        ('Future/Forward', 'Stock', None, True, 'Forward') :    EQUITY_FUTURE ,
        ('Future/Forward', 'Bond', None, False, 'Future') :    BOND_FUTURE ,
        ('Future/Forward', 'Bond', None, False, 'Forward') :    BOND_FUTURE ,
        ('Future/Forward', 'Bond', None, True, 'Future') :    BOND_FUTURE ,
        ('Future/Forward', 'Bond', None, True, 'Forward') :    BOND_FUTURE ,
        ('Future/Forward', 'Curr', None, False, 'Future') :    TRADEABLE_FOREX_FUTURE ,
        ('Future/Forward', 'Curr', None, True, 'Future') :    TRADEABLE_FOREX_FUTURE ,
        ('Future/Forward', 'Curr', None, True, 'Forward') :    TRADEABLE_FOREX_FUTURE ,
        ('Future/Forward', 'EquityIndex', None, False, 'Future') :    INDEX_FUTURE ,
        ('Future/Forward', 'EquityIndex', None, False, 'Forward') :    INDEX_FUTURE ,
        ('Future/Forward', 'EquityIndex', None, True, 'Future') :    INDEX_FUTURE ,
        ('Future/Forward', 'EquityIndex', None, True, 'Forward') :    INDEX_FUTURE ,
        ('Future/Forward', 'RateIndex', None, False, 'Future') :    INDEX_FUTURE ,
        ('Future/Forward', 'RateIndex', None, True, 'Future') :    INDEX_FUTURE ,
        ('Future/Forward', 'Combination', None, True, 'Future') :    INDEX_FUTURE ,
        ('Future/Forward', 'Combination', None, True, 'Forward') :    INDEX_FUTURE ,
        ('Future/Forward', 'Commodity', None, False, 'Future') :    COMMODITY_FUTURE ,
        ('Future/Forward', 'Commodity', None, False, 'Forward') :    COMMODITY_FUTURE ,
        ('Future/Forward', 'Commodity', None, True, 'Future') :    COMMODITY_FUTURE ,
        ('Future/Forward', 'Commodity', None, True, 'Forward') :    COMMODITY_FUTURE ,
        ('Future/Forward', 'ETF', 'EquityIndex', False, 'Future') :    INDEX_FUTURE ,
        ('Future/Forward', 'ETF', 'EquityIndex', True, 'Forward') :    INDEX_FUTURE ,
        ('Option', 'Stock', None, False, 'Spot') :    EQUITY_SPOT_OPTION ,
        ('Option', 'Stock', None, False, 'Future') :    EQUITY_MARGINED_FUTURE_OPTION ,
        ('Option', 'Stock', None, True, 'Spot') :    EQUITY_SPOT_OPTION ,
        ('Option', 'Stock', None, True, 'Future') :    EQUITY_MARGINED_SPOT_OPTION ,
        ('Option', 'Future/Forward', 'Stock', False, 'Spot') :    EQUITY_OTC_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'Stock', False, 'Future') :    EQUITY_MARGINED_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'Stock', True, 'Spot') :    EQUITY_OTC_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'Stock', True, 'Future') :    EQUITY_MARGINED_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'EquityIndex', False, 'Spot') :    INDEX_OTC_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'EquityIndex', False, 'Future') :    INDEX_MARGINED_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'EquityIndex', True, 'Spot') :    INDEX_OTC_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'EquityIndex', True, 'Future') :    INDEX_MARGINED_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'Commodity', False, 'Spot') :    COMMODITY_OTC_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'Commodity', False, 'Future') :    COMMODITY_MARGINED_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'Commodity', True, 'Spot') :    COMMODITY_OTC_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'Commodity', True, 'Future') :    COMMODITY_MARGINED_FUTURE_OPTION ,
        ('Option', 'Future/Forward', 'Commodity', True, 'Forward') :    COMMODITY_OTC_FUTURE_OPTION ,
        ('Option', 'Option', 'Stock', True, 'Spot') :    EQUITY_SPOT_OPTION ,
        ('Option', 'Option', 'Commodity', True, 'Spot') :    COMMODITY_SPOT_OPTION ,
        ('Option', 'Bond', None, False, 'Spot') :    BOND_SPOT_OPTION ,
        ('Option', 'Bond', None, False, 'Future') :    BOND_MARGINED_FUTURE_OPTION ,
        ('Option', 'Bond', None, True, 'Spot') :    BOND_SPOT_OPTION ,
        ('Option', 'Bond', None, True, 'Future') :    BOND_SPOT_OPTION ,
        ('Option', 'FRA', None, True, 'Spot') :    CAP_FLOOR_OR_COLLAR ,
        ('Option', 'FRA', None, False, 'Spot') :    CAP_FLOOR_OR_COLLAR ,
        ('Option', 'FRA', None, True, 'Spot') :    CAP_FLOOR_OR_COLLAR ,
        ('Option', 'Swap', None, True, 'Spot') :    SWAPTION ,
        ('Option', 'Swap', None, False, 'Spot') :    SWAPTION ,
        ('Option', 'Swap', None, True, 'Spot') :    SWAPTION ,
        ('Option', 'Swap', None, True, 'Forward') :    SWAPTION ,
        ('Option', 'Swap', None, True, 'Contingent') :    SWAPTION ,
        ('Option', 'Cap', None, False, 'Spot') :    CAP_FLOOR_OR_COLLAR ,
        ('Option', 'Cap', None, True, 'Spot') :    CAP_FLOOR_OR_COLLAR ,
        ('Option', 'Floor', None, True, 'Spot') :    CAP_FLOOR_OR_COLLAR ,
        ('Option', 'Curr', None, False, 'Spot') :    TRADEABLE_FOREX_SPOT_OPTION ,
        ('Option', 'Curr', None, False, 'Future') :    TRADEABLE_FOREX_MARGINED_FUTURE_OPTION ,
        ('Option', 'Curr', None, True, 'Spot') :    TRADEABLE_FOREX_SPOT_OPTION ,
        ('Option', 'Curr', None, True, 'Future') :    TRADEABLE_FOREX_OTC_FUTURE_OPTION ,
        ('Option', 'EquityIndex', None, False, 'Spot') :    INDEX_SPOT_OPTION ,
        ('Option', 'EquityIndex', None, False, 'Future') :    INDEX_MARGINED_FUTURE_OPTION ,
        ('Option', 'EquityIndex', None, True, 'Spot') :    INDEX_SPOT_OPTION ,
        ('Option', 'EquityIndex', None, True, 'Forward') :    INDEX_OTC_FUTURE_OPTION ,
        ('Option', 'Commodity', None, False, 'Spot') :    COMMODITY_SPOT_OPTION ,
        ('Option', 'Commodity', None, True, 'Spot') :    COMMODITY_SPOT_OPTION ,
        ('Option', 'Commodity', None, True, 'Forward') :    COMMODITY_SPOT_OPTION ,
        ('Option', 'ETF', 'EquityIndex', False, 'Future') :    INDEX_MARGINED_SPOT_OPTION ,
        ('Option', 'ETF', 'EquityIndex', True, 'Spot') :    INDEX_OTC_FUTURE_OPTION ,
        ('Bond', None, None, False, 'Spot') :    BOND_SPOT ,
        ('FRN', None, None, False, 'Spot') :    NCD_WITH_COUPON ,
        ('FRN', None, None, True, 'Spot') :    NCD_WITH_COUPON ,
        ('Zero', None, None, False, 'Spot') :    BOND_SPOT ,
        ('Zero', None, None, True, 'Spot') :    BOND_SPOT ,
        ('Bill', None, None, False, 'Spot') :    BOND_SPOT ,
        ('CD', None, None, False, 'Spot') :    CASH ,
        ('CD', None, None, True, 'Spot') :    CASH ,
        ('Deposit', None, None, False, 'Spot') :    CASH ,
        ('Deposit', None, None, True, 'Spot') :    CASH ,
        ('FRA', None, None, True, 'Spot') :    FRA ,
        ('Swap', None, None, True, 'Spot') :    SWAP ,
        ('CurrSwap', None, None, True, 'Spot') :    SWAP ,
        ('Cap', None, None, True, 'Spot') :    CAP_FLOOR_OR_COLLAR ,
        ('Floor', None, None, True, 'Spot') :    CAP_FLOOR_OR_COLLAR ,
        ('Curr', None, None, True, 'Spot') :    TRADEABLE_FOREX_SPOT ,
        ('EquityIndex', None, None, False, 'Spot') :    INDEX_SPOT ,
        ('FxSwap', None, None, False, 'Spot') :    TRADEABLE_FOREX_SPOT ,
        ('FxSwap', None, None, True, 'Spot') :    TRADEABLE_FOREX_SPOT ,
        ('SecurityLoan', 'Stock', None, True, 'Spot') :    EQUITY_SPOT ,
        ('SecurityLoan', 'Bond', None, True, 'Spot') :    BOND_SPOT ,
        ('SecurityLoan', 'FRN', None, True, 'Spot') :    BOND_SPOT ,
        ('SecurityLoan', 'CD', None, True, 'Spot') :    CASH ,
        ('SecurityLoan', 'IndexLinkedBond', None, True, 'Spot') :    LINKED_BOND_SPOT ,
        ('SecurityLoan', 'ETF', 'EquityIndex', True, 'Spot') :    INDEX_SPOT ,
        ('Repo/Reverse', 'Bond', None, False, 'Spot') :    BOND_SPOT ,
        ('Repo/Reverse', 'Bond', None, True, 'Spot') :    BOND_SPOT ,
        ('Repo/Reverse', 'FRN', None, True, 'Spot') :    BOND_SPOT ,
        ('Repo/Reverse', 'Bill', None, True, 'Spot') :    BOND_SPOT ,
        ('Repo/Reverse', 'CD', None, True, 'Spot') :    CASH ,
        ('Repo/Reverse', 'Deposit', None, True, 'Spot') :    CASH ,
        ('Repo/Reverse', 'IndexLinkedBond', None, True, 'Spot') :    LINKED_BOND_SPOT ,
        ('BuySellback', 'Bond', None, False, 'Spot') :    BOND_SPOT ,
        ('BuySellback', 'Bond', None, True, 'Spot') :    BOND_SPOT ,
        ('BuySellback', 'FRN', None, True, 'Spot') :    BOND_SPOT ,
        ('BuySellback', 'Bill', None, True, 'Spot') :    BOND_SPOT ,
        ('BuySellback', 'CD', None, True, 'Spot') :    CASH ,
        ('BuySellback', 'Deposit', None, True, 'Spot') :    CASH_FIXED_DEPOSIT ,
        ('BuySellback', 'IndexLinkedBond', None, False, 'Spot') :    LINKED_BOND_SPOT ,
        ('BuySellback', 'IndexLinkedBond', None, True, 'Spot') :    LINKED_BOND_SPOT ,
        ('PriceIndex', None, None, False, 'Spot') :    INDEX_SPOT ,
        ('IndexLinkedBond', None, None, False, 'Spot') :    LINKED_BOND_SPOT ,
        ('TotalReturnSwap', None, None, False, 'Spot') :    INDEX_SPOT ,
        ('TotalReturnSwap', None, None, True, 'Spot') :    INDEX_SPOT ,
        ('CreditDefaultSwap', None, None, True, 'Spot') :     CREDIT_DEFAULT_SWAP ,
        ('CreditDefaultSwap', 'Bond', None, True, 'Spot') :   CREDIT_DEFAULT_SWAP ,
        ('CLN', None, None, False, 'Spot')                 :   CREDIT_DEFAULT_SWAP ,
        ('Commodity', None, None, False, 'Spot') :    COMMODITY_SPOT ,
        ('CreditIndex', None, None, False, 'None') :    CREDIT_DEFAULT_SWAP ,
        ('IndexLinkedSwap', None, None, True, 'Spot') :    SWAP ,
        ('BasketSecurityLoan', None, None, True, 'Spot') :    EQUITY_SPOT ,
        ('CFD', 'Stock', None, True, 'Future') :    EQUITY_SPOT ,
        ('CFD', 'EquityIndex', None, True, 'Future') :    INDEX_SPOT ,
        ('VarianceSwap', 'Stock', None, False, 'Forward') :    VARIANCE_SWAP ,
        ('VarianceSwap', 'Stock', None, True, 'Forward') :    VARIANCE_SWAP ,
        ('VarianceSwap', 'Curr', None, True, 'Forward') :    VARIANCE_SWAP ,
        ('VarianceSwap', 'EquityIndex', None, False, 'Forward') :    VARIANCE_SWAP ,
        ('VarianceSwap', 'EquityIndex', None, True, 'Forward') :    VARIANCE_SWAP ,
        ('Portfolio Swap', None, None, True, 'Spot') :    EQUITY_SPOT ,
        ('ETF', 'EquityIndex', None, False, 'Spot') :    INDEX_SPOT ,
        ('ETF', 'EquityIndex', None, True, 'Spot') :    INDEX_SPOT
    }
    
    
    @staticmethod
    def TranslateFrontInstrument(instrument):
        instrumentType = instrument.InsType()
        underlying = instrument.Underlying()
        underlyingType = underlying.InsType() if underlying else None
        if underlying:
            underlyingUnderlyingType = underlying.Underlying().InsType() if underlying.Underlying() else None
        else:
            underlyingUnderlyingType = None
        instrumentPayType = instrument.PayType()

        key = (instrumentType, underlyingType, underlyingUnderlyingType, instrument.Otc(), instrumentPayType)
        
        if Risk101InstrumentTypes.INSTRUMENT_MAP.has_key(key):
            return [Risk101InstrumentTypes.INSTRUMENT_MAP[key], None]
        else:
            msg = 'No Risk101 instrument mapping exists for Instrument Type: [%(instrument)s]%(underlying)s, OTC [%(otc)s], Paytype [%(payType)s] \n' \
                %{'instrument': instrumentType, 'underlying': (' ' + underlyingType) if underlyingType else '', 'otc': 'Yes' if instrument.Otc() else 'No','payType': instrumentPayType}
            return [Risk101InstrumentTypes.DEFAULT_INS_TYPE, msg]
            
class InstrumentRecord(Record):

    def __init__(self):
        Record.__init__(self, 'Risk101 Trade Detail', [
            StringField('START_TradeNumber', 8),
            StringField('StrategyCode', 8),
            StringField('InstrumentType', 2),
            StringField('InstrumentCode', 14, None, True),
            ListField('CapacityType', ['A', 'P'], None, True),
            StringField('BookCode', 8),
            HourField('DealTimeHour'),
            MinuteField('DealTimeMinute'),
            DayField('DealDateDay'),
            MonthField('DealDateMonth'),
            YearField('DealDateYear'),
            DayField('SettlementDateDay'),
            MonthField('SettlementDateMonth'),
            YearField('SettlementDateYear'),
            DoubleField('Nominal', None, True),
            ListField('BuyOrSell', ['B', 'S'], None, True),
            StringField('Portfolio', 8, None, True),
            StringField('Counterparty', 8, None, True),
            StringField('PaymentCurrency', 4, None, True),
            StringField('BaseCurrency', 4, None, True),
            DoubleField('Price', None, True),
            DoubleField('Yield'),
            DoubleField('CleanConsideration', None, True),
            DoubleField('TotalConsideration', None, True),
            DoubleField('CrossRate'),
            DoubleField('BookingCosts'),
            DoubleField('BookingCostVat'),
            DoubleField('ExchangeFees'),
            DoubleField('OtherCosts1'),
            DoubleField('OtherCosts2'),
            DoubleField('OtherCosts3'),
            DoubleField('OtherCosts4'),
            StringField('Comment', 32),
            DayField('FuturesCloseOutDateDay'),
            MonthField('FuturesCloseOutDateMonth'),
            YearField('FuturesCloseOutDateYear'),
            DoubleField('InitialMargin'),
            DoubleField('StrikePrice'),
            ListField('AmericanOrEuropean', ['A', 'E']),
            ListField('PutOrCall', ['P', 'C']),
            DayField('OptionExpiryDateDay'),
            MonthField('OptionExpiryDateMonth'),
            YearField('OptionExpiryDateYear'),
            HourField('OptionExpiryTimeHour'),
            MinuteField('OptionExpiryTimeMinute'),
            DayField('StockDeliveryDateOnExpiryDay'),
            MonthField('StockDeliveryDateOnExpiryMonth'),
            YearField('StockDeliveryDateOnExpiryYear'),
            ListField('SettlementTerms', [Risk101SettlementTerms.PREVIOUS_BUSINESS_DAY, Risk101SettlementTerms.SAME_BUSINESS_DAY, Risk101SettlementTerms.NEXT_BUSINESS_DAY, Risk101SettlementTerms.T_PLUS_0, Risk101SettlementTerms.T_PLUS_1, Risk101SettlementTerms.T_PLUS_2, Risk101SettlementTerms.T_PLUS_3, Risk101SettlementTerms.T_PLUS_4, Risk101SettlementTerms.T_PLUS_5, Risk101SettlementTerms.SECOND_THURSDAY]),
            DoubleField('OptionSpotPrice'),
            DoubleField('OptionVolatility'),
            DayField('IsueDateDay'),
            MonthField('IsueDateMonth'),
            YearField('IsueDateYear'),
            DayField('CouponDate1Day'),
            MonthField('CouponDate1Month'),
            DayField('CouponDate2Day'),
            MonthField('CouponDate2Month'),
            DayField('CouponDate3Day'),
            MonthField('CouponDate3Month'),
            DayField('CouponDate4Day'),
            MonthField('CouponDate4Month'),
            DayField('MaturityDateDay'),
            MonthField('MaturityDateMonth'),
            YearField('MaturityDateYear'),
            DoubleField('MaturityValue'),
            ListField('PrimaryOrSecondary', ['P', 'S']),
            DoubleField('Commission'),
            DoubleField('CommissionVat'),
            StringField('CommissionAccount', 8),
            StringField('CommissionCurrency', 8),
            DoubleField('IssuePriceOrYield'),
            DoubleField('CouponRate'),
            DoubleField('Special1'),
            DoubleField('Special2'),
            ListField('TimeZone', ['HST', 'AKST', 'PST', 'MST', 'CST', 'EST', 'AST', 'GMT', 'CET', 'SAST', 'AWST', 'JST', 'ACST', 'AEST', 'NZST']),
            YesNoField('MarginTraded'),
            DoubleField('AccruedInterest'),
            DoubleField('ConsiderationVat'),
            StringField('DealtByCode', 8),
            DoubleField('TotalPaymentCurrencySettlementAmount'),
            StringField('SwapSettleRules', 8),
            StringField('SwapDayCount', 8),
            StringField('SwapHolidays', 4),
            StringField('SwapResetFrequency', 1),
            StringField('SwapRateCode', 80),
            DoubleField('SwapResetSpread'),
            StringField('SwapTermination', 10),
            DoubleField('Reserved89'),
            DoubleField('Reserved90'),
            DoubleField('Reserved91'),
            DoubleField('Reserved92'),
            DoubleField('Reserved93'),
            DoubleField('Reserved94'),
            DoubleField('Reserved95'),
            DoubleField('Reserved96'),
            DoubleField('Reserved97'),
            DoubleField('Reserved98'),
            DoubleField('Reserved99'),
            DoubleField('Reserved100'),
            DoubleField('Dl_PC_clean_cons'),
            DoubleField('Dl_PC_total_cons'),
            DoubleField('Dl_PC_cons_vatgst'),
            DoubleField('Dl_PC_booking_costs'),
            DoubleField('Dl_PC_bcost_vatgst'),
            DoubleField('Dl_PC_exchfees'),
            DoubleField('Dl_PC_othercosts1'),
            DoubleField('Dl_PC_othercosts2'),
            DoubleField('Dl_PC_othercosts3'),
            DoubleField('Dl_PC_othercosts4'),
            DoubleField('Dl_PC_commision'),
            DoubleField('Dl_PC_comm_vatgst'),
            DoubleField('TotalBaseCurrencySettlementAmount'),
            StringField('Dl_exch_instrs', 16),
            StringField('Dl_spec_instrs', 8),
            DoubleField('TotalCash'),
            DayField('TotalCashDateDay'),
            MonthField('TotalCashDateMonth'),
            YearField('TotalCashDateYear'),
            StringField('CashCurrency', 4),
            DoubleField('TotalNav'),
            DoubleField('Reserved122'),
            DoubleField('Reserved123'),
            DoubleField('Reserved124'),
            DoubleField('Reserved125'),
            DoubleField('Reserved126'),
            DoubleField('Reserved127'),
            DoubleField('Reserved128'),
            DoubleField('Reserved129'),
            DoubleField('Reserved130'),
            DoubleField('Reserved131'),
            DoubleField('Reserved132'),
            DoubleField('Reserved133'),
            DoubleField('Reserved134'),
            DoubleField('Reserved135'),
            DoubleField('Reserved136'),
            DoubleField('Reserved137'),
            DoubleField('Reserved138'),
            DoubleField('Reserved139'),
            DoubleField('Reserved140'),
            DoubleField('Reserved141'),
            DoubleField('Reserved142'),
            DoubleField('Reserved143'),
            DoubleField('Reserved144'),
            DoubleField('Reserved145'),
            DoubleField('Reserved146'),
            DoubleField('Reserved147'),
            DoubleField('Reserved148'),
            DoubleField('Reserved149'),
            DoubleField('Reserved150'),
            DoubleField('Reserved151'),
            StringField('SecurityShortName', 20),
            StringField('BloombergCode', 80),
            DoubleField('BloombergMultiplier'),
            StringField('IsinCode', 16),
            StringField('IcbeSector', 8),
            StringField('GicsSector', 8),
            StringField('FcccSector', 16),
            DoubleField('SecurityMultiplier'),
            StringField('HybridType', 12),
            StringField('UnderlyingCode', 80),
            DoubleField('Delta'),
            DoubleField('Beta'),
            DayField('IssueDateDay'),
            MonthField('IssueDateMonth'),
            YearField('IssueDateYear'),
            IntegerField('CouponsPerYear'),
            DayField('SecurityCouponDate1Day'),
            MonthField('SecurityCouponDate1Month'),
            DayField('SecurityCouponDate2Day'),
            MonthField('SecurityCouponDate2Month'),
            DayField('SecurityCouponDate3Day'),
            MonthField('SecurityCouponDate3Month'),
            DayField('SecurityCouponDate4Day'),
            MonthField('SecurityCouponDate4Month'),
            DayField('SecurityMaturityDateDay'),
            MonthField('SecurityMaturityDateMonth'),
            YearField('SecurityMaturityDateYear'),
            IntegerField('SecurityCouponRate'),
            ListField('TradeMethod', ['P', 'Y']),
            StringField('PricingMethod', 4),
            StringField('AccruedInterestMethod', 4),
            IntegerField('DaysPerYear'),
            StringField('Country', 4)
            ], ',')
        
class InstrumentFile:
    
    def __init__(self):
        self._records = {}
    
    @property    
    def _header(self):
        dummyRecord = InstrumentRecord()
        return dummyRecord.FieldListing
        
    def CreateRecord(self, trade):
        _record = InstrumentRecord()
        if not trade in self._records:
            self._records[trade] = []
        self._records[trade].append(_record)
        return _record
        
    def WriteFile(self, filepath):
        if self._records:
            timestamp = acm.Time().TimeNow()
            success = True
            errorFilePath = filepath + '.err'
            acm.BeginTransaction()
            try:    
                with open(filepath, 'w') as reportFile:
                    reportFile.write(self._header)
                    with open(errorFilePath, 'w') as errorFile:
                        formatting = ''
                        for trade in self._records:
                            try:
                                for _record in self._records[trade]:
                                    reportFile.write(NEWLINE + str(_record))
                            except Exception, ex:
                                errorFile.write(''.join([formatting, 'ERROR for trade: ', str(trade.Oid()), ' :', str(ex)]))
                                formatting = NEWLINE
                                success =  False
                acm.CommitTransaction()
            except Exception, ex:           
                acm.AbortTransaction()
                raise ex
                
            if not success:
                raise Exception('An error occurred while writing the Risk 101 Transaction file. Please review the error file [%s].' % errorFilePath)
