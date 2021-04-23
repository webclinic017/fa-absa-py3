"""
    PackageInsertItems
    
    (C)2012-2018 FIS Front Arena
    
    Return dependents
    
    20120522 Richard Ludwig
    
"""
import acm
import FUxCore
import PackageExportAMBA


def OnOpenClicked(self, cd ):
    PackageExportAMBA.ExportCommonObject(self.Shell(), self.selection, package = None, follow=self.m_follow.Checked())
    
    
class MyInsertItemsPanel (FUxCore.LayoutPanel):
    def __init__(self):
        pass

    def UpdateControls(self):
        self.selection = self.Owner().Selection()
        self.m_selectedCount.SetData(self.selection.Size() )
        self.m_export.Enabled(self.selection.Size() > 0)

    def ServerUpdate(self, sender, aspect, parameter ):
        if str(aspect) == str('SelectionChanged'):
            self.UpdateControls()
    
    def HandleCreate( self):
        layout = self.SetLayout(self.BuildLayout())

        self.m_export = layout.GetControl('buttonExport')
        self.m_export.AddCallback( "Activate", OnOpenClicked, self )

        self.m_selectedCount = layout.GetControl('selectedCount')
        self.m_selectedCount.Editable(False)

        self.m_follow = layout.GetControl('followDependents')
        
        self.Owner().AddDependent(self)
        self.UpdateControls()

    def BuildLayout( self):
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('EtchedIn', 'AMBA Packager')
        b.  AddInput('selectedCount', 'Selected items', 5, 6)
        b.  AddFill()
        b.  AddCheckbox('followDependents', 'Add dependents')
        b.  AddButton('buttonExport', 'Export...')
        b.EndBox()
        return b

"""
def AddSubClasses( cls, arr ):
    for subClass in cls.Subclasses():
        if cls.IsEqual( acm.FInstrument ) or not cls.IncludesBehavior( acm.FInstrument ):
            arr.Add(subClass)
            AddSubClasses(subClass, arr )
"""

def AddSubClasses( cls, arr ):
    """ Only Add classes which is not "owned" by another class 
        e.g. YieldCurve -> YieldCurvePoint, only YieldCurve added
    """
    for subClass in cls.Subclasses():
        if subClass.PartOfAttribute() == None:
            if (cls.IsEqual( acm.FInstrument ) or not cls.IncludesBehavior( acm.FInstrument )):
                if str(subClass.InstanceStorage() ) == 'pom':
                    # Only add if class is stored in database
                    arr.Add(subClass)
                AddSubClasses(subClass, arr )


def StartIIExtendedCB(eii):
    arr = acm.FArray()
    AddSubClasses( acm.FCommonObject, arr )
    arr.SortByProperty('StringKey', True)
    customPanel = MyInsertItemsPanel()
    acm.StartFASQLEditor( 'AMBA Packager', arr, None, None, None, '', False, customPanel, False, None, False )

#caption, providers, storedQuery, query, ownerFrame, ownerKey, autoInitialSearch, customLayoutPanel,useArchivedMode, nameOfFExtensionValueDefiningDefaultQuery, realTime 

