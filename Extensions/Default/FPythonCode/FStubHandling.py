'''Default hook for automated Stub Handling

This module implements the SuggestStubHandlingHook, enabling automated stub
handling. The default implementation suggests the use of instrument alias
types STUB_FIXING and STUB_ESTIMATION for grouping of rate indices. Aliases
of these two types should follow a naming convention, defaulted to:
FAMILYNAME-TENOR, with e.g., FAMILYNAME=EUR-EURIBOR and TENOR is a valid
period, e.g., 3M (resulting in an alias  value “EURIBOR-3M”). A STUB_ESTIMATION 
alias is used to define a valid rate index for stub (forward rate) estimation. 
Likewise, a STUB_FIXING alias is used to define a valid rate index for stub fixing 

Example: 
    Swap A has a float leg with float rate ref=EUR/EURIBOR/6M. EUR/EURIBOR/6M
    has STUB_FIXING= EURIBOR-6M and STUB_ESTIMATION= EURIBOR-6M. Rate
    indices EUR/EURIBOR/1M and EUR/EURIBOR/3M also exist with corresponding
    STUB_FIXING/STUB_ESTIMATION aliases. EUR/EURIBOR/1M and EUR/EURIBOR/3M are
    then considered available for use in stub handling, both for fixing and
    estimating first/last reset(s). 

Two modes for stub handling are available: "Triggered" and "Automatic". The
SuggestStubHandlingHook is run in "Triggered" mode when the Resets...>Stub
Handling>Suggest-button is clicked in an instrument definition. "Automatic"
mode is run when a relevant leg-field is updated. 

The default implementation further demonstrates the
proposed use of the utility class SuggestStubHandlingHelper.
'''

import acm
from SuggestStubHandlingHelper import SuggestStubHandlingHelper

class SuggestStubHandlingTriggered(SuggestStubHandlingHelper):

    # Abstract properties      
    @property
    def aliasTypeFixing(self):
        return 'STUB_FIXING'
        
    @property
    def aliasTypeEstimation(self):
        return 'STUB_ESTIMATION'
        
    @property
    def threshold(self):
        return 5
        
    @property
    def delimiter(self):
        return '-'
    
    # Abstract methods
    def Validate(self):
        self.valid = True
        
        if self.floatRateReference and not self.family:
            msg = (
                'No alias of type '
                + self.aliasTypeFixing
                + ' found on ' 
                + self.floatRateReference.Name())
            raise AssertionError(msg)


class SuggestStubHandlingAuto(SuggestStubHandlingTriggered):
    
    @property
    def invalidInstrumentTypes(self):
        lst = [
            'FRN',
            'PromisLoan',
            'CLN'
        ]
        return lst
    
    # Abstract methods
    def Validate(self):
        self.valid = True
        
        ins = self.leg.Instrument()
        insType = ins.InsType()
        
        if insType in self.invalidInstrumentTypes:
            self.valid = False
    
def SuggestStubHandlingHook(*params):
    '''Extension point for automated stub handling
    
    Args:
        *params (FArray):
            params[0] (FLeg): The leg that will be considered for stub
            handling. The leg has passed default validation for stub reset
            estimation (e.g., has a valid leg type, is not generic, has float
            rate reference, etc.). Note: Forbidden to modify.

            params[1] (str): "auto" if called when a field on the leg has been
            updated. "triggered" if the suggest-button was clicked.
    Returns:
        FDictionary(FStubResetEstimation):
            Keys (str): "First" for first FStubResetEstimation. "Last" for last
            FStubResetEstimation.
            Values (FStubResetEstimation): Container for the actual
            FStubResetEstimation that will be set on the leg. Attributes Fixin
            gMethod/EstimationMethod/FixingRef1/FixingRef2/EstimationRef1/Esti
            mationRef2 should be set in a valid manner on the
            FStubResetEstimation for a later validation to pass. Note: the
            actual FStubResetEstimation objects created within the hook are
            nothing but templates for the FStubResetEstimation that will be
            set on the leg.
        None: ignore the call to this hook. 

    Raises:
        Raised exceptions within the hook are catched in a sensible manner.

    Examples:
        def SuggestStubHandlingHook(*params):
            # Will set the stub handling to First with fixing/estimation
            # method/references according to the FStubResetEstimation
            stubs = acm.FDictionary()
            
            sre1 = acm.FStubResetEstimation()
            sre1.EstimationMethod('Interpolate')
            sre1.EstimationRef1('EUR/EURIBOR/1M')
            sre1.EstimationRef2('EUR/EURIBOR/3M')
            sre1.FixingMethod('Closest')
            sre1.FixingRef1('EUR/EURIBOR/1M')
            
            stubs.AtPut('First', sre1)
            stubs.AtPut('Last', None)

            return stubs
            
        def SuggestStubHandlingHook(*params):
            # Will ignore the call, nothing will be done.
            return None

        def SuggestStubHandlingHook(*params):
            # Stub handling None will be suggested
            stubs = acm.FDictionary()

            stubs.AtPut('First', None)
            stubs.AtPut('Last', None)

            return stubs

        def SuggestStubHandlingHook(*params):
            # Will complain that the first FStubResetEstimation is invalid
            # (missing attributes)
            stubs = acm.FDictionary()
            
            sre1 = acm.FStubResetEstimation()

            stubs.AtPut('First', sre1)
            stubs.AtPut('Last', None)

            return stubs
    '''
    h = SuggestStubHandlingHelper.Create(
            params, 
            SuggestStubHandlingAuto,
            SuggestStubHandlingTriggered
    )
    h.Validate()
    stubs = h.GetStubs()

    return stubs
