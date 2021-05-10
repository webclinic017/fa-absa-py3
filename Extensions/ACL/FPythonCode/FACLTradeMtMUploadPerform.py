""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLTradeMtMUploadPerform.py"
import acm
import amb
import traceback

class FACLTradeMtMUploadPerform:
    def __init__(self, gateway, factory, writer, logme, summary):
        self._gateway = gateway
        self._factory = factory
        self._writer  = writer
        self._logme   = logme
        self._summary = summary
        self._generator = self._initMbfGenerator()

    def SendMtM(self, trades):
        trades = sorted(trades, key=lambda trade: trade.Oid())
        
        for trade in trades:
            msgCount = 0
            try:
                mbfObject = self._gateway.Process(self.CreateMbfObject(trade)) 
            except Exception as e:
                self._summary.notOk(self._summary.FAIL, trade, 'UPLOAD', str(e), trade.Oid())
                tb = traceback.format_exc()
                self._logme(tb, 'DEBUG')
                continue
   
            if mbfObject:
                armlMessages = None
                
                try:
                    armlMessages = self._factory.Work(mbfObject, trade)
                except Exception as e:
                    msg = "Error sending trade: %s\n%s" % (trade.Oid(), str(e))
                    self._summary.notOk(self._summary.FAIL, trade, 'UPLOAD', msg, trade.Oid())
                    
                if armlMessages:
                    msgCount = len(armlMessages)
                    self._logme('%s %s resulted in %s ArML messages to be added to the message buffer' % (trade.ClassName(), trade.Oid(), msgCount), 'INFO')
                    for tradeFromFactory, armlMsg in armlMessages:
                        self._writer.addMsgToBuffer(armlMsg, tradeFromFactory)
            if msgCount == 0:
                self._summary.notOk(self._summary.IGNORE, trade, 'UPLOAD', 'Object did not result in any ArML messages', trade.Oid())
    
        self._writer.writeBuffer()

    def _initMbfGenerator(self):
        source = 'FACL_MTM_UPLOAD'
        generator = acm.FAMBAMessageGenerator()
        generator.SourceName(source)
        return generator
        
    def CreateMbfObject(self, trade):
        mbfBuffer = amb.mbf_create_buffer_from_data(self._generator.Generate(trade).AsString())
        return mbfBuffer.mbf_read()
