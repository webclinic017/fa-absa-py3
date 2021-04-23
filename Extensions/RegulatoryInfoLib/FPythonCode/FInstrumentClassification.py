import acm, ael
import FRegulatoryLogger
logger = 'FInstrumentClassification'

class FInstrumentClassification(object):
    def __init__(self, instrument, current_date=None):
        self.__instrument = instrument
        self.current_date = current_date

    def CD(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def Bill(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def Bond(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def DualCurrBond(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def Flexi_Bond(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def Convertible(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def Zero(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def FRN(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def IndexLinkedBond(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def PromisLoan(self):
        rts2_instype = 'Bonds'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def CreditDefaultSwap(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        if self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'Credit Index':
            rts2_instype = 'Credit Derivatives'
            rts2_subtype = 'Index credit default swap (CDS)'
            fpml_code = 'IndexCreditDefaultSwap'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() in ['Bill', 'Bond',
                                                                                             'Convertible', 'Zero',
                                                                                             'FRN', 'IndexLinkedBond',
                                                                                             'PromisLoan']:
            rts2_instype = 'Credit Derivatives'
            rts2_subtype = 'Single name credit default swap (CDS)'
            fpml_code = 'SingleNameCreditDefaultSwap'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'Combination':
            rts2_instype = 'Credit Derivatives'
            rts2_subtype = 'Bespoke basket credit default swap (CDS)'
            fpml_code = 'BespokeCreditDefaultSwap'

        else:
            rts2_instype = 'Credit Derivatives'
            rts2_subtype = 'Other credit derivatives'
            fpml_code = 'Other'
        return rts2_instype, rts2_subtype, fpml_code

    def CFD(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        if self.__instrument.Underlying() and self.__instrument.Underlying().InsType() in ['Stock',
                                                                                           'Depository Receipt']:
            rts2_instype = 'Financial contracts for differences'
            rts2_subtype = 'Equity CFDs'
            fpml_code = None
        if self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'Bond':
            rts2_instype = 'Financial contracts for differences'
            rts2_subtype = 'Bond CFDs'
            fpml_code = None
        if self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'EquityIndex':
            rts2_instype = 'Financial contracts for differences'
            rts2_subtype = 'Other CFDs'
            fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def CurrSwap(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        legs = self.__instrument.Legs()
        if all([leg.LegType() == 'Fixed' for leg in legs]):
            rts2_instype = 'Interest Rate Derivatives'
            rts2_subtype = "Fixed-to-Fixed 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Fixed-to-Fixed 'multi-currency swaps' or 'cross-currency swaps'"
            fpml_code = 'FixedFixed:CrossCurrency'
        elif any([leg.LegType() == 'Fixed' for leg in legs]) and any(
                [leg.LegType() == 'Float' for leg in legs]):
            rts2_instype = 'Interest Rate Derivatives'
            rts2_subtype = "Fixed-to-Float 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Fixed-to-Float 'multi-currency swaps' or 'cross-currency swaps'"
            fpml_code = 'FixedFloat:CrossCurrency'
        elif all([leg.LegType() == 'Float' for leg in legs]):
            rts2_instype = 'Interest Rate Derivatives'
            rts2_subtype = "Float-to-Float 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Float-to-Float 'multi-currency swaps' or 'cross-currency swaps'"
            fpml_code = 'FloatFloat:CrossCurrency'
        for leg in self.__instrument.Legs():
            if leg.LegType() == 'Float':
                if leg.RollingPeriodCount() == 1 and leg.RollingPeriodUnit() == "Days":
                    rts2_instype = 'Interest Rate Derivatives'
                    rts2_subtype = "Overnight Index Swap (OIS) 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Overnight Index Swap (OIS) 'multi-currency swaps' or 'cross-currency swaps'"
                    fpml_code = 'OIS:CrossCurrency'
        return rts2_instype, rts2_subtype, fpml_code

    def Future_Forward(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''

        if self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'CurrSwap':
            legs = self.__instrument.Legs()
            if all([leg.LegType() == 'Fixed' for leg in legs]):
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = "Fixed-to-Fixed 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Fixed-to-Fixed 'multi-currency swaps' or 'cross-currency swaps'"
                fpml_code = 'FixedFixed:CrossCurrency'
            elif any([leg.LegType() == 'Fixed' for leg in legs]) and any(
                    [leg.LegType() == 'Float' for leg in legs]):
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = "Float-to-Float 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Float-to-Float 'multi-currency swaps' or 'cross-currency swaps'"
                fpml_code = 'FixedFloat:CrossCurrency'
            elif all([leg.LegType() == 'Float' for leg in legs]):
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = "Float-to-Float 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Float-to-Float 'multi-currency swaps' or 'cross-currency swaps'"
                fpml_code = 'FloatFloat:CrossCurrency'
            for leg in self.__instrument.Legs():
                if leg.LegType() == 'Float':
                    if leg.RollingPeriodCount() == 1 and leg.RollingPeriodUnit() == "Days":
                        rts2_instype = 'Interest Rate Derivatives'
                        rts2_subtype = "Overnight Index Swap (OIS) 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Overnight Index Swap (OIS) 'multi-currency swaps' or 'cross-currency swaps'"
                        fpml_code = 'OIS:CrossCurrency'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'Dividend Point Index':
            rts2_instype = 'Equity Derivatives'
            rts2_subtype = 'Dividend index futures/ forwards'
            fpml_code = 'DividendIndexFutureForward'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'ETF':
            rts2_instype = 'Equity Derivatives'
            rts2_subtype = 'ETF futures/ forwards'
            fpml_code = 'ETFFutureForward'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() in ['Stock',
                                                                                             'Depository Receipt']:
            rts2_instype = 'Equity Derivatives'
            rts2_subtype = 'Stock futures/ forwards'
            fpml_code = 'StockFutureForward'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'EquityIndex':
            rts2_instype = 'Equity Derivatives'
            rts2_subtype = 'Stock index futures/ forwards'
            fpml_code = 'StockIndexFutureForward'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'Curr' and not self.__instrument.Otc():
            rts2_instype = 'Foreign Exchange Derivatives'
            rts2_subtype = 'FX futures'
            fpml_code = 'Future'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() in ['Bill', 'Bond',
                                                                                             'Convertible', 'Zero',
                                                                                             'CLN', 'FRN',
                                                                                             'IndexLinkedBond',
                                                                                             'PromisLoan']:
            rts2_instype = 'Interest Rate Derivatives'
            rts2_subtype = 'Bond futures/forwards'
            fpml_code = 'BondFutureForward'
        elif self.__instrument.Underlying().InsType() == 'Combination':
            for leg in self.__instrument.Legs():
                instrument_map = leg.FloatRateReference().InstrumentMaps()
                if all([ins.Instrument().InsType() in ['Stock', 'EquityIndex', 'ETF', 'Depositary Receipt',
                                                                   'Dividend Point Index'] for ins in instrument_map]):
                    rts2_instype = 'Equity Derivatives'
                    rts2_subtype = 'Other equity derivatives'
                    fpml_code = 'Other'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'Curr':
            settlement_type = self.__instrument.SettlementType()
            if settlement_type == 'Physical Delivery' and self.__instrument.Otc():
                rts2_instype = 'Foreign Exchange Derivatives'
                rts2_subtype = 'Deliverable forward(DF)'
                fpml_code = 'DeliverableForward'
            elif settlement_type == 'Cash' and self.__instrument.Otc():
                rts2_instype = 'Foreign Exchange Derivatives'
                rts2_subtype = 'Non-deliverable forward (NDF)'
                fpml_code = 'NonDeliverableForward'
        elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'Swap':
            legs = self.__instrument.Underlying().Legs()
            if all([leg.LegType() == 'Fixed' for leg in legs]):
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = "Fixed-to-Fixed 'single currency swaps' and futures/forwards on Fixed-to-Fixed 'single currency swaps'"
                fpml_code = 'FixedFixed:SingleCurrency'
            elif any([leg.LegType() == 'Fixed' for leg in legs]) and any(
                    [leg.LegType() == 'Float' for leg in legs]):
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = "Fixed-to-Float 'single currency swaps' and futures/forwards on Fixed-to-Float 'single currency swaps'"
                fpml_code = 'FixedFloat:SingleCurrency'
            elif all([leg.LegType() == 'Float' for leg in legs]):
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = "Float-to-Float 'single currency swaps' and futures/forwards on Float-to-Float 'single currency swaps'"
                fpml_code = 'FloatFloat:SingleCurrency'
            for leg in self.__instrument.Legs():
                if leg.LegType() == 'Float':
                    if leg.RollingPeriodCount() == 1 and leg.RollingPeriodUnit() == 'Days':
                        rts2_instype = 'Interest Rate Derivatives'
                        rts2_subtype = "Overnight Index Swap (OIS) 'single currency swaps' and futures/forwards on Overnight Index Swap (OIS) 'single currency swaps'"
                        fpml_code = 'OIS:SingleCurrency'

        for leg in self.__instrument.Legs():
            if leg.FloatRateReference().InsType() == 'PriceIndex':
                curr = {l.Currency().Name() for l in self.__instrument.Legs()}
                if len(curr) > 1:
                    rts2_instype = 'Interest Rate Derivatives'
                    rts2_subtype = "Inflation 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Inflation 'multi-currency swaps' or 'cross-currency swaps'"
                    fpml_code = 'Inflation:CrossCurrency'
                else:
                    rts2_instype = 'Interest Rate Derivatives'
                    rts2_subtype = "Inflation 'single currency swaps' and futures/forwards on Inflation 'single currency swaps'"
                    fpml_code = 'Inflation:SingleCurrency'

        underlying = self.__instrument.Underlying()
        if underlying and underlying.InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index']:
            try:
                if underlying.RegulatoryInfo() and underlying.RegulatoryInfo().CommodityBaseProduct():
                    if underlying.RegulatoryInfo().CommodityBaseProduct().Name() == 'AGRI':
                        rts2_instype = 'Commodity Derivatives'
                        rts2_subtype = 'Agricultural commodity futures/forwards'
                        fpml_code = 'AgriculturalCommodityFutureForward'
                    elif underlying.RegulatoryInfo().CommodityBaseProduct().Name() == 'METL':
                        rts2_instype = 'Commodity Derivatives'
                        rts2_subtype = 'Metal commodity futures/forwards'
                        fpml_code = None
                    elif underlying.RegulatoryInfo().CommodityBaseProduct().Name() == 'NRGY':
                        rts2_instype = 'Commodity Derivatives'
                        rts2_subtype = 'Energy commodity futures/forwards'
                        fpml_code = None
                    elif underlying.RegulatoryInfo().CommodityBaseProduct().Name() not in ['AGRI', 'METL', 'NRGY']:
                        rts2_instype = 'Commodity Derivatives'
                        rts2_subtype = 'Other commodity derivatives'
                        fpml_code = 'Other'
                else:
                    rts2_instype = 'Commodity Derivatives'
                    rts2_subtype = 'Other commodity derivatives'
                    fpml_code = 'Other'
            except Exception as e:
                FRegulatoryLogger.ERROR(logger, "RegulatorySupport package needs to be installed to use this functionality")
        return rts2_instype, rts2_subtype, fpml_code

    def Certificate(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        if self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'EquityIndex':
            rts2_instype = 'Equity Derivatives'
            rts2_subtype = 'Stock index futures/ forwards'
            fpml_code = 'StockIndexFutureForward'
        return rts2_instype, rts2_subtype, fpml_code

    def Deposit_Loan(self):
        rts2_instype = 'Interest Rate Derivatives'
        rts2_subtype = 'Other Interest Rate Derivatives'
        fpml_code = 'Other'
        return rts2_instype, rts2_subtype, fpml_code

    def FRA(self):
        rts2_instype = 'Interest Rate Derivatives'
        rts2_subtype = 'IR futures and FRA'
        fpml_code = 'FutureFra'
        return rts2_instype, rts2_subtype, fpml_code

    def Average_Future_Forward(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''

        for leg in self.__instrument.Legs():
            if leg.LegType() == 'Float' and leg.FloatRateReference():
                if leg.FloatRateReference().InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index']:
                    try:
                        if leg.FloatRateReference().RegulatoryInfo() and leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct():
                            if leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct().Name() == 'AGRI':
                                rts2_instype = 'Commodity Derivatives'
                                rts2_subtype = 'Agricultural commodity futures/forwards'
                                fpml_code = 'AgriculturalCommodityFutureForward'
                            elif leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct().Name() == 'METL':
                                rts2_instype = 'Commodity Derivatives'
                                rts2_subtype = 'Metal commodity futures/forwards'
                                fpml_code = None
                            elif leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct().Name() == 'NRGY':
                                rts2_instype = 'Commodity Derivatives'
                                rts2_subtype = 'Energy commodity futures/forwards'
                                fpml_code = None
                            elif leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct().Name() not in ['AGRI',
                                                                                                                 'METL',
                                                                                                                 'NRGY']:
                                rts2_instype = 'Commodity Derivatives'
                                rts2_subtype = 'Other commodity derivatives'
                                fpml_code = 'Other'
                        else:
                            rts2_instype = 'Commodity Derivatives'
                            rts2_subtype = 'Other commodity derivatives'
                            fpml_code = 'Other'
                    except Exception as e:
                        FRegulatoryLogger.ERROR(logger, "RegulatorySupport package needs to be installed to use this functionality")
        return rts2_instype, rts2_subtype, fpml_code

    def Option(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        if self.__instrument.Underlying():

            if self.__instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index']:
                try:
                    if self.__instrument.Underlying().RegulatoryInfo() and self.__instrument.Underlying().RegulatoryInfo().CommodityBaseProduct():
                        if self.__instrument.Underlying().RegulatoryInfo().CommodityBaseProduct().Name() == "AGRI":
                            rts2_instype = 'Commodity Derivatives'
                            rts2_subtype = 'Agricultural commodity options'
                            fpml_code = 'AgriculturalCommodityOption'
                        elif self.__instrument.Underlying().RegulatoryInfo().CommodityBaseProduct().Name() == 'METL':
                            rts2_instype = 'Commodity Derivatives'
                            rts2_subtype = 'Metal commodity options'
                            fpml_code = None
                        elif self.__instrument.Underlying().RegulatoryInfo().CommodityBaseProduct().Name() == 'NRGY':
                            rts2_instype = 'Commodity Derivatives'
                            rts2_subtype = 'Energy commodity options'
                            fpml_code = None
                        elif self.__instrument.Underlying().RegulatoryInfo().CommodityBaseProduct().Name() not in [
                            'AGRI', 'METL', 'NRGY']:
                            rts2_instype = 'Commodity Derivatives'
                            rts2_subtype = 'Other commodity derivatives'
                            fpml_code = 'Other'
                    else:
                        rts2_instype = 'Commodity Derivatives'
                        rts2_subtype = 'Other commodity derivatives'
                        fpml_code = 'Other'
                except Exception as e:
                    FRegulatoryLogger.ERROR(logger, "RegulatorySupport package needs to be installed to use this functionality")

            elif self.__instrument.Underlying().InsType() == 'ETF':
                rts2_instype = 'Equity Derivatives'
                rts2_subtype = 'ETF options'
                fpml_code = 'ETFOption'
            elif self.__instrument.Underlying().InsType() == 'EquityIndex':
                rts2_instype = 'Equity Derivatives'
                rts2_subtype = 'Stock index options'
                fpml_code = 'StockIndexOption'
            elif self.__instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
                rts2_instype = 'Equity Derivatives'
                rts2_subtype = 'Stock options'
                fpml_code = 'StockOption'
            elif self.__instrument.Underlying().InsType() == 'RateIndex':
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = 'IR options'
                fpml_code = 'Option'
            elif self.__instrument.Underlying().InsType() in ['Swap', 'CurrSwap']:
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = 'Swaptions'
                fpml_code = 'Swaption'
            elif self.__instrument.Underlying().InsType() == 'Curr':
                settlement_type = self.__instrument.SettlementType()
                if settlement_type == 'Physical Delivery':
                    rts2_instype = 'Foreign Exchange Derivatives'
                    rts2_subtype = 'Deliverable FX options (DO)'
                    fpml_code = 'DeliverableOption'
                elif settlement_type == 'Cash':
                    rts2_instype = 'Foreign Exchange Derivatives'
                    rts2_subtype = 'Non-Deliverable FX options (NDO)'
                    fpml_code = 'NonDeliverableOption'

            elif self.__instrument.Underlying().InsType() == 'CreditDefaultSwap':
                if self.__instrument.Underlying().Underlying() and self.__instrument.Underlying().Underlying().InsType() == 'CreditIndex':
                    rts2_instype = 'Credit Derivatives'
                    rts2_subtype = 'CDS index options'
                    fpml_code = 'IndexOption'
                elif self.__instrument.Underlying().Underlying() and self.__instrument.Underlying().Underlying().InsType() in [
                    'Bill', 'Bond', 'Convertible',
                    'Zero', 'FRN', 'IndexLinkedBond', 'PromisLoan']:
                    rts2_instype = 'Credit Derivatives'
                    rts2_subtype = 'Single name CDS options'
                    fpml_code = 'SingleNameOption'
            elif self.__instrument.Underlying().InsType() in ['Bill', 'Bond', 'Convertible', 'Zero', 'CLN', 'FRN',
                                                              'IndexLinkedBond', 'PromisLoan']:
                rts2_instype = 'Interest Rate Derivatives'
                rts2_subtype = 'Bond options'
                fpml_code = 'BondOption'

            elif self.__instrument.Underlying() and self.__instrument.Underlying().InsType() == 'Combination':
                if all([ins.Instrument().InsType() in ['Stock', 'EquityIndex', 'ETF', 'Depositary Receipt',
                                                                   'Dividend Point Index'] for ins in self.__instrument.Underlying().InstrumentMaps()]):
                    rts2_instype = 'Equity Derivatives'
                    rts2_subtype = 'Other equity derivatives'
                    fpml_code = 'Other'
        return rts2_instype, rts2_subtype, fpml_code

    def FX_Option(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        settlement_type = self.__instrument.SettlementType()
        if settlement_type == 'Physical Delivery':
            rts2_instype = 'Foreign Exchange Derivatives'
            rts2_subtype = 'Deliverable FX options (DO)'
            fpml_code = 'DeliverableOption'
        elif settlement_type == 'Cash':
            rts2_instype = 'Foreign Exchange Derivatives'
            rts2_subtype = 'Non-Deliverable FX options (NDO)'
            fpml_code = 'NonDeliverableOption'
        return rts2_instype, rts2_subtype, fpml_code

    def Swap(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        legs = self.__instrument.Legs()
        if all([leg.LegType() == 'Fixed' for leg in legs]):
            rts2_instype = 'Interest Rate Derivatives'
            rts2_subtype = "Fixed-to-Fixed 'single currency swaps' and futures/forwards on Fixed-to-Fixed 'single currency swaps'"
            fpml_code = 'FixedFixed:SingleCurrency'
        elif any([leg.LegType() == 'Fixed' for leg in legs]) and any(
                [leg.LegType() == 'Float' for leg in legs]):
            rts2_instype = 'Interest Rate Derivatives'
            rts2_subtype = "Fixed-to-Float 'single currency swaps' and futures/forwards on Fixed-to-Float 'single currency swaps'"
            fpml_code = 'FixedFloat:SingleCurrency'
        elif all([leg.LegType() == 'Float' for leg in legs]):
            rts2_instype = 'Interest Rate Derivatives'
            rts2_subtype = "Float-to-Float 'single currency swaps' and futures/forwards on Float-to-Float 'single currency swaps'"
            fpml_code = 'FloatFloat:SingleCurrency'

        elif self.__instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index']:
            rts2_instype = 'Commodity Derivatives'
            rts2_subtype = 'Other commodity derivatives'
            fpml_code = 'Other'

        for leg in self.__instrument.Legs():
            if leg.LegType() == 'Float':
                if leg.RollingPeriodCount() == 1 and leg.RollingPeriodUnit() == 'Days':
                    rts2_instype = 'Interest Rate Derivatives'
                    rts2_subtype = "Overnight Index Swap (OIS) 'single currency swaps' and futures/forwards on Overnight Index Swap (OIS) 'single currency swaps'"
                    fpml_code = 'OIS:SingleCurrency'
        return rts2_instype, rts2_subtype, fpml_code

    def FXOptionDatedFwd(self):
        rts2_instype = 'Foreign Exchange Derivatives'
        rts2_subtype = 'Deliverable forward (DF)'
        fpml_code = 'DeliverableForward'
        return rts2_instype, rts2_subtype, fpml_code

    def FXNDF(self):
        rts2_instype = 'Foreign Exchange Derivatives'
        rts2_subtype = 'Non-deliverable forward (NDF)'
        fpml_code = 'NonDeliverableForward'
        return rts2_instype, rts2_subtype, fpml_code

    def MBS_ABS(self):
        rts2_instype = 'Structured Finance Products (SFPs)'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def CLN(self):
        rts2_instype = 'Structured Finance Products (SFPs)'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def BasketRepo_Reverse(self):
        rts2_instype = 'Structured Finance Products (SFPs)'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def BasketSecurityLoan(self):
        rts2_instype = 'Structured Finance Products (SFPs)'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def BuySellback(self):
        rts2_instype = 'Structured Finance Products (SFPs)'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def Cap(self):
        rts2_instype = 'Interest Rate Derivatives'
        rts2_subtype = 'IR options'
        fpml_code = 'Option'
        return rts2_instype, rts2_subtype, fpml_code

    def Floor(self):
        rts2_instype = 'Interest Rate Derivatives'
        rts2_subtype = 'IR options'
        fpml_code = 'Option'
        return rts2_instype, rts2_subtype, fpml_code

    def IndexLinkedSwap(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        for leg in self.__instrument.Legs():
            if leg.LegType() == 'Float':
                if leg.RollingPeriodCount() == 1 and leg.RollingPeriodUnit() == 'Days':
                    rts2_instype = 'Interest Rate Derivatives'
                    rts2_subtype = "Overnight Index Swap (OIS) 'single currency swaps' and futures/forwards on Overnight Index Swap (OIS) 'single currency swaps'"
                    fpml_code = 'OIS:SingleCurrency'
        return rts2_instype, rts2_subtype, fpml_code

    def Repo_Reverse(self):
        rts2_instype = 'Structured Finance Products (SFPs)'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def PriceSwap(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        for leg in self.__instrument.Legs():
            if leg.LegType() == 'Float' and leg.FloatRateReference():
                if leg.FloatRateReference().InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index']:
                    rts2_instype = 'Commodity Derivatives'
                    rts2_subtype = 'Other commodity derivatives'
                    fpml_code = 'Other'
        return rts2_instype, rts2_subtype, fpml_code

    def TotalReturnSwap(self):
        rts2_instype = ''
        rts2_subtype = ''
        fpml_code = ''
        for leg in self.__instrument.Legs():
            if leg.LegType() == 'Total Return' and leg.FloatRateReference():
                if leg.FloatRateReference().InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index']:

                    try:
                        if leg.FloatRateReference().RegulatoryInfo() and leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct():
                            if leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct().Name() == "AGRI":
                                rts2_instype = 'Commodity Derivatives'
                                rts2_subtype = 'Agricultural commodity swaps'
                                fpml_code = 'AgriculturalCommoditySwap'
                            elif leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct().Name() == "NRGY":
                                rts2_instype = 'Commodity Derivatives'
                                rts2_subtype = 'Energy commodity swaps'
                                fpml_code = 'EnergyCommoditySwap'
                            elif leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct().Name() == "METL":
                                rts2_instype = 'Commodity Derivatives'
                                rts2_subtype = 'Metal commodity swaps'
                                fpml_code = None
                            elif leg.FloatRateReference().RegulatoryInfo().CommodityBaseProduct().Name() not in ['AGRI',
                                                                                                                 'METL',
                                                                                                                 'NRGY']:
                                rts2_instype = 'Commodity Derivatives'
                                rts2_subtype = 'Other commodity derivatives'
                                fpml_code = 'Other'
                        else:
                            rts2_instype = 'Commodity Derivatives'
                            rts2_subtype = 'Other commodity derivatives'
                            fpml_code = 'Other'
                    except Exception as e:
                        FRegulatoryLogger.ERROR(logger, "RegulatorySupport package needs to be installed to use this functionality")

                elif leg.FloatRateReference().InsType() in ['Stock', 'EquityIndex', 'Dividend Point Index', 'ETF',
                                                            'Depository Receipt']:
                    rts2_instype = 'Equity Derivatives'
                    rts2_subtype = 'Swaps'
                    fpml_code = 'Swap'
                elif leg.FloatRateReference().InsType() == 'Combination' and all([ins.Instrument().InsType() in ['Stock', 'EquityIndex', 'ETF', 'Depositary Receipt',
                                                                   'Dividend Point Index'] for ins in leg.FloatRateReference().InstrumentMaps()]):
                    rts2_instype = 'Equity Derivatives'
                    rts2_subtype = 'Portfolio Swaps'
                    fpml_code = 'PortfolioSwap'
                elif leg.FloatRateReference().InsType() == 'PriceIndex':
                    curr = {l.Currency().Name() for l in self.__instrument.Legs()}
                    if len(curr) > 1:
                        rts2_instype = 'Interest Rate Derivatives'
                        rts2_subtype = "Inflation 'multi-currency swaps' or 'cross-currency swaps' and futures/forwards on Inflation 'multi-currency swaps' or 'cross-currency swaps'"
                        fpml_code = 'Inflation:CrossCurrency'
                    else:
                        rts2_instype = 'Interest Rate Derivatives'
                        rts2_subtype = "Inflation 'single currency swaps' and futures/forwards on Inflation 'single currency swaps'"
                        fpml_code = 'Inflation:SingleCurrency'
        return rts2_instype, rts2_subtype, fpml_code

    def Warrant(self):
        rts2_instype = 'Securitised Derivatives'
        rts2_subtype = None
        fpml_code = None
        return rts2_instype, rts2_subtype, fpml_code

    def __instrument_classification(self):
        instrument_type = self.__instrument.InsType()
        if instrument_type.find('/') != -1:
            instrument_type = instrument_type.replace('/', '_')
        if instrument_type.find(' ') != -1:
            instrument_type = instrument_type.replace(' ', '_')
        ins_type = None
        sub_type = None
        fpml_code = None
        try:
            ins_type, sub_type, fpml_code = eval('self.' + instrument_type + '()')
        except Exception as e:
            if instrument_type in ['Combination', 'Commodity', 'Curr', 'Commodity_Index', 'Commodity_Variant',
                                   'Credit_Balance', 'CreditIndex', 'Depositary_Receipt', 'Deposit',
                                   'Dividend_Point_Index', 'ETF', 'EquityIndex', 'FreeDefCF', 'FxSwap', 'PriceIndex',
                                   'PriceSwap', 'RateIndex', 'Rolling_Schedule', 'SecurityLoan', 'Stock',
                                   'VarianceSwap', 'VolatilitySwap']:
                pass
            else:
                FRegulatoryLogger.ERROR(logger, "Could not infer the instrument classification. Error: <%s>"%str(e))

        return ins_type, sub_type, fpml_code

    def fpml_code(self):
        ins_type, subtype, fpml_code = self.__instrument_classification()
        return fpml_code

    def mifid2_rts2_instype(self):
        ins_type, subtype, fpml_code = self.__instrument_classification()
        return ins_type

    def mifid2_rts2_inssubtype(self):
        ins_type, subtype, fpml_code = self.__instrument_classification()
        return subtype



