import acm

zar_curve_names=[
'ZAR-SWAP',
'ZAR-SWAP-SPREAD',
'ZAR_Bond_repo_153',
'ZAR_Bond_repo_157',
'ZAR_Bond_repo_GC',
'ZAR_Bond_discount_I2025',
'ZAR_Bond_discount_I2038',
'ZAR_Bond_discount_I2050',
'ZAR_Bond_discount_R154',
'ZAR_Bond_discount_R155',
'ZAR_Bond_discount_R157',
'ZAR_Bond_discount_R186',
'ZAR_Bond_discount_R189',
'ZAR_Bond_discount_R197',
'ZAR_Bond_discount_R201',
'ZAR_Bond_discount_R202',
'ZAR_Bond_discount_R2023',
'ZAR_Bond_discount_R203',
'ZAR_Bond_discount_R2030',
'ZAR_Bond_discount_R2037',
'ZAR_Bond_discount_R204',
'ZAR_Bond_discount_R2048',
'ZAR_Bond_discount_R206',
'ZAR_Bond_discount_R207',
'ZAR_Bond_discount_R208',
'ZAR_Bond_discount_R209',
'ZAR_Bond_discount_R210',
'ZAR_Bond_discount_R211',
'ZAR_Bond_discount_R212',
'ZAR_Bond_discount_R213',
'ZAR_Bond_discount_R214']

def getZarCurves():
    curves = acm.FArray()
    for name in zar_curve_names:
        yc = acm.FYieldCurve[name]
        if yc:
            curves.Add(yc)
    return curves

def getNonZarCurves():
    zar_curves = getZarCurves()
    non_zar_curves = acm.FArray()   
    all_curves = acm.FYieldCurve.Select('')
    for yc in all_curves:
        if yc not in zar_curves:
            non_zar_curves.Add(yc)
    return non_zar_curves
    
