"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    DocumentProcessingMain
    
DESCRIPTION
    Module-mode ATS used for event-driven document processing.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-09-17      FAOPS-460       Cuen Edwards            Letitia Carboni         Initial Implementation.
2019-10-14      FAOPS-531       Cuen Edwards            Letitia Carboni         Added support for amendments.
2020-04-30      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Relocated list of subscribed tables to parameters module
                                                                                DocumentProcessingParameters.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import FOperationsATSRoutines as ATSRoutines

import acm
import at_logging
import DocumentProcessingParameters


LOGGER = at_logging.getLogger(__name__)
LOGGING_FORMAT = '%(asctime)s,%(msecs)03d %(levelname)s %(message)s'
LOGGING_DATE_FORMAT = '%y%m%d %H%M%S'
at_logging.setFormat(LOGGING_FORMAT, LOGGING_DATE_FORMAT)


class FDocumentProcessingATSEngine(ATSRoutines.FOperationsATSEngine):
    """
    ATS Engine for Document Processing.
    """

    def __init__(self, name, dbTables, paramsModule, paramsModuleTemplateName):
        """
        Constructor.
        """
        ATSRoutines.FOperationsATSEngine.__init__(self, name, dbTables, paramsModule, paramsModuleTemplateName)

    def Start(self):
        """
        ATS Engine Start hook for Document Processing.

        This hook is called by FOperationsATSRoutines.
        """
        LOGGER.info('Event Handlers:')
        for event_handler in DocumentProcessingParameters.event_handlers:
            LOGGER.info("- {event_handler_name}".format(
                event_handler_name=event_handler.get_name()
            ))

    def Work(self, message, event_object):
        """
        ATS Engine Work hook for Document Processing.

        This hook is called by FOperationsATSRoutines.
        """
        LOGGER.info('Processing event on {event_object_class} {event_object_oid}.'.format(
            event_object_class=event_object.ClassName(),
            event_object_oid=event_object.Oid()
        ))
        for event_handler in DocumentProcessingParameters.event_handlers:
            try:
                if event_handler.handles(message, event_object):
                    info_message = "Event on {event_object_class} {event_object_oid} has triggered "
                    info_message += "event handler '{event_handler_name}', executing..."
                    LOGGER.info(info_message.format(
                        event_object_class=event_object.ClassName(),
                        event_object_oid=event_object.Oid(),
                        event_handler_name=event_handler.get_name()
                    ))
                    event_handler.handle_event(message, event_object)
            except:
                error_message = "An exception occurred executing event handler '{event_handler_name}' "
                error_message += "for event on {event_object_class} {event_object_oid}."
                LOGGER.exception(error_message.format(
                    event_handler_name=event_handler.get_name(),
                    event_object_class=event_object.ClassName(),
                    event_object_oid=event_object.Oid()
                ))

    def Stop(self):
        """
        ATS Engine Stop hook for Document Processing.

        This hook is called by FOperationsATSRoutines.
        """
        LOGGER.info('Stop called at {time}.'.format(time=acm.Time.TimeNow()))

    def Status(self):
        """
        ATS Engine Status hook for Document Processing.

        This hook is called by FOperationsATSRoutines.
        """
        return "Document Processing ATS status"


ats_engine = FDocumentProcessingATSEngine('Document Processing', DocumentProcessingParameters.event_tables,
    DocumentProcessingParameters, 'DocumentProcessingParameters')
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
