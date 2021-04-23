import acm
import csv
import SAGEN_IT_TM_Column_Calculation
import ael
from at_ael_variables import AelVariableHandler

context = acm.GetDefaultContext()
sheetType = 'FTradeSheet'
calcSpace = acm.Calculations().CreateCalculationSpace(context, sheetType)
space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()

ael_variables = AelVariableHandler()
ael_variables.add(
    'trade_filter', 
    label='Trade Filter Name', 
    cls='FStoredASQLQuery',
    default=acm.FStoredASQLQuery['MRBB_FXNOP_Accrual']
)

ael_variables.add(
    'output_file', 
    label='Output File', 
    default='/services/frontnt/Task/MRBB_FXNOP_Accrual.csv'
)

ael_variables.add(
    'accounting_treatment', 
    label='Accounting Treatment (FV / Accrual)',
    cls = 'string',
    collection = ['FV', 'Accrual'],
    default='Accrual'
)


def get_tm_column_calculation_per_currency(trade_id, currency, tm_column_name):
    '''returns calculated value of specified trading manager column containing currency vectors'''
    return SAGEN_IT_TM_Column_Calculation.get_TM_Column_Calculation(None, 'Standard', 'FPortfolioSheet',
                                                                    trade_id, 'Trade',
                                                                    tm_column_name, currency, 1,
                                                                    None, None)

def get_trade_column_value(trade, currency, tm_column_name):
    '''returns calculated value of specified trading manager column in denominated trade currency'''
    if trade.Currency().Name() == currency:
        return calcSpace.CreateCalculation(trade, tm_column_name)


def get_current_nominal(instrument_type, trade, currency, position):
    '''only pull current nominal if depo trade booking produces blank Position per CCY'''
    if instrument_type == 'Deposit' and position == 0:
        try:
            return get_trade_column_value(trade, currency, 'Current Nominal').Value()
        except:
            return None
    else:
        return None


def get_inverse_position_end(instrument_type, trade, currency):
    '''inverse position end incorporated to flatten breaks created by pulling Position per CCY'''
    try:
      return get_trade_column_value(trade, currency, 'Inv Portfolio Profit Loss Position End').Value().Number()
    except:
      return None


def get_unrealized_deprec(instrument_type, trade, currency):
    '''unrealised depreciation incorporated to correctly accrue premia on the bonds'''
    if instrument_type == 'Bond' or trade.Portfolio().Name() == 'Non Zar Liquid Assets':
        try:
            return get_trade_column_value(trade, currency, 'UnRealized Deprec').Value().Number()
        except:
            return None
    else:
        return None

def get_fx_rate(currency):
    curr1 = acm.FInstrument['USD']
    curr2 = acm.FInstrument[currency]
    return curr1.Calculation().MarketPrice(space, acm.Time.DateToday(), 0,
                                           curr2).Value().Number()

def calculate_usd_equivalent(metric, fx_rate):
    try:
      return metric / fx_rate
    except:
      return None

def get_currencies_per_trade(trade):
    '''returns currencies linked to trade'''
    trade_list = []
    curr_list = []
    trade_list.append(trade)
    moneyFlowAndTradesDiscountingUnits = acm.GetFunction('moneyFlowAndTradesDiscountingUnits', 3)
    currenciesFromInstrumentAndTradesDiscountingUnits = acm.GetFunction(
        'currenciesFromInstrumentAndTradesDiscountingUnits', 1)
    discounting_units = moneyFlowAndTradesDiscountingUnits(trade_list, acm.Time().DateToday(), 381)
    currencies = currenciesFromInstrumentAndTradesDiscountingUnits(discounting_units)
    curr_list.append(trade.Currency().Name())
    for curr in currencies:
        curr_list.append(curr.Name())
    return curr_list


def get_payment_currencies_per_trade(trade):
    '''returns payment currencies linked to trade'''
    unique_addPayments_currency_list = []
    curr_addpayment_list = []
    payments = trade.Payments()
    for payment in payments:
        curr_addpayment_list.append(payment.Currency().Name())
        unique_addPayments_currency_list = list(dict.fromkeys(curr_addpayment_list))
    return unique_addPayments_currency_list


def currency_combination(trade):
    '''combines currencies'''
    currencies_per_trade = get_currencies_per_trade(trade)
    payment_currencies_per_trade = get_payment_currencies_per_trade(trade)
    full_currency_list = payment_currencies_per_trade + currencies_per_trade
    unique_currency_list = list(dict.fromkeys(full_currency_list))
    return unique_currency_list


def WriteCSVFile(outputFileLocation, resultsList, HeaderList):
    '''
    Create a file to store all results
    '''
    with open(outputFileLocation,  'wb') as reconBreaksFile:
        reconWriter = csv.writer(reconBreaksFile,  quoting=csv.QUOTE_ALL)
        reconWriter.writerow(HeaderList)
        for itemInList in resultsList:
           reconWriter.writerow(itemInList)

def ael_main(ael_dict):
    final_results = []
    unique_key_list = []
    reporting_date = acm.Time.DateToday()
    trade_filter_query = ael_dict['trade_filter'].Query().Select()
    accounting_treatment_note = ael_dict['accounting_treatment']
    outputFileLocation = ael_dict['output_file']
    accounting_treatment = ael_dict['accounting_treatment']    
    for trade_filter in trade_filter_query:
        trade_list = trade_filter.Trades()
        for trade in trade_list:
            trade_id = trade.Name()
            currency_list = currency_combination(trade)
            for currency in currency_list:
                unique_key = trade_id + "_" + currency

                if currency == 'ZAR': 
                    continue

                elif unique_key in unique_key_list:
                    continue    

                else:
                    unique_key_list.append(unique_key)
                    instrument_type = trade.TradeInstrumentType()
                    instrument_sub_type = trade.InstrumentSubType()
                    portfolio_name = trade.Portfolio().Name()
                    portfolio_number = trade.Portfolio().Oid()
                    value_day = trade.ValueDay()
                    trade_status = trade.Status()
                    instrument_id = trade.Instrument().Name()
                    fx_rate = get_fx_rate(currency)

                    if accounting_treatment_note == 'Accrual' and instrument_type != 'CurrSwap':
                        cash = get_tm_column_calculation_per_currency(trade_id, currency, 'Portfolio Cash Vector')
                        accrued_interest = get_tm_column_calculation_per_currency(trade_id, currency, 'Portfolio Accrued Interest Per Currency')
                        position = get_tm_column_calculation_per_currency(trade_id, currency, 'Portfolio Position Per Currency')
                        present_value = None
                        current_nominal = get_current_nominal(instrument_type, trade, currency, position)
                        inverse_position_end = get_inverse_position_end(instrument_type, trade, currency)
                        unrealized_deprec = get_unrealized_deprec(instrument_type, trade, currency)
                    
                    else:
                        cash = get_tm_column_calculation_per_currency(trade_id, currency, 'Portfolio Cash Vector')
                        accrued_interest = None
                        position = None
                        present_value = get_tm_column_calculation_per_currency(trade_id, currency, 'Portfolio Present Value Per Currency')
                        current_nominal = None
                        inverse_position_end = None
                        unrealized_deprec = None

                    cash_USD_equivalent = calculate_usd_equivalent(cash, fx_rate)
                    accrued_interest_USD_equivalent = calculate_usd_equivalent(accrued_interest, fx_rate)
                    position_USD_equivalent = calculate_usd_equivalent(position, fx_rate)
                    present_value_USD_equivalent = calculate_usd_equivalent(present_value, fx_rate)
                    current_nominal_USD_equivalent = calculate_usd_equivalent(current_nominal, fx_rate)
                    inverse_position_end_USD_equivalent = calculate_usd_equivalent(inverse_position_end, fx_rate)
                    unrealized_deprec_USD_equivalent = calculate_usd_equivalent(unrealized_deprec, fx_rate)
                
                final_results.append([  reporting_date
                                        , trade_id
                                        , currency
                                        , unique_key
                                        , value_day
                                        , portfolio_name
                                        , portfolio_number
                                        , accounting_treatment_note
                                        , instrument_type
                                        , instrument_sub_type
                                        , trade_status
                                        , instrument_id
                                        , trade_filter.Name()
                                        , cash
                                        , position
                                        , accrued_interest
                                        , present_value
                                        , current_nominal
                                        , inverse_position_end
                                        , unrealized_deprec
                                        , fx_rate
                                        , cash_USD_equivalent
                                        , position_USD_equivalent
                                        , accrued_interest_USD_equivalent
                                        , present_value_USD_equivalent
                                        , current_nominal_USD_equivalent
                                        , inverse_position_end_USD_equivalent
                                        , unrealized_deprec_USD_equivalent
                                        ])
    
    HeaderList = [ 'reporting_date'
                    , 'trade_id'
                    , 'currency'
                    , 'unique_key'
                    , 'value_day'
                    , 'portfolio_name'
                    , 'portfolio_number'
                    , 'accounting_treatment'
                    , 'instrument_type'
                    , 'instrument_sub_type'
                    , 'trade_status'
                    , 'instrument_id'
                    , 'trade_filter'                  
                    , 'cash'
                    , 'position'
                    , 'accrued_interest'
                    , 'present_value'
                    , 'current_nominal'
                    , 'inverse_position_end'
                    , 'unrealized_deprec'
                    , 'fx_rate'
                    , 'cash_USD_equivalent'
                    , 'position_USD_equivalent'
                    , 'accrued_interest_USD_equivalent'
                    , 'present_value_USD_equivalent'
                    , 'current_nominal_USD_equivalent'
                    , 'inverse_position_end_USD_equivalent'
                    , 'unrealized_deprec_USD_equivalent'         
                ]

    WriteCSVFile(outputFileLocation, final_results, HeaderList)
