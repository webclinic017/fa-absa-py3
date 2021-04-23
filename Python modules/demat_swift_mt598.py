'''-----------------------------------------------------------------------------
PROJECT                 : Markets Message Gateway
PURPOSE                 : SWIFT MT598 message definition
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               : Rohan van der Walt
CR NUMBER               : CHNG0003744247 (2016-08-19)
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date            Change no       Developer       Description
--------------------------------------------------------------------------------
2016-08-23      CHNG0003898744  Manan Ghosh     Changed to use prod header settings
2016-12-06                      Willie vd Bank  Added a lookup to demat_config for field 108
2017-12-11      CHNG0005220511  Manan Ghosh     DIS go-live
'''

import at_addInfo
import time
import demat_config
from gen_swift_mt_messages import MtMessageBase
from gen_swift_mt_blocks import Body
from gen_swift_mt_fields import *
from datetime import datetime
from gen_absa_xml_config_settings import SwiftParamXmlConfig
from gen_absa_xml_config_settings import AbsaXmlConfigSettings  

MANDATORY = True
OPTIONAL = False
SINGLE = False
MULTIPLE = True

#Constants
ABSA_SWIFT_NODE = 'AbcapSwiftParameters'
STRATE_SWIFT_NODE = 'StrateSwiftParameters'

class ISSU_Mt598(MtMessageBase):
    def __init__(self):
        MtMessageBase.__init__(self)
        self.ApplicationHeader.MessageType = 598
        
        self._body = Body([
            MtField20('TransactionReference', MANDATORY),
            MtField12('SubMessageType', MANDATORY),             #2
            MtField77E('ProprietaryMessage', MANDATORY),        #3
            MtField16R('StartOfBlock_General', MANDATORY, 'GENL'),      #4
                MtField23G('MessageFunction', MANDATORY),                #5
                MtField98C('PreparationDate', MANDATORY, 'PREP'),         #6
                MtField22F('InstructionType', MANDATORY, 'INST'),         #7
            MtField16S('EndOfBlock_General', MANDATORY, 'GENL'),         #8
            MtField16R('StartOfBlock_MMID', MANDATORY, 'MMID'),         #9
                MtField95R('IssuerCSDParticipant', MANDATORY, 'CSDP'),   #10
                MtField95R('IssuerParticipantCode', MANDATORY, 'ISSR'),  #11     
                MtField95R('AgentParticipantCode', MANDATORY, 'ISSA'),   #12
                MtField35B_MT598('SecuritiesIdentifierISSU', OPTIONAL),    #13 - ISSU only
                MtField36B('Nominal', MANDATORY, 'QISS'),                #14
                MtField97B('IssuerSORAccount', MANDATORY, 'SAFE'),       #15
                MtField16R('StartOfBlock_Instrument', OPTIONAL, 'FIA'), #16
                    MtField22F('CouponFrequency', OPTIONAL, 'PFRE'),     #17
                    MtField13B('CouponPaymentDay', OPTIONAL, 'CPYD'),    #18
                    MtField13B('CouponPaymentCycle', OPTIONAL, 'CCYC'),   #19
                    MtField12A('GenericCategory', OPTIONAL, 'CATG'),     #20
                    MtField22H('MMSecurityType', OPTIONAL, 'TYPE'),      #21
                    MtField98A('MaturityDate', OPTIONAL, 'MATU'),        #22
                    MtField98A('IssueDate', OPTIONAL, 'ISSU'),           #23
                    MtField92A_MT598('InterestRate', OPTIONAL, 'INTR'),   #24 - Only present for CAT2 ie CD instruments
                    MtField22F('RateType', OPTIONAL, 'RTYP'),            #25
                    MtField36B('MinimumNominalAmount', OPTIONAL, 'MINO'),#26 - Minimum tradable denomination
                    MtField36B('AuthorisedAmount', OPTIONAL, 'AUTH'),    #27
                    MtField36B('MinimumIssueAmount', OPTIONAL, 'MINI'),  #29 - Minimum issue denomination
                    MtField17B('WithholdingTaxOnInterest', OPTIONAL, 'WITI'), #32 - ... Y/N
                    MtField92A_MT598('TaxRate', OPTIONAL, 'TAXR'), #32 - ... //[N]15d
                    MtField17B('FinalCouponPaymentIndicator', OPTIONAL, 'FCPM'), #34 - Coupon payment on Maturity ... Y/N
                    MtField17B('CouponPaymentIndicator', OPTIONAL, 'CPMI'),      #35 - Coupons disbursed through CSD? Y/N
                    MtField17B('AutomatedCouponPaymentCalculation', OPTIONAL, 'ACPC'),     #36 - Coupon payment calculation must be done by CSD? Y/N
                    MtField17B('AutomatedCouponPaymentOnly', OPTIONAL, 'ACPO'),  #37 - Calculation done by Issuer, CSD only pays coupon
                    MtField17B('OverrideIndicator', OPTIONAL, 'OVER'), #39 - Y/N
                    MtField13B('CouponPaymentCalculationMethod', OPTIONAL, 'CPCM'), #40 - Must be present for CAT 2 & 3 if ACPC (automated coupon payment) is Y. Valid Values are 1, 2, 3 This field must be 3 for Category 3
                    MtField14F('CouponRateSource', OPTIONAL, ''),   #41 
                    MtField25('CouponRateVarianceFromSource', OPTIONAL),   #42
                    MtField22F('CouponCompoundingFrequency', OPTIONAL, 'CCFR'), #43 - Only for generic CAT3 (FRN) instruments
                    MtField22F('CouponResetFrequency', OPTIONAL, 'RESF'),       #44
                    MtField98A('CouponResetStartDate', OPTIONAL, 'CRSD'),       #45 - Only for generic CAT3 (FRN) instruments
                    MtField16R('StartOfBlock_CRDDET', OPTIONAL, 'CRDDET'),
                    RepetitiveSequence('CouponResetDateDetails', [
                        MtField98A('ResetDate', OPTIONAL, 'RESD'),
                    ], OPTIONAL),
                    MtField16S('EndOfBlock_CRDDET', OPTIONAL, 'CRDDET'),
                    MtField16R('StartOfBlock_CPDDET', OPTIONAL, 'CPDDET'),
                    RepetitiveSequence('CouponPaymentDateDetails', [
                        MtField98A('PayDate', OPTIONAL, 'PAYD'),
                    ], OPTIONAL),
                    MtField16S('EndOfBlock_CPDDET', OPTIONAL, 'CPDDET'),                    
                MtField16S('EndOfBlock_Instrument', OPTIONAL, 'FIA'),
            MtField16S('EndOfBlock_MMID', MANDATORY, 'MMID')
            

        ])
        
class nonISSU_Mt598(MtMessageBase):     #TOPU/REDU/DISS actions only
    def __init__(self):
        MtMessageBase.__init__(self)
        self.ApplicationHeader.MessageType = 598
        self._body = Body([
            MtField20('TransactionReference', MANDATORY),
            MtField12('SubMessageType', MANDATORY),             #2
            MtField77E('ProprietaryMessage', MANDATORY),        #3
            MtField16R('StartOfBlock_General', MANDATORY, 'GENL'),      #4
                MtField23G('MessageFunction', MANDATORY),                #5
                MtField98C('PreparationDate', MANDATORY, 'PREP'),         #6
                MtField22F('InstructionType', MANDATORY, 'INST'),         #7
            MtField16S('EndOfBlock_General', MANDATORY, 'GENL'),         #8
            MtField16R('StartOfBlock_MMID', MANDATORY, 'MMID'),         #9
                MtField95R('IssuerCSDParticipant', MANDATORY, 'CSDP'),   #10
                MtField95R('IssuerParticipantCode', MANDATORY, 'ISSR'),  #11     
                MtField95R('AgentParticipantCode', MANDATORY, 'ISSA'),   #12
                MtField35B('SecuritiesIdentifier', OPTIONAL),          #13 - TOPU, REDU, Deissue
                MtField36B('Nominal', MANDATORY, 'QISS'),                #14
                MtField97B('IssuerSORAccount', MANDATORY, 'SAFE'),       #15
                MtField97A_MT598('IssuerCSAAccount', OPTIONAL, 'SAFE'),       #16
            MtField16S('EndOfBlock_MMID', MANDATORY, 'MMID')
        ])
        
INS_CATEGORY = {'FRN':('CATG3', 'FRNX'),
                'LNCD':('CATG3', 'LNCD'),
                'CLN':('CATG3', 'CLNX'),
                'NCD':('CATG2', 'NCDX'),
                'NCC':('CATG2', 'NCDX'),
                'PN':('CATG2', 'PNXX'),
                'BOND':('CATG2', 'BOND'),
                'NOTX':('CATG2', 'NOTX')
                }
                
REFERENCE_INDEX = {'ZAR-JIBAR-1M': ('JIBAR1', 'J01XXXX'),
                   'ZAR-JIBAR-3M': ('JIBAR3', 'J03XXXX'),
                   'ZAR-JIBAR-6M': ('JIBAR6', 'J06XXXX'),
                   'ZAR-JIBAR-9M': ('JIBAR9', 'J09XXXX'),
                   'ZAR-JIBAR-12M': ('JIBAR12', 'J12XXXX'),
                   'ZAR-CPI-3M': ('CPI', 'CPIXXXX'),
                   'ZAR-PRIME': ('PRIME', 'PRMABSA'),
                   'ZAR-REPO': ('SREPO', 'SRPXXXX'),
                   'ZAR-SABOR': ('SABOR', 'SBRXXXX'),}
         
class Demat_MT598_Helper():
    def __init__(self, ins):
        self.acm_ins = ins
        self.issuer_defined = True
        self.config_dict = demat_config.get_config()
        self.config = AbsaXmlConfigSettings()   
        
    def validate(self):
        #TODO
        #Validate that TOPU REDU and DISS ins has ISIN set
        valid = True
        try:
            if self.acm_ins.AdditionalInfo().Demat_Instrument() == True:

                if float(self.MinimumTradeDenomination()) < 0.01:
                    print 'MinimumTradeDenomination must be greater than 1'
                    valid = False
            
                if self.acm_ins.AdditionalInfo().MM_MMInstype() == None or self.acm_ins.AdditionalInfo().MM_MMInstype() == '':
                    print 'Please set Money Market InsType'
                    valid = False
                
                if self.acm_ins.AdditionalInfo().MM_MMInstype() == None or self.acm_ins.AdditionalInfo().MM_MMInstype() == '':
                    print 'Please set Money Market InsType'
                    valid = False

                if self.acm_ins.AdditionalInfo().Demat_Ins_SOR_Acc() == None or self.acm_ins.AdditionalInfo().Demat_Ins_SOR_Acc() == '':
                    print 'Please select SOR Account'
                    valid = False
                
                if self.acm_ins.AdditionalInfo().Demat_Issuer_BPID() == None or self.acm_ins.AdditionalInfo().Demat_Issuer_BPID() == '':
                    print 'Please set Issuer Participant Code'
                    valid = False

                if self.acm_ins.AdditionalInfo().Demat_WthhldTax() == True:
                    if self.acm_ins.AdditionalInfo().Demat_WthhldTx_Rate() == None:
                        print 'Please set Withholding Tax Rate'
                        valid = False
                
        except Exception, ex:
            print 'Validation Exception - Please check that all demat fields are filled in'
            return False
            
        return valid
        
    def Category(self):
        if self.acm_ins is not None:    
            ins_type = self.acm_ins.AdditionalInfo().MM_MMInstype()
            return INS_CATEGORY[ins_type][0]
        return None
        
    def CouponPaymentFrequency(self):
        return 'ISDF'
     
    def GenericCategory(self): 
        return self.Category()[-1:]
        
    def MMSecurityType(self):
        if self.acm_ins is not None:    
            ins_type = self.acm_ins.AdditionalInfo().MM_MMInstype()
            return INS_CATEGORY[ins_type][1]
        return None
        
    def MaturityDate(self):
        return '%s' % (datetime.strptime(self.acm_ins.ExpiryDate()[0:10], '%Y-%m-%d').strftime('%Y-%m-%d'))
        
    def IssueDate(self):
        return '%s' % (datetime.strptime(self.acm_ins.StartDate(), '%Y-%m-%d').strftime('%Y-%m-%d'))
        
    def CouponRateTypeIndicator(self):
        if self.Category() == 'CATG3':
            fleg = self.acm_ins.FirstFloatLeg()
            if fleg.RollingPeriodUnit() == "Days":
                return 'VLDY'
            else:
                return 'VLIN'
        elif self.Category() == 'CATG2':
            return 'FIXD'
        return None

        
    def MinimumTradeDenomination(self):
        min_trd_deno = ''
        if self.Category() in ['CATG2', 'CATG3']:
            min_trd_deno = self.acm_ins.AdditionalInfo().Demat_MinTrdDeno() or 0.0
        return min_trd_deno

    def MinimumIssueDenomination(self):
        min_issue_deno = ''
        if self.Category() in ['CATG2', 'CATG3']:
            min_issue_deno = self.acm_ins.AdditionalInfo().Demat_MinIssDeno() or 0.0
        return min_issue_deno

    def FinalCouponPaymentIndicator(self):
        return 'Y'
        
    def CouponPaymentIndicator(self):
        return 'Y'
        
    def AutomatedCouponPaymentCalculation(self):
        return 'N'
        
    def AutomatedCouponPaymentOnly(self):
        return 'Y'
        
    def CouponCompoundingFrequency(self):
        if self.Category() in ['CATG3']:
            return 'NONE'
        return None
        
    def CouponResetFrequency(self):
        if self.Category() in ['CATG3']:
            if self.CouponRateSource() in ['PRIME', 'CPI', 'SREPO', 'SABOR']:
                return 'ADHC'
            else:
                return 'ISDF'
        
    def InterestRate(self):
        if self.Category() in ['CATG2']:
            return self.acm_ins.FirstFixedLeg().FixedRate()
        return None
        
    def CouponRateVarianceFromSource(self):
        result = ''
        if self.Category() in ['CATG3']:
            fleg = [leg for leg in self.acm_ins.Legs() if leg.IsFloatLeg() == True]
            if len(fleg) > 0:
                spread = fleg[0].Spread() #always in percentage points
                if spread == 0:
                    result = 'PLUS-0,-PRCT'
                else:
                    spread_str = "%2.5f" % spread
                    spread_str = spread_str.replace('.', ',')
                    if spread_str.find(',') > 0:
                        parts = spread_str.split(',')
                        last_part = parts[-1]
                        spread_str = ','.join([parts[0], last_part])
                    else:
                        spread_str = '%s,' % spread_str
                if spread > 0:
                    result = 'PLUS-%s-PRCT' % spread_str
                elif spread < 0:
                    result = 'MINUS-%s-PRCT' % spread_str
        return result.replace('.', ',').replace('--', '-')
        
    def CouponResetDates(self):
        if self.issuer_defined and self.Category() in ['CATG3']:
            fleg = [leg for leg in self.acm_ins.Legs() if leg.IsFloatLeg() == True]
            if len(fleg) > 0:
                resets = fleg[0].Resets()
                if resets:
                    resetdates = [datetime.strptime(reset.Day(), '%Y-%m-%d') for reset in resets]
                    resetdates = [r.strftime('%Y-%m-%d') for r in resetdates if r.strftime('%Y-%m-%d') != self.acm_ins.StartDate()]
                    result = list(set(resetdates))
                    result.sort()
                    return result
        return [None]
    
    def CouponPayDates(self):
        if self.issuer_defined:
            if self.Category() in ['CATG3']:
                fleg = [leg for leg in self.acm_ins.Legs() if leg.IsFloatLeg() == True]
                if len(fleg) > 0:
                    cfs = fleg[0].CashFlows()
                    if cfs:
                        paydates = [datetime.strptime(cf.PayDate(), '%Y-%m-%d').strftime('%Y-%m-%d') for cf in cfs]
                        result = list(set(paydates))
                        result.sort()
                        return result
            elif self.Category() in ['CATG2']:
                fleg = [leg for leg in self.acm_ins.Legs() if leg.IsFixedLeg() == True]
                if len(fleg) > 0:
                    cfs = fleg[0].CashFlows()
                    if cfs:
                        paydates = [datetime.strptime(cf.PayDate(), '%Y-%m-%d').strftime('%Y-%m-%d') for cf in cfs]
                        result = list(set(paydates))
                        result.sort()
                        return result
        return [None]
    
    def CouponRateSource(self):
        if self.Category() in ['CATG3']:
            fleg = self.acm_ins.FirstFloatLeg()
            if fleg:
                return REFERENCE_INDEX[fleg.FloatRateReference().Name()][0]
        else:
            return ''
            
    def CouponRateSourceShort(self):
        if self.Category() in ['CATG3']:
            fleg = self.acm_ins.FirstFloatLeg()
            if fleg:
                result = REFERENCE_INDEX[fleg.FloatRateReference().Name()][1]
                spread = fleg.Spread() #always in percentage points
                if spread == 0:
                    result += 'PLP0,'
                else:
                    spread_str = "%2.5f" % spread
                    spread_str = spread_str.replace('.', ',')
                    
                    if spread_str.find(',') > 0:
                        parts = spread_str.split(',')
                        last_part = parts[-1]
                        spread_str = ','.join([parts[0], last_part])
                    else:
                        spread_str = '%s,' % spread_str
                    spread_str = spread_str.replace('-', '')
                if spread > 0:
                    result += 'PLP'+ spread_str
                elif spread < 0:
                    result += 'MIP' + spread_str
                return result
        else:
            return ''
            
    def CouponPaymentCalculationMethod(self):
        return 3
    
    def Issuer_Short_Code(self):
        issuer_short_code, issuer_bpid = self.acm_ins.AdditionalInfo().Demat_Issuer_BPID().replace(' ', '').split('/')
        return issuer_short_code
        
    def IdentificationSecurities(self):
        shortcode = self.Issuer_Short_Code()
        if shortcode == None:
            raise Exception('Issuer Party does not have Strate Short Code set')
        if self.Category() in ['CATG2']:
            maturityDate = datetime.strptime(self.MaturityDate(), '%Y-%m-%d').strftime('%Y%m%d') 
            genericCategory = self.GenericCategory()
            couponFrequency = self.CouponPaymentFrequency()
            mmSecurityType = self.MMSecurityType()
            couponFrequency = len(couponFrequency) > 0 and couponFrequency[:1] or ''
            cpn_rate = ("%2.7f" % self.InterestRate())
            if cpn_rate.find('.') > 0:
                parts = cpn_rate.split('.')
                part = parts[1]
                while len(part) > 0 and part[-1] == '0':
                    part = part[:-1]
                cpn_rate_str = ','.join([parts[0], part])
            else:
                cpn_rate_str = '%s,' % spread_str
            cpn_rate_str = cpn_rate_str.replace('-', '').replace('.', ',')
            securityIdentifier = '{0:3s}{1:4s}{2:8s}{3:1s}{4:1s}{5:s}'.format(shortcode, mmSecurityType, maturityDate, genericCategory, couponFrequency[0], cpn_rate_str )
            securityIdentifier = securityIdentifier.replace(' ', '0')
            return securityIdentifier
        if self.Category() in ['CATG3']:
            maturityDate = datetime.strptime(self.MaturityDate(), '%Y-%m-%d').strftime('%Y%m%d') 
            genericCategory = self.GenericCategory()
            variableCouponRateSource = self.CouponRateSourceShort()
            couponFrequency = self.CouponPaymentFrequency()
            mmSecurityType = self.MMSecurityType()
            couponFrequency = len(couponFrequency) > 0 and couponFrequency[:1] or ''        
            securityIdentifier = '{0:3s}{1:4s}{2:8s}{3:1s}{4:1s}{5:s}'.format(shortcode, mmSecurityType, maturityDate, genericCategory, couponFrequency[0], variableCouponRateSource )
            securityIdentifier = securityIdentifier.replace(' ', '0')
            return securityIdentifier
        return ''

    def csd_participant_code(self):
        csd_sor = self.acm_ins.AdditionalInfo().Demat_Ins_SOR_Acc()
        if len(csd_sor.replace(' ', '').split('/')) == 3:
            CSD, CSD_Participant_code, SOR_Accnr = csd_sor.replace(' ', '').split('/')
            return CSD_Participant_code            
        if len(csd_sor.replace(' ', '').split('/')) == 4:
            CSD, CSD_Participant_code, SOR_Accnr, CSA_Acc = csd_sor.replace(' ', '').split('/')
            return CSD_Participant_code

        return ''

        
    def issuer_participant_code(self):
        issuer_short_code, issuer_bpid = self.acm_ins.AdditionalInfo().Demat_Issuer_BPID().replace(' ', '').split('/')
        return issuer_bpid
        
    def agent_participant_code(self):

        absa_swift_param     = self.config.GetUniqueNode('AbcapSwiftParameters')
        
        if  self.acm_ins.AdditionalInfo().DIS_Instrument() == True :
            return self.config.GetValue(absa_swift_param, 'DisAgentParticipantCode', True)
        else:
            return self.config.GetValue(absa_swift_param, 'AgentParticipantCode', True)
        
    def sor_account(self):
        csd_sor = self.acm_ins.AdditionalInfo().Demat_Ins_SOR_Acc()
        if len(csd_sor.replace(' ', '').split('/')) == 3:
            CSD, CSD_Participant_code, SOR_Accnr = csd_sor.replace(' ', '').split('/')
            return SOR_Accnr            
        if len(csd_sor.replace(' ', '').split('/')) == 4:
            CSD, CSD_Participant_code, SOR_Accnr, CSA_Acc = csd_sor.replace(' ', '').split('/')
            return SOR_Accnr

        return ''

    def csa_account(self):
        csa_acc = self.acm_ins.AdditionalInfo().Demat_Ins_SOR_Acc()
      
        if len(csa_acc.replace(' ', '').split('/')) == 4:
            CSD, CSD_Participant_code, SOR_Accnr, CSA_Acc = csa_acc.replace(' ', '').split('/')
            return CSA_Acc

        return ''

        
    def withholding_tax(self):
        if self.acm_ins.AdditionalInfo().Demat_WthhldTax() == True:
            return 'Y'
        else:
            return 'N'
        
    def withholding_tax_rate(self):
        if self.acm_ins.AdditionalInfo().Demat_WthhldTx_Rate() != None:
            return self.acm_ins.AdditionalInfo().Demat_WthhldTx_Rate()
        else:
            return 0.0
        
TODAY = acm.Time().DateToday()

def from_instrument(ins, action, amount = 0.0, send_bp_id = None):
    acm.PollAllDbEvents()
    helper = Demat_MT598_Helper(ins)
    issuer = ins.Issuer()
    config_dict = demat_config.get_config()

    if action != 'ISSU':
        message = nonISSU_Mt598()
        abcapSwiftParameters = SwiftParamXmlConfig(ABSA_SWIFT_NODE)
        strateSwiftParameters = SwiftParamXmlConfig(STRATE_SWIFT_NODE)

        if  ins.AdditionalInfo().Demat_Instrument() == True: 
            message.UserHeader.MessageUserReference = str(int(time.time()*10))[-8:] + config_dict['routing_code'] + config_dict['strate_env'] + config_dict['message_version']
        
        if  ins.AdditionalInfo().DIS_Instrument() == True: 
            message.UserHeader.MessageUserReference = str(int(time.time()*10))[-8:] + config_dict['dis_routing_code'] + config_dict['dis_strate_env'] + config_dict['message_version']
        
        if  ins.AdditionalInfo().Demat_Instrument() == True :
            message.Header.LogicalTerminal.BicCode = abcapSwiftParameters.LogicalTerminalBic  + abcapSwiftParameters.IsinMgmtBicExtension

        if  ins.AdditionalInfo().DIS_Instrument() == True :
            message.Header.LogicalTerminal.BicCode = abcapSwiftParameters.LogicalTerminalBic  +  abcapSwiftParameters.IssueragentBicExtension

        message.ApplicationHeader.Address.BicCode = strateSwiftParameters.LogicalTerminalBic 
        
        


        #message.ApplicationHeader.Address.TerminalId = 'X'


        body = message.Body
        '''
            below modified 2020-08-12 - production fix 
            fix for field 20c being longer than 16 characters
        '''
        body.TransactionReference = 'ISM-%s' % (send_bp_id )
        body.SubMessageType = 155
        body.ProprietaryMessage = ' '
        body.StartOfBlock_General = 'GENL'
        body.MessageFunction.Function = 'NEWM'
        body.PreparationDate = acm.Time().TimeNow()
        body.InstructionType.Indicator = action
        body.InstructionType.DataSourceScheme = 'STRA'
        body.EndOfBlock_General = 'GENL'
        body.StartOfBlock_MMID = 'MMID'
        body.IssuerCSDParticipant.ProprietaryCode = helper.csd_participant_code()
        body.IssuerCSDParticipant.DataSourceScheme = 'STRA'
        body.IssuerParticipantCode.ProprietaryCode = helper.issuer_participant_code()
        body.IssuerParticipantCode.DataSourceScheme = 'STRA'     
        body.AgentParticipantCode.ProprietaryCode = helper.agent_participant_code()
        body.AgentParticipantCode.DataSourceScheme = 'STRA'
        body.SecuritiesIdentifier.Isin = ins.Isin().zfill(12)
        try:
            at_addInfo.save(ins, 'Demat_IsinShortDesc', helper.IdentificationSecurities()) #Also update instrument add_info with this field
        except Exception, ex:
            print 'Could not update Short Description', ex
        body.Nominal.Value = amount
        body.Nominal.QuantityTypeCode = 'FAMT'

        if  ins.AdditionalInfo().Demat_Instrument() == True :
            body.IssuerSORAccount.AccountNumber = helper.sor_account()
            body.IssuerSORAccount.DataSourceScheme = 'STRA'
            body.IssuerSORAccount.AccountType = 'IORT'

        if  ins.AdditionalInfo().DIS_Instrument() == True :
            body.IssuerSORAccount.AccountNumber = helper.csa_account()
            body.IssuerSORAccount.DataSourceScheme = 'STRA'
            body.IssuerSORAccount.AccountType = 'IORT'           

            body.IssuerCSAAccount.AccountNumber = helper.sor_account()
            body.IssuerCSAAccount.DataSourceScheme = 'STRA'
            body.IssuerCSAAccount.AccountType = ''  

        body.EndOfBlock_MMID = 'MMID'
        
    elif action == 'ISSU':
        message = ISSU_Mt598()
        abcapSwiftParameters = SwiftParamXmlConfig(ABSA_SWIFT_NODE)
        strateSwiftParameters = SwiftParamXmlConfig(STRATE_SWIFT_NODE)
        #message.UserHeader.MessageUserReference = str(int(time.time()*10))[-8:] + 'MS10' + 'P' + '002'
        print 'time ', int(time.time()*10)
        print 'routing_code ', config_dict['routing_code']
        print 'strate_env ', config_dict['strate_env']
        print 'message_version ', config_dict['message_version']
        
        message.UserHeader.MessageUserReference = str(int(time.time()*10))[-8:] + config_dict['routing_code'] + config_dict['strate_env'] + config_dict['message_version']
        message.Header.LogicalTerminal.BicCode = abcapSwiftParameters.LogicalTerminalBic  + abcapSwiftParameters.IsinMgmtBicExtension
        message.ApplicationHeader.Address.BicCode = strateSwiftParameters.LogicalTerminalBic 
        body = message.Body
        '''
            below modified 2020-08-12 - production fix 
            fix for field 20c being longer than 20 characters
        '''
        body.TransactionReference = 'ISM-%s' % (send_bp_id)
        body.SubMessageType = 155
        body.ProprietaryMessage = ' '
        body.StartOfBlock_General = 'GENL'
        body.MessageFunction.Function = 'NEWM'
        body.PreparationDate = acm.Time().TimeNow()
        body.InstructionType.Indicator = action
        body.InstructionType.DataSourceScheme = 'STRA'
        body.EndOfBlock_General = 'GENL'
        body.StartOfBlock_MMID = 'MMID'
        body.IssuerCSDParticipant.ProprietaryCode = helper.csd_participant_code()
        body.IssuerCSDParticipant.DataSourceScheme = 'STRA'
        body.IssuerParticipantCode.ProprietaryCode = helper.issuer_participant_code()
        body.IssuerParticipantCode.DataSourceScheme = 'STRA'     
        body.AgentParticipantCode.ProprietaryCode = helper.agent_participant_code()
        body.AgentParticipantCode.DataSourceScheme = 'STRA'
        body.SecuritiesIdentifierISSU.Description = helper.IdentificationSecurities()
        at_addInfo.save(ins, 'Demat_IsinShortDesc', body.SecuritiesIdentifierISSU.Description) #Also update instrument add_info with this field
        body.Nominal.Value = amount
        body.Nominal.QuantityTypeCode = 'FAMT'
        body.IssuerSORAccount.AccountNumber = helper.sor_account()
        body.IssuerSORAccount.DataSourceScheme = 'STRA'
        body.IssuerSORAccount.AccountType = 'IORT'
        body.StartOfBlock_Instrument = 'FIA'
        body.CouponFrequency.DataSourceScheme = 'STRA'
        body.CouponFrequency.Indicator = helper.CouponPaymentFrequency()
        body.GenericCategory.Description = helper.GenericCategory()
        body.MMSecurityType = helper.MMSecurityType()
        body.MaturityDate = helper.MaturityDate()
        body.IssueDate = helper.IssueDate()
        body.RateType.Indicator = helper.CouponRateTypeIndicator()
        body.RateType.DataSourceName = 'STRA'
        body.MinimumNominalAmount.Value = helper.MinimumTradeDenomination()
        body.MinimumNominalAmount.QuantityTypeCode = 'FAMT'
        #body.MinimumIssueAmount.Value = helper.MinimumIssueDenomination()
        #body.MinimumIssueAmount.QuantityTypeCode = 'FAMT'
        body.FinalCouponPaymentIndicator = helper.FinalCouponPaymentIndicator()
        body.CouponPaymentIndicator = helper.CouponPaymentIndicator()
        body.AutomatedCouponPaymentCalculation = helper.AutomatedCouponPaymentCalculation()
        body.WithholdingTaxOnInterest = helper.withholding_tax()
        if helper.withholding_tax() == 'Y':
            body.TaxRate = helper.withholding_tax_rate()
        body.AutomatedCouponPaymentOnly = helper.AutomatedCouponPaymentOnly()
        body.OverrideIndicator = 'N'
        body.CouponRateVarianceFromSource = helper.CouponRateVarianceFromSource()
        if not helper.CouponCompoundingFrequency() is None:
            body.CouponCompoundingFrequency.Indicator = helper.CouponCompoundingFrequency()
            body.CouponCompoundingFrequency.DataSourceScheme = 'STRA'
        body.EndOfBlock_Instrument = 'FIA'
        body.EndOfBlock_MMID = 'MMID'
        
        if helper.Category() == 'CATG2':
            #CD Instruments
            body.InterestRate = helper.InterestRate()
            if helper.issuer_defined:
                #Cashflow details used from Instrument
                for cpd in helper.CouponPayDates():
                    line = body.CouponPaymentDateDetails.AddSequence()
                    line.PayDate = cpd
            #ISDF period invalid for CD
            body.StartOfBlock_CRDDET = None
            body.EndOfBlock_CRDDET = None

        elif helper.Category() == 'CATG3':
            #FRN Instruments
            body.CouponRateSource.Country = 'ZAR'
            body.CouponRateSource.Source = helper.CouponRateSource()
            if body.CouponRateSource.Source == 'PRIME':
                body.CouponRateSource.PrimeSource = 'ABSA'
        
            if helper.issuer_defined:
                #Cashflow details used from Instrument
                body.CouponResetFrequency.Indicator = helper.CouponResetFrequency()
                if not body.CouponRateSource.Source in ['PRIME', 'CPI', 'SREPO', 'SABOR']:
                    body.CouponResetFrequency.DataSourceScheme = 'STRA'
                    for crd in helper.CouponResetDates():
                        line = body.CouponResetDateDetails.AddSequence()
                        line.ResetDate = crd
                else:
                    body.StartOfBlock_CRDDET = None
                    body.EndOfBlock_CRDDET = None
                    
                for cpd in helper.CouponPayDates():
                    line = body.CouponPaymentDateDetails.AddSequence()
                    line.PayDate = cpd
    
    return message
    
    
#print '=-'*30
msg = None
#NCD
#ins = acm.FInstrument['ZAR/160120-190121/7.30']
#msg = from_instrument(ins, 'ISSU', 100000000)
#msg = from_instrument(ins, 'TOPU', 50000000)
#msg = from_instrument(ins, 'REDU', 50000000)
#msg = from_instrument(ins, 'DISS')

#NCC
#ins = acm.FInstrument['ZAR/160120-190121/7.30']
#msg = from_instrument(ins, 'ISSU', 100000000)
#msg = from_instrument(ins, 'TOPU', 50000000)
#msg = from_instrument(ins, 'REDU', 50000000)
#msg = from_instrument(ins, 'DISS')

#PRN
#ins = acm.FInstrument['ZAR/160120-190121/7.30']
#msg = from_instrument(ins, 'ISSU', 100000000)
#msg = from_instrument(ins, 'TOPU', 50000000)
#msg = from_instrument(ins, 'REDU', 50000000)
#msg = from_instrument(ins, 'DISS')

#FRN - JIBAR
#ins = acm.FInstrument['ZAR/160120-190121/7.30']
#msg = from_instrument(ins, 'ISSU', 100000000)
#msg = from_instrument(ins, 'TOPU', 50000000)
#msg = from_instrument(ins, 'REDU', 50000000)
#msg = from_instrument(ins, 'DISS')

#FRN - PRIME
#ins = acm.FInstrument['ZAR/160120-190121/7.30']
#msg = from_instrument(ins, 'ISSU', 100000000)
#msg = from_instrument(ins, 'TOPU', 50000000)
#msg = from_instrument(ins, 'REDU', 50000000)
#msg = from_instrument(ins, 'DISS')

#CLN
#ins = acm.FInstrument['ZAR/160120-190121/7.30']
#msg = from_instrument(ins, 'ISSU', 100000000)
#msg = from_instrument(ins, 'TOPU', 50000000)
#msg = from_instrument(ins, 'REDU', 50000000)
#msg = from_instrument(ins, 'DISS')


#LNCD
#ins = acm.FInstrument['ZAR/FRN/ABSA B/JI/160204-160804']
#msg = from_instrument(ins, 'ISSU', 100000000)
#msg = from_instrument(ins, 'TOPU', 50000000)
#msg = from_instrument(ins, 'REDU', 50000000)
#msg = from_instrument(ins, 'DISS')

if msg:
    print str(msg)
