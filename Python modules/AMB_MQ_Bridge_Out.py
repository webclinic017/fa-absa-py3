import acm
import FSwiftMLUtils
import AMB_MQ_Bridge_Base

TASK_USER = acm.UserName()
TASK_USER_PARAM = FSwiftMLUtils.Parameters(TASK_USER)
CONFIG_PARAM = FSwiftMLUtils.Parameters('FSwiftSolutionConfig')
SWIFT_READER_CONFIG = FSwiftMLUtils.Parameters('FSwiftReaderConfig')
AMB_ADDRESS = str(getattr(CONFIG_PARAM, 'AMBAddress', None))
AMB_SENDER_NAME = str(getattr(TASK_USER_PARAM, 'AMBASender', None))
AMB_SUBJECTS = [str(getattr(CONFIG_PARAM, 'AMBASenderSource', None)) + '/BUSINESSPROCESS']
PAYMENT_TYPE = getattr(TASK_USER_PARAM, 'PaymentType', None)

AMB_TO_MQ = AMB_MQ_Bridge_Base.AMB_TO_MQ(TASK_USER, AMB_ADDRESS, AMB_SENDER_NAME, AMB_SUBJECTS, PAYMENT_TYPE)

def start():
    """
    This hook is called when a module-mode ATS is started and is used
    to perform any start-up actions (e.g. connecting to an AMB, etc.).
    If the start hook returns False, then the ATS will shutdown.
    """
    AMB_TO_MQ._start()


def work():
    """
    This hook is called continuously after a module-mode ATS has been
    started and can be used to perform any periodic work.  It is
    approximately called, max 10 times/sec when idle).
    """
    AMB_TO_MQ._work()


def stop():
    """
    This hook is called when a module-mode ATS is stopped and is used
    to perform any shutdown actions (e.g. disconnecting from an AMB,
    etc.).
    """
    AMB_TO_MQ._stop()


def status():
    """
    This hook is called to retrieve the status of a module-mode ATS.
    """
    return AMB_TO_MQ._status()
