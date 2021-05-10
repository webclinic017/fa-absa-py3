""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLMessageATS.py"
import acm
import amb

from FACLParameters import MessageATSSettings as Parameters
from FOperationsATSRoutines import FOperationsATSRoutines
from FOperationsATSRoutines import FOperationsATSEngine
from FACLArMLMessageBuilder import FACLArMLMessageBuilder
from FACLAttributeMapper import FACLAttributeMapper
from FACLMessageRouter import FACLMessageRouter
from FACLArMLMessageFactory import FACLArMLMessageFactory
import FOperationsUtils as Utils

class FACLMessageATSEngine(FOperationsATSEngine):

    def __init__(self, router, factory):
        super(FACLMessageATSEngine, self).__init__('FACLMessageATS', ['TRADE', 'INSTRUMENT', 'PARTY'], Parameters, 'FACLParametersTemplate')
        self._router = router
        self._factory = factory

    def Start(self):
        pass

    def IsCreateObjectFromAMBAMessage(self, mbfObject):
        return self._factory.IsCreateObjectFromAMBAMessage(mbfObject)

    def Work(self, mbfObject, acmObj):
        try:
            armlMessages = self._factory.Work(mbfObject, acmObj)
            for acmObject, message in armlMessages:
                self._router.RouteMessage(acmObject, message)

        except Exception as e:
            import traceback
            s = 'Failed to process message\n' + traceback.format_exc()            
            Utils.LogAlways(s)

def InitATS():
    senderMBName = Parameters.senderMBName
    senderSource = Parameters.senderSource
    timeout = Parameters.timeoutForReplyInSeconds
    receiverMBName = Parameters.receiverMBName
    
    router = FACLMessageRouter(senderMBName, senderSource, timeout, receiverMBName)
    builder = FACLArMLMessageBuilder()
    mapper = FACLAttributeMapper()
    factory = FACLArMLMessageFactory(builder, mapper)
    engine = FACLMessageATSEngine(router, factory)
    return FOperationsATSRoutines(engine)

def work():
    global ats
    if ats:
        ats.Work()

def start():
    global ats
    ats = InitATS()
    ats.Start()
