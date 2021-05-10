
# ----------------------------------
# Find instrument hooks
# ----------------------------------

import acm

def CustomFindInstrument(tempDeal):
    '''
    Customize the search for existing instruments on an instrment-by-instrument basis.
    I.e. for a strip that shoudl contain six components, the hook will be called six times.

    The tempDeal is a Deal wrapping a non persisted instrument that has been populated 
    with date entered in the commodity strip user interface.
    It should NOT be updated but used as an information on what to search for.
    
    Return values:
    - Return None to use the core default search logic.
    - If custom logic is used but no instrument is found, return the Instrument
      that was wrapped by the Deal sent to the method as input.
      Note: Do NOT return the Deal itself.
    - If custom logic is used and a matching instrument is found, return the instrument
      that was found. Note, do not return a storage image of the instrument.
    '''
    return None
        
def CustomFindInstruments(stripDealPackage, startDate, endDate):
    '''
    Customize the logic for generating / finding all instruments for the strip.
    
    Parameters:
    stripDealPackage - the strip deal package
    startDate - the start date for the strip
    endDate - the end date for the stripip
    
    Return values:
    - Return None to use the core logic for generating strip components
    - If custom logic is used return a list of instrument that should be
      included in the strip (either new or already existing instruments).
      
    Note: If the CustomFindInstruments extension point is used, the extension point 
          CustomFindInstrument is never called.
    
    '''
    return None
