'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Creates SWIFT MT515 messages and places them on AMB
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 XXXXXX    Francois Truter           Initial Implementation
'''


'''========================== SWIFT MT515 MESSAGE ==========================='''

from gen_swift_mt_messages import MtMessageBase
from gen_swift_common import CRLF
from gen_swift_mt_fields import *
from gen_swift_mt_blocks import Body

MANDATORY = True
OPTIONAL = False

SINGLE = False
MULTIPLE = True

class Mt515MessageFunction:
    New = 'NEWM'
    Cancel = 'CANC'
    
    @staticmethod
    def OptionsDictionary():
        return {
             'New trade': Mt515MessageFunction.New
            ,'Trade cancellation': Mt515MessageFunction.Cancel
        }
    
    @staticmethod
    def GetFunctionFromTrade(trade):
        status = trade.Status()
        if status == 'BO Confirmed':
            return Mt515MessageFunction.New
        elif status == 'Void':
            return Mt515MessageFunction.Cancel
        else:
            raise Exception('No Mt515MessageFunction is mapped for trade status [%s].' % status)
    
class Mt515MessageSubfunction:
    Copy = 'COPY' 
    Duplicate = 'DUPL'
    CopyDuplicate = 'CODU'
    
class Mt515Amounts:
    AccruedInterestAmount = 'ACRU'
    Aktiengewinn = 'AKTI'
    ExecutingBrokersCommission = 'EXEC'
    NetGainLossAmount = 'ANTO'
    BackloadFeesAmount = 'BAKL'
    CorrespondentBankCharges = 'CBCH'
    ChargesFees = 'CHAR'
    RebateBonification = 'CREB'
    LocalBrokersCommission = 'LOCO'
    CountryNationalFederalTax = 'COUN'
    TradeAmount = 'DEAL'
    DiscountAmount = 'DSCA'
    EntranceFeesAmount = 'ENTF'
    EqualisationDepreciationDeposit = 'EQUL'
    EUTaxRetentionAmount = 'EUTR'
    IssueDiscountAllowance = 'ISDI'
    LocalTaxCountryspecific1 = 'LADT'
    PaymentLevyTax = 'LEVY'
    LocalTaxCountryspecific2 = 'LIDT'
    LocalTax = 'LOCL'
    LocalTaxCountryspecific3 = 'LOTE'
    LocalTaxCountryspecific4 = 'LYDT'
    MatchingConfirmationFee = 'MACC'
    MarginAmount = 'MARG'
    PostageAmount = 'POST'
    PremiumAmount = 'PRMA'
    ExpectedRefund = 'REFD'
    RegulatoryFees = 'REGF'
    SettlementAmount = 'SETT'
    ShippingAmount = 'SHIP'
    SpecialConcessions = 'SPCN'
    StampDuty = 'STAM'
    StockExchangeTax = 'STEX'
    SubscriptionInterest = 'SUBS'
    TransferTax = 'TRAN'
    TransactionTax = 'TRAX'
    ValueAddedTax = 'VATA'
    WithholdingTax = 'WITH'
    OtherAmount = 'OTHR'
    ConsumptionTax = 'COAX'
    AccruedCapitalisation = 'ACCA'
    Zwischengewinn = 'ZWIS'
    EarlyRedemptionFeeAmount = 'ERFE'
    PartialRedemptionWithholdingAmount = 'PRWI'

class Mt515(MtMessageBase):
    
    def __init__(self):
        MtMessageBase.__init__(self)
        self.ApplicationHeader.MessageType = 515
        
        self._body = Body([
            MtField16R('StartOfBlock_GeneralInformation', MANDATORY, 'GENL'),
            MtField20C('Reference', MANDATORY, 'SEME'),
            MtField23G('MessageFunction', MANDATORY),
            MtField98a('PreperationDate', OPTIONAL, 'PREP', SINGLE, ['A', 'C', 'E']),
            MtField22F('TradeTransactionType', MANDATORY, 'TRTR'),
            RepetitiveSequence('Linkages', [
                MtField16R('StartOfBlock_Linkages', MANDATORY, 'LINK'),
                MtField13a('IdentificationNumber', OPTIONAL, 'LINK', SINGLE, ['A', 'B']),
                MtField20C('Reference', MANDATORY, None),
                MtField16S('EndOfBlock_Linkages', MANDATORY, 'LINK')
            ], MANDATORY),
            MtField16S('EndOfBlock_GeneralInformation', MANDATORY, 'GENL'),
            RepetitiveSequence('PartialFillDetails', [
                MtField16R('StartOfBlock_PartialFillDetails', MANDATORY, 'PAFILL'),
                MtField36B('Quantity', MANDATORY, 'PAFI'),
                MtField90a('Price', MANDATORY, 'DEAL', SINGLE, ['A', 'B']),
                RepetitiveSequence('Indicator', [MtField22F('Value', OPTIONAL, None)], OPTIONAL),
                MtField98a('TradeDate', OPTIONAL, 'TRAD', SINGLE, ['A', 'B', 'C']),
                MtField94B('Place', OPTIONAL, 'TRAD'),
                MtField16S('EndOfBlock_PartialFillDetails', MANDATORY, 'PAFILL')
            ], OPTIONAL),
            MtField16R('StartOfBlock_ConfirmationDetails', MANDATORY, 'CONFDET'),
            MtField98a('ConfirmationDate', MANDATORY, None, MULTIPLE, ['A', 'B', 'C']),
            MtField90a('ConfirmationPrice', MANDATORY, None, MULTIPLE, ['A', 'B']),
            RepetitiveSequence('ConfirmationRate', [MtField92A('Value', OPTIONAL, None)], OPTIONAL),
            RepetitiveSequence('ConfirmationNumberCount', [MtField99A('Value', MANDATORY, None)], OPTIONAL),
            MtField94a('ConfirmationPlace', OPTIONAL, None, MULTIPLE, ['B', 'C', 'F']),
            MtField19A('SettlementAmount', OPTIONAL, 'SETT'),
            MtField22a('Indicator', MANDATORY, None, MULTIPLE, ['F', 'H']),
            MtField11A('Currency', OPTIONAL, None),
            RepetitiveSequence('ConfirmationParties', [
                MtField16R('StartOfBlock_ConfirmationParties', MANDATORY, 'CONFPRTY'),
                MtField95a('Party', MANDATORY, None, MULTIPLE, ['P', 'Q', 'R', 'S']),
                MtField97a('Account', OPTIONAL, None, MULTIPLE, ['A', 'B', 'E']),
                MtField98a('ProcessingDate', OPTIONAL, 'PROC', SINGLE, ['A', 'C']),
                MtField20C('ProcessingReference', OPTIONAL, 'PROC'),
                MtField70a('Narrative', OPTIONAL, None, MULTIPLE, ['C', 'E']),
                RepetitiveSequence('Indicator', [MtField22F('Value', OPTIONAL, None)], OPTIONAL),
                MtField16S('EndOfBlock_ConfirmationParties', MANDATORY, 'CONFPRTY')
            ], MANDATORY),
            RepetitiveSequence('Quantity', [MtField36B('Value', MANDATORY, None)], MANDATORY),
            MtField35B('Instrument', MANDATORY),
            RepetitiveSequence('InstrumentAttributes', [
                MtField16R('StartOfBlock_InstrumentAttributes', MANDATORY, 'FIA'),
                MtField94B('Place', OPTIONAL, 'PLIS'),
                RepetitiveSequence('Indicator', [MtField22F('Value', OPTIONAL, None)], OPTIONAL),
                MtField12a('InstrumentType', OPTIONAL, None, MULTIPLE, ['A', 'B', 'C']),
                MtField11A('DenominationCurrency', OPTIONAL, 'DENO'),
                RepetitiveSequence('Date', [MtField98A('Value', OPTIONAL, None)], OPTIONAL),
                RepetitiveSequence('Rate', [MtField92A('Value', OPTIONAL, None)], OPTIONAL),
                MtField13a('IdentificationNumber', OPTIONAL, None, MULTIPLE, ['A', 'B']),
                RepetitiveSequence('Flag', [MtField17B('Value', OPTIONAL, None)], OPTIONAL),
                MtField90a('Price', OPTIONAL, None, MULTIPLE, ['A', 'B']),
                RepetitiveSequence('Quantity', [MtField36B('Value', OPTIONAL, None)], OPTIONAL),
                RepetitiveSequence('InstrumentId', [MtField35B('Instrument', OPTIONAL)], OPTIONAL),
                MtField70E('Narrative', OPTIONAL, 'FIAN'),
                MtField16S('EndOfBlock_InstrumentAttributes', MANDATORY, 'FIA')
            ], OPTIONAL, 1),
            RepetitiveSequence('CertificateNumber', [MtField13B('Value', OPTIONAL, 'CERT')], OPTIONAL),
            RepetitiveSequence('Narrative', [MtField70E('Value', OPTIONAL, None)], OPTIONAL),
            MtField16S('EndOfBlock_ConfirmationDetails', MANDATORY, 'CONFDET'),
            RepetitiveSequence('SettlementDetails', [
                MtField16R('StartOfBlock_SettlementDetails', MANDATORY, 'SETDET'),
                RepetitiveSequence('Indicator', [MtField22F('Value', MANDATORY, None)], MANDATORY),
                MtField11A('Currency', OPTIONAL, None),
                RepetitiveSequence('SettlementParties', [
                    MtField16R('StartOfBlock_SettlementParties', MANDATORY, 'SETPRTY'),
                    MtField95a('Party', MANDATORY, None, MULTIPLE, ['C', 'P', 'Q', 'R', 'S']),
                    MtField97a('Account', OPTIONAL, 'SAFE', SINGLE, ['A', 'B']),
                    MtField98a('ProcessingDate', OPTIONAL, 'PROC', SINGLE, ['A', 'C']),
                    MtField20C('Reference', MANDATORY, 'PROC'),
                    MtField70a('Narrative', OPTIONAL, None, MULTIPLE, ['C', 'D']),
                    MtField16S('EndOfBlock_SettlementParties', MANDATORY, 'SETPRTY')
                ], OPTIONAL),
                RepetitiveSequence('CashParties', [
                    MtField16R('StartOfBlock_CashParties', MANDATORY, 'CSHPRTY'),
                    MtField95a('Party', MANDATORY, None, MULTIPLE, ['P', 'Q', 'R', 'S']),
                    MtField97a('Account', OPTIONAL, 'SAFE', MULTIPLE, ['A', 'E']),
                    MtField98a('ProcessingDate', OPTIONAL, 'PROC', SINGLE, ['A', 'C']),
                    MtField20C('Reference', MANDATORY, 'PROC'),
                    MtField70C('Narrative', OPTIONAL, 'PACO'),
                    MtField16S('EndOfBlock_CashParties', MANDATORY, 'CSHPRTY')
                ], OPTIONAL),
                RepetitiveSequence('Amounts', [
                    MtField16R('StartOfBlock_Amounts', MANDATORY, 'AMT'),
                    RepetitiveSequence('Flag', [MtField17B('Value', OPTIONAL, None)], OPTIONAL),
                    RepetitiveSequence('Amount', [MtField19A('Value', MANDATORY, None)], MANDATORY),
                    MtField98a('ValueDate', OPTIONAL, 'VALU', SINGLE, ['A', 'C']),
                    MtField92B('ExchangeRate', OPTIONAL, 'EXCH'),
                    MtField16S('EndOfBlock_Amounts', MANDATORY, 'AMT')
                ], OPTIONAL),
                MtField16S('EndOfBlock_SettlementDetails', MANDATORY, 'SETDET')
            ], OPTIONAL, 1),
            RepetitiveSequence('OtherParties', [
                MtField16R('StartOfBlock_OtherParties', MANDATORY, 'OTHRPRTY'),
                MtField95a('Party', MANDATORY, None, MULTIPLE, ['P', 'Q', 'R', 'S']),
                MtField97a('Account', OPTIONAL, 'SAFE', MULTIPLE, ['A', 'B', 'E']),
                MtField70C('Narrative', OPTIONAL, 'PACO'),
                MtField20C('Reference', OPTIONAL, 'PROC'),
                MtField16S('EndOfBlock_OtherParties', MANDATORY, 'OTHRPRTY')
            ], OPTIONAL),
            RepetitiveSequence('TwoLegTransactionDetails', [
                MtField16R('StartOfBlock_TwoLegTransactionDetails', MANDATORY, 'REPO'),
                MtField98a('Date', OPTIONAL, None, MULTIPLE, ['A', 'B', 'C']),
                RepetitiveSequence('Indicator', [MtField22F('Value', OPTIONAL, None)], OPTIONAL),
                RepetitiveSequence('Reference', [MtField20C('Value', OPTIONAL, None)], OPTIONAL),
                MtField92a('Rate', OPTIONAL, None, MULTIPLE, ['A', 'C']),
                RepetitiveSequence('NumberCount', [MtField99B('Value', OPTIONAL, None)], OPTIONAL),
                RepetitiveSequence('Amount', [MtField19A('Value', OPTIONAL, None)], OPTIONAL),
                MtField70C('Narrative', OPTIONAL, 'SECO'),
                MtField16S('EndOfBlock_TwoLegTransactionDetails', MANDATORY, 'REPO')
            ], OPTIONAL, 1)
        ])
        
    def SetRecipientFromParty(self, party):
        super(Mt515, self).SetRecipientFromParty(party, 'MT535Et515Recipient')
