import acm

class CreateStubResetEstimations(object):
    '''
    Helper class for SuggestStubHandlingHelper
    '''
    
    def __init__(self, helper, cashflow):
        self.helper = helper
        self.cf = cashflow
        self.fixOrEst = None
        
    def __call__(self):
        return self.sre
        
    @property
    def helper(self):
        return self._helper
        
    @helper.setter
    def helper(self, helper):
        self._helper = helper
        
    @property
    def cf(self):
        return self._cf
        
    @cf.setter
    def cf(self, cf):
        self._cf = cf
        
    @property
    def fixOrEst(self):
        return self._fixOrEst
        
    @fixOrEst.setter
    def fixOrEst(self, val):
        self._fixOrEst = val
        
    @property
    def method(self):
        m = None
        if self.fixOrEst == 'Estimation':
            m = 'Calculation Period'
        elif self.fixOrEst == 'Fixing':
            m = 'Closest'
        return m
        
    @property
    def sre(self):
        return self._StubEstimation()
        
    # Private methods
    def _AddTenors(self, sre, ft1, ft2):
        assert self.fixOrEst
        def Add(sre, ri, ri2 = None):
            sre = sre or acm.FStubResetEstimation()
            
            Method = getattr(sre, self.fixOrEst + 'Method')
            Ref1 = getattr(sre, self.fixOrEst + 'Ref1')
            Ref2 = getattr(sre, self.fixOrEst + 'Ref2')
            
            Ref1(ri)
            
            if ri2:
                Ref2(ri2)
                Method('Interpolate')
            else:
                Method(self.method)
            
            return sre
            
        if ft1 and ft2:
            sre = Add(sre, ft1, ft2)
        elif ft1 and not ft2:
            sre = Add(sre, ft1)
        elif ft2 and not ft1:
            sre = Add(sre, ft2)
            
        return sre
        
    def _Tenors(self, cf):
        def DeltaDays(cf, ri):
            delta =  self.helper._DeltaDays(
                cf.StartDate(),
                ri.FirstReceiveLeg().EndPeriod(),
                cf.EndDate()
            )
            return delta
            
        assert self.fixOrEst  
        ri1 = None
        ri2 = None
        refs = getattr(
            self.helper, 
            self.fixOrEst.lower() + 'Refs'
        )
        for ri in refs:
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
        
    def _StubEstimation(self):
        sre = None
        self.fixOrEst = 'Fixing'
        ft1, ft2 = self._Tenors(self.cf)
        sre = self._AddTenors(sre, ft1, ft2)
        
        self.fixOrEst = 'Estimation'
        ft1, ft2 = self._Tenors(self.cf)
        sre = self._AddTenors(sre, ft1, ft2)
            
        return sre
