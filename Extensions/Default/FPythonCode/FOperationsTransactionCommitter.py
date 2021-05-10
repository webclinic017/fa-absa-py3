""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTransactionCommitter.py"
import acm

from FOperationsWriter import Writer
from FOperationsExceptions import CommitException, UpdateCollisionException

#-------------------------------------------------------------------------
class TransactionCommitter(Writer.Committer):

    #-------------------------------------------------------------------------
    def __init__(self, operations, resultCls):
        super(TransactionCommitter, self).__init__()
        
        self.__operations = operations
        self.__resultCls = resultCls
        self.__provider = None
        self.__logHooks = dict()

    #-------------------------------------------------------------------------
    def PO_Init(self, provider):
        self.__provider = provider

    #-------------------------------------------------------------------------
    def CO_CreateResult(self):
        return self.__resultCls()

    #-------------------------------------------------------------------------
    def CO_Commit(self, objs):
        result = self.CO_CreateResult()

        try:
            self.PrivateCommitTransaction(objs, result)
            
        except CommitException as e:
            self.__provider.LP_Log('ERROR: A commit exception occurred while committing transaction, transaction aborted: %s' % str(e))
            result.RE_AddException(e)
            
        except UpdateCollisionException as e:
            self.__provider.LP_Log('ERROR: An update collision occurred while committing transaction, transaction aborted: %s' % str(e))
            result.RE_AddException(e)

        if len(self.__logHooks):
            self.PrivateLogTransaction(objs)

        return result

    #-------------------------------------------------------------------------
    def CO_RegisterLogHook(self, objClass, idx):
        self.__logHooks[objClass] = idx

    #-------------------------------------------------------------------------
    def PrivateCommitTransaction(self, objs, result):
        acm.BeginTransaction()
        try:
            for op, obj in objs:
                self.__operations[op](obj)
            acm.CommitTransaction()
            
        except Exception as e:
            acm.AbortTransaction()
            self.PrivateRaiseException(e)

        for op, obj in objs:
            result.RE_AddToResult(op, obj)
        
    #-------------------------------------------------------------------------
    def PrivateLogTransaction(self, objs):
        for op, obj in objs:
            className = str(obj.ClassName())

            if className in self.__logHooks:
                self.__provider.LP_LogVerbose(self.__provider.HA_CallHook(self.__logHooks[className], obj, op))

    #-------------------------------------------------------------------------
    def PrivateRaiseException(self, e):
        if (str(e).find("Update collision") != -1):
            raise UpdateCollisionException(e)
        else:
            raise CommitException(e)

#-------------------------------------------------------------------------
# Committer class used for testing, no commit is done, but result is aggregated
#-------------------------------------------------------------------------
class TestTransactionCommitter(TransactionCommitter):

    def __init__(self, operations, resultCls):
        super(TestTransactionCommitter, self).__init__(operations, resultCls)

    #-------------------------------------------------------------------------
    def CO_Commit(self, objs):
        result = self.CO_CreateResult()

        for op, obj in objs:
            result.RE_AddToResult(op, obj)
        
        return result
