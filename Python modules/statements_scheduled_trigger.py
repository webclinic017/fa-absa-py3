"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        This script identifies all statements that should be
                        generated on a particular day and creates corresponding
                        business processes.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-03-14  CHG1001488095  Libor Svoboda       Enable Option statements
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
"""
import acm

from at_addInfo import save
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_time import acm_date
from statements_config import STATEMENTS


CALENDAR = acm.FCalendar['ZAR Johannesburg']
LOGGER = getLogger(__name__)
WEEKLY = 1  # nth day of week
MONTHLY = 1  # nth day of month


def enable_custom_date(ael_input):
    """Hook enabling custom date."""
    custom_date = ael_variables.get('release_date')
    if ael_input.value == 'Custom Date':
        custom_date.enabled = True
    else:
        custom_date.enabled = False
        custom_date.value = acm.Time.DateToday()


ael_variables = AelVariableHandler()
ael_variables.add(
    'date_selection',
    label='Release Date',
    collection=['Date Today', 'Custom Date'],
    default='Date Today',
    cls='string',
    hook=enable_custom_date,
    alt='Custom Date or Date Today.'
)
ael_variables.add(
    'release_date',
    label='Custom Date',
    cls='date',
    default=acm.Time.DateToday(),
    alt='Custom release date.'
)
ael_variables.add(
    'val_date',
    label='Valuation Date',
    collection=['Same as Release', 'Release - 1BD'],
    default='Release - 1BD',
    cls='string',
    alt='Valuation Date defined in relation to the Release Date.'
)
ael_variables.add(
    'statement_type',
    label='Statement type',
    collection=sorted(STATEMENTS.keys()),
    default='FEC',
    cls='string'
)
ael_variables.add(
    'filter_clients',
    label='Filter clients',
    multiple=True,
    mandatory=False,
    cls='FParty',
    alt='If specified, statements will be only triggered for the selected parties.',
)


def get_release_date(ael_params):
    if ael_params['date_selection'] == 'Date Today':
        return acm.Time.DateToday()
    return acm_date(ael_params['release_date'])


def trigger_statements(date_today, frequency):
    if frequency == 'Daily':
        return not CALENDAR.IsNonBankingDay(None, None, date_today)
    elif frequency == 'Weekly':
        first_day_of_week = acm.Time.FirstDayOfWeek(date_today)
        last_sunday = acm.Time.DateAddDelta(first_day_of_week, 0, 0, -1)
        day_before_release = acm.Time.DateAddDelta(last_sunday, 0, 0, WEEKLY - 1)
        release_date = CALENDAR.AdjustBankingDays(day_before_release, 1)
        return release_date == date_today
    elif frequency == 'Monthly':
        first_day_of_month = acm.Time.FirstDayOfMonth(date_today)
        last_day_of_previous_month = acm.Time.DateAddDelta(first_day_of_month,
                                                           0, 0, -1)
        day_before_release = acm.Time.DateAddDelta(last_day_of_previous_month, 
                                                   0, 0, MONTHLY - 1)
        release_date = CALENDAR.AdjustBankingDays(day_before_release, 1)
        return release_date == date_today
    return False


def request_statements(bps, state):
    for bp in bps:
        party_name = bp.Subject().Name()
        try:
            bp.ForceToState(state)
            bp.Commit()
        except Exception as exc:
            LOGGER.exception('%s: Failed to force %s to "%s".' 
                             % (party_name, bp.Oid(), state))
        else:
            LOGGER.info('%s: %s forced to "%s".' 
                        % (party_name, bp.Oid(), state))


def ael_main(ael_params):
    LOGGER.msg_tracker.reset()
    statement_type = ael_params['statement_type']
    release_date = get_release_date(ael_params)
    LOGGER.info('Statement type: %s, Release date: %s.' 
                % (statement_type, release_date))
    config = STATEMENTS[statement_type]
    
    contact_rules = []
    if trigger_statements(release_date, 'Daily'):
        LOGGER.info('%s is a daily release date.' % release_date)
        contact_rules.extend(config.find_contact_rules('Daily'))
        contact_rules.extend(config.find_contact_rules('All'))
    if trigger_statements(release_date, 'Weekly'):
        LOGGER.info('%s is a weekly release date.' % release_date)
        contact_rules.extend(config.find_contact_rules('Weekly'))
    if trigger_statements(release_date, 'Monthly'):
        LOGGER.info('%s is a monthly release date.' % release_date)
        contact_rules.extend(config.find_contact_rules('Monthly'))
        
    if not contact_rules:
        LOGGER.info('No contact rules found.')
        LOGGER.info('Completed successfully.')
        return
    
    if ael_params['val_date'] == 'Same as Release':
        val_date = release_date
    else:
        val_date = CALENDAR.AdjustBankingDays(release_date, -1)
    
    contacts = list({contact_rule.Contact() 
                         for contact_rule in contact_rules})
    bps = []
    for contact in contacts:
        party = contact.Party()
        if (ael_params['filter_clients'] 
                and party not in ael_params['filter_clients']):
            LOGGER.info('%s: Skipped, not specified in the filter.' 
                        % party.Name())
            continue
        if config.find_bps(contact, val_date):
            LOGGER.info('%s: BP already created, contact %s.'
                        % (party.Name(), contact.Name()))
            continue
        try:
            bp = config.create_bp(contact, val_date)
        except Exception as exc:
            LOGGER.exception('%s: Failed to create BP.' % party.Name())
            continue
        LOGGER.info('%s: Created BP %s.' % (party.Name(), bp.Oid()))
        bps.append(bp)
    
    request_statements(bps, 'Pending Calculation')
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError('ERRORS occurred. Please check the log.')
    LOGGER.info('Completed successfully.')
