import acm
from InsDefAPI import GetAnswerAt, SetAnswerAt


def CreateAnswersFromDict(dict):
    answers = acm.FCreateTradeAnswers()
    for key in dict:
        SetAnswerAt(answers, key, dict[key])
    return answers

def GetOrderAmountExceededAnswer(answers):
    return GetAnswerAt(answers, 'OrderAmountExceeded')
    
def SetOrderAmountExceededAnswer(answers, answer):
    SetAnswerAt(answers, 'OrderAmountExceeded', answer)
    
def GetInvalidTradeStatusSetSimulatedAnswer(answers):
    return GetAnswerAt(answers, 'InvalidTradeStatusSetSimulated')
    
def SetInvalidTradeStatusSetSimulatedAnswer(answers, answer):
    SetAnswerAt(answers, 'InvalidTradeStatusSetSimulated', answer)
    
def GetReallyCreateNewTradeAnswer(answers):
    return GetAnswerAt(answers, 'ReallyCreateNewTrade')
    
def SetReallyCreateNewTradeAnswer(answers, answer):
    SetAnswerAt(answers, 'ReallyCreateNewTrade', answer)
    
def GetTradeTimeAfterValueDayAnswer(answers):
    return GetAnswerAt(answers, 'TradeTimeAfterValueDay')
    
def SetTradeTimeAfterValueDayAnswer(answers, answer):
    SetAnswerAt(answers, 'TradeTimeAfterValueDay', answer)
    
def GetSuggestBaseCurrencyEquivalentAnswer(answers):
    return GetAnswerAt(answers, 'SuggestBaseCurrencyEquivalent')
    
def SetSuggestBaseCurrencyEquivalentAnswer(answers, answer):
    SetAnswerAt(answers, 'SuggestBaseCurrencyEquivalent', answer)
    
