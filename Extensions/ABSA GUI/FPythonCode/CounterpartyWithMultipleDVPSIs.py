"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    CounterpartyWithMultipleDVPSIs
    
DESCRIPTION
    This module contains code to show a custom gui to choose SSI when there are multiple DVP SSIs present on counterparty

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-11      FAOPS-42       Sadanand Upase           Rayan Govender          Initial Implementation
2018-11-14      FAOPS-42       Jaysen Naicker           		            	Fix bug on in get_difference() method
2020-12-22      FAOPS-1022     Ncediso Nkambule         Kgomostso               Added Client party type to the party type check on the module
-----------------------------------------------------------------------------------------------------------------------------------------
"""


import acm

import FUxCore

class SelectSSIDialog (FUxCore.LayoutDialog):
    def __init__(self, trade, system_si, eligible_si):
        self.m_okBtn = 0
        self.m_ssiLabel = 0
        self.m_ssi = 0
        self.m_system_si = system_si
        self.m_eligible_si = eligible_si
        self.trade=trade
        
    def PopulateData(self):
        for si in self.m_eligible_si:
            self.m_ssi.AddItem(si)
        self.m_ssi.SetData(self.m_system_si)
        self.m_ssiLabel.SetData("Counterparty has multiple SSIs, select the appropriate instruction:")
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('Select Settlement Instruction ')
        self.m_ssiLabel = layout.GetControl("ssiLabel")
        self.m_ssi = layout.GetControl("ssi")
        self.m_okBtn = layout.GetControl("ok")
        self.m_okBtn.AddCallback( "Activate", on_ok_clicked, self )
        self.PopulateData()
        
def create_layout():
    b = acm.FUxLayoutBuilder()
    #b.BeginVertBox('None')
    b.  BeginVertBox('None')
    b.    BeginHorzBox('None')
    #The icon does not show up
    #b.      BeginVertBox('None')
    #b.        AddIcon('Warning')
    #b.      EndBox()
    b.      BeginVertBox('EtchedIn', '')
    b.        AddLabel('ssiLabel', 'Note', 200, 200)
    b.        AddOption('ssi', 'Settlement Instruction', 50, 50)
    b.      EndBox()    
    b.    EndBox()
    b.    BeginHorzBox('None')
    b.          AddSpace(150)
    b.          AddButton('ok', 'OK')
    b.    EndBox()
    b.  EndBox()
    return b

def on_ok_clicked(dlg_obj, x):
    ssi_selected = dlg_obj.m_ssi.GetData()
    #Avoiding to create trade account link when user selectes the same SSI that system chose
    if dlg_obj.m_system_si == ssi_selected:
        return
    cp = dlg_obj.trade.Counterparty()
    for si in cp.SettleInstructions():
        if si.Name() == str(ssi_selected):
            selected_si = si
            break
    
    set_trade_account_link(dlg_obj.trade, ['Security Nominal', 'End Security'], 'Delivery versus Payment', selected_si)    



def show_dvp_choosing_gui(shell, trade, system_si, eligbile_si):
    builder = create_layout()
    custom_dlg = SelectSSIDialog(trade, system_si, eligbile_si)
    custom_dlg.m_count = 0
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, custom_dlg)



def set_trade_account_link(trade, cf_type, delivery_type, si):
    if not trade.AccountLinks():
        end_security_present = False
        for mf in trade.MoneyFlows():
            if mf.Type() == 'End Security':
                end_security_present = True
                break
        for each_cf_type in cf_type:
            #Skipping generation of TradeAccountLink for End Security if money flow of that type is not present.
            if each_cf_type == 'End Security' and not end_security_present:
                continue
            ta = acm.FTradeAccountLink()
            ta.PartyType('Counterparty')
            ta.SecSettleCashFlowType(each_cf_type)
            ta.SettleDeliveryType(delivery_type)
            ta.SettleInstruction(si)
            ta.Trade(trade)
            ta.Commit()
        return

    for ta in trade.AccountLinks():
        if  ta.PartyType() in ['Counterparty', 'Client'] and \
            ta.SecSettleCashFlowType() in cf_type and \
            ta.SettleDeliveryType() == delivery_type:
            acm.BeginTransaction()
            ta.SettleInstruction(si)
            ta.Commit()
            acm.CommitTransaction()


def get_eligible_settlement_instructions(trade, party):
    sett_inst = []
    for si in party.SettleInstructions():
        if si.SettleDeliveryType() == acm.FString('Delivery versus Payment') or  si.Type() == acm.FString('Security'):
            if si.QueryAttributeCurrency() == '' or str(trade.Currency().Name()) in str(si.QueryAttributeCurrency()): 
                sett_inst.append(si.Name()) 
    return sett_inst
    
def to_string(o):
    return "%s" % (o.StringKey() if hasattr(o, 'Class') else str(o))

def get_difference(org_obj, modified_obj):
    return org_obj.Difference(modified_obj, False, 1)

def get_dvp_moneyflow_from_trade(trade):
    for mf in trade.MoneyFlows():
        if mf.Type() == 'Security Nominal':
            return mf
    return None

def validate_and_show_ssi_choosing_gui(shell, params):
    data = params.At('initialData')
    modified_object = data.At('editObject')
    original_object = data.At('originalObject')
    type = modified_object.RecordType()
    if type == 'Trade':
        #For a new trade counterparty is chosen and hence chounterparty_changed flag will be by default true.
        counterparty_changed = True
        #original_object is present when trade is being modified
        if original_object:
            #checking id FDifference object if the counterparty is being changed.
            diff = get_difference(original_object, modified_object)
            if 'counterparty' not in [to_string(each) for each in diff.Keys()]:
                counterparty_changed = False
        if counterparty_changed and modified_object.SettleCategoryChlItem() and modified_object.SettleCategoryChlItem().Name() == 'Euroclear':
            trade = modified_object
            cpty = trade.Counterparty()
            mf = get_dvp_moneyflow_from_trade(trade)
            if mf and mf.CounterpartySettleInstruction():
                default_si = mf.CounterpartySettleInstruction().Name()
                eligible_si = get_eligible_settlement_instructions(trade, cpty)
                if default_si and len(eligible_si) > 1:
                    show_dvp_choosing_gui(shell, trade, default_si, eligible_si)
    
    return params



'''def ael_custom_dialog_show(shell, params):
    

def ael_custom_dialog_main(_parameters, dict_extra):
    return dict_extra'''
