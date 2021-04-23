""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/correlation/FCorrelationUploadFromFile.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FCorrelationUpload - Import Correlations from a text file
    
DESCRIPTION
    Imports correlations on the following format. 

    Store the data in a comma separated textfile with the two Instrument or CurrencyPair
    as first two elements on each row followed by the correlation. 

    Exclude the diagonals


ASA;ABL;0.413
ASA;AFB;0.213
ASA;USD/CHF;0.23
ABL;AFB;0.137
ABL;USD/CHF;-0.52
AFB;USD/CHF;0.82


------------------------------------------------------------------------------"""

# IMPORTANT!!! Please specify the name of the input file, the name of the 
# correlation matrix and the time bucket .


source = 'C:\\Correlations.csv'
corrname = 'My Correlations'
corrbucket = '0d'       # 0d = 0 days, 4m = 4 months, 1y = 1 year etc
commaseparator = ';'    # select ';' or ','

#------------------------------------------------------------------------------

import ael
import string


def findRecaddr(val):


    query = 'extern_id2="' + val + '"'
    #rec = ael.Instrument.read(query)
    rec = ael.Instrument[val]
    if rec:
        return rec.insaddr, 'Instrument'
    else:
        rec = ael.CurrencyPair[val]
        if rec:
            return rec.seqnbr, 'CurrencyPair'
            
    return 'Error', 0

ttSource = 'File containing the correlations to load (path and name)'
ttCorrName = 'Name of the Correlation parameter in PRIME'
ttCorrBucket = 'Time bucket for correlations'
ttColumnSeparator = 'Column separator in the correlation file'


ael_variables = [\
    ('source', 'Correlation file', 'string', [source], source, 1, 0, ttSource),
    ('corrname', 'Correlation name', 'string', [corrname], corrname, 1, 0, ttCorrName),
    ('corrbucket', 'Time bucket', 'string', ['0d', '1m', '1y'], corrbucket, 1, 0, ttCorrBucket),
    ('commaseparator', 'Column separator', 'string', [',', ';'], commaseparator, 1, 0, ttColumnSeparator)]
    
def ael_main(dict):
    source = dict['source']
    corrname = dict['corrname']
    corrbucket = dict['corrbucket']
    commaseparator = dict['commaseparator']
    
    try:
        d_test = ael.date_today().add_period(corrbucket)
    except TypeError:
        msg = 'ERROR! Time bucket, invalid format: %s. Time period expected (1d, 2w, 3m 1y)' % corrbucket        
        raise TypeError(msg)

    try:
        inf = open(source)
    except IOError:
        msg = 'Unable to read Correlation file: %s' % source
        raise IOError(msg)

    lines = inf.readlines()


    corrMat = ael.CorrelationMatrix[corrname]

    if corrMat:

        corrClone = corrMat.clone()
        for c in corrClone.correlations():
            c.delete()

        corrClone.commit()

        corrMat = corrClone

        ael.poll()

    else:    

        corrMat = ael.CorrelationMatrix.new()
        corrMat.name = corrname

    next = 0
    for l in lines:

        if len(l) > 0:

            va = string.replace(l, '\012', '')

            row = string.split(va, commaseparator)

            if row[0] != row[1]:

                if not next:
                    newCorr = ael.Correlation.new(corrMat)

                addr, ty =  findRecaddr(row[0]) 
                if addr != 'Error':
                    newCorr.recaddr0 = addr
                    newCorr.rec_type0 = ty
                else:
                    print('Wrong value of 1st riskfactor in:', row)      
                    next = 1
                    continue

                addr, ty =  findRecaddr(row[1])
                if addr != 'Error':

                    newCorr.recaddr1 = addr
                    newCorr.rec_type1 = ty
                else:
                    print('Wrong value of 2nd riskfactor in:', row)
                    next = 1
                    continue

                try:
                    newCorr.corr = float(row[2]) / 100.0
                except:    
                    print('Wrong format of correlation in:', row)
                    next = 1
                    continue

                newCorr.bucket0 = corrbucket
                newCorr.bucket1 = corrbucket

                next = 0
                try:
                    corrMat.commit()

                except:
                    print('Error storing correlation cell:', row)
                    continue

    print('Ready')
    inf.close()
