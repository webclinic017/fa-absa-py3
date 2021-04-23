""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/FTradingCapacityProducer.py"

import FACABTradingCapacityMessages
import FPaceProducer
import acm
import traceback


def CreateProducer():
    return FTradingCapacityProducer()

class FTradingCapacityProducer(FPaceProducer.Producer):
    def __init__(self):
        super(FTradingCapacityProducer, self).__init__()
        self._tasks = {}
        self._depots = acm.FDepot.Select("")
        self._depots.AddDependent(self)
        self._clients = acm.FClient.Select("")
        self._clients.AddDependent(self)
        self._portfolios = acm.FPhysicalPortfolio.Select("compound=False")
        self._portfolios.AddDependent(self)

        for entity in list(self._depots) + list(self._clients) + list(self._portfolios):
            ObjectAspects.Factory( entity )

        self._countryparty = CounterParty(self)
        
    '''
        Pace Core interface
    '''
    def OnCreateTask(self, taskId, request):
        try:
            for entity in list( self._depots ) + list( self._portfolios ) + list( self._clients ): 
                self.DoInsertOrUpdate(entity.Name(), taskId)
            
            self._countryparty.SendAlgoResults(taskId)
                    
            self._tasks.setdefault( taskId, request)
            self.SendInitialPopulateDone( taskId )
        except:
            print(traceback.format_exc())
            self.SendException( taskId, traceback.format_exc() )

    def OnDoPeriodicWork(self):
        pass

    def OnDestroyTask(self, taskId):
        if taskId in self._tasks.keys():
            self._tasks.pop( taskId )

    def DoDelete(self, entityName):
        resultKey = FACABTradingCapacityMessages.ResultKey()
        resultKey.account = entityName.decode('latin1')
        for taskId in self._tasks.keys():
            self.SendDelete( taskId, resultKey )

    def DoInsertOrUpdate(self, entityName, taskId = None):
        resultKey = FACABTradingCapacityMessages.ResultKey()
        resultKey.account = entityName.decode('latin1')
        result = FACABTradingCapacityMessages.Result()
        result.validationState = FACABTradingCapacityMessages.Result.WHITE
        taskIds = [ taskId ] if taskId != None else self._tasks.keys()
        for tid in taskIds:
            self.SendInsertOrUpdate( tid, resultKey, result )

    def ServerUpdate(self, sender, aspect, param):
        objectAspect = ObjectAspects.Factory(param) 
        if aspect.AsString() == "remove":
            self.DoDelete(objectAspect.CachedName())
            objectAspect.Remove()
        else:
            if objectAspect.IsNameChanged():
                self.DoDelete(objectAspect.CachedName())
                objectAspect.UpdateCachedName()
            self.DoInsertOrUpdate(objectAspect.CachedName())

class ObjectAspects(object):
    _instances = {}                 # { limitAspect => limitAspect } - used to find an existing item based on its hash
    def __init__(self, item):
        self._item = item
        self.UpdateCachedName()     # Store to know if an update is triggered by a change of the name

    def __hash__(self):
        return hash( ( self._item.Class(), self._item.Oid() ) )

    def __eq__(self, other):
        return ( self._item.Class(), self._item.Oid() ) == ( other._item.Class(), other._item.Oid() )

    @staticmethod
    def Factory(entity, * args):
        instance = ObjectAspects( entity, * args )
        return ObjectAspects._instances.setdefault( instance, instance )   # Get newly created instance or get previously existing one (based on __hash__ above)

    @staticmethod
    def Instances():
        return ObjectAspects._instances

    def Remove(self):
        return ObjectAspects._instances.pop( self )

    def Name(self):
        return self._item.Name()

    def CachedName(self):
        return self._name

    def UpdateCachedName(self):
        self._name = self.Name()

    def IsNameChanged(self):
        return self.Name() != self.CachedName()


class CounterParty():
    def __init__(self, producer):
        self._producer = producer
        self._isAlgoKeys = []
        self._algoKeys = {}
        self._exchangeIdKeys = {}
        self._counterpartys = acm.FCounterParty.Select("")
        self._counterpartys.AddDependent(self) 
        self.SetAddInfoSpec() 

    def SetAddInfoSpec(self):
        addInfoSpec = acm.FAdditionalInfoSpec["isAlgorithm"] 
        if addInfoSpec == None:
            addInfoSpec = acm.FAdditionalInfoSpec()
            addInfoSpec.FieldName("isAlgorithm")
            addInfoSpec.RecType("Party")
            addInfoSpec.AddSubType("Counterparty")
            addInfoSpec.DataTypeType(acm.FEnumeration['enum(B92StandardType)'].Enumeration('Boolean'))
            addInfoSpec.Description("Storage for Algo Id as Contacts")
            addInfoSpec.Commit()
        self._algoAddInfoSpec = addInfoSpec
        addInfoSpec = acm.FAdditionalInfoSpec["exchange_id"] 
        if addInfoSpec == None:
            addInfoSpec = acm.FAdditionalInfoSpec()
            addInfoSpec.FieldName("exchange_id")
            addInfoSpec.RecType("Contact")
            addInfoSpec.DataTypeType(acm.FEnumeration['enum(B92StandardType)'].Enumeration('Integer'))
            addInfoSpec.Description("TNP RegulatoryAlgoTradingStrategyId")
            addInfoSpec.Commit()
        self._exchangeIdAddInfoSpec = addInfoSpec
    
    def AddCounterParty(self, counterparty, taskId = None):
        if counterparty.AddInfoValue(self._algoAddInfoSpec):
            self._isAlgoKeys.append(counterparty.Oid())
            self._algoKeys[counterparty.Oid()] = list()
            for contact in counterparty.Contacts():
                self.DoSendInsertOrUpdate(counterparty, contact, taskId) 
        
    def DoSendInsertOrUpdate(self, counterparty, contact, taskId = None):
        exchangeId = contact.AddInfoValue(self._exchangeIdAddInfoSpec)
        if exchangeId != None:
            #print "add", str(exchangeId), counterparty.Oid()
            self._algoKeys[counterparty.Oid()].append(contact)
            self._exchangeIdKeys[contact.Oid()] = exchangeId
            resultKey = FACABTradingCapacityMessages.ResultKey()
            resultKey.account = str(exchangeId)
            result = FACABTradingCapacityMessages.Result()
            result.validationState = FACABTradingCapacityMessages.Result.WHITE
            taskIds = [ taskId ] if taskId != None else self._producer._tasks.keys()
            for tid in taskIds:
                self._producer.SendInsertOrUpdate( tid, resultKey, result )
    
    def RemoveCounterParty(self, counterparty):   
        self._isAlgoKeys.remove(counterparty.Oid())
        for contact in self._algoKeys[counterparty.Oid()]:
            self.DoSendDelete(contact)
        del self._algoKeys[counterparty.Oid()]
                
    def DoSendDelete(self, contact, contactsToBeDelete = None):
        exchangeId = self._exchangeIdKeys[contact.Oid()]
        if exchangeId != None:
            #print "remove", str(exchangeId)
            if contactsToBeDelete != None:
                contactsToBeDelete.append(contact)
            del self._exchangeIdKeys[contact.Oid()]
            resultKey = FACABTradingCapacityMessages.ResultKey()
            resultKey.account = str(exchangeId)
            for taskId in self._producer._tasks.keys():
                self._producer.SendDelete( taskId, resultKey )

    def SendAlgoResults(self, taskId):
        for counterparty in list( self._counterpartys ):
            self.AddCounterParty(counterparty, taskId)

    def ServerUpdate(self, sender, aspect, counterparty):
        if aspect.AsString() == "remove":
            if counterparty.Oid() in self._isAlgoKeys:
                self.RemoveCounterParty(counterparty)
        elif aspect.AsString() == "insert":
                self.AddCounterParty(counterparty)
        else:
            if counterparty.Oid() in self._isAlgoKeys:
                if counterparty.AddInfoValue(self._algoAddInfoSpec):
                    for contact in counterparty.Contacts():
                        if not contact in self._algoKeys[counterparty.Oid()]:
                            self.DoSendInsertOrUpdate(counterparty, contact)
                        elif self._exchangeIdKeys[contact.Oid()] != contact.AddInfoValue(self._exchangeIdAddInfoSpec):
                            self.DoSendDelete(contact)
                            self._algoKeys[counterparty.Oid()].remove(contact)
                            self.DoSendInsertOrUpdate(counterparty, contact)
                    contactsToBeDelete = []
                    for contact in self._algoKeys[counterparty.Oid()]:
                        if contact.AddInfoValue(self._exchangeIdAddInfoSpec) == None:
                            self.DoSendDelete(contact, contactsToBeDelete)
                    for contact in contactsToBeDelete:
                        self._algoKeys[counterparty.Oid()].remove(contact)
                else:
                    self.RemoveCounterParty(counterparty)
            else:  
                self.AddCounterParty(counterparty)





