'''-----------------------------------------------------------------------------
PROJECT                 : Markets Message Gateway
PURPOSE                 : SWIFT MT535 message definition
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               : Francois Truter
CR NUMBER               : XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no    Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 XXXXXX       Francois Truter         Initial Implementation
2016                    Willie van der Bank     Remove PageNumber hardcoding
                                                for Demat
'''
'''========================== SWIFT MT535 MESSAGE ==========================='''

from gen_swift_mt_messages import MtMessageBase

from gen_swift_mt_blocks import Body
from gen_swift_mt_fields import *

MANDATORY = True
OPTIONAL = False

SINGLE = False
MULTIPLE = True

class Mt535(MtMessageBase):
    
    def __init__(self):
        MtMessageBase.__init__(self)
        self.ApplicationHeader.MessageType = 535
        #self.ApplicationHeader.InputOutput = 'O'
        
        self._body = Body([
            MtField16R('StartOfBlock_General', MANDATORY, 'GENL'),
            MtField28E('PageNumber', MANDATORY),
            MtField13a('StatementNumber', OPTIONAL, 'STAT', SINGLE, ['A', 'J']),
            MtField20C('Reference', MANDATORY, 'SEME'),
            MtField23G('MessageFuntion', MANDATORY),
            MtField98a('Date', MANDATORY, None, MULTIPLE, ['A', 'C']),
            RepetitiveSequence('Indicator', [MtField22F('Value', MANDATORY, None)], MANDATORY),
            RepetitiveSequence('Linkages', [
                MtField16R('StartOfBlock_Linkages', MANDATORY, 'LINK'),
                MtField13a('IdentificationNumber', OPTIONAL, 'LINK', SINGLE, ['A', 'B']),
                MtField20C('Reference', MANDATORY, None),
                MtField16S('EndOfBlock_Linkages', MANDATORY, 'LINK')
            ], OPTIONAL),
            MtField95a('AccountOwner', OPTIONAL, 'ACOW', SINGLE, ['P', 'R']),
            MtField97a('SafekeepingAccount', MANDATORY, 'SAFE', SINGLE, ['A', 'B']),
            RepetitiveSequence('Flag', [MtField17B('Value', MANDATORY, None)], MANDATORY),
            MtField16S('EndOfBlock_General', MANDATORY, 'GENL'),
            RepetitiveSequence('SubSafekeepingAccount', [
                MtField16R('StartOfBlock_SubSafekeepingAccount', MANDATORY, 'SUBSAFE'),
                MtField95a('AccountOwner', OPTIONAL, 'ACOW', SINGLE, ['P', 'R']),
                MtField97a('Account', OPTIONAL, 'SAFE', SINGLE, ['A', 'B']),
                MtField94a('Place', OPTIONAL, None, SINGLE, ['B', 'C', 'F']),
                MtField17B('ActivityFlag', OPTIONAL, 'ACTI'),
                RepetitiveSequence('Instrument', [
                    MtField16R('StartOfBlock_Instrument', MANDATORY, 'FIN'),
                    MtField35B('Identification', MANDATORY),
                    RepetitiveSequence('InstrumentAttributes', [
                        MtField16R('StartOfBlock_InstrumentAttributes', MANDATORY, 'FIA'),
                        MtField94a('Place', OPTIONAL, None, MULTIPLE, ['B', 'D']),
                        RepetitiveSequence('Indicator', [MtField22F('Value', OPTIONAL, None)], OPTIONAL),
                        MtField12a('InstrumentType', OPTIONAL, None, MULTIPLE, ['A', 'B', 'C']),
                        MtField11A('DenominationCurrency', OPTIONAL, 'DENO'),
                        RepetitiveSequence('Date', [MtField98A('Value', OPTIONAL, None)], OPTIONAL),
                        RepetitiveSequence('Rate', [MtField92A('Value', OPTIONAL, None)], OPTIONAL),
                        MtField13a('IdentificationNumber', OPTIONAL, None, MULTIPLE, ['A', 'B', 'K']),
                        RepetitiveSequence('Flag', [MtField17B('Value', OPTIONAL, None)], OPTIONAL),
                        MtField90a('Price', OPTIONAL, None, MULTIPLE, ['A', 'B']),
                        RepetitiveSequence('Quantity', [MtField36B('Value', OPTIONAL, None)], OPTIONAL),
                        RepetitiveSequence('InstrumentId', [MtField35B('Instrument', OPTIONAL)], OPTIONAL),
                        MtField70E('Narrative', OPTIONAL, 'FIAN'),
                        MtField16S('EndOfBlock_InstrumentAttributes', MANDATORY, 'FIA')
                    ], OPTIONAL, 1),
                    MtField22H('CorporateActionCode', OPTIONAL, 'CAOP'),
                    MtField90a('Price', OPTIONAL, None, SINGLE, ['A', 'B']),
                    MtField94B('PriceSource', OPTIONAL, 'PRIC'),
                    MtField98a('PriceQuoteDate', OPTIONAL, 'PRIC', SINGLE, ['A', 'C']),
                    RepetitiveSequence('Balance', [MtField93B('Value', MANDATORY, None)], MANDATORY),
                    RepetitiveSequence('SubBalance', [
                        MtField16R('StartOfBlock_SubBalance', MANDATORY, 'SUBBAL'),
                        MtField93a('Balance', MANDATORY, None, MULTIPLE, ['B', 'C']),
                        MtField94a('Place', OPTIONAL, None, MULTIPLE, ['B', 'C', 'F']),
                        MtField90a('Price', OPTIONAL, None, SINGLE, ['A', 'B', 'E']),
                        MtField98a('PriceQuoteDate', OPTIONAL, 'PRIC', SINGLE, ['A', 'C']),
                        MtField99A('DaysAccrued', OPTIONAL, 'DAAC'),
                        RepetitiveSequence('Amount', [MtField19A('Value', OPTIONAL, None)], OPTIONAL),
                        MtField92B('ExchangeRate', OPTIONAL, 'EXCH'),
                        MtField70C('Narrative', OPTIONAL, 'SUBB'),
                        RepetitiveSequence('QuantityBreakdown', [
                            MtField16R('StartOfBlock_QuanitityBreakdown', MANDATORY, 'BREAK'),
                            MtField13a('LotNumber', OPTIONAL, 'LOTS', SINGLE, ['A', 'B']),
                            MtField36B('LotQuantity', OPTIONAL, 'LOTS'),
                            MtField98a('LotDate', OPTIONAL, 'LOTS', SINGLE, ['A', 'C', 'E']),
                            MtField90a('LotPrice', OPTIONAL, 'LOTS', SINGLE, ['A', 'B']),
                            MtField22F('TypeOfPrice', OPTIONAL, 'PRIC'),
                            RepetitiveSequence('Amount', [MtField19A('Value', OPTIONAL, None)], OPTIONAL),
                            MtField16S('EndOfBlock_QuanitityBreakdown', MANDATORY, 'BREAK')
                        ], OPTIONAL),
                        MtField16S('EndOfBlock_SubBalance', MANDATORY, 'SUBBAL')
                    ], OPTIONAL),
                    MtField99A('DaysAccrued', OPTIONAL, 'DAAC'),
                    RepetitiveSequence('Amount', [MtField19A('Value', OPTIONAL, None)], OPTIONAL),
                    MtField92B('ExchangeRate', OPTIONAL, 'EXCH'),
                    MtField70E('HoldingsNarrative', OPTIONAL, 'HOLD'),
                    RepetitiveSequence('QuantityBreakdown', [
                        MtField16R('StartOfBlock_QuanitityBreakdown', MANDATORY, 'BREAK'),
                        MtField13a('LotNumber', OPTIONAL, 'LOTS', SINGLE, ['A', 'B']),
                        MtField36B('LotQuantity', OPTIONAL, 'LOTS'),
                        MtField98a('LotDate', OPTIONAL, 'LOTS', SINGLE, ['A', 'C', 'E']),
                        MtField90a('LotPrice', OPTIONAL, 'LOTS', SINGLE, ['A', 'B']),
                        MtField22F('TypeOfPrice', OPTIONAL, 'PRIC'),
                        RepetitiveSequence('Amount', [MtField19A('Value', OPTIONAL, None)], OPTIONAL),
                        MtField16S('EndOfBlock_QuanitityBreakdown', MANDATORY, 'BREAK')
                    ], OPTIONAL),
                    MtField16S('EndOfBlock_Instrument', MANDATORY, 'FIN')
                ], OPTIONAL),
                MtField16S('EndOfBlock_SubSafekeepingAccount', MANDATORY, 'SUBSAFE')
            ], OPTIONAL),
            RepetitiveSequence('AdditionalInformation', [
                MtField16R('StartOfBlock_AdditionalInformation', MANDATORY, 'ADDINFO'),
                MtField95a('Party', OPTIONAL, None, MULTIPLE, ['P', 'Q', 'R']),
                RepetitiveSequence('Amount', [MtField19A('Value', OPTIONAL, None)], OPTIONAL),
                MtField16S('EndOfBlock_AdditionalInformation', MANDATORY, 'ADDINFO')
            ], OPTIONAL)
        ])
        
        #self._body.PageNumber.Value = 1
        #self._body.PageNumber.ContinuationIndicator = 'ONLY'
        
    def SetRecipientFromParty(self, party):
        super(Mt535, self).SetRecipientFromParty(party, 'MT535Et515Recipient')
            
class Mt535Frequency:

    AdHoc = 'ADHO'
    Daily = 'DAIL'
    IntraDay = 'INDA'
    Monthly = 'MNTH'
    Weekly = 'WEEK'
    Yearly = 'YEAR'
    
    @staticmethod
    def OptionsDictionary():
        return {
             'Ad Hoc': Mt535Frequency.AdHoc
            ,'Daily': Mt535Frequency.Daily
            ,'Intra Day': Mt535Frequency.IntraDay
            ,'Monthly': Mt535Frequency.Monthly
            ,'Weekly': Mt535Frequency.Weekly
            ,'Yearly': Mt535Frequency.Yearly
        }
    
class Mt535StatementType:

    Accounting = 'ACCT'
    Custody = 'CUST'
