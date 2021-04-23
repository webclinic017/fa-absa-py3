"""----------------------------------------------------------------------------
MODULE
    CCG_Move_Trades

DESCRIPTION
    Date                : 18/05/2015
    Purpose             : Business data maintenance.
    Requester           : Karen Charmain Griffin.
    Developer           : Dmitry Kovalenko

NOTES
    Changes counterparties on trades and issuers on instruments based on CSV
    input with the line format being "FROM_PARTY,TO_PARTY".

----------------------------------------------------------------------------"""

from collections import defaultdict
from datetime import datetime
from itertools import repeat

import acm

from at_ael_variables import AelVariableHandler


DELIMITER = ","


def log(msg):
    print(datetime.now().isoformat() + ': ' + msg)


def read_file(filename):
    try:
        with open(filename) as fd:
            return fd.readlines()
    except IOError as e:
        log("IOError: {0}".format(str(e)))
        raise RuntimeError(str(e))


def get_party(party_name):
    """Return an acm.FParty object or throw."""

    party = acm.FParty[party_name]
    if not party:
        raise RuntimeError("Party '{0}' does not exist.".format(party_name))
    return party


def record_to_party_link(record):
    return (get_party(record[0]), get_party(record[1]))


def extract_party_link(line, line_number=None):
    """Attempts to convert string to (Party, Party) tuple."""

    record = line.rstrip().split(DELIMITER)
    if len(record) < 2:
        return None
    try:
        party_link = record_to_party_link(record)
        log("Extracted party pair '{0}' -> {1}".format(party_link[0].Name(),
                                                       party_link[1].Name()))
    except Exception as e:
        # If a line can't be converted to a party link we ignore it.
        if line_number:
            log("Line {0} cannot be parsed.\n{1}".format(line_number, str(e)))
        return None
    return party_link


def parse_data(data):
    """Convert raw data to structured business object references."""

    party_links = []
    for i, line in enumerate(data):
        # Lines numbers are 0 based list indices, therefore, adding 1.
        if i > 0:
            party_link = extract_party_link(line, i + 1)
            if party_link:
                party_links.append(party_link)
    return party_links


def get_instruments_with_party_as_issuer(party):
    return list(acm.FInstrument.Select("issuer = {0}".format(party.Name())))


def get_trades_with_party_as_cp(party):
    return list(acm.FTrade.Select("counterparty = {0}".format(party.Name())))


def change_counterparty(trade, to_party):
    """Changes and attempts to commit the counterparty on the trade."""

    from_party = trade.Counterparty()
    acm.BeginTransaction()
    trade.Counterparty(to_party)
    try:
        trade.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        log("ERROR: Unable to change CPTY of trade {0} from '{1} '"
            "to {2}.\n{3}".format(trade.Oid(),
                                  from_party.Name(),
                                  to_party.Name(),
                                  str(e)))


def change_issuer(instrument, to_party):
    """Changes and attempts to commit the issuer field on the instrument."""

    # Store original issuer for logging purposes.
    from_party = instrument.Issuer()

    acm.BeginTransaction()
    instrument.Issuer(to_party)

    try:
        instrument.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        log("ERROR: Unable to change ISSUER of instrument {0} from '{1} '"
            "to {2}.\n{3}".format(instrument.Oid(),
                                  from_party.Name(),
                                  to_party.Name(),
                                  str(e)))


def execute_move(party_link, dry_run=False):
    """Performs the party change on appropriate insturments."""

    from_party = party_link[0]
    to_party = party_link[1]

    # Retrieve business objects that will be affected.
    log("Retrieving instruments with issuer set to "
        "'{0}'.".format(party_link[0].Name()))
    instruments = get_instruments_with_party_as_issuer(from_party)
    log("Retrieving trades with counterparty set to "
        "{0}.'".format(party_link[0].Name()))
    trades = get_trades_with_party_as_cp(from_party)

    log("Modification of party {0} will involve:".format(party_link[0].Name()))
    log("- changes to {0} instruments.".format(len(instruments)))
    log("- changes to {0} trades.".format(len(trades)))

    if dry_run:
        return

    # Apply modification functions to the business objects.
    log("Applying modification for party '{0}'".format(party_link[0].Name()))
    log("Moving issuers.".format(len(instruments)))
    map(change_issuer, instruments, repeat(to_party, len(instruments)))
    log("Moving counterparties.".format(len(trades)))
    map(change_counterparty, trades, repeat(to_party, len(trades)))


def link_info(link):
    """Retrieve trade count on both parties in the link."""

    # FromParty trade count
    fptc = len(acm.FTrade.Select("counterparty = '{0}'".format(link[0].Id())))
    # ToPart trade count
    tptc = len(acm.FTrade.Select("counterparty = '{0}'".format(link[1].Id())))

    return (link, fptc, tptc)


def log_statistics(pre, post):
    """Output information about pre- and postmove trade counts on parties."""

    results = defaultdict(dict)

    # Convert tuple lists to a dictionary.
    for stat in pre:
        results[stat[0]]['pre'] = stat[1:]
    for stat in post:
        results[stat[0]]['post'] = stat[1:]

    log("Run statistics.")
    log("---------------")

    template = "'{0}' trade count change {1} -> {2} d = {3}"
    for l, counts in results.iteritems():
        from_pre = counts['pre'][0]
        from_post = counts['post'][0]
        to_pre = counts['pre'][1]
        to_post = counts['post'][1]
        from_delta = from_post - from_pre
        to_delta = to_post - to_pre
        log(template.format(l[0].Id(), from_pre, from_post, from_delta))
        log(template.format(l[1].Id(), to_pre, to_post, to_delta))
        log('---')


ael_variables = AelVariableHandler()
ael_variables.add(
    "filename",
    label="File path:",
    default="",
    mandatory=True,
    alt="Path to the file which contains information about parties.")
ael_variables.add_bool('dry_run',
                       label='Dry run',
                       default=True)


def ael_main(args):
    log("Launching...")
    filename = args["filename"]
    dry_run = args['dry_run']
    log("Input file path - {0}".format(filename))
    log("Retrieving data...")
    try:
        links = parse_data(read_file(filename))
        pre_move_trade_count = map(link_info, links)
        log("Executing move...")
        map(execute_move, links, repeat(dry_run, len(links)))
        post_move_trade_count = map(link_info, links)
        log_statistics(pre_move_trade_count, post_move_trade_count)
        log("Run complete.")
    except RuntimeError as e:
        log('FATAL: {0}'.format(str(e)))
        log("Run terminated unsuccessfully.")
