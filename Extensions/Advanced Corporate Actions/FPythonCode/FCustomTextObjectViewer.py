""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCustomTextObjectViewer.py"
"""----------------------------------------------------------------------------
MODULE

    FCustomTextObjectViewer.py - Custom dialog for custom text objects.

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import acm
import ael
import string
import FUxCore


class FCustomTextObjectViewer(FUxCore.LayoutDialog):
    CAPTION = 'Source Record'

    def __init__(self, params):
        if params['selected']:
            textObject = params['selected'][0]
            text = textObject.Text().split(',')
            self.sourceTxt = '\n'.join(text)

    def HandleApply(self):
        resultDic = acm.FDictionary()
        return resultDic

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.CAPTION)
        self.m_currentNodeText = layout.GetControl("current_node_text")
        self.m_currentNodeText.Editable(False)
        self.m_currentNodeText.SetStandardFont('Monospace')
        self.sourceTxt
        self.m_currentNodeText.SetData(self.sourceTxt)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginVertBox('None')
        b.   AddText('current_node_text', 400, 300)
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b
