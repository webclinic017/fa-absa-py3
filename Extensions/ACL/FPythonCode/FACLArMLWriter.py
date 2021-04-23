""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLArMLWriter.py"
from FACLArMLResponse import FACLArMLResponseTextView
import re

class FACLArMLWriter(object):
    def __init__(self, logme, summary):
        self._msgBufferDict = {}
        self._logme = logme
        self._summary = summary
        self._regexpRefId = re.compile('<Ref>(.+?)</Ref>', re.IGNORECASE)
    
    def _getRefId(self, msg):
        ref = self._regexpRefId.search(msg)
        if ref:
            return ref.group(1)
        else:
            return
    
    def isCreateGivePermission(self, msg):
        return '<Name>Security Rights\Branches</Name>' in msg
    
    def addMsgToBuffer(self, msg, acmObj=None):
        refId = self._getRefId(msg)
        if refId and not self.isCreateGivePermission(msg):
            if refId in self._msgBufferDict:
                self._logme('Replaced message for reference %s in buffer' % refId, 'INFO')
            self._logme('Message Added: %s' % msg, 'DEBUG')
            self._msgBufferDict[refId] = (msg, acmObj)
    
    def writeBuffer(self):
        pass

class FACLArMLFileWriter(FACLArMLWriter):
    def __init__(self, fileObject, logme, summary):
        super(FACLArMLFileWriter, self).__init__(logme, summary)
        self._fileObject = fileObject
        
        self._regexpDealReverse = re.compile(re.escape('Deal.Reverse'), re.IGNORECASE)
        
    def __enter__(self):
        self._fileObject.write("<?xml version='1.0' encoding='UTF-8'?><ArML>")
        return self
    
    def __exit__(self, typeV, value, traceback):
        try:
            self._fileObject.write('</ArML>')
        except:
            pass
            
    def _isDealReverse(self, msg):
        return self._regexpDealReverse.search(msg)
        
    def _removeProloge(self, msg):
        return re.sub(r'<\?.*>', '', msg).strip()
    
    def writeBuffer(self):
        for _, msgTuple in list(self._msgBufferDict.items()):
            msg, acmObj = msgTuple
            if self._isDealReverse(msg):
                oid = acmObj.Oid() if acmObj else -1
                self._summary.notOk(self._summary.IGNORE, acmObj, 'UPLOAD', 'Message is ignored since it is a Deal.Reverse message', oid)
            else:
                msg = self._removeProloge(msg)
                self._fileObject.write(msg)
                self._summary.ok(acmObj, 'UPLOAD')

        
        
class FACLArMLACRWriter(FACLArMLWriter):
    def __init__(self, router, responseBuilder, logme, summary):
        super(FACLArMLACRWriter, self).__init__(logme, summary)
        self._router = router
        self._responseBuilder = responseBuilder
        
        self._regexpConfirm = re.compile(re.escape('Deal.Confirm'), re.IGNORECASE)
      
    def _replaceConfirmWithAdd(self, msg):
        return self._regexpConfirm.sub('Deal.Add', msg)
    
    def writeBuffer(self):
        for _, msgTuple in list(self._msgBufferDict.items()):
            msg, acmObj = msgTuple
            msgTowrite = self._replaceConfirmWithAdd(msg)
            
            reply = self._router.RouteMessagePersistentWithReply(acmObj, msgTowrite)
            response = self._responseBuilder(reply)
            self._logResponse(response, acmObj)
            
    def _logResponse(self, response, acmObj):
        if response.ExceptionOccurred():
            oid = acmObj.Oid() if acmObj else -1
            details = FACLArMLResponseTextView(response)
            if response.ActionDealAlreadyReversed():
                self._summary.notOk(self._summary.IGNORE, acmObj, 'UPLOAD', details.Details(), oid)
            else:
                self._summary.notOk(self._summary.FAIL, acmObj, 'UPLOAD', details.Details(), oid)
        else:
            self._summary.ok(acmObj, 'UPLOAD')
