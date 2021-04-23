'''
In the current state this script can only be used to add new SSIs and SSI rule.
It is based on the core query called FSettlementUpgradeSettleInstructions.

Main function to be called:
main(ptyid, ssiName, accType, overrideSSI, acquirer, instype, currency, tradesettlecat, inssettlecat, cftype, account_name)

The parameters need to be passed to the function main in the order indicated by the number:
non-blank string:
1) party name
2) ssi name
3) ssi account type
12) account to be selected on the SSI rule

boolean:
4) should the SSI be overriden if it already exists

list
valid options for all/blank are [], '' and None
add <NOT> to any 1 or more values in the list to add a NOT to the SSI rule:
5)  acquirer
6)  instype
7)  currency
8)  trade settle category
9)  insrument settle category
10) trade optional key 1
11) cash flow ftype

History
==========
2017-12-11      CHNG0005220511  Willie vd Bank Created
2019-04-08      FAOPS-427       Stuart Wilson   modified to work with four eyes process for
                                                client static uploads
2020-01-09      PCGDEV-227      Joash Moodley   added effective_from to AddSSIRule.
'''

import acm
import traceback


class SettleInstructionQuery(object):
    def __init__(self, settleInstruction, acquirer, instype, currency, tradesettlecat, inssettlecat, optkey1, cftype):
        self.acquirer = acquirer
        self.instype = instype
        self.currency = currency
        self.tradesettlecat = tradesettlecat
        self.inssettlecat = inssettlecat
        self.optkey1 = optkey1
        self.cftype = cftype
        self.settleInstructionOid = str(settleInstruction)

    def CreateASQLQuery(self):
        asqlQuery = acm.FASQLQuery()
        asqlQuery = acm.CreateFASQLQuery(acm.FSettlement, "AND")

        self.Add_RE_LIKE_NOCASE_Node(asqlQuery, self.acquirer, "Acquirer.Name")
        self.Add_EQUAL_Node(asqlQuery, self.instype, "Trade.Instrument.InsType")
        self.Add_RE_LIKE_NOCASE_Node(asqlQuery, self.currency, "Currency.Name")
        self.Add_RE_LIKE_NOCASE_Node(asqlQuery, self.tradesettlecat, "Trade.SettleCategoryChlItem.Name")
        self.Add_RE_LIKE_NOCASE_Node(asqlQuery, self.inssettlecat, "Trade.Instrument.SettleCategoryChlItem.Name")
        self.Add_RE_LIKE_NOCASE_Node(asqlQuery, self.optkey1, "Trade.OptKey1.Name")
        self.Add_EQUAL_Node(asqlQuery, self.cftype, "Type")
        #self.AddFromPartyCounterpartyNode(asqlQuery, settleInstruction, messages)
        #self.AddUnderlyingInstrumentTypeNode(asqlQuery, settleInstruction)
        #self.AddCollateralQueryNode(asqlQuery, settleInstruction)
        #self.AddOTCNode(asqlQuery, settleInstruction)
        #self.AddIssuanceTypeNode(asqlQuery, settleInstruction)
        return asqlQuery

    def Add_RE_LIKE_NOCASE_Node(self, query, valList, field):
        if valList and type(valList) == type([]):   #this will exclude [], '' and None
            orNode = query.AddOpNode('OR')
            for value in valList:
                if '<NOT>' in value:
                    orNode.Not('True')
                    value = value.replace('<NOT>', '')
                orNode.AddAttrNode(field, 'RE_LIKE_NOCASE', value)

    def Add_EQUAL_Node(self, query, valList, field):
        if valList and type(valList) == type([]):
            orNode = query.AddOpNode('OR')
            for value in valList:
                orNode.AddAttrNode(field, 'EQUAL', value)


def createSSI(ptyid, ssiName, accType, overrideSSI):
    party = acm.FParty[ptyid]
    for partySSI in party.SettleInstructions():
        if partySSI.Name() == ssiName:
            if overrideSSI:
                print 'SSI already exists and will be overridden.'
                return partySSI
            else:
                raise ValueError('SSI already exists!!!')
    newSSI = acm.FSettleInstruction()
    newSSI.Name(ssiName)
    newSSI.Party(party)
    if accType == 'Delivery versus Payment':
        newSSI.AccountType('Cash and Security')
        newSSI.SettleDeliveryType('Delivery versus Payment')
    else:
        newSSI.AccountType(accType)
        newSSI.SettleDeliveryType('Delivery Free of Payment')
    newSSI.DefaultInstruction(True)
    return newSSI


def AddSSIRule(ssi, account_name, effective_from):
    newRule = acm.FSettleInstructionRule()
    party = ssi.Party()
    newRule = acm.FSettleInstructionRule()
    newRule.EffectiveFrom(effective_from)

    acc = [acc for acc in party.Accounts() if acc.Name() == account_name]
    if acc:
        if ssi.AccountType() == 'Cash':
            newRule.CashAccount(acc[0])
        else:
            newRule.SecAccount(acc[0])
    else:
        print 'No account has been provided to link to new SSI!!!'
    newRule.SettleInstruction(ssi)
    ssi.Rules().Add(newRule)

def main(
    ptyid, ssiName, accType, overrideSSI, acquirer, instype, currency,
    tradesettlecat, inssettlecat, optkey1, cftype,
    account_name, effective_from
    ):
    try:
        acm.BeginTransaction()
        print 'SSI creation started...'
        newSSI = createSSI(ptyid, ssiName, accType, overrideSSI)
        print 'SSI %s created on %s.' %(ssiName, ptyid)
        ssiQueryClass = SettleInstructionQuery(str(newSSI.Oid()), acquirer, instype, currency, tradesettlecat, inssettlecat, optkey1, cftype)
        asqlQuery = ssiQueryClass.CreateASQLQuery()
        newSSI.QueryFilter(asqlQuery)
        AddSSIRule(newSSI, account_name, effective_from)
        newSSI.Commit()
        acm.CommitTransaction()
        print 'SSI query %s created.' % str(newSSI.Oid())
        print 'SSI creation done.'

    except Exception as ex:
        acm.AbortTransaction()
        traceback.print_exc()
        print ex
