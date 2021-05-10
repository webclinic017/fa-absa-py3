'''
Purpose:                Update the original HCashIncep script for FA 2010.2 to 2013.3.1 upgrade because 2013.3.1 uses vector columns.
Department and Desk:    Markets IT
Requester:              Upgrade related
Developer:              Macanda Sanele, Chissungo Edmundo
CR Number:              FAU-287
Date:                   2013-10-25

'''

import ael, acm, SAGEN_IT_TM_Column_Calculation

#from SAGEN_IT_TM_Column_Calculation import get_TM_Column_Calculation
def cashinzar(temp, tradenbr, date, curr, *rest):
    
    return SAGEN_IT_TM_Column_Calculation.get_TM_Column_Calculation(None, 'Standard', 'FPortfolioSheet', tradenbr, 
           'Trade', 'Portfolio Cash Vector ZAR', curr, 1, None, date)
   

