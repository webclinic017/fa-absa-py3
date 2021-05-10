""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeSettleInstructions.py"
import acm
import FOperationsUtils as Utils
import datetime, time

ael_variables = []

class SettleInstructionUpgradeHandler(object):

    def RunUpgradingScript(self):
        Utils.LogAlways("Starting upgrade of Settlement Solution")
        try:
            parties = acm.FParty.Select("")
            messages = list()
            for party in parties:
                self.UpdateSettleInstructionsForParty(party, messages)
            self.PrintMessages(messages)
            Utils.LogAlways("\nFinished upgrading Settlement Solution")
        except Exception as e:
            Utils.LogAlways("Error: %s" % str(e))

    def PrintMessages(self, messages):
        if len(messages) > 0:
            Utils.LogAlways("\n\n")
            for message in messages:
                Utils.LogAlways(message)


    def UpdateSettleInstructionsForParty(self, party, messages):
        Utils.LogAlways("\nProcessing settle instructions for party %s." % party.Name())
        settleInstructions = party.SettleInstructions()
        if settleInstructions.Size() > 0:
            currentSettleInstruction = None
            try:
                acm.BeginTransaction()
                queryList = []
                for settleInstruction in settleInstructions:
                    currentSettleInstruction = settleInstruction
                    if settleInstruction.Query() == None and settleInstruction.QueryFilter() == None:
                        Utils.LogAlways("Creating query for settle instruction '%s'." % settleInstruction.Name())

                        ssiQuery = self.CreateSettleInstructionQueryFromSettleInstruction(settleInstruction, messages)
                        ssiQuery.Commit()

                        queryList.append(ssiQuery)
                    else:
                        Utils.LogAlways("Settle instruction '%s' already has a query and will not be updated." % settleInstruction.Name())
                i = 0
                for settleInstruction in settleInstructions:
                    currentSettleInstruction = settleInstruction
                    if settleInstruction.Query() == None and settleInstruction.QueryFilter() == None:
                        Utils.LogAlways("Committing settle instruction '%s'." % settleInstruction.Name())

                        ssiQuery = queryList[i]

                        settleInstruction.Query(ssiQuery)
                        settleInstruction.Commit()

                        i = i + 1
                acm.CommitTransaction() 
            except Exception as e:
                acm.AbortTransaction()
                Utils.LogAlways("An error occurred while processing settle instruction '%s': %s." % (currentSettleInstruction.Name(), str(e)))
                Utils.LogAlways("Aborting processing of settle instructions for '%s'. No changes will be saved." % party.Name())
            




    def CreateSettleInstructionQueryFromSettleInstruction(self, settleInstruction, messages):
        ssiQuery = acm.FSettleInstructionQuery()
        asqlQuery = self.CreateASQLQueryFromSettleInstruction(settleInstruction, messages)
        ssiQuery.Query(asqlQuery)
        ssiQuery.Name(str(settleInstruction.Oid()))
        ssiQuery.User(None)
        ssiQuery.AutoUser(False)
        return ssiQuery

    def CreateASQLQueryFromSettleInstruction(self, settleInstruction, messages):
        asqlQuery = acm.FASQLQuery()
        asqlQuery = acm.CreateFASQLQuery(acm.FSettlement, "AND")
        self.AddFromPartyCounterpartyNode(asqlQuery, settleInstruction, messages)
        self.AddFromPartyAcquirerNode(asqlQuery, settleInstruction, messages)
        self.AddInstrumentTypeNode(asqlQuery, settleInstruction)
        self.AddUnderlyingInstrumentTypeNode(asqlQuery, settleInstruction)
        self.AddCurrencyNode(asqlQuery, settleInstruction)
        self.AddSettlementCashFlowTypeNode(asqlQuery, settleInstruction)
        self.AddCollateralQueryNode(asqlQuery, settleInstruction)
        self.AddTradeSettleCategoryNode(asqlQuery, settleInstruction)
        self.AddInstrumentSettleCategoryNode(asqlQuery, settleInstruction)
        self.AddOTCNode(asqlQuery, settleInstruction)
        self.AddIssuanceTypeNode(asqlQuery, settleInstruction)


        return asqlQuery

    def AddFromPartyCounterpartyNode(self, query, ssi, messages):
        field = "Counterparty.Name"
        value = self.GetFromPartyCounterpartyValue(ssi, messages, field)
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'RE_LIKE_NOCASE', value)

    def AddFromPartyAcquirerNode(self, query, ssi, messages):
        field = "Acquirer.Name"
        value = self.GetFromPartyAcquirerValue(ssi, messages, field)
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'RE_LIKE_NOCASE', value)

    def AddInstrumentTypeNode(self, query, ssi):
        field = "Trade.Instrument.InsType"
        value = None
        if ssi.InstrumentType() != "None":
            value = Utils.GetEnum("InsType", ssi.InstrumentType())
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'EQUAL', value)

    def AddUnderlyingInstrumentTypeNode(self, query, ssi):
        field = "Trade.Instrument.Underlying.InsType"
        value = None
        if ssi.UndInsType() != "None":
            value = Utils.GetEnum("InsType", ssi.UndInsType())
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'EQUAL', value)

    def AddCurrencyNode(self, query, ssi):
        field = "Currency.Name"
        value = None
        if ssi.Currency() != None:
            value = ssi.Currency().Name()
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'RE_LIKE_NOCASE', value)

    def AddSettlementCashFlowTypeNode(self, query, ssi):
        cashCashFlow = ssi.CashSettleCashFlowType()
        secCashFlow = ssi.SecSettleCashFlowType()
        field = "Type"
        orNode = query.AddOpNode('OR')
        if cashCashFlow != "None":
            value = Utils.GetEnum("SettlementCashFlowType", cashCashFlow)
            orNode.AddAttrNode(field, 'EQUAL', value)
        if secCashFlow != "None":
            value = Utils.GetEnum("SettlementCashFlowType", secCashFlow)
            orNode.AddAttrNode(field, 'EQUAL', value)
        if orNode.AsqlNodes() == None or len(orNode.AsqlNodes()) == 0:
            orNode.AddAttrNode(field, 'EQUAL', None)

    #its called collateral in the UI when selecting DvP
    def AddCollateralQueryNode(self, query, ssi):
        field = "Trade.TradeCategory"
        value = None
        if ssi.TradeCategory() != "None":
            value = Utils.GetEnum("TradeCategory", ssi.TradeCategory())
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'EQUAL', value)

    #In the GUI it is called Trade Category,
    #but the choice list value is TradeSettleCategoryChlItem
    def AddTradeSettleCategoryNode(self, query, ssi):
        field = "Trade.SettleCategoryChlItem.Name"
        value = None
        if ssi.TradeSettleCategoryChlItem() != None:
            value = ssi.TradeSettleCategoryChlItem().Name()
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'RE_LIKE_NOCASE', value)

    #In the GUI it is called Ins Category,
    #but the choice list value is SettleCategoryChlItem
    def AddInstrumentSettleCategoryNode(self, query, ssi):
        field = "Trade.Instrument.SettleCategoryChlItem.Name"
        value = None
        if ssi.SettleCategoryChlItem() != None:
            value = ssi.SettleCategoryChlItem().Name()
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'RE_LIKE_NOCASE', value)

    def AddOTCNode(self, query, ssi):
        field = "Trade.Instrument.Otc"
        value = None
        if ssi.OtcInstr() == "OTC":
            value = True
        elif ssi.OtcInstr() == "Non OTC":
            value = False
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'EQUAL', value)

    def AddIssuanceTypeNode(self, query, ssi):
        field = "Trade.Instrument.IssuanceType"
        value = None
        if ssi.IssuanceType() != "None":
            value = Utils.GetEnum("IssuanceType", ssi.IssuanceType())
        orNode = query.AddOpNode('OR')
        orNode.AddAttrNode(field, 'EQUAL', value)



#----------------------- Utiliy functions --------------------------------------

    def GetFromPartyMethodChain(self, ssi):
        return ""

    def GetFromPartyAcquirerValue(self, ssi, messages, field):
        val = None
        fromParty = ssi.FromParty()
        if fromParty:
            if ssi.Party().Type() != "Intern Dept":
                message = self.GetFromPartyMessage(ssi, field)
                messages.append(message)
                val = fromParty.Name()
        return val

    def GetFromPartyCounterpartyValue(self, ssi, messages, field):
        val = None
        fromParty = ssi.FromParty()
        if fromParty:
            if ssi.Party().Type() == "Intern Dept":
                message = self.GetFromPartyMessage(ssi, field)
                messages.append(message)
                val = fromParty.Name()
        return val

    def GetFromPartyMessage(self, ssi, field):
        message = "NOTE: Settle instruction '%s' in party '%s' is using the criterion 'From party'.\n\
This criterion will be replaced with the method chain '%s'. Please validate your settle instruction setup." % (ssi.Name(), ssi.Party().Name(), field)
        return message


#-------------------------------------------------------------------------------

def ael_main(dictionary):
    upgradeHandler = SettleInstructionUpgradeHandler()
    upgradeHandler.RunUpgradingScript()

