from TMS_Functions_Common import FloatToStrFormat

''' =======================================================================
    TMS TradeWrapper Base

    This module exposes the base element wrapper as well as the base factory 
    wrapper classes. The "detail classes" (trade, instrument, leg, etc.)
    of all asset classes will be derived from the Wrapper class. All trade
    factory wrappers will be derived from WrapperFactory.

    Eben Mare

    Changes 	            : Added _addFloatProperty to Wrapper
    
    Date                    : //2012
    Developer               : Jan Mach
    Requester               : Mathew Berry
    CR Number               :  
    ======================================================================= '''

""" Base class for all wrappers """

class Wrapper:
    def __init__(self):
        self._properties = []
        self._children = []

    def _addProperty(self, name, value):
        self._properties.append( (name, value) )
 
    def _addFloatProperty(self, name, value, precision=5):
        self._addProperty(name, FloatToStrFormat(value, precision) )

    def _addChild(self, child):
        self._children.append( child )

    def _sortProperties(self):
        self._properties.sort()

    def _getPropertyValue(self, attrib):
        for item in self._properties:
            if item[0] == attrib:
                return item[1]

    def _changePropertyValue(self, name, value):
        for index, item in enumerate(self._properties):
            if item[0] == name:
                self._properties[index] = (name, value)
                return True

        return False

    def getTypeName(self):
        raise NotImplementedError

    def properties(self):
        return self._properties

    def children(self):
        return self._children


""" Base class for all wrapper factories """
class WrapperFactory:
    def supports(self, obj):
        raise NotImplementedError

    def create(self, obj):
        raise NotImpementedError

    def _name(self):
        raise NotImpementedError
