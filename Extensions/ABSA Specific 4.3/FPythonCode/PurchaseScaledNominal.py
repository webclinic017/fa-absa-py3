# This script is used to create the column "Purchase Scaled Nominal" for 
# Index linked bonds. As per JIRA, ABITFA - 4780
# Example trade = 12230102
# Example portfolio = "GT Gov Inflation"

import acm

cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()

def getScaledNominal(trade):    
    date = trade.ValueDay()
    nominal = trade.Quantity() * 1000000 
    ins = trade.Instrument()
    leg = ins.Legs()[0]
    initial_index_value = leg.InitialIndexValue()
    cpi_reference = leg.IndexRef()
    current_cpi_value = cpi_reference.Calculation().ForwardPrice(cs, date).Number()
    cpi_scalar = float(current_cpi_value) / float(initial_index_value)
    scaled_nominal = nominal * cpi_scalar
    return scaled_nominal
