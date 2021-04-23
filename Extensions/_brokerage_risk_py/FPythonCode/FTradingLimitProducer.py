""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/FTradingLimitProducer.py"
from __future__ import print_function
import FPaceProducer
import FACABTradingLimitMessages
import acm
import traceback
import re


class LimitObjectAspects(object):
    _factoryMap = {}                # { acmClass => limitAspectClass } - used to create limitAspect instance from acm entity
    _instances = {}                 # { limitAspect => limitAspect } - used to find an existing item based on its hash
    def __init__(self, item):
        self._parameters = acm.FConditionParameters()
        self._models = {}           # { FConditionalValueModel -> FCondition }
        self._item = item
        self.UpdateCachedName()     # Store to know if an update is triggered by a change of the name

    def __hash__(self):
        return hash( ( self._item.Class(), self._item.Oid() ) )

    def __eq__(self, other):
        return ( self._item.Class(), self._item.Oid() ) == ( other._item.Class(), other._item.Oid() )

    @staticmethod
    def Factory(entity, * args):
        cls = LimitObjectAspects._factoryMap[ entity.Class() ]
        instance = cls( entity, * args )
        return LimitObjectAspects._instances.setdefault( instance, instance )   # Get newly created instance or get previously existing one (based on __hash__ above)

    @staticmethod
    def Instances():
        return LimitObjectAspects._instances

    def Remove(self):
        return LimitObjectAspects._instances.pop( self )

    def Name(self):
        return self._item.Name()

    def CachedName(self):
        return self._name

    def UpdateCachedName(self):
        self._name = self.Name()

    def KeyName(self):
        return self._name

    def Currency(self):
        return None

    def ConditionParameters(self):
        raise RuntimeError('Not implemented')   # Must be implemented in derived class

    def Models(self):
        return self._models

    def Valid(self):
        return True

    def IsNameChanged(self):
        return self.Name() != self.CachedName()

class PortfolioAspects(LimitObjectAspects):
    def Currency(self):
        return self._item.Currency()

    def ConditionParameters(self):
        self._parameters.Portfolio(self._item)
        return self._parameters

class DepotAspects(LimitObjectAspects):
    def ConditionParameters(self):
        self._parameters.Depot(self._item)
        return self._parameters

class ClientAspects(LimitObjectAspects):
    def ConditionParameters(self):
        self._parameters.Client(self._item)
        return self._parameters

class ContactAspects(LimitObjectAspects):
    _exchangeIdAddInfoSpec = acm.FAdditionalInfoSpec["exchange_id"]

    def ConditionParameters(self):
        self._parameters.Contact(self._item)
        if self._item.Party().Class() == acm.FCounterParty:
            self._parameters.CounterParty(self._item.Party())
        return self._parameters

    def UpdateCachedName(self):
        super(ContactAspects, self).UpdateCachedName()
        self._exchangeId = self._item.AddInfoValue(ContactAspects._exchangeIdAddInfoSpec)

    def KeyName(self):
        return str(self._exchangeId)

    def Valid(self):
        return self._exchangeId != None

    def IsNameChanged(self):
        return super(ContactAspects, self).IsNameChanged() or \
            self._exchangeId != self._item.AddInfoValue(ContactAspects._exchangeIdAddInfoSpec)
        

LimitObjectAspects._factoryMap = { acm.FPhysicalPortfolio : PortfolioAspects, acm.FCompoundPortfolio : PortfolioAspects, acm.FDepot : DepotAspects, acm.FClient : ClientAspects, acm.FContact : ContactAspects }


class Observer:
    def __init__(self, handler):
        self._handler = handler
        self._subscriptions = {}

    def Subscribe(self, item, callback, cbArgs):
        if not item in self._subscriptions:
            item.AddDependent( self )
            self._subscriptions[ item ] = callback, cbArgs

    def ServerUpdate(self, sender, aspect, param):
        callback, cbArgs = self._subscriptions.get( sender )
        callback( param, aspect.AsString(), * cbArgs )





class Handler:
    def __init__(self, producer):
        self._producer = producer
        self._observer = Observer(self)

        self._conditions    = {}   # { condition => set( limits ) }
        self._models        = self.Filter( self.Select( acm.FConditionalValueModel, self.OnModelChange, "modelCategory='AMS Limits'" ), self.ModelFilter )
        self._portfolios    = self.Select( acm.FPhysicalPortfolio, self.OnLimitEntityChange, 'compound=False' )
        self._depots        = self.Select( acm.FDepot, self.OnLimitEntityChange )
        self._clients       = self.Select( acm.FClient, self.OnLimitEntityChange )
        self._contacts      = self.Select( acm.FContact, self.OnLimitEntityChange )

    def UpdateAllLimitsForModels(self, conditions, query = None, group = None):
        # Find models affected by a change to the set of conditions
        models      = [ condition.Model() for condition in conditions ]
        # Find limitAspects currently using any of the conditions (before the change is applied)
        current     = [ limitAspect for condition in conditions for limitAspect in self._conditions.get( condition, [] ) ]
        # Find limitAspects potentially affected directly by any of the conditions once the change is applied
        portfolios  = [ LimitObjectAspects.Factory( condition.Portfolio() ) for condition in conditions if condition.Portfolio() ]
        clients     = [ LimitObjectAspects.Factory( condition.Client() ) for condition in conditions if condition.Client() ]
        depots      = [ LimitObjectAspects.Factory( condition.Depot() ) for condition in conditions if condition.Depot() ]
        contacts    = [ LimitObjectAspects.Factory( condition.Contact() ) for condition in conditions if condition.Contact() ]
        # Find limitAspects potentially affected indirectly - through query or groups - by any of the conditions once the change is applied
        if query:
            portfolios += [ LimitObjectAspects.Factory( portfolio ) for portfolio in query.Query().Select_Triggered().Result() ]
        if group:
            clients += [ LimitObjectAspects.Factory( link.Party() ) for link in group.Parties() ]
        # 'updated' will hold all limitAspects potentially affected by any of the conditions once the change is applied
        # however, if conditions were default condition(s) only then no filters were set (updated will be empty), in which case all items must be checked
        updated     =  [ limitAspect for limitAspect in portfolios + clients + depots + contacts] \
                       or \
                       [ limitAspect for limitAspect in LimitObjectAspects.Instances() ]

        for limitAspect in set( current + updated ):
            self.OnLimitOjbectChange( limitAspect, 'refresh', models )

    def Subscribe01(self, item, callback, *cbArgs):
        self._observer.Subscribe( item, callback, cbArgs )
        callback( item, 'subscribe', * cbArgs )

    def Subscribe(self, collection, callback, *cbArgs):
        self._observer.Subscribe( collection, callback, cbArgs )
        for member in collection:
            callback( member, 'subscribe', * cbArgs )
        return collection

    def Select(self, cls, callback, criteria = ''):
        return self.Subscribe( cls.Select( criteria ), callback )

    def Filter(self, collection, callback, *cbArgs):
        return [ member for member in collection if callback( member, * cbArgs ) ]

    def ModelFilter(self, model):
        return model.Name() in self._producer.LimitNames()

    def OnModelChange(self, model, change):
        if self.ModelFilter(model):
            self.Subscribe01( model.FilterList(), self.OnFilterListChange )
            self.Subscribe( model.Conditions(), self.OnConditionChange )
            if change == 'insert':
                self._models.append( model )

    def OnLimitOjbectChange(self, limitAspect, change, models = None):
        renamed = limitAspect.IsNameChanged()
        updated = renamed

        for model in models or self._models:
            current = limitAspect.Models().get( model )
            matched = model.MatchingCondition( limitAspect.ConditionParameters() )
            if change == 'remove' or matched != current or renamed:
                self.TryRemoveLimit( model, current, limitAspect )
            if change != 'remove' and matched != None:
                self.AddLimit( model, matched, limitAspect )
            updated = updated or matched != current

        if change in [ 'insert', 'update' ] and not renamed:
            self.ProducerUpdateLimit( limitAspect )

        elif change == 'subscribe':
            # No need to call self.ProducerUpdateLimit( limitAspect ) when initializing, since the producer will anyway iterate over all limitAspects
            pass

        elif change == 'refresh' and updated:
            self.ProducerUpdateLimit( limitAspect )

        elif change == 'remove':
            limitAspect.Remove()
            self.ProducerRemoveLimit( limitAspect )

        elif renamed:
            self.ProducerRemoveLimit( limitAspect )
            limitAspect.UpdateCachedName()
            self.ProducerUpdateLimit( limitAspect )

    def OnLimitEntityChange(self, entity, change):
        self.OnLimitOjbectChange( LimitObjectAspects.Factory( entity ), change )

    def OnFilterListChange(self, filter, change):
        if change != 'subscribe':
            conditions = [ condition for model in filter.Models() for condition in model.Conditions() ]
            self.UpdateAllLimitsForModels( conditions )

    def OnConditionChange(self, condition, change):
        if change != 'remove':
            values = self.Subscribe( condition.Curve(), self.OnCurveChange, condition.Model(), condition )

            portfolioQuery = condition.PortfolioFilter()
            if portfolioQuery:
                self.Subscribe01( portfolioQuery, self.OnPortfolioQueryChange )

            clientGroup = condition.ClientGroup()
            if clientGroup:
                self.Subscribe( clientGroup.Parties(), self.OnClientGroupChange )

        if change != 'subscribe':
            self.UpdateAllLimitsForModels( [ condition ], query = condition.PortfolioFilter(), group = condition.ClientGroup() )

    def OnCurveChange(self, curve, change, model, condition):
        if change == 'update':
            for limitAspect in self._conditions.get( condition, () ):
                self.OnLimitUpdate( model, condition, limitAspect )
                self.ProducerUpdateLimit( limitAspect )

    def OnPortfolioQueryChange(self, query, change):
        if change != 'subscribe':
            conditions = { condition for condition in self._conditions if condition.PortfolioFilter() == query }
            self.UpdateAllLimitsForModels( conditions, query = query )

    def OnClientGroupChange(self, link, change):
        if change != 'subscribe':
            group = link.PartyGroup()
            conditions = { condition for condition in self._conditions if condition.ClientGroup() == group }
            self.UpdateAllLimitsForModels( conditions, group = group )

    def OnLimitUpdate(self, model, condition, limitAspect):
        #print 'Updating condition for %s/%s/%s' % ( model.Name(), limitAspect.Name(), limitAspect.Currency().Name() if limitAspect.Currency() else '' )
        pass

    def AddLimit(self, model, condition, limitAspect):
        limitAspect.Models()[ model ] = condition
        self._conditions.setdefault( condition, set() ).add( limitAspect )
        self.OnLimitUpdate( model, condition, limitAspect )

    def TryRemoveLimit(self, model, condition, limitAspect):
        #print 'Removing limit for %s/%s/%s' % ( model.Name(), limitAspect.CachedName(), limitAspect.Currency().Name() if limitAspect.Currency() else '' )
        try:        limitAspect.Models().pop( model )
        except:     pass
        try:        self._conditions.get( condition ).remove( limitAspect )
        except:     pass

    def ProducerUpdateLimit(self, limitAspect):
        self._producer.UpdateLimit(limitAspect, taskIds = [])

    def ProducerRemoveLimit(self, limitAspect):
        self._producer.RemoveLimit(limitAspect, taskIds = [])




class FTradingLimitProducer(FPaceProducer.Producer):
    def __init__(self):
        super(FTradingLimitProducer, self).__init__()

        int32LimitNames = ("maxOrderPerDay", "maxOrderActivity")
        limitNames = ("maxGrossValuePerDay", "maxShortSellValuePerDay", "minOrderValue",  "maxOrderValue", "maxBuyValuePerDay", "maxSellValuePerDay", "maxOrderPerDay", "maxOrderActivity")
        self._int32LimitNames = dict( [ [ self.ConvertProtoName2ModelName( name ), name ] for name in int32LimitNames ] )
        self._limitNames = dict( [ [ self.ConvertProtoName2ModelName( name ), name ] for name in limitNames + int32LimitNames ] )

        self._tasks = {}
        self._calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        self._handler = Handler(self)


    '''
        Pace Core interface
    '''
    def OnCreateTask(self, taskId, request):
        try:
            for limitAspect in LimitObjectAspects.Instances():
                self.UpdateLimit( limitAspect, taskIds = [ taskId ] )
            self._tasks[ taskId ] = request
            self.SendInitialPopulateDone( taskId )
        except:
            print(traceback.format_exc())
            self.SendException( taskId, traceback.format_exc() )

    def OnDoPeriodicWork(self):
        pass

    def OnDestroyTask(self, taskId):
        if taskId in self._tasks.keys():
            self._tasks.pop( taskId )

    def DoSendInsertOrUpdate(self, resultKey, result, taskIds):
        for tid in taskIds or self._tasks.keys():
            self.SendInsertOrUpdate( tid, resultKey, result )

    def DoSendDelete(self, resultKey, taskIds):
        for tid in taskIds or self._tasks.keys():
            self.SendDelete( tid, resultKey )

    def ConvertProtoName2ModelName(self, protoName):
        protoNameSpace = re.sub('([A-Z])', r' \1', protoName)
        return protoNameSpace[:1].upper() + protoNameSpace[1:]

    def LimitNames(self):
        return self._limitNames

    def CreateResultKey(self, limitAspect):
        resultKey = FACABTradingLimitMessages.ResultKey()
        resultKey.account = limitAspect.KeyName().decode('latin1')        # Use this to handle remove properly
        return resultKey

    def RemoveLimit(self, limitAspect, taskIds):
        resultKey = self.CreateResultKey(limitAspect)
        self.DoSendDelete( resultKey, taskIds )

    def UpdateLimit(self, limitAspect, taskIds):
        if not limitAspect.Models():
            return self.RemoveLimit(limitAspect, taskIds)

        if limitAspect.Valid():
            resultKey = self.CreateResultKey(limitAspect)
            result = FACABTradingLimitMessages.Result()

            usedCurrency = limitAspect.Currency()   # Can be None

            for model, condition in limitAspect.Models().iteritems():
                if condition:
                    protobufName = self._limitNames[ model.Name() ]
                    value = condition.Curve()[ 0 ]
                    usedCurrency = usedCurrency or value.Currency()
                    fxRate = value.Currency().Calculation().FXRate(self._calcSpace, usedCurrency)

                    if model.Name() in self._int32LimitNames:
                        setattr(result, protobufName, int( value.MinValue() ))
                        if protobufName == "maxOrderActivity":
                            result.maxOrderActivityTime = 1000 # milliseconds
                    else:
                        setattr(result, protobufName, value.MinValue() * fxRate.Number())

            if usedCurrency:
                result.currency = usedCurrency.Name()

            self.DoSendInsertOrUpdate( resultKey, result, taskIds )



def CreateProducer():
    return FTradingLimitProducer()



