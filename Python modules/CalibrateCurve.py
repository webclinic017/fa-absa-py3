'''-----------------------------------------------------------------------
MODULE
    CalbrateCurve

DESCRIPTION
    
    Date                : 2010-08-05
    Purpose             : Instrument Spread curves need to be recalibrated to the updated market price
    Department and Desk : MO / Market Risk
    Requester           : Andiswa Tshele
    Developer           : Anwar Banoo
    CR Number           : ??????
    
ENDDESCRIPTION
-----------------------------------------------------------------------'''

import acm

ael_variables = [ ['CurveName', 'Curve Name', 'string', [curve.Name() for curve in acm.FInstrumentSpreadCurve.Select("")], 'PM-SWAP_CS', 1] ]

def ael_main(parameter, *rest):
    curveName = parameter['CurveName']
    try:
        curve = acm.FYieldCurve[curveName]
        if curve:
            curve.CalibrateSpreads()
            message = 'Success'
    except Exception, e:
        message =  'Failure,' + e
    print(message)
