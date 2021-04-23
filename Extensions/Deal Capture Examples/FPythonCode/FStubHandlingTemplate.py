import functools
import acm

class cached_property(object):
    """
    Descriptor (non-data) for building an attribute on-demand on first use.
    """
    def __init__(self, factory):
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        attr = self._factory(instance)
        setattr(instance, self._attr_name, attr)

        return attr


class SuggestStubHandlingHelper(object):

    THRESHOLD = 5
    ALIAS_TYPE = 'IndexFamily'
    VALID_INSTRS = ['FSwap']
    VALID_CURRS = ['EUR', 'DKK']
    VALID_LEG_TYPES = [
        'Float', 'Cap', 'Floor',
        'Capped Float', 'Floored Float',
        'Collared Float', 'Reverse Float']
    VALID_CF_TYPES = [
        'Float Rate', 'Caplet', 'Floorlet',
        'Digital Caplet', 'Digital Floorlet',
        'Call Float Rate', 'Collared Float',
        'Float Price']
    
    def __init__(self, leg):
        self.leg = leg
        self.cf1 = leg
        self.cf2 = leg
        self.frr = leg
        self.isStub1 = (self.cf1, self.frr)
        self.isStub2 = (self.cf2, self.frr)
        self.valid = False

    # Decorators
    class Requires(object):
    
        @classmethod
        def initiated(cls, fun):
            @functools.wraps(fun)
            def inner(*args, **kw):
                s = args[0] # self
                res = None
                if (s.leg, s.cf1, s.cf2, s.frr):
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
        cfs = leg.CashFlows().SortByProperty('StartDate')
        self._cf1 = cfs.First() 

    @property
    def cf2(self):
        return self._cf2
    
    @cf2.setter
    def cf2(self, leg):
        cfs = leg.CashFlows().SortByProperty('StartDate')
        self._cf2 = cfs.Last()

    @property
    def frr(self):
        return self._frr

    @frr.setter
    def frr(self, leg):
        self._frr = leg.FloatRateReference()

    @property
    def isStub1(self):
        return self._isStub1
    
    @isStub1.setter
    def isStub1(self, vals):
        try:
            cf1, frr = vals
        except:
            raise ValueError('In SuggestStubHandlingHelper.isStub1')
        else:
            self._isStub1 = self._IsStub(cf1, frr)

    @property
    def isStub2(self):
        return self._isStub2
    
    @isStub2.setter
    def isStub2(self, vals):
        try:
            cf2, frr = vals
        except:
            raise ValueError('In SuggestStubHandlingHelper.isStub2')
        else:
            self._isStub2 = self._IsStub(cf2, frr)

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
            self._sre1 = self._StubEstimation(cf1)
    
    @property
    def sre2(self):
        return self._sre2

    @sre2.setter
    def sre2(self, cf2):
        self._sre2 = None
        if self.isStub2:
            self._sre2 = self._StubEstimation(cf2)

    @cached_property
    def frrFamily(self):
        alias = self.frr.Alias(SuggestStubHandlingHelper.ALIAS_TYPE)
        msg = (
            'Failed to suggest stub handling: '
            'No alias of type ' + SuggestStubHandlingHelper.ALIAS_TYPE
            + ' was found on ' + self.frr.Name() + '')
        assert alias, msg
        family = self._RemoveTenor(alias)
        return family

    @cached_property
    def rateIndecies(self):
        ris = acm.FArray()
        q = 'type="IndexFamily" and alias like "*%s*"' % self.frrFamily
        aliases = acm.FInstrumentAlias.Select(q)
        ris = aliases.Transform('Instrument', 'FArray', None)
        
        msg = (
            'Failed to suggest stub handling: '
            'No related rate indecies found.')
        assert ris, msg
        msg = (
            'Failed to suggest stub handling: '
            'Only one rate index was found in '
            + SuggestStubHandlingHelper.ALIAS_TYPE + '.')
        assert len(ris) > 1, msg

        return ris
        
    # Private methods
    def _IsStub(self, cf, frr):
        isStub = False
        if cf and frr:
            threshold = SuggestStubHandlingHelper.THRESHOLD
            isStub = abs(self._DeltaDays(cf, frr)) > threshold
        return isStub

    def _DeltaDays(self, cf, ri):
        riEndDate = acm.Time.DateAdjustPeriod(
            cf.StartDate(), ri.FirstReceiveLeg().EndPeriod())
        riDays = abs(acm.Time.DateDifference(cf.StartDate(), riEndDate))
        cfDays = abs(acm.Time.DateDifference(cf.StartDate(), cf.EndDate()))

        days = riDays - cfDays

        return days

    def _RemoveTenor(self, alias):
        tmp = alias.split('-')
        del tmp[-1]
        familyName = ''.join(tmp)
        return familyName

    def _Refs(self, cf):
        ri1 = None
        ri2 = None
        DeltaDays = self._DeltaDays
        for ri in self.rateIndecies:
            if DeltaDays(cf, ri) < 0:
                ri1 = ri if (
                    not ri1 
                    or abs(DeltaDays(cf, ri)) < abs(DeltaDays(cf, ri1))
                ) else ri1
            else:
                ri2 = ri if (
                    not ri2 
                    or abs(DeltaDays(cf, ri)) < abs(DeltaDays(cf, ri2))
                ) else ri2
        return ri1, ri2

    def _StubEstimation(self, cf):
        def CreateClosest(ri):
            sre = acm.FStubResetEstimation()
            sre.FixingMethod("Closest")
            sre.FixingRef1(ri)
            sre.EstimationMethod("Closest")
            sre.EstimationRef1(ri)
            return sre
        
        sre = None
        ri1, ri2 = self._Refs(cf)
        if ri1 and ri2:
            sre = acm.FStubResetEstimation()
            sre.FixingMethod("Interpolate")
            sre.FixingRef1(ri1)
            sre.FixingRef2(ri2)
            sre.EstimationMethod("Interpolate")
            sre.EstimationRef1(ri1)
            sre.EstimationRef2(ri2)
        if ri1 and not ri2:
            sre = CreateClosest(ri1)
        if ri2 and not ri1:
            sre = CreateClosest(ri2)
        return sre

    # Public methods
    @Requires.initiated
    def Validate(self):
        validInstrs = SuggestStubHandlingHelper.VALID_INSTRS
        validCurrs = SuggestStubHandlingHelper.VALID_CURRS
        validLegTypes = SuggestStubHandlingHelper.VALID_LEG_TYPES
        validCfTypes = SuggestStubHandlingHelper.VALID_CF_TYPES
        
        self.valid = True
        
        if (not self.leg.Instrument().ClassName().Text() in validInstrs
            or not self.leg.Currency().Name() in validCurrs
            or not self.leg.LegType() in validLegTypes
            or not self.cf1.CashFlowType() in validCfTypes
            or not self.cf2.CashFlowType() in validCfTypes
        ):
            self.valid = False
    
    @Requires.initiated
    @Requires.valid
    def GetStubs(self):
        sres = acm.FDictionary()
        self.sre1 = self.cf1
        self.sre2 = self.cf2
        sres.AtPut('First', self.sre1)
        sres.AtPut('Last', self.sre2)

        return sres

def SuggestStubHandlingHook(leg):
    h = SuggestStubHandlingHelper(leg)
    
    h.Validate()
    stubs = h.GetStubs()

    return stubs

