""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FTransactionHandler.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
""" ---------------------------------------------------------------------------
MODULE

    TransactionHandler

    Classes to implement the transaction functionality.

DESCRIPTION

----------------------------------------------------------------------------"""


import acm
import FBDPCommon
import FBDPRollback

from contextlib import contextmanager
from FBDPCurrentContext import Logme


class TransactionHandler(object):

    def Name(self):
        raise NotImplementedError

    def AddAll(self, object):
        raise NotImplementedError

    def Add(self, object):
        raise NotImplementedError

    def TestMode(self):
        raise NotImplementedError
        
    def transit_business_process_state(self, bp, event, toState = None, reason = ''):
        raise NotImplementedError

    @contextmanager
    def Transaction(self):
        raise NotImplementedError
            

class UndefinedHandler(TransactionHandler):

    def Name(self):
        pass

    def AddAll(self, object):
        pass

    def Add(self, object):
        pass
                
    def TestMode(self):
        pass

    def transit_business_process_state(self, bp, event, toState = None, reason = ''):
        pass

    @contextmanager
    def Transaction(self):
        yield
        
            
class RollbackHandler(TransactionHandler):

    def __init__(self, rollback):
        self._rollback = rollback
        
    def Name(self):
        return self._rollback.spec.name
        
    def AddAll(self, objects):
        for obj in objects:
            self.Add(obj)

    def Add(self, obj, attribs=[], op=None, modified_child_entities=None):
        if obj:
            if FBDPCommon.is_acm_object(obj) and obj.IsKindOf(acm.FTrade):
                self._rollback.add_trade(obj, attribs, op, modified_child_entities)
            else:
                self._rollback.add(obj, attribs, op, modified_child_entities)
    
    def TestMode(self):
        return FBDPRollback.RollbackWrapper.Testmode

    def transit_business_process_state(self, bp, event, toState = None, reason = ''):
        self._rollback.transit_business_process_state(bp, event, toState, reason)

    @contextmanager
    def Transaction(self):
        try:
            self._rollback.beginTransaction()
            yield
            self._rollback.commitTransaction()
        except Exception as e:
            Logme()('Exception occurred, %s' %(e), "ERROR")
            self._rollback.abortTransaction()
            

class ACMHandler(TransactionHandler):

    def __init__(self):
        self._objects = acm.FArray()
        
    def Name(self):
        pass
        
    def AddAll(self, objects):
        for obj in objects:
            self.Add(obj)

    def Add(self, obj):
        if obj:
            self._objects.Add(obj)
            
    @contextmanager
    def Transaction(self):
        try:
            acm.BeginTransaction()
            yield
            self._objects.Commit()
            acm.CommitTransaction()
        except Exception as e:
            Logme()('Exception occurred, %s' %(e), "ERROR")
            acm.AbortTransaction()
        finally:
            self._objects.Clear()
