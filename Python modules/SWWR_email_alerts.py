import acm
from at_logging import getLogger
from at_email import EmailHelper
from at_time import to_timestamp
from at_ael_variables import AelVariableHandler

ael_variables = AelVariableHandler()

LOGGER = getLogger()
TODAY = acm.Time().DateToday()
SUBJECT = 'Specific Wrong Way Risk Alert'
BREACH_STATUS = 'SWWR Detected'

EMAIL_TABLE_COLUMNS = ["Trade Number", "Product Type", "Client Name", "Client SDS ID",
                       "Issuer Name", "Relationship", "Status"]

TIMES = ['07:00:00', '10:00:00', '13:00:00', '16:00:00', '19:00:00']

ael_variables.add('start_time',
                  label='Start Time',
                  collection=TIMES,
                  alt=('start of execution time from which SWWR trades should '
                       'be reported.'))
ael_variables.add('end_time',
                  label='End Time',
                  collection=TIMES,
                  alt=('end of execution time from which SWWR trades should '
                       'be reported.'))

ael_variables.add('out_email',
                  label='Output Email',
                  default=['John.Greene@absa.africa', 'DCEMJHBStructuredTradeRisking@Absacapital.com'],
                  multiple=True)


def select_trade_population():
    query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    query.AddAttrNode('TradeTime', 'GREATER_EQUAL', TODAY)
    query.AddAttrNode('TradeTime', 'LESS_EQUAL', TODAY)
    query.AddAttrNodeString('Status', ['FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'], 'EQUAL')
    query.AddAttrNode('Instrument.InsType', 'NOT_EQUAL', 'SecurityLoan')
    op = query.AddOpNode('OR')
    op.AddAttrNode('Instrument.UnderlyingType', 'EQUAL', 'Stock')
    op.AddAttrNode('Instrument.Legs.IndexRef.InsType', 'EQUAL', 'Stock')
    op.AddAttrNode('Instrument.Legs.IndexRef.InsType', 'EQUAL', 'Bond')
    swwr_trades = query.Select()
    return swwr_trades


def get_issuer(trade):
    issuer_id = None
    if trade.Instrument().UnderlyingType() == 'Stock':
        if trade.Instrument().Underlying().Issuer():
            issuer_id = trade.Instrument().Underlying().Issuer().Oid()
    else:
        for leg in trade.Instrument().Legs():
            index_ref = leg.IndexRef()
            if index_ref and index_ref.InsType() in ('Stock', 'Bond') and index_ref.Issuer():
                issuer_id = index_ref.Issuer().Oid()
    return issuer_id


def in_breach_check(trade):
    # issuer details
    relationship = None
    issuer_id = get_issuer(trade)
    if issuer_id:
        # counterparty details
        party_id = trade.Counterparty()
        party_parent_id = party_id.AdditionalInfo().Parent_ID()
        party_group_parent_id = party_id.AdditionalInfo().Group_Parent_ID()
        if str(issuer_id) == str(party_id):
            # direct relationship between counterparty and issuer
            relationship = 'ISSUER = COUNTERPARTY'
        elif str(party_parent_id) == str(issuer_id):
            # direct relationship between counterparty and issuer
            relationship = 'PARENT'
        elif str(party_group_parent_id) == str(issuer_id):
            # indirect relationship between counterparty and issuer
            relationship = 'GROUP PARENT'
        return relationship


def construct_body(trade_list):
    msg = """
    <br /><br />
    <table width="1800" border="1">
    <tr>{column_titles}</tr>
    <tr>{rows}</tr>
    </table>
    <br /><br />
    """
    rows = [(trade.Oid(),
             trade.Instrument().InsType(),
             trade.Counterparty().Name(),
             acm.FParty[trade.Counterparty().Oid()].AdditionalInfo().BarCap_Eagle_SDSID(),
             acm.FParty[get_issuer(trade)].Name(),
             in_breach_check(trade),
             BREACH_STATUS) for trade in trade_list]
    return msg.format(
        column_titles="".join(map("<td><b>{}</b></td>".format, EMAIL_TABLE_COLUMNS)),
        rows="</tr><tr>".join("".join(map("<td>{0}</td>".format, row)) for row in rows)
    )


def booking_time_passage(trade, start, end):
    threshold = to_timestamp(end) - to_timestamp(start)
    time_passage = to_timestamp(acm.Time.TimeNow()) - to_timestamp(trade.TradeTime())
    return time_passage <= threshold


def send_report(body, recipients):
    # Email sender
    environment = acm.FDhDatabase['ADM'].InstanceName()
    subject = "{0} {1} ({2})".format(SUBJECT, acm.Time.DateToday(), environment)
    email_helper = EmailHelper(
        body,
        subject,
        recipients,
        "Front Arena {0}".format(environment)
    )
    try:
        email_helper.send()
    except Exception as exc:
        LOGGER.exception("Error while sending e-mail: %s", exc)
    LOGGER.info("Email sent successfully.")


def ael_main(ael_dict):
    swwr_trades = select_trade_population()
    trade_list = []
    for trade in swwr_trades:
        if in_breach_check(trade) and booking_time_passage(trade, ael_dict['start_time'], ael_dict['end_time']):
            trade_list.append(trade)
    if trade_list:
        body = construct_body(trade_list)
        send_report(body, list(ael_dict['out_email']))
