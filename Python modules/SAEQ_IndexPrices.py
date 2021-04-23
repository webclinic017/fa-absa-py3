'''
Purpose: Used by ASQL called SAEQ_IndexPrices. Also scheduled to automatically run and send email.
Department: PCG
Requester: Herman Levin
Developer: Willie van der Bank
CR Number: 204775 (21/01/2010)

Purpose: Updated for scheduling purposes.
Department: PCG
Requester: Herman Levin
Developer: Willie van der Bank
CR Number: 218100 (04/02/2010)

Purpose: Updated for auditing purposes.
Department: PCG
Requester: Herman Levin
Developer: Willie van der Bank
CR Number: 229973 (18/02/2010)


CHNG0003433131 - ABITFA-4075 - Add additional indexes to SPOT VS. Theoretical price comparision report 

'''

import ael, acm

ael_variables = [('Path', 'OutputDirectory', 'string', '', 'F://')]

def Prices(temp, Instr, *rest):
    i = acm.FInstrument[str(Instr)]
    calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FDealSheet')
    calc = calc_space.CalculateValue(i, 'Instrument Market Price')
    marketPrice = calc.Value().Number()
    return round(marketPrice, 2)
    
def SPrice(temp, Instr, *rest):
    i = ael.Instrument[Instr]
    SpotPrice = i.spot_price('ZAR')
    return round(SpotPrice, 2)

def ael_main(dict):
    Insts = ['ZAR/ALSI',
             'ZAR/SWIX',
             'ZAR/INDI',
             'ZAR/FINI',
             'ZAR/RESI',
             'ZAR/CAPI',
             'ZAR/FNDI',
             'ZAR/ALSI_Harmony',
             'ZAR/ALSI_85DIVS',
             'ZAR/SWIX_85DIVS',
             'ZAR/INDI_100DIVS']
    anydiff = 0
    Message = ''
    MessageTop = "SAEQ_IndexPricesReport."
    for ins in Insts:
        i = ael.Instrument[ins]
        InstName = i.insid
        SpotPrice = SPrice(1, InstName)
        TheorPrice = Prices(1, InstName)
        diff = SpotPrice - TheorPrice
        if diff != 0:
            anydiff = 1
        Message = Message + 'Instrument: ' + InstName + '\n' + 'ReutersPrice: ' + str(SpotPrice) + '\n' + 'TheorPrice: ' + str(TheorPrice) + '\n' + 'Difference: ' + str(diff) + '\n' + '\n'
    #anydiff = 1
    MessageTotal = MessageTop + '\n' + '\n' + Message
    print(MessageTotal)
    if anydiff == 1:
        outfiletext = open(dict['Path'] + MessageTop + "txt", 'w')
        outfiletext.write(MessageTotal)
        outfiletext.close()
