"""------------------------------------------------------------------------
MODULE
    FRegulatoryNotionalAmount -
DESCRIPTION:
    This file consists of the functions to infer the NotionalAmount for trades
VERSION: 1.0.25(0.25.7)
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end
--------------------------------------------------------------------------"""
import acm
import FRegulatoryLogger

calc_space = None
calc_space_collection = acm.FCalculationSpaceCollection()
gridBuilderConfig = acm.Report.CreateDealGridConfiguration(False, True, True)
logger = 'FRegulatoryNotionalAmount'


class FRegulatoryNotionalAmount(object):
    def __init__(self, trade):
        self.__trade = trade
        self.__instrument = trade.Instrument()
    # -------------------------------- API's based on InsType, returning Notional amount ----------------------------
    def Warrant(self):
        """API for notional amount calculation for InsType: Warrant"""
        return self._notional_amount_based_on_quantity_contractsize_strikeprice()

    def _trade_premium(self):
        return self.__trade.Premium()

    def _trade_nominal(self):
        """Covering Instrument types: 'Bill', 'Bond', 'Convertible', 'Zero', 'FRN', 'IndexLinkedBond', 
        'PromisLoan', 'DualCurrBond', 'Flexi_Bond', 'CD', 'FRA', 'MBS_ABS', 'CLN', 'BasketSecurityLoan', 
        'BuySellback', 'Cap', 'Floor', 'Deposit_Loan', 'IndexLinkedSwap', 'CreditDefaultSwap', 
        'CurrSwap', 'FX_Option', 'TotalReturnSwap', Certificate, Swap for notional amount calculation"""
        return self._notional_amount_based_on_nominal()

    def _trade_remaining_premium(self):
        """Covering Instrument types: 'PriceSwap', 'FXOptionDatedFwd', 'Average_Future_Forward' for notional amount calculation"""
        return self._notional_amount_based_on_remaining_premium()

    def _trade_notional_on_start_cash(self):
        """Covering Instrument types: 'Repo_Reverse', 'BasketRepo_Reverse' for notional amount calculation"""
        return self._notional_amount_based_on_start_cash()

    def CFD(self):
        """API for notional amount calculation for InsType: CFD"""
        notional_amount = None
        if self.__instrument.Underlying():
            if self.__instrument.Underlying().InsType() in ['Stock', 'Depository Receipt', 'EquityIndex', 'Warrant', 'ETF']:
                notional_amount = self._notional_amount_based_on_remaining_premium()
            if self.__instrument.Underlying().InsType() == 'Bond':
                notional_amount = self._notional_amount_based_on_underlyernominal_remainingpremium()
        return notional_amount

    def Future_Forward(self):
        """API for notional amount calculation for InsType: Future_Forward"""
        notional_amount = None
        if self.__instrument.Underlying():
            if self.__instrument.Underlying().InsType() in ['CurrSwap', 'Swap', 'Average Future/Forward', 'CreditDefaultSwap', 'Deposit', 'FRA', \
                    'FreeDefCF', 'Future/Forward', 'RateIndex', 'Combination']:
                notional_amount = self._notional_amount_based_on_nominal()
            elif self.__instrument.Underlying().InsType() in ['Bill', 'Bond', 'Convertible', 'Zero', 'CLN', 'FRN', 'IndexLinkedBond', 'PromisLoan']:
                notional_amount = self._notional_amount_based_on_underlyernominal_remainingpremium()
            elif self.__instrument.Underlying().InsType() in ['Curr', 'Commodity', 'Commodity Variant', \
                    'Commodity Index', 'ETF', 'Dividend Point Index', 'Stock', 'Depository Receipt', \
                    'EquityIndex']:
                notional_amount = self._notional_amount_based_on_remaining_premium()
        return notional_amount

    def Option(self):
        """API for notional amount calculation for InsType: Option"""
        notional_amount = None
        if self.__instrument.Underlying():
            if self.__instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', \
                    'Commodity Index', 'ETF', 'EquityIndex', 'Stock', 'Depositary Receipt']: #no extra
                notional_amount = self._notional_amount_based_on_quantity_contractsize_strikeprice()
            
            elif self.__instrument.Underlying().InsType() in ['Swap', 'CurrSwap']:
                notional_amount = self._notional_amount_based_on_underlyernominal_quantity()
            elif self.__instrument.Underlying().InsType() == 'CreditDefaultSwap':
                #if self.__instrument.Underlying().Underlying(): 
                #    if self.__instrument.Underlying().Underlying().InsType() in ['CreditIndex', 'Bill', 'Bond', \
                #        'Convertible','Zero', 'FRN', 'IndexLinkedBond', 'PromisLoan']:
                notional_amount = self._notional_amount_based_on_underlyernominal_quantity()
            elif self.__instrument.Underlying().InsType() in ['Bill', 'Bond', 'Convertible', 'Zero', 'CLN', 'FRN',\
                                                              'IndexLinkedBond', 'PromisLoan']:
                notional_amount = self._notional_amount_based_on_quantity_contractsize_strikeprice_underlyernominal()
            else:#'RateIndex', 'Curr', 'Combination'
                notional_amount = self._notional_amount_based_on_nominal()#defaulting it to the trade nominal
        return notional_amount

    # -------------------------------------------------------------Calculation API's-----------------------------------------------------------------------------------
    def _notional_amount_based_on_nominal(self):
        """API to calculate Notional Amount, where notional amount = nominal """
        nominal, error_msg = self._nominal()
        if error_msg:
            raise Exception('Cannot infer NominalAmount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), error_msg))
        return nominal

    def _notional_amount_based_on_start_cash(self):
        """API to calculate Notional Amount, where notional_amount = start_cash"""
        start_cash, error_msg = self._start_cash()
        if error_msg:
            raise Exception(
                'Cannot infer Nominal Amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), error_msg))
        return start_cash

    def _notional_amount_based_on_remaining_premium(self):
        """API to calculate Notional Amount, where notional amount = remaining premium
             Followed for instrument types like: [PriceSwap', 'FXOptionDatedFwd', 'Average_Future_Forward']"""
        remaining_premium, error_msg = self._remaining_premium()
        if error_msg:
            raise Exception(
                'Cannot infer NominalAmount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), error_msg))
        return remaining_premium

    def _notional_amount_based_on_quantity_contractsize_strikeprice(self):
        """API to calculate Notional Amount, where notional amount = quantity * contract_size * strike_price
            Followed for instrument types like: [Option, Warrant] """
        err_msg = ''
        notional_amount = None
        contract_size, error_msg = self._contract_size()
        err_msg = err_msg + '\n' + error_msg
        strike_price, error_msg = self._absolute_strike_price()
        err_msg = err_msg + '\n' + error_msg
        quantity, error_msg = self._quantity()
        err_msg = err_msg + '\n' + error_msg
        err_msg = err_msg.strip()
        if err_msg:
            raise Exception('Cannot infer NominalAmount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), err_msg))
        try:
            notional_amount = quantity * contract_size * strike_price
        except Exception as e:
            raise Exception('Cannot calculate notional amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), e))
        return notional_amount

    def _notional_amount_based_on_quantity_contractsize_strikeprice_underlyernominal(self):
        """API to calculate Notional Amount, where notional_amount = quantity * contract_size * strike_price * nominal_underlying
            Followed for instrument types like: [Option] """
        err_msg = ''
        notional_amount = None
        contract_size, error_msg = self._contract_size()
        err_msg = err_msg + '\n' + error_msg
        strike_price, error_msg = self._absolute_strike_price()
        err_msg = err_msg + '\n' + error_msg
        quantity, error_msg = self._quantity()
        err_msg = err_msg + '\n' + error_msg
        nominal_underlying, error_msg = self._nominal_underlying()
        err_msg = err_msg + '\n' + error_msg
        err_msg = err_msg.strip()
        if err_msg:
            raise Exception('Cannot infer Notional Amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), err_msg))
        try:
            notional_amount = quantity * contract_size * strike_price * nominal_underlying
        except Exception as e:
            raise Exception('Cannot calculate Notional Amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), e))
        return notional_amount

    def _notional_amount_based_on_underlyernominal_remainingpremium(self):
        """API to calculate Notional Amount, where notional_amount = remaining_premium * underlyer_nominal
            Followed for instrument types like: [CFD, Future/Forward] """
        err_msg = ''
        notional_amount = None
        remaining_premium, error_msg = self._remaining_premium()
        err_msg = err_msg + '\n' + error_msg
        underlyer_nominal, err_msg = self._nominal_underlying()
        err_msg = err_msg + '\n' + error_msg
        err_msg = err_msg.strip()
        if err_msg:
            raise Exception('Cannot infer Nominal Amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), err_msg))
        try:
            notional_amount = remaining_premium * underlyer_nominal
        except Exception as e:
            raise Exception('Cannot calculate Notional Amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), e))
        return notional_amount

    def _notional_amount_based_on_underlyernominal_quantity(self):
        """API to calculate Notional Amount, where notional_amount = underlyer_nominal * quantity
            Followed for instrument types like: [Option] """
        err_msg = ''
        notional_amount = None
        underlyer_nominal, error_msg = self._nominal_underlying()
        err_msg = err_msg + '\n' + error_msg
        quantity, error_msg = self._quantity()
        err_msg = err_msg + '\n' + error_msg
        err_msg = err_msg.strip()
        if err_msg:
            raise Exception('Cannot infer Nominal Amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), err_msg))
        elif underlyer_nominal and quantity:
            try:
                notional_amount = underlyer_nominal * quantity
            except Exception as e:
                raise Exception('Cannot calculate Notional Amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), e))
        return notional_amount

    # ------------------------------------------------------------- API's for retrieving field values --------------------------------------------------------------------------------

    def _nominal_underlying(self):
        """Retrieve nominal value of underlying instrument for instrument on given trade"""
        nominal_underlying = None
        err_msg = ''
        try:
            nominal_underlying = self.__instrument.Underlying().NominalAmount()
            msg = "Retrieved Nominal <%d> of underlying instrument <%s> for Notional calculation for trade <%d>." % (
            nominal_underlying, self.__instrument.Name(), self.__trade.Oid())
            if nominal_underlying == 0:
                FRegulatoryLogger.WARN(logger, msg + ' Hence Nominal inferred will also be zero.')
            else:
                FRegulatoryLogger.DEBUG(logger, msg)
        except Exception as e:
            err_msg = "Error while accessing Nominal of underlying instrument <%s> for trade <%s>. Error: <%s>." % (
            self.__instrument.Name(), self.__trade.Oid(), str(e))
            FRegulatoryLogger.ERROR(logger, err_msg)
        return nominal_underlying, err_msg

    def _contract_size(self):
        """Retrieve value of contract size of instrument for given trade """
        contract_size = None
        err_msg = ''
        try:
            contract_size = self.__instrument.ContractSize()
            msg = "Retrieved ContractSize <%d> of instrument <%s> for Notional calculation for trade <%d>." % (
            contract_size, self.__instrument.Name(), self.__trade.Oid())
            if contract_size == 0:
                FRegulatoryLogger.WARN(logger, msg + ' Hence Nominal inferred will also be zero.')
            else:
                FRegulatoryLogger.DEBUG(logger, msg)
        except Exception as e:
            err_msg = "Error while accessing ContractSize of instrument <%s> for trade <%s>. Error: <%s>." % (
            self.__instrument.Name(), self.__trade.Oid(), str(e))
            FRegulatoryLogger.ERROR(logger, err_msg)
        return contract_size, err_msg

    def _nominal(self):
        """Retrieve nominal value for given trade """
        nominal = None
        err_msg = ''
        try:
            nominal = self.__trade.Nominal()
            msg = "Retrieved Nominal <%d> for Notional calculation for trade <%d>." % (nominal, self.__trade.Oid())
            if nominal == 0:
                FRegulatoryLogger.WARN(logger, msg + 'Hence Nominal inferred will also be zero.')
            else:
                FRegulatoryLogger.DEBUG(logger, msg)
        except Exception as e:
            err_msg = "Error while accessing Nominal for trade <%s>. Error: <%s>." % (self.__trade.Oid(), str(e))
            FRegulatoryLogger.ERROR(logger, err_msg)
        return nominal, err_msg

    def _start_cash(self):
        """Retrieve startcash value for given trade"""
        start_cash = None
        err_msg = ''
        try:
            start_cash = self.__trade.StartCash()
            msg = "Retrieved StartCash <%d> for Notional calculation for trade <%d>." % (start_cash, self.__trade.Oid())
            if start_cash == 0:
                FRegulatoryLogger.WARN(logger, msg + 'Hence Nominal inferred will also be zero.')
            else:
                FRegulatoryLogger.DEBUG(logger, msg)
        except Exception as e:
            err_msg = "Error while accessing StartCash for trade <%s>. Error: <%s>." % (self.__trade.Oid(), str(e))
            FRegulatoryLogger.ERROR(logger, err_msg)
        return start_cash, err_msg

    def _absolute_strike_price(self):
        """Retrieve absolute strike price value of instrument for given trade"""
        absolute_strike_price = None
        err_msg = ''
        try:
            absolute_strike_price = acm.GetCalculatedValueFromString(acm.FInstrument[self.__instrument.Name()],
                                                                     acm.GetDefaultContext(), "absoluteStrikePrice",
                                                                     None).Value().Number()
            msg = "Retrieved AbsoluteStrikePrice <%d> of instrument <%s> for Notional calculation for trade <%d>" % (\
                absolute_strike_price, self.__instrument.Name(), self.__trade.Oid())
            if absolute_strike_price == 0:
                FRegulatoryLogger.WARN(logger, msg + 'Hence Nominal inferred will also be zero.')
            else:
                FRegulatoryLogger.DEBUG(logger, msg)
        except Exception as e:
            err_msg = "Error while accessing AbsoluteStrikePrice of instrument <%s> for trade <%s>. Error: <%s>." % (
            self.__instrument.Name(), self.__trade.Oid(), str(e))
            FRegulatoryLogger.ERROR(logger, err_msg)
        return absolute_strike_price, err_msg

    def _quantity(self):
        """Retrieve quantity value from trade"""
        quantity = None
        err_msg = ''
        try:
            quantity = self.__trade.Quantity()
            msg = "Retrieved Quantity <%d> for Notional calculation for trade <%d>." % (quantity, self.__trade.Oid())
            if quantity == 0:
                FRegulatoryLogger.WARN(logger, msg + 'Hence Nominal inferred will also be zero.')
            else:
                FRegulatoryLogger.DEBUG(logger, msg)
        except Exception as e:
            err_msg = "Error while accessing Quantity for trade <%s>. Error: <%s>." % (self.__trade.Oid(), str(e))
            FRegulatoryLogger.ERROR(logger, err_msg)
        return quantity, err_msg

    def _trade_quantity(self):
        """trade quantity as notinal in case of fxSwaps"""
        notional, err_msg = self._quantity()
        if err_msg:
            raise Exception('Cannot infer Notional Amount for trade <%d>. Error : <%s>.' % (self.__trade.Oid(), err_msg))
        return notional

    def _remaining_premium(self):
        """Retrieve remaining premium value for given trade"""
        remaining_premium = None
        err_msg = ''
        global calc_space
        global gridBuilderConfig
        global calc_space_collection
        if calc_space:
            calc_space.Clear()
        calc_space_collection.Clear()
        calc_space = calc_space_collection.GetSpace('FDealSheet', acm.GetDefaultContext(), gridBuilderConfig)
        try:
            remaining_premium = calc_space.CalculateValue(self.__trade, 'Remaining Premium').Number()
            msg = "Retrieved RemainingPremium <%d> for Notional calculation for trade <%d>." % (remaining_premium, self.__trade.Oid())
            if remaining_premium == 0:
                FRegulatoryLogger.WARN(logger, msg + 'Hence Nominal inferred will also be zero.')
            else:
                FRegulatoryLogger.DEBUG(logger, msg)
        except Exception as e:
            err_msg = "Error while accessing RemainingPremium for trade <%s>. Error: <%s>." % (self.__trade.Oid(), str(e))
            FRegulatoryLogger.ERROR(logger, err_msg)
        return remaining_premium, err_msg

    # ------------------------------------------------------------- API for Notional Amount -----------------------------------------------------------------------------------
    def notional_amount(self):
        """Returns notional amount for given trade"""
        instrument_type = self.__instrument.InsType()
        if instrument_type.find('/') != -1:
            instrument_type = instrument_type.replace('/', '_')
        if instrument_type.find(' ') != -1:
            instrument_type = instrument_type.replace(' ', '_')
        notional_amount = None
        try:
            if instrument_type in ['Bill', 'Convertible', 'Zero', 'FRN', 'IndexLinkedBond', 'PromisLoan',\
                                   'DualCurrBond', 'Flexi_Bond', 'CD', 'FRA', 'MBS_ABS', 'CLN', 'BasketSecurityLoan',\
                                   'BuySellback', 'Cap', 'Floor', 'Deposit', 'IndexLinkedSwap', \
                                   'CreditDefaultSwap', 'CurrSwap', 'FX_Option', 'TotalReturnSwap', 'Swap', 'Certificate']:
                instrument_type = '_trade_nominal'
            elif instrument_type in ['Bond']:
                instrument_type = '_trade_premium'
            elif instrument_type in ['PriceSwap', 'Average_Future_Forward']:
                instrument_type = '_trade_remaining_premium'
            elif instrument_type in ['Repo_Reverse', 'BasketRepo_Reverse']:
                instrument_type = '_trade_notional_on_start_cash'
            elif self.__trade.IsFxForward():
                if self.__trade.QuantityIsDerived():
                    instrument_type = '_trade_premium'
                else:
                    instrument_type = '_trade_quantity'
            elif (instrument_type == 'Curr' and self.__trade.IsFxSwap()) or \
                instrument_type in ['VarianceSwap', 'VolatilitySwap', 'FXOptionDatedFwd'] or \
                instrument_type == 'Future_Forward' and self.__instrument.Underlying().InsType() == 'Curr':
                instrument_type = '_trade_quantity'
            notional_amount = eval('self.' + instrument_type + '()')
        except Exception as e:
            if instrument_type in ['Combination', 'Commodity', 'Curr', 'Commodity_Index', 'Commodity_Variant',
                                   'Credit_Balance', 'CreditIndex', 'Depositary_Receipt', \
                                   'Dividend_Point_Index', 'ETF', 'EquityIndex', 'FreeDefCF', \
                                   'PriceIndex', 'RateIndex', 'Rolling_Schedule', 'SecurityLoan',\
                                   'Collateral', 'CreditIndex', 'Stock',\
                                   'Fund', 'Portfolio_Swap', 'Fx_Rate', 'Precious_Metal_Rate']:
                raise Exception('Trade Nominal calculation on instrument of type <%s> is currently not supported.' %self.__instrument.InsType())
            else:
                raise Exception('Cannot infer NominalAmount for trade <%d> with instrument type <%s>. Error : <%s>.' %(\
                self.__trade.Oid(), self.__instrument.InsType(), e))
        return notional_amount

