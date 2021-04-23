"""Deprecated FValidation module.

This module contains rules that have not (yet) been fully refactored
and integrated into the new FValidation modules.  No new rules should
be added to this module, only hotfixes if necessary.


HISTORY
=======================================================================================================================================================
Date            Change no       Developer               Requestor               Description
-------------------------------------------------------------------------------------------------------------------------------------------------------
                616426          Heinrich Cronje         Venessa Kennel (PCG)    Only users in FO PSSecLend Trader group can deleted SecLoan cashflows.
                                                                                No other person with FO Call Trades in their profile can deleted cashflows.
                852383          Jaysen Naicker          Dirk Strauss (MO)       Check swaptions so that the swap and option both have the same type of fixed leg.
                875685          Jaysen Naicker          Alex Boshoff            Fix swaption check to look for the fixed leg on the underlying swap
                ???             Anwar Banoo             Haroon Mansoor (PCG)    Added support for floating rate deposit/loan - existing validation
                                                                                prevented anything other than fixed rate from being booked
2011-04-18      626123          Rohan vd Walt                                   Exclude AMBA user from FICA check on counterparty and acquirer
2012-02-16      48574           Heinrich Cronje                                 Allow Deletion of Simulated Cashflows for FO Call Trader
2012-07-20      318335          Aaeda Salejee           Julian Naik (Credit)    Added product restriction check for Credit and Ccg
2012-08-08      ABITFA-1511     Anwar Banoo             Prime PCG               Changed call validation to validate daycount against currency against instrument for everything other than funding desk
2012-10-26      ABITFA-1301     Tomas Adler             Pedro De Moura          Add Barrier exotic event monitoring functionallity
2012-11-07      586166          Jan Sinkora             Pedro de Moura (PCG)    Prevent trades to be booked on options with underlying swaps or FRAs when the strike price != the underlying fixed rate
2013-05-16      1024176         Jan Sinkora                                     ABITFA-1821 - Preventing cash-posting trades involved in the archiving process from being changed
2013-06-06      1079567         Jan Sinkora                                     Fix for the validation introduced in previous release - more strict distinguishing of the aggregate cash-posting trades
2014-08-31      CHNG0002210109  Vojtech Sidorin                                 Mark as deprecated module
2014-09-39      CHNG0002328679  Dmitry Kovalenko                                Updated imports and removed usage of the Information class
2015-02-12                      Vojtech Sidorin                                 Refactor rule 85; move it to FValidation_FOCallTrader.
2015-08-20      ABITFA-3743     Vojtech Sidorin                                 Include rule numbers in messages.
2016-02-18      ABITFA-3840     Ondrej Bahounek                                 Change messages to be more specific
2017-10-05      ABITFA-5071     Gabriel Marko                                   Make FV83-2c case insensitive
2018-07-05      FAOPS-127       Cuen Edwards                                    Updated several rules to cater for simulated trades.  Before this change, simulated trades were being filtered out in
                                                                                the main FValidation module.  This has now been relaxed in order to prevent changes to simulated trades created to own 
                                                                                multi-trade confirmations (e.g. term statements, loan notices, etc.).
2018-09-05      FAOPS-185       Bhavnisha Sarawan       Sarah Elstob            Add a check for Asset Managers. Asset Managers do not need to be FICA Compliant to book Block Trades.
2019-11-07	FAOPS-42	Jaysen Naicker		Rayan Govender		Amend Rule 75a to bypass check on BESA instrument for Euroclear payments
2020-02-06      PCGDEV-221      Sihle Gaxa              Shaun Du Plessis        Amend Rule 75a to bypass check on BESA instrument for SBL collateral instruments
-------------------------------------------------------------------------------------------------------------------------------------------------------
"""


import ael, acm
from aggregation import LOCKED_TRADE_TEXT

from FValidation_core import (DataValidationError,
                              show_validation_warning,
                              validate_entity)

BESA_INSTRUMENTS = ('Bond', 'BuySellback', 'Repo/Reverse', 'FRN', 'IndexLinkedBond')
ALLOWED_PRODUCTS = ('Bond', 'BuySellback', 'Cap', 'CFD', 'CLN', 'CreditDefaultSwap', 'Curr', 'CurrSwap', 'EquityIndex', 'Floor', 'FRA', 'FRN', 'Future/Forward', 'FXOptionDatedFwd', 'IndexLinkedBond', 'IndexLinkedSwap', 'Option', 'Portfolio Swap', 'Repo/Reverse', 'Swap', 'TotalReturnSwap', 'VarianceSwap', 'Warrant')
BSB_COUNTERPARTIES = (5336, 531, 13481) # ABSA SECURITIES LENDING, MORGAN STANLEY CAP SERVICED NY, SABFIN PTY LTD
MENTIS_PORTS = ['SF1511', 'SF 9926' ]
FIRSTDAYOFNEXTMONTH = ael.date_today().add_months(1).first_day_of_month().adjust_to_banking_day(ael.Instrument['ZAR'])
FUNDING_DESK =   ael.Party['Funding Desk']
AGRI_DESK    =   ael.Party['Agris Desk']
PS_DESK      =   ael.Party['PRIME SERVICES DESK']
NON_ZAR_CFC  =   ael.Party['ABCAP NON ZAR CFCI DIV']
CALL_ACQUIRERS = [FUNDING_DESK, PS_DESK, NON_ZAR_CFC]

# General Trade Validation

@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def validate_trade_gen(e, op):

    """

        VALIDATE TRADE GENERAL - INSERT AND UPDATE
        ==========================================

        a) Ensure that a trade has a counterparty
        b) Check that the counterparty of a trade is FICA Compliant
        c) Check that the counterparty of a trade does not have a product restriction and only trades allowed products
        d) Ensure that a trade has an acquirer
        3) Check that the acquirer of a trade is FICA Complaint
        f) Ensure that Bonds, BSB and Repos are booked against BESA Compliant counterparties, if the counterparty is external
        g) Only Repos and not BSB to be booked with specific counterparties
        h) Only Simulated trades in portfolio IRD_SIMULATED
        i) Trades in the Mentis Portfolios must have a Mentis Project Number on the trades
        j) Commodity Trades with an external ID beginning with SFX2_ and instrument name HOLDER, have value and acq day set to First Business Day of Next Month
        k) Commodities booked against the Agri Desk must have an AgriStatus

    """

    # Rule 74
    #Insert and Update
    if (ael.user() != ael.User['AMBA']):
        if e.counterparty_ptynbr:
            if e.counterparty_ptynbr.add_info('FICA_Compliant') == 'No' and e.counterparty_ptynbr.add_info('RegulatedAstMngBulk') in ('No', ''):
                raise DataValidationError("FV74-2a: The Counterparty '%s' is not FICA Compliant." %e.counterparty_ptynbr.ptyid)
            elif e.counterparty_ptynbr.add_info('FICA_Compliant') == 'No' and e.counterparty_ptynbr.add_info('RegulatedAstMngBulk') == 'Yes':
                if e.optkey1_chlnbr is None or e.optkey1_chlnbr.entry != 'Block Trade':
                    raise DataValidationError("FV74-2b: Client '%s' is not compliant for direct trade. Select TradArea = Block Trade if applicable" %e.counterparty_ptynbr.ptyid)
            else:
                if e.counterparty_ptynbr.add_info('Product Restriction') == 'Exemption 4':
                    if e.insaddr.instype not in ALLOWED_PRODUCTS:
                        raise DataValidationError("FV74-3: The Counterparty '%s' is not allowed to trade instrument '%s'. "
                            %(e.counterparty_ptynbr.ptyid, e.insaddr.insid) + "Please contact CCG and Credit." )
        else:
            raise DataValidationError("FV74-1: Please select a Counterparty")

        if e.acquirer_ptynbr:
            if e.acquirer_ptynbr.add_info('FICA_Compliant') == 'No':
                raise DataValidationError("FV74-5: The Acquirer that you have selected to trade with is not FICA Compliant.")
        else:
            raise DataValidationError("FV74-4: Please select an Acquirer")

    # Rule 75
    if e.insaddr.instype in BESA_INSTRUMENTS:
        # Rule 75a
        # 2014-08-11 Vojtech Sidorin: Limit rule only to instruments traded on
        #     BESA exchange (amended by Anwar Banoo).
        if e.insaddr.add_info('Exchange') == 'BESA' or (e.insaddr.und_insaddr and e.insaddr.und_insaddr.add_info('Exchange') == 'BESA'):
            if not((e.settle_category_chlnbr and e.settle_category_chlnbr.entry == 'Euroclear') or (e.category == "Collateral")):
                if e.counterparty_ptynbr.add_info('BESA_Member_Agree') == 'No' and e.counterparty_ptynbr.type != 'Intern Dept':
                    raise DataValidationError("FV75a: The party '%s' does not have a BESA Client agreement set up" %e.counterparty_ptynbr.ptyid)

        # Rule 75b
        if e.insaddr.instype == 'BuySellback' and e.insaddr.und_instype == 'Bond':
            if e.counterparty_ptynbr.ptynbr in BSB_COUNTERPARTIES:
                raise DataValidationError("FV75b: Please book a Repo not a BSB with this counterparty")

    # Rule 76
    if e.status != 'Simulated' and e.prfnbr.prfid == 'IRD_SIMULATED':
        raise DataValidationError("FV76: Unable to commit the trade because only simulated trades are allowed in the IRD_SIMULATED Portfolio")

    # Rule 77
    if e.status != 'Simulated' and e.prfnbr.prfid in MENTIS_PORTS:

        if not e.add_info('Mentis Project Num'):
            raise DataValidationError("FV77: Traders not allowed to capture trade without Mentis Project Num")

    if e.insaddr.instype == 'Commodity':
        # Rule 78
        if  e.optional_key:
            if e.insaddr.insid.find('HOLDER') == 9 and e.optional_key.find('SFX2_') == 0:
                e.value_day = e.acquire_day = FIRSTDAYOFNEXTMONTH
                show_validation_warning('FV78: Value and Acquire Day set to the first business day of next month')

        # Rule 79
        if e.acquirer_ptynbr == AGRI_DESK:
            if e.add_info('AgriStatus') == '':
                raise DataValidationError('FV79: Please select Physical in the AgriStatus AddInfo field')

# Rule 83
@validate_entity("Trade", "Insert", caller="validate_transaction")
@validate_entity("Trade", "Update", caller="validate_transaction")
def validate_call_trade(e, op):

    """

        VALIDATE CALL TRADE - INSERT AND UPDATE
        =======================================

        a) Fixed Period must be selected for Funding Desk, Prime Services Desk and Non ZAR CFC I/DIV

        For Funding Desk:
            - A Call Region must be specified
            - An Account name must be specified
            - The Funding Instype must begin with 'Call'
            - The Daycount method must be Act/365
            - The poortfolio for the trade must beging with 'Call_'

        For Everybody else:
            - The daycount method must be the same as the daycount of the instrument currency


    """
    if e.insaddr.instype == 'Deposit' and e.insaddr.legs().members()!= [] and e.insaddr.legs()[0].type == 'Call Fixed Adjustable':

        if e.acquirer_ptynbr in CALL_ACQUIRERS:

            if e.insaddr.legs()[0].fixed_coupon == 0:
                raise DataValidationError('FV83-1: Please select the Fixed Period.')


            if e.acquirer_ptynbr == FUNDING_DESK: #Funding Desk
                
                if not e.add_info('Call_Region'):
                    raise DataValidationError('FV83-2a: Please select a region for the Call Account')

                if e.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                    if not e.add_info('Account_Name'):
                        raise DataValidationError('FV83-2b: Please add an Account Name.')

                if not (e.add_info('Funding Instype').lower().startswith('call') or e.add_info('Funding Instype').lower().startswith('access')):
                    raise DataValidationError('FV83-2c: Please change the Funding Instype.')
                
                if e.status != 'Simulated' and e.prfnbr.prfid[0:5] != 'Call_':
                    raise DataValidationError('FV83-2d: Unable to commit the trade. Please pick a Call portfolio')

                if e.insaddr.legs()[0].daycount_method != 'Act/365':
                    raise DataValidationError('FV83-2e: The daycount method is not Act/365.')

            else:
                cur = e.insaddr.curr
                ldc = e.insaddr.legs()[0].daycount_method
                cdc = cur.legs()[0].daycount_method

                if ldc != cdc:
                    raise DataValidationError('FV83-3: The daycount method for the %s currency should be %s' %(cur.insid, cdc))

# Rule 84
@validate_entity("Instrument", "Update", caller="validate_transaction")
def validate_call_instrument(e, op):

    """

        VALIDATE CALL INSTRUMENT - UPDATE ONLY
        ======================================

        a) Fixed Period must be selected for Funding Desk, Prime Services Desk and Non ZAR CFC I/DIV

        For Funding Desk:
            - The Daycount method must be Act/365

        For Everybody else:
            - The daycount method must be the same as the daycount of the instrument currency


    """
    if e.instype == 'Deposit' and e.legs().members() != [] and e.legs()[0].type == 'Call Fixed Adjustable':

        if e.legs()[0].daycount_method != 'Act/365' or e.curr.insid != 'ZAR':
            if len(e.original().trades()) == 1:
                for t in e.original().trades():

                    if (t.acquirer_ptynbr == FUNDING_DESK):   #Funding Desk
                        if e.curr.insid != 'ZAR':  #can only be non zar or daycount incorrect
                            raise DataValidationError('FV84-1a: The currency is not set to ZAR.')
                        else:
                            raise DataValidationError('FV84-1b: The daycount method is not Act/365.')

                    if t.acquirer_ptynbr in CALL_ACQUIRERS:
                        cur = t.curr
                        ldc = e.legs()[0].daycount_method
                        cdc = cur.legs()[0].daycount_method
                        if ldc != cdc:
                            raise DataValidationError('FV84-2: The daycount method for the %s currency should be %s' %(cur.insid, cdc))


        if e.legs()[0].fixed_coupon == 0:
            if len(e.original().trades()) == 1:
                for t in e.original().trades():
                    if t.acquirer_ptynbr in CALL_ACQUIRERS:   #Funding Desk
                        raise DataValidationError('FV84-1c: Please select the Fixed Period.')

# Rule 86
@validate_entity("Instrument", "Insert")
@validate_entity("Instrument", "Update")
def validate_swaption_trade(e, op):

    """

        VALIDATE SWAPTION TRADE - INSERT AND UPDATE
        ===========================================

        a) Swap and Option shold both have Receive Fixed leg or Pay Fixed Leg


    """
    if e.instype == 'Option' and e.und_instype == 'Swap':
        if (acm.FInstrument[e.und_insaddr.insid].RecLeg().LegType() == 'Fixed' and e.call_option == 1) or (acm.FInstrument[e.und_insaddr.insid].PayLeg().LegType() == 'Fixed' and e.call_option == 0):
            raise DataValidationError('FV86: Option and underlying swap should have receiver or payer type set to the same on both.')



# Rule 87
@validate_entity("Instrument", "Insert", caller="validate_transaction")
@validate_entity("Instrument", "Update", caller="validate_transaction")
def validate_barrier_instrument(e, op):
    """
        VALIDATE BARRIER OPTION INSTRUMENT - INSERT AND UPDATE
        ======================================================

        a) Any barrier option should have 'monitoring' set
        b) 'Window' or 'Discrete' barrier options should have at least one 'Barrier Date' set
        c) All 'Barrier Date' entries should be before the option's expiry date

    """
    if e.record_type == 'Instrument' and op in ('Insert', 'Update') and e.instype == 'Option':
        if e.exotic_type == "Other" and e.exotic() and e.exotic().barrier_option_type != "None":
            bm = e.exotic().barrier_monitoring
            all_events = e.exotic_events()
            barrier_date_events = [event for event in all_events if event.type == "Barrier date"]
            if bm == "None":
                raise DataValidationError("FV87-1: ERROR, Must select Barrier Monitoring!")
            elif bm == "Window" or bm == "Discrete":
                if len(barrier_date_events) == 0:
                    raise DataValidationError("FV87-2a: ERROR, Selected %s barrier monitoring, but no date set!" %bm)
                else:
                    for event in barrier_date_events:
                        if event.date > e.exp_day or event.end_date > e.exp_day:
                            raise DataValidationError("FV87-2b: ERROR, Exotic event (Barrier date) must be before expiry!")





# the tolerance for fixed rate floating point comparison
FIXED_RATE_TOLERANCE = 0.00001

def float_eq(f1, f2, eps):
    """Floating point comparison."""
    return abs(f1 - f2) < eps

def option_and_underlying_eq_rates(opt, und):
    """
    Compare the option and the underlying Swap or FRA
    in terms of strike price vs fixed rate.

    """
    if und.instype == 'Swap':
        fixed_leg = filter(lambda l: l.type == 'Fixed', und.legs())[0]
    elif und.instype == 'FRA':
        fixed_leg = und.legs()[0]

    return float_eq(opt.strike_price, fixed_leg.fixed_rate, FIXED_RATE_TOLERANCE)

# Rule 88
@validate_entity("Trade", "Insert")
@validate_entity("Trade", "Update")
def validate_swap_or_fra_option_trade_rates(e, op):
    """
    The underlying fixed rate should be equal to the strike price of the option.
    """
    ins = e.insaddr
    und = ins.und_insaddr
    if ins.instype == 'Option' and und and und.instype in ('Swap', 'FRA'):
        # compare the rate with the strike price
        if not option_and_underlying_eq_rates(ins, und):
            raise DataValidationError('FV88: Booking an Option trade while the strike '
                                      'price is different from the underlying '
                                      'fixed rate.')

# Rule 89
@validate_entity("Instrument", "Update")
def validate_swap_or_fra_option_instrument_change(e, op):
    """
    Swaption/FRA option strike prices should not be changed when
    a trade is booked.

    """
    ins = e
    und = ins.und_insaddr
    if ins.instype == 'Option' and und.instype in ('FRA', 'Swap'):
        if not option_and_underlying_eq_rates(ins, und):
            trades = ael.Trade.select('insaddr = {0}'.format(e.insaddr))
            if trades:
                show_validation_warning('FV89: Warning: Changing the strike price while there '
                                 'are trades booked for this option.')
                # uncomment this in case the business users want to switch to
                # raising exceptions (to disable the action)
                #raise DataValidationError('Changing the strike price while there '
                #                          'are trades booked for this option.')

# Rule 90
@validate_entity("Leg", "Update")
def validate_fixed_leg_change(e, op):
    """
    A fra's/swap's fixed rate should not be changed when a trade
    is booked on the overlying option.

    """
    ins = e.insaddr
    if ins.instype in ('FRA', 'Swap'):
        overlying = ael.Instrument.select("und_insaddr = '{0}'".format(ins.insaddr))

        # if any overlying option has any trades associated with it, show
        # the notice
        options_with_trades = []
        for o in overlying:
            if o.instype == 'Option':
                if not float_eq(o.strike_price, e.fixed_rate, FIXED_RATE_TOLERANCE) and o.trades():
                    options_with_trades.append(o.insid)

        if options_with_trades:
            err = ('FV90: Warning: Changing the fixed rate when there are trades booked '
                   'for overlying options: {0}.').format(', '.join(options_with_trades))
            show_validation_warning(err)
            # uncomment this in case the business users want to switch to
            # raising exceptions (to disable the action)
            #err = ('Changing the fixed rate when there are trades booked for '
            #       'overlying options: {0}.').format(', '.join(options_with_trades)
            #raise DataValidationError(err)

def has_trades_of_statuses(instrument, statuses):
    return any(map(lambda t: t.status in statuses, instrument.trades()))

def user_is_allowed(user, component, component_type):
    return user.IsAllowed(component, component_type)

# Rule 91
@validate_entity("Instrument", "Update")
def validate_trs_index_ref_change(e, op):
    """
    When a Total Return Swap has a BO or BO-BO confirmed trade, the index-ref'd
    equity index cannot be amended without having the 'Modify FO Part' component.

    This is set up only updates.

    """
    component = 'Modify FO Part'
    confirmed_statuses = ('BO Confirmed', 'BO-BO Confirmed')
    msg_invalid = ("FV91: Instrument has confirmed trades. "
                   "You need the following actions to be able to change this instrument: "
                   "'{0}'").format(component)

    user = acm.User()
    if e.instype == 'EquityIndex' and not user_is_allowed(user, component, 'Operation'):
        legs = ael.Leg.select('index_ref = {0}'.format(e.insaddr))
        trss = [i for i in map(lambda l: l.insaddr, legs) if i.instype == 'TotalReturnSwap']
        if any(map(lambda i: has_trades_of_statuses(i, confirmed_statuses), trss)):
            raise DataValidationError(msg_invalid)

# Rule 92
@validate_entity("Trade", "Update")
@validate_entity("Trade", "Delete")
def validate_cash_posting_trade_lock(e, op):
    """
    A trade cannot be changed if it's owned by FMAINTENANCE and is of type 'Cash posting'.

    """
    orig = None
    if op == 'Update':
        orig = e.original()
    elif op == 'Delete':
        orig = e

    if (orig and orig.type == 'Cash Posting'
            and orig.owner_usrnbr.userid == 'FMAINTENANCE'
            and orig.text1 == LOCKED_TRADE_TEXT):
        raise DataValidationError("FV92: Cannot change a locked cash posting "
                                  "trade during archivation preparation.")
