""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionUtils.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionUtils 

DESCRIPTION
----------------------------------------------------------------------------"""
import acm
import FBDPCommon
import FCorpActionElectionStatesSetup
import math

CORP_ACTION_FILTER = FBDPCommon.valueFromFParameter('FCAVariables', 'CorpActionFilter')

def HandlerFromParams(insClass):
    positionSpec = None
    fParamDict = FBDPCommon.FParamsParser().get_dict('FCAVariables')
    specKey = 'Handler.{0}'.format(insClass)
    if fParamDict and specKey in fParamDict:
        mod, func = fParamDict[specKey].split('.')
        return getattr(__import__(mod), func)
    return None

def GetTradesForAction(action):
    storedquery = BuildASQLQueryFolder(action)
    return storedquery.Query().Select()

'''
Need to include:
1) all trades eligible for the corporate action.
2) all trades generated by the corporate action.'''
def BuildASQLQueryFolder(action):
    ins = action.Instrument()
    instruments = ins.Derivatives().AsList()
    instruments.Add(ins)
    storedQuery = acm.FStoredASQLQuery[CORP_ACTION_FILTER]
    if storedQuery:
        query = storedQuery.Query()
    else:
        query = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    orNode = query.AddOpNode('OR')
    shouldUseRecordDate = ShouldUseRecordDate(action)
    for instrument in instruments:
        andNode = orNode.AddOpNode('AND')
        andNode.AddAttrNode('Instrument.Name', 'EQUAL', instrument.Name())
        if shouldUseRecordDate:
            andNode.AddAttrNode('AcquireDay', 'LESS_EQUAL', action.RecordDate())
        else:
            andNode.AddAttrNode('TradeTime', 'LESS', action.ExDate())
    
    #Add Corp Action-generated trades
    trades = GetCorporateActionTrades(action)
    for trade in trades:
        orNode.AddAttrNode('Oid', 'EQUAL', trade.Oid())
    
    storedquery = acm.FStoredASQLQuery()
    storedquery.Name('Corporate Action Positions')
    storedquery.Query(query)
    return storedquery
    
def GetCorporateActionTrades(action):
    trades = []
    choices = action.CaChoices()
    for choice in choices:
        elections = choice.CaElections()
        for election in elections:
            businessEvent = GetBusinessEventForElection(election)
            if businessEvent:
                trades.extend(businessEvent.Trades(0))
    return trades

def PortfolioFromInstance(positionInstance):
    # Found a bug in CreatePortfolioFromPosition
    # When the attribute value is None, The query will be empty.
    # return acm.PositionStorage.CreatePortfolioFromPosition(positionInstance)
    # So I did the implementation myself.
    
    attributes = positionInstance.Attributes()
    q = acm.CreateFASQLQuery(acm.FTrade, 'AND')
    for a in attributes:
        attName = a.DefinitionAsString()
        attValue = a.AttributeValue()
        if attName == "Instrument.Underlying.Name":
            if attValue in ['None', 'No Trade: Underlying']:
                attValue = None
        q.AddAttrNode(attName, 'EQUAL', attValue);
    
    return acm.FASQLPortfolio(q)

def ShouldUseRecordDate(corporateAction):

    return corporateAction.Market().Name() == 'RecordDate' if corporateAction.Market() else False


def IsMandatory(action):
    return (action.CaChoiceType() == 'Mandatory' and
            action.CaChoices().Size() is 1)


def GetBusinessEventForElectionFromAdditionalInfo(election):
    try:
        addInfoSpec = acm.FAdditionalInfoSpec['BusinessEvent']
        if not addInfoSpec:
            return None
        eventOid = FBDPCommon.GetAdditionalInfoValue(election,
                                                     'CorpActionElection',
                                                     'BusinessEvent')
        if eventOid:
            return acm.FBusinessEvent[eventOid]
    except Exception:
        return None
    return None

def GetBusinessEventForElection(election):
    event = election.BusinessEvent()
    if not event:
        return GetBusinessEventForElectionFromAdditionalInfo(election)
        
    return event

def getElectionsForAction(action):
    elections = []
    choices = action.CaChoices()
    for choice in choices:
        elections.extend(getElectionsForChoice(choice))
    return elections

def getElectionsForChoice(choice):
    elections = [election for election in choice.CaElections() if election.Oid() > 0]
    return elections

def getStateChartStates():
    stateChart = acm.FStateChart['CorpActionElectionStateChart']
    scStates = stateChart.States()
    stateList = [st.Name() for st in scStates]    
    states = acm.FArray()
    for item in stateList:
        states.Add(item)
    
    return states

# Eventually move to another module
# Basic validation only
def isValidCorporateAction(action):
    choices = action.CaChoices()
    if len(choices) == 0:
        return False
    for choice in choices:
        if not isValidCorpActionChoice(choice):
            return False
    
    return True

def isValidCorpActionChoice(choice):
    payouts = choice.CaPayouts()
    if len(payouts) == 0:
        return False
    for payout in payouts:
        if payout.PayoutRate() < 0.0:
            return False
        if payout.PayoutAmount() < 0.0:
            return False
    
    return True


def NewInstrument(payout, ins = None):
    aelPayout = FBDPCommon.acm_to_ael(payout)
    if not ins:
        if aelPayout.new_instrument_seqnbr:
            return acm.FInstrument[aelPayout.new_instrument_seqnbr.insid]
        else:
            return None

    aelPayoutClone = aelPayout.clone()
    aelPayoutClone.new_instrument_seqnbr = ins.Oid()
    aelPayoutClone.commit()
    return ins

def SetNewInstrument(payout, ins):
    aelPayout = FBDPCommon.acm_to_ael(payout)
    if ins is None:
        insOid = 0
    else:
        insOid = ins.Oid()
    aelPayoutClone = aelPayout.clone()
    aelPayoutClone.new_instrument_seqnbr = insOid
    aelPayoutClone.commit()
    return ins

def GetNewInstrument(payout):
    aelPayout = FBDPCommon.acm_to_ael(payout)
    if aelPayout.new_instrument_seqnbr:
        return acm.FInstrument[aelPayout.new_instrument_seqnbr.insid]
    return None

def GetCorpActionValidDate(action):
    shouldUseRecordDate = ShouldUseRecordDate(action)
    validDate = action.RecordDate() if shouldUseRecordDate else action.ExDate()
    return validDate
    
def get_next_corporate_action(corp_acts):
    if not corp_acts:
        return None
    nextCorpAction = None
    earliestCorpActionDate = None
    today = acm.Time().DateToday()
    for aCorpAction in corp_acts:
        validDate = GetCorpActionValidDate(aCorpAction)
        if validDate >= today and not nextCorpAction:
            nextCorpAction = aCorpAction
            earliestCorpActionDate = validDate
        elif validDate >= today and validDate < earliestCorpActionDate:
            nextCorpAction = aCorpAction
            earliestCorpActionDate = validDate
    return nextCorpAction

def get_corp_action_choice_type(corp_action):
    if corp_action:
        return corp_action.CaChoiceType()
    return ''

def get_corp_action_text(corp_action):
    if corp_action:
        return corp_action.Text()
    return ''

def get_corp_action_name(corp_action):
    if corp_action:
        return corp_action.Name()
    return ''

def get_corp_action_exdate(corp_action):
    if corp_action:
        return corp_action.ExDate()
    return ''

def get_corporate_actions(instrument):
    query = 'instrument = %i'%instrument.Originator().Oid()
    return acm.FCorporateAction.Select(query)

def getBusinessProcessAndEvent(caPosition, toState):
    if FCorpActionElectionStatesSetup.CorporateActionUsingBusinessProcess():
        businessProcess = FBDPCommon.GetBusinessProcess(caPosition.Oid(), 'CorpActionElection')
        if businessProcess:
            fromState = businessProcess.CurrentStep().State().Name()
            if fromState == toState:
                return businessProcess, None, True
            event = FCorpActionElectionStatesSetup.GetEvent(fromState, toState)
            print(fromState, '--', toState, '--', event)
            if not event:
                print('State transition does not exist')
            return businessProcess, event, False
    return None, None, False

def validateBusinessProcessTransition(caPosition, toState):
    action = caPosition.CaChoice().CorpAction()
    if action.CaChoiceType() in ['Mandatory', 'MandatoryWithChoice']:
        return True
    businessProcess, event, sameState = getBusinessProcessAndEvent(caPosition, toState)
    return True if (event or not businessProcess or sameState or (not event and toState != 'Processed')) else False

def positionBusinessProcessTransition(caPosition, toState):
    businessProcess, event, sameState = getBusinessProcessAndEvent(caPosition, toState)
    if sameState:
        return
    if event:
        businessProcess.HandleEvent(event)
        businessProcess.Commit()
    elif businessProcess and (caPosition.CaChoice().CorpAction().CaChoiceType() in ['Mandatory', 'MandatoryWithChoice'] or
                            toState != 'Processed'):
        businessProcess.ForceToState(toState, 'Forced')
        businessProcess.Commit()

def forceToRollbackBusinessProcess(stateChartName, subject, fromState, reason):
    businessProcess = FBDPCommon.GetBusinessProcess(subject.Oid(), stateChartName)
    if businessProcess and businessProcess.CurrentStep().State().Name() == fromState:
        previousState = businessProcess.CurrentStep().PreviousStep().State().Name()
        businessProcess.ForceToState(previousState, reason)
        businessProcess.Commit()


def GetCorporateActionIssuer(corporateAction):
    underlying = corporateAction.Instrument()
    while underlying.Underlying():
        underlying = underlying.Underlying()

    return underlying.Issuer()


def GetShortName(countryName):
    """ Limits country name to 10 characters"""
    return countryName if len(countryName) < 11 else countryName[:9] + '.'

def GetOriginCountry(corporateAction):
    """ Function returns:
        1) name of country of corporate action market if exists
        2) name of country of issuer of sotck which is object of corporet action
            if exists
        3) empty string if first two names do not exist"""
    market = corporateAction.Market()
    if market and market.Country():
        return GetShortName(market.Country())

    issuer = GetCorporateActionIssuer(corporateAction)
    if issuer and issuer.Country():
        return GetShortName(issuer.Country())

    return ''

def get_elections_for_position(election, position):
    elections = []
    corp_action = election.CaChoice().CorpAction()
    for choice in corp_action.CaChoices():
        for elec in choice.CaElections():
            if elec.PositionInstance() == position:
                elections.append(elec)

    return elections

def find_total_percentage(elections):
    percentage = 0.0
    for election in elections:
        #ignore oversubscription
        if isOverSubscription(election.CaChoice()):
            continue
        percentage += math.fabs(election.Percentage())
    
    return percentage

def isOverSubscription(choice):
    choiceRecord = choice.ChoiceRecord()
    if choiceRecord:
        dict = eval(choiceRecord.Text())
        if dict['Option Action'] == 'OVER':
            return True
    
    return False

def StateTransitionFromElectedQuantity(election, oldQuantity, pos):

    newQuantity = getattr(election, 'Quantity')()
    if newQuantity != oldQuantity:
        if newQuantity == 0.0:
            if pos > 0:
                forceToRollbackBusinessProcess('CorpActionElection', election, 'Lender Election Received', '')
            else:
                forceToRollbackBusinessProcess('CorpActionElection', election, 'Borrower Instructed', '')
        elif oldQuantity == 0.0:
            if pos > 0:
                positionBusinessProcessTransition(election, 'Lender Election Received')
            else:
                positionBusinessProcessTransition(election, 'Borrower Instructed')
