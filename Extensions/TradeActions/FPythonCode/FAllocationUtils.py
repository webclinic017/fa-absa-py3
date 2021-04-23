"""----------------------------------------------------------------------------
    
    MODULE: FAllocationUtils
    
    DECRIPTION: 
    Utility functions and classes

----------------------------------------------------------------------------"""
import acm

PARAMS_NAME = 'FAllocationParameters'

class Parameters( object ):
    
    INSTANCES = {}
    
    def __init__(self, name):
        self.name = name
        self._init_parameters()
    
    @classmethod
    def get_parameters(cls, name):
        if cls.INSTANCES.get(name):
            return cls.INSTANCES.get(name)
        else:
            instance = Parameters(name)
            cls.INSTANCES[name] = instance
            return instance
    
    def _init_parameters(self):
        param_dict = self._get_parameter_dict()
        for k, v in param_dict.items():
            setattr(self, k, v)
        
    def _get_parameter_dict( self):
        """get values from FParameter by name"""
        values = {}
        p = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', self.name)
        try:
            template = p.Value()
        except AttributeError as e:
            logger.ELOG( "Error getting parameters ( %s ): %s", self.name, str( e ) )
        for k in template.Keys():
            k = str(k)
            value = str( template.At(k) )
            value = None if value == "" else value
            values[ str(k) ] = value
        return values

def get_parameters():
    return Parameters.get_parameters(PARAMS_NAME)



class TradeAttributeHelper(object):
    
    ATTRIBUTES = None
        
    @classmethod
    def get_attribute_names(cls):
        if not cls.ATTRIBUTES:
            cls.ATTRIBUTES = cls.get_attribute_names_impl()
        return cls.ATTRIBUTES
        
    @classmethod
    def get_attribute_names_impl(cls):
        attrs = acm.FArray()
        for attr in acm.FTrade.Attributes():
            if acm.Allocation.Dimension().IsValidAttribute(attr):
                name = attr.Name().AsString()
                attrs.Add(name)
        attrs.Sort()
        attrs.AtInsert(0, "")
        return attrs

def get_attribute_names():
    return TradeAttributeHelper.get_attribute_names()

def AllocationParent(trade):
    con = acm.Allocation().ConstellationFromAllocatedTrade(trade)
    if con:
        return con.ParentTrade()
    else:
        con = acm.Allocation().ConstellationFromParentTrade(trade)
        if con:
            return con.ParentTrade()
        else:
            return None
