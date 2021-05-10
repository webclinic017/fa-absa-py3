"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    NeoXActivityReportMain

DESCRIPTION
    Module-mode ATS used for event-driven Neox Activity Reports (straight-through-processing).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-10-21      FAOPS-959       Ncediso Nkambule        Cuen Edwards            Initial implementation.
2020-10-21      FAOPS-1016      Ncediso Nkambule        Gasant Thulsie          Updated Hook Logger with Hook Name.
2021-02-02      FAOPS-1044      Ncediso Nkambule        Gasant Thulsie          Fixed confusing variable names
2021-03-16      FAOPS-982       Ncediso Nkambule        Gasant Thulsie          Added functions to handle Cashflow driven events.

-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import at_logging
from datetime import datetime, date
import FOperationsATSRoutines as ATSRoutines
import NeoXActivityReportParameters as Parameters
from NeoXActivityReportsUtils import get_fparameter


LOGGER = at_logging.getLogger(__name__)
LOGGING_FORMAT = '%(asctime)s,%(msecs)03d %(levelname)s %(message)s'
LOGGING_DATE_FORMAT = '%y%m%d %H%M%S'
at_logging.setFormat(LOGGING_FORMAT, LOGGING_DATE_FORMAT)


class FActivityReportsNeoxATSEngine(ATSRoutines.FOperationsATSEngine):
    """
    ATS Engine for NeoX Activity Reports.
    """
    starting_time_str = get_fparameter('NeoXParameters', 'neox_starting_time').AsString()
    ending_time_str = get_fparameter('NeoXParameters', 'neox_ending_time').AsString()
    date_format = '%Y-%m-%d %H:%M'
    log_opening_ours = True
    is_business_hours = False

    def __init__(self, name, db_tables, params_module, params_module_template_name):
        """
        Constructor.
        """
        ATSRoutines.FOperationsATSEngine.__init__(self, name, db_tables, params_module, params_module_template_name)

    def Start(self):
        """
        ATS Engine Start hook for NeoX Activity Reports.

        This hook is called by FActivityReportsNeoxATSEngine.
        """
        LOGGER.info('NeoX Activity Reports Hooks:')
        for report_hook in Parameters.reportHooks:
            LOGGER.info("- {hook_name}".format(hook_name=report_hook.Name()))

    def Work(self, message, event_object):
        """
        ATS Engine Work hook for NeoX Activity Reports.

        This hook is called by FActivityReportsNeoxATSEngine.
        """

        LOGGER.info('Processing event on {event_object_class} {event_object_oid}.'.format(
            event_object_class=event_object.ClassName(),
            event_object_oid=event_object.Oid()))
        for report_hook in Parameters.reportHooks:
            try:
                if report_hook.IsTriggeredBy(event_object, event_message=message):
                    info_message = "Event on {event_object_class} {event_object_oid} has triggered "
                    info_message += "NeoX Activity Reports Hook '{hook_name}', executing..."
                    LOGGER.info(info_message.format(
                        event_object_class=event_object.ClassName(),
                        event_object_oid=event_object.Oid(),
                        hook_name=report_hook.Name()))
                    self._perform_report_generation(report_hook, event_object, message)
                else:
                    info_message = "{hook_name} is not triggered by {event_object_class} , {event_object_oid}"
                    LOGGER.info(info_message.format(
                        hook_name=report_hook.Name(),
                        event_object_class=event_object.ClassName(),
                        event_object_oid=event_object.Oid()))
            except Exception as error:
                error_message = "An exception occurred executing NeoX Activity Reports hook '{hook_name}' "
                error_message += "for event on {event_object_class} {event_object_oid}."
                LOGGER.error(error)
                LOGGER.exception(error_message.format(
                    hook_name=report_hook.Name(),
                    event_object_class=event_object.ClassName(),
                    event_object_oid=event_object.Oid()
                ))

    def Stop(self):
        """
        ATS Engine Stop hook for NeoX Activity Reports.

        This hook is called by FActivityReportsNeoxATSEngine.
        """
        LOGGER.info('Stop called at {time}.'.format(time=acm.Time.TimeNow()))

    def Status(self):
        """
        ATS Engine Status hook for NeoX Activity Reports.

        This hook is called by FOperationsATSRoutines.
        """

        return "NeoX Activity Report ATS status"

    @staticmethod
    def _perform_report_generation(report_hook, event_object, message):
        """
        Execute the NeoX Activity hook within a transaction.
        """
        try:
            report_hook.PerformEventProcessing(event_object, message)
        except Exception as error:
            LOGGER.exception(error)
            raise

    def is_acceptable_time(self, date_time_now):
        if self.is_before_starting_time(date_time_now) or self.is_after_ending_time(date_time_now):
            return False
        return True

    def is_before_starting_time(self, date_time_now):
        date_today = date.today().isoformat()
        starting_date_time = datetime.strptime('{} {}'.format(date_today, self.starting_time_str), self.date_format)
        return starting_date_time > date_time_now

    def is_after_ending_time(self, date_time_now):
        date_today = date.today().isoformat()
        ending_date_time = datetime.strptime('{} {}'.format(date_today, self.ending_time_str), self.date_format)
        return ending_date_time < date_time_now


ats_engine = FActivityReportsNeoxATSEngine(
    name='NeoX Activity Reporting',
    db_tables=Parameters.eventTables,
    params_module=Parameters,
    params_module_template_name='NeoXActivityReportParameters')
ats_routines = ATSRoutines.FOperationsATSRoutines(ats_engine)


def start():
    """
    Start hook for module-mode ATS.

    This hook is called when a module-mode ATS is started and is used
    to perform any start-up actions (e.g. connecting to an AMB, etc.).
    If the start hook returns False, then the ATS will shutdown.
    """

    ats_routines.Start()


def work():
    """
    Work hook for module-mode ATS.

    This hook is called continuously after a module-mode ATS has been
    started and can be used to perform any periodic work.  It is
    approximately called, max 10 times/sec when idle).
    """

    date_time_now = datetime.now()
    if ats_engine.is_acceptable_time(date_time_now) is False and FActivityReportsNeoxATSEngine.is_business_hours:
        LOGGER.info("Closing time {}.".format(date_time_now.isoformat()))
        FActivityReportsNeoxATSEngine.is_business_hours = False
        FActivityReportsNeoxATSEngine.log_opening_ours = True
        info_message = "Trading Hours {} at {}. Amendment will not be processed."
        if ats_engine.is_after_ending_time(date_time_now):
            LOGGER.info(info_message.format("ends", ats_engine.ending_time_str))
        if ats_engine.is_before_starting_time(date_time_now):
            LOGGER.info(info_message.format("starts", ats_engine.starting_time_str))

        _do_file_processing(0)
        LOGGER.info("NeoX  ATS will be stale")

    if ats_engine.is_acceptable_time(date_time_now):
        if FActivityReportsNeoxATSEngine.log_opening_ours:
            LOGGER.info("Business hours has opened. Time Now: {}".format(date_time_now.isoformat()))
            FActivityReportsNeoxATSEngine.log_opening_ours = False
        FActivityReportsNeoxATSEngine.is_business_hours = True

        _do_file_processing(15)
        ats_routines.Work()


def stop():
    """
    Stop hook for module-mode ATS.

    This hook is called when a module-mode ATS is stopped and is used
    to perform any shutdown actions (e.g. disconnecting from an AMB,
    etc.).
    """
    _do_file_processing(0)
    ats_routines.Stop()


def status():
    """
    Status hook for module-mode ATS.

    This hook is called to retrieve the status of a module-mode ATS.
    """
    return ats_routines.Status()


def _do_file_processing(minutes_limit):
    for report_hook in Parameters.reportHooks:
        if report_hook.IsTimeForNewFile(report_hook.file_identifier, minutes_limit=minutes_limit):
            report_hook.PerformFileProcessing()
