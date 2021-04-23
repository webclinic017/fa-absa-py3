'''
Implementation of Murabaha uploader in Python -- specification
and representation of trades to be created in the
Murabaha transaction.

Project:    Murabaha Uploader
Department: Markets Structuring
Requester:  Gisella Nicola Bascelli
Developer:  Peter Fabian
CR Number:  CHNG0001979991


HISTORY
================================================================================================
Date        CR number       Developer       Description
------------------------------------------------------------------------------------------------
2014-08-14  CHNG0002267615  Nico Louw   Removed FwdDepositTradeSNDesk as it is no longer in use,
                                        and updated the portfolio and mirror portfolio arguments
                                        in the FwdDepositTradeFundingDesk method. Also changed
                                        acquirer 'STRUCT NOTES DESK' to 'ACQ STRUCT DERIV DESK'

------------------------------------------------------------------------------------------------

'''
import acm
import at
import at_choice
from Structured_murabaha_instrument import value_or_exc


class MurabahaTrade(object):
    """ Abstract class for all Murabaha trade objects.
        Supports also add info values.
        Generally the properties of trades are divided into 2 groups --
        a) properties common for all objects of a (sub)class
        b) properties which vary for each object (dates, rates, etc)

        This design allows for interlinking between objects and logically
        divides the constant from variable properties.

        All the data will be provided from Excel file by data provider
        instances.

        Originally the trades should have been linked to Future/Forward
        by using transaction reference, but this does not work
        correctly in one transaction. Therefore it's done
        in post process in a separate transaction.
    """

    def __init__(self, data_provider, ins, logger):
        self._data_provider = data_provider
        self._constants = {}
        self._variables = {}
        self._add_infos = {}
        self.acm_trd = acm.Create("FTrade")
        self.acm_trd.Instrument(ins.acm_ins)
        self.ins = ins
        self.logger = logger
        if not self.acm_trd:
            raise RuntimeError("Could not create trade %s" % self.__class__.__name__)

    def get_variable_data(self):
        raise NotImplementedError('Subclasses must implement this method')

    def _log_property(self, obj, property_, value):
        try:
            value_name = value.Name()
        except:
            value_name = value

        self.logger.log("%s %s: %s\t\t=> %s"
                        % (self.__class__.__name__, obj, property_, value_name),
                        self.logger.DEBUG)

    def commit(self):
        properties = dict(list(self._constants.items()) + list(self._variables.items()))
        for property_, value in properties.items():
            self._log_property("trd", property_, value)
            self.acm_trd.SetProperty(property_, value)

        for add_info_name, add_info_value in self._add_infos.items():
            self._log_property("add info", add_info_name, add_info_value)
            # at.addInfo.save_or_delete(self.acm_trd, add_info_name, add_info_value)
            add_info_name = add_info_name.replace('.', '_46').replace(' ', '_')
            self.acm_trd.AdditionalInfo().SetProperty(add_info_name, add_info_value)
        self.acm_trd.RegisterInStorage()
        self.acm_trd.Commit()

        return self.acm_trd


class FwdHedgeTrade(MurabahaTrade):
    def __init__(self, data_provider, ins, logger):
        super(FwdHedgeTrade, self).__init__(data_provider, ins, logger)
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "Acquirer": value_or_exc(acm.FParty["ACQ STRUCT DERIV DESK"],
                                     "'ACQ STRUCT DERIV DESK' party not found"),
            "Portfolio": value_or_exc(acm.FPhysicalPortfolio["ST Islamic Hedges"],
                                      "'ST Islamic Hedges' prf not found"),
            "DocumentType": value_or_exc(at_choice.get("Standard Document", "ISDA"),
                                         "'ISDA' document type not found"),
            "Text1": "MurabahaTransaction",
            "Status": "Simulated",
            "Type": value_or_exc(acm.EnumFromString("TradeType", "Normal"),
                                 "'Normal' trade type not found"),
        }

        self._add_infos = {
            "Approx. load": "Yes",
            "Approx. load ref": 0,
            "InsOverride": "Not Applicable",
        }

    @staticmethod
    def identifier():
        """ Identify these trades in logs and output file
        """
        return "OTC Fwd Hedge"

    def get_variable_data(self):
        self._variables = {
            "AcquireDay": self._acquire_day(),
            "Counterparty": self._counterparty(),
            "Guarantor": self._guarantor(),
            "Price": self._price(),
            "Quantity": self._quantity(),
            "Trader": self._trader(),
            "TradeTime": self._acquire_day(),
            "ValueDay": self._acquire_day(),

        }

    def _acquire_day(self):
        return self._data_provider.acquire_day().strftime("%Y-%m-%d")

    def _trader(self):
        # current user
        return acm.User()

    def _counterparty(self):
        return acm.FParty[self._data_provider.counterparty()]

    def _guarantor(self):
        return self._counterparty()

    def _price(self):
        return self._data_provider.price()

    def _quantity(self):
        return -1 * self._data_provider.quantity()


class FwdDepositTrade(MurabahaTrade):
    """ Class which holds common data/properties for
        the subclasses. Kind-of like-an abstract class.
    """

    def __init__(self, data_provider, ins, logger):
        super(FwdDepositTrade, self).__init__(data_provider, ins, logger)
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "Guarantor": value_or_exc(acm.FParty["ABSA BANK LTD"],
                                      "'ABSA BANK LTD' party not found"),
            "Price": 100,
            "PrimaryIssuance": False,
            "Text1": "MurabahaTransaction",
            "Status": "Simulated",
            #
            "Type": value_or_exc(acm.EnumFromString("TradeType", "Normal"),
                                 "'Normal' trade type not found"),
        }

        self._add_infos = {
            "Funding Instype": "CL",
        }

    def get_variable_data(self):
        self._variables = {
            "AcquireDay": self._acquire_day(),
            "Premium": self._premium(),
            "Quantity": self._quantity(),
            "TradeTime": self._trade_time(),
            "Trader": self._trader(),
            "ValueDay": self._acquire_day(),

        }

    def _trade_time(self):
        return self._data_provider.trade_time().strftime("%Y-%m-%d")

    def _acquire_day(self):
        acquire_day = self._data_provider.acquire_day()
        trade_time = self._data_provider.trade_time()
        if trade_time > acquire_day:
            raise ValueError("Trade Time %s for Deposits cannot be greater than Value Date %s"
                             % (trade_time, acquire_day))
        return acquire_day.strftime("%Y-%m-%d")

    def _trader(self):
        return acm.User()

    def _premium(self):
        return abs(self._data_provider.premium())

    def _quantity(self):
        return -1 * self._premium() / self.ins.contr_size()


class FwdDepositTradeFundingDesk(FwdDepositTrade):
    def __init__(self, data_provider, ins, logger):
        super(FwdDepositTradeFundingDesk, self).__init__(data_provider, ins, logger)
        self._constants.update({
            "Acquirer": value_or_exc(acm.FParty["Funding Desk"],
                                     "'Funding Desk' party not found"),
            "Counterparty": value_or_exc(acm.FParty["Funding Desk"],
                                         "'Funding Desk' party not found"),
            "Portfolio": value_or_exc(acm.FPhysicalPortfolio["Allocate_Pfolio_GroupFin"],
                                      "'Allocate_Pfolio_GroupFin' prf not found"),
            "MirrorPortfolio": value_or_exc(acm.FPhysicalPortfolio["Group 2476 Shariah"],
                                            "'Group 2476 Shariah' prf not found"),
        })

    @staticmethod
    def identifier():
        """ Identify these trades in logs and output file
        """
        return "MMK SND FRN"


class MurabahaSwapTrade(MurabahaTrade):
    def __init__(self, data_provider, ins, logger):
        super(MurabahaSwapTrade, self).__init__(data_provider, ins, logger)
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "Acquirer": value_or_exc(acm.FParty["IRD DESK"],
                                     "'IRD DESK' party not found"),
            "Counterparty": value_or_exc(acm.FParty["MONEY MARKET DESK"],
                                         "'Money Market Desk' party not found"),
            "Portfolio": value_or_exc(acm.FPhysicalPortfolio["Swap Flow"],
                                      "'Swap Flow' prf not found"),
            "PrimaryIssuance": False,
            "Price": 0,
            "MirrorPortfolio": value_or_exc(acm.FPhysicalPortfolio["Shariah Hedges 1573"],
                                            "'Shariah Hedges 1573' prf not found"),
            "Text1": "MurabahaTransaction",
            "Premium": 0,
            "Status": "Simulated",
            "Type": value_or_exc(acm.EnumFromString("TradeType", "Normal"),
                                 "'Normal' trade type not found"),
        }

    @staticmethod
    def identifier():
        """ Identify these trades in logs and output file
        """
        return "Swap"

    def get_variable_data(self):
        self._variables = {
            "AcquireDay": self._acquire_day(),
            "Quantity": self._quantity(),
            "TradeTime": self._trade_time(),
            "Trader": self._trader(),
            "ValueDay": self._acquire_day(),

        }

    def _acquire_day(self):
        return self._data_provider.acquire_day().strftime("%Y-%m-%d")

    def _trader(self):
        return acm.User()

    def _quantity(self):
        return -1 * self._data_provider.deposit_amount() / self.ins.contract_size()

    def _trade_time(self):
        return self._data_provider.trade_time().strftime("%Y-%m-%d")


class InternalDepositTrade(MurabahaTrade):
    def __init__(self, data_provider, ins, logger):
        super(InternalDepositTrade, self).__init__(data_provider, ins, logger)
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "Acquirer": value_or_exc(acm.FParty["Funding Desk"],
                                     "'Funding Desk' party not found"),
            "Counterparty": value_or_exc(acm.FParty["Funding Desk"],
                                         "'Funding Desk' party not found"),
            "Guarantor": value_or_exc(acm.FParty["ABSA BANK LTD"],
                                      "'ABSA BANK LTD' party not found"),
            "Portfolio": value_or_exc(acm.FPhysicalPortfolio["Shariah Structured Deposits"],
                                      "'Shariah Structured Deposits' prf not found"),
            "PrimaryIssuance": False,
            "MirrorPortfolio": value_or_exc(acm.FPhysicalPortfolio["ST Islamic Accrual"],
                                            "'ST Islamic Accrual' prf not found"),
            "Text1": "MurabahaTransaction",
            "Status": "Simulated",
            #
            "Type": value_or_exc(acm.EnumFromString("TradeType", "Normal"),
                                 "'Normal' trade type not found"),
        }

        self._add_infos = {
            "Funding Instype": "CD",
        }

    @staticmethod
    def identifier():
        """ Identify these trades in logs and output file
        """
        return "Internal Deposit"

    def get_variable_data(self):
        self._variables = {
            "AcquireDay": self._acquire_day(),
            "Price": self._price(),
            "Premium": self._premium(),
            "Quantity": self._quantity(),
            "TradeTime": self._trade_time(),
            "Trader": self._trader(),
            "ValueDay": self._acquire_day(),

        }

    def _acquire_day(self):
        return self._data_provider.acquire_day().strftime("%Y-%m-%d")

    def _trader(self):
        return acm.User()

    def _quantity(self):
        return -1 * self._premium() / self.ins.contract_size()

    def _premium(self):
        return abs(self._data_provider.premium())

    def _price(self):
        return self._data_provider.price() * 100

    def _trade_time(self):
        return self._data_provider.trade_time().strftime("%Y-%m-%d")


class ABSADepositTrade(MurabahaTrade):
    def __init__(self, data_provider, ins, logger):
        super(ABSADepositTrade, self).__init__(data_provider, ins, logger)
        self._constants = {
            "Currency": acm.FCurrency['ZAR'],
            "Acquirer": value_or_exc(acm.FParty["ACQ STRUCT DERIV DESK"],
                                     "'ACQ STRUCT DERIV DESK' party not found"),

            "Guarantor": value_or_exc(acm.FParty["ABSA BANK LTD"],
                                      "'ABSA BANK LTD' party not found"),
            "Portfolio": value_or_exc(acm.FPhysicalPortfolio["ST Islamic Accrual"],
                                      "'ST Islamic Accrual' prf not found"),
            "PrimaryIssuance": False,

            "Text1": "MurabahaTransaction",
            "Status": "Simulated",
            #
            "Type": value_or_exc(acm.EnumFromString("TradeType", "Normal"),
                                 "'Normal' trade type not found"),
        }

        self._add_infos = {
            "Funding Instype": "CD",
        }

    @staticmethod
    def identifier():
        """ Identify these trades in logs and output file
        """
        return "Client Deposit"

    def get_variable_data(self):
        self._variables = {
            "Counterparty": self._counterparty(),
            "AcquireDay": self._acquire_day(),
            "Price": self._price(),
            "Premium": self._premium(),
            "Text2": self._zero_bond_premium(),
            "Quantity": self._quantity(),
            "TradeTime": self._trade_time(),
            "Trader": self._trader(),
            "ValueDay": self._acquire_day(),

        }

    def _acquire_day(self):
        return self._data_provider.acquire_day().strftime("%Y-%m-%d")

    def _counterparty(self):
        return acm.FParty[self._data_provider.counterparty()]

    def _trader(self):
        return acm.User()

    def _quantity(self):
        return self._data_provider.cash() / self.ins.contract_size()

    def _zero_bond_premium(self):
        return self._data_provider._zero_bond_premium()

    def _premium(self):
        return 0.0

    def _price(self):
        return self._data_provider.price() * 100

    def _trade_time(self):
        return self._data_provider.trade_time().strftime("%Y-%m-%d")
