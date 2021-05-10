import xml.etree.cElementTree as ET
import acm
from t3_alloc_logic import get_process_class


def settle_days_offset(trade):
    calendar = trade.Instrument().Currency().Calendar()
    return calendar.BankingDaysBetween(trade.TradeTime()[:10],
                                       trade.AcquireDay())


def process_theta_ladder_report(report, params, xml_string):
    root = ET.fromstring(xml_string)
    table = root.find(".//Table")
    keep_rows = table.findall("./Rows/Row/Rows/Row/Rows/Row/Rows/Row/Rows")
    prf_level = table.find("./Rows/Row")
    all_rows = prf_level.find("./Rows")
    prf_level.remove(all_rows)
    for row in keep_rows:
        prf_level.append(row)
    output = ET.tostring(root, "ISO-8859-1")
    return output


def remove_first_grouping_level(report, params, xml_string):
    # XML preprocessing function for FWorksheetReport.
    root = ET.fromstring(xml_string)
    table = root.find(".//Table")
    top_level = table.find("./Rows/Row")
    first_grouping = top_level.find("./Rows")
    second_grouping = table.findall("./Rows/Row/Rows/Row/Rows")
    top_level.remove(first_grouping)
    for row in second_grouping:
        top_level.append(row)
    output = ET.tostring(root, "ISO-8859-1")
    return output


def is_trade_valid(trade):
    Process = get_process_class(trade.Portfolio().Name())
    return Process.is_trade_valid(trade)


def get_parent_portfolio(portfolio):
    plinks = acm.FPortfolioLink.Select("memberPortfolio = %s" % portfolio.Oid())
    if plinks and plinks[0]:
        return plinks[0].OwnerPortfolio()
    return None


def get_parent_prf_l1(trade):
    parent_prf = get_parent_portfolio(trade.Portfolio())
    if not parent_prf:
        return ''
    return parent_prf.Name()


def get_parent_prf_l2(trade):
    parent_prf_l1 = get_parent_portfolio(trade.Portfolio())
    if not parent_prf_l1:
        return ''
    parent_prf_l2 = get_parent_portfolio(parent_prf_l1)
    if not parent_prf_l2:
        return ''
    return parent_prf_l2.Name()


def get_open_close(trade):
    Process = get_process_class(trade.Portfolio().Name())
    if Process.is_closing(trade):
        return 'to Close'
    else:
        return 'to Open'


def get_match_id(trade):
    Process = get_process_class(trade.Portfolio().Name())
    return Process.get_match_id(trade)


def get_long_short(trade):
    Process = get_process_class(trade.Portfolio().Name())
    return Process.get_position_string(trade)


def get_bp_trade(trade):
    Process = get_process_class(trade.Portfolio().Name())
    return Process.get_bp_trade(trade)


def get_alloc_key(trade):
    Process = get_process_class(trade.Portfolio().Name())
    return Process.get_key(trade)
    

def get_payment_amount(trade, payment_type):
    total_amount = 0
    for payment in trade.Payments():
        if payment.Type() == payment_type:
            amount = acm.DenominatedValue(payment.Amount(), payment.Currency(),
                                          payment.Type(), None)
            total_amount = total_amount + amount if total_amount else amount
    return total_amount

