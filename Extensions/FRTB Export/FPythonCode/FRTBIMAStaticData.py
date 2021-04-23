""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/frtb/./etc/FRTBIMAStaticData.py"
from __future__ import print_function
#Issuer type
    #  Seniority : LGD
LGD = { 
                'Corporates': {
                                'Covered Bonds' : 0.6,
                                'Senior Debt' : 0.6,
                                'Equity' : 1.0,
                                'Non-Senior Debt': 1.0
                                },
                'Sovereigns': {
                                'Covered Bonds' : 0.6,
                                'Senior Debt' : 0.6,
                                'Equity' : 1.0,
                                'Non-Senior Debt': 1.0
                                },
                'Local Governments/Municipalities': {
                                'Covered Bonds' : 0.6,
                                'Senior Debt' : 0.6,
                                'Equity' : 1.0,
                                'Non-Senior Debt': 1.0
                                },
                '': {
                        '' : 1.0,
                        'Other' : 1.0,
                        'Covered Bonds' : 0.6,
                        'Senior Debt' : 0.6,
                        'Equity' : 1.0,
                        'Non-Senior Debt': 1.0
                    },
    }


def getLGD(issuerType, seniority):
    print(issuerType)
    print(seniority)
    return LGD[issuerType][seniority]
    
