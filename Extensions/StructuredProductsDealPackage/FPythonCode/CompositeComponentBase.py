
import acm
import inspect, string, types
from DealPackageDevKit import CompositeAttributeDefinition, DealPackageException, ParseSuffixedFloat

class CompositeBaseComponent(CompositeAttributeDefinition):
    
    # ##########################################################################
    # Methods to transform solver parameter input to solve for top value
    # ##########################################################################
    
    def TransformSolver(self, attrName, value):
        goalValue = None
        topValue = None

        if self.HasMethod("TopValueFields") and type(self.GetMethod("TopValueFields")()) == dict:
            if self.GetMethod("TopValueFields")().has_key('PV'):
                f = self.GetMethod('GetFormatter')(self.GetMethod("TopValueFields")().get('PV'))
                goalValue = ParseSuffixedFloat(value, suffix=['pv'], formatter=f)
                if goalValue != None:
                    topValue = self.GetMethod("TopValueFields")().get('PV')
                    
            if self.GetMethod("TopValueFields")().has_key('Price') and (goalValue == None):
                f = self.GetMethod('GetFormatter')(self.GetMethod("TopValueFields")().get("Price"))
                goalValue = ParseSuffixedFloat(value, suffix=['price'], formatter=f)
                if goalValue != None:
                    topValue = self.GetMethod("TopValueFields")().get("Price")
                    
        if goalValue != None and topValue != None:
            return self.GetMethod("Solve")(topValue, attrName, goalValue)
        else:
            return value


