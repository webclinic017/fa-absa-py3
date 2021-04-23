"""PURPOSE                 :  Functions that are used for Front End UI validation of SBL Ahency desk
DEPARTMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Candice Johnson, Thulsie Gasant
DEVELOPER               :  Andreas Bayer
CR NUMBER               :  

History:

Date            CR Number       Who                      What

2014-03-28                      Andreas Bayer           Added the module to introcude the UI Validation 
                                                        that is required to default CP Portfolio for certain Portfolios 
                                                        select with SBL AGENCYI/DESK as counterparty
2020-07-08      PCGDEV-508      James Stevens           Added rule to bypass mirror GUI validation for closing trades
-----------------------------------------------------------------------------"""



import acm
import FUxCore
import FUxUtils
import string
import ael
import sl_functions

RELEVANT_COUNTERPARTIES = [
    acm.FParty['SBL AGENCY I/DESK']
]

'''###############################################################################
# 
# FUx Error Dialog UI Class
#
###############################################################################'''

class SecLoanValidationCustomDialog (FUxCore.LayoutDialog):
    def __init__(self):
        self.m_bindings = None
        self.m_okBtn = None
        self.m_initData = None
        self.m_changeString = None
        self.m_infoText = None
        
    def HandleApply( self ):
        return 1
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        self.UpdateControls()
    
    def UpdateControls(self):
        pass
        
    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption('SecLoan GUI Validation Failed')
        self.m_okBtn = layout.GetControl("ok")
        self.m_infoText = layout.GetControl("infoText")
        self.m_infoText.AppendText(self.m_changeString)
        self.m_infoText.Editable(False)
        self.UpdateControls()
        
    def InitControls(self, diffText):
        self.m_changeString = diffText
    
    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.  AddText('infoText', 400, 150)
        b.  BeginHorzBox('None')
        b.    AddFill()
        b.    AddButton('ok', 'Ok')
        b.  EndBox()
        b.EndBox()
        return b

'''###############################################################################
# 
# Validation Helper Functions
#
###############################################################################'''

def is_relevant_sec_loan(trade):
    instr = trade.Instrument()
    res = False
    msg = []
    
  
    '''###############################################################################
    #  Validation has to performed if Instrument Type is Security Loan, Counterpart
    #  SBL AGENCY I/DESK, and if the trade is booked in a Portfolio that have CP_Portfolio 
    #  Additional info populated. This additional info indicates the portfolio in mich the mirro trades has to be booked.
    #
    ###############################################################################'''
    
    
    
    
    if (trade.Counterparty().Oid() in [elem.Oid() for elem in RELEVANT_COUNTERPARTIES]):
        if (instr.InsType() == 'SecurityLoan' and 
            trade.Counterparty().Type() == 'Intern Dept' and 
            trade.Portfolio().AdditionalInfo().CP_Portfolio() and
            acm.FPhysicalPortfolio[trade.Portfolio().AdditionalInfo().CP_Portfolio()] and 
            not trade.Type() == "Closing"): 
            res = True
            if(not (trade.MirrorTrade() or trade.Type() == "Closing")):
                msg.append('Please select a CP Portfolio.')
        
    return res, msg
    
    
    
    
def _delete_add_info(field_name, recaddr):
    ''''delete additional info object
    '''
    ai_spec = acm.FAdditionalInfoSpec.Select01(
        'fieldName = "%s"' % field_name, '')
    add_info = acm.FAdditionalInfo.Select01(
        'recaddr = %s addInf = %s' % (
            recaddr, ai_spec.Oid()),
        '')
    if add_info:
        add_info.Delete()       

def field_validation(trade):
    valid = True
    msg = []
    #Global One Field Validation:
    if not trade.AdditionalInfo().SL_G1Counterparty1():
        msg.append('Please select a Global One Borrower.')
        valid = False
    if not trade.AdditionalInfo().SL_G1Counterparty2():
        msg.append('Please select a Global One Fund/Lender.')
        valid = False
    return valid, msg

def check_mirror(trade):
    valid = True
    msg = []
    if not trade.MirrorTrade():
        valid = False
    return valid, msg

        
    
    return valid, msg
    
def amend_trade(trade):
    mirror_trade = trade.MirrorTrade()
    portf = acm.FPhysicalPortfolio[trade.Portfolio().AdditionalInfo().CP_Portfolio()]
    acm.BeginTransaction()
    try:
        portfs = acm.FPhysicalPortfolio.Select('')
        #mirror_trade.Portfolio(portfs.At(0))
        #mirror_trade.Commit()
        mirror_trade.Portfolio(portf)
        mirror_trade.Commit()
        acm.CommitTransaction()
    except Exception, e:
        print e
        acm.AbortTransaction()

'''###############################################################################
# 
# Validation entry point
#
###############################################################################'''

def ael_custom_dialog_show(shell, params):
    try:
        callData = params['initialData']
        if not callData:
            return None
            
        trade = callData.At('editObject')
        relevant, msg = is_relevant_sec_loan(trade)

        if relevant:

            if len(msg) > 0:
                customDlg = SecLoanValidationCustomDialog()
                customDlg.InitControls( string.join(msg, '\n') )
                acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg )
                
            valid, msg = check_mirror(trade)
            if not valid:
                #customDlg = SecLoanValidationCustomDialog()
                #customDlg.InitControls( string.join(msg, '\n') )
                #acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg )
                return None
                
            valid, msg = field_validation(trade)
            if not valid:
                customDlg = SecLoanValidationCustomDialog()
                customDlg.InitControls( string.join(msg, '\n') )
                acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg )
                return None
            amend_trade(trade)
            mirror_trade = trade.MirrorTrade()

            _delete_add_info('SL_G1Counterparty1', mirror_trade.Oid())
            _delete_add_info('SL_G1Counterparty2', mirror_trade.Oid())
            _delete_add_info('SL_G1Fee2', mirror_trade.Oid())

    except Exception, e:
        print 'dbg2', e       
    # Return parameters
    returnParameters = acm.FDictionary()
    return returnParameters
        
def ael_custom_dialog_main( parameters, dictExtra ):
    # not used for validation
    return dictExtra
