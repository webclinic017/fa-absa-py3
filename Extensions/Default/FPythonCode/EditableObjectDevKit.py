import acm
from DealPackageDevKit import *
from EditableObjectBase import EditableObjectBase

class EditableObjectDefinition(EditableObjectBase):

    def Object(self):
        ''' Return the object being edited.
        '''
        return EditableObjectBase.Object(self)
    
    def EditableObject(self):
        ''' Return the FEditableObject instance being edited.
        '''
        return EditableObjectBase.EditableObject(self)
        
    def OnInit(self):
        ''' Override this method to run code at initiation of a new DealPackageDefinition instance.
            For example to initiate member variables.
        '''

    def AssemblePackage(self, optArg = None):
        ''' Override this method to return the default structure of 
            the deal package after creation.
        '''
        
    def OnNew(self):
        ''' Use this method to dictate the behaviour when creating a new Editable Object. The 
            method is called after all the attribute default values are registered.
        '''
        
    def OnOpen(self):
        ''' Use this method to dictate the behaviour when Opening an 
            existing Editable Object. For instance to initialize non-objectmapping attributes.
        '''    
    
    def OnCopy(self, originalDealPackage, anAspectSymbol):
        ''' Use this method to dictate the behaviour when creating a copy.
        '''        

    def OnSave(self, saveConfig):
        ''' Use this method to dictate the behaviour when saving deal package. Possible to return
            an array with objects that should be commited together with the dealpackage.
        '''
    
    def OpenAfterSave(self, config):
        ''' Override this method to dictate what deal package(s) to open after a succecssfull save.
        '''        
        return self.EditableObject()

    def OnDelete(self, allTrades):
        ''' Use this method to dictate the behaviour when deleting a deal package. 
            Return an object or a list of objects that should be deleted.
        '''        

    def IsValid(self, exceptionAccumulator, aspect):
        ''' Override this method if Pre-Save Validation should be applied.
        '''
        
    def Refresh(self):
        ''' Called on any attribute change, and is good for smaller tasks that you need to do
            for many attributes. Avoid heavy calculations and performance intensive tasks here
            since the callback will be called often.
        '''
        
    def CustomPanes(self):
        ''' Return list of panes'''
        return []
