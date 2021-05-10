import acm
from DealPackageDevKit import DealPackageDefinition, DealPackageException, Settings

@Settings(GraphApplicable=False)
class EditableObjectBase(DealPackageDefinition):
    
    def EditableObject(self):   
        return self.DealPackage()
        
    def Object(self):   
        return self.EditableObject().Object()
        
