"""-----------------------------------------------------------------------
MODULE
    Structured_SwapParRate

DESCRIPTION
    Date                : 2010-12-09
    Purpose             : The Par Rate of a combination instrument, that has two underlying Swaps, will be calculated and displayed in the log
    Department and Desk : Structered Desk
    Requester           : Yalusa Jongihlati
    Developer           : Herman Hoon
    CR Number           : 519986 

HISTORY
================================================================================
Date            Change no    Developer          Description
--------------------------------------------------------------------------------
2010-12-09      519986       Herman Hoon        Initial Implementation
2011-06-24      693486       Herman Hoon        Updated to cater for sculpted capital repayments

ENDDESCRIPTION
-----------------------------------------------------------------------"""

import acm 
import ael

context = acm.GetDefaultContext()
sheet_type = 'FDealSheet'
calcSpace = acm.Calculations().CreateCalculationSpace( context, sheet_type )

def myFunc(rate, **rest):
    """
    Gets a dictionary in rest containg the Combination instrument
    Simulate the Fixed Rate of the underlying Swaps
    Set the nominal structure of the second Swap
    return the present value of the Combination
    """
    ins = rest['instrument']
    instruments = ins.Instruments()
    
    list = sorted(instruments, key=lambda this: this.StartDate())

    ins1 = list[0]
    ins2 = list[1]

    calcSpace.SimulateValue(ins1, 'Fixed Rate', rate)
    calcSpace.SimulateValue(ins2, 'Fixed Rate', rate)
    
    nom = 0
    legs = ins1.Legs()
    for leg in legs:
        if leg.LegType() == 'Zero Coupon Fixed':
            inf = leg.StaticLegInformationFix(ins1, acm.Time.NotADateTime(), rate * 0.01, 'RSA', 'None')
            legInf = leg.LegInformation(acm.Time().DateNow())
            # Front Upgrade 2013.3 -- small fix of ProjectedCashFlow method, different class, params, etc.
            # needs to be tested thoroughly
            cashFlows = inf.ProjectedCashFlow(legInf, None)
            for cf in cashFlows:
                nom = nom + abs(cf.Number())
            
            cashFlows = leg.CashFlows()
            for cf in cashFlows:
                nom = nom + abs(cf.NominalFactor())

    structure = rest['structure']
    # Append a 0 to make the list the same length as the number of cashflows for the loop below
    # the final item in the list wont get used in updating the nominal
    structure.append(0)
    amortizing = True
    if float(structure[0]) == 0 and len(structure) == 1:
        amortizing = False
    
    ins2Clone = ins2.Clone()
    legs = ins2Clone.Legs()
    for leg in legs:
        count = 0
        prevNom = nom
        cashFlows = leg.CashFlows()
        cfList = sorted(cashFlows, key=lambda this: this.StartDate())
        for cf in cfList:
            cf.NominalFactor(prevNom)
            if amortizing:
                strucVal = float(structure[count])
                prevNom = prevNom - (nom * strucVal/100)
            
            count = count + 1
    try:
        ins2.Apply(ins2Clone)
        ins2.Commit()
    except Exception, err:
        print 'ERROR: %s did not commit: %s' %(ins2.Name(), err)
    
    
    pv = calcSpace.CreateCalculation(ins, 'Present Value').Value().Number()
    return pv

    
def secant(func, oldx, x, TOL=1e-12, **rest):    # f(x)=func(x)
    """
    Similar to Newton's method, but the derivative is estimated by line through 2 starting points.
    http://en.wikipedia.org/wiki/Secant_method
    """

    oldf, f = func(oldx, **rest), func(x, **rest)
    if (abs(f) > abs(oldf)):        # swap so that f(x) is closer to 0
        oldx, x = x, oldx
        oldf, f = f, oldf
    count = 0
    while 1:
        dx = f * (x - oldx) / float(f - oldf)
        if abs(dx) < TOL * (1 + abs(x)): 
            return str("%.10f" % (x-dx))
        else:
            if count >= 500:
                return 'Optimization did not converge'
        oldx, x = x, x - dx
        oldf, f = f, func(x, **rest)
        count = count + 1


def validate(ins, structure):
    instruments = ins.Instruments()
    if len(instruments) != 2:
        acm.LogAll('ERROR: Combination instrument must contain exaclty 2 instruments to calculate the Par Rate.')
        return False
    
    instruments = ins.Instruments()
    list = sorted(instruments, key=lambda this: this.StartDate())
    ins2 = list[1]
    
    if not(float(structure[0]) == 0 and len(structure) == 1):
        legs = ins2.Legs()
        for leg in legs:
            cf = leg.CashFlows()
            
            if (len(cf)-1) != len(structure):
                acm.LogAll('ERROR: The number of Sculpted Capital Repayments %s should be one less than the number of cashlows %s on each leg of the second instrument.' %(len(structure), len(cf)))
                return False
    return True

"""-----------------------------------------------------------------------"""
x0 = 0
x1 = 100

instrumentList = []
instrs = acm.FCombination.Select('')
for i in instrs:
    instrumentList.append(i.Name())
instrumentList.sort()

defaultStructure = '0.10000,0.20356,0.50787,0.50533,0.50281,0.55032,0.59705,1.08802,1.27170,1.44827'


descIns = 'The Par Rate of a combination instrument, that has two underlying Swaps, will be calculated and displayed in the log. \
The near Swap should have a Zero Coupon Fixed leg. The far Swap should be a normal IRS.'
descStruc = 'Sculpted capital structure of far Swap, expressed in terms of a percentage of the outstanding capital balance of the near Swap. \
Should contain the same number of values, seperated by a comma, as the number of cashflows of the far Swap OR a value of 0 if no sculpted capital structure is required.'



#Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [   
                    ['instrument', 'Combination Instrument', 'string', instrumentList,  '', 1, 0, descIns],
                    ['structure', 'Sculpted Capital Repayments %', 'string', None, defaultStructure, 1, 0, descStruc]
                ]
                
def ael_main(ael_dict):
    insName = ael_dict['instrument']
    ins = acm.FInstrument[insName]
    struc = ael_dict['structure']
    struc = struc.split(',')
    
    if validate(ins, struc):
        parRate = secant(myFunc, x0, x1, instrument=ins, structure = struc)
        acm.LogAll('PAR Rate for combination %s = %s' %(ins.Name(), parRate))
