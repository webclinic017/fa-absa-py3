"""-----------------------------------------------------------------------
MODULE
    PCG_Deposit_Uploader.py
HISTORY
==================================================================================
Date            Change no       Developer               Description
----------------------------------------------------------------------------------
2017/12/14      CHNG0005239381  Bhavnisha Sarawan       Uploader for Fixed Term Deposits using a csv file. 
                                                        Note csv file data must be accruate for uploader to work (Initial implementation)

--------------------------------------------------------------------------------"""
import acm
import csv
from at_logging import getLogger
from at_ael_variables import AelVariableHandler

businessLogicHandler = acm.FBusinessLogicGUIDefault()
LOGGER = getLogger(__name__)


def CreateDeposit(ins_name, curr, leg_type, val_group, start_date, end_date, exp_date, calendar, fixed_rate, quotation, spotbankdaysoffset, payoffsetmethod, daycount, rolling_period, cash_amount, value_day, acquire_day, trade_time, portfolio, acquirer, counterparty, funding_instype, guarantor, free_text_1, contract_ref, trans_ref, broker_status, primary_issuance, approx_load, approx_load_ref, insoverride, salescreditsubteam1, salescreditsubteam2, salescreditsubteam3):
    try:
        if not acm.FInstrument[ins_name]:
            deposit = acm.FDeposit()
            deposit = acm.FInstrumentLogicDecorator(deposit, businessLogicHandler)
            deposit.Name(ins_name)
            deposit.Currency(curr)
            deposit.ExpiryDate(exp_date)
            deposit.ValuationGrpChlItem(val_group)
            deposit.Quotation(quotation)
            deposit.QuoteType(quotation)
            deposit.SpotBankingDaysOffset(spotbankdaysoffset)
            deposit.PayOffsetMethod(payoffsetmethod)
            deposit.DayCountMethod(daycount)
            deposit.OpenEnd('None')
            deposit.RoundingSpecification('Rounding_FX_2Dec')
            deposit.StrikeCurrency(curr)
            deposit.PriceFindingChlItem('Close')
            #  Leg
            leg = deposit.CreateLeg(1)
            leg.LegType(leg_type)
            leg.Decimals(11)
            leg.StartDate(start_date)
            leg.EndDate(end_date)
            leg.DayCountMethod(daycount)
            leg.FixedRate(fixed_rate)
            leg.ResetDayOffset(0)
            leg.ResetType('None')
            leg.RollingConv('Preserve EOM')
            leg.DayCountMethod(daycount)
            leg.Currency(curr)
            leg.NominalFactor(1)
            leg.Rounding('Normal')
            leg.RollingPeriod(rolling_period)
            leg.RollingPeriodBase(end_date)
            leg.StrikeType('Absolute')
            leg.PayDayMethod('Mod. Following')
            leg.PayCalendar(acm.FCalendar[calendar])
            leg.FixedCoupon(True)
            leg.NominalAtEnd(True)
            leg.FloatRateFactor(1)
            leg.FixedCoupon(True)
            leg.StartPeriod('-1d')
            leg.AmortDaycountMethod(daycount)
            leg.AmortEndDay(end_date)
            leg.AmortStartDay(start_date)
            deposit.Commit() #  Commits both the instrument and the leg.
        #  Trade
        trade = acm.FTrade()
        trade = acm.FTradeLogicDecorator(trade, businessLogicHandler)
        if acm.FInstrument[ins_name]:
            trade.Instrument(acm.FInstrument[ins_name])
            qty = (float(cash_amount)/acm.FInstrument[ins_name].ContractSize())*-1
        else:
            trade.Instrument(deposit)
            qty = (float(cash_amount)/deposit.ContractSize())*-1
        trade.Quantity(qty)
        trade.ValueDay(value_day)
        trade.AcquireDay(acquire_day)
        trade.TradeTime(trade_time)
        trade.Portfolio(acm.FPhysicalPortfolio[portfolio])
        trade.Acquirer(acm.FParty[acquirer])
        trade.Counterparty(acm.FParty[counterparty])
        trade.Guarantor(acm.FParty[guarantor])
        trade.Text1(free_text_1)
        if contract_ref:
            trade.ContractTrdnbr(contract_ref)
        if trans_ref:
            trade.TrxTrade(trans_ref)
        trade.PrimaryIssuance(primary_issuance)
        trade.Currency(curr)
        trade.Price(fixed_rate)
        trade.Type('Normal')
        trade.Status('Simulated')
        trade.RegisterInStorage()
        trade.AdditionalInfo().Funding_Instype(funding_instype)
        trade.AdditionalInfo().Broker_Status(broker_status)
        trade.AdditionalInfo().Approx_46_load(approx_load)
        trade.AdditionalInfo().Approx_46_load_ref(approx_load_ref)
        trade.AdditionalInfo().InsOverride(insoverride)
        trade.AdditionalInfo().SalesCreditSubTeam1(salescreditsubteam1)
        trade.AdditionalInfo().SalesCreditSubTeam2(salescreditsubteam2)
        trade.AdditionalInfo().SalesCreditSubTeam3(salescreditsubteam3)
        trade.Trader(acm.User())
        trade.Commit()
    except Exception as e:
        LOGGER.error("Error ", ins_name, e)
    return trade.Oid()


ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'Fixed Term Deposit Uploader'}

ael_variables = AelVariableHandler()
ael_variables.add_input_file('input_file',
                            label='CSV File',
                            collection=None,
                            mandatory=True,
                            alt='C:\DepoUploader.csv',
                            enabled=True)

def ael_main(parameter):
    input_file = str(parameter["input_file"])
    with open(input_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in reader:
            try:
                ins_name = row[0]
                curr = row[1]
                leg_type = row[2]
                val_group = row[3]
                start_date = row[4]
                end_date = row[5]
                exp_date = row[6]
                calendar = row[7]
                fixed_rate = row[8]
                quotation = row[9]
                spotbankdaysoffset = row[10]
                payoffsetmethod = row[11]
                daycount = row[12]
                rolling_period = row[13]
                cash_amount = row[14]
                value_day = row[15]
                acquire_day = row[16]
                trade_time = row[17]
                portfolio = row[18]
                acquirer = row[19]
                counterparty = row[20]
                funding_instype = row[21]
                guarantor = row[22]
                free_text_1 = row[23]
                contract_ref = row[24]
                trans_ref = row[25]
                broker_status = row[26]
                primary_issuance = row[27]
                approx_load = row[28]
                approx_load_ref = row[29]
                insoverride = row[30]
                salescreditsubteam1 = row[31]
                salescreditsubteam2 = row[32]
                salescreditsubteam3 = row[33]
                LOGGER.info(CreateDeposit(ins_name, curr, leg_type, val_group, start_date, end_date, exp_date, calendar, fixed_rate,
                        quotation, spotbankdaysoffset, payoffsetmethod, daycount, rolling_period, cash_amount, value_day, acquire_day, trade_time, 
                        portfolio, acquirer, counterparty, funding_instype, guarantor, free_text_1, contract_ref, trans_ref, broker_status, 
                        primary_issuance, approx_load, approx_load_ref, insoverride, salescreditsubteam1, salescreditsubteam2, salescreditsubteam3))
            except Exception, e:
                LOGGER.error('Error processing ', row[0], 'with error: ', e)


