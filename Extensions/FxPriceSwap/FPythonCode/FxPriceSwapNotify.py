
import FUxCore
import acm, ael

class FxPriceSwapNotify(FUxCore.LayoutDialog):

    def __init__(self, createEvents, action):
        self.createEvents = createEvents
        self.action = action

    def HandleApply( self ):
        return True

    def CreateLayout(self):
            b = acm.FUxLayoutBuilder()
            b.BeginVertBox()
            b.      AddLabel("label1", "Action the following ## Exotic Events")
            b.      AddLabel("label2", " of type \"Fx Rate\"?")
            b. AddSpace(8)
            b.      AddList("datesList", 20, -1, 20, -1) 
            b. AddSpace(8)
            b.  BeginHorzBox()
            b. AddSpace(4)
            b.    AddButton("ok", "OK", 1, 0)
            b. AddSpace(4)
            b.    AddButton("cancel", "Cancel", 1, 0)
            b.  EndBox()
            b.  EndBox()
            return b
            
    def HandleCreatePR( self, dlg, layout):
        self.dlg = dlg
        
        self.m_label1 = layout.GetControl("label1")
        self.m_label1.SetData("%s the following %s Exotic Events" % (self.action, len(self.createEvents)))
        
        self.m_datesList = layout.GetControl("datesList")
        
        dates = self.createEvents.keys()
        dates.sort()
        for i, date in enumerate(dates):
            self.m_datesList.AddItem("%s" % (str(date)))
        
    def HandleCreate( self, dlg, layout):
        try:
            self.HandleCreatePR(dlg, layout)
        except Exception, e:
            print "exception", e
            import traceback
            traceback.print_exc()

