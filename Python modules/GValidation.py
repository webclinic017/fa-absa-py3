"""
UI validation hooks. This module is scheduled to run after clicking save in
Trade Editor and before FValidation. Module can validate instruments
and trades.


DESCRIPTION
Amendment Diary
2015-10-02        Andrei Conicov                        Have added the backdate amendment logic.
2015-11-13        Fancy Dire	                        Extended the backdate logic to multiple trade updates.
2015-11-26        Marcelo Almiron                       Cleaned input_amendment_reason function and
                                                        passed the logic to requires_amendment_reason
                                                        function.
2016-03-08        Mighty Mkansi                         ABITFA-3970-Added a function: set_float_ref, use default float refs corresponding to instrument currency.
2016-07-19        Anil Parbhoo          CHNG0003808399  Instrument that has a companion defined should have a corresponding spread
2016-08-19        Rohan van der Walt    CHNG0003744247  Demat changes for validation of Demat Instruments and Trades
2016-09-06        Willie van der Bank   CHNG0003914707  Include Bill instruments in setting the settlement category for Demat instruments by removing issuer check
2016-11-22        Willie van der Bank   CHNG0004119231  Fixed minimum tradeable denomination internal Python issue
2017-11-07        Libor Svoboda         CHNG0005105452  Updated warning logic for populated Sales Credits.
2017-12-11        Manan Ghosh           CHNG0005220511  Added validation for DIS trades
2018-01-25        Delsayo / Mighty      CHG1000075709   Prevent booking of ETF and Stocks in RTM restricted portfolios
2018-01-25        Willie vd Bank        CHG1000078271   Changes made to the way the primary trade is selected for DIS instruments
2018-04-19        Tibor Reiss           CHG1000397187   ABITFA-5248: Backdating trades (exception Swaps and FRAs) with acquirer PRIME SERVICES DESK only allowed if
                                                           - same month
                                                           - and if trade_date < now-3days user confirmation needed
2018-05-03        Tibor Reiss           CHG1000436602   ABITFA-5248: moved rule for backdating trades to FValidation_General
2018-07-24        Mighty Mkansi         CHG1000703840   ABITFA-5484 -A change in GValidation to commit group trade number when initially saving a trade, restricted to the Funding Desk
2018-10-16        Sadanand Upase                        FAOPS-42 - show a custom gui to choose SSI when there are multiple DVP SSIs present on counterparty
2018-11-13        Libor Svoboda         CHG1001100033   FtF-CAL: Remove TradeAmendments dependency, move pop-up GUI to FValidation_cal
2019-02-12        Mighty Mkansi                         ABITFA-5678: Duplicate payments - USD67 and USD10 and proposed solution.
2019-05-31        Hugo Decloedt         FAOPS-475       Add check for cash flow duplicates and prompt user to confirm
                                                        saving trade if there are duplicates.
2019-11-01        Amit Kardile          FAFO-44         NCD JIBAR contribution check
2019-11-21        Stuart Wilson         FAOPS-586       Added change to set MM_DEMAT_PRE_SETT to No if already set
2020-01-22        Amit Kardile          FAFO-77         Sales credit calculation
2020-02-03        Cuen Edwards          FAOPS-704       Changed demat trade nominal validations to only apply for buys and sells to the market.
2020-02-14        Amit Kardile          FAFO-71         SOFR Lockout functionality
2020-02-25        Jaco Swanepoel        FAFO-85         Functionality to select ACM credit facility pre-deal.
2020-70-15        Anil Parbhoo          CHG0113161      notification (not block) each time a bond trade is defined for trade settle category 'Euroclear'
2020-08-07        Jaysen Naicker        FAOPS-847       Add Demat Instype "RBD" on a CD Ticket for SARB Debentures 
2020-08-25        Amit Kardile          FAFO-139        block external trades booked in LCH books without MW ID
"""

from math import fabs

# pylint: disable=import-error
import acm
import ael
import CorpBond_Spreads
from demat_functions import GetFirstTrade, is_valid_trade, is_active
from demat_isin_mgmt_menex import demat_available_amount, demat_authorised_amount, get_party_demat_BPID
from CounterpartyWithMultipleDVPSIs import validate_and_show_ssi_choosing_gui
from at_logging import getLogger
from at_ux import msg_dialog
from GValidation_DuplicateCashFlows import DialogDuplicateCashFlows, CreateLayout
from GValidation_NCD_Jibar_Check import ncd_jibar_contribution_check_failed
from GValidation_Sales_Credits import calculate_and_save_sales_credits
from GValidation_Lockout import fix_lockout_resets_check_failed
from CreditFacilitySelection import predeal_acm_credit_facility_check
from GValidation_LCH_MW_Check import lch_mw_check_failed

LOGGER = getLogger()
SUPERUSERS = ["FMAINTENANCE", "UPGRADE43"]
TYPE_MAPPING = {'PN': 'PRN', 'NCC': 'NCD', 'Bill': 'TB', 'RBD': 'Debentures'}


class ValidationError(Exception):
    pass


def show_exception(message):
    dialog_func = acm.GetFunction('msgBox', 3)
    dialog_func('Validation Error', message, 0)


# Gui validation functions.
def extend_deposit_about_quotation(shell, obj):
    if obj.IsKindOf('FInstrument') and obj.InsType() == 'Deposit':
        legs = obj.Legs()
        if legs and legs[0].LegType() == 'Float':
            if obj.Quotation().Name() != 'Pct of Nominal':
                obj.Quotation('Pct of Nominal')
                acm.UX().Dialogs().MessageBoxInformation(shell, 'Deposit/Loan quotation was set to Pct Of Nominal.')


def premium_check(shell, obj):
    if obj.IsKindOf('FTrade') and obj.Instrument().InsType() == 'Deposit' and obj.Instrument().OpenEnd() == 'None' and acm.User().UserGroup().Oid() in (656, 650):
        if abs(obj.Premium()) != abs(obj.Quantity()*obj.Instrument().ContractSize()):
            warning = "Premium Amount does not equal the Cash Amount. Do you wish to proceed?"
            clicked = msg_dialog(warning, type_="Warning", shell=shell, button3="Cancel")
            if clicked == "Button3":
                raise ValidationError('Premium incorrect. Cancelled by user.')


def popup(shell, message):
    return acm.UX.Dialogs().MessageBoxInformation(shell, message)


def check_MTM_version(shell, obj):
    """ Alert the user in case if the modified instrument is a copy
    of a theoretical priced instrument.

    ABITFA-2712
    """
    if obj.IsKindOf('FInstrument'):
        ins = obj
        mirrorCandidate = "%s/MTM" % ins.Name()
        mirrors = acm.FInstrument.Select('name = %s' % mirrorCandidate)
        if mirrors:
            message = 'Note that MTM version of instrument exists - %s' % mirrorCandidate
            popup(shell, message)
            LOGGER.info(message)


def check_credit_sales(shell, edit_obj, data):
    """Traders copy trades with sales credit fields populate, this fixes that"""
    if edit_obj.IsKindOf('FTrade'):
        original_obj = data['originalObject']
        action = data['action']

        if original_obj and action == 'create':  # if this is a copy
            add_info = edit_obj.AdditionalInfo()
            if edit_obj.SalesCredit() or add_info.ValueAddCredits() or \
                    add_info.Sales_Credit2() or add_info.Sales_Credit3() or \
                    add_info.Sales_Credit4() or add_info.Sales_Credit5() or \
                    add_info.Sales_Credit6():

                LOGGER.warning("sales credit being copied over to new trade...potential error")
                popup(shell, "Potential copy error, Copied Trade has credit sales values set!")


def update_trade_groupref(shell, obj):
    """
    Update group trade number for CD, Deposit and FRN instruments booked to the Funding Desk.
    :param shell: FUxShell
    :param obj: FTrade or FInstrument
    """
    del shell
    if obj.IsKindOf('FTrade'):
        instrument = obj.Instrument()
        if obj.Acquirer():
            if obj.Acquirer().Name() == 'Funding Desk' and instrument.InsType() in ('CD', 'Deposit', 'FRN'):
                obj.GroupTrdnbr(obj)
                obj.Commit()


def corresponding_companion_spread(shell, obj):
    """
    Check if the companion spread is set.
    :param shell: FUxShell
    :param obj: FTrade or FInstrument
    """
    if obj.IsKindOf('FTrade'):
        ins = obj.Instrument()
        if ins.InsType() in ('FRN', 'Bond', 'IndexLinkedBond'):
            if ins.AdditionalInfo().Companion() and obj.Status()in ('Simulated', 'FO Confirmed'):
                if not obj.AdditionalInfo().Companion_Spread():
                    CompMsg = 'Instrument has Companion %s but Trade has NO Companion_Spread' % (ins.AdditionalInfo().Companion())
                else:
                    sp = CorpBond_Spreads.corres_spread(ins.Name())
                    CompMsg = 'Trade has spread %s VS. spread on the curve ZAR-CORPBONDS-SPREADS is %s' % (obj.AdditionalInfo().Companion_Spread(), sp)

                acm.UX().Dialogs().MessageBoxInformation(shell, CompMsg)
            if not (ins.AdditionalInfo().Companion()) and obj.Status()in ('Simulated', 'FO Confirmed'):
                if obj.AdditionalInfo().Companion_Spread():
                    NoCompMsg = 'Instrument has NO Companion but Trade has Companion_Spread  = %s' % (obj.AdditionalInfo().Companion_Spread())
                    acm.UX().Dialogs().MessageBoxInformation(shell, NoCompMsg)


def check_demat_fields(shell, obj, data):
    del shell
    del data

    if obj.IsKindOf('FInstrument'):
        try:
            if obj.AdditionalInfo().Demat_Instrument() is True:
                import demat_functions
                # Min Trade Denomination must be greater than R 1 million.
                if not obj.AdditionalInfo().Demat_MinTrdDeno():
                    obj.AdditionalInfo().Demat_MinTrdDeno(1)  # Set default value of 1
                if not obj.AdditionalInfo().Demat_Ins_SOR_Acc():
                    obj.AdditionalInfo().Demat_Ins_SOR_Acc(demat_functions.sor_accounts(obj)[0])
                if not obj.AdditionalInfo().Demat_Issuer_BPID():
                    obj.AdditionalInfo().Demat_Issuer_BPID(demat_functions.bp_ids(obj)[0])
                if not obj.AdditionalInfo().Demat_WthhldTax():
                    obj.AdditionalInfo().Demat_WthhldTax(False)

                # When Withholding Tax is checked then Withholding Tax rate must be entered
                if obj.AdditionalInfo().Demat_WthhldTax() is True:
                    if obj.AdditionalInfo().Demat_WthhldTx_Rate() is None:
                        raise ValidationError('Withholding Tax must not be empty if selected')
                    if float(obj.AdditionalInfo().Demat_WthhldTx_Rate()) < 0.0:
                        raise ValidationError('Withholding Tax Rate not set')

                if not obj.AdditionalInfo().MM_MMInstype():
                    obj.AdditionalInfo().MM_MMInstype(demat_functions.INS_TYPES[obj.InsType()][0])

                if not obj.SettleCategoryChlItem():
                    obj.SettleCategoryChlItem("Demat")

            if obj.AdditionalInfo().DIS_Instrument() is True:
                import demat_functions
                # Min Trade Denomination must be greater than R 1 million.
                if not obj.AdditionalInfo().Demat_MinTrdDeno():
                    obj.AdditionalInfo().Demat_MinTrdDeno(1)  # Set default value of 1
                if not obj.AdditionalInfo().Demat_Ins_SOR_Acc():
                    obj.AdditionalInfo().Demat_Ins_SOR_Acc(demat_functions.sor_accounts(obj)[0])
                if not obj.AdditionalInfo().Demat_Issuer_BPID():
                    obj.AdditionalInfo().Demat_Issuer_BPID(demat_functions.bp_ids(obj)[0])
                if not obj.AdditionalInfo().Demat_WthhldTax():
                    obj.AdditionalInfo().Demat_WthhldTax(False)

                # When Withholding Tax is checked then Withholding Tax rate must be entered
                if obj.AdditionalInfo().Demat_WthhldTax() is True:
                    if obj.AdditionalInfo().Demat_WthhldTx_Rate() is None:
                        raise ValidationError('Withholding Tax must not be empty if selected')
                    if float(obj.AdditionalInfo().Demat_WthhldTx_Rate()) < 0.0:
                        raise ValidationError('Withholding Tax Rate not set')

                if not obj.AdditionalInfo().MM_MMInstype():
                    obj.AdditionalInfo().MM_MMInstype(demat_functions.INS_TYPES[obj.InsType()][0])

                if not obj.AdditionalInfo().DIS_Ins_Category():
                    obj.AdditionalInfo().DIS_Ins_Category(demat_functions.CATEGORIES[obj.InsType()][0])

                if not obj.SettleCategoryChlItem():
                    obj.SettleCategoryChlItem("DIS")

                if not obj.AdditionalInfo().Listed():
                    obj.AdditionalInfo().Listed(False)

                if not obj.AdditionalInfo().Structure():
                    obj.AdditionalInfo().Structure(False)

        except Exception as e:
            LOGGER.exception('Demat GValidation Exception during setting defaults. Detail: %s' % e)

    if obj.IsKindOf('FTrade'):
        try:
            trade = obj
            relevant, fields = is_valid_trade(trade)

            if relevant:
                LOGGER.info('Demat trade validation invoked!! ')
                if fields:
                    raise ValidationError('Validation error : Missing mandatory fields [%s] ' % (','.join(fields)))
                if trade.Status() in ['FO Confirmed', 'BO Confirmed']:
                    if obj.Instrument().AdditionalInfo().Demat_Instrument() is True:
                        in_business_process, in_active_state = is_active(trade.Instrument())

                        LOGGER.info('is_active %s , %s ', str(in_business_process), str(in_active_state))
                        LOGGER.info('Instrument Name %s ', trade.Instrument().Name())

                        if in_business_process:
                            if not in_active_state:
                                raise ValidationError('Instrument not in an Active state')
                            _validate_demat_trade_instrument_availability(trade)
                            _validate_demat_trade_denomination(trade)
                        else:
                            if trade.Instrument().Isin() is None:
                                raise ValidationError('Instrument not in an Business Process and does not have ISIN')

                        if trade.AdditionalInfo().Demat_Deliv_vs_Paym() is None:
                            raise ValidationError('Demat Delivery vs Payment flag is blank ')

                        LOGGER.info('Validating FRN trade - Passed ')
                        trade.AdditionalInfo().MM_DEMAT_TRADE('Yes')
                        trade.PrimaryIssuance(True)
                        first_trade = GetFirstTrade(trade)
                        if first_trade and trade.Oid() == first_trade.Oid():
                            trade.AdditionalInfo().MM_DEMAT_PRE_SETT('Yes')
                        else:
                            trade.AdditionalInfo().MM_DEMAT_PRE_SETT('No')

                        dematinstype = trade.Instrument().InsType()

                        if trade.Instrument().AdditionalInfo().Demat_Instrument() is True:
                            trade.Instrument().SettleCategoryChlItem('Demat')

                        if dematinstype == 'CD':
                            instype = trade.Instrument().AdditionalInfo().MM_MMInstype()
                            if instype == 'RBD':
                                trade.AdditionalInfo().Funding_Instype(TYPE_MAPPING[instype])
                                trade.AdditionalInfo().Instype(instype)
                            elif instype == 'NCC':
                                trade.AdditionalInfo().Funding_Instype(instype)
                                trade.AdditionalInfo().Instype(instype)
                            else:
                                instype = instype in TYPE_MAPPING and TYPE_MAPPING[instype] or instype
                                trade.AdditionalInfo().Funding_Instype(instype)
                                trade.AdditionalInfo().Instype(instype)

                        if dematinstype in ['FRN']:
                            trade.AdditionalInfo().MM_Instype(trade.Instrument().AdditionalInfo().MM_MMInstype())

                        if dematinstype in ['Bill']:
                            trade.AdditionalInfo().MM_Instype((dematinstype in TYPE_MAPPING) and TYPE_MAPPING[dematinstype] or None)
                        trade.Commit()

                    if obj.Instrument().AdditionalInfo().DIS_Instrument() is True:
                        first_trade = GetFirstTrade(trade)
                        if first_trade and trade.Oid() == first_trade.Oid():
                            trade.AdditionalInfo().MM_DEMAT_PRE_SETT('Yes')
                        else:
                            trade.AdditionalInfo().MM_DEMAT_PRE_SETT('No')
                    trade.Commit()

        except ValidationError as ex:
            show_exception(format(ex))
            raise ex


def _validate_demat_trade_instrument_availability(trade):
    """
    Validate that the traded quantity of a demat instrument is
    available to (in the case of a sell) or from (in the case of
    a buy) the market.

    This validation is only applicable to trades that are between
    the issuer and the market.
    """
    instrument = trade.Instrument()
    issuer_bpid = get_party_demat_BPID(instrument.Issuer())
    acquirer_bpid = get_party_demat_BPID(trade.Acquirer())
    if acquirer_bpid != issuer_bpid:
        # Trade is not a sale to or buy from the market.
        return
    if trade.Quantity() < 0:
        # Sell trade.
        trade_nominal = trade.Nominal() * -1
        if trade_nominal > demat_available_amount(instrument):
            raise ValidationError('Trade nominal greater than instrument value available.')
    elif trade.Quantity() > 0:
        # Buy trade.
        if trade.Nominal() + demat_available_amount(instrument) > demat_authorised_amount(instrument):
            raise ValidationError('Instrument not available in the market, please book sell trades first.')


def _validate_demat_trade_denomination(trade):
    """
    Validate that the nominal of a demat trade is a multiple of the
    minimum trade-able quantity.
    """
    abs_nominal_in_cents = int(fabs(trade.Nominal()) * 100)
    min_denomination_in_cents = int(trade.Instrument().AdditionalInfo().Demat_MinTrdDeno() * 100)
    if abs_nominal_in_cents % min_denomination_in_cents != 0:
        raise ValidationError('Trade nominal is not a trade-able denomination.')


# to use default float reference associated with the instrument currency when saving a deposit with a float leg
def set_float_ref(shell, obj):
    """
    Set the default floating reference on trade.
    :param shell: FUxShell
    :param obj: FTrade or FInstrument
    """
    float_ref_default_dict = {'AUD':'AUD-3MBBR-3M',
                              'BRL':'BRL-LIBOR-3M',
                              'BWP':'BWP-TBILL-3M',
                              'CAD':'CAD-LIBOR-3M',
                              'CHF':'CHF-LIBOR-3M',
                              'CZK':'CZK-PRIBOR-3M',
                              'DKK':'DKK-CIBOR-3M',
                              'EUR':'EUR-EURIBOR-3M',
                              'GBP':'GBP-LIBOR-3M',
                              'GHS':'GHS-TBILL-3M',
                              'HUF':'HUF-BUBOR-3M',
                              'ILS':'ILS-TELBOR-3M',
                              'JPY':'JPY-LIBOR-3M',
                              'KES':'KES-TBILL-3M',
                              'MUR':'MUR-TBILL-3M',
                              'MZN':'MZN-TBILL-3M',
                              'NAD':'NAD-TBILL-3M',
                              'NGN':'NIBOR-3m',
                              'NOK':'NOK-NIBOR-3M',
                              'NZD':'NZD-LIBOR-3M',
                              'PLN':'PLN-WIBOR-3M',
                              'RUB':'RUB-MOSPRIME-3M',
                              'SEK':'SEK-STIBOR-3M',
                              'TZS':'TZS-TBILL-3M',
                              'UGX':'UGX-TBILL-3M',
                              'USD':'USD-LIBOR-3M',
                              'ZAR':'ZAR-JIBAR-3M',
                              'ZMK':'ZMK-TBILL-3M',
                              'ZMW':'ZMW-TBILL-3M'}

    if obj.IsKindOf('FInstrument') or obj.IsKindOf('FTrade'):
        if obj.IsKindOf('FTrade'):
            obj = obj.Instrument()

        if obj.IsKindOf('FDeposit'):
            leg = obj.Legs()[0]

            if obj.Legs():
                if leg.LegType() in ('Float', 'Capped Float', 'Floored Float', 'Call Float') and leg.FloatRateReference() is not None:                                             
                    if leg.Currency().Name() != leg.FloatRateReference().Currency().Name():

                        newRef = float_ref_default_dict[obj.Currency().Name()]
                        leg.FloatRateReference(newRef)
                        for cashflow in leg.CashFlows():
                            for reset in cashflow.Resets():
                                if reset.IsFixed():
                                    for price in leg.FloatRateReference().HistoricalPrices():
                                        if price.Day() == reset.Day() and price.Market().Name() == 'SPOT':
                                            fixingValue = price.Settle()
                                            reset.FixingValue(float(fixingValue))

                        msg = 'Float ref for leg currency %s defaulted to %s' % (leg.FloatRateReference().Currency().Name(), float_ref_default_dict[obj.Currency().Name()])
                        acm.UX().Dialogs().MessageBoxInformation(shell, msg)


def prevent_booking_old_portfolio(shell, obj):
    """
    Prevent booking to an old portfolio
    :param shell: FUxShell
    :param obj: FTrade or FInstrument
    """
    if obj.IsKindOf('FTrade'):
        if obj.Instrument().InsType()in ('ETF', 'Stock'):
            if obj.Portfolio().AdditionalInfo().RTMRestricted() == 'Yes':
                msg = 'Booking of %s trade on portfolio %s not allowed for RTM trades' % (obj.Instrument().InsType(), obj.Portfolio().Name())
                acm.UX().Dialogs().MessageBoxInformation(shell, msg)
                raise ValidationError('Could not book trade')

def set_trade_settle_cat(shell, obj):
    # set the trade settle category base on PM_FacilityAgent value.
    if obj.IsKindOf('FTrade'):
        if obj.AdditionalInfo().PM_FacilityAgent() == 'Absa Bank Limited':
            obj.SettleCategoryChlItem("Syndicated_Absa")
        elif obj.AdditionalInfo().PM_FacilityAgent() not in ['', None]:
            obj.SettleCategoryChlItem("Syndicated_Non-Absa")

def prevent_voiding_settling_trades(shell, obj):
    """
    Prevent voiding trades that are settling.
    :param shell: FUxShell
    :param obj: FTrade or FInstrument
    """
    if obj.IsKindOf('FTrade'):
        if obj.Instrument().InsType() == 'Curr' and obj.Status() == 'Void':
            currPair = obj.CurrencyPair()
            if currPair:
                valueDay = obj.ValueDay()
                spotDate = currPair.SpotDate(acm.Time.DateNow())
                daysToSettle = acm.Time.DateDifference(valueDay, acm.Time.DateNow())
                spotDaysOffset = acm.Time.DateDifference(spotDate, acm.Time.DateNow())
                if daysToSettle <= spotDaysOffset:
                    msg = 'FX trade is settling within %s days, TCU please ' \
                          'contact PTS prior to voiding the trade' % daysToSettle
                    acm.UX().Dialogs().MessageBoxInformation(shell, msg)
                    

def prevent_duplicate_cash_flows(shell, obj):
    """
    Display dialog containing duplicate cash flows in a money flow sheet.
    :param shell: FUxShell
    :param obj: FTrade or FInstrument
    :return: boolean
    """
    if obj.IsKindOf('FTrade'):
        obj = obj.Instrument()

    # Only perform check on instrument update for cash flow instruments
    if obj.IsKindOf('FDeposit'):
        instrument = obj
        duplicates = __get_duplicate_cash_flows(instrument)
        if duplicates:
            dialog = DialogDuplicateCashFlows(duplicates)
            if not acm.UX().Dialogs().ShowCustomDialogModal(shell, CreateLayout(), dialog):
                return True
    return False


def __get_duplicate_cash_flows(instrument):
    seen = set()
    duplicates = []

    if instrument.InsType() == 'Deposit':
        for flow in instrument.Legs().First().CashFlows():
            cashFlow = (flow.FixedAmount(), flow.PayDate(), flow.UpdateDay())
            if flow.FixedAmount() != 0:
                if cashFlow not in seen:
                    seen.add(cashFlow)
                elif flow.UpdateDay() == acm.Time.DateToday():
                    duplicates.append(flow)
    return duplicates


def get_acm_credit_facility_information(shell, params):
    return predeal_acm_credit_facility_check(shell, params)

def check_trade_settle_cat(shell, obj):
    """
    Check if trade settle catigory is Euroclear
    :param shell: FUxShell
    :param obj: FTrade or FInstrument
    """
    if obj.IsKindOf('FTrade'):
        ins = obj.Instrument()
        if ins.InsType() in ('Bond', 'FRN', 'IndexLinkedBond') and ins.Currency().Name() == 'ZAR' and ins.AdditionalInfo().Exchange()=='BESA':
            if obj.Status() == 'FO Confirmed':
                if obj.SettleCategoryChlItem():
                    if obj.SettleCategoryChlItem().Name() == 'Euroclear':
                        if obj.Counterparty().HostId():
                            EuroMsg = 'This trade will NOT go to JSE Nutron because the Trade Settle Category is Euroclear. '
                        else:
                            EuroMsg = 'Any alocations of this block trade will NOT go to JSE Nutron because the Trade Settle Category is Euroclear. '
                        
                        acm.UX().Dialogs().MessageBoxInformation(shell, EuroMsg)


# Main entry point called from the hook.
def validate_gui(shell, params):
    """Validate GUI before submitting the changes into FValidation."""
    # Bypass transaction validation.
    if ael.user().userid in SUPERUSERS:
        return acm.FDictionary()

    data = params['initialData']
    if not data:
        return None

    try:
        # Modify the data if necessary.
        obj = data['editObject']

        # Validate on insert or edit.
        if obj:
            premium_check(shell, obj)
            extend_deposit_about_quotation(shell, obj)
            set_float_ref(shell, obj)
            corresponding_companion_spread(shell, obj)
            check_MTM_version(shell, obj)
            check_credit_sales(shell, obj, data)
            check_demat_fields(shell, obj, data)
            prevent_booking_old_portfolio(shell, obj)
            prevent_voiding_settling_trades(shell, obj)
            update_trade_groupref(shell, obj)
            validate_and_show_ssi_choosing_gui(shell, params)
            set_trade_settle_cat(shell, obj)
            check_trade_settle_cat(shell, obj)
            if prevent_duplicate_cash_flows(shell, obj):
                return None
            if ncd_jibar_contribution_check_failed(shell, obj):
                return None
            calculate_and_save_sales_credits(shell, obj)
            if fix_lockout_resets_check_failed(shell, obj):
                return None
            #FAFO-85 API call to ACM to get credit facility data for loans
            if not get_acm_credit_facility_information(shell, params):
                return None
            if lch_mw_check_failed(shell, obj):
                return None

    except ValidationError as e:
        # Print error message to Prime's console.
        LOGGER.error("Validation Error: %s", e)

        # By returning None Prime stops saving the changes.
        return None

    # when returning FDict Prime will continue saving the changes
    return params  # acm.FDictionary()

