import acm
from DealDevKit import DealDefinition, Str

class DefaultDefinition(DealDefinition):
    
    dummy = Str()
    
    def CustomPanes(self):
        return [{'General': ''}]
        
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('Default deal can\'t be saved.')
        
