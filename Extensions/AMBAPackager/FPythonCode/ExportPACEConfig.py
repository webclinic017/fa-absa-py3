"""
    ExportPACEConfig
    
    (C)2014-2016 SunGard Front Arena
        
    20140805 Richard Ludwig

    
"""

import acm
import PackageExportAMBA

def export(eii):
    shell = eii.Parameter('shell')
    objects = []
    for pe in acm.FPaceEngine.Select(''):
        objects.append( pe)
    for pe in acm.FStoredCalculationEnvironment.Select(''):
        objects.append( pe)
    for pe in acm.FPaceConfiguration.Select(''):
        objects.append( pe)

    PackageExportAMBA.ExportCommonObject(shell, objects, 'PACEconfig_' + str(acm.Time.DateNow()), follow=False)
