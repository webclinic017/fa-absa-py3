
'''--------------------------------------------------------------------------------------------------------
Date                    : 2011-12-06
Purpose                 : This script refreshes the theoretical price for all Aqua instruments.  This is called from a button in a workbook column and forces the data in the workbook to refresh.
Department and Desk     : Front Office - Equity Derivatives
Requester               : Stephen Zoio and Andrey Chechin
Developer               : Paul Jacot-Guillarmod
CR Number               : 851489
--------------------------------------------------------------------------------------------------------'''

import acm

def CalculateTheoreticalPrice(instrument):
    ''' Calculate the theoretical price for an instrument.
    '''
    calculationSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    calculation = instrument.Calculation()
    calculation.TheoreticalPrice(calculationSpace)

def RefreshAquaInstruments(invokationInfo):
    query = acm.CreateFASQLQuery('FInstrument', 'OR')
    query.AddAttrNode('ValuationGrpChlItem.Name', 'EQUAL', 'AQUA_MEPDN_ED_OPTIONS')
    query.AddAttrNode('ValuationGrpChlItem.Name', 'EQUAL', 'AQUA_MEUAT_ED_OPTIONS')
    query.AddAttrNode('ValuationGrpChlItem.Name', 'EQUAL', 'AQUA_MEPDN_PV')
    query.AddAttrNode('ValuationGrpChlItem.Name', 'EQUAL', 'AQUA_MEGROUP_PV')
    
    for instrument in query.Select():
        CalculateTheoreticalPrice(instrument)

def wantButton(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    
    return True       
