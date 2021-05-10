import acm
from EditableObjectDevKit import EditableObjectDefinition, Str
class DefaultDefinition(EditableObjectDefinition):
    
    dummy = Str()
    
    def CustomPanes(self):
        return [{'General' : ''}] 
        
    
