""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLProlong.py"
import acm
from FACLAttributeMapper import FACLAttributeMapper
from FACLArMLMessageBuilder import FACLArMLMessageBuilder
from FACLTradeActionUtils import is_trade_action_prolong
from FACLFunctions import FACLUnwrapTradeActionOriginal

def FloatEq(a, b, tolerance):
    return round(abs(a - b), tolerance) == 0
    
def IsEarlyDelivery(parent, farChild):    
    return parent.ValueDay() == farChild.ValueDay()
    
class ProlongFxSwap():
    def __init__(self, trade, mapper):
        self.trade = trade
        self.mapper = mapper        
        self.master = FACLUnwrapTradeActionOriginal(trade)                             
        self.parent = trade.TrxTrade()
    
    def IsPartialProlong(self):
        trade = self.trade
        parent = self.parent
        nominal = -trade.Nominal() if IsEarlyDelivery(parent, trade) else trade.Nominal()     

        return not acm.Math.AlmostEqual(parent.Nominal(), nominal)

    def Add(self):
        parent = self.parent
        trade = self.trade
        ref = str(self.master.ConnectedTrade().Oid()) 
    
        if IsEarlyDelivery(parent, trade):
            near = trade.ConnectedTrade()
            if acm.Math.AlmostEqual(-parent.Nominal(), trade.Nominal()):
                prolongation = self.FullProlong(near.ValueDay())
            else:
                prolongation = self.PartialProlongBase(near.ValueDay(), near.Nominal(), near.Premium())
        else:
            if acm.Math.AlmostEqual(parent.Nominal(), trade.Nominal()):
                prolongation = self.FullProlong(trade.ValueDay())
            else:
                prolongation = self.PartialProlongBase(parent.ValueDay(), parent.Nominal() - trade.Nominal(), parent.Premium() - trade.Premium())
                ref = str(self.parent.ConnectedTrade().Oid()) 
                            
        attributes = self.mapper.MapAttributes(prolongation)            
        attributes['Reference'] = ref   

        return prolongation, attributes
    
    def AddPartial(self):
        parent = self.parent
    
        if IsEarlyDelivery(parent, self.trade):
            prolongation = self.PartialEarlyDeliveryExtension()
        else:
            prolongation = self.PartialProlongExtension()
                            
        attributes = self.mapper.MapAttributes(prolongation)            
        attributes['Reference'] = str(self.trade.ConnectedTrade().Oid())        

        return prolongation, attributes
 
    def FullProlong(self, date):      
        prolongation = self.master.Clone()
        prolongation.RegisterInStorage()
        prolongation.ValueDay(date)
        prolongation.AcquireDay(date)
        return prolongation
                        
    def PartialProlongBase(self, date, nominal, premium):        
        prolongation = self.parent.Clone()
        prolongation.RegisterInStorage()
        
        # make sure to send a forward and not a swap
        if self.parent != self.master:
            prolongation.TradeProcess(1<<13)
        
        prolongation.ValueDay(date)
        prolongation.AcquireDay(date)
        prolongation.Nominal(nominal)
        prolongation.Premium(premium)
        return prolongation

    def PartialProlongExtension(self):        
        trade = self.trade
        parent = self.parent        
        prolongation = trade.Clone()
        prolongation.RegisterInStorage()
        prolongation.TradeProcess(1<<13)
        prolongation.ValueDay(parent.ValueDay())

        return prolongation

    def PartialEarlyDeliveryExtension(self):        
        trade = self.trade
        parent = self.parent
        ins = trade.Instrument()                
        prolongation = acm.FTrade(instrument=ins)
        prolongation.RegisterInStorage()
        prolongation.TradeProcess(1<<13)
        prolongation.Currency(trade.Currency())
        prolongation.ValueDay(trade.ValueDay())
        prolongation.AcquireDay(trade.AcquireDay())
        prolongation.Counterparty(trade.Counterparty())
        prolongation.Acquirer(trade.Acquirer())
        prolongation.TradeTime(trade.TradeTime())
        prolongation.Price(trade.Price())
        prolongation.Premium(parent.Premium() + trade.Premium())
        prolongation.Nominal(parent.Nominal() + trade.Nominal())
        
        return prolongation
        
    def EarlyDelivery(self):
        prolongation = self.master.Clone()
        prolongation.RegisterInStorage()
        near = self.trade.ConnectedTrade()
        prolongation.ValueDay(near.ValueDay())
        prolongation.AcquireDay(near.AcquireDay())
        return prolongation
    
    def Reverse(self):                 
        attribs = self.mapper.MapAttributes(self.parent)
        target = self.parent if self.IsPartialProlong() else self.master
        attribs['Reference'] = str(target.ConnectedTrade().Oid())

        return target, attribs

        
class ProlongFxForward():
    def __init__(self, trade, mapper):
        self.trade = trade
        self.mapper = mapper        
        self.master = FACLUnwrapTradeActionOriginal(trade)                             
        self.parent = trade.TrxTrade()    
        
    def IsPartialProlong(self):
        trade = self.trade
        parent = self.parent    
        nominal = -trade.Nominal() if IsEarlyDelivery(parent, trade) else trade.Nominal()        
        return not acm.Math.AlmostEqual(nominal, parent.Nominal())
    
    def Add(self):
        master = self.master
        parent = self.parent        
        trade = self.trade
        attributes = None
        
        if IsEarlyDelivery(master, trade):          
            prolongation = master.Clone()
            prolongation.RegisterInStorage()
            
            if self.IsPartialProlong():                
                prolongation.Nominal(parent.Nominal() + trade.Nominal())
                prolongation.UpdatePremium(False)
            else:
                prolongation.AcquireDay(trade.ConnectedTrade().AcquireDay())
                prolongation.ValueDay(trade.ConnectedTrade().ValueDay())
                
            attributes = self.mapper.MapAttributes(prolongation)
            attributes['Reference'] = str(parent.Oid())
            
            return prolongation, attributes  
        else:
            prolongation = master.Clone()
            prolongation.RegisterInStorage()
            
            if self.IsPartialProlong():        
                prolongation.ValueDay(parent.ValueDay())
                prolongation.AcquireDay(parent.AcquireDay())
                prolongation.Nominal(parent.Nominal() - trade.Nominal())
                prolongation.Premium(parent.Premium() - trade.Premium())
                ref = parent.ConnectedTrade().Oid()
            else:
                prolongation.ValueDay(trade.ValueDay())
                prolongation.AcquireDay(trade.AcquireDay())                
                ref = master.Oid()
                
            attributes = self.mapper.MapAttributes(prolongation)
            attributes['Reference'] = str(ref)
            
            return prolongation, attributes  
                
        return trade, attributes


    def AddPartial(self):
        trade = self.trade        
        master = self.master
        
        if IsEarlyDelivery(master, trade):    
            prolongation = self.master.Clone()
            prolongation.RegisterInStorage()
            source = trade.ConnectedTrade()
            prolongation.Nominal(source.Nominal())
            prolongation.Premium(source.Premium())
            prolongation.ValueDay(source.ValueDay())
            prolongation.AcquireDay(source.AcquireDay())
            attributes = self.mapper.MapAttributes(prolongation)            

            attributes['Reference'] = str(trade.ConnectedTrade().Oid())
            return prolongation, attributes
            
        else:            
            prolongation = self.master.Clone()
            prolongation.RegisterInStorage()
            prolongation.Nominal(trade.Nominal())
            prolongation.Premium(trade.Premium())
            prolongation.ValueDay(trade.ValueDay())
            prolongation.AcquireDay(trade.AcquireDay())

            attributes = self.mapper.MapAttributes(prolongation)            
            attributes['Reference'] = str(trade.ConnectedTrade().Oid())
            return prolongation, attributes

    def Reverse(self):
        if (self.IsPartialProlong() and self.parent != self.master):
            prol = ProlongFxForward(self.parent, self.mapper)
            t, attribs = prol.AddPartial()
        else:
            attribs = self.mapper.MapAttributes(self.parent)
            attribs['Reference'] = str(self.master.Oid())            
                
        return self.parent, attribs


class ProlongRepo():
    def __init__(self, trade, mapper):
        self.trade = trade
        self.mapper = mapper        
        self.parent = trade.Contract()        
        self.master = FACLUnwrapTradeActionOriginal(trade)                             
    
    def Add(self):
        master = self.master
        parent = self.parent        
        trade = self.trade
        attributes = None
        
        if master and master != trade:            
            if FloatEq(master.FaceValue(), trade.FaceValue(), 5):
                prolongation = master.Clone()
                prolongation.RegisterInStorage()
                
                insClone = master.Instrument().Clone()
                insClone.RegisterInStorage()
                legs = insClone.Legs()
                legs[0].EndDate(trade.Instrument().EndDate())
                prolongation.Instrument(insClone)            
                    
                attributes = self.mapper.MapAttributes(prolongation)
                attributes['Reference'] = str(master.Oid())
                
                return prolongation, attributes
            else:
                prolongation = parent.Clone()
                prolongation.RegisterInStorage()
                
                prolongation.Nominal(parent.Nominal() - trade.Nominal())
                    
                attributes = self.mapper.MapAttributes(prolongation)
                attributes['Reference'] = str(parent.Oid())
                
                return prolongation, attributes  
                    
        return trade, attributes
    
    def AddPartial(self):
        prolongation = self.trade.Clone()
        prolongation.RegisterInStorage()        
        prolongation.ValueDay(self.parent.ValueDay())
        attributes = self.mapper.MapAttributes(prolongation)            
        attributes['Reference'] = str(self.trade.ConnectedTrade().Oid())        

        return prolongation, attributes

    def IsPartialProlong(self):
        return not FloatEq(self.master.FaceValue(), self.trade.FaceValue(), 5)

    def Reverse(self):
        attribs = self.mapper.MapAttributes(self.parent)        
        attribs['Reference'] = str(self.parent.Oid())
        
        return self.parent, attribs
        

def GetProlonger(trade, mapper):
    if is_trade_action_prolong(trade):
        if trade.IsFxSwap():
            master = FACLUnwrapTradeActionOriginal(trade)        
    
            if master.IsFxSwap():
                return ProlongFxSwap(trade, mapper)
            else:                
                return ProlongFxForward(trade, mapper)
        elif trade.Instrument().IsRepoInstrument():
            return ProlongRepo(trade, mapper)

    return None
