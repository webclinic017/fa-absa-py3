""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPHook.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FFBDPHook - Module where customisation can be done.

DESCRIPTION
    This module contains a number of AEL hook function templates, which,
    if defined, is called by BDP.
    Customers can do their own customisation for e.g. valuation of
    MtM-prices, decimal rounding, defining trade field values for
    generated trades, trade status for aggregation.

RENAME this module to FBDPHook. Also remove "_template" from those
    functions that should be called and used.
----------------------------------------------------------------------------"""

import acm
import ael


from FBDPCurrentContext import Logme

from FBDPCommon import getMaxNameLength

"""
************************
*      GENERAL BDP     *
************************
"""


"""aef-------------------------------------------------------------------------
hook.FBDPHook::recalculate_position

This hook is called from BDPCalculatePosition procedure, which is used to
calculate positions in the scripts FCorporateAction, FExerciseAssign and
FExpiration.  This hook is called in the end of the BDPCalculatePosition
procedure and it is used modify the calculated position.  The list of positions
returned should contain clones of trade entities, either created with the
clone() method, or the new() method.

If this hook is activated, BDPCalculatePosition will return the positions
defined here instead of the default position calculated in
BDPCalculatePosition.  If an exception is raised in the hook, the default
position will be used.  All GUI Parameter values are accessible by the hook.
The hook is activated by renaming the hook function from
**recalculate_position_template** to **recalculate_position**.

@category BDP CalculatePosition
@param instrument:Instrument The instrument for which to create a position.
@param default_pos:list A list of the default positions of the instrument.
each default position is a list of calculated trades and original trades.
eg: [[t_calc1, t_calc2], [t_orig1, ..., t_origN]]
@param parameters:dict A dictionary with GUI parameters {parameter: value}
@return list A list of the positions of the instument
positions in the same format: [[t_new,...], [t_orig1, ..., t_origN]]
@example
def recalculate_position(instrument, default_pos, parameters):
    positions = default_pos
    otc = parameters['AdjustOTC']
    if logme.ScriptName == 'Corporate Action':
        if (otc == 'All' or otc == 'Only OTC') and instrument.otc:
            calc_trades = [t.clone() for t in instrument.trades()]
            orig_trades = [t for t in instrument.trades()]
            positions = [[calc_trades, orig_trades]]

        CA = parameters['CorporateAction']
        #modify trades and instrument if needed
        for pos in positions:
            for calc_trade in pos[0]:
                calc_trade.text1 = "CA " + str(CA.Oid())
    elif logme.ScriptName == 'Exercise Assign':
        pass
    elif logme.ScriptName == 'Expiration':
        pass
    return positions
----------------------------------------------------------------------------"""


def recalculate_position_template(instrument, default_pos, parameters):
    positions = default_pos
    if Logme().ScriptName == 'Corporate Action':
        pass
    elif Logme().ScriptName == 'Exercise Assign':
        pass
    elif Logme().ScriptName == 'Expiration':
        pass
    return positions


"""----------------------------------------------------------------------------
FUNCTIONS
    set_trade_field_counterparty(trades, default)
    set_trade_field_acquirer(trades, default)
    set_trade_field_trader(trades, default)
    set_trade_field_market(trades, default)
    set_trade_field_broker(trades, default)
    set_trade_field_owner(trades, default)
    set_trade_field_optkey1(trades, default)
    set_trade_field_optkey2(trades, default)
    set_trade_field_optkey3(trades, default)
    set_trade_field_optkey4(trades, default)
    set_trade_field_cp_ref(trades, default)
    set_trade_field_status(trades, default)
    set_trade_field_text1(trades, default)
    set_trade_field_text2(trades, default)

DESCRIPTION
    These functions can be used for overriding administrative fields of
    generated trades.
    These functions are used by Aggregation, Corporate Action and Expiration.
    NOTE! If a certain trade grouping criteria has been specified for a
    Aggregation Rule, the corresponding set_trade_field hook will be ignored
    for that rule. In this case the aggregate trade's field will get the
    field value of the trade group it represents.

ARGUMENTS
    trades  - a list of AEL Trade objects
    default - a default value that can be used as return value.

RETURNS
    The following functions should return an integer:
      set_trade_field_counterparty(trades, default)
      set_trade_field_acquirer(trades, default)
      set_trade_field_trader(trades, default)
      set_trade_field_market(trades, default)
      set_trade_field_broker(trades, default)
      set_trade_field_owner(trades, default)
      set_trade_field_optkey1(trades, default)
      set_trade_field_optkey2(trades, default)
      set_trade_field_optkey3(trades, default)
      set_trade_field_optkey4(trades, default)
      set_trade_field_contract_trade(trades, default)
    The following functions should return a string:
      set_trade_field_cp_ref(trades, default)
      set_trade_field_status(trades, default)
      set_trade_field_text1(trades, default)
      set_trade_field_text2(trades, default)
----------------------------------------------------------------------------"""

def set_trade_field_contract_trade_template(trades, default):
    """
    Default: 0
    """
    if trades:
        return trades[0].contract_trdnbr
    else:
        return default


def set_trade_field_counterparty_template(trades, default):
    """
    Default: ptynbr for Party FMAINTENANCE
    """
    if trades:
        return trades[0].counterparty_ptynbr.ptynbr
    else:
        return default


def set_trade_field_acquirer_template(trades, default):
    """
    Default: ptynbr for Party FMAINTENANCE
    """
    if trades:
        return trades[0].acquirer_ptynbr.ptynbr
    else:
        return default


def set_trade_field_trader_template(trades, default):
    """
    Default: usrnbr for User FMAINTENANCE
    """
    if trades:
        return trades[0].trader_usrnbr.usrnbr
    else:
        return default


def set_trade_field_market_template(trades, default):
    """
    Default: 0
    """
    if trades:
        return trades[0].market_ptynbr.ptynbr
    else:
        return default


def set_trade_field_broker_template(trades, default):
    """
    Default: 0
    """
    if trades:
        return trades[0].broker_ptynbr.ptynbr
    else:
        return default


def set_trade_field_owner_template(trades, default):
    """
    Default: usrnbr for Current User
    """
    if trades:
        return trades[0].owner_usrnbr.usrnbr
    else:
        return default


def set_trade_field_optkey1_template(trades, default):
    """
    Default: 0
    """
    if trades and trades[0].optkey1_chlnbr:
        return trades[0].optkey1_chlnbr.seqnbr
    else:
        return default


def set_trade_field_optkey2_template(trades, default):
    """
    Default: 0
    """
    if trades and trades[0].optkey2_chlnbr:
        return trades[0].optkey2_chlnbr.seqnbr
    else:
        return default


def set_trade_field_optkey3_template(trades, default):
    """
    Default: 0
    """
    if trades and trades[0].optkey3_chlnbr:
        return trades[0].optkey3_chlnbr.seqnbr
    else:
        return default


def set_trade_field_optkey4_template(trades, default):
    """
    Default: 0
    """
    if trades and trades[0].optkey4_chlnbr:
        return trades[0].optkey4_chlnbr.seqnbr
    else:
        return default


def set_trade_field_cp_ref_template(trades, default):
    """
    NOTE! set_trade_field_cp_ref should return a string
    Default: ""
    """
    if trades:
        return trades[0].your_ref
    else:
        return default


def set_trade_field_status_template(trades, default):
    """
    NOTE! set_trade_field_status should return a string
    Statuses Simulated and Reserved are not allowed.
    """
    if trades[0].status == "Exchange":
        return "Exchange"
    else:
        return default


def set_trade_field_text1_template(trades, default):
    """
    NOTE! set_trade_field_text1 should return a string
    Default: ""
    """
    if trades[0].text1 == "":
        return "This is a text"
    else:
        return trades[0].text1


def set_trade_field_text2_template(trades, default):
    """
    NOTE! set_trade_field_text2 should return a string
    Default: ""
    """
    return "This is another text"


"""----------------------------------------------------------------------------
FUNCTION
    trade_status_to_aggregate(status) - Used to redefine which trades
    statuses to be included when aggregating or calculating trades.

DESCRIPTION
    In Aggregation Rules, by default, trades with status Simulated and
    Reserved are not included in the selection of trades for
    aggregation or calculation, i.e. position calculation used by
    Corporate Action and Expiration.
    The default behaviour can be overridden by this AEL hook function.
    The function trade_status_to_aggregate defines whether trades with
    trade status 'status' should be aggregated or be left out.

ARGUMENT
    status - a string

RETURNS
    One of the following strings:
      "Aggregate"
      "None"
----------------------------------------------------------------------------"""


def trade_status_to_aggregate_template(status):
    if status == "Simulated" or status == "Void":
        return "None"
    else:
        return "Aggregate"


"""----------------------------------------------------------------------------
FUNCTION
    Exclude hook - Used to define whether some trades are to be excluded
    in Trade Aggregation.

DESCRIPTION
    The Trade Aggregation Rule allows for additional trade filtering to be
    applied by using this AEL hook function.  The function should be defined
    inside a python file by receiving the trade as an AEL object and return
    whether the trade should be included in or excluded from the aggregation.
    The 'ExcludeHook' field in Trade Aggregation Rule should be set to the
    corresponding Exclude hook name.

    For example, to enable an exclude hook called 'example_of_exclude_hook()':
    1. The definition of the hook function needs to be defined in FBDPHook.py
       (or another Python file).
    2. 'ExcludeHook' field in the Trade Aggregation Rule needs to be set to
       'example_of_exclude_hook' if it is defined in FBDPHook.py (or
       'OtherPythonFile.example_of_exclude_hook' if it is defined in another
       python file).

ARGUMENT
    trade - a AEL trade

RETURNS
    One of the following strings:
      1 - if the trade should be excluded from the aggregation
      0 - if the trade should be included in the aggregation
----------------------------------------------------------------------------"""


def example_of_exclude_hook(trade):
    # Exclude all trades done in the Euro currency
    if trade.curr.insid == 'EUR':
        return 1
    else:
        return 0


"""
*************************
*    CORPORATE ACTION   *
*************************
"""


"""aef-------------------------------------------------------------------------
hook.FBDPHook::corporate_action_selection

This hook is called from the Corporate Action BDP procedure, before any
processing has started.  It is used to modify the instrument selection, which
equals the addresses of the instrument specified in the parameters window if
the field InstrumentType is not of type Derivative or subtypes of Derivative
(instument types that are derivatives, like Option, Warrant, etc).  In the case
when InstrumentType is Derivative or subtypes of Derivative, the selections
will be all derivatives of the instument that match the selected
InstrumentType.  All Corporate Action Parameter values are accessible by the
hook.

@category BDP.CorporateActions
@param instrumentSelection:list A list of instrument addresses
@param parameters:dict A dictionary with parameters {parameter: value}
@return list A list of the instrument addresses that the script should process
----------------------------------------------------------------------------"""


def corporate_action_selection(instrumentSelection, parameters):
    return instrumentSelection


# """aef----------------------------------------------------------------------
# hook.FBDPHook::get_corporate_actions
#
# This hook allows you to define the initial selection of corporate actions,
# using the method ca_candidate(..).
# This selection will be used as a firsthand choice if no Corporate Action or
# Template is specified in the guiparameters.
# The hook can also be used for custom processing of any kind. This can be
# done in the function ca_modify(..).
# All Corporate Action Parameter values are accessible by the hook.
# The hook is activated by renaming the hook function from
# **get_corporate_actions_template** to **get_corporate_actions**.
#
# @category BDP.CorporateActions
# @param guiParameters:dict A dictionary with parameters {parameter: value}
# @return list A list of the FCorporateActions the scrript should process.
# @example
# def ca_candidate(ca, upto_date):
#     guiParameters = get_corporate_actions.guiParameters
#     if ca.ExDate() and toDate(ca.ExDate()) == upto_date:
#         return True
#     return False
#
# def ca_modify(ca):
#     list = []
#     ca.Text = "My Text"
#     list.append(["Text"])
#     return (ca, list)
# -------------------------------------------------------------------------"""


def get_corporate_actions_template(guiParameters):

    from FBDPCommon import toDate

    def ca_candidate(ca, upto_date):
        """
        Filter corporate actions. Use this to select corporate actions.
        Return True to select it, False to filter it away.
        """
        if ca.ExDate() and toDate(ca.ExDate()) == upto_date:
            return True
        return False

    def ca_modify(ca):
        """
        Used to modify the selected corporate actions. List should contain the
        names of modified attributes.
        """
        lst = []
        return (ca, lst)

    get_corporate_actions.guiParameters = guiParameters
    try:
        upto_date = toDate(guiParameters['Date'])
        upto_date.to_string()  # raise exception if Date is empty string
    except AttributeError:
        raise Exception('There was no Date specified.')
    corpactions = filter(lambda x: ca_candidate(x, upto_date),
            acm.FCorporateAction.Instances())

    if guiParameters['Logmode']:
        Logme()("Customised selection of Corporate Actions called with date " +
                str(upto_date), 'INFO')
        if len(corpactions) > 0:
            Logme()('The following corporate actions will be processed:',
                    'DEBUG')
            for m in corpactions:
                Logme()('Name: %-s, Date: %-s, Status: %-s' % (m.Name(),
                        m.Exdate(), m.Status()), 'DEBUG')
        else:
            Logme()('No corporate actions to process.', 'DEBUG')

    CA_list = list(map(ca_modify, [c.Clone() for c in corpactions]))
    return ([c[0] for c in CA_list], [c[1] for c in CA_list])


# """aef------------------------------------------------------------------
# hook.FBDPHook::update_old_instrument_hook
#
# This hook is called from the Corporate Action script if Method does not
# equal Adjust.  It provides the possibility to adjust the old derivative
# instrument. old_ins is the clone of the old instrument in which
# modifications should be made.
#
# Adjustments made to the instrument will only be supported in the rollback
# functionality if a list of changed attribute names are returned along with
# the instrument in a tuple.  In the same way, adjustments made to children
# of the entity will only be supported in the rollback functionality if a
# list of tuples are returned as a third element, along with the new
# instrument and the list of changed instrument attributes. These tuples
# must contain a child entity, along with a list of changed attributes if
# it is an clone.
#
# The hook is activated by renaming the hook function from
# **update_old_instrument_hook_template** to **update_old_instrument_hook**.
#
# @category BDP.CorporateActions
# @param old_ins:object The old instrument
# @param ca:object An instance of a subclass to FCATypes.CorpactType
# @return Tuple A tuple containing the old instrument, a list of modified
# attribute names, and a list of tuples for the children
#
# @example
# def update_old_instrument_hook(new_ins, ca):
#     list_of_adjusted_instrument_properties = []
#     #modifications to the instrument
#     #updates the list with updated attributes
#     return (new_ins, list_of_adjusted_instrument_properties)
#
# def update_old_instrument_hook(new_ins, ca):
#     list_of_adjusted_instrument_properties = []
#     list_of_children_tuples = []
#     #modifications to the instrument
#     #updates the list with updated attributes
#
#     c1 = child_entity
#     #modifies attributes of child
#     tuple = (c1, list_of_adjusted_child_attributes)
#     list_of_children_tuples.append(tuple)
#
#     c2 = another_child_entity
#     #modifies attributes of child
#     tuple = (c2, another_list_of_adjusted_child_attributes)
#     list_of_children_tuples.append(tuple)
#
#     return (new_ins, list_of_adjusted_instrument_properties,
#             list_of_children_tuples)
# ---------------------------------------------------------------------"""


def update_old_instrument_hook_template(old_ins, ca):
    list_of_adjusted_instrument_properties = []
    list_of_children_tuples = []
    return (old_ins, list_of_adjusted_instrument_properties,
            list_of_children_tuples)


"""aef-------------------------------------------------------------------------
hook.FBDPHook::update_renamed_instrument_hook

This hook is called from the Corporate Action script. It provides the
possibility to adjust the new derivative instrument. new_ins is the new
renamed instument in which adjustments should be made. Both adjustments made
to the instrument and children to the instrument will be supported by the
rollback functionality.

If Method is Adjust, adjustments made to the instrument will only be supported
in the rollback functionality if a list of changed attribute names are
returned along with the instrument in a tuple.  In the same way, adjustments
made to children of the entity will only be supported in the rollback
functionality if a list of tuples are returned as a third element, along with
the new instrument and the list of changed instrument attributes.  These
tuples must contain a child entity, along with a list of changed attributes if
it is an clone.

If Method is not Adjust, it is suficient to return only the new instrument.
Changes made to children will still be supported in the rollback functionality.

If the new instrument already exists (for example when using the option
Already received from Exchange),
the modifications made in this hook will be ignored, and the existing
instrument will be used.

The hook is activated by renaming the hook function from
**update_renamed_instrument_hook_template** to
**update_renamed_instrument_hook**.

@category BDP.CorporateActions
@param new_ins:object The new renamed instrument
@param ca:object An instance of a subclass to FCATypes.CorpactType
@return object The new instrument or a tuple containing the new instrument,
optionaly a list of modified attribute names and optionally a list of tuples
for adjusted children

@example
def update_renamed_instrument_hook(new_ins, ca):
    '''new_ins is a new instrument (Method is not Adjust)'''
    lst = []
    if new_ins.otc and new_ins.barrier:
            d = ca.__dict__
            q = d['OldQuantity'] / d['NewQuantity']
            new_ins.barrier *= q
            for e in new_ins.exotics():
                e.double_barrier *= q
            for e in new_ins.exotic_events():
                e.value *= q
    return new_ins

def update_renamed_instrument_hook(new_ins, ca):
    '''new_ins is a clone of the old instrument (Method is Adjust)'''
    lst = []
    children_tuples = []
    if new_ins.otc and new_ins.barrier:
            d = ca.__dict__
            q = d['OldQuantity'] / d['NewQuantity']
            new_ins.barrier *= q
            lst.append('barrier')

            for e in new_ins.exotics():
                e.double_barrier *= q
                children_tuples.append((e, ['double_barrier']))

            for e in new_ins.exotic_events():
                e.value *= q
                children_tuples.append((e, ['value']))
    return (new_ins, lst, children_tuples)
----------------------------------------------------------------------------"""


def update_renamed_instrument_hook_template(new_ins, ca):
    lst = []
    return (new_ins, lst)


"""aef-------------------------------------------------------------------------
hook.FBDPHook::update_name_hook

This hook is called from the Corporate Action script. It provides the
possibility to implement custom logic for generating the instrument ID of
derivative instruments that the script creates, and for renaming updated
combinations and equityindices.

Below is an example that uses the suggest name functionality for renaming of
OTC options. 'ca.x' is the instrument for which the instrument name should be
changed.  The hook is activated by renaming the hook function from
**update_name_hook_template** to **update_name_hook**.

@category BDP.CorporateActions
@param ca:object An instance of a subclass to FCATypes.CorpactType

@return str The new instrument id (with max length of ADM instrument
insid field). Return False if the standard naming should be used.
@example
def update_name_hook(ca):
    max_length = getMaxNameLength(acm.FInstrument)
    if ca.x.otc:
        if ca.addModifier:
            modifiers = ('X', 'Y', 'Z')
            old_mod = ''
            if x.insid[-1] in modifiers:
                old_mod = ca.x.insid[-1]
                ca.x.insid = ca.x.insid[:-1] ### Peel off the modifier.
            if not old_mod:
                new_mod = 'X'
            elif old_mod == 'X':
                new_mod = 'Y'
            elif old_mod == 'Y':
                new_mod = 'Z'
            elif old_mod == 'Z':
                new_mod = 'A'
        else:
            new_mod = ''
        if ca.new_insaddr:
            ca.x.und_insaddr=ca.new_insaddr
            s = ca.x.suggest_id() + new_mod
            ca.x.und_insaddr=ca.insaddr
        else:
            s = ca.x.suggest_id() + new_mod
            s = s[:max_length]
        return s
    elif ca.x.instype in ['Combination', 'EquityIndex']:
        s = ca.x.suggest_id()
        return s[:max_length]
    else:
        return False
----------------------------------------------------------------------------"""


def update_name_hook_template(ca):
    """
    Change name to 'update_name_hook' to activate.
    """
    max_length = getMaxNameLength(acm.FInstrument)
    if ca.x.otc:
        s = ca.x.insid + 'OTC'
        return s[:max_length]
    elif ca.x.instype in ['Combination', 'EquityIndex']:
        s = ca.x.suggest_id()
        return s[:max_length]
    else:
        return False  # use standared naming


"""aef-------------------------------------------------------------------------
hook.FBDPHook::rename_old_derivative_hook

This hook is called from the Corporate Action script. It provides the
possibility to implement custom logic for renaming old derivatives.
It must be able to suggest a valid new name for an not yet renamed old
instrument, and it must return the instrument name for a already renamed old
instrument. It is also possible to specify separate new names for external_id1,
external_id2 and for isin, using one of the following return types:

Possible return types:
 new_insid:
    The insid will be renamed to this name. The external_id1, external_id2 and
    isin will also be renamed to this, if to is not to long for those
    attributes, otherwise they will be empty.

 (new_insid):
    The same as last return type.

 (new_insid, ext):
    The insid will be given the new name "new_insid", while external_id1 and
    external_id2 will be given their old names plus the extension "ext".
    Isin will get the same name as insid if possible, else it will be empty.

 (new_insid, new_ext_id1, new_ext_id2):
    The same as last, only external_id1 will get the new name "new_ext_id1" and
    external_id2 will get the new name "new_ext_id2".

 (new_insid, new_ext_id1, new_ext_id2, new_insid):
    The insid, external_id1, external_id2 and isin will now all get the new
    name given in the tuple.

If a name is empty, the script will assume that it will use the old name for
that attribute, with insid as an exception, which instead will get the default
extension '_ca' + date.

The hook is activated by renaming the hook function from
**rename_old_derivative_hook_template** to **rename_old_derivative_hook**.


@category BDP.CorporateActions
@param instr:instrument An old instrument

@return tuple The new instrument id for the old instrument as a first element.
Optionally a tuple with the Return False if the standard
naming (name + "_ca" + date) should be used.
@example
def rename_old_derivative_hook(instr):
    "Logic to add suffix '_An', where n is an integer"
    end = instr.insid[-3:]
    if end[:2] == '_A' and end[-1:] in map(str, range(10)):
        return instr.insid
    name = instr.insid + '_A'
    for i in range(10):
        if not ael.Instrument[name + str(i)]:
            return name + str(i)
    raise FCATypes.SkipPosition("Could not rename old derivative %s through "
            "custom logic.")

----------------------------------------------------------------------------"""


def rename_old_derivative_hook_template(instr):
    return False


"""
************************
*   SCRIP DIVIDEND     *
************************
"""


"""aef-------------------------------------------------------------------------
hook.FBDPHook::modify_scrip_issue_trade

This hook is called from the Scrip Dividend script. It provides a way to modify
the newly created scrip issue trade, before this new trade is committed into
database.

This hook modifies the given scrip issue trade, and does not return.

The hook is activated by renaming the hook function from
**modify_scrip_issue_trade_template** to
**modify_scrip_issue_trade**.

@category BDP.ScripDividend
@param scripIssueTrade:FTrade The newly created, yet-to-be committed FTrade.

----------------------------------------------------------------------------"""


def modify_scrip_issue_trade_template(scripIssueTrade):

    pass


"""aef-------------------------------------------------------------------------
hook.FBDPHook::modify_offset_dividend_cash_payment

This hook is called from the Scrip Dividend script. It provides a way to modify
the newly created offset dividend cash payment, before this new payment is
committed into database.

This hook modifies the given offset dividend cash payment, and does not return.

The hook is activated by renaming the hook function from
**modify_offset_dividend_cash_payment_template** to
**modify_offset_dividend_cash_payment**.

@category BDP.ScripDividend
@param offsetDividendCashPayment:FPayment The newly created, yet-to-be
        committed FPayment.

----------------------------------------------------------------------------"""


def modify_offset_dividend_cash_payment_template(offsetDividendCashPayment):

    pass


"""
*************************
*   EXERCISE ASSIGN     *
*************************
"""


"""aef-------------------------------------------------------------------------
hook.FBDPHook::exercise_assign_selection

This hook is called from the Exercise/Assign BDP procedure, before any
processing has started.  It is used to modify the trade selection made in the
Parameters window.  All Exercise Assign Parameter values are accessible by the
hook.

@category BDP.ExerciseAssign
@param tradeSelection:list A list of trade numbers from the trades selected in
the Exersise Assign Parameters window.
@param guiParameters:dict A dictionary with parameters {parameter: value}
@return list A list of the trade numbers that the script should process
@example
def exercise_assign_selection(tradeSelection, guiParameters):
    for trdnbr in tradeSelection[:]:
        if ael.Trade[trdnbr].text1 == 'someValue':
            tradeSelection.remove(trdnbr)
    return tradeSelection
----------------------------------------------------------------------------"""


def exercise_assign_selection(tradeSelection, guiParameters):
    return tradeSelection


"""aef-------------------------------------------------------------------------
hook.FBDPHook::exercise_mode

This hook is called from both the manual "Exercise Trade" and the script
FExerciseAssign.  It is used to define the default mode used when calculating
the closing trade of the Derivative, and the corresponding opeing trade of the
underlying instrument.

- Strike mode: Close at zero and open at strike. Is represented with value 1.
- Market mode: Close at intrinsic value and open at market value.
    Is represented with value 0.

@param default:int Default value used in calling application.
@category BDP.ExerciseAssign
@return int 1 for "Strike" or 0 for "Market"
@example
def exercise_mode(default):
    return 1 #strike mode always
----------------------------------------------------------------------------"""


def exercise_mode(default):
    return default


"""aef-------------------------------------------------------------------------
hook.FBDPHook::exercise_trade

This hook is, if activated, called as a last step before new trades are
committed to the database.  It is called from both the manual "Exercise Trade"
and the script FExerciseAssign, and is used to modify the exercise trade and
the delivery trade.

The hook will be called once per created trade and derivative instrument,
first for the deliverytrade, if such a trade is created, and secondly for the
excercise trade.

The hook is activated by renaming the hook function from
**exercise_trade_template** to **exercise_trade**.

@category BDP.ExerciseAssign
@param ins:object The derivative instrument that is being
exercised/assigned/abandoned.
@param trade:object Either the closing trade of ins, or the delivery trade of
the underlying instrument.
@return object The modified trade
@example
def exercise_trade_template(ins, trade):
    if not trade.insaddr == ins: # delivery trade
        #modify trade in some way...
    else:                        # exercise trade
        #modify trade in another way...
    return trade
----------------------------------------------------------------------------"""


def exercise_trade_template(ins, trade):
    return trade


"""aef-------------------------------------------------------------------------
hook.FBDPHook::additional_excercise_trades

This hook is, if activated, called as a last step after the ordinary excercise
trade and delivery trade have been created.

The hook will be called once per derivative instrument.

The hook takes as parameters the trades created by the FExerciseAssign script,
and lets the user return a set of new trades that will also be committed
together by the ordinary ones.

The hook is activated by renaming the hook function from
**additional_excercise_trades_template** to **additional_excercise_trades**.

@category BDP.ExerciseAssign
@param exe_trade:object The the closing trade of ins
@param und_trade:object The delivery trade of the underlying instrument.
@param settle_price The settle price
@param ael_variables A dictionary with gui variables
@return object The modified trade
@example
def additional_excercise_trades_template(exe_trade, und_trade, settle_price,
        ael_variables):
    list_of_new_trades = []
    ins = exe_trade.insaddr
    und_ins = und_trade.insaddr
    fx_trade = exe_trade.new() #creates a new clone, similar to fx_trade
    #modify fx_trade
    list_of_new_trades.append(fx_trade)
    return list_of_new_trades

----------------------------------------------------------------------------"""


def additional_excercise_trades_template(exe_trade, und_trade, settle_price,
        ael_variables):
    list_of_new_trades = []
    return list_of_new_trades


"""aef-------------------------------------------------------------------------
hook.FBDPHook::custom_exercise

This hook is, if activated, called instead of the standard exercise routine.

The hook will be called once per grouped position.

The hook takes as parameters the propoerties of the position being processed
by the FExerciseAssign script, the test mode setting and the mode of exercise;
Strike or Market and lets the user implement their own exercise functionality.

The hook is activated by renaming the hook function from
**custom_exercise_template** to **custom_exercise**.

@category BDP.ExerciseAssign
@param attributes:dictionary name value pairs of the attributes of the
position.
@param testMode:bool A bool representing the testmode setting.
@param mode The exercise mode either Strike or Market
@return book True or False. True indicates the position should be processed
by the hook and not by the standard script. False if the position should
be processed by the standard script.

@example
def custom_exercise_template(attributes, testMode, mode):

    try:
        from CustomLifeCycleEvents import customExercise
    except ImportError:
        customExercise = None

    if customExercise:
        return customExercise(attributes, testMode, mode)

    return False

----------------------------------------------------------------------------"""

def custom_exercise_template(attributes, testMode, mode):

    try:
        from CustomLifeCycleEvents import customExercise
    except ImportError:
        customExercise = None

    if customExercise:
        return customExercise(attributes, testMode, mode)

    return False


"""aef-------------------------------------------------------------------------
hook.FBDPHook::trade_status

This hook is, if activated, as a last step in function which creates
new trades.

The hook takes as parameters values which determine the context.
The hook is activated by renaming the hook function from
** trade_status_template** to ** trade_status_status **.

@category BDP.ExerciseAssign
@param tradetype:script actions and trade types for
    closing/ exercise/ assign trade
    ('Exercise', 'Assign', 'Abandon', 'Close').
@param trade:newly created trade which status should be set.
@param isPreview:proprety of caller "preview"
@return string. String represents trade status.

@example
def trade_status(tradetype, trade, exercise):
    if (tradetype == 'Exercise'):
        return 'Void'
    if (tradetype == 'Assign'):
        return 'Void'
    if (tradetype == 'Abandon'):
        return 'Void'
    if (tradetype == 'Close'):
        return 'Simulated' if exercise.preview else 'FO Confirmed'

----------------------------------------------------------------------------"""

def trade_status_template(tradetype, trade, isPreview=False):
    if (tradetype == 'Exercise'):
        return 'Simulated' if isPreview else 'Void'
    if (tradetype == 'Assign'):
        return 'Simulated' if isPreview else 'Void'
    if (tradetype == 'Abandon'):
        return 'Simulated' if isPreview else 'Void'
    if (tradetype == 'Close'):
        return 'Simulated' if isPreview else 'FO Confirmed'


"""
************************
*      EXPIRATION      *
************************
"""

"""aef-------------------------------------------------------------------------
hook.FBDPHook::expiration_selection

This hook is called from the Expiration BDP procedure, before any processing
has started.  It is used to modify the instrument selection made in the
Parameters window.  All Expiration Parameters are accessible by the hook.

@category BDP.Expiration
@param instrumentSelection:list A list of instrument addresses from the
instruments selected in the Expiration Parameters window.
@param guiParameters:dict A dictionary with parameters {parameter: value}
@return list A list of the instrument addresses that the script should process
@example
def expiration_selection(instrumentSelection, guiParameters):
    for insaddr in instrumentSelection[:]:
        if ael.Instrument[insaddr].extern_id1 == 'someValue':
            instrumentSelection.remove(insaddr)
    return instrumentSelection
----------------------------------------------------------------------------"""


def expiration_selection(instrumentSelection, guiParameters):
    return instrumentSelection


"""aef-------------------------------------------------------------------------
hook.FBDPHook::objects_to_be_deleted_or_archived_template

The instruments or trades to be deleted in script FExpiration may be referenced
by other ADM objects. To be able to delete the selected instruments or trades,
these referencing objects must also be deleted.
A user sometimes wants to keep some of these objects and can then define which
object types are acceptable to delete. If an instrument is referenced only by
objects that are allowed to be deleted, then the instrument and the objects can
be deleted. Otherwise, neither instrument nor referencing objects can be
deleted.

By default, objects of the following ADM types are allowed to be deleted when
using the expiration script:
['IntradayPrice', 'ListLeaf', 'MtmValue',  'OrderBook', 'OwnOrder',
'OwnOrderLink', 'PriceDefinition',  'PriceLinkDefinition', 'MatchLot',
'TradeAlias', 'QuoteParameter', 'CombinationLink', 'BusinessEventTrdLink']

The BDP hook objects_to_be_deleted_or_archived can be used to provide a
customised version of this list. The customised list will override the default
list.

If an instrument or trade is referenced by any objects NOT in the list, the
script will not delete the instrument or trade and report the reason.

In the case of archiving an instrument or trade where an object not included in
the list is referencing the instrument or trade, the result is different.
The instrument or trade and the objects defined in the list will still be
archived, but the objects not in the list will be left as is.

Children of instruments and trades, such as 'Leg', 'Cashflow' and 'Reset',
don't need to be specified in the list. They will automatically be archived
or deleted along with the instrument or trades.

An example of object types that users do not want to delete and can be
referencing trades, are 'Settlement', 'JournalInformation', 'Confirmation' and
'OperationsDocument'.
These should then not be included in the list.


@category BDP.Expiration
@return list A list of strings that indicate ADM types.
----------------------------------------------------------------------------"""


def objects_to_be_deleted_or_archived_template():

    return ['IntradayPrice', 'ListLeaf', 'MtmValue',
       'OrderBook', 'OwnOrder', 'OwnOrderLink', 'PriceDefinition',
       'PriceLinkDefinition', 'MatchLot', 'TradeAlias', 'QuoteParameter',
       'CombinationLink', 'BusinessEventTrdLink', 'VolPoint']


"""
************************
*    MARK TO MARKET    *
************************
"""


"""aef-------------------------------------------------------------------------
hook.FBDPHook::mark_to_market_selection

This hook is called from the Mark to Market BDP procedure, before any
processing has started.  It is used to modify the instrument selection made in
the Parameters window.  All Mark to Market Parameters are accessible by the
hook.

@category BDP.MarkToMarket
@param instrumentSelection:list A list of instrument addresses from the
instrument selected in the Mark to Market Parameters window.
@param guiParameters:dict A dictionary with parameters {parameter: value}
@return list A list of the instrument addresses that the script should process
@example
def mark_to_market_selection(instrumentSelection, guiParameters):
    for insaddr in instrumentSelection[:]:
        if ael.Instrument[insaddr].extern_id1 == 'someValue':
            instrumentSelection.remove(insaddr)
    return instrumentSelection
----------------------------------------------------------------------------"""


def mark_to_market_selection(instrumentSelection, guiParameters):
    """
    Both bechmarks and price selection are sent to the hook.
    """
    return instrumentSelection


"""aef-------------------------------------------------------------------------
hook.FBDPHook::calculate_mtm_price

This function allows you to implement your own calculation method for the MtM
price of an instrument. If the function returns a price, this price will become
the MtM price of the concerned instrument. If the function returns 'None',
the MtM price will be calculated by the MtM script. Every instrument handled
by the MtM script will be sent to this function. The hook is activated by
renaming the hook function from **calculate_mtm_price_template** to
**calculate_mtm_price**.

@category BDP.MarkToMarket
@param ins:Instrument The instrument for which an MtM price should be
calculated.
@param mtm_date:ael_date The date for which the MtM price should be calculated
@param curr:Instrument The MtM price should be expressed in this currency
@return float
@example
def calculate_mtm_price(ins, mtm_date, curr):

    if ins.instype == 'Option':
        custom_mtm_price = my_custom_calculation()
        return custom_mtm_price
    else:
        return None #use standard calculation
----------------------------------------------------------------------------"""


def calculate_mtm_price_template(ins, mtm_date, curr):
    if ins.instype == 'Option':
        # return custom calculation
        return None
    else:
        # use standard calculation
        return None


"""aef-------------------------------------------------------------------------
hook.FBDPHook::adjust_mtm_price

This function allows you to make a final adjustment of the calculated MtM
price.  Each price calculated by the script is sent to this function before it
is saved.  Activate the function by renaming it to **adjust_mtm_price**.
Below is an example of how you could use your own rounding, and how to modify
the MtM price for Index Warrants.

@category BDP.MarkToMarket
@param ins:Instrument The instrument for which the MtM price may be adjusted
@param sugg_price:float The suggested MtM price, ready for the final
adjustment.
@return float
@example
def adjust_mtm_price_template(ins, sugg_price):

    #Spread for index warrants.
    spread = 0.1
    if(ins.instype == 'Warrant' and
        ins.und_insaddr.instype == 'EquityIndex'):
        sugg_price = sugg_price - spread

    #Rounding
    force_positive_mtm_price = 1
    if ins.instype == 'Option' and ins.otc:
        if ins.und_insaddr.instype == 'Stock':
            if (ins.curr.insid == 'EUR' or ins.curr.insid == 'USD' or
            ins.curr.insid == 'CHF' or ins.curr.insid == 'JPY'):
                if force_positive_mtm_price == 1:
                    if sugg_price <= 0.0:
                        sugg_price = 0.01
                sugg_price = round(sugg_price, 2)
            elif ins.curr.insid == 'GBP':
                if force_positive_mtm_price == 1:
                    if sugg_price <= 0.0:
                        sugg_price = 0.001
                sugg_price = round(sugg_price, 3)
            else:
                if force_positive_mtm_price == 1:
                    if sugg_price <= 0.0:
                        sugg_price = 0.001
                sugg_price = round(sugg_price, 3)

        elif ins.und_insaddr.instype == 'EquityIndex':
            if (ins.curr.insid == 'EUR' or ins.curr.insid == 'GBP'):
                if force_positive_mtm_price == 1:
                    if sugg_price <= 0.0:
                        sugg_price = 0.1
                sugg_price = round(sugg_price, 1)
            elif ins.curr.insid == 'CHF':
                if force_positive_mtm_price == 1:
                    if sugg_price <= 0.0:
                        sugg_price = 0.1

                        if sugg_price >= 0.1 and sugg_price < 9.90:
                            sugg_price = round(sugg_price, 1)

                        elif sugg_price >= 9.90 and sugg_price < 19.80:
                            sugg_price = sugg_price * 10
                            sugg_price = int(sugg_price)
                            if(float(sugg_price) % 2) != 0:
                                sugg_price = sugg_price + 1
                                sugg_price = float(sugg_price) / 10

                        elif sugg_price >= 19.80 and sugg_price < 299.5:
                            sugg_price_int = int(sugg_price)
                            sugg_price_dec = sugg_price - sugg_price_int
                            if sugg_price_dec >= 0 and sugg_price_dec < 0.25:
                                sugg_price_dec = 0.0
                            elif (sugg_price_dec >= 0.25 and
                                      sugg_price_dec < 0.75):
                                sugg_price_dec = 0.5
                            else:
                                sugg_price_dec = 1.0
                                sugg_price = sugg_price_int + sugg_price_dec

                        elif sugg_price >= 299.5:
                            sugg_price = round(sugg_price)
            else:
                if force_positive_mtm_price == 1:
                    if sugg_price <= 0.0:
                        sugg_price = 0.001
                sugg_price = round(sugg_price, 3)
        else:
            if force_positive_mtm_price == 1:
                if sugg_price <= 0.0:
                    sugg_price = 0.001
            sugg_price = round(sugg_price, 3)
    return sugg_price
----------------------------------------------------------------------------"""


def adjust_mtm_price_template(ins, sugg_price):

    if ins.instype == 'Option' and ins.otc:
        return round(sugg_price, 3)
    else:
        return sugg_price


"""aef-------------------------------------------------------------------------
hook.FBDPHook::tweak_und_lastprice

This hook adjusts the underlying last prices to be the same as the MtM price.
This to ensure that implied volatility will be calculated using MtM prices and
not by default **used_price()**. Activate the hook by renaming it from
**tweak_und_lastprice_template** to **tweak_und_lastprice**.

NOTE
* The underlying mtm prices have already been calculated.
* The price finding rules used for the underlying must be latest.

@category BDP.MarkToMarket
@param instrumentPriceSelection:list A list of (instrument_address, mtm_price)
tuples
@return None
@visibility private
----------------------------------------------------------------------------"""


def tweak_und_lastprice_template(instrumentPriceSelection):

    from FBDPCommon import eps_compare

    # Name on the Market were tweak prices are stored
    InitMarketName = 'MTM-Tweak'

    def get_tweak_market():
        " Creates if missing "
        market = ael.Party[InitMarketName]
        if not market:
            market = ael.Party.new()
            market.ptyid = InitMarketName
            market.type = 'Market'
            market.commit()
            Logme()("Created market %s of type %s" % (InitMarketName,
                    'Market'), 'INFO')
        return market

    def commit_transaction():
        try:
            ael.commit_transaction()
        except Exception as ex:
            ael.abort_transaction()
            Logme()('Failed tweaking prices. %s' % str(ex), 'WARNING')

    def get_used_price(insaddr, calcSpaceColl):
        acm_ins = acm.FInstrument[insaddr]
        used_value = acm_ins.Calculation().MarketPrice(calcSpaceColl).Value()
        return used_value.Number()

    def tweak(instrumentPriceSelection):
        day = ael.date_today()
        tweak_market = get_tweak_market()
        calcSpaceColl = (acm.Calculations().
                CreateStandardCalculationsSpaceCollection())
        n_ins = 0
        n = 0
        n_del = 0
        batch_size = 10
        tweaked_ins = []
        ael.begin_transaction()
        for und_address, mtm_price in instrumentPriceSelection:
            und = ael.Instrument[und_address]
            if not und.mtm_from_feed:
                continue
            used_price = get_used_price(und_address, calcSpaceColl)
            if eps_compare(used_price, mtm_price):
                continue
            n_ins = n_ins + 1
            price = None
            for p in und.prices():
                if p.ptynbr == tweak_market:
                    price = p
            save_price = True
            if price and price.day == day:
                save_price = False
                for p in [price.last, price.settle, price.bid, price.ask]:
                    if not eps_compare(p, mtm_price):
                        save_price = True
                        break
            if save_price:
                n += 1
                tweaked_ins.append((und, mtm_price))
                Logme()("Tweaking mtm_suggest_price for %s :: old(%.2lf) "
                        "new(%.2lf)" % (und.insid, used_price, mtm_price))
                for p in und.prices():
                    if p.ptynbr == tweak_market:
                        price = p
                        break
                if price:
                    price = price.clone()
                else:
                    price = ael.Price.new()
                    price.curr = und.curr
                    price.ptynbr = tweak_market
                    price.insaddr = und
                price.day = day
                price.last = mtm_price
                price.settle = mtm_price
                price.bid = mtm_price
                price.ask = mtm_price
                price.commit()
            else:
                for p in und.prices():
                    if p.ptynbr == tweak_market and p.day != day:
                        p.delete()
                        n_del = n_del + 1
                        break
            if n_ins % batch_size == 0:
                commit_transaction()
                ael.begin_transaction()
        commit_transaction()
        if n > 0:
            n_err = 0
            ael.poll()
            Logme()("Tweaked %d instruments of total of %d" % (n, n_ins))
            for ins, mtm_price in tweaked_ins:
                market_price = get_used_price(ins.insaddr, calcSpaceColl)
                if not eps_compare(mtm_price, market_price):
                    Logme()("Tweaking failed for %s(%s,%s) mtm(%.2lf) "
                            "used_price(%.2lf)" % (ins.insid, ins.instype,
                            ins.curr.insid, mtm_price, market_price),
                            'WARNING')
                    for p in ins.prices():
                        if p.insaddr and p.ptynbr:
                            Logme()("Ins(%s) Day(%s) Market(%s) Last(%.2lf) "
                                    "Settle(%.2lf)" % (p.insaddr.insid,
                                    p.day, p.ptynbr.ptyid, p.last, p.settle))
                        else:
                            Logme()("Ins(%s) Day(%s) Market(%s) Last(%.2lf) "
                                    "Settle(%.2lf)" % (p.insaddr.insid, p.day,
                                    p.ptynbr.ptyid, p.last, p.settle))
                    print(70 * '-')
                    n_err = n_err + 1
            if n_err == 0:
                Logme()("Tweaking worked OK.")
            else:
                Logme()("Tweaking FAILED with %d errors of total %d tweaked "
                        "instruments" % (n_err, n))
        if n_del > 0:
            Logme()("Dropped %d tweaked prices" % (n_del))

    Logme()('Start tweaking underlying prices...', 'START')
    tweak(instrumentPriceSelection)
    Logme()('Ended tweaking of prices', 'FINISH')


"""
***********************
*    DELETE PRICES    *
***********************
"""


"""aef-------------------------------------------------------------------------
hook.FBDPHook::get_delete_prices_transaction_size

This hook is called from the Delete Prices BDP procedure and is used for
optimizing the performance of deleting the prices.

The hook is used to set the delete price transaction size, that is, the amount
of prices that are deleted in one database transaction.

A larger transaction size results in fewer transactions, but for each
transaction the parsing and processing time increases. On the other hand, the
processing time for a smaller transaction size is efficient, but the larger
number of transactions increases the time consumed for communication between
system components.

The optimal transaction size is dependent upon network topology and server
efficiency, and is somewhere in between a large and a small transaction size.

The default value is 250.


@category BDP.FBDPHook
@return A integer value for price transaction size.

DELETE_PRICES_TRANSACTION_SIZE = 250
----------------------------------------------------------------------------"""


def get_delete_prices_transaction_size_template():

    return 250


"""aef-------------------------------------------------------------------------
hook.FBDPHook::get_delete_prices_instrument_batch_size

This hook is called from the Delete Prices BDP procedure and is used for
optimizing the performance of deleting prices when saving them to file.

The hook is used to set the batch size for instruments, that is, the number of
instruments processed at one time.

Prices on the same date are saved to the same file. The idea is to collect
as many prices as possible from the same date in order to minimise the number
of file operations. On the other hand, the number of prices cannot be too
large since the cost of reading a large amount of prices from the database
at one time, for saving them to file, also impacts performance.

A larger instrument batch size also ensures there is enough number of prices to
keep the delete_price_transactions_size reasonably utilised.

The default value is 100.


@category BDP.FBDPHook
@return A integer value for instrument batch size.

DELETE_PRICES_INSTRUMENT_BATCH_SIZE = 100
----------------------------------------------------------------------------"""


def get_delete_prices_instrument_batch_size_template():

    return 100


"""
************************
*         FIXING       *
************************
"""


"""aef-------------------------------------------------------------------------
hook.FBDPHook::calculate_fixing

This hook is called from the Fixing script. If a value is returned, this value
will become the fixing for the reset. Rename the function to 'calculate_fixing'
to activate it.

@category BDP.MarkToMarket
@param reset:Reset
@param rateSpecification:int This parameter is used to differentiate between
float reference 1 and float reference 2 on a reset. If rateSpecification is
equal to 1 return the fixing for float reference 1. If rateSpecification is
equal to 2 return the fixing for float reference 2. The default value for
rateSpecification if no value is provided is 1.
----------------------------------------------------------------------------"""


def calculate_fixing_template(reset, rateSpecification=1):
    return None


"""
************************
*         FX           *
************************
"""


"""aef-------------------------------------------------------------------------
hook.FBDPHook::adjust_fx_ftrade

This hook is called from the FX scripts: .
Rename the function to 'adjust_fx_ftrade' to activate it.

@category BDP.FX
@param fTrade:acm.FTrade

@return None
----------------------------------------------------------------------------"""


def adjust_fx_ftrade_template(fTrade, scriptName):
    fTrade.Text1('Adjusted by hook')


"""aef-------------------------------------------------------------------------
hook.FBDPHook::pos_move_split_filter_selection

This hook is called from the FFXPositionDecompDialog script: .
Rename the function to 'pos_move_split_filter_selection' to activate it.

@category BDP.FFXPositionDecompDialog
@param sel:list

@return list
----------------------------------------------------------------------------"""


def pos_move_split_filter_selection_template(sel):
    if sel:
        if sel[0].IsKindOf(acm.FPhysicalPortfolio):
            filteredSelection = []
            for obj in sel:
                if obj.CurrencyPair():
                    filteredSelection.append(obj)
            return filteredSelection
        elif sel[0].IsKindOf(acm.FInternalDepartment):
            filteredSelection = []
            for obj in sel:
                if str(obj.Name()).endswith('_DEAL'):
                    filteredSelection.append(obj)
            return filteredSelection
    return sel


"""aef-------------------------------------------------------------------------
hook.FBDPHook::fx_aggregation_exclude_trade_template

This hook is called from FX Aggregation .
Rename the function to 'fx_aggregation_exclude_trade' to activate it.

@category BDP.FX
@param acmTrade:acm.FTrade

@return False to include the trade in the aggregate.
----------------------------------------------------------------------------"""


def fx_aggregation_exclude_trade_template(acmTrade):
    return False


"""aef-------------------------------------------------------------------------
hook.FBDPHook::get_grouping_attribute_from_grouper_template

This hook is called from FX Common. It allows users to map the customer grouper
name to a system attribute name. Each grouper in the grouper chain is sent
to this hook to be mapped to the system attibute name. The hook enable BDP FX
scripts to understand what the grouping criteria of the customer grouper.
Rename the function to 'get_grouping_attribute_from_grouper' to activate it.

@category BDP.FX
@param grouperName:String

@return system attribute name which corresponds to the customer grouper
name. Return None if no mapping for the given grouper name.
----------------------------------------------------------------------------"""


def get_grouping_attribute_from_grouper_template(grouperName):
    return 'Currency Pair' if grouperName == 'Trade.FPLSweepGrouper' else None


"""aef-------------------------------------------------------------------------
hook.FBDPHook::get_instrument_selection_template

This hook is called from FBDPInstSelectionDialog. The archived instruments are
not visiable from the acm. This hook allows users to select the instrument
directly from the db query.

The user could write the query like the one in the following example. and put
it into a dictionary. The user defined function expects to return the result
of the db query or [[]]

def MyGetUnTradedInstruments():
    query = 'select instrument.insid FROM instrument \
WHERE NOT EXISTS(SELECT 1 FROM trade where trade.insaddr=instrument.insaddr)'
    return ael.dbsql(query)

@return The dictionary holds the user defined db query functions and their
associated names.
----------------------------------------------------------------------------"""


def MyGetUnTradedInstruments():
    query = 'select instrument.insid FROM instrument \
WHERE exp_day != NULL and NOT EXISTS(SELECT 1 FROM trade \
where trade.insaddr=instrument.insaddr)'
    return ael.dbsql(query)


def get_instrument_selection_template():
    inst_selection_dic = {}
    inst_selection_dic['user defined Untraded Instruments'] = \
        MyGetUnTradedInstruments

    return inst_selection_dic

"""aef-------------------------------------------------------------------------
hook.FBDPHook::exotic_fixings

This hook is called from the FSEQDataMaint if ExoticFixingsHook attributes
in the FCustomInstrumentDefinition entries are set to
'FBDPHook.exotic_fixings'.
It is to return the exotic events types of the given instrument, which need
to be updated by using Mark-to-Market prices.

Rename the function to 'exotic_fixings' and set 'ExoticFixingsHook'
attribute in FCustomInstrumentDefinition to
'FBDPHook.exotic_fixings' to activate it.

@category BDP.MarkToMarket
@param instrument:A instrument whose exotic events need updates.
@param dateToday:date.
@param updateHistorical:int Update historical event or not
@param updateResult
----------------------------------------------------------------------------"""

def exotic_fixings_template(instrument, dateToday, updateHistorical,
                            updateResult):
    return ['Price Fixing']


def update_corporate_action_diary_template(old_ca, new_ca, op):
    print(old_ca, new_ca, op)
    if op == 'Insert':
        print('BDP hook insert state')
        return 1

    import FBDPCommon
    import FCorpActionStatesSetup
    FCorpActionStatesSetup.CreateCorporateActionStateChart()
    ca = FBDPCommon.ael_to_acm(old_ca)

    if op == 'Update':
        print('BDP hook update state')
        fromStatus = FCorpActionStatesSetup.ConvertStatus(old_ca.status)
        toStatus = FCorpActionStatesSetup.ConvertStatus(new_ca.status)
        if fromStatus != toStatus:
            if ca.UpdateSource() == 0:
                param = {'NoUpdateCA': 1}
                FCorpActionStatesSetup.UpdateBusinessProcess(
                                            'CorporateActionStateChart',
                                            ca,
                                            fromStatus,
                                            toStatus,
                                            param)
    elif op == 'Delete':
        print('BDP hook delete state')
        toStatus = 'Removed'
        import FBusinessProcessUtils
        bp = FBusinessProcessUtils.GetOrCreateBusinessProcess(ca,
                                'CorporateActionStateChart')
        bp.ForceToState(toStatus)

    return 1


"""aef-------------------------------------------------------------------------
hook.FBDPHook::should_process_instrument

This hook is called from the FCorpActionElectionHandler.
It is to return true if the instrument should be processed
or false if the instrument should be skipped.

Rename the function to 'should_process_instrument'.

@category BDP.AdvancedCorporateActions
@param caPosition:The FCorporateActionElection of the position.
----------------------------------------------------------------------------"""
def should_process_instrument_template(caPosition):
    ins = caPosition.Instrument()
    if not ins:
        return 1
    for leg in ins.Legs():
        if leg.NominalScaling() == 'Initial Price':
            msg = 'Fixed loan processed. Please check' \
                ' instrument \'{0}\' and update with correct details.'. \
                    format(ins.Name())
            Logme()(msg, 'WARNING')
            break
    return 1

#"""aef-------------------------------------------------------------------------
# hook.FBDPHook::GetPriceForExoticFixings
#
# This hook is called from FSEQDataMaint.
# It returns the MtM Price for a particular fixing source.
#
# To enable the hook, rename the function to 'GetPriceForExoticFixings'
#
# @category BDP.MarkToMarket
# @param exotic event: The exotic event which will be fixed.
# @param currency: The currency in which the fixing price is denominated.
# If a valid price exists in different currencies, only the price in the currency
# matching the parameter should be returned.
#----------------------------------------------------------------------------"""
def GetPriceForExoticFixings_template(exoticEvent, currency=None):
    return 100.0, False


#************************
#         FRTB          *
#************************

#"""aef-------------------------------------------------------------------------
# hook.FBDPHook::RiskFactorNameHandler
#
# This hook is called from FRTBSASBAExport.
# It returns the risk factor name acceptable for Adaptiv Analytics.
#
# To enable the hook, rename the function to 'RiskFactorNameHandler'
#
# @category BDP.FRTBExport
# @param riskClass: the risk class of the risk factor
# @param rfNames: the list of risk factor names
# @param rfValues: risk factor values
#
# The code in the hook is just an example and it depends on paricular
# naming issue related to risk factor names.
#----------------------------------------------------------------------------"""
def RiskFactorNameHandler_template(riskClass, rfNames, rfValues):
    nameIndex = rfNames.index('Name')
    rfName = rfValues[nameIndex]
    rfNamesMapping = {'AUDZAR': 'AUD/ZAR',
                        'EURZAR': 'EUR/ZAR',
                        'GBPZAR': 'GBP/ZAR',
                        'USDZAR': 'USD/ZAR',
                        'ZARJPY': 'ZAR/JPY'
                    }
    if rfName in rfNamesMapping:
        return rfNamesMapping[rfName]
    if riskClass == 'FX':
        if 'Volatility' not in rfNames:
            termCurrencyIndex = rfNames.index('TermCurrency')
            rfName += '/' + rfValues[termCurrencyIndex]
    return rfName
