import acm
from DealPackageDevKit import DealPackageDefinition, List, Action, Text, Settings
from inspect import cleandoc

@Settings(GraphApplicable=False,
          SheetApplicable=False)
class ListControlInteraction(DealPackageDefinition):
    """
    Double click on one of the elements in the list, and it will move to 
    the other list. You can also select one element and then click on the 
    arrows in the middle to move an elemnt.
    """
    
    left          = List(   defaultValue=['Cat', 'Dog', 'Mouse'],
                            label='Left',
                            elementDomain='FString',
                            onSelectionChanged='@UpdateSelectedElement',
                            onDoubleClick='@MouseMoveTo',
                            addNewItem =['First', 'Sorted'],
                            sortIndexCallback='@AnimalSortingCallback',
                            _moveToDestination='right')
                                
    right         = List(   label='Right',
                            elementDomain='FString',
                            onSelectionChanged='@UpdateSelectedElement',
                            onDoubleClick='@MouseMoveTo',
                            addNewItem =['First', 'Sorted'],
                            sortIndexCallback='@AnimalSortingCallback',
                            _moveToDestination='left')
                                
    moveToRight   = Action( label='>',
                            action='@ButtonMoveTo',
                            _moveToDestination='right',
                            enabled='@IsLeftElementSelected',
                            sizeToFit=True)
                                
    moveToLeft    = Action( label='<',
                            action='@ButtonMoveTo',
                            _moveToDestination='left',
                            enabled='@IsRightElementSelected',
                            sizeToFit=True)
                                
    doc           = Text(   defaultValue=cleandoc(__doc__),
                            editable=False,
                            height=80) 

    # ####################### #
    #   Interface Overrides   #
    # ####################### #
    
    def OnInit(self):
        self._selected = {}
        
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_ListControlInteraction_DPE')
    
    def IsValid(self, exceptionAccumulator, aspect):
        exceptionAccumulator('This example is used to demonstrate lists and can not be saved.')

    # ####################### #
    #   Attribute Callbacks   #
    # ####################### #
    
    def MouseMoveTo(self, attrName, selectedElement):
        self.UpdateSelectedElement(attrName, selectedElement)
        self.ButtonMoveTo(attrName)
    
    def ButtonMoveTo(self, attrName):
        destination = self.GetAttributeMetaData(attrName, '_moveToDestination')()
        self._MoveSelectedElementTo( destination )
    
    def UpdateSelectedElement(self, attrName, selectedElement):
        self._selected[attrName] = selectedElement
    
    def IsRightElementSelected(self, attrName):
        return self._GetSelectedElementInList('right') != None
    
    def IsLeftElementSelected(self, attrName):
        return self._GetSelectedElementInList('left') != None

    def AnimalSortingCallback(self, attrName, columnNbr, value1, formatter, obj):
        # Sort by reverse string
        return value1[::-1]
    
    # ####################### #
    #   Convenience Methods   #
    # ####################### #  
    def _MoveSelectedElementTo(self, toList):
        fromList = self._GetOppositeListAttribute(toList)
        element = self._GetSelectedElementInList(fromList)
        if element != None:
            index = getattr(self, fromList).IndexOfFirstEqual(element)
            if index != -1:
                getattr(self, fromList).RemoveAt(index)
                getattr(self, toList).Add(element)
        self._selected['right'] = None
        self._selected['left'] = None
    
    def _GetOppositeListAttribute(self, attrName):
        return 'right' if attrName == 'left' else 'left'
    
    def _GetSelectedElementInList(self, listName):
        return self._selected.get(listName, None)
