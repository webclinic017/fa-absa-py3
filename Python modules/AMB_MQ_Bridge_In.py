import acm
import FSwiftMLUtils
import AMB_MQ_Bridge_Base

TASK_USER = acm.UserName()
TASK_USER_PARAM = FSwiftMLUtils.Parameters(TASK_USER)
CONFIG_PARAM = FSwiftMLUtils.Parameters('FSwiftSolutionConfig')
SWIFT_READER_CONFIG = FSwiftMLUtils.Parameters('FSwiftReaderConfig')
AMB_ADDRESS = str(getattr(CONFIG_PARAM, 'AMBAddress', None))
AMB_SENDER_NAME = str(getattr(TASK_USER_PARAM, 'AMBAReceiver', None))
AMB_SUBJECT = str(getattr(SWIFT_READER_CONFIG, 'AMBReceiverSubject', None))
SOURCE = 'SWIFT_NETWORK' 
MBF_OBJECT = 'SWIFT_MESSAGE'
MBF_TAG = 'SWIFT'

MQ_TO_AMB = AMB_MQ_Bridge_Base.MQ_TO_AMBA(TASK_USER, AMB_ADDRESS, AMB_SENDER_NAME, AMB_SUBJECT, SOURCE, MBF_OBJECT, MBF_TAG)

def start():
    """
    This hook is called when a module-mode ATS is started and is used
    to perform any start-up actions (e.g. connecting to an AMB, etc.).
    If the start hook returns False, then the ATS will shutdown.
    """
    MQ_TO_AMB._start()
   

def work():
    """
    This hook is called continuously after a module-mode ATS has been
    started and can be used to perform any periodic work.  It is
    approximately called, max 10 times/sec when idle).
    """
    MQ_TO_AMB._work()


def stop():
    """
    This hook is called when a module-mode ATS is stopped and is used
    to perform any shutdown actions (e.g. disconnecting from an AMB,
    etc.).
    """
    MQ_TO_AMB._stop()


def status():
    """
    This hook is called to retrieve the status of a module-mode ATS.
    """
    return MQ_TO_AMB._status()
