'''
MODULE
    CommUtilFeeUI - This module prvoides Commitment fees details
   
HISTORY
    Date        Developer               Notes
    2017-10-09  Ntuthuko Matthews       created
'''


from acm import FUxLayoutBuilder


def CommUtilFeePane(cls):
    b = FUxLayoutBuilder() 
    b.BeginVertBox('None')
    b.AddSpace(5)
    b. BeginVertBox('None')
    b.    BeginHorzBox('None')
    cls.txtTradeNumberCtrl.BuildLayoutPart(b, 'Trade Number')
    b.      AddButton('btnInsertItems', '...', False, True)
    b.    EndBox()
    cls.cboCalcFeeTypeCtrl.BuildLayoutPart(b, 'Calculate Fee Type*')
    b.  AddCheckbox('chkCalcCommFeeCtrl', 'Calculate Comm Fee*')
    b.  AddCheckbox('chkCalcUtilFeeCtrl', 'Calculate Utilization Fee*')
    b.  AddCheckbox('chkLinkedCtrl', 'Credit Linked & Financial Covenant Linked*')
    cls.txtFacilityMaxCtrl.BuildLayoutPart(b, 'Facility Limit*')
    cls.txtThresholdCtrl.BuildLayoutPart(b, 'Threshold (0<x<1)*')
    cls.txtCommitFeeRateCtrl.BuildLayoutPart(b, 'Comm Fee Rate (%)*')
    cls.txtFacilityExpiryCtrl.BuildLayoutPart(b, 'Facility Expiry (dd/mm/yyyy)*')
    cls.txtCommitFeeBaseCtrl.BuildLayoutPart(b, 'Rolling Base Day (dd/mm/yyyy)*')
    cls.cboCommitPeriodCtrl.BuildLayoutPart(b, 'Rolling Period*')
    cls.cboRollingConventionCtrl.BuildLayoutPart(b, 'Rolling Convention*')
    cls.cboDayCountCtrl.BuildLayoutPart(b, 'Day Count')
    b.  AddCheckbox('chkCopyCtrl', 'Copy Commitment Fee Details')
    b. EndBox() 
    b. BeginVertBox()
    b.  AddLabel('lblline', '_'*75)
    b.  AddLabel('lblMandatoryFields', '* indicates mandatory field')
    b.  AddLabel('lblMessageCtrl', '', 75, 75)       
    b. EndBox()
    b.EndBox()
    
    return b
