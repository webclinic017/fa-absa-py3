""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/SingleValueTask.py"
import acm

import Contracts_SingleValue_Messages_SingleValueMessages as SingleValueTraits
import Contracts_Tk_Messages_TkMessages as Tk
import SingleValueUtils

from SingleValueUtils import (
    PaceVariantConversion, 
    PaceVariantFieldConversion,
    AcmVariant,
    Unpack
    )


class SpaceCollection(object):
    
    _spaces = dict()
    
    def __init__(self, scope):
        self._scope = scope
        
    def GetSpace(self, context, sheetClass, distributedMode=False):
        calcKey = (self._scope, context, sheetClass, distributedMode)
        if calcKey not in self._spaces:
            self._spaces[calcKey] = acm.Calculations().CreateCalculationSpaceFromScope(*calcKey)
        return self._spaces[calcKey]
        

class TaskInterface(object):

    def Result(self):
        raise NotImplementedError

    def HasPendingResult(self):
        return False

    def Destroy(self):
        pass
        
        
class CalculationTask(TaskInterface):
    pass
    

class TaskArguments(object):

    def __init__(self, *args):
        self._args = args
        
    def Get(self, index):
        return Unpack(self._args, index)
        
    def GetAll(self):
        return self._args
        
        
class CalculationTaskArguments(TaskArguments):

    @property
    def SpaceCollection(self):
        if isinstance(self._args[-1], SpaceCollection):
            return self._args[-1]
        return None
        
    def GetAll(self):
        return self._args[:-1]
    

class Task(object):

    def __init__(self, producer, taskId, definition):
        self.taskId = taskId
        self.producer = producer
        self.definition = definition
        self.interface = None
        self.Init()

    def Init(self):
        self.interface = self.CreateInterface()
        self.SendResult()
        self.producer.SendInitialPopulateDone(self.taskId)        
        
    def CreateInterface(self):
        module = __import__(self.definition.moduleName)
        className = self.definition.className
        interface = getattr(module, className)
        if issubclass(interface, CalculationTask):
            return interface(*self.CalculationArguments())
        return interface(*self.Arguments())
            
    def CreateResult(self):
        result = SingleValueTraits.Result()
        interfaceResult = self.interface.Result()
        resultValue = self.CreateVariant(interfaceResult)
        result.value.CopyFrom(resultValue)
        return result
        
    def CreateResultKey(self):
        resultKey = SingleValueTraits.ResultKey()
        resultKey.id = self.taskId
        return resultKey
        
    def CalculationArguments(self):
        args = self.Arguments()
        spaceCollection = SpaceCollection(self.producer.LoopbackCalculationScope())
        args.append(spaceCollection)
        return args
               
    def Arguments(self):
        return list(self.definition.arguments)
            
    def SendResult(self):
        result = self.CreateResult()
        resultKey = self.CreateResultKey()
        self.producer.SendInsertOrUpdate(self.taskId, resultKey, result)
        
    def OnDoPeriodicWork(self):
        if not hasattr(self.interface, 'HasPendingResult'):
            self.producer.OnDestroyTask(self.taskId)
        elif self.interface.HasPendingResult():
            self.SendResult()
        
    def Destroy(self):
        if hasattr(self.interface, 'Destroy'):
            self.interface.Destroy()
        self.interface = None
        self.taskId = None
        self.producer = None
        self.definition = None
        
    @staticmethod
    def CreateVariant(interfaceResult):
        variant = Tk.Variant()    
        domain = AcmVariant.ToDomain(interfaceResult)
        variant.type = PaceVariantConversion.ToPaceType(interfaceResult, domain)
        if variant.type != PaceVariantConversion.NONE:
            fieldName = PaceVariantFieldConversion.FieldName(variant.type)
            setattr(variant, fieldName, AcmVariant.Value(interfaceResult, domain))
        return variant
