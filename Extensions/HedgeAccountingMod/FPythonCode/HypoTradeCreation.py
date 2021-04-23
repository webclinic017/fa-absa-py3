'''
===================================================================================================
PURPOSE: Create a hypothethical instrument from an existing instrument for Cash Flow hedges
         Change curve to ZAR/Hypo_PRIME
         Change val group to AC_GLOBAL_PRIME
         Nominals * -1
         For swaps, solve for a fixed rate such that the PV = 0. This is essentially a dirty par
            rate.
         For FRAs, there is not accrued interest, so the par rate is used as the fixed rate
         For Curr Swaps and FX Forwads, no calculations are done
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016      FIS Team                Initial implementation
28-08-2018      Jaysen Naicker          Check if rate index has underlying when calculating fixing price
08-02-2021      Qaqamba Ntshobane       Added MirrorPortfolio, set Premium to 0, removed payments 
                                        creation and ensured all resets are updated upon new 
                                        hypo creation.
===================================================================================================
'''

import acm
import ael
import FLogger
import HedgeConstants

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)


class NewHypo(object):

    def __init__(self, trade, shell):
        self.shell = shell
        self.trade = trade
        self.ins = trade.Instrument()
        self.percentage = None
        self.currency = self.trade.Currency()
        self.ins_type = trade.Instrument().InsType()
        self.val_group = acm.FChoiceList[HedgeConstants.STR_HYPO_VAL_GROUP]
        self.float_rate_ref = acm.FRateIndex[HedgeConstants.STR_HYPO_FLOAT_RATE]
        self.bump_size = 0.002
        self.tolerance = 1e-6
        self.epsilon = 1e-10
        self.max_iterations = 100
        if not self.get_percentage():
            return
        if not self.get_designation_date():
            return
        
        self.portfolio_sheet_calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
        self.portfolio_sheet_calc_space.SimulateGlobalValue('Valuation Date', self.designation_date)
        
        try:
            self.create_hypo()
        except Exception as e:
            raise e
        finally:
            self.portfolio_sheet_calc_space.RemoveGlobalSimulation('Valuation Date')

    def get_designation_date(self):
        self.designation_date = acm.UX().Dialogs().GetTextInput(self.shell,
                                                                "HR's Designation Date",
                                                                HedgeConstants.DAT_TODAY)
        if self.designation_date:
            try:
                calendar = self.currency.Calendar()
                self.value_date = self.ins.SpotDate(self.designation_date, calendar)
                return True
            except Exception as e:
                acm.UX().Dialogs().MessageBoxInformation(self.shell, e)
                self.get_designation_date()
        else:
            return

    def get_percentage(self):
        percentage = acm.UX().Dialogs().GetTextInput(self.shell, "Hypo's percentage", '100')
        if percentage:
            try:
                self.percentage = float(percentage) / 100.0
                if self.percentage > 1:
                    acm.UX().Dialogs().MessageBoxInformation(self.shell,
                                                             'Please enter a percentage < 100.')
                    self.get_percentage()
                return True
            except Exception as e:
                acm.UX().Dialogs().MessageBoxInformation(self.shell, e)
                self.get_percentage()
        else:
            return

    def create_hypo(self):
        try:
            float_leg = None
            fixed_leg = None

            self.new_instrument = self.ins.Clone()
            self.new_instrument.ValuationGrpChlItem(self.val_group)
            self.new_instrument.ExternalId1(None)
            self.new_instrument.ExternalId2(None)

            for leg in self.new_instrument.Legs():
                if leg.LegType() == 'Fixed':
                    fixed_leg = leg
                    self.fixed_cash_flows = fixed_leg.CashFlows()
                else:
                    leg.FloatRateReference(self.float_rate_ref)
                    float_leg = leg
            self.new_instrument.RegisterInStorage()

            self.create_trade()

            # regenerate the Float leg cashflows
            self.new_instrument.FirstFloatLeg().GenerateCashFlows(None)

            if float_leg:
                for cashflow in float_leg.CashFlows():

                    for reset in cashflow.Resets():

                        price_date = reset.Day()
                        ref_rate_name = float_leg.FloatRateReference().Name()
                        ref_price = self.get_instrument_price(ref_rate_name, price_date)

                        # Check if rate index has underlying
                        if float_leg.FloatRateReference().Underlying():
                            underlying_rate_name = float_leg.FloatRateReference().\
                                                        Underlying().Name()

                            underlying_ref_price = self.get_instrument_price(underlying_rate_name,
                                                                             price_date)

                            fixing_price = ref_price + underlying_ref_price
                        else:
                            fixing_price = ref_price

                        reset.FixingValue(fixing_price)
                            
            if self.new_instrument.InsType() == 'Swap':
                self.newtons_method()
            else:
                par_rate = self.portfolio_sheet_calc_space.CreateCalculation(self.new_trade, 'Par Rate')
                self.new_fixed_rate = par_rate.Value().Number() * 100
                self.new_instrument.Legs()[0].FixedRate(self.new_fixed_rate)

                for flow in self.new_instrument.Legs()[0].CashFlows():
                    flow.FloatRateOffset(self.new_fixed_rate)

            if float_leg and self.new_instrument.InsType() == 'FRA':
                float_leg.FixedRate(self.new_fixed_rate)
            elif fixed_leg:
                fixed_leg.FixedRate(self.new_fixed_rate)
                
            # regenerate the Fixed leg cashflows
            self.new_instrument.FirstFixedLeg().GenerateCashFlows(None)

            # make sure there are no ExternId's set on the resets
            for leg in self.new_instrument.Legs():
                for cashFlow in leg.CashFlows():
                    for reset in cashFlow.Resets():
                        reset.ExternalId(None)

            self.get_new_name()
            self.new_instrument.Name(self.new_name)
            self.new_instrument.Commit()
        except Exception as e:
            logger.ELOG('Exception while creating hypo instrument: %s' % (e))
            return

        self.new_trade.Commit()
        acm.StartApplication('Instrument Definition', self.new_trade)

    def create_trade(self):

        try:
            new_trade = acm.FTrade()

            new_trade.Trader(self.trade.Trader())
            new_trade.Currency(self.currency)
            new_trade.Instrument(self.new_instrument)
            new_trade.TrxTrade(self.trade.Oid())
            new_trade.Text1('Hypo')
            new_trade.Text2(self.trade.Oid())
            new_trade.Type('Normal')
            new_trade.Status('Simulated')
            new_trade.Premium(0.0)
            new_trade.Portfolio(HedgeConstants.STR_CHILD_TRADE_PORTFOLIO)
            new_trade.MirrorPortfolio(HedgeConstants.STR_CHILD_COUNTERPARTY_PORTFOLIO)
            new_trade.Acquirer(HedgeConstants.STR_CHILD_TRADE_ACQUIRER)
            new_trade.Counterparty(HedgeConstants.STR_CHILD_TRADE_COUNTERPARTY)
            new_trade.Nominal(self.trade.Nominal() * self.percentage * -1)
            new_trade.TradeTime(self.designation_date)
            new_trade.ValueDay(self.value_date)
            new_trade.AcquireDay(self.value_date)

            new_trade.RegisterInStorage()
            self.new_trade = new_trade

        except Exception as e:
            logger.ELOG(e)

    def get_all_HRs(self):
        query = r"""SELECT
                        i.insid
                    FROM
                        instrument i
                    WHERE
                        i.instype in ('Swap', 'FRA', 'CurrSwap', 'Curr')
                    and i.insid like '{0}{1}'""".format(self.ins.Name(), '%/Hypo/%')
        _, self.data = ael.asql(query)

    def get_new_name(self):
        next_increment = 0
        self.get_all_HRs()
        insid_list = self.ins.Name().split('/')
        insid_list.append(str(round(self.new_fixed_rate, 3)))
        insid_list.append('Hypo')
        insid_list.append(str(next_increment))
        proposed_name = '/'.join(insid_list)
        if self.data[0]:
            for insid in self.data[0]:
                if insid[0] == proposed_name:
                    next_increment += 1
                    proposed_list = proposed_name.split('/')[:-1]
                    proposed_list.append(str(next_increment))
                    proposed_name = '/'.join(proposed_list)
        if (self.ins_type == 'FRA') and (next_increment == 0):
            proposed_list = proposed_name.split('/')
            del proposed_list[-4]
            proposed_name = '/'.join(proposed_list)
        self.new_name = proposed_name

    def set_fixed_rates(self, new_rate):
        if self.ins_type == 'Swap':
            for flow in self.fixed_cash_flows:
                flow.FixedRate(new_rate)

    def bump_rate(self, step):
        if self.ins_type == 'Swap':
            for flow in self.fixed_cash_flows:
                fixed_rate = flow.FixedRate()
                flow.FixedRate(fixed_rate + step)

    def approximate_derivative(self):
        self.bump_rate(self.bump_size)
        bump_up = self.portfolio_sheet_calc_space.CreateCalculation(self.new_trade, 'Portfolio Present Value').Value().Number()
        self.bump_rate(-2 * self.bump_size)
        bump_down = self.portfolio_sheet_calc_space.CreateCalculation(self.new_trade, 'Portfolio Present Value').Value().Number()
        return (bump_up - bump_down)/(self.bump_size * 2)

    def newtons_method(self):
        solution_found = False
        par_rate = self.portfolio_sheet_calc_space.CreateCalculation(self.new_trade, 'Par Rate')
        x0 = par_rate.Value().Number()
        
        self.set_fixed_rates(x0)
        
        iteration_counter = 0
        for _ in range(self.max_iterations):
            pv = self.portfolio_sheet_calc_space.CreateCalculation(self.new_trade, 'Portfolio Present Value')
            y = pv.Value().Number()
            
            y_prime = self.approximate_derivative()

            if abs(y_prime) < self.epsilon:
                logger.ELOG('Denominator approaching zero. Cannot converge.')
                break

            x1 = x0 - (y/y_prime)
            
            if abs(x1 - x0) <= self.tolerance * abs(x1):
                solution_found = True
                break
            x0 = x1
            self.set_fixed_rates(x0)
            
            iteration_counter = iteration_counter + 1

        if solution_found:
            self.set_fixed_rates(x1)
            logger.LOG('Fixed rate solved: %s' % x1)
            self.new_fixed_rate = x1
        else:
            logger.ELOG('A fixed rate to set PV = 0 was not found.')
            self.new_fixed_rate = None

    @staticmethod
    def get_instrument_price(instrument_name, price_date):
        '''Get the Internal market closing price for a instrument
            on a specific date.
        '''

        query = 'instrument = "%s" and market = "%s" and day <= "%s"'\
                % (instrument_name, "internal", price_date)
        prices = acm.FPrice.Select(query).SortByProperty('Day', False)

        if prices:
            price = prices[0].Settle()
            return price

        return 0.0


def create_hypo(eii):
    insdef = eii.ExtensionObject()
    shell = insdef.Shell()
    trade = insdef.OriginalTrade()
    if trade:
        instrument = trade.Instrument()
        # Only swaps and FRAs are catered for.
        if (instrument.InsType() in ['Swap', 'FRA']):
            NewHypo(trade, shell)
        else:
            acm.UX().Dialogs().MessageBoxInformation(shell, "Hypos can only be created from "
                                                     "instruments of type 'Swap' and 'FRA'")
    else:
        acm.UX().Dialogs().MessageBoxInformation(shell, "It is not possible to create a hypo from "
                                                 "an unsaved trade.")
