import functools
import abc
import acm
from CreateStubResetEstimations import CreateStubResetEstimations
    
class cached_property(object): 
    #Descriptor (non-data) for building an attribute on-demand on first use.

    def __init__(self, factory):
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        attr = self._factory(instance)
        setattr(instance, self._attr_name, attr)

        return attr

def CurrentState(leg):
    return SuggestStubHandlingHelper.CurrentState(leg)
     
class SuggestStubHandlingHelper(object, metaclass=abc.ABCMeta):
    '''Abstract utility class for FStubHandling.SuggestStubHandlingHook

    Two derived classes are proposed: SuggestStubHandlingTriggered and
    SuggestStubHandlingAuto (cf. default FStubHandling for examples). Objects
    of these classes are proposed to be instantiated using
    SuggestStubHandlingHelper.Create(*args).

    '''
    
    def __init__(self, leg):
        self.leg = leg
        self.cf1 = leg
        self.cf2 = leg
        self.floatRateReference = leg
        self.isStub1 = (self.cf1, self.floatRateReference)
        self.isStub2 = (self.cf2, self.floatRateReference)
        self.valid = False
    
    # Abstract properties
    @abc.abstractproperty
    def aliasTypeFixing(self):  
        pass
        
    @abc.abstractproperty
    def threshold(self):
        pass
        
    @abc.abstractproperty
    def delimiter(self):
        pass

    # Decorators
    class Requires(object):

        @classmethod
        def initiated(cls, fun):
            @functools.wraps(fun)
            def inner(*args, **kw):
                s = args[0] # self
                res = None
                if (s.leg, s.cf1, s.cf2, s.floatRateReference):
                    res = fun(s)
                return res
            return inner
            
        @classmethod
        def valid(cls, fun):
            @functools.wraps(fun)
            def inner(*args, **kw):
                s = args[0] # self
                res = None
                if (s.valid):
                    res = fun(s)
                return res
            return inner
            
    # Setters / Getters
    @property
    def cf1(self):
        return self._cf1

    @cf1.setter
    def cf1(self, leg):
        cfs = SuggestStubHandlingHelper._CashFlows(leg)
        self._cf1 = None
        if cfs:
            self._cf1 = cfs.First()
        

    @property
    def cf2(self):
        return self._cf2
    
    @cf2.setter
    def cf2(self, leg):
        cfs = SuggestStubHandlingHelper._CashFlows(leg)
        self._cf2 = None
        if cfs:
            self._cf2 = cfs.Last()

    @property
    def floatRateReference(self):
        return self._floatRateReference

    @floatRateReference.setter
    def floatRateReference(self, leg):
        self._floatRateReference = leg.FloatRateReference()

    @property
    def isStub1(self):
        return self._isStub1
    
    @isStub1.setter
    def isStub1(self, vals):
        try:
            cf1, floatRateReference = vals
        except:
            raise ValueError('In SuggestStubHandlingHelper.isStub1')
        else:
            if not self.cf1:
                self._isStub1 = False
            else:
                self._isStub1 = self._IsStub(cf1, floatRateReference)

    @property
    def isStub2(self):
        return self._isStub2
    
    @isStub2.setter
    def isStub2(self, vals):
        try:
            cf2, floatRateReference = vals
        except:
            raise ValueError('In SuggestStubHandlingHelper.isStub2')
        else:
            if not self.cf2 or self.cf2 == self.cf1:
                self._isStub2 = False
            else:
                self._isStub2 = self._IsStub(cf2, floatRateReference)

    @property
    def valid(self):
        return self._valid
    
    @valid.setter
    def valid(self, val):
        self._valid = val

    @property
    def sre1(self):
        return self._sre1

    @sre1.setter
    def sre1(self, cf1):
        self._sre1 = None
        if self.isStub1:
            helper = CreateStubResetEstimations(self, cf1)
            self._sre1 = helper()
    
    @property
    def sre2(self):
        return self._sre2

    @sre2.setter
    def sre2(self, cf2):
        self._sre2 = None
        if self.isStub2:
            helper = CreateStubResetEstimations(self, cf2)
            self._sre2 = helper()

    @cached_property
    def family(self):
        family = None
        if acm.FInstrAliasType[self.aliasTypeFixing]:
            alias = self.floatRateReference.Alias(self.aliasTypeFixing)
            if alias:
                family = self._Parse(alias)
                msg = (
                    'Failed to suggest stub handling: '
                    'Unsuccessful in parsing alias ' + alias 
                    + ' to a rate index family using delimiter "' 
                    + self.delimiter + '".') 
                assert family, msg
        return family

    @cached_property
    def fixingRefs(self):
        ris = acm.FArray()
        if self.family:
            q = 'type="%s" and alias like "*%s*"' % (
                self.aliasTypeFixing, self.family)
            aliases = acm.FInstrumentAlias.Select(q)
            ris = aliases.Transform('Instrument', 'FArray', None)
            
            msg = (
                'Failed to suggest stub handling: '
                'No related fixing references found.')
            assert ris, msg
            msg = (
                'Failed to suggest stub handling: '
                'Only one rate index was found in '
                + self.aliasTypeFixing + '.')
            assert len(ris) > 1, msg

        return ris
    
    @cached_property
    def estimationRefs(self):
        ris = acm.FArray()
        if self.family:
            q = 'type="%s" and alias like "*%s*"' % (
                self.aliasTypeEstimation, self.family)
            aliases = acm.FInstrumentAlias.Select(q)
            ris = aliases.Transform('Instrument', 'FArray', None)
     
            if not ris:
                '''
                Motivation: If no Estimation Ref is available, 
                set Estimation Ref to Float Rate Ref. This yields the 
                same fwd estimation (i.e., forward curve) as all other 
                cash flows on the leg. 
                At the moment, this is assumed the best fall-back.
                '''
                ris.Add(self.floatRateReference)

        return ris
        
    # Class methods
    @classmethod
    def Create(cls, params, autoClass, triggeredClass):
        '''Factory method for instantiation of objects of derived classes.

        Args:
            params (FArray):
                params[0] (FLeg): The leg that will be considered for stub
                handling. The leg has passed default validation for stub reset
                estimation (e.g., has a valid leg type, is not generic, has
                float rate reference, etc.)
                params[1] (str): "auto" if called when a field on the leg has
                been updated. "triggered" if the suggest-button was clicked.
            autoClass (class): Handle to definition of class implementing
            functionallity that will be run when in "auto" mode

            triggeredClass (class): Handle to definition of class implementing

            functionallity that will be run when in "triggered" mode

        Returns:
            object of autoClass or triggeredClass

        Example:
            See FStubHandling for an example use of this method
        '''

        def Unpack(params):
            obj = None
            modes = ('auto', 'triggered')
            assert len(params) == 2
            leg = params[0]
            mode = params[1]
            assert hasattr(leg, 'IsKindOf') and leg.IsKindOf(acm.FLeg)
            assert isinstance(mode, str)
            assert mode in modes
            return leg, mode
            
        leg, mode = Unpack(params)
        
        if mode == 'triggered':
            obj = triggeredClass(leg)
        if mode == 'auto':
            obj = autoClass(leg)
        return obj 
        
    @classmethod
    def CurrentState(cls, leg):
        '''
        Extension point for definition of what field changes that should
        trigger the FStubHandling.SuggestStubHandlingHook to be called when in
        "auto" mode. In the Instrument definition, a change on any field of
        the leg will trigger a call to this function. If the any of the values
        in the returning dictionary has changed,
        FStubHandling.SuggestStubHandlingHook will be called.

        Args:
            leg (FLeg): The leg that will be considered for stub
            handling. Note: Forbidden to modify.

        Returns:     
            FDictionary with arbitrary keys. Values of the
            FDictionary are fields where a change should trigger the
            StubHandling.SuggestStubHandlingHook to be called.
            
        Note:
        Since this method is called only when a leg field has been updated in
        the Instrument definition, adding any value that is leg field is not
        supported. I.e., adding leg.Instrument().Currency() to the dictionary
        is not supported.
        
        '''

        assert hasattr(leg, 'IsKindOf') and leg.IsKindOf(acm.FLeg)
        
        dict = acm.FDictionary()
        
        dict.AtPut('FloatRateRef', leg.FloatRateReference())
        dict.AtPut('LegType', leg.LegType())
        dict.AtPut('Rolling', leg.RollingPeriod())
        
        cfs = SuggestStubHandlingHelper._CashFlows(leg)
        if cfs:
            dict.AtPut('Cf1StartDate', cfs.First().StartDate())
            dict.AtPut('Cf2StartDate', cfs.Last().StartDate())
            dict.AtPut('Cf1EndDate', cfs.First().EndDate())
            dict.AtPut('Cf2EndDate', cfs.Last().EndDate())
        
        return dict
        
    @staticmethod    
    def _CashFlows(leg):
        cfs = None
        orgArr = leg.CashFlows()
        if orgArr:
            sortArr = orgArr.SortByProperty('StartDate')
            newArr = acm.FArray()
            for cf in sortArr:
                if SuggestStubHandlingHelper._ValidCashflow(cf):
                    newArr.Add(cf)
            cfs = newArr
        return cfs
    
    @staticmethod
    def _ValidCashflow(cf):
        valid = cf.StartDate() and cf.EndDate()
        return valid

    # Private methods        
    def _DeltaDays(self, ref, t1, t2):
        def IsPeriod(t): return t[-1].isalpha()
        
        if IsPeriod(t1):
            t1 = acm.Time.DateAdjustPeriod(ref, t1)
        if IsPeriod(t2):
            t2 = acm.Time.DateAdjustPeriod(ref, t2)
            
        d1 = acm.Time.DateDifference(ref, t1)
        d2 = acm.Time.DateDifference(ref, t2)
        
        delta = abs(d1) - abs(d2)
        
        return delta
        
    def _IsStub(self, cf, floatRateReference):
        isStub = False
        if cf and floatRateReference:
            d1 = abs(
                self._DeltaDays(
                    cf.StartDate(), 
                    cf.EndDate(), 
                    floatRateReference.FirstReceiveLeg().EndPeriod()
                )
            )
            d2 = abs(
                self._DeltaDays(
                    acm.Time.DateToday(),
                    self.floatRateReference.FirstReceiveLeg().EndPeriod(), 
                    self.leg.RollingPeriod()
                )
            )
            if (d1 > self.threshold and d2 < self.threshold):
                isStub = True
                
        return isStub

    def _Parse(self, alias):
        tmp = alias.split(self.delimiter)
        del tmp[-1]
        familyName = self.delimiter.join(tmp)
        return familyName

    # Public methods
    @Requires.initiated
    @Requires.valid
    def GetStubs(self):
        sres = acm.FDictionary()
        self.sre1 = self.cf1
        self.sre2 = self.cf2
        sres.AtPut('First', self.sre1)
        sres.AtPut('Last', self.sre2)

        return sres
        
    @abc.abstractmethod
    @Requires.initiated
    def Validate(self):
        pass
