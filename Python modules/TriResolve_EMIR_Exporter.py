




# coding=ascii
"""
Brendan Bosman      MINT-164.3      2015/09/03    1. Refactored from TR_EMIRReportGenerastor
Brendan Bosman      MINT-366        2015/09/15    Implement Non EU files
Brendan Bosman      MINT-453        2015/12/08    Additional changes to Tri Resolve to use FA values instead of Midas values for trades dual key trades that are specified as "outright spot"
Melusi Maseko       FXFA-2674       2016/07/11    Made FxF changes to exclude REUTERS
Melusi Maseko       FXFA-3037       2016/07/19    Made FxF changes to exclude AOL
Heinrich Cronje     FXFA-2703       2016/08/11    Made FxF changes to exclude BARX STP, BARX PRF and OWM
Heinrich Cronje     FXFA-2696       2016/09/01    Made FxF changes to exclude SMML
Melusi Maseko       FXFA-3400       2016/07/19    Made FxF changes to exclude BIICM
Melusi Maseko       MINT-985        2016/12/05    Ammend logic of equal and opposite for MIDAS DUAL KEY trades
Melusi Maseko       CHNG0004232355  2017/01/11    Exclude Midas Dual Key trades for cp '10538' and '522623' to avoid duplicates. These trades are being fed through the FA task
Melusi Maseko       MINT-998        2017/01/19    Amend logic of equal and opposite trades to ignore decimals on Notional for except for Midas Dual Key trades for cp '10538' and '522623'
Melusi Maseko       MINT-1000       2017-01-27    Ammend equal and opposite logic for all Barclay's CP trades (CP_ID 10538 and 522623)
Melusi Maseko       MINT-1003       2017-04-12    Exclude all shadow deals from the TriOptima population 
Bhavik Mistry       ABITFA-4906     2017-05-25    Include near legs of fx swaps where far legs have passed the filter
Bhavik Mistry       ABITFA-4924     2017-06-09    Added new Trade Group ID column for swap trades
Main Purpose:
1. Class declarations of the export features

"""

import os
import acm
import ael
import time
import csv
import traceback
import StringIO
import TriResolve_EMIR_Functions
from TriResolve_EMIR_MidasTradeColl import *


class EMIRExport(object):
    """

    :param context:
    """

    def __init__(self, context):
        """

        :param context:
        :return:
        """
        self.context = context
        filename = self.get_context().get_issue_output_path()
        if filename:
            self._error_output = open(self.get_context().get_issue_output_path(), 'w')
        else:
            self._error_output = StringIO.StringIO("")

        self._written_midas_ids = {}
        self._written_front_ids = {}

    def get_written_midas_ids(self):
        """


        :return:
        """
        return self._written_midas_ids

    def get_written_front_ids(self):
        """


        :return:
        """
        return self._written_front_ids

    def create_fieldnames(self):
        """ Return a list of colums names

        :rtype : tuple
        :return:
        """
        return [
            COL_TRADE_ID, COL_TRADE_GROUP_ID, COL_PARTY_ID, COL_CP_ID, COL_PRODUCT_CLASS, COL_TRADE_DATE,
            COL_START_DATE, COL_END_DATE, COL_NOTIONAL, COL_TRADE_CURR, COL_NOTIONAL_2,
            COL_TRADE_CURR_2, COL_UNDERLYING, COL_UNDERLYING_ISIN, COL_MTM_DATE, COL_MTM_VALUE,
            COL_MTM_CURR, COL_CP_TRADE_ID, COL_SWAPSWIRE_ID, COL_PAY_REC, COL_STRIKE_PRICE, COL_OPTION_TYPE,
            COL_BOOK, COL_LEI, COL_DATA_SOURCE, COL_RATE, COL_COUPON_RATE,
            XCOL_COLLATERALIZED, XCOL_OPTIONAL_KEY, XCOL_OTC, XCOL_INSTYPE]

    def create_writer(self, iostream):
        """
        Create a dict writer with. Columns is from the method called fieldnames


        :rtype : csv.DictWriter
        :param iostream:
        :return:
        """
        fieldnames = self.create_fieldnames()
        writer = csv.DictWriter(iostream, fieldnames, extrasaction='ignore', delimiter='\t', lineterminator='\n')
        return writer

    def get_context(self):
        """


        :rtype : BaseEMIRContext
        :return:
        """
        return self.context

    def write_error(self, message, *args):
        """Writes non-critical error to an error log file.
        :param args:
        :param message:
        """
        formatted_message = message.format(*args)
        print formatted_message
        self._error_output.write(formatted_message + '\n')

    def get_trade_row(self, trd, cp_collateralized=NON_COLLATERALIZED, flt=FLT_ENABLE, use_counter_party_name=False):
        """Returns a dictionary of data for EMIR report for specified trade.
        :param use_counter_party_name:
        :param flt:
        :param cp_collateralized:
        :param trd:
            """
        ins = trd.Instrument()
        ins_type = ins.InsType()
        trade_date = norm_date(trd.TradeTime())

        # This is a test to make sure that there is no duplicte trades id's written to file
        if trd.Oid() in self.get_written_front_ids():
            return

        # For TRS "Expiry" field in PRIME refers to leg's end date.
        expiry = ins.FirstPayLeg().EndDate() if ins.IsKindOf(acm.FTotalReturnSwap) else ins.ExpiryDate()
        expiry = norm_date(expiry)
        value_date = norm_date(trd.ValueDay())

        # Call filter trade
        if flt == FLT_ENABLE and not self.filter_trade(trd):
            return

        # write trade id into list
        self.get_written_front_ids()[trd.Oid()] = None
        midas_id = get_midas_id(trd, ai_fallback=True)
        if midas_id:
            self.get_written_midas_ids()[midas_id] = None

        data = {COL_TRADE_ID: trd.Oid(), COL_PARTY_ID: 'ABSABANK'}
        
        # Add Far leg trade number to trade group id column for both legs of swap
        if trd.IsFxSwapFarLeg():
            data[COL_TRADE_GROUP_ID] = trd.Oid()
        elif trd.IsFxSwapNearLeg():
            data[COL_TRADE_GROUP_ID] = trd.FxSwapNearLeg().Oid()

        ctpy_obj = trd.Counterparty()

        if ctpy_obj.Name() == 'MIDAS DUAL KEY':
            midas_party_id = int(trd.AdditionalInfo().Source_Ctpy_Id())

            if midas_party_id in self.get_context().get_le_names_by_midas_id():
                data[COL_CP_ID] = self.get_context().get_le_names_by_midas_id()[midas_party_id]
            else:
                le_name = trd.AdditionalInfo().Source_Ctpy_Name()
                data[COL_CP_ID] = le_name
                print "Warning! Counterparty", midas_party_id, "is not in the mapping file! Using", le_name, "instead."

                # try:
                #
                #     le_name = self.get_context().get_le_names_by_midas_id()[midas_party_id]
                # except KeyError:
                #     le_name = trd.AdditionalInfo().Source_Ctpy_Name()
                #     print "Warning! Counterparty", midas_party_id, "is not in the mapping file! Using", le_name, "instead."
        else:
            if use_counter_party_name:
                le_name = ctpy_obj.Name()
                data[COL_CP_ID] = le_name
            else:
                le_name = self.get_context().get_le_names_by_front_id()[ctpy_obj.Oid()]
                data[COL_CP_ID] = le_name

        data[COL_TRADE_DATE] = trade_date

        if ins.IsKindOf(acm.FTotalReturnSwap):
            data[COL_END_DATE] = ins.EndDate()
        else:
            data[COL_END_DATE] = expiry or value_date

        (nom1, curr1), (nom2, curr2) = self.get_nominals(trd)
        data[COL_NOTIONAL] = nom1 and abs(nom1)
        data[COL_TRADE_CURR] = curr1
        data[COL_NOTIONAL_2] = nom2 and abs(nom2)
        data[COL_TRADE_CURR_2] = curr2

        und, isin = self.get_und_type_isin(ins)
        data[COL_UNDERLYING] = und
        data[COL_UNDERLYING_ISIN] = isin
        data[COL_PRODUCT_CLASS] = product_class(trd) or und or ins_type

        mtm_val, mtm_curr = mtm_val_curr(trd)
        data[COL_MTM_DATE] = self.get_context().get_today()
        data[COL_MTM_VALUE], data[COL_MTM_CURR] = mtm_val, mtm_curr

        data[COL_CP_TRADE_ID] = trd.YourRef()

        if trd.OptionalKey() and trd.OptionalKey().startswith('MW'):
            data[COL_SWAPSWIRE_ID] = trd.OptionalKey()  # market wire id

        data[COL_PAY_REC] = self.get_payrec(trd)

        if ins.IsKindOf(acm.FCreditDefaultSwap):
            data[COL_START_DATE] = trd.AcquireDay()
        else:
            data[COL_START_DATE] = (ins.StartDate() or trade_date) if expiry else trade_date

        if ins_type == 'Option':
            data[COL_STRIKE_PRICE] = ins.StrikePrice()
            data[COL_OPTION_TYPE] = 'Call' if ins.IsCallOption() else 'Put'

        if ins.IsKindOf(acm.FPriceSwap):
            data[COL_STRIKE_PRICE] = ins.FirstFixedLeg().FixedPrice()

        if ins.IsKindOf(acm.FCurrency) and is_precmet(ins, trd.Currency()):
            data[COL_STRIKE_PRICE] = trd.Price()

        data[COL_BOOK] = trd.Portfolio().Name()

        data[COL_LEI] = ABSA_LEI

        data[COL_DATA_SOURCE] = DATA_SOURCE_FRONT

        data[COL_RATE] = trd.Price()

        if ins_type == 'FRA':
            data[COL_COUPON_RATE] = ins.Legs()[0].FixedRate()  # always one leg
        elif ins_type == 'Swap':
            fixed_legs = [l for l in ins.Legs() if l.LegType() == 'Fixed']
            if len(fixed_legs) == 1:
                data[COL_COUPON_RATE] = fixed_legs[0].FixedRate()

        if not (COL_STRIKE_PRICE in data) and COL_COUPON_RATE in data:
            # copy the values from coupon rate to strike
            data[COL_STRIKE_PRICE] = data[COL_COUPON_RATE]

        data[XCOL_COLLATERALIZED] = self.get_collateralized(trd, cp_collateralized)

        data[XCOL_OPTIONAL_KEY] = trd.OptionalKey()

        data[XCOL_OTC] = ins.Otc()
        data[XCOL_INSTYPE] = ins.InsType()

        return data

    def cf_nominal(self, leg, trade):
        """Return cashflow nominal amount or None.
        :param trade:
        :param leg:
        """
        leg_curr = leg.Currency().Name()
        has_cf = 0
        res = 0.0
        for cf in leg.CashFlows():
            if cf.StartDate() > self.get_context().get_today() or cf.EndDate() <= self.get_context().get_today():
                continue
            if cf.CashFlowType() in ['Return', 'Credit Default', 'Total Return']:
                continue
            has_cf = 1
            mf = acm.Risk().CreateMoneyFlowFromObject(cf, trade)
            res += acs.calculate_value('FMoneyFlowSheet', mf, 'Cash Analysis Nominal', vector_currs=[leg_curr]).Number()
        nom = res if has_cf else False

        return nom if nom is not False else None

    def get_nominals(self, trd):
        """Return ((nominal1, currency1), (nominal2, currency2)) for specified trade.
        :param trd:
        """
        ins = trd.Instrument()
        ins_type = ins.InsType()

        if trd.IsFxSwap():  # use t.Quantity and t.Premium
            nom1, curr1 = trd.Premium(), trd.Currency().Name()  # far trade first
            nom2, curr2 = trd.Nominal(), ins.Name()
        elif ins.IsKindOf(acm.FCurrency):
            nom1, curr1 = trd.Nominal(), ins.Name()
            nom2, curr2 = trd.Premium(), trd.Currency().Name()
        elif ins.IsKindOf(acm.FOption) and ins.UnderlyingType() == 'Curr':  # FX Option
            nom1, curr1 = trd.Nominal(), ins.Underlying().Name()
            nom2, curr2 = trd.Nominal() * ins.StrikePrice(), ins.StrikeCurrency().Name()
        elif ins.IsKindOf(acm.FFuture) and ins.Underlying().IsKindOf(acm.FCommodity):
            # use premium for commodity forwards
            nom1, curr1 = -trd.Price() * trd.Quantity(), trd.Currency().Name()
            nom2, curr2 = nom1, curr1
        elif ins.IsKindOf(acm.FPriceSwap) and ins.FirstFloatLeg().FloatRateReference().IsKindOf(acm.FCommodityIndex):
            # use fixed price*nominal for commodity price swaps
            nom1, curr1 = ins.FirstFixedLeg().FixedRate() * trd.Quantity(), trd.Currency().Name()
            nom2, curr2 = nom1, curr1
        elif len(ins.Legs()) <= 1:  # use t.Nominal()
            nom1, curr1 = trd.Nominal(), trd.Currency().Name()
            nom2, curr2 = '', ''
        else:  # use current cashflow nominal
            rec_leg_nom = self.get_leg_nominal(trd, False)
            (nom1, curr1) = rec_leg_nom or (trd.Nominal(), trd.Currency().Name())

            pay_leg_nom = self.get_leg_nominal(trd, True)
            (nom2, curr2) = pay_leg_nom or ('', '')

            if ins.IsKindOf(acm.FSwap) and not nom1:  # pulling notional from trade if no active CF
                nom1, curr1 = trd.Quantity() * ins.ContractSize(), trd.Currency().Name()

            if ins.IsKindOf(acm.FCurrencySwap) and not nom2:  # pulling nominal values if no active CF
                payleg, recleg = ins.FirstPayLeg(), ins.FirstReceiveLeg()
                curr1, nom1 = recleg.Currency().Name(), ins.ContractSize() * recleg.NominalFactor()
                curr2, nom2 = payleg.Currency().Name(), ins.ContractSize() * payleg.NominalFactor()

        if ins.IsKindOf(acm.FCreditDefaultSwap) or (ins.IsKindOf(acm.FOption) and ins.Underlying().IsKindOf(acm.FSwap)):
            # copy for CDS
            nom2, curr2 = nom1, curr1

        return ((nom1, curr1), (nom2, curr2))

    @staticmethod
    def get_unds(ins):
        """Return underlying instruments for specified instrument.
        :param ins:
        """
        unds = []
        if insis(ins, acm.FEquityIndex, acm.FCombination):
            unds = ins.Instruments()

        # If the TRS contains a float leg, bring the index reference's instype through as the underlying
        elif insis(ins, acm.FTotalReturnSwap):
            unds = [l.IndexRef() for l in ins.Legs() if l.LegType() == 'Float']

        # If the PriceSwap contains a float leg, please bring the float rate's instype through as underlying.
        elif insis(ins, acm.FPriceSwap, acm.FCap, acm.FFra, acm.FFrn, acm.FSwap):
            unds = [l.FloatRateReference() for l in ins.Legs() if l.LegType() in ['Float', 'Cap']]

        # Bring the credit ref's instype through on the instrument for a CreditDefaultSwap.
        elif insis(ins, acm.FCreditDefaultSwap):
            unds = [ins.Legs()[0].CreditRef()]

        und = ins.Underlying()
        return unds or ([und] if und else [])

    def get_und_type_isin(self, ins):
        """Return (underlying_type, isin) for specified instrument.
        :param ins:
        """
        unds = self.get_unds(ins)

        if len(unds) == 0:
            return ('', '')
        if len(unds) == 1:
            return unds[0].InsType(), unds[0].Isin()

        und_types = list(set(und.InsType() for und in unds))
        return (und_types[0], '') if len(und_types) == 1 else ('', '')

    def get_payrec(self, trd):
        """Return PAY or REC for specified trade.
        :param trd:
        """
        if trd.Instrument().InsType() != 'Swap':
            return ''

        legs = trd.Instrument().Legs()
        leg_types = [l.LegType() for l in legs]
        if 'Float' not in leg_types or 'Fixed' not in leg_types:
            return ''

        fixed_legs = [l for l in legs if l.LegType() == 'Fixed']
        nominal = filter(bool, [self.cf_nominal(l, trd) for l in fixed_legs])
        if nominal:
            return 'REC' if nominal[0] > 0 else 'PAY'
        else:
            return ''

    def get_collateralized(self, trd, cp_coll):
        """Return a string value indicating whether the trade is collateralized.
        :param trd:
        :param cp_coll:
        """
        if trd.Oid() in self.get_context().get_coll_fa_trades():
            return COLLATERALIZED
        if trd.Oid() in self.get_context().get_noncoll_fa_trades():
            return NON_COLLATERALIZED
        if trd.Instrument().InsType() in self.get_context().get_non_coll_instypes():
            return NON_COLLATERALIZED
        if trd.Portfolio().Name() in self.get_context().get_noncoll_nonotc_pf() and not trd.Instrument().Otc():
            return NON_COLLATERALIZED
        return cp_coll

    @staticmethod
    def filter_static(trd):
        """

        :param trd:
        """
        ins = trd.Instrument()

        # Exclude portfolios ending with _LCH (e.g. LTFX_LCH, Swap Flow_LCH)
        if trd.Portfolio().Name().endswith('_LCH'):
            return False

        if ins.IsKindOf(acm.FCombination):
            # Ignore combinations without any links
            if not ins.Instruments():
                return False

        # For TRS "Expiry" field in PRIME refers to leg's end date.
        value_date = norm_date(trd.ValueDay())
        expiry = ins.FirstPayLeg().EndDate() if ins.IsKindOf(acm.FTotalReturnSwap) else ins.ExpiryDate()
        expiry = norm_date(expiry)

        # ASQL can't filter by combination's expiry date - filtering here.
        # Also applies to other instruments - expiry rules over value date.
        today = acm.Time.DateToday()
        if not (expiry > today or (expiry is None and value_date > today)):
            return False

        # Removed code that excludes FX Spot trades.MINT-164

        if ins.IsKindOf(acm.FOption):
            # barrier options in status "confirmed" but include all other barrier options until
            # expiration date is reached
            ex = ins.Exotic()
            if ex and ins.IsBarrier():
                if ins.ExpiryDate() <= today or ex.BarrierCrossedStatus() in ('Confirmed'):
                    # Excluding barrier options
                    return False

        # FRA with start date in past should be excluded
        if ins.IsKindOf(acm.FFra) and ins.StartDate() <= today:
            return False

        # We deal with far leg
        if trd.IsFxSwap():
            if trd.IsFxSwapNearLeg():
                return False

        # Not interested in buried trades.
        if trd.match_portfolio('GRAVEYARD'):
            return False

        # Exclude all exchange traded trades with few exceptions
        if not ins.Otc():
            if not (
                    (ins.IsKindOf(acm.FOption) and ins.Underlying().IsKindOf(acm.FCurrency)) or insis(ins, acm.FCombination,
                                                                                                      acm.FPriceSwap,
                                                                                                      acm.FETF, acm.FCfd)):
                return False

        # Exclude trades with ~0 MTM
        mtm_val, mtm_curr = mtm_val_curr(trd)
        if abs(mtm_val) < MTM_THRESHOLD:
            return False

        # Exclude close out trades on equity swaps
        if ins.IsKindOf(acm.FTotalReturnSwap):
            und = ins.IndexReference() or ins.Legs()[0].FloatRateReference()
            if und and und.IsKindOf(acm.FStock) or und.IsKindOf(acm.FEquityIndex):
                has_closing = any(t for t in ins.Trades() if
                                  t != trd
                                  and t.Quantity() == -trd.Quantity()
                                  and t.Counterparty() == trd.Counterparty()
                                  and t != trd
                                  and mtm_val_curr(t) == (-mtm_val, mtm_curr))
                if has_closing:
                    return False

        return True

    def filter_trade(self, trd):
        """

        :param trd:
        :return:
        """
        ins = trd.Instrument()

        if ins.InsType() in self.get_context().get_exclude_instypes():
            return False

        # Filter by acquirers
        if trd.Acquirer() in self.get_context().get_exc_fa_acquirers():
            return False

        if not self.filter_static(trd):
            return False

        # Exclude shadow deals for BARCLAYS BANK PLC (10538)
        if trd.AdditionalInfo().Source_Ctpy_Id()=='10538' and trd.AdditionalInfo().Source_Trade_Type() == 'SH':
            return

        return True

    def get_leg_nominal(self, trade, is_pay_leg):
        """Return (amount, currency) tuple representing nominal for selected leg.
        :param is_pay_leg:
        :param trade:
        """
        # Get all selected legs
        legs = [l for l in trade.Instrument().Legs() if l.PayLeg() == is_pay_leg]

        # Compute cashflow nominals
        lwn = [(l, self.cf_nominal(l, trade)) for l in legs]
        # Selected only legs with nominals
        lwn = [(l, n) for l, n in lwn if n is not None]

        if len(lwn) > 1:
            raise Exception(
                'Trade {0} ({1}) has far too many active legs.'.format(trade.Oid(), trade.Instrument().Name()))
        if len(lwn) == 0:
            return None

        return (lwn[0][1], lwn[0][0].Currency().Name())

    def write_trade(self, trade, writer, cpty_coll, flt, use_counter_party_name=False):
        """


        :param use_counter_party_name:
        :param trade:
        :param writer:
        :param cpty_coll:
        :param flt:
        :return:
        """
        try:
            data = self.get_trade_row(trade, cpty_coll, flt, use_counter_party_name)
        except Exception, e:
            errmsg = traceback.format_exc()
            self.write_error("An error occurred while processing trade {0}: {1}", trade.Oid(), errmsg)
            return




        if data:
            print str(trade.Oid()) + " with data "
        else:
            print str(trade.Oid()) + " NO data "


        if data and writer:
            writer.writerow(data)
            if trade.IsFxSwapFarLeg():  # include also FX Swap near leg
                near_trade = trade.FxSwapNearLeg()
                if near_trade.ValueDay() >= self.get_context().get_today():
                    self.write_trade(near_trade, writer, cpty_coll, False)


class EMIRFrontArena(EMIRExport):
    """

    :param context:
    """

    def __init__(self, context):
        """


        :rtype : EMIRFrontArena
        :param context:
        """
        super(EMIRFrontArena, self).__init__(context)

    def run(self, writer):
        # Processing only Front Arena data
        """


        :param writer:
        """

        list_of_counter_parties_ids_written = {}

        list_of_counter_parties_ids_written = self.step_write_non_eu_counter_parties_non_coll(writer, list_of_counter_parties_ids_written)

        list_of_counter_parties_ids_written = self.step_write_legal_entities(writer, list_of_counter_parties_ids_written)
        
        list_of_counter_parties_ids_written = self.step_write_eu_legal_sdsid_non_coll_entities(writer, list_of_counter_parties_ids_written)

        self.step_write_include_fa_trades(writer)

    def step_write_legal_entities(self, writer, list_of_counter_parties_ids_written):
        """ Get all the counter parties which legal id is found and write it to writer

        Counter parties should not include counter parties that have been written

        :param list_of_counter_parties_ids_written:
        :type writer: csv.DictWriter
        :rtype : dict
        :param writer:
        """
        print "Processing collateralized counter parties from Legal Entity SDS list."
        legal_ids = self.get_legal_entities(list_of_counter_parties_ids_written)
        print "Entries found: " + str(len(legal_ids))
        self.run_cpty_ids(writer, legal_ids, COLLATERALIZED)
        print "Processing collateralized counter parties from Legal Entity SDS list finished."

        print "Add legal_ids to list_of_counter_parties_ids_written"
        for id in legal_ids:
            list_of_counter_parties_ids_written[id] = None

        return list_of_counter_parties_ids_written

    def step_write_eu_legal_sdsid_non_coll_entities(self, writer, list_of_counter_parties_ids_written):
        """ Get all the EU non collateral counter parties

        Counter parties should not include counter parties that have been written

        :rtype : dict
        :param writer:csv.DictWriter
        """
        print "Processing non-collateralized counter parties from EU counter party SDS list."
        eu_ids = self.get_eu_legal_SDS_non_coll_entities(list_of_counter_parties_ids_written)
        print "Entries found: " + str(len(eu_ids))
        self.run_cpty_ids(writer, eu_ids, NON_COLLATERALIZED)
        print "Processing non-collateralized counter parties from EU counter party SDS list finished."

        print "Add legal_ids to list_of_counter_parties_ids_written"
        for id in eu_ids:
            list_of_counter_parties_ids_written[id] = None

        return list_of_counter_parties_ids_written

    def step_write_non_eu_counter_parties_non_coll(self, writer, list_of_counter_parties_ids_written):
        """ Get all the EU non collateral counter parties

        Counter parties should not include counter parties that have been written

        :rtype : dict
        :param writer:csv.DictWriter
        """
        print "Processing collateralized counter parties....."
        non_eu_counter_party_ids = self.get_non_eu_counter_parties(list_of_counter_parties_ids_written)
        print "Entries found: " + str(len(non_eu_counter_party_ids))
        self.run_cpty_ids(writer, non_eu_counter_party_ids, COLLATERALIZED, True)
        print "Processing collateralized counter parties finished."

        print "Add legal_ids to list_of_counter_parties_ids_written"
        for id in non_eu_counter_party_ids:
            list_of_counter_parties_ids_written[id] = None

        return list_of_counter_parties_ids_written

    def step_write_include_fa_trades(self, writer):
        """

        :rtype : dict
        :param writer:csv.DictWriter
        """
        for trade_id in self.get_context().get_inc_fa_trades():
            # Should look up cpty coll?
            self.write_trade(acm.FTrade[trade_id], writer, NON_COLLATERALIZED, FLT_DISABLE)

    def run_cpty_ids(self, writer, coll_cpty_ids, cpty_coll, use_counter_party_name=False):
        """

        :param use_counter_party_name:
        :param cpty_coll:
        :type coll_cpty_ids: tuple
        :type writer: csv.writer
        :param writer:
        :param coll_cpty_ids:
        """
        trade_filter_enabled = self.get_context().get_use_trade_filter()
        counter = 1
        count = len(coll_cpty_ids)
        for cpty_id in coll_cpty_ids:
            name = "(None)"
            if cpty_id in self.get_context().get_le_names_by_front_id():
                name = self.get_context().get_le_names_by_front_id()[cpty_id ]

            print str(counter) + " of " + str(count) + ". cpty_id:  " + str(cpty_id)+ " "  +  name  + " begin..."
            row_count = self.process_cpty(cpty_id, cpty_coll, writer, trade_filter_enabled, use_counter_party_name)
            print str(counter) + " of " + str(count) + ". cpty_id:  " + str(cpty_id) + " end. " + str(row_count) + " persisted."
            counter += 1

    def get_legal_entities(self, list_of_counter_parties_ids_written):
        """Find all the counter parties, which legal entity is listed in get_context().get_le_sds_ids()

        :param list_of_counter_parties_ids_written:
        :rtype : tuple
        :return:
        """
        return [m.front_id for m in self.get_context().get_mappings()
                if m.front_id
                and not (m.front_id in list_of_counter_parties_ids_written)
                and (m.le_sdsid in self.get_context().get_le_sds_ids())]

    def get_eu_legal_SDS_non_coll_entities(self, list_of_counter_parties_ids_written):
        """



        :rtype : tuple
        :return:
        """
        return [m.front_id for m in self.get_context().get_mappings()
                if m.front_id
                and not (m.front_id in list_of_counter_parties_ids_written)
                and m.cp_sdsid in self.get_context().get_eu_cp_sds_ids()]

    def get_non_eu_counter_parties(self, list_of_counter_parties_ids_written):
        """

        :rtype : tuple
        :return:
        """
        return [cp for cp in self.get_context().get_non_eu_cp_ids()
                if not (cp in list_of_counter_parties_ids_written)]

    def process_cpty(self, cpty_id, cpty_coll, writer, flt, use_counter_party_name=False):
        """Process trades for specified counterparty.

        Three steps
        1. Get all the trade id's for the counterparty. will return a tuple of integers
        2. With result from 1, get the ftrade objects. Return a tuple of FTrades
        3. Write result from 2 to the writer object

        :param use_counter_party_name:
        :rtype : int
        :param flt:
        :param writer:
        :param cpty_coll:
        :param cpty_id:
        """

        # Step 1
        query_result_data = self.process_cpty_get_trades_via_asql(cpty_id)

        # Step 2
        ftrades = self.process_cpty_get_ftrades_from_data(cpty_coll, query_result_data)

        # Step 3
        row_count = self.process_cpty_write_to_writer(cpty_coll, writer, flt, ftrades, use_counter_party_name)

        return row_count

    def process_cpty_get_trades_via_asql(self, cpty_id):
        """


        :param cpty_id:
        :rtype : tuple
        """
        query = CPTY_TRADES_QUERY.format(self.get_context().get_tomorrow(), cpty_id)
        query_result = ael.asql(query)[1][0]
        query_result_data = [row[0] for row in query_result]

        return query_result_data

    def process_cpty_get_ftrades_from_data(self, cpty_coll, query_result_data):
        """ Tale a tuple of trade id's and return a tuple of Ftrades.

        :rtype : tuple
        :param cpty_coll:
        :param query_result_data:
        :return:
        """
        result = []

        trades = [acm.FTrade[row] for row in query_result_data]
        if trades:
            print "Processing counterparty", trades[0].Counterparty().Name(), "with", len(
                trades), "trades. Coll status:", cpty_coll

        # Before writing to file/report, remove equal but opposite trades from the list trades.
        trade_list = {}

        for trade in trades:
            # value = Provision.calculate(trade)
            # print  value
            nominal_of_trade = trade.Nominal()
            nominal_of_opposite_trade = -1 * nominal_of_trade
            unique_trade_id = 0
            unique_opposite_trade_id = 0

            # For Midas Dual Key check if the Source Cpty ID in Add info is 10538 or 522623. Also add value day as part of the unique key MINT-985
            # Ammend unique_trade_id for all Barclay's CP trades (CP_ID 10538 and 522623), both Midas Dual Key and Non Midas Dual Key trades MINT-1000
            if trade.Counterparty().Oid() in (10395, 33075) or trade.AdditionalInfo().Source_Ctpy_Id() in ('10538', '522623'):
                unique_trade_id = trade.Instrument().Name() + "-" + trade.Counterparty().Name() + "-" + trade.Acquirer().Name() + "-" + str(
                    nominal_of_trade)+ "-" + trade.ValueDay() + "-" + str(trade.Premium()) + "-" + trade.Currency().Name()
                unique_opposite_trade_id = trade.Instrument().Name() + "-" + trade.Counterparty().Name() + "-" + trade.Acquirer().Name() + "-" + str(
                    nominal_of_opposite_trade)+ "-" + trade.ValueDay() + "-" + str(trade.Premium()) + "-" + trade.Currency().Name()

            #Ensure that any other MIDAS DUAL KEY trades that don't meet the criteria above are not pulled in
            else:
                unique_trade_id = trade.Instrument().Name() + "-" + trade.Counterparty().Name() + "-" + trade.Acquirer().Name() + "-" + str(
                    int(nominal_of_trade))
                unique_opposite_trade_id = trade.Instrument().Name() + "-" + trade.Counterparty().Name() + "-" + trade.Acquirer().Name() + "-" + str(
                    int(nominal_of_opposite_trade))
           
            if unique_opposite_trade_id in trade_list and unique_opposite_trade_id > 0:
                # Find the list of the unique oppisite trade
                temp_list = trade_list[unique_opposite_trade_id]

                if len(temp_list) > 0:
                    trade_to_be_removed = temp_list[0]
                    print 'Excluding trade %s and %s. Reason:Equal and opposite trades.' % (
                        trade.Oid(), trade_to_be_removed.Oid())
                    temp_list.pop(0)
                    if len(temp_list) == 0:
                        del trade_list[unique_opposite_trade_id]
            elif unique_trade_id > 0:
                # Add a tuple in the dictionary.
                temp_list = trade_list.setdefault(unique_trade_id, [])
                temp_list.append(trade)

        for iterator_list in trade_list.values():
            for trade in iterator_list:
                result.append(trade)


        return result

    def process_cpty_write_to_writer(self, cpty_coll, writer, flt, ftrades, use_counter_party_name=False):
        """ write a tuple of FTrades into  the writer object

        Return the amount of trades written to the writer.

        :type use_counter_party_name: bool
        :param cpty_coll:
        :param writer:
        :param flt:
        :param ftrades:
        :rtype : int
        """
        result = 0
        for trade in ftrades:
            if trade.Oid() not in self.get_context().get_exc_fa_trades():
                result += 1
                self.write_trade(trade, writer, cpty_coll, flt, use_counter_party_name)

        return result


class EMIRMidasTrades(EMIRExport):
    """

    :param context:
    """

    def __init__(self, context):
        """

        :param context:
        """
        super(EMIRMidasTrades, self).__init__(context)

        self._mdk_collection = MidasDualKeyTradesCollection()

    def run(self, writer):
        """

        :param writer:
        """
        self.add_midas_trades(writer)

    def create_cp_maps_for_custno(self, custno):
        """

        :param custno:
        :return:
        """
        return [mi for mi in self.get_context().get_mappings() if mi.midas_id == custno]


    def filter_on_party(self, bxa_xml_config, row, midas_cust_no, cp_sdsid):
        start_column = row[COL_START_DATE]
        broker_code = row[COL_BROKER_CODE]
        if row[COL_BROKER_CODE] in ("REUT", "REU") and start_column > "20160719":
            return False
        elif row[COL_BROKER_CODE] in ("ABOL", "AOL") and start_column > "20160728":
            return False
        elif row[COL_BROKER_CODE] in ("BRX", "BSTP", "PRF", "BPRF", "OWM", "FXAG", "FXH", "FXHG") and start_column > "20160811":
            return False
        elif row[COL_BROKER_CODE] in ("SML", "SMML") and start_column > "20160901":
            return False
        elif row[COL_BROKER_CODE] in ("BII", "BICM") and start_column > "20160922":
            return False
        elif row[COL_BROKER_CODE] in ("FAR", "FRAR") and start_column > "20161020":
            return False
        elif row[COL_BROKER_CODE] in ("PHO", "PHOX") and start_column > "20170510":
            return False
        return TriResolve_EMIR_Functions.barx_africa_filter(bxa_xml_config, broker_code, midas_cust_no, cp_sdsid, start_column) 


    def add_midas_trades(self, writer):
        """Add trades from Midas trade file to the report.
        :param writer:
        """

        # convert Midas date to Y-m-d
        fixdate = lambda d: time.strftime('%Y-%m-%d', time.strptime(d, '%Y%m%d'))

        midas_extract_path = self.get_context().demacroize(self.get_context().get_params()[const_midas_extract_path],
                                                           self.get_context()._from_fa)
        
        TriResolve_EMIR_Functions.check_file_exists(midas_extract_path, "Midas extract")        
                
        fxf_filtered_clients_path = self.get_context().demacroize(self.get_context().get_params()[const_fxf_filtered_clients_path],
                                                           self.get_context()._from_fa)

        TriResolve_EMIR_Functions.check_file_exists(fxf_filtered_clients_path, "Barx Africa filter config")
        
        bxa_xml_config =  TriResolve_EMIR_Functions.serialize_bxa_config_to_xml(fxf_filtered_clients_path)

        with open(midas_extract_path, 'rb') as f_midas_extract:
            reader = csv.DictReader(f_midas_extract)
            reader.next()  # skip delimiter row
            for row in reader:  # The file has almost identical columns to the output

                custno = int(row['CUSTNO'])
                cp_maps = self.create_cp_maps_for_custno(custno)

                if not cp_maps:
                    continue  # Exclude trades for cpties which are not even mapped.
                    
                cust_mapping = cp_maps[0]
                
                trade_midas_id = int(row[COL_TRADE_ID])

                if not self.filter_on_party(bxa_xml_config, row, custno, cust_mapping.cp_sdsid):                
                    print 'Trade excluded:', trade_midas_id, 'Midas Cust No:', custno, 'SDS:', cust_mapping.cp_sdsid, 'Broker:', row[COL_BROKER_CODE], 'Start:', row[COL_START_DATE]
                    continue

                if trade_midas_id in self.get_written_midas_ids():
                    continue  # Trade already in the report

                if trade_midas_id in self.get_context().get_exc_midas_trades():
                    continue

                if cust_mapping.le_sdsid in self.get_context().get_le_sds_ids():
                    row[XCOL_COLLATERALIZED] = COLLATERALIZED
                elif cust_mapping.cp_sdsid in self.get_context().get_eu_cp_sds_ids():
                    row[XCOL_COLLATERALIZED] = NON_COLLATERALIZED
                else:
                    row[XCOL_COLLATERALIZED] = COLLATERALIZED

                row[COL_END_DATE] = fixdate(row[COL_END_DATE])
                mtm_val = row[COL_MTM_VALUE]

                if trade_midas_id not in self.get_context().get_inc_midas_trades():
                    # Mint-164 Remove the exclusion of OUTRIGHT SPOT trades.Exclude all spot trades and near legs of swaps
                    if row[COL_END_DATE] <= self.get_context().get_today():
                        continue

                    pf = row[COL_BOOK]
                    if pf in self.get_context().get_midas_stl_pf():
                        continue

                    # Exlude trades for cpties which are not in LE or EU list.
                    if 'OUTRIGHT SPOT' not in row[COL_PRODUCT_CLASS] and not XCOL_COLLATERALIZED in row:
                        continue
                    # if the trade is in move portfolio, it could be in FA and split in several trades
                    # each of these trades should belong to MIDAS DUAL KEY counterparty
                    # but not necessarily will all trades be in the same portfolio
                    # if the trades are found, we can ignore the one from midas file.

                    # Additional change for MIN 453. Took out:  and 'OUTRIGHT SPOT' not in row[COL_PRODUCT_CLASS] in line below
                    if pf in self.get_context().get_midas_moved_pf():
                        cp_collateralized = row[XCOL_COLLATERALIZED]
                        if self.process_moved_trade(trade_midas_id, row[COL_END_DATE], cp_collateralized,
                                                    writer):
                            continue

                    if mtm_val == 'NULL' or abs(float(row[COL_MTM_VALUE])) < MTM_THRESHOLD:
                        continue

                row[COL_CP_ID] = cust_mapping.le_name

                if trade_midas_id in self.get_context().get_coll_midas_trades():
                    row[XCOL_COLLATERALIZED] = COLLATERALIZED
                elif trade_midas_id in self.get_context().get_noncoll_midas_trades():
                    row[XCOL_COLLATERALIZED] = NON_COLLATERALIZED

                row[COL_PRODUCT_CLASS] = 'FX'
                row[COL_PAY_REC] = ''
                row[COL_TRADE_DATE] = fixdate(row[COL_TRADE_DATE])
                row[COL_START_DATE] = fixdate(row[COL_START_DATE])
                row[COL_MTM_DATE] = self.get_context().get_today()
                row[COL_MTM_VALUE] = mtm_val if mtm_val != 'NULL' else 0

                writer.writerow(row)

    def process_moved_trade(self, midas_id, value_date, cp_collateralized, writer):
        """Process trade in Midas move portfolio (replace by corresponding FA trades).
        :param writer:
        :param cp_collateralized:
        :param value_date:
        :param midas_id:
        """

        # The corresponding trades are in booked for MDK counterparty by CFR pump.
        trades = self._mdk_collection.trades_by_midas_id.get(midas_id)
        if not trades:
            return False

        trades = filter(lambda t: t.ValueDay() == value_date, trades)

        fx_swap_other_legs = [t.FxSwapFarLeg() if t.IsFxSwapNearLeg() else t.FxSwapNearLeg()
                              for t in trades if
                              t.Instrument().IsKindOf(acm.FCurrency) and
                              t.IsFxSwap() and
                              t.ValueDay() >= self.get_context()._today]

        trades = list(set(trades + fx_swap_other_legs))

        for trade in trades:
            # Process all trades in FA moved from Midas except for those in exclusion list
            # Exclude Midas Dual Key trades for cp '10538' and '522623' to avoid duplicates. These trades are being fed through the FA task
            if trade.Oid() in self.get_context()._exc_fa_trades or \
                (trade.Counterparty().Name() == 'MIDAS DUAL KEY' and trade.AdditionalInfo().Source_Ctpy_Id() in ('10538', '522623')):
                continue
            self.write_trade(trade, writer, cp_collateralized, FLT_ENABLE)

        return True
