'''----------------------------------------------------------------------------------------------------------
MODULE                  :       MarkitWireSideUpload
PROJECT                 :       OTC Clearing
PURPOSE                 :       This module serves the purpose of updating all legacy Markit Wire trades Side Id to the relevant Side Id 
                                supplied by Markit Wire through the Deal Extractor. This extractor is used for a full population download 
                                of the Markit Wire trades. 
                                The Deal Extractor full population download is located here: Y:\Jhb\FALanding\Prod\MarkitWire\DEbaseline.csv
                                The source file for this module is located here and has been ironed out for specific inter-desk deals and normal 
                                trades firstly: Y:\Jhb\FALanding\Prod\MarkitWire\MWSideIdProdOutputIntegration\MWSideIdProdOutputIntegration.csv
DEPARTMENT AND DESK     :       ABSA Capital / IRD Desk and Prime Services Desk
REQUESTER               :       Helder Loio
DEVELOPER               :       Arthur Grace
CR NUMBER               :       CHNG0002811857
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2015-06-05    CHNG0002811857    Arthur Grace                    Initial Implementation

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module we update legacy Markit Wire trades with the side id given to us by Markit Wire in a full population download
'''

import acm
import csv

def updateSideIds(source, parameters):
    try:
        lineRead = 0
        addInfoNameCCP='mwire_sideid'
        print 'About to process the side for the Markit Wire legacy trades'
        fLog = open(parameters['LogFile'], 'a')
        fLog.write('About to start the update process of the side id for Markit Wire trades\n')
        for read in source:
            if read[0] != 'tradeid' and read[0] != '':
                trd = acm.FTrade[read[11]]
                
                specCCP = acm.FAdditionalInfoSpec[addInfoNameCCP]
                addInfoCCP = acm.FAdditionalInfo.Select01('recaddr='+ str(trd.Oid()) +' and addInf=' + str(specCCP.Oid()), '')
                if not parameters['RunRollback']:
                    if not addInfoCCP:
                        print 'Nothing set on this trade for side id ', read[0], ' so will be updating this trade with the side id'
                        addInfoCCP = acm.FAdditionalInfo()
                        addInfoCCP.AddInf(specCCP)
                        addInfoCCP.Recaddr(trd)
                        addInfoCCP.FieldValue(read[1])
                        if not parameters['RunDontUpdate']:
                            try:
                                fLog.write('-> About to commit side id on trade '+str(trd.Oid())+' with side id '+str(read[1])+'\n')
                                addInfoCCP.Commit()
                                lineRead+=1
                                fLog.write(str(lineRead)+' <- Done committing the trade side id '+str(trd.Oid())+' with side id '+str(read[1])+'\n')
                                fLog.write('****************************************************************************************')
                            except Exception, e:
                                fLog.write('********************ERROR: The following error occurred on FA trade '+str(trd.Oid())+' Error-> '+str(e)+'\n')
                    else:       
                        print 'Additional Info set on this trade for side id', read[0]
                else:
                    'About to commence with the rollback of the add info'
                    addInfoCCP = acm.FAdditionalInfo.Select('recaddr = %i' %trd.Oid())
                    print addInfoCCP
                    for addinfo in addInfoCCP:
                        if addinfo.AddInf().Name() == addInfoNameCCP:
                            print 'Removing add info for trade', read[11]
                            fLog.write('Rollback -> About to remove (rollback) the side id on trade '+str(trd.Oid())+'\n')
                            lineRead+=1
                            addinfo.Delete()
                            print '************************ Removed the additional info field value'
                            fLog.write(str(lineRead)+' Rollback -< Done removing the side id on trade '+str(trd.Oid())+'\n')
                            fLog.write('*******************************************************************************************')
        fLog.close()
    except Exception, e:
        print 'The following error occurred in running the update script for the side id', str(e)
        fLog.close()
        
ael_variables = \
    [
        ['SourceFile', 'Output file', 'string', None, 'Y:\Jhb\FALanding\Prod\MarkitWire\MWSideIdProdOutputIntegration.csv', 1],
        ['LogFile', 'Log file', 'string', None, 'Y:\Jhb\FALanding\Prod\MarkitWire\MWSideIdProdOutputIntegrationLog.log', 1],
        ['RunDontUpdate', 'Run Do Not Update - No Commit', 'bool', [True, False], True, 0, 0, 'Log file only', None, 1],
        ['RunRollback', 'Rollback', 'bool', [True, False], False, 0, 0, 'Log file only', None, 1]
    ]

def ael_main(parameters):
    f= open(parameters['SourceFile'], 'rt')
    reader = csv.reader(f)

    updateSideIds(reader, parameters)

    f.close()
