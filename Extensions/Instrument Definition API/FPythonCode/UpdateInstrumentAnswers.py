import acm
from InsDefAPI import GetAnswerAt, SetAnswerAt


def CreateAnswersFromDict(dict):
    answers = acm.FUpdateInstrumentAnswers()
    for key in dict:
        SetAnswerAt(answers, key, dict[key])
    return answers
    
def GetNameChangedAnswer(answers):
    return GetAnswerAt(answers, 'NameChanged')
    
def SetNameChangedAnswer(answers, answer):
    SetAnswerAt(answers, 'NameChanged', answer)
    
def GetAdjustExpiryAnswer(answers):
    return GetAnswerAt(answers, 'AdjustExpiry')
    
def SetAdjustExpiryAnswer(answers, answer):
    SetAnswerAt(answers, 'AdjustExpiry', answer)
    
def GetFloatRateReferenceExpiryAnswer(answers):
    return GetAnswerAt(answers, 'FloatRateReferenceExpiry')
    
def SetFloatRateReferenceExpiryAnswer(answers, answer):
    SetAnswerAt(answers, 'FloatRateReferenceExpiry', answer)
    
def GetQuotationChangedAnswer(answers):
    return GetAnswerAt(answers, 'QuotationChanged')
    
def SetQuotationChangedAnswer(answers, answer):
    SetAnswerAt(answers, 'QuotationChanged', answer)
    
def GetClosedSettlementsExistAnswer(answers):
    return GetAnswerAt(answers, 'ClosedSettlementsExist')
    
def SetClosedSettlementsExistAnswer(answers, answer):
    SetAnswerAt(answers, 'ClosedSettlementsExist', answer)
    
def GetRegenerateCashFlowsAnswer(answers):
    return GetAnswerAt(answers, 'RegenerateCashFlows')
    
def SetRegenerateCashFlowsAnswer(answers, answer):
    SetAnswerAt(answers, 'RegenerateCashFlows', answer)
    
def GetFixedResetsExistRegenerateAllAnswer(answers):
    return GetAnswerAt(answers, 'FixedResetsExistGenerateAll')
    
def SetFixedResetsExistRegenerateAllAnswer(answers, answer):
    SetAnswerAt(answers, 'FixedResetsExistGenerateAll', answer) 

def GetFixedResetsExistRegenerateFutureAnswer(answers):
    return GetAnswerAt(answers, 'FixedResetsExistGenerateFuture')
    
def SetFixedResetsExistRegenerateFutureAnswer(answers, answer):
    SetAnswerAt(answers, 'FixedResetsExistGenerateFuture', answer) 

def GetSetFixedRateAnswer(answers):
    return GetAnswerAt(answers, 'SetFixedRate')
    
def SetSetFixedRateAnswer(answers, answer):
    SetAnswerAt(answers, 'SetFixedRate', answer)   

def GetSetStrikeAnswer(answers):
    return GetAnswerAt(answers, 'SetStrike')
    
def SetSetStrikeAnswer(answers, answer):
    SetAnswerAt(answers, 'SetStrike', answer)   

def GetSetStrike2Answer(answers):
    return GetAnswerAt(answers, 'SetStrike2')
    
def SetSetStrike2Answer(answers, answer):
    SetAnswerAt(answers, 'SetStrike2', answer)  

def GetSetSpreadAnswer(answers):
    return GetAnswerAt(answers, 'SetSpread')
    
def SetSetSpreadAnswer(answers, answer):
    SetAnswerAt(answers, 'SetSpread', answer)  
    
def GetSetSpread2Answer(answers):
    return GetAnswerAt(answers, 'SetSpread2')
    
def SetSetSpread2Answer(answers, answer):
    SetAnswerAt(answers, 'SetSpread2', answer) 
    
def GetRegenerateDividendCashFlowsAnswer(answers):
    return GetAnswerAt(answers, 'RegenerateDividendCashFlows')
    
def SetRegenerateDividendCashFlowsAnswer(answers, answer):
    SetAnswerAt(answers, 'RegenerateDividendCashFlows', answer)
