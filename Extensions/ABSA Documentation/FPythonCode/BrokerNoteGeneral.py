"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteGeneral

DESCRIPTION
    This module contains general functionality related to broker notes.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-02-10      FAOPS-725       Cuen Edwards            Kgomotso Gumbo          Refactored out functionality from other modules.
2020-05-22      FAOPS-739       Ntokozo Skosana         Nqubeko Zondi           Added function that checks if combination trade
                                                                                broker note should be generated.
-----------------------------------------------------------------------------------------------------------------------------------------
"""


def get_broker_note_event_name():
    """
    Get the name of the event to associate with broker note
    confirmations.
    """
    return 'Broker Note'


def get_broker_note_template_name():
    """
    Get the name of the template to associate with broker note
    confirmations.
    """
    return 'ABSA_Broker_Note'


def is_broker_note_trade(trade):
    """
    Determine whether or not a trade is a supported trade for broker
    note generation purposes.
    """
    instrument = trade.Instrument()
    if instrument.InsType() not in ['Bond', 'BuySellback', 'FRN', 'IndexLinkedBond', 'Repo/Reverse']:
        return False
    if instrument.AdditionalInfo().Demat_Instrument():
        return False
    if _is_zau_instrument(instrument):
        if not trade.SettleCategoryChlItem():
            return False
    if trade.AddInfoValue('Approx. load'):
        return False
    if trade.TradeCategory() == 'Collateral':
        return False
    if trade.OptKey1AsEnum() == 'Block Trade':
        return False
    if trade.Status() not in ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed']:
        return False
    return True


def is_broker_note_combination_trade(trade):

    if trade.Instrument().InsType() != 'Combination':
        return False
    if trade.Instrument().Isin() is None:
        return False
    if trade.Status() not in ['FO Confirmed', 'BO Confirmed']:
        return False
    settle_category = _is_sa_custodian_settle_category(trade)
    if not settle_category:
        return False
    if not _is_zag_instrument(trade.Instrument()):
        return False
    return True


def get_broker_note_status(trade):
    """
    Get the broker note status for a trade.
    """
    broker_notes = _get_broker_note_confirmations(trade)
    if len(broker_notes) == 0:
        return ''
    broker_notes.sort(key=lambda broker_note: broker_note.CreateTime())
    last_broker_note = broker_notes[-1]
    broker_note_status = 'Broker Note Status: {status}'.format(status=last_broker_note.Status())
    if len(broker_notes) > 1:
        return 'Latest ' + broker_note_status
    return broker_note_status


def _is_zau_instrument(instrument):
    """
    Determine whether or not an instrument has an ISIN starting with
    ZAU.
    """
    isin = _get_instrument_isin(instrument)
    if isin is None:
        return False
    if len(isin) != 12:
        # Valid ISINs should have 12 characters
        return False
    return isin.startswith('ZAU')


def _is_zag_instrument(instrument):
    isin = instrument.Isin()
    return isin.startswith('ZAG')


def _is_sa_custodian_settle_category(trade):
    """
    Check if settle category is blank or SA_CUSTODIAN.
    """
    if trade.SettleCategoryChlItem() is None:
        return True
    if trade.SettleCategoryChlItem().Name() == 'SA_CUSTODIAN':
        return True
    return False


def _get_instrument_isin(instrument):
    """
    Gets the ISIN related to a specified instrument.
    """
    if instrument.Underlying() is not None:
        return instrument.Underlying().Isin()
    return instrument.Isin()


def _get_broker_note_confirmations(trade):
    """
    Get the broker note confirmations for the specified trade.
    """
    broker_notes = list()
    for confirmation in trade.Confirmations():
        if confirmation.EventChlItem() is None:
            continue
        if confirmation.EventChlItem().Name() == get_broker_note_event_name():
            broker_notes.append(confirmation)
    return broker_notes
