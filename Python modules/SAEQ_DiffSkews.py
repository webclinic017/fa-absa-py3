'''
======
SAEQ_DiffSkews
======
Purpose               :  Produce a report of relative equities vol surface updates between days
Department and Desk   :  Eq derivatives desk
Requester             :  Andrey Chechin
Developer             :  Peter Kutnik
CR Number             :  888720


HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2012-02-15 891974	kutnikpe	   Fix crash for surfaces with no suitable benchmark points
2012-04-12 145951   kutnikpe	   Remove relative diff
--------------------------------------------------------------------------------
'''

import ael
import os
from zak_funcs import write_file
import csv
from SAEQ_DumpSkews import AppendSurfaceToCsv, VolSurface

def LoadAelSurfacesFromCsv(fileName):
#takes a file name, returns a list of ael Volatility objects loaded from csv of said name
    f = open(fileName, 'rt')
    surfaces = {} 
    reader = csv.reader(f, delimiter=',')        
    
    try:
        row = reader.next()
        while 1:
            #skip empty rows
            while len(row) < 2:
                row = reader.next()
                continue            
            
            #load surface
            (surface, name, strikes) = LoadAelSurfaceHeader(row)
            ael.log( 'Loading %s...' % name)
            row = reader.next()     
            if surface:
                while len(row) >=2:
                    LoadAelSurfaceBodyRow(surface, strikes, row)
                    row = reader.next()
            surfaces[name] = surface
            ael.log( 'Loaded.')
    except StopIteration:
        pass
                
    f.close()
    return surfaces
    
def LoadAelSurfaceHeader(csvRow):
    if len(csvRow) < 2:
        return None
    surface = ael.Volatility.new()
    surface.vol_name = '__tmp' + csvRow[0]   
    surface.interpolation_method = 'Hermite'
    surface.vol_type = 'Benchmark'  
    strikes=[float(n) for n in csvRow[1:]]
    return (surface, csvRow[0], strikes)
    
def LoadAelSurfaceBodyRow(surface, strikes, csvRow):
    expiry = ael.date_from_string(csvRow[0])
    
    for i in range(1, len(csvRow)):
        if csvRow[i] == '-':
            continue
        vp = ael.VolPoint.new(surface)
        vp.strike = strikes[i-1]
        vp.exp_day = expiry
        vp.volatility = float(csvRow[i]) / 100
                
def subtractTempAelSurfaceFromCurrent(tmpSurface, currentName, relative=False):
#Takes a vol surface from Front by name, subtracts a temp surface loaded from file from it
#Outputs a CSV-able structure

    currentSurface = ael.Volatility[currentName]
    if not currentSurface:
        ael.log("Surface %s does not exist in Front!" % currentName)
        return None
    (outStrikes, outExpiryDates) = getImportantPoints(currentSurface)
    if not outStrikes:
        ael.log('No suitable points for diffing found for %s' % currentName)
        return None
        
    outExpiryStrings = []
    outValues = {}    
    outSurface = VolSurface(name=currentName, strikes=outStrikes, expiries=outExpiryStrings, values=outValues)    
    changes = 0    
    for expiry in outExpiryDates:
        expiryStr = expiry.to_string('%Y-%m-%d')         
        if expiryStr not in outExpiryStrings:
            outExpiryStrings.append(expiryStr)
        for strike in outStrikes:
            curValue = currentSurface.vol_get(strike, expiry) * 100            
            oldValue = tmpSurface.vol_get(strike, expiry) * 100
            resultValue = curValue - oldValue
            if abs(resultValue) < 0.00000001:
                resultValue = 0
            else:
                changes += 1
                if relative:
                    resultValue = (resultValue / oldValue) * 100
            if strike not in outValues:
                outValues[strike] = {}
            outValues[strike][expiryStr] = '%8.6f%%' % resultValue
    if changes > 0:
        return outSurface
    else:
        return None


def getAnchorStrikeAndExpiries(currentSurface):
    tmpStrikes = []
    outExpiries = []
    today = ael.date_today()
    pastExpLogged = 0
    for vp in currentSurface.points():
        if vp.insaddr:
            expiryDate = vp.insaddr.exp_day
        elif vp.exp_day:                
            expiryDate = vp.exp_day
        else:
            ael.log( '%s has points without benchmarks' % currentSurface.vol_name)
            continue
        if expiryDate < today:
            if not pastExpLogged:
                ael.log( '%s has past expiries' % currentSurface.vol_name)
                pastExpLogged = 1
            continue
        strike = vp.insaddr.strike_price if vp.insaddr else vp.strike
        if expiryDate not in outExpiries:
            outExpiries.append(expiryDate)
        if strike not in tmpStrikes:
            tmpStrikes.append(strike)
    tmpStrikes.sort()
    outExpiries.sort()
    if len(tmpStrikes) > 0:
        return (tmpStrikes[len(tmpStrikes)/2], outExpiries)
    return (None, None)
    
def getImportantPoints(currentSurface):
#filters strikes and expiries to display the key points for report brevity    
    (anchorStrike, outExpiries) = getAnchorStrikeAndExpiries(currentSurface)
    if anchorStrike:
        outStrikes = [anchorStrike*0.1,
        anchorStrike*0.3,
        anchorStrike*0.4,
        anchorStrike*0.5,
        anchorStrike*0.6,
        anchorStrike*0.7,
        anchorStrike*0.8,
        anchorStrike*0.85,
        anchorStrike*0.9,
        anchorStrike*0.95,
        anchorStrike*0.975,
        anchorStrike,
        anchorStrike*1.025,
        anchorStrike*1.05,
        anchorStrike*1.1,
        anchorStrike*1.15,
        anchorStrike*1.2,
        anchorStrike*1.3,
        anchorStrike*1.4,
        anchorStrike*1.5,
        anchorStrike*1.6,
        anchorStrike*2]
        return (outStrikes, outExpiries)
    return (None, None)
        
def DiffSkewsAgainstFile(againstDate, inputPath, outputPath):
    
    if againstDate == 'yesterday':
        againstDate = ael.date_today().add_banking_day(ael.Instrument['ZAR'], -1)
    else:
        againstDate = ael.date_from_string(againstDate)
    
    fileName = '%s/%s/SAEQ_DumpSkews_%s.csv' % (inputPath, againstDate.to_string('%Y-%m-%d'), againstDate.to_string('%y%m%d'))
    tmpSurfaces = LoadAelSurfacesFromCsv(fileName)
    
    outCsv = [['Volatility skew updates between %s and %s:' % (againstDate.to_string('%Y-%m-%d'), ael.date_today().to_string('%Y-%m-%d'))]]
    
    for key in tmpSurfaces:
        tmpSurface = tmpSurfaces[key]
        if not tmpSurface:
            continue
        absChange = subtractTempAelSurfaceFromCurrent(tmpSurface, key)
        if not absChange:
            continue

        AppendSurfaceToCsv(outCsv, absChange, key)
    
    if len(outCsv) == 1:
        outCsv.append(['No updates recorded'])
    
    outFileName = '%s/SAEQ_DiffSkews.csv' % outputPath
    write_file(outFileName, outCsv)
    ael.log('Complete, wrote file %s' % outFileName)
    ael.log('completed successfully')

ael_variables = [('InputDir', 'Input Directory', 'string', None, '/services/frontnt/Task'),
                ('OutputDir', 'Output Directory', 'string', None, '/services/frontnt/Task'),
                ('AgainstDate', 'Date to diff against', 'string', None, 'yesterday')]

def ael_main(ael_dict):
    DiffSkewsAgainstFile(ael_dict['AgainstDate'], ael_dict['InputDir'], ael_dict['OutputDir'])
