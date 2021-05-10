

'''

Purpose: FColumnDefinitions for if a stock is a member of the ALSI40 index
Department : Finance
Desk : Capital Markets
Requester :  Riaan Breedt
Developer : Anil Parbhoo
CR Number : 787476
Jira Call Reference Number : ABITFA-878

'''

import acm

def alsiStockTest(self):
    if not self.IsKindOf('FStock'):
        return None
    else:
        stk = self
        index = acm.FEquityIndex['ZAR/ALSI']

        for mem in index.Instruments():
        #Instruments() method applied to FEquityIndex returns FArray(FInstrument) 
            if stk.Name() == mem.Name():
                return 'Yes'
        return 'No'

