""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLBatchUploadPerform.py"
import acm
import amb
import traceback

class FACLBatchUploadPerform:
    def __init__(self, gateway, factory, writer, logme, summary):
        self._gateway = gateway
        self._factory = factory
        self._writer = writer
        self._logme = logme
        self._summary = summary
        self._generator = self._initMbfGenerator()
        
    def SendObjects(self, acmObjsToUpload):
        acmObjsToUpload = sorted(acmObjsToUpload, key=self._objectSortHelper)

        for acmObj in acmObjsToUpload:
            msgCount = 0
            try:
                mbfObject = self._gateway.Process(self.CreateMbfObject(acmObj))
            except Exception as e:
                self._summary.notOk(self._summary.FAIL, acmObj, 'UPLOAD', str(e), acmObj.Oid())
                tb = traceback.format_exc()
                self._logme(tb, 'DEBUG')
                continue
            if mbfObject:
                try:
                    armlMessages = self._factory.Work(mbfObject, acmObj)
                except Exception as e:
                    self._summary.notOk(self._summary.FAIL, acmObj, 'UPLOAD', str(e), acmObj.Oid())
                    tb = traceback.format_exc()
                    self._logme(tb, 'DEBUG')
                    continue
                if armlMessages:
                    msgCount = len(armlMessages)
                    self._logme('%s %s resulted in %s ArML messages to be added to the message buffer' % (acmObj.ClassName(), acmObj.Oid(), msgCount), 'INFO')
                    for acmObjFromFactory, armlMsg in armlMessages:
                        self._writer.addMsgToBuffer(armlMsg, acmObjFromFactory)
            if msgCount == 0:
                self._summary.notOk(self._summary.IGNORE, acmObj, 'UPLOAD', 'Object did not result in any ArML messages', acmObj.Oid())
        
        self._writer.writeBuffer()
        
    def _objectSortHelper(self, acmObj):
        """
        Will return a list with oid´s
        [789] # parent
        [789, 123] # child
        [789, 123, 456] # grandchild
        When sorted the parent will always come first, child next...
        """
        def partyCompareList(acmObj):
            compareList = []
            if acmObj.Parent():
                compareList = partyCompareList( acmObj.Parent() )
            compareList.append( acmObj.Oid() )
            return compareList
        
        def insCompareList(acmObj):
            compareList = []
            if acmObj.Underlying():
                compareList = insCompareList( acmObj.Underlying() )
            compareList.append( acmObj.Oid() )
            return compareList
        
        if acmObj.IsKindOf(acm.FParty):
            return partyCompareList( acmObj )
        elif acmObj.IsKindOf(acm.FInstrument):
            return insCompareList( acmObj )
        else:
            return acmObj.Oid()

    def _initMbfGenerator(self):
        source = 'FACL_BATCH_UPLOAD'
        generator = acm.FAMBAMessageGenerator()
        generator.SourceName(source)
        return generator
        
    def CreateMbfObject(self, acmObj):
        mbfBuffer = amb.mbf_create_buffer_from_data(self._generator.Generate(acmObj).AsString())
        return mbfBuffer.mbf_read()
