""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/corporate_actions_workbench/./etc/FCAElectionColumns.py"
"""--------------------------------------------------------------------------
MODULE
    FCAElectionColumns

DESCRIPTION
    Functions supporting Corporate action election sheet columns.

-----------------------------------------------------------------------------"""
import acm
import FBDPCommon
from FCorpActionUtils import ShouldUseRecordDate
from FCorpActionUtils import get_elections_for_position, find_total_percentage
from FPositionUtils import GetAttributeValue
from FCorpActionUtils import positionBusinessProcessTransition, StateTransitionFromElectedQuantity
from FCorpActionElectionPosition import PositionCalculator
import FCorpActionElectionStatesSetup
import math

CA_POSITION_STATES_ORDER = FCorpActionElectionStatesSetup.CA_POSITION_STATES_ORDER

def caDeadline(action):
    return getCADateTime(action, 'Deadline')

def caReplyDate(action):
    return getCADateTime(action, 'ReplyDate')

def getCADateTime(action, methodName):
    deadline = 0
    choices = action.CaChoices()
    for choice in choices:
        elections = choice.CaElections()
        for election in elections:
            date = getattr(election, methodName)()
            if deadline < date:
                deadline = date
    return deadline

def caSaveDateTime(row, col, calcval, val, operation):
    colStrKey = col.StringKey()
    if row.IsKindOf(acm.FCorporateAction) and colStrKey in ['ReplyDate', 'Deadline']:
        dt = None
        try:
            dt = FBDPCommon.toDateTime(acm.Time.UtcToLocal(val))
        except:
            pass
        if dt:
            choices = row.CaChoices()
            for choice in choices:
                elections = choice.CaElections()
                for election in elections:
                    getattr(election, colStrKey)(dt)
                    election.Commit()
        calcval.GetEvaluator().RemoveSimulation()

def caEligiblePosition(election, trades):

    action = election.CaChoice().CorpAction()
    posCalc = PositionCalculator(action)
    posInstance = election.PositionInstance()
    positions = posCalc.Positions(posInstance)
    #there should only be one position
    eligiblePosition = positions[0].Value()
    if eligiblePosition == 0.0 and len(trades) == 1:
        #check if this is the box position
        bEvent = action.BusinessEvent()
        bTrades = bEvent.Trades(0)
        if len(bTrades) == 1:
            if bTrades[0] == trades[0]:
                return trades[0].Quantity()

    return eligiblePosition

def caStockEntitlement(election, payouts):

    pos = caEligiblePosition(election, None)
    stockAmount = caElectionStockAmount(election, payouts)
    if stockAmount:
        return stockAmount * pos
    return None

def caCashEntitlement(election, payouts):

    pos = caEligiblePosition(election, None)
    cashAmount = caElectionCashAmount(election, payouts)
    if cashAmount:
        return cashAmount * pos
    return None


def caElectionCashAmount(election, payouts):

    if election:
        choice = election.CaChoice()
        array = acm.FDenominatedValueArray()
        dv = acm.GetFunction('denominatedvalue', 4)
        action = choice.CorpAction()
        for p in payouts:
            payoutAmount = p.PayoutAmount() if p.PayoutAmount() else p.PayoutNetAmount()
            if not payoutAmount:
                payoutAmount = p.PayoutGrossAmount() * election.AdditionalInfo().TaxRate()
            if not payoutAmount:
                continue
            currencyName = p.Currency().AsSymbol() if p.Currency().AsSymbol() else None
            val = dv(payoutAmount, None, currencyName, action.SettleDate())
            array.Add(val)
        if array.Size() > 0:
            return array
    return None


def caElectionStockAmount(election, payouts):
    if election:
        choice = election.CaChoice()
        array = acm.FDenominatedValueArray()
        dv = acm.GetFunction('denominatedvalue', 4)
        action = choice.CorpAction()
        for p in payouts:
            payoutRate = p.PayoutRate()
            if not payoutRate:
                continue
            inst = p.NewInstrument() if p.NewInstrument() else action.Instrument()
            val = dv(payoutRate, None, inst.AsSymbol(), action.SettleDate())
            array.Add(val)
        if array.Size() > 0:
            return array
    return None

def nextCorpActionStockEntitlement(action, eligiblePosition):
    if not action:
        return None
    if not eligiblePosition:
        return None
    if math.isnan(eligiblePosition):
        return None
    entitlement = 0.0
    array = acm.FDenominatedValueArray()
    dv = acm.GetFunction('denominatedvalue', 4)
    choices = action.CaChoices()
    for choice in choices:
        payouts = choice.CaPayouts()
        for p in payouts:
            payoutRate = p.PayoutRate()
            if not payoutRate:
                continue
            inst = p.NewInstrument() if p.NewInstrument() else action.Instrument()
            val = dv(payoutRate * eligiblePosition, None, inst.AsSymbol(), action.SettleDate())
            array.Add(val)
        if array.Size() > 0:
            return array
    return None

def caElectionInstrument(election):
    positionInstance = election.PositionInstance()
    instrument = None
    name = GetAttributeValue(positionInstance, 'Instrument.Name')
    if name is not None:
        instrument = acm.FInstrument[name]
    return instrument

def BusinessProcessQuery(subject_seqnbr, subject_type):
    return "subject_seqnbr={0} and subject_type={1}".format(
                        subject_seqnbr, subject_type)


def caElectionStatus(election):
    if (election and 
         FCorpActionElectionStatesSetup.CorporateActionUsingBusinessProcess()):
        condition = BusinessProcessQuery(election.Oid(),
                                'CorpActionElection')
        bp = acm.FBusinessProcess.Select(condition)
        if bp.Size() > 0:
            return bp[0].CurrentStep().State().Name()
    return 'Unknown'


def onIsTotalPercentageClick(row, col, cell, activate, operation):
    epos = caEligiblePosition(row, None)
    if not row.IsKindOf(acm.FCorporateActionElectionMultiItem):
        oldQuantity = getattr(row, 'Quantity')()
        elections = get_elections_for_position(row, row.PositionInstance())
        for e in elections:
            if activate:
                if e == row:
                    e.Percentage(100)
                    if epos:
                        e.Quantity(epos)
                else:
                    e.Percentage(0.0)
                    e.Quantity(0.0)                
            elif e == row:
                    e.Percentage(0.0)
                    e.Quantity(0.0)
            e.Commit()
        StateTransitionFromElectedQuantity(row, oldQuantity, epos)
    cell.GetEvaluator().RemoveSimulation()


def isTotalPercentage(election):
    return election.Percentage() == 100


def SummaryOfCAPositionStatus(childStatus):
    returnStatusIndex = CA_POSITION_STATES_ORDER.index('Processed')
    currentStatusIndex = -1
    for status in childStatus:
        currentStatusIndex = CA_POSITION_STATES_ORDER.index(status)
        if currentStatusIndex < returnStatusIndex:
            returnStatusIndex = currentStatusIndex
    if currentStatusIndex == -1:
        return None
    return CA_POSITION_STATES_ORDER[returnStatusIndex]


def saveCAElectionStatus(row, col, calcval, val, operation):
    if str(operation) == 'remove':
        val = 'Unknown'
    if val == 'Processed':
        calcval.GetEvaluator().RemoveSimulation()
        return
    colStrKey = col.StringKey()
    targetState = val
    if row.IsKindOf(acm.FCorporateActionElection) and colStrKey == 'Status':
        if val:
            positionBusinessProcessTransition(row, targetState)
        calcval.GetEvaluator().RemoveSimulation()
    elif row.IsKindOf(acm.FCorporateActionElectionMultiItem) and colStrKey == 'Status':
        if val:
            elections = row.Elections()
            elStatesList = []
            for election in elections:
                bp = FBDPCommon.GetBusinessProcess(election.Oid(), 'CorpActionElection')
                bpState = bp.CurrentStateName()
                elStatesList.append(bpState)
            elSet = set(elStatesList)
            if len(elSet) == 1:
                for election in elections:
                    positionBusinessProcessTransition(election, targetState)
        calcval.GetEvaluator().RemoveSimulation()


def SaveCAElectionDateTime(row, col, calcval, val, operation):
    if str(operation) == 'remove':
        val = '1970-01-01 00:00:00'
    colStrKey = col.StringKey()
    if row.IsKindOf(acm.FCorporateActionElection) and colStrKey in ['ReplyDate', 'Deadline']:
        dt = None
        try:
            dt = FBDPCommon.toDateTime(acm.Time.UtcToLocal(val))
        except:
            pass
        if dt:
            getattr(row, colStrKey)(dt)
            row.Commit()
        calcval.GetEvaluator().RemoveSimulation()
    elif row.IsKindOf(acm.FCorporateActionElectionMultiItem) and colStrKey in ['ReplyDate', 'Deadline']:
        dt = None
        try:
            dt = FBDPCommon.toDateTime(acm.Time.UtcToLocal(val))
        except:
            pass
        if dt:
            elections = row.Elections()
            for election in elections:
                getattr(election, colStrKey)(dt)
                elections.Commit()
        calcval.GetEvaluator().RemoveSimulation()


def SaveCAElectionTextInfo(row, col, calcval, val, operation):

    colStrKey = col.StringKey()
    if row.IsKindOf(acm.FCorporateActionElection) and colStrKey in ['TextInfo']:
        customText = getattr(row, colStrKey)()
        if not customText:
            customText = acm.FCustomTextObject()
            customText.Name(str(row.Oid()) + row.Name())
            row.TextInfo(customText)
            row.Commit()
        customText.Text(val)
        customText.Commit()
        calcval.GetEvaluator().RemoveSimulation()


def SaveCAElectionQuantity(row, col, calcval, val, operation):

    if str(operation) == 'remove':
        val = 0.0
    if not isinstance(val, (int, long, float, complex)):
        return

    pos = caEligiblePosition(row, None)
    if abs(pos + val) != abs(pos) + abs(val) or abs(val) > abs(pos):
        calcval.GetEvaluator().RemoveSimulation()
        return

    if row.IsKindOf(acm.FCorporateActionElection) and col.StringKey() == 'Quantity':
        oldQuantity = getattr(row, 'Quantity')()
        percentage = abs(val / pos * 100)
        
        if percentage <= 100:
            getattr(row, 'Quantity')(val)
            getattr(row, 'Percentage')(percentage)
            elections = get_elections_for_position(row, row.PositionInstance())
            total_percentage = find_total_percentage(elections)
            print 'total_percentage', total_percentage
            if total_percentage <= 100:
                row.Commit()
            else:
                getattr(row, 'Quantity')(0.0)
                getattr(row, 'Percentage')(0.0)
                row.Commit()
        StateTransitionFromElectedQuantity(row, oldQuantity, pos)
        calcval.GetEvaluator().RemoveSimulation()

def SaveCAElectionPrice(row, col, calcval, val, operation):

    if str(operation) == 'remove':
        val = 0.0
    if not isinstance(val, (int, long, float, complex)):
        return

    if row.IsKindOf(acm.FCorporateActionElection) and col.StringKey() == 'Price':
        getattr(row, 'Price')(val)
        row.Commit()
        calcval.GetEvaluator().RemoveSimulation()

def _GetEntityType(entity):

    entityType = None    
    if entity.IsKindOf(acm.FCorporateActionElection):
        entityType = 'CorpActionElection'
    elif entity.IsKindOf(acm.FCorporateAction):
        entityType = 'CorpAction'
    return entityType

def SaveCAAddInfoStr(row, col, calcval, val, operation):

    entityType = _GetEntityType(row)    
    if entityType:
        colStrKey = col.StringKey()
        AddInfoStr = FBDPCommon.SetAdditionalInfoValue(row,
                                                        entityType, 
                                                        colStrKey, 
                                                        val)
        AddInfoStr.Commit()
        calcval.GetEvaluator().RemoveSimulation()

def ElectionsForTheSamePosition(self):
    lastPosition = None
    for election in self.Elections():    
        posAddInfo = FBDPCommon.GetAdditionalInfoValue(election,
                                                   'CorpActionElection', 
                                                   'Position')
        if not lastPosition:
            lastPosition = posAddInfo
        elif lastPosition != posAddInfo:
            return False

    return True

