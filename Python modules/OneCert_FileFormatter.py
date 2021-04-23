'''-----------------------------------------------------------------------
MODULE
    OneCert_FileFormatter

DESCRIPTION
    This module is used to remove the column header row and the add a footer.

    Department and Desk : UT
    Requester           : One Cert (UT Book Access)
    Developer           : Fancy Dire

    History:
    When: 	  Who:		What:       
    2015-12-10    Fancy Dire	Created

END DESCRIPTION
-----------------------------------------------------------------------'''
import ael
import datetime 
    
ael_variables = [
                    ['filetype', 'File Type', 'string', ['User', 'Group'], 'User'],
                    ['inpath', 'Input Path', 'string', None, 'C:\\cygwin\\home\\direfanc\\'],
                    ['inputfile', 'Input File', 'string', None, 'ABCAP_FA_BOOK_ENTITLE.txt'],
                    ['outpath', 'Output Path', 'string', None, 'C:\\cygwin\\home\\direfanc\\'],
                    ['outputfile', 'Output File', 'string', None, 'ABCAPFRONTARENA_ITSER000000000040304_USER_BOOK_ENTITLEMENTS_FEED_']
                ]


def ael_main(parameter):

    runDate = ael.date_today()
    dt = datetime.datetime.now()
    time_stamp = datetime.datetime.strftime(dt, "%Y%m%d_%H%M")
    fileSuffix = '_ACL.txt' if parameter['filetype'] == 'User' else '.txt'
    inputFile = parameter ['inpath'] + runDate.to_string('%Y-%m-%d') + '/' + parameter ['inputfile']
    outputFile = parameter ['outpath'] + parameter ['outputfile'] + time_stamp + fileSuffix
    print 'output_filename:', outputFile
    
    
    count = 0
    with open(outputFile, 'w') as out_f:
        with open(inputFile, 'r') as in_f:
            fl = in_f.readline() #Skip the header row
            for line in in_f:
                temp = line.split('|')
                #Check for empty rows and skip
                if len(temp)> 1:
                    out_f.write(line)
                    count+=1 #Record count to be written to the Footer
                    
        line = 'FOOTER|NumberOfRecordsProcessed|'+str(count)
        out_f.write(line)
                    
    print "Wrote secondary output to: " + outputFile
