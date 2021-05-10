"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    OperationsSTPMain

DESCRIPTION
    Module-mode ATS used for event-driven Operations STP (straight-through-
    processing).

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-05      FAOPS-448       Hugo Decloedt           Kgomotso Gumbo          Initial implementation.
                                Cuen Edwards
                                Stuart Wilson
2019-04-18      FAOPS-425       Cuen Edwards            Kgomotso Gumbo          Addition of support for cashflow events.
2020-04-30      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Relocated list of subscribed tables to parameters module
                                                                                OperationsSTPParameters.
2020-05-26      PCGDEV-10       Sihle Gaxa              James Stevens           Addition of the Trade table for SBL auto confirm process
2020-10-19      PCGDEV-598      Sihle Gaxa              Shaun Du Plessis        Addition of transaction independent Dual booking hook
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import FOperationsATSRoutines as ATSRoutines

import at_logging
import OperationsSTPParameters


LOGGER = at_logging.getLogger(__name__)
LOGGING_FORMAT = '%(asctime)s,%(msecs)03d %(levelname)s %(message)s'
LOGGING_DATE_FORMAT = '%y%m%d %H%M%S'
at_logging.setFormat(LOGGING_FORMAT, LOGGING_DATE_FORMAT)
EXCLUDED_HOOKS = ["SBL Collateral Dual Booking STP Hook"]


class FOperationsSTPATSEngine(ATSRoutines.FOperationsATSEngine):
    """
    ATS Engine for Operations STP.
    """

    def __init__(self, name, dbTables, paramsModule, paramsModuleTemplateName):
        """
        Constructor.
        """
        ATSRoutines.FOperationsATSEngine.__init__(self, name, dbTables, paramsModule, paramsModuleTemplateName)

    def Start(self):
        """
        ATS Engine Start hook for Operations STP.

        This hook is called by FOperationsATSRoutines.
        """
        LOGGER.info('STP hooks:')
        for stp_hook in OperationsSTPParameters.stpHooks:
            LOGGER.info("- {hook_name}".format(
                hook_name=stp_hook.Name()
            ))

    def Work(self, message, event_object):
        """
        ATS Engine Work hook for Operations STP.

        This hook is called by FOperationsATSRoutines.
        """
        LOGGER.info('Processing event on {event_object_class} {event_object_oid}.'.format(
            event_object_class=event_object.ClassName(),
            event_object_oid=event_object.Oid()
        ))
        for stp_hook in OperationsSTPParameters.stpHooks:
            try:
                if stp_hook.IsTriggeredBy(event_object):
                    info_message = "Event on {event_object_class} {event_object_oid} has triggered "
                    info_message += "STP Hook '{hook_name}', executing..."
                    LOGGER.info(info_message.format(
                        event_object_class=event_object.ClassName(),
                        event_object_oid=event_object.Oid(),
                        hook_name=stp_hook.Name()
                    ))
                    if stp_hook.Name() in EXCLUDED_HOOKS:
                        stp_hook.PerformSTP(event_object)
                    else:
                        self._perform_stp_in_transaction(stp_hook, event_object)
            except:
                error_message = "An exception occurred executing STP hook '{hook_name}' "
                error_message += "for event on {event_object_class} {event_object_oid}."
                LOGGER.exception(error_message.format(
                    hook_name=stp_hook.Name(),
                    event_object_class=event_object.ClassName(),
                    event_object_oid=event_object.Oid()
                ))

    def Stop(self):
        """
        ATS Engine Stop hook for Operations STP.

        This hook is called by FOperationsATSRoutines.
        """
        LOGGER.info('Stop called at {time}.'.format(time=acm.Time.TimeNow()))

    def Status(self):
        """
        ATS Engine Status hook for Operations STP.

        This hook is called by FOperationsATSRoutines.
        """
        return "Operations STP ATS status"

    def _perform_stp_in_transaction(self, stp_hook, event_object):
        """
        Execute the STP hook within a transaction.
        """
        acm.BeginTransaction()
        try:
            stp_hook.PerformSTP(event_object)
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            raise


ats_engine = FOperationsSTPATSEngine('Operations STP', OperationsSTPParameters.eventTables, OperationsSTPParameters,
    'OperationsSTPParameters')
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
    ats_routines.Work()


def stop():
    """
    Stop hook for module-mode ATS.

    This hook is called when a module-mode ATS is stopped and is used
    to perform any shutdown actions (e.g. disconnecting from an AMB,
    etc.).
    """
    ats_routines.Stop()


def status():
    """
    Status hook for module-mode ATS.

    This hook is called to retrieve the status of a module-mode ATS.
    """
    return ats_routines.Status()
