"""-----------------------------------------------------------------------------
Sends notification if the blank prices are encountered at some of the stocks in FA.

Custom date can be set in order to see older blank prices.
Defines list of old stocks which have blank prices and should be omitted in the report.

HISTORY
================================================================================
Date            Change no       Developer           Description
--------------------------------------------------------------------------------
2021-02-16      FAPE-505        Katerina Frickova   Initial implementation
--------------------------------------------------------------------------------
"""

import acm
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_time import to_datetime
from datetime import datetime
from PS_SendEmailNotification import CreateEmailReport
from PS_NotificationTextObject import NotificationTextObject

LOGGER = getLogger(__name__)
CURRENT_TIME = to_datetime(acm.Time.TimeNow())
DATE_TODAY = acm.Time.DateToday()
TEXT_OBJECT_NAME = 'PS_Blank_Stock_Prices_{}'


def historical_date_hook(selected):
    date_custom = ael_variables.get('historical_date')
    date_custom.enabled = selected.value
    date_custom.mandatory = selected.value


def send_email_hook(selected):
    email_destination = ael_variables.get('email_destinations')
    email_destination.enabled = selected.value 
    email_destination.mandatory = selected.value 
    

ael_variables = AelVariableHandler()

ael_variables.add(
    'ignored_stocks',
    label='List of the excluded stocks',
    alt='Old stocks with blank prices.'
)

ael_variables.add_bool(
    'historical_values',
    label='Show Historical Values',
    default=False,
    alt='Choose date to see historical values.',
    hook=historical_date_hook
)

ael_variables.add(
    'historical_date',
    default='YYYY-MM-DD',
    label='Historical Date',
    alt='Date in the format YYYY-MM-DD'
)

ael_variables.add_bool(
    'send_email',
    label='Send email',
    default=True,
    alt='Send email to the given email addresses.',
    hook=send_email_hook
)

ael_variables.add(
    'email_destinations',
    label='Email Destinations',
    mandatory=True,
    alt='Email Destinations - Comma Separated'
)


class BlankPriceReport(CreateEmailReport):

    def __init__(self, table_header_tuple, table_rows_list):
        super(BlankPriceReport, self).__init__(table_header_tuple, table_rows_list)

    def to_html_description(self):
        return 'Blank Prices Notification: {date_today}.<br><br>The following stocks have blank\
                prices:<br><small style="color:Tomato;">\
                Dates highlighted in red are in latest, but update time is outdated.\
                </small><br><br>'.format(date_today=DATE_TODAY)


def check_input_date(date):

    try:
        datetime_output = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        return datetime_output
    except ValueError as ve:
        LOGGER.error('Incorrect date format, should be YYYY-MM-DD.')
        raise ve
        
        
def find_blank_prices_historical(stocks, historical_date):
    stock_collection = {}
    
    for stock in stocks:
        hist_prices = stock.HistoricalPrices().Filter(
                lambda price: price.Day() == historical_date).SortByProperty('UpdateTime', False)
        spot_hist_prices = hist_prices.Filter(lambda price: price.Market().Name() == 'SPOT')

        if spot_hist_prices:
            if str(spot_hist_prices[0].Settle()) == 'nan':
                LOGGER.info('Blank settle price found for stock: {}'.format(stock.Name()))
                stock_collection[str(spot_hist_prices[0].Oid())] = [spot_hist_prices[0].Oid(), stock.Name(),
                                                                    spot_hist_prices[0].ReadProperty('UpdateTime')]
            
    return stock_collection
    
    
def find_blank_prices_latest(stocks):
    stock_collection = {}

    for stock in stocks:
        spot_prices = stock.Prices().Filter(
            lambda price: price.Market().Name() == 'SPOT').SortByProperty('UpdateTime', False)

        if spot_prices:
            update_date = to_datetime(spot_prices[0].ReadProperty('UpdateTime')).strftime("%Y-%m-%d")
            
            if str(spot_prices[0].Settle()) == 'nan':
                if update_date != DATE_TODAY:
                    LOGGER.info('Settle price for stock {} is blank.\
                                    The last time it was updated is on {}'.format(stock.Name(), update_date))
                                    
                    stock_collection[str(spot_prices[0].Oid())] = [spot_prices[0].Oid(), stock.Name(),
                                                                   '<i style="color:Tomato;">{}</i>'
                                                                   .format(spot_prices[0].ReadProperty('UpdateTime'))]
                else:
                    LOGGER.info('Blank settle price found for stock: {}'.format(stock.Name()))
                    stock_collection[str(spot_prices[0].Oid())] = [spot_prices[0].Oid(),
                                                                   stock.Name(),
                                                                   spot_prices[0].ReadProperty('UpdateTime')]

    return stock_collection


def add_issue_status(resolved_issues, unresolved_issues):
    issue_collection = []
            
    if unresolved_issues:
        for oid, issue in list(unresolved_issues.items()):
            issue.append('<i style="color:#FF0000">unresolved</i>')
            tuple_issue = tuple(issue)
            issue_collection.append(tuple_issue)
    
    if resolved_issues:
        for oid, issue in list(resolved_issues.items()):
            issue.append('<i style="color:#228B22">resolved</i>')
            tuple_issue = tuple(issue)
            issue_collection.append(tuple_issue)
    
    return issue_collection


def ael_main(ael_dict):
    all_stocks = acm.FStock.Select('')
    
    filtered_stocks = [stock for stock in all_stocks if stock.Name() not in ael_dict['ignored_stocks']]
    
    if ael_dict['historical_values']:
        date = check_input_date(ael_dict['historical_date'])
        blank_prices = find_blank_prices_historical(filtered_stocks, date)
    else:
        blank_prices = find_blank_prices_latest(filtered_stocks)
        date = DATE_TODAY
    
    stocks_text_object = NotificationTextObject(TEXT_OBJECT_NAME.format(date.replace('-', '_')), blank_prices)
    resolved_issues = stocks_text_object.update_text_object()

    issue_collection = add_issue_status(resolved_issues, blank_prices)
    
    if ael_dict['send_email'] and issue_collection:
        header_table = ('Price Oid', 'Stock', 'Update time', 'Issue status')
        blank_price_report = BlankPriceReport(header_table, issue_collection)
        
        LOGGER.info('Sending email')
        try:
            blank_price_report.send_mail('Stocks Blank Prices', ael_dict['email_destinations'])
        except Exception as err:
            LOGGER.error('Failed to send email notification: {}'.format(err))
        else:
            LOGGER.info('Email sent')
    else:
        LOGGER.info('Blank prices check done.')
