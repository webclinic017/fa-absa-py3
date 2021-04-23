""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLMarketPricesUploadPerform.py"
import acm
import math
from FACLArMLResponse import FACLArMLResponse, FACLArMLResponseTextView
            
class FACLMarketPricesUploadPerform:
    FixedIncomeInstrumentTypes = ['Bond', 'Bill', 'BondIndex', 'CD', 'CLN', 'Deposit',
        'FRN', 'FreeDefCF', 'IndexLinkedBond', 'PromisLoan', 'Zero']
    EquityInstrumentTypes = ['Commodity', 'CreditIndex', 'Depositary Receipt', 'EquityIndex', 'Stock', 'ETF']

    def __init__(self, writer, builder, mapper, logme, summary):
        self._writer = writer
        self._builder = builder
        self._mapper = mapper
        self._logme = logme
        self._summary = summary

    def SendPrices(self, instruments, batchSize = 1):
        if batchSize < 1:
            raise ValueError('batchSize must be 1 or greater')

        for ins in instruments:        
            if not ins.IsKindOf(acm.FInstrument):
                self._summary.notOk(self._summary.IGNORE, ins, 'UPLOAD', 'Not an Instrument:', ins.Oid())
                continue
            if ins.IsExpired():
                self._summary.notOk(self._summary.IGNORE, ins, 'UPLOAD', 'Instrument has expired', ins.Oid())
                continue
            if not ins.Issuer():
                self._summary.notOk(self._summary.IGNORE, ins, 'UPLOAD', 'Instrument is missing an issuer', ins.Oid())
                continue
        
            try:
                cols = ('Reference', 'Identification\Code', 'Type', 'Security Information\Market Price')

                params = dict((k, v) for (k, v) in self._mapper.MapAttributes(ins).iteritems() if k in cols)
                if 'Security Information\Market Price' in params:
                    msg = self._builder.CreateMarketPrice(params)
                    self._writer.addMsgToBuffer(msg, ins)
                else:
                    self._summary.notOk(self._summary.IGNORE, ins, 'UPLOAD', 'Instrument have no Market Price', ins.Oid())
            except Exception as e:
                msg = "Error pricing instrument: %s\n%s" % (ins.Name(), str(e))
                self._summary.notOk(self._summary.FAIL, ins, 'UPLOAD', msg, ins.Oid())
        
        self._writer.writeBuffer()
