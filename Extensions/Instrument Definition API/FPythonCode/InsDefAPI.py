import acm
import functools

import NovateTrade as TA_NovateTrade

def UnsupportedTrades(*_args):
    '''
        Decorator for stopping action to be applied on unsupported trade types
        - Requires the trade to be the first argument of the decorated method
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def GroupRef(trade):
                assert not trade.GroupTrdnbr(), (
                    '%s is not currently not supported for '
                    'trade with Group References (e.g., B2B-covered trades)'
                    % (func.__name__)
                )
            
            def FXSwap(trade):
                assert not trade.IsFxSwap(), (
                    '%s is not currently not supported for FX Swaps' 
                    % (func.__name__)
                )
                
            checkers = {
                'GroupRef': GroupRef,
                'FXSwap': FXSwap
            }            
            
            trade = args[0]
            
            for a in _args:
                checker = checkers[a]
                checker(trade)                
            
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
    
def _CallMethodChain(methodChain, parameter, obj):
    methods = methodChain.split('.')
    for method in methods:
        if method == methods[-1]:
            obj.PerformWith(method, [parameter])
        else:
            obj = obj.PerformWith(method, [])
            
def _ApplyParameters(decorator, parameters):
    if parameters:
        for methodChain in parameters.Keys():
            _CallMethodChain(methodChain, parameters[methodChain], decorator)
        
def _GetAnswers(decorator, questions, answers):
    if answers:
        previousAnswers = acm.FDictionary()
        for question in questions:
            answer = GetAnswerAt(answers, question.QuestionId())
            validAnswers = question.Answers().Keys()
            if answer == None:
                if question.ValidatePrerequisites(previousAnswers):
                    error = "Missing answer for question '" + question.QuestionId() + "' " + validAnswers
                    raise RuntimeError(error)
            else:
                if question.ValidatePrerequisites(previousAnswers):
                    if not answer in validAnswers:
                        error = "Invalid answer '" + answer + "' for '" + question.QuestionId() + "' " + validAnswers
                        raise RuntimeError(error)
                    question.AnswerId = answer
                    previousAnswers[acm.FSymbol(question.QuestionId())] = acm.FSymbol(answer)
                
    return questions

def _ActionFromSaveMethod(saveMethod):
    action = None
    if 'Save' == saveMethod:
        action = 'update'
    elif 'SaveNew' == saveMethod:
        action = 'create'
    elif 'Delete' == saveMethod:
        action = 'delete'
    else:
        error = "Invalid Save Method'" + saveMethod
        raise RuntimeError(error)
    return action
    
def _SaveWithPreCommitHook(saveMethod, decorator, answers, preCommitBlock, abortBlock):
    success = False
    decorator.PerformWith('Prepare'+saveMethod, [])
    questions = decorator.PerformWith(saveMethod+'Questions', [])
    answerList = _GetAnswers(decorator, questions, answers)
    if decorator.PerformWith('Apply'+saveMethod+'Answers', [answerList]):
        preCommitResult = None
        preCommitAborted = False
        if preCommitBlock:
            action = _ActionFromSaveMethod(saveMethod)
            preCommitArg = {'decorator':decorator, 'answers':answers, 'action':action}
            preCommitResult = preCommitBlock(preCommitArg)
            preCommitAborted = not preCommitResult
        if preCommitAborted:
            if abortBlock:
                abortBlock(preCommitResult)
        else:
            acm.BeginTransaction()
            try:
                decorator.PerformWith(saveMethod, [answerList])
                if preCommitResult and hasattr(preCommitResult, 'IsKindOf') and preCommitResult.IsKindOf('FDictionary'):
                    if 'commit' in preCommitResult:
                        preCommitResult['commit'].Commit()
                    if 'delete' in preCommitResult:
                        preCommitResult['delete'].Delete()
                acm.CommitTransaction()
            except Exception as e:
                acm.AbortTransaction()
                if abortBlock:
                    abortBlock(preCommitResult)
                raise(e)
                
            success = True
    
    return success
        
def _CreateInstrument(instrument, parameters, answers, preCommitBlock, abortBlock):
    decorator = acm.FBusinessLogicDecorator.WrapObject(instrument)
    _ApplyParameters(decorator, parameters)
    success = _SaveWithPreCommitHook('SaveNew', decorator, answers, preCommitBlock, abortBlock)
    return instrument if success else None

def _CreateTrade(trade, parameters, answers, preCommitBlock, abortBlock):
    decorator = acm.FBusinessLogicDecorator.WrapObject(trade)
    _ApplyParameters(decorator, parameters)
    success = _SaveWithPreCommitHook('SaveNew', decorator, answers, preCommitBlock, abortBlock)
    return trade if success else None
            
def CreateInstrument(type, parameters, answers, preCommitBlock, abortBlock):
    instrument = acm.DealCapturing.CreateNewInstrument(type)
    return _CreateInstrument(instrument, parameters, answers, preCommitBlock, abortBlock)

def CreateInstrumentFromTemplate(template, parameters, answers, preCommitBlock, abortBlock):
    if not template:
        raise RuntimeError('Template is missing')        
    if template.Originator().IsInfant():
        instrument = template.StorageNew()
    else:
        instrument = template.StorageImage()
    instrument.InitializeUniqueIdentifiers()
    return _CreateInstrument(instrument, parameters, answers, preCommitBlock, abortBlock)
    
def CreateTrade(instrument, parameters, answers, preCommitBlock, abortBlock):
    trade = acm.DealCapturing.CreateNewTrade(instrument)
    return _CreateTrade(trade, parameters, answers, preCommitBlock, abortBlock)

def CreateTradeFromTemplate(template, parameters, answers, preCommitBlock, abortBlock):
    if not template:
        raise RuntimeError('Template is missing')        
    if template.Originator().IsInfant():
        trade = template.StorageNew()
    else:
        trade = template.StorageImage()
    trade.InitializeUniqueIdentifiers()
    return _CreateTrade(trade, parameters, answers, preCommitBlock, abortBlock)
    
def UpdateInstrument(instrument, parameters, answers, preCommitBlock, abortBlock):
    decorator = acm.FBusinessLogicDecorator.WrapObject(instrument).Edit()
    _ApplyParameters(decorator, parameters)
    _SaveWithPreCommitHook('Save', decorator, answers, preCommitBlock, abortBlock)
    return instrument

@UnsupportedTrades('GroupRef', 'FXSwap')    
def UpdateTrade(trade, parameters, answers, preCommitBlock, abortBlock):
    decorator = acm.FBusinessLogicDecorator.WrapObject(trade).Edit()
    _ApplyParameters(decorator, parameters)
    _SaveWithPreCommitHook('Save', decorator, answers, preCommitBlock, abortBlock)
    return trade

@UnsupportedTrades('GroupRef', 'FXSwap')    
def CorrectTrade(trade, reason1, reason2, parameters, answers, preCommitBlock, abortBlock):
    if not reason1:
        raise ValueError('Must enter reason for correction')
    tradeDecorator = acm.FBusinessLogicDecorator.WrapObject(trade).Edit()
    dict = acm.TradeActions.CorrectTrade(tradeDecorator)
    correcting = dict['correcting']
    original = dict['original']
    correctingDecorator = acm.FBusinessLogicDecorator.WrapObject(correcting)
    correctingDecorator.TradeTime = original.TradeTime()
    correctingDecorator.ValueDay = original.ValueDay()
    correctingDecorator.AcquireDay = original.AcquireDay()
    original.Text1 = reason1
    if reason2:
        original.Text2 = reason2
    original.CorrectionTrade = original
    _ApplyParameters(correctingDecorator, parameters)
    
    acm.BeginTransaction()
    
    try:
        original.Commit()
        
        commit = _SaveWithPreCommitHook(
            'SaveNew', 
            correctingDecorator,
            answers, 
            preCommitBlock, 
            abortBlock)
            
        if not commit:
            msg = 'The transaction was aborted by the user.'
            raise RuntimeError(msg)
            
        if 'farLegOriginal' in dict:
            dict['farLegOriginal'].Commit()
            
        if 'farLegCorrecting' in dict:
            dict['farLegCorrecting'].Commit()

        dict['businessEvent'].Commit()
        
            
        acm.CommitTransaction()
        
    except Exception as e:
        acm.AbortTransaction()
        raise(e)

    
    return correcting

@UnsupportedTrades('GroupRef', 'FXSwap')
def CloseTrade(trade, acquireDay, valueDay, nominal, payments):
    def Validate(trade):
        msg = acm.TradeActionUtil().ValidateTradeToClose(trade)
        if msg:
            raise RuntimeError(msg)
    
    class Params(object):
        def __init__(self, trade, acquireDay, valueDay, nominal, payments):
            FCM = acm.FCalculationMethods()
            
            self._spaceCollection = FCM.CreateStandardCalculationsSpaceCollection()
            
            self._trade = trade
            self._acquireDay = acquireDay
            self._valueDay = valueDay
            self.nominal = nominal 
            self.payments = payments

        @property
        def acquireDay(self):
            return self._acquireDay

        @property
        def valueDay(self):
            return self._valueDay
        
        @property    
        def nominal(self):
            return self._nominal
            
        @property    
        def payments(self):
            return self._payments
        
        @property
        def premium(self):
            premium = 0.0
            if not self.payments:
                t = acm.FBusinessLogicDecorator.WrapObject(self._trade).Edit()
                t.Nominal(self.nominal)
                p = t.Calculation().PriceToPremium(
                    self._spaceCollection,
                    self.valueDay, 
                    t.Price())
                premium = p.Number()
            return premium
            
        @nominal.setter
        def nominal(self, val):
            if not val:
                val = acm.TradeActionUtil.RemainingNominal(
                    self._trade,
                    self.acquireDay, 
                    self.valueDay)
                    
            self._nominal = -1.0 * val
            
        @payments.setter
        def payments(self, pmts):
            def ModifyPmts(pmts):
                def PV():
                    t = acm.FBusinessLogicDecorator.WrapObject(self._trade).Edit()
                    t.Nominal(self.nominal)
                    t.Premium(0.0)
                    _pv = t.Calculation().PresentValueSource(self._spaceCollection)
                    pv = _pv.Value()
                    return pv
                    
                def CreatePV(p):
                    if (p.Type() == 'Termination Fee' and p.Amount() == 0.0):
                        p.Amount = -PV()
                        
                def SetDefaults(p):
                    if not p.Party():
                        p.Party(self._trade.Counterparty())
                    if not p.Currency():
                        p.Currency(self._trade.Instrument().Currency())
                        
                for p in pmts:
                    CreatePV(p)
                    SetDefaults(p)    
                        
            if pmts:
                if next((p for p in pmts if p.Oid() > 0), None):
                    msg = 'Invalid storage state of payment'
                    raise ValueError(msg)
                    
                if next((p for p in pmts if p.Type() == 'None'), None):
                    msg = 'Missing payment type for payment'
                    raise ValueError(msg) 
                                
                ModifyPmts(pmts)
                    
            self._payments = pmts

    Validate(trade)
    
    params = Params(trade, acquireDay, valueDay, nominal, payments)
    
    ct1 = acm.TradeActions.CloseTrade(
        trade, 
        params.acquireDay,    
        params.valueDay, 
        params.nominal, 
        params.premium, 
        params.payments)
    
    ct1deco = acm.FBusinessLogicDecorator.WrapObject(ct1).Edit()
    ct1deco.SaveNew()
    
    return ct1deco.Originator()

@UnsupportedTrades('GroupRef', 'FXSwap')    
def NovateTrade(
        trade, party, acquireDay, valueDay,
        nominal, payments1, payments2):
        
    def Validate(trade):
        msg = acm.TradeActionUtil().ValidateTradeToNovate(trade)
        if msg:
            raise RuntimeError(msg)
    
    class Params(object):
        def __init__(
                self, trade, acquireDay, valueDay, 
                nominal, party, payments1, payments2):
            FCM = acm.FCalculationMethods()
            
            self._spaceCollection = FCM.CreateStandardCalculationsSpaceCollection()
            
            self._trade = trade
            self._acquireDay = acquireDay
            self._valueDay = valueDay
            self._party = party
            self.nominal = nominal 
            self.payments1 = payments1
            self.payments2= payments2
            
        def _ValidatePayments(self, pmts, validParty):
            if pmts:
                if next((p for p in pmts if p.Party() != validParty), None):
                    msg = 'Invalid counterparty found in payments'
                    raise ValueError(msg)
                    
                if next((p for p in pmts if p.Type() == 'None'), None):
                    msg = 'Missing payment type found in payments'
                    raise ValueError(msg) 
                
                if next((p for p in pmts if p.Amount() == 0.0), None):
                    msg = 'Invalid amount value found in payments'
                    raise ValueError(msg)
        
        def _DefaultPayments(self, pmts):
            if pmts:
                for p in pmts:
                    if not p.Currency():
                        p.Currency(self._trade.Instrument().Currency())

        @property
        def acquireDay(self):
            return self._acquireDay

        @property
        def valueDay(self):
            return self._valueDay
        
        @property    
        def nominal(self):
            return self._nominal
            
        @property
        def party(self):
            return self._party
            
        @property    
        def payments1(self):
            return self._payments1
            
        @property    
        def payments2(self):
            return self._payments2
        
        @property
        def premium(self):
            t = acm.FBusinessLogicDecorator.WrapObject(self._trade).Edit()
            t.Nominal(self.nominal)
            p = t.Calculation().PriceToPremium(
                self._spaceCollection,
                self.valueDay, 
                t.Price())
            premium = p.Number()
            
            return premium
            
        @nominal.setter
        def nominal(self, val):
            if not val:
                val = acm.TradeActionUtil.RemainingNominal(
                    self._trade,
                    self.acquireDay, 
                    self.valueDay)
                    
            self._nominal = -1.0 * val
            
        @payments1.setter
        def payments1(self, pmts):
            validParty = self._trade.Counterparty()
            self._ValidatePayments(pmts, validParty)
            self._DefaultPayments(pmts)
                
            self._payments1 = pmts
            
        @payments2.setter
        def payments2(self, pmts):
            self._ValidatePayments(pmts, self.party)
            self._DefaultPayments(pmts)  
            
            self._payments2 = pmts

    Validate(trade)
    
    params = Params(
        trade, 
        acquireDay, 
        valueDay, 
        nominal, 
        party, 
        payments1, 
        payments2)
        
    ts = acm.TradeActions.NovateTrade(
        trade, 
        params.acquireDay,    
        params.valueDay, 
        params.nominal, 
        params.premium,
        params.party,
        params.payments1,
        params.payments2)
    
    nt1 = ts['Novated']
    nt2 = ts['Novated Assigned']
    
    nt1Deco = acm.FBusinessLogicDecorator.WrapObject(nt1).Edit()
    nt2Deco = acm.FBusinessLogicDecorator.WrapObject(nt2).Edit()
    
    acm.BeginTransaction()

    try:
        nt1Deco.SaveNew()
        nt2Deco.SaveNew()
        
        bel = acm.FArray()
        _bel = TA_NovateTrade.CreateBusinessEventAndLinks(
            trade, nt2Deco.Originator().Trade())
        bel.AddAll(_bel)
        bel.Commit()
        
        acm.CommitTransaction()
        
    except Exception as e:
        acm.AbortTransaction()
        raise(e)

    return nt1Deco.Originator().Trade(), nt2Deco.Originator().Trade()

@UnsupportedTrades('GroupRef', 'FXSwap')
def NovateTradeStepOut(trade, acquireDay, valueDay, nominal, payments):
    def Validate(trade):
        msg = acm.TradeActionUtil().ValidateTradeToNovate(trade)
        if msg:
            raise RuntimeError(msg)
    
    class Params(object):
        def __init__(self, trade, acquireDay, valueDay, nominal, payments):
            FCM = acm.FCalculationMethods()
            
            self._spaceCollection = FCM.CreateStandardCalculationsSpaceCollection()
            
            self._trade = trade
            self._acquireDay = acquireDay
            self._valueDay = valueDay
            self.nominal = nominal 
            self.payments = payments

        @property
        def acquireDay(self):
            return self._acquireDay

        @property
        def valueDay(self):
            return self._valueDay
        
        @property    
        def nominal(self):
            return self._nominal
            
        @property    
        def payments(self):
            return self._payments
        
        @property
        def premium(self):
            premium = 0.0
            t = acm.FBusinessLogicDecorator.WrapObject(self._trade).Edit()
            t.Nominal(self.nominal)
            p = t.Calculation().PriceToPremium(
                self._spaceCollection,
                self.valueDay, 
                t.Price())
            premium = p.Number()
            return premium
        
        @property
        def party(self):
            dummy = acm.FParty()
            return dummy
            
        @nominal.setter
        def nominal(self, val):
            if not val:
                val = acm.TradeActionUtil.RemainingNominal(
                    self._trade,
                    self.acquireDay, 
                    self.valueDay)
                    
            self._nominal = -1.0 * val
            
        @payments.setter
        def payments(self, pmts):
            def ModifyPmts(pmts):
                def PV():
                    t = acm.FBusinessLogicDecorator.WrapObject(self._trade).Edit()
                    t.Nominal(self.nominal)
                    t.Premium(0.0)
                    _pv = t.Calculation().PresentValueSource(self._spaceCollection)
                    pv = _pv.Value()
                    return pv
                        
                def SetDefaults(p):
                    if not p.Party():
                        p.Party(self._trade.Counterparty())
                    if not p.Currency():
                        p.Currency(self._trade.Trade().Currency())
                        
                for p in pmts:
                    SetDefaults(p)    
                        
            if pmts:
                if next((p for p in pmts if p.Oid() > 0), None):
                    msg = 'Invalid storage state of payment'
                    raise ValueError(msg)
                    
                if next((p for p in pmts if p.Type() == 'None'), None):
                    msg = 'Missing payment type for payment'
                    raise ValueError(msg) 
                                
                ModifyPmts(pmts)
                    
            self._payments = pmts

    Validate(trade)
    
    params = Params(trade, acquireDay, valueDay, nominal, payments)
    
    ct1 = acm.TradeActions.NovateTradeStepOut(
        trade, 
        params.acquireDay,    
        params.valueDay, 
        params.nominal, 
        params.premium, 
        params.party,
        params.payments)
    
    ct1deco = acm.FBusinessLogicDecorator.WrapObject(ct1).Edit()
    ct1deco.SaveNew()
    
    return ct1deco.Originator()
        
def GetAnswerAt(answers, key):
    dict = eval(answers.Text()) if answers.Text() else {}
    return dict[key] if key in dict else None
    
def SetAnswerAt(answers, key, value):
    dict = eval(answers.Text()) if answers.Text() else {}
    dict[key] = value
    answers.Text = str(dict)
    
