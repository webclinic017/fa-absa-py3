
import FUxUtils
import FUxCore
import acm

from ColumnParameterization import ColumnParameterizationDialog
from ColumnParameterization import CustomFieldInfo

def OnStoredASQLJournalQuery(self, ad):
    query = acm.UX().Dialogs().SelectStoredASQLQuery(self.m_parent.m_fuxDlg.Shell(), acm.FJournal, self.m_value)
    if query:
        self.m_value = query
        self.m_objectText.SetData( query.Name() )

class StoredASQLJournalQueryFieldInfo( CustomFieldInfo ):
    
    def __init__(self, parent, columnParameterDefinition, populator, is_mandatory, counter):
        CustomFieldInfo.__init__( self, parent, columnParameterDefinition, populator, is_mandatory, counter )
        
    def Init(self, layout, initialValues):
        CustomFieldInfo.Init( self, layout, initialValues )
        self.m_objectBtn.AddCallback( "Activate", OnStoredASQLJournalQuery, self )

class AccountingReportParameterizationDialog(ColumnParameterizationDialog):
        
    def _customFieldInfo( self, colParam, is_mandatory, counter ):
        fieldInfo = None
        if colParam.ParameterDomain() == acm.FStoredASQLQuery:
            fieldInfo = StoredASQLJournalQueryFieldInfo( self, colParam, None, is_mandatory, counter )
        
        return fieldInfo
        

def ael_custom_dialog_show(shell, params):
    dlg = AccountingReportParameterizationDialog(FUxUtils.UnpackInitialData(params))
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)
    
    
def ael_custom_dialog_main(parameters, dictExtra):
    return parameters
