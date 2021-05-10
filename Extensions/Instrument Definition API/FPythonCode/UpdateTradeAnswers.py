import acm
from InsDefAPI import GetAnswerAt, SetAnswerAt

def CreateAnswersFromDict(dict):
    answers = acm.FUpdateTradeAnswers()
    for key in dict:
        SetAnswerAt(answers, key, dict[key])
    return answers
    
def GetReallySaveChangesAnswer(answers):
    return GetAnswerAt(answers, 'ReallySaveChanges')
    
def SetReallySaveChangesAnswer(answers, answer):
    SetAnswerAt(answers, 'ReallySaveChanges', answer)
    
def GetSaveTradeInStatusAnswer(answers):
    return GetAnswerAt(answers, 'SaveTradeInStatus')
    
def SetSaveTradeInStatusAnswer(answers, answer):
    SetAnswerAt(answers, 'SaveTradeInStatus', answer)
    
def GetAssignTradeToNewInstrumentAnswer(answers):
    return GetAnswerAt(answers, 'AssignTradeToNewInstrument')
    
def SetAssignTradeToNewInstrumentAnswer(answers, answer):
    SetAnswerAt(answers, 'AssignTradeToNewInstrument', answer)
    
def GetClosedSettlementsExistAnswer(answers):
    return GetAnswerAt(answers, 'ClosedSettlementsExist')
    
def SetClosedSettlementsExistAnswer(answers, answer):
    SetAnswerAt(answers, 'ClosedSettlementsExist', answer)
    
def GetTradeTimeAfterValueDayAnswer(answers):
    return GetAnswerAt(answers, 'TradeTimeAfterValueDay')
    
def SetTradeTimeAfterValueDayAnswer(answers, answer):
    SetAnswerAt(answers, 'TradeTimeAfterValueDay', answer)
