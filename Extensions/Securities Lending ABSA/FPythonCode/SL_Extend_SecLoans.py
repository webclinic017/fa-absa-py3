"""--------------------------------------------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending, Front Arena Upgrade 2010.2
PURPOSE                 :  Extends the open end of security loans, Added completed successfully for
                           RTB Error checking script.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach, RTB
DEVELOPER               :  Paul Jacot-Guillarmod, Heinrich Cronje
CR NUMBER               :  243997, 733363

History:

Date            Who                             What
    
2010-10-16      Paul Jacot-Guillarmod           CR494829, Update script to take CFD security loans into account
2019-09-25      Libor Svoboda                   Update nominal factor calculations.
2020-01-09      Libor Svoboda                   Update sec loan regenerate logic.
2020-06-03      Libor Svoboda                   Regenerate all cashflows for CFD sec loans.
2020-08-18      Sihle Gaxa                      PCGDEV-566: Update to extend same day loans
2020-10-27      Sihle Gaxa                      PCGDEV-605 Exclude today's same day loans from extend script
------------------------------------------------------------------------------------------------------------------"""

import acm
import sl_functions
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from at_time import acm_date


LOGGER = getLogger(__name__)
CALENDAR = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time.DateToday()
PREVBUSDAY = CALENDAR.AdjustBankingDays(TODAY, -1)
START_DATES = {
    'Date Today': TODAY,
    'Previous Business Day': PREVBUSDAY,
    'Custom Date': TODAY,
}


def enable_custom_date(ael_input):
    custom_date = ael_variables.get('custom_date')
    if ael_input.value == 'Custom Date':
        custom_date.enabled = True
    else:
        custom_date.enabled = False
        custom_date.value = START_DATES[ael_input.value]


ael_variables = AelVariableHandler()
ael_variables.add(
    'start_date',
    label='Start Date',
    collection=list(START_DATES.keys()),
    default='Previous Business Day',
    cls='string',
    hook=enable_custom_date,
    alt='Start date for Reprice cashflow recalculation.'
)
ael_variables.add(
    'custom_date',
    label='Custom Date',
    cls='date',
    default=PREVBUSDAY,
    alt='Custom start date.'
)
ael_variables.add(
    'instruments',
    label='Instruments to Extend',
    cls='FInstrument',
    mandatory=True,
    multiple=True,
)


def extend_security_loans(instruments, start_date):
    for instrument in instruments:
        try:
            if instrument.InsType() != 'SecurityLoan':
                continue
            leg = instrument.Legs().At(0)
            if leg.EndDate() <= TODAY and instrument.OpenEnd() == 'Open End':
                if leg.StartDate() == leg.EndDate():
                    if leg.EndDate() == TODAY:
                        continue
                    leg.EndDate(TODAY)
                    leg.Commit()
                    instrument.SLGenerateCashflows()
                instrument.SLExtendOpenEnd()
                LOGGER.info("Instrument '%s': Open End extended." % instrument.Name())
                if instrument.AdditionalInfo().SL_CFD():
                    instrument.SLGenerateCashflows(update_leg=True)
                    LOGGER.info("Instrument '%s': Cashflows generated." % instrument.Name())
            elif (leg.EndDate() >= TODAY and instrument.AdditionalInfo().SL_CFD()
                    and instrument.OpenEnd() in ('Terminated', 'None')):
                instrument.SLGenerateCashflows(update_leg=True)
                LOGGER.info("Instrument '%s': Cashflows generated." % instrument.Name())
            elif leg.StartDate() == TODAY and instrument.AdditionalInfo().SL_CFD():
                instrument.SLGenerateCashflows(update_leg=True)
                LOGGER.info("Instrument '%s': Cashflows generated." % instrument.Name())
        except Exception as exc:
            LOGGER.exception("Instrument '%s' not extended: '%s'", instrument.Name(), exc)


def ael_main(args):
    LOGGER.msg_tracker.reset()
    instruments = args['instruments']
    if args['start_date'] == 'Custom Date':
        start_date = acm_date(args['custom_date'])
    else:
        start_date = START_DATES[args['start_date']]
    LOGGER.info("Using start date: %s" % start_date)
    
    extend_security_loans(instruments, start_date)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
        
    if not LOGGER.msg_tracker.warnings_counter:
        LOGGER.info("Completed successfully")
