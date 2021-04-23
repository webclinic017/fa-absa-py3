import acm, FUxCore, math, StiwUtils
from StiwQuoteRequestSubscriber import QuoteRequestSubscriber
from RFQHistoryUtil import FromRequest
from RFQUtils import Status

class StiwNotifyUserOnQuoteRequestUpdate(object):   
    def __init__(self, owner):
        self.quoteRequestSubscriber = QuoteRequestSubscriber(owner, self.QueryFilter, self.StatusFilter)       
        self.statuses = []
    
    def QueryFilter(self):
        query = None
        userName = acm.User()
        role = StiwUtils.GetNotificationSetting('Role')
        query = acm.CreateFASQLQuery(acm.FQuoteRequestInfo, 'AND')
        query.AddAttrNode('Role', 'EQUAL', 'Trading') # Should always be 'Trading'
        if role == 'Trading':
            op = query.AddOpNode('OR')
            op.AddAttrNode('ToBrokerId', 'EQUAL', userName)
            op.AddAttrNode('ToBrokerId', 'EQUAL', '')
        elif role == 'Sales':
            query.AddAttrNode('FromBrokerId', 'EQUAL', userName)
        return query

    def StatusFilter(self, quoteRequest, aspect):
        return FromRequest.StatusName(quoteRequest) in self.statuses
    
    def Statuses(self, value=None):
        if value is None:
            return self.statuses
        else:
            if (value and not self.statuses) or (not value and self.statuses):
                self.ToggleEnabled()
            self.statuses = value
    
    def ToggleEnabled(self):
        self.quoteRequestSubscriber.ToggleEnabled()

def OnClear(self, cd):
    for ctrl in self.m_controls:
        ctrl.Checked(False)


class FilterSelectionDlg(FUxCore.LayoutDialog):
    
    def __init__(self, statuses):
        self.m_statuses = [['field%s'%(i), name, name in statuses] for i, name in enumerate(Status.PingPongChoices())]
        self.m_controls = []
    
    def HandleApply( self ):
        result = []
        for ctrl in self.m_controls:
            if ctrl.Checked():
                result.append(ctrl.Label())
        return result
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Select Notifications')
        self.m_clear = layout.GetControl('clear')
        for setting in self.m_statuses:
            ctrl = layout.GetControl(setting[0])
            if setting[2]:
                ctrl.Checked(True)
            self.m_controls.append(ctrl)
            
        self.m_clear.AddCallback( "Activate", OnClear, self )
    
    def CreateLayout(self):
        columns = 3.0
        splitAt = math.ceil(len(self.m_statuses)/columns)
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginHorzBox('None')
        b.    BeginVertBox('None')
        for i, s in enumerate(self.m_statuses):
            if i%splitAt == 0:
                b.EndBox()
                b.BeginVertBox('None')
            b.  AddCheckbox(s[0], s[1])
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('clear', 'Clear')
        b.    AddButton('ok', 'Close')
        b.  EndBox()
        b.EndBox()
        return b
            
