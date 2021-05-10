import acm
from InsDefAPI import GetAnswerAt, SetAnswerAt

def CreateAnswersFromDict(dict):
    answers = acm.FCreateInstrumentAnswers()
    for key in dict:
        SetAnswerAt(answers, key, dict[key])
    return answers
    
def GetAdjustExpiryAnswer(answers):
    return GetAnswerAt(answers, 'AdjustExpiry')
    
def SetAdjustExpiryAnswer(answers, answer):
    SetAnswerAt(answers, 'AdjustExpiry', answer)
    
def GetFloatRateReferenceExpiryAnswer(answers):
    return GetAnswerAt(answers, 'FloatRateReferenceExpiry')
    
def SetFloatRateReferenceExpiryAnswer(answers, answer):
    SetAnswerAt(answers, 'FloatRateReferenceExpiry', answer)
        
def GetCopyBaseSecurityCashFlowsAnswer(answers):
    return GetAnswerAt(answers, 'CopyBaseSecurityCashFlows')
    
def SetCopyBaseSecurityCashFlowsAnswer(answers, answer):
    SetAnswerAt(answers, 'CopyBaseSecurityCashFlows', answer)
    
def GetCopyBaseSecurityExerciseEventsAnswer(answers):
    return GetAnswerAt(answers, 'CopyBaseSecurityExerciseEvents')
    
def SetCopyBaseSecurityExerciseEventsAnswer(answers, answer):
    SetAnswerAt(answers, 'CopyBaseSecurityExerciseEvents', answer)
    
def GetCopyManuallyEditedCashFlowsAnswer(answers):
    return GetAnswerAt(answers, 'CopyManuallyEditedCashFlows')
    
def SetCopyManuallyEditedCashFlowsAnswer(answers, answer):
    SetAnswerAt(answers, 'CopyManuallyEditedCashFlows', answer)
