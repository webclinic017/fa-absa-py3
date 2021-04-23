import acm
import FUxCore
  
def UnpackInitialData(params):
    initalData = None
    if params:
        initalData = params.At('initialData')
    
    return initalData

def UnpackNamedParameters(ael_custom_dialog_mainParameters):
    if ael_custom_dialog_mainParameters:
        return ael_custom_dialog_mainParameters['namedParameters']
    return None

"""
Helper method for creating a named parameter GUI.

@params:
parameterDefinition is a string of the format "name1,domain1[,displayName1,uniqueIdMethod1,description1];name2,domain2[,displayName2,uniqueIdMethod2,description2]"
commonParametersDefinition is an optional string of the formation "name1,domain1[,displayName1,defaultValue1,description1];name2,domain2[,displayName2,defaultValue2,description2];

"""
def ShowNamedParametersDlg( shell, ael_custom_dialog_showParams, parametersDefinition, commonParametersDefinition = "" ):
    editParameters = None
    initData = UnpackInitialData( ael_custom_dialog_showParams )
    if( initData ):
        editParameters = initData.At( 'namedParameters' )
    
    editParameters = acm.UX().Dialogs().CreateNamedParametersVector( shell, parametersDefinition, editParameters, None, "", "", commonParametersDefinition )
    if editParameters:
        resultDict = acm.FDictionary()
        resultDict.AtPut( 'namedParameters', editParameters )
        return resultDict    
    return None


'''
Show a dialog to a short text from the user 
'''

def ShowGetShortTextDialog(shell, caption, label, initialText, maxLength=-1, checkAlphaNum=False, names = None):
    customDlg = GetShortTextDlg()
    customDlg.m_caption = caption
    customDlg.m_label = label
    customDlg.m_initialText = initialText
    customDlg.m_maxLength = maxLength
    customDlg.m_checkAlphaNum = checkAlphaNum
    customDlg.m_names = names

    builder = customDlg.CreateLayout()
    
    text = None
    if acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customDlg ) :
        text = customDlg.m_text
        
    return text
    


    
class GetShortTextDlg (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_okButton = 0
        self.m_edit = 0
        self.m_initialText = ''
        self.m_text = ''
        self.m_label = ''
        self.m_caption = 'Input'
        self.m_maxLength = -1
        self.m_checkAlphaNum = False
        self.m_names = None
        
    def HandleApply( self ):
        ret = True
        s = self.m_edit.GetData()

        if self.m_checkAlphaNum :
            s = s
            if not s.isalnum():
                s = [x for x in s if x.isalnum() or x == '_'] 
                s = s.lstrip('0123456789')


        if self.m_names != None:
            if s in self.m_names :
                acm.UX().Dialogs().MessageBoxInformation(self.m_fuxDlg.Shell(), 'The name ' + s + ' is already used, please select another name')
                self.m_edit.SetFocus()
                self.m_edit.SetTextSelection(0, -1)


                ret = None

        self.m_text = s

        return ret

    def OnEditChanged(self, ud, cd):
        self.UpdateControls()
        
    def UpdateControls(self) :
        self.m_okButton.Enabled(len(self.m_edit.GetData()) > 0)
    
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.m_caption)
        self.m_okButton = layout.GetControl('ok')
        self.m_edit = layout.GetControl('editCtrl')
        
        self.m_edit.AddCallback( 'Changed', self.OnEditChanged, self )

        self.m_edit.SetData(self.m_initialText)
        self.m_edit.SetTextSelection(0, -1)
        
        if self.m_maxLength != -1 :
            self.m_edit.MaxTextLength(self.m_maxLength)

        self.UpdateControls()

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  AddInput('editCtrl', self.m_label, 50)
        b.  AddSpace(10)
        b.  BeginHorzBox()
        b.          AddFill()
        b.          AddButton('ok', 'OK')
        b.          AddButton('cancel', 'Cancel')
        b.  EndBox()    
        b.EndBox()
        return b


