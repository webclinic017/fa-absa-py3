import acm

from AMWICommon import log_debug, AMWI_STATUS_FO_CONFIRMED, AMWI_STATUS_VOID, AMWI_STATUS_TERMINATED


def get_message_status(trade):
    return trade.AdditionalInfo().CCPmwire_message_st()


def set_message_status(trade, new_status):
    if get_message_status(trade) != new_status:
        log_debug("Setting message status on %i to %s" % (trade.Oid(), new_status))
        trade.AdditionalInfo().CCPmwire_message_st(new_status)
        trade.Commit()


def is_trade_released(trade):
    if get_message_status(trade) == "Released":
        return True

    return False


def is_trade_portfolio_allocate(trade):
    portfolio = trade.Portfolio()
    if portfolio:
        portfolio_name = portfolio.Name()
        if portfolio_name.lower().startswith("allocate"):
            log_debug("Trade is in an Allocate portfolio: %s" % portfolio_name)
            return True

    return False


def is_allocate_trade(trade):
    if is_trade_portfolio_allocate(trade):
        return True

    mirror = trade.MirrorTrade()
    if mirror and is_trade_portfolio_allocate(mirror):
        return True

    return False


def _find_mirrors_for_version(mirror_trades, mw_id, mw_version):
    r = []
    for mw_related_trade in mirror_trades:
        if not mw_related_trade.MirrorTrade():
            if mw_related_trade.AdditionalInfo().CCPmiddleware_id() == mw_id:
                trade_version = get_markitwire_major_version(mw_related_trade)
                if trade_version == mw_version:
                    r.append(mw_related_trade)

    return r


def _do_mirror(t1, t2, original_trade):
    log_debug("Creating mirror: %i <-> %i" % (t1.Oid(), t2.Oid()))

    original_oid = original_trade.ConnectedTrdnbr()

    if original_oid in (t1.Oid(), t2.Oid()):
        # Force status,
        t1.Status(original_trade.Status())
        t2.Status(original_trade.Status())

    t2.Instrument(t1.Instrument())
    t2.MirrorTrade(t1)
    t1.MirrorTrade(t1)

    # We always have to commit the secondary trade, otherwise the primary trade
    # won't commit because the mirror is missing.
    t2.Commit()
    if t1.Oid() != original_oid:
        t1.Commit()


def _update_mirror(trade, mirror_trades, original_trade):
    mirrors = _find_mirrors_for_version(mirror_trades,
                                        trade.AdditionalInfo().CCPmiddleware_id(),
                                        get_markitwire_major_version(trade))

    is_allocate = False
    mirror = None
    for t in mirrors:
        if not is_trade_released(t):
            log_debug("Not creating mirror for %i. Trade %i is not released yet." % (trade.Oid(), t.Oid()))
            return False

        if is_allocate_trade(t):
            is_allocate = True

        if not mirror or t.Oid() < mirror.Oid():
            mirror = t

    # Original trade is used to set the status. We can't link a trade in
    # the allocate portfolio if the status > FO Confirmed.
    if is_allocate and original_trade.Status() not in (AMWI_STATUS_VOID, AMWI_STATUS_TERMINATED):
        original_trade.Status(AMWI_STATUS_FO_CONFIRMED)

    if mirror and len(mirrors) > 1:
        for t in mirrors:
            if not t.MirrorTrade():
                if t.Oid() != mirror.Oid():
                    _do_mirror(mirror, t, original_trade)

    return True


def get_markitwire_major_version(trade):
    version = trade.AdditionalInfo().CCPmiddleware_versi()
    if version and len(version) > 2:
        versions = version[1:-1].split("\\")
        return versions[0]

    return None


def find_trades_by_markitwire_id(mw_id, ignore_trade_ids, match_version=None):
    r = []
    ais = acm.FAdditionalInfoSpec["CCPmiddleware_id"]
    query = 'addInf=%i and fieldValue="%s"' % (ais.Oid(), str(mw_id))
    for ai in acm.FAdditionalInfo.Select(query):
        trade = acm.FTrade[ai.Recaddr()]
        if not ignore_trade_ids or trade.Oid() not in ignore_trade_ids:
            if match_version:
                trade_version = get_markitwire_major_version(trade)
                if trade_version == match_version:
                    r.append(trade)
            else:
                r.append(trade)

    return r


def update_all_mirrors(original_trade):
    # This is called even if the current trade is not a mirror,
    # as there may be previous versions that have mirrors.
    markitwire_id = original_trade.AdditionalInfo().CCPmiddleware_id()

    all_trades = []
    for trade in find_trades_by_markitwire_id(markitwire_id, None):
        all_trades.append(trade)
    for trade in find_trades_by_markitwire_id("%s_closing" % markitwire_id, None):
        all_trades.append(trade)

    mirror_trades = []
    for trade in all_trades:
        if trade.Counterparty() and trade.Counterparty().Type() == "Intern Dept":
            mirror_trades.append(trade)

    for trade in mirror_trades:
        if not trade.MirrorTrade():
            _update_mirror(trade, mirror_trades, original_trade)


def remove_mirrors(markitwire_id, major_version):
    trades = find_trades_by_markitwire_id(markitwire_id, None, str(major_version))
    for trade in [t for t in trades]:
        if trade.MirrorTrade():
            log_debug("Removing mirror from trade: %i" % trade.Oid())
            trade.MirrorTrade(None)
            trade.Commit()

    if major_version > 1:
        remove_mirrors(markitwire_id, major_version - 1)
