""" Compiled: 2018-12-05 17:44:06 """

#__src_file__ = "extensions/settlement/etc/FSettlementCreator.py"

'''Module that generates settlements out of trades.'''
'''
------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Requester               Description
------------------------------------------------------------------------------------------------------------------------
22-03-2019      FAOPS-659       Joash Moodley           Kgomotso Gumbo          Generate MT202's for SSA MT54x 
                                                                                securities Funding.
01-05-2020      SBL             Jaysen Naicker          Gasant Thulsie          Amend SBL counterparty and counterparty 
                                                                                account. 
14-09-2020      FAOPS-864       Jaysen Naicker          Wandile Sithole         Enable End Cash for Euroclear 
                                                                                Repo/Reverse and include BuySellBack 
                                                                                instrument type in Funding.
05-03-2021      FAOPS-1030/53   Tawanda Mukhalela       Wandile Sithole         Refactored code to cater for Netted 
                                                                                Euroclear funding settlements.
24-05-2021      FAOPS-997       Ntokozo Skosana         Wandile Sithole         Added support for Euroclear and
                                                                                Africa Desk 'Cash' and 'Internal Fee' 
                                                                                settlement types modify counterparty
                                                                                details.
------------------------------------------------------------------------------------------------------------------------

'''
import acm

import FOperationsUtils as Utils
from FOperationsDateUtils import AdjustDateToday
from FOperationsRuleEngine import Rule, QueryCondition, RuleExecutor, ValueType, ActionFunction, ActionValue

import FSettlementUtils as SettlementUtils
import FSettlementStatusQueries as queries
import FSettlementDepositHandler, FSettlementModificationInspectorSingleton
from FSettlementCorrectTradeHandler import CorrectTradeHandler
from FSettlementExCouponDateHandler import ExCouponDateHandler
from FSettlementHookAdministrator import SettlementHooks, GetHookAdministrator
from FSettlementSplitter import SettlementSplitter
from FSettlementEnums import SettlementStatus, SettlementType, RelationType
from FOperationsEnums import TradeType, SettleType, LegType, InsType, QuotationType
import FSettlementSettledAmountHandler as SettledAmountHandler
import FSettlementValidations as Validations

calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
AFRICA_DESK_PARTY_NAME = 'AFRICA DESK'
TRADE_SETTLE_CATEGORIES = [
            'SSA_BWP_ALL_Custodian',
            'SSA_GHS_ALL_Custodian',
            'SSA_KES_ALL_Custodian',
            'SSA_MUR_ALL_Custodian',
            'SSA_UGX_ALL_Custodian',
            'SSA_ZMW_ALL_Custodian',
            'Euroclear'
]


class SettlementCreator(object):

    def __init__(self):
        self.__amountCalculator = self.__CreateAmountCalculator()
        self.__depositHandler = FSettlementDepositHandler.DepositHandler()
        self.__preventionRuleEngine = self.__CreatePreventionRuleEngine()
        self.__usedRefPayments = list() #A list containing payments id numbers. The purpose of this list is to make sure that that only one new settlement is referring to a payment
        self.__settlementSplitter = SettlementSplitter()

    @staticmethod
    def IsSpecialCaseAmountCalculation(settlement):
        specialCase = False
        if settlement.Type() == SettlementType.PAYOUT:
            specialCase = True
        elif settlement.Trade() and settlement.Trade().CorrectionTrade():
            specialCase = True
        elif Validations.PartiallySettledTrade(settlement.Trade()):
            specialCase = True
        return specialCase

    @staticmethod
    def __CreatePreventionRuleEngine():
        import FSettlementParameters as SettlementParams
        rules = []
        ruleExecutor = None
        for query in SettlementParams.preventSettlementCreationQueries:
            preventQuery = Utils.GetStoredQuery(query, acm.FSettlement)
            if preventQuery:
                rules.append(Rule(QueryCondition(preventQuery.Query()), ActionValue(True)))
        if len(rules):
            ruleExecutor = RuleExecutor(rules, ActionValue(False))
        return ruleExecutor

    @staticmethod
    def __AddCashflowNode(nodeToAddTo, cashflowType):
        '''In: nodeToAddTo - The OpNode that will contain the cashflow.
               cashflowType - The type of cashflow to add.'''

        nodeToAddTo.AddAttrNode('Type', 'EQUAL', Utils.GetEnum('SettlementCashFlowType', cashflowType))

    @staticmethod
    def GetClosedTradePayoutAmount(settlement):
        import FSettlementParameters as SettlementParams

        trade = settlement.Trade()
        instrument = trade.Instrument()
        hasMtmPrice = instrument.MtMPrice(instrument.ExpiryDate(), instrument.Currency(), 0)
        fet = SettlementParams.forwardEarlyTermination
        closingTrades = SettlementUtils.GetClosingTrades(trade)
        nominalAmount = 0.0
        payoutAmount = 0.0
        if hasMtmPrice and (acm.Time.TimeNow() >= instrument.ExpiryDate()) and \
           instrument.SettlementType() != SettleType.PHYSICAL_DELIVERY:
            if fet:
                payoutAmount = SettlementCreator.CalculateDefaultAmount(settlement)
            else:
                for t in closingTrades:
                    nominalAmount = nominalAmount + t.Nominal()
                cashAmount = SettlementCreator.CalculateDefaultAmount(settlement)
                totalNominal = trade.Nominal() + nominalAmount
                payoutAmount = (cashAmount / trade.Nominal()) * totalNominal

        return payoutAmount

    @staticmethod
    def GetClosingNDFTrades(trade):
        closingEnum = Utils.GetEnum('TradeType', TradeType.CLOSING)
        closingTrades = list()
        try:
            closingTrades = acm.FTrade.Select('instrument = {} and type = {} and contractTrdnbr = {}'.format(trade.Instrument().Oid(), closingEnum, trade.ContractTrdnbr()))
        except Exception as e:
            Utils.LogAlways(e)
        return closingTrades

    @staticmethod
    def GetOpeningNDFTrade(trade):
        openingEnum = Utils.GetEnum('TradeType', TradeType.NORMAL)
        errorMsg = "Found more than one opening trade for closing trade {}".format(trade.Oid())
        openingTrade = None
        try:
            openingTrade = acm.FTrade.Select01('instrument = {} and type = {} and contractTrdnbr = {}'.format(trade.Instrument().Oid(), openingEnum, trade.ContractTrdnbr()), errorMsg)
        except Exception as e:
            Utils.LogAlways(e)
        return openingTrade

    @staticmethod
    def GetNDFTradePayoutAmount(settlement):
        trade = settlement.Trade()
        instrument = trade.Instrument()
        quotation = instrument.Quotation()
        payoutAmount = 0.0

        closingTrades = SettlementCreator.GetClosingNDFTrades(trade)

        if trade in closingTrades:
            openingTrade = SettlementCreator.GetOpeningNDFTrade(trade)
            if openingTrade:
                if trade.Price() == 0:
                    Utils.LogVerbose("No price entered for closing trade {}".format(trade.Oid()))
                else:
                    if quotation.QuotationType() == QuotationType.PER_UNIT:
                        payoutAmount = (trade.Nominal() * (openingTrade.Price() - trade.Price()))
                    else:
                        payoutAmount = (trade.Nominal() * (1/openingTrade.Price() - 1/trade.Price()))
        else:
            hasMtmPrice = instrument.MtMPrice(instrument.ExpiryDate(), instrument.Currency(), 0)
            if hasMtmPrice:
                payoutAmount = SettlementCreator.CalculateDefaultAmount(settlement)
        return payoutAmount

    @staticmethod
    def GetClosingTradePayoutAmount(settlement):
        import FSettlementParameters as SettlementParams
        trade = settlement.Trade()
        instrument = trade.Instrument()
        hasMtmPrice = instrument.MtMPrice(instrument.ExpiryDate(), instrument.Currency(), 0)
        fet = SettlementParams.forwardEarlyTermination
        payoutAmount = 0.0
        if (fet == True and acm.Time.TimeNow() >= instrument.ExpiryDate()) or (fet == False):
            if instrument.SettlementType() != SettleType.PHYSICAL_DELIVERY and fet:
                if hasMtmPrice:
                    payoutAmount = SettlementCreator.CalculateDefaultAmount(settlement)
            else:
                closedTrade = acm.FTrade[trade.ContractTrdnbr()]
                if fet == False:
                    settlement.ValueDay(trade.ValueDay())
                payoutAmount = (instrument.Quotation().QuotationFactor() * trade.Nominal() * (closedTrade.Price() - trade.Price())) - \
                                CorrectTradeHandler().GetCorrectedAmount(trade, settlement)
        return payoutAmount

    @staticmethod
    def GetPayoutAmount(settlement):
        instrument = settlement.Trade().Instrument()
        payoutAmount = 0.0
        hasMtmPrice = instrument.MtMPrice(instrument.ExpiryDate(), instrument.Currency(), 0)
        if hasMtmPrice and (acm.Time.TimeNow() >= instrument.ExpiryDate()) and \
           instrument.SettlementType() != SettleType.PHYSICAL_DELIVERY:
            payoutAmount = SettlementCreator.CalculateDefaultAmount(settlement)
        return payoutAmount

    @staticmethod
    def CalculatePayoutAmount(settlement):
        trade = settlement.Trade()
        instrument = trade.Instrument()
        payoutAmount = 0.0
        if SettlementUtils.IsNDFTrade(trade):
            payoutAmount = SettlementCreator.GetNDFTradePayoutAmount(settlement)
        elif SettlementUtils.IsApplicableForPayoutProcessing(instrument):
            if SettlementUtils.IsClosingTrade(trade):
                payoutAmount = SettlementCreator.GetClosingTradePayoutAmount(settlement)
            elif SettlementUtils.IsClosedTrade(trade):
                payoutAmount = SettlementCreator.GetClosedTradePayoutAmount(settlement)
            else:
                payoutAmount = SettlementCreator.GetPayoutAmount(settlement)

        return payoutAmount

    @staticmethod
    def __SpecialCaseRule():
        '''Out: A rule for calculating the amount on a settlement.'''

        payoutQuery = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
        SettlementCreator.__AddCashflowNode(payoutQuery, SettlementType.PAYOUT)
        rule = Rule(QueryCondition(payoutQuery), ActionFunction(SettlementCreator.CalculatePayoutAmount))

        return [rule]

    @staticmethod
    def GetErrorString(settlement):
        errorString = 'Trade: %d, Settlement type: %s' % (settlement.Trade().Oid(), settlement.Type())
        if settlement.CashFlow():
            errorString = errorString + ', Cashflow: %d' % settlement.CashFlow().Oid()
        elif settlement.Dividend():
            errorString = errorString + ', Dividend: %d' % settlement.Dividend().Oid()
        return errorString

    @staticmethod
    def CalculateDefaultAmount(settlement):
        '''In: information needed to calculate amount.
           Out: The calculated amount.'''

        calcValue = settlement.Amount()
        if Validations.PartiallySettledTrade(settlement.Trade()):
            calcValue = calcValue - SettledAmountHandler.GetSettledAmount(settlement.Trade(), settlement)
        else:
            calcValue = calcValue - CorrectTradeHandler().GetCorrectedAmount(settlement.Trade(), settlement)
        return calcValue

    @staticmethod
    def __CreateAmountCalculator():
        '''Out: A RuleExecutor for calculating the amount on a settlement.'''

        return RuleExecutor(SettlementCreator.__SpecialCaseRule(), \
                            ActionFunction(SettlementCreator.CalculateDefaultAmount))
    @staticmethod
    def IsExDivDayApproved(dividend, trade):
        isExDivDayApproved = trade.ValueDay() <= dividend.ExDivDay()
        if not isExDivDayApproved:
            Utils.LogVerbose('A settlement record for dividend %d will not be created.\n' % dividend.Oid() + \
                            'Ex dividend day %s is earlier than trade\n' % dividend.ExDivDay() + \
                            'value day %s' % trade.ValueDay())
        return isExDivDayApproved

    @staticmethod
    def __AddPortfolioToSettlement(settlement, trade):
        '''In: settlement - The settlement to add a portfolio to.
               tal - The trade account link that is used to look up a Portfolio.'''

        portfolio = None
        if trade != None:
            portfolio = trade.Portfolio()
        if portfolio != None:
            if settlement.Amount() >= 0:
                settlement.ToPortfolio(portfolio)
            else:
                settlement.FromPortfolio(portfolio)

    @staticmethod
    def ApplyClientModification(settlement, netChildrenList = None):
        hookAdmin = GetHookAdministrator()
        if hookAdmin.HA_IsCustomHook(SettlementHooks.SETTLEMENT_MODIFICATION) :
            customerModifiedSettlement = settlement.Clone()
            customerModifiedSettlement.RegisterInStorage()
            diaryNote = hookAdmin.HA_CallHook(SettlementHooks.SETTLEMENT_MODIFICATION, customerModifiedSettlement, netChildrenList)
            modificationInspector = FSettlementModificationInspectorSingleton.GetModInspector()
            SBLSettlementModifier(customerModifiedSettlement).change_counterparty_account_ref()
            FundingSettlementModifier(customerModifiedSettlement).modify_funding_settlement()
            modifiedValuesList = modificationInspector.GetClientModifiedValues(customerModifiedSettlement, settlement)

            for field, newValueString, oldValueString in modifiedValuesList:
                eval('settlement.'+ str(field) + "('" + newValueString + "')")
                Utils.LogVerbose("Field " + str(field) + " on the settlement record " + str(settlement.Oid()) + " has been changed from " + str(oldValueString) + " to " + str(newValueString) + " by the customer")
            if diaryNote is not None and diaryNote != '':
                settlement.AddDiaryNote(diaryNote)

    def __IsPaymentEqual(self, prevPayment, payment):
        '''In: revPayment - A Payment
              payment - A Payment
           Out: Returns True if the two payments are equal
        '''
        if payment.RecordType() == prevPayment.RecordType():
            if payment.Type() == prevPayment.Type():
                if payment.Party() == prevPayment.Party():
                    if payment.PayDay() == prevPayment.PayDay():
                        if payment.Currency() == prevPayment.Currency():
                            if payment.ArchiveStatus() == prevPayment.ArchiveStatus():
                                if payment.OurAccount() == prevPayment.OurAccount():
                                    if payment.OriginalCurrency() == prevPayment.OriginalCurrency():
                                        if payment.FxTransaction() == prevPayment.FxTransaction():
                                            if payment.FxTransaction() == prevPayment.FxTransaction():
                                                if payment.Account() == prevPayment.Account():
                                                    if payment.ValidFrom() == prevPayment.ValidFrom():
                                                        return True
        return False

    def __GetRefPayment(self, trade, payment):
        '''In: trade - the corrected trade
              payment - The new payment that needs to find his ancestor
           Out: A payment.
        '''
        for prevTrade in CorrectTradeHandler.GetCorrectedTrades(trade):
            if prevTrade:
                for prevPayment in prevTrade.Payments():
                    if self.__IsPaymentEqual(payment, prevPayment):
                        settlements = acm.FSettlement.Select("payment = %d" %prevPayment.Oid())
                        if not (prevPayment.Oid() in self.__usedRefPayments):
                            foundSettlementInStatusClosed = False
                            for settlement in settlements:
                                if settlement.Status() == SettlementStatus.CLOSED or SettlementUtils.CorrectTradePayNet(settlement):
                                    foundSettlementInStatusClosed = True

                                if settlement.Status() == SettlementStatus.VOID and settlement.Parent() and \
                                   (settlement.Parent().RelationType() == RelationType.NET or settlement.Parent().RelationType() == RelationType.AD_HOC_NET):
                                    foundSettlementInStatusClosed = True

                                if foundSettlementInStatusClosed:
                                    self.__usedRefPayments.append(prevPayment.Oid())
                                    return prevPayment

        return None



    def __CreateSettlement(self, settlement, settlementCorrectTradeRecaller):
        """

        :param settlement: FSettlement
        :param settlementCorrectTradeRecaller: list
        :return: FSettlement
        """
        '''In: flow (FMoneyFlow) - Contains info about the new settlement.
           Out: The created settlement.'''

        import FSettlementParameters as SettlementParams
    
        Utils.LogVerbose("In CreateSettlement")
        Utils.LogVerbose(str(settlement.Amount()) + str(settlement.Type()))
    
        settlement.RegisterInStorage()

        if settlement.IsSecurity():
            settlement.PartialSettlementType(SettlementParams.defaultPartialSettlementType)

        if settlement.Type() == SettlementType.REDEMPTION_SECURITY:
            settlement.RestrictNet(True)

        date = settlement.ValueDay()
        if date == None:
            raise LookupError('Date missing.')

        settleType = settlement.Type()
        if settleType == None:
            raise LookupError('SettlementCashFlowType missing.')

        trade = settlement.Trade()
        refObject = settlement.SourceObject()
        isExDateApproved = True

        if refObject:
            if (refObject.Class() == acm.FDividend):
                isExDateApproved = SettlementCreator.IsExDivDayApproved(refObject, trade)
            elif (refObject.Class() == acm.FCashFlow):
                if trade:
                    isExDateApproved = ExCouponDateHandler(settlement, refObject).IsExCouponDateApproved()
            elif (refObject.Class() == acm.FPayment):
                settlement.RefPayment(self.__GetRefPayment(trade, refObject))
        Utils.LogVerbose("Before Special Case")
        Utils.LogVerbose(str(settlement.Amount()) + str(settlement.Type()))
        if self.IsSpecialCaseAmountCalculation(settlement):
            Utils.LogVerbose("inside Special Case")
            settlement.Amount(self.__amountCalculator.Execute(settlement, ValueType.SINGLE_VALUE, settlement))
            counterpartyAccount = acm.Operations.AccountAllocator().CalculateCounterpartyAccountForSettlement(settlement, settlement.Counterparty())
            acquirerAccount = acm.Operations.AccountAllocator().CalculateAcquirerAccountForSettlement(settlement, settlement.Acquirer())
            settlement.CounterpartyAccountRef(counterpartyAccount)
            settlement.AcquirerAccountRef(acquirerAccount)

        self.__AddPortfolioToSettlement(settlement, settlement.Trade())
        if trade:
            if SettlementParams.setProtectionAndOwnerFromTrade:
                Utils.SetProtectionAndOwnerFromTrade(settlement, trade)

        SettlementCreator.ApplyClientModification(settlement)
        Utils.LogVerbose("After Client Modification")
        Utils.LogVerbose(str(settlement.Amount()) + str(settlement.Type()))
        hookAdmin = GetHookAdministrator()
        settlement.NotificationDay(hookAdmin.HA_CallHook(SettlementHooks.GET_NOTIFICATION_DATE, settlement))
        createdSettlement = settlement
        Utils.LogVerbose(str(createdSettlement.Amount()) + str(createdSettlement.Type()))
        settlementCorrectTradeRecaller.AddSettlement(settlement)
        if self.__IsPreventSettlement(settlement, isExDateApproved):
            createdSettlement = None
        self.__settlementSplitter.SplitSettlement(createdSettlement)
        for splittedSettlement in self.__settlementSplitter.GetSplittedSettlements():
            SettlementCreator.ApplyClientModification(splittedSettlement)
            splittedSettlement.NotificationDay(hookAdmin.HA_CallHook(SettlementHooks.GET_NOTIFICATION_DATE, splittedSettlement))
            settlementCorrectTradeRecaller.AddSettlement(splittedSettlement)
        if None == createdSettlement:
            self.__settlementSplitter.ClearSplittedSettlements()

        return createdSettlement

    def __IsCreditDefaultLegTypeSettlement(self, settlement):
        creditDefaultType = False
        if (settlement.CashFlow()):
            if (settlement.CashFlow().Leg().LegType() == LegType.CREDIT_DEFAULT):
                creditDefaultType = True
        return creditDefaultType

    def __IsPreventSettlement(self, settlement, isExDateApproved):
        """
        Block settlements from creating. Settlement will be blocked from being created if the settlement
        amount is equal to the ceded amount for Deposits where the Ceded flag (additional info) is set to True.
        :param settlement:
        :param isExDateApproved:
        :return:
        """
        Utils.LogVerbose("In IsPreventSettlement")
        Utils.LogVerbose(str(isExDateApproved))
        Utils.LogVerbose(str(self.__depositHandler.PreventSettlementCreation(settlement)))
        isPreventSettlement = False
        addInfos = settlement.Trade().AdditionalInfo()
        if SettlementUtils.IsWithinTimeWindow(settlement) == False:
            isPreventSettlement = True

        elif (settlement.Type() == SettlementType.NONE):
            Utils.LogVerbose("Preventing %s, since this type of not mapped for settlement" % (settlement.Type()))
            isPreventSettlement = True

        elif 'MM_Ceded_Amount' in dir(addInfos) and 'MM_Account_Ceded' in dir(addInfos) and addInfos.MM_Account_Ceded() is True:
            # Check if the add infos exist on the trade
            if addInfos.MM_Ceded_Amount():
                # Check if account is ceded and if the ceded amount is set
                if (round(settlement.Amount(), 2)) == (settlement.Trade().AdditionalInfo().MM_Ceded_Amount()*-1):
                    # Block settlement if ceded amount is equal to the settle amount
                    Utils.LogVerbose("Preventing %s, due to ceding" % (settlement.Type()))
                    isPreventSettlement = True

        elif self.__depositHandler.PreventSettlementCreation(settlement) or \
           not isExDateApproved or (settlement.Amount() == 0.0):
            Utils.LogVerbose("Preventing %s, Amount %f" % (settlement.Type(), settlement.Amount()))
            isPreventSettlement = True

        elif self.__IsCreditDefaultLegTypeSettlement(settlement):
            Utils.LogVerbose("Preventing %s, since it belongs to a credit default leg" % (settlement.Type()))
            isPreventSettlement = True

        return isPreventSettlement

    def __IsPreventSettlementByPreventionQuery(self, settlement):
        isPreventSettlement = False
        if self.__preventionRuleEngine and \
           self.__preventionRuleEngine.Execute(settlement,
                                               ValueType.SINGLE_VALUE,
                                               settlement):
            Utils.LogVerbose("preventSettlementCreation query satisfied.\n" +  \
                          "Preventing %s settlement %d" % (settlement.Type(), settlement.Oid()))
            isPreventSettlement = True
        return isPreventSettlement

    def __GetSettlements(self, trade):
        import FSettlementParameters as SettlementParams
        calendar = trade.Currency().Calendar()
        startDate = AdjustDateToday(calendar, -SettlementParams.maximumDaysBack)
        endDate = SettlementUtils.INFINITE_NUMBER_OF_DAYS
        if trade.Instrument().InsType() != InsType.FUTURE_FORWARD:
            endDate = AdjustDateToday(calendar, SettlementParams.maximumDaysForward)
        return trade.GenerateSettlements(startDate, endDate)

    def CreateSettlements(self, trade, settlementCorrectTradeRecaller):
        '''In: trade - Trade to create settlements for.
           Out: The created settlements or an empty list.'''
        self.__usedRefPayments = list()
        settlements = list()
        settlementsToBeCreated = list()
        if not queries.GetRecallStatusesQuery().IsSatisfiedBy(trade):
            allSettlementsForTrade = self.__GetSettlements(trade)
            for settlementForTrade in allSettlementsForTrade:
                settlement = self.__CreateSettlement(settlementForTrade, settlementCorrectTradeRecaller)
                if settlement:
                    if self.__settlementSplitter.HasSplittedSettlements():
                        for splittedSettlement in self.__settlementSplitter.GetSplittedSettlements():
                            settlements.append(splittedSettlement)
                    else:
                        settlements.append(settlement)
            for settlementToBeCreated in settlements:
                if settlementToBeCreated.SplitTypeChlItem():
                    if settlementToBeCreated.SplitTypeChlItem().Name() == 'CededAmount':
                        acm.Log('CEDED : Change settlement status to "Hold"')
                        settlementToBeCreated.Status('Hold')
                if self.__IsPreventSettlementByPreventionQuery(settlementToBeCreated) is False:
                    settlementsToBeCreated.append(settlementToBeCreated)

        return settlementsToBeCreated

    def CreateSettlementsFromSettlement(self, trade, settlementForTrade, settlementCorrectTradeRecaller):
        '''In: trade - Trade to create settlements for.
           Out: The created settlements or an empty list.'''
        self.__usedRefPayments = list()
        settlements = list()
        settlementsToBeCreated = list()
        if not queries.GetRecallStatusesQuery().IsSatisfiedBy(trade):
            settlement = self.__CreateSettlement(settlementForTrade, settlementCorrectTradeRecaller)
            if settlement:
                if self.__settlementSplitter.HasSplittedSettlements():
                    for splittedSettlement in self.__settlementSplitter.GetSplittedSettlements():
                        settlements.append(splittedSettlement)
                else:
                    settlements.append(settlement)
            for settlementToBeCreated in settlements:
                if self.__IsPreventSettlementByPreventionQuery(settlementToBeCreated) is False:
                    settlementsToBeCreated.append(settlementToBeCreated)

        return settlementsToBeCreated


class SBLSettlementModifier(object):
    '''
    Check if Security Loan instrument and set party on settlments as per SBL logic
    '''
    def __init__(self, settlement):
        self.settlement = settlement
        self.trade = settlement.Trade()
        self.counterparty = settlement.Counterparty()
        if self.trade is not None:
            self.counterparty = self._change_counterparty()

    def change_counterparty_account_ref(self):
        """
        Change AccountRef for Counterparty.
        """
        is_sbl_settlement = self._is_valid_sbl_settlement()
        if is_sbl_settlement:
            party = self._change_counterparty()
            counterparty_account = acm.Operations.AccountAllocator().CalculateCounterpartyAccountForSettlement(
                self.settlement, party)
            self.settlement.CounterpartyAccountRef(counterparty_account)

    def _is_valid_sbl_settlement(self):
        """
        Determine whether or not to trigger the counterparty change
        for the settlement.
        """
        if not self.trade:
            return False
        instrument = self.trade.Instrument()
        if instrument.InsType() != 'SecurityLoan':
            return False
        if self.trade.Acquirer().Name() != 'SECURITY LENDINGS DESK':
            return False
        if self.settlement.Type() in ['Security Nominal', 'End Security']:
            party_1 = self.trade.AdditionalInfo().SL_G1Counterparty1()
            party_2 = self.trade.AdditionalInfo().SL_G1Counterparty2()
            if self.counterparty and self.counterparty.Name() in (party_1, party_2):
                return True
        return False

    def _change_counterparty(self):
        """
        Change Settlement Counterparty.
        """
        counterparty = self.settlement.Counterparty()
        if self.settlement.Type() == 'Security Nominal':
            party_name = self.trade.AdditionalInfo().SL_G1Counterparty1()
            if party_name:
                counterparty = acm.FParty[party_name]
        if self.settlement.Type() == 'End Security':
            party_name = self.trade.AdditionalInfo().SL_G1Counterparty2()
            if party_name:
                counterparty = acm.FParty[party_name]
        if counterparty:
            self.settlement.Counterparty(counterparty)
        return counterparty


class FundingSettlementModifier(object):
    """
    Class to modify the counterparty and acoountref for
    qualifying funding settlements
    """
    def __init__(self, settlement):
        self.settlement = settlement

    def modify_funding_settlement(self):
        """
        Change the Settlement Counterparty and Account
        """
        if not self.settlement.Trade():
            return
        if self._is_valid_settle_category(self.settlement.Trade(), TRADE_SETTLE_CATEGORIES):
            africa_funding_settlement_types = (
                'Premium', 'Payment Premium', 'Broker Fee',
                'Payment Cash', 'Internal Fee'
            )
            euroclear_funding_settlement_types = (
                'Premium', 'Payment Premium', 'Stand Alone Payment',
                'End Cash', 'None', 'Fixed Rate', 'Fixed Amount',
                'Payment Cash', 'Internal Fee'
            )
            if self._is_for_africa_desk_acquirer(self.settlement):
                if not self._check_settlement_type(self.settlement, africa_funding_settlement_types):
                    return
                self._set_counterparty_and_account(self.settlement)

            elif self.settlement.Trade().SettleCategoryChlItem().Name() == 'Euroclear':
                if not self._check_settlement_type(self.settlement, euroclear_funding_settlement_types):
                    return
                self._set_counterparty_and_account(self.settlement)

    @staticmethod
    def _is_for_africa_desk_acquirer(settlement):
        """
        Check if the settlement Acquirer is Africa Desk
        """
        if not settlement.Acquirer():
            return False
        if not settlement.Acquirer().Name() == AFRICA_DESK_PARTY_NAME:
            return False

        return True

    @staticmethod
    def _is_valid_settle_category(trade, settle_categories):
        """
        Check if the trade has a desired trade settle category.
        """
        if not trade.SettleCategoryChlItem():
            return False
        if trade.SettleCategoryChlItem().Name() not in settle_categories:
            return False

        return True

    @staticmethod
    def _check_settlement_type(settlement, settlement_type):
        """
        Determine if settlement has the desired settlement type
        '"""
        if settlement.Type() in settlement_type:
            return True
        return False

    @staticmethod
    def _set_counterparty_and_account(settlement):
        """
        Set the counterparty and its account to be same as the acquirer.
        """
        settlement.Counterparty(settlement.Acquirer())
        settlement.CounterpartyName(settlement.Acquirer().Name())
        settlement.CounterpartyAccountRef(settlement.AcquirerAccountRef())
