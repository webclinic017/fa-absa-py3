from __future__ import print_function
import itertools
import string
import acm
import FUxCore

import RiskFactorUtils


def Show(shell, fields, name = '') :
    dlg = EditDialog( fields, name )
    dlg.InitControls()
        
    return acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg) 

class EditField :
    def __init__(self, name, label, domain, value, choices = None) :
        self.m_name = name
        self.m_label = label
        self.m_domain = domain
        self.m_value = value
        self.m_choices = choices


class EditDialog( FUxCore.LayoutDialog ):
    
    def __init__(self, fields, name = ''):
        self.m_fields = fields
        self.m_bindings = None
        self.m_binders = {}
        self.m_name = name
        
    def CreateToolTip(self):
        pass
        
    def HandleCreate( self, dlg, layout ):
        self.m_fuxDlg = dlg
        if self.m_name:
            self.m_fuxDlg.Caption( self.m_name )

        for field in self.m_fields:
            binder = self.m_binders[ field.m_name ]
            binder.InitLayout( layout )
            binder.Label(field.m_label)

            try:
                val = field.m_value
                if val:
                    binder.SetValue( val )

            except Exception as e:
                print (e)

    def ValueAsString(self, value) :
        if isinstance(value, type(True)) :
            value = 'Yes' if value else 'No'

        return value


    def InitControls(self):
        self.m_bindings = acm.FUxDataBindings()
        self.m_bindings.AddDependent( self )
        
        for field in self.m_fields :
            binder = self.m_bindings.AddBinder( field.m_name, field.m_domain, None, field.m_choices, False, True, 30 )
            self.m_binders[field.m_name] = binder
            
    def HandleApply(self):
        values = {}
        for field in self.m_fields :
            binder = self.m_binders[ field.m_name ]
            try:
                val = binder.GetValue()
                values[field.m_name] = self.ValueAsString(val)

            except Exception as e:
                print (e)

        return values

            
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  BeginVertBox('Invisible')
        for field in self.m_fields:
            binder = self.m_binders[field.m_name]
            binder.BuildLayoutPart( b, field.m_name )
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'OK')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b
