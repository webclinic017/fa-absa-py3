"""----------------------------------------------------------------------------
MODULE
    Struct_Trading_Repo_Booker

DESCRIPTION
    Date                : 15/09/2014
    Purpose             : BuySellBack booking functions from a CSV file
    Requester           : Marko Milutinovic
    Developer           : Dmitry Kovalenko

NOTES
    The module reads trade specifications from a CSV file and books BSB trades
    
HISTORY
ABITFA-5606   Ondrej Bahounek   Add external counteparty column.
                                Add single trade possibility (no mirror).

----------------------------------------------------------------------------"""

import acm

from at_feed_processing import (ValidatingCSVFeedProcessor,
                                FeedProcessor,
                                notify_log)
from at_feed_field_validators import (create_type_validator,
                                      custom_validator_function,
                                      portfolio_validator,
                                      party_validator)

from PS_RepoBonds_BSBBooker import bookBsb


def log(message):
    """Basic console logging with timestamp prefix."""
    print("{0}: {1}".format(acm.Time.TimeNow(), message))


def parse_date(raw_date):
    """Parses the input date.

    The expected format is dd/mm/yyyy.

    Returns an ACM time.
    """

    (day, month, year) = raw_date.split('/')
    return acm.Time.DateFromYMD(year, month, day)
   

def cpty_validate(cpty_id):
    if len(cpty_id) == 0:
        return None
    return party_validator(cpty_id)


def portf_validate(portf_id):
    if len(portf_id) == 0:
        return None
    return portfolio_validator(portf_id)


class BsbCSVFeedProcessor(ValidatingCSVFeedProcessor):
    """Processor used for BSB trade booking."""

    # Key constants for indexing dictionary items
    REPO_FROM = 'Repo From'
    REPO_TO = 'Repo to'
    START_DATE = 'Start Date'
    END_DATE = 'End Date'
    REPO_RATE = 'Repo rate'
    CPARTY = 'Counterparty'
    YMTM = 'YMtM'
    INS_ID = 'Insid'
    QUANTITY = 'Quantity'

    _validation_parameters = {
        REPO_FROM: create_type_validator(acm.FPhysicalPortfolio),
        INS_ID: create_type_validator(acm.FInstrument),
        REPO_RATE: create_type_validator(float),
        REPO_TO: custom_validator_function(portf_validate),
        CPARTY: custom_validator_function(cpty_validate),
        YMTM: create_type_validator(float),
        QUANTITY: create_type_validator(float),
        START_DATE: custom_validator_function(parse_date),
        END_DATE: custom_validator_function(parse_date)
    }

    @classmethod
    def _populate_ael_variables(cls, variables, defaults):
        """This override removes GUI elements added by RecordsFeedProcessor."""

        variables.add('dry_run',
                      label='Dry run',
                      cls='bool',
                      collection=(True, False),
                      default=True)

        variables.add_input_file('file_path', 'CSV Path', mandatory=True)

    def _process_record(self, record, dry_run):
        record_data = record[1]

        # Data in record_data is validated and complex types constructed
        acquirer_pf = record_data[self.REPO_FROM]
        counterparty_pf = record_data[self.REPO_TO]
        acquirer = acquirer_pf.PortfolioOwner()
        counterparty = record_data[self.CPARTY]
        if counterparty is None:
            counterparty = counterparty_pf.PortfolioOwner()
            
        start_date = record_data[self.START_DATE]
        end_date = record_data[self.END_DATE]
        repo_rate = record_data[self.REPO_RATE]
        start_price = record_data[self.YMTM]
        ins = record_data[self.INS_ID]
        quantity = (-1) * record_data[self.QUANTITY]
        
        cparty_portf_name = counterparty_pf.Name() if counterparty_pf else "[no cparty portf]"

        if not dry_run:
            try:
                trade_numbers = bookBsb(start_date, end_date, repo_rate, ins,
                                        quantity, acquirer_pf, acquirer,
                                        counterparty, counterparty_pf,
                                        tradeDate=min(acm.Time.DateToday(),
                                                      start_date),
                                        acquireDate=start_date,
                                        startPrice=start_price,
                                        transaction=None,
                                        status='FO Confirmed')

                log('Trades successfully booked: %s' % trade_numbers)
            except Exception as e:
                log('Error: %s' % str(e))
        else:
            log('%s(%s) -> %s (%s) %s of %s' %
                (acquirer.Name(), acquirer_pf.Name(), counterparty.Name(),
                 cparty_portf_name, quantity, ins.Name()))


ael_variables = BsbCSVFeedProcessor.ael_variables()


def ael_main(args):
    # NOTE: file existence check is not required here, done in constructor.
    processor = BsbCSVFeedProcessor(str(args['file_path']))
    processor.add_error_notifier(notify_log)
    processor.process(args['dry_run'])
