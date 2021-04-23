'''
======
SAEQ_DumpSkews
======
Purpose               :  Dump daily state of eq vol surfaces for day-to-day diffing
Department and Desk   :  Eq derivatives desk
Requester             :  Andrey Chechin
Developer             :  Peter Kutnik
CR Number             :  888720


HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
-----------------------------------------------------------------------------
'''

import ael
import os, os.path
from collections import namedtuple
from zak_funcs import write_file

VolSurface = namedtuple('VolSurface', ['name', 'strikes', 'expiries', 'values'])

def GetSkews():
    surfaces = {}
    skewsList = [ x[0] for x in ael.asql("select vol_name from Volatility where vol_name like '%Skew%'")[1][0]]
    strToday = ael.date_today().to_string('%Y-%m-%d')
    for surface in skewsList:
        ael.log('Getting %s...' % surface)
        pastExpiriesMessageGiven = False
        aelSkew = ael.Volatility[surface]
        surfaces[surface] = VolSurface(name=surface, strikes=[], expiries=[], values={})
        
        for vp in aelSkew.points():
            if vp.insaddr:
                expiry = vp.insaddr.exp_day.to_string('%Y-%m-%d')
            elif vp.exp_day:                
                expiry = vp.exp_day.to_string('%Y-%m-%d')
            else:
                ael.log('%s has points without benchmarks' % surface)
                continue
            if expiry < strToday:
                if not pastExpiriesMessageGiven:
                    ael.log('%s has past expiries' % surface)
                    pastExpiriesMessageGiven = True                
                continue
            strike = vp.insaddr.strike_price if vp.insaddr else vp.strike
            value = vp.volatility * 100
            
            if expiry not in surfaces[surface].expiries:
                surfaces[surface].expiries.append(expiry)                           
                    
            if strike not in surfaces[surface].strikes:
                surfaces[surface].strikes.append(strike)
                
                surfaces[surface].values[strike] = {} #expiry: vol
            
            surfaces[surface].values[strike][expiry] = value
        surfaces[surface].expiries.sort()
        surfaces[surface].strikes.sort()
    return surfaces
    
def AppendSurfaceToCsv(listRows, surface, surfaceName):
    if not surface:
        return
    header = [surfaceName]
    header.extend(surface.strikes)
    listRows.append(header)
    for expiry in surface.expiries:
        row = [expiry]
        for strike in surface.strikes:     #sorted!
            if expiry in surface.values[strike]:
                row.append(surface.values[strike][expiry])
            else:
                row.append('-')
        listRows.append(row)
    listRows.append([])           

def DumpAllSkews(myPath):
    outSkews = []
    skews = GetSkews()
    for skew in skews:
        AppendSurfaceToCsv(outSkews, skews[skew], skew)
    outFile = '%s/SAEQ_DumpSkews.csv' % myPath
    write_file(outFile, outSkews)
    ael.log('Done, written file %s' % outFile)
    ael.log('completed successfully')
    
ael_variables = [('OutputDir', 'Output Directory', 'string', None, '/services/frontnt/Task')]    

def ael_main(dict):
    DumpAllSkews(dict['OutputDir'])
        


