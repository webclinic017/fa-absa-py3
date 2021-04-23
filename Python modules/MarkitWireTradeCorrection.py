'''----------------------------------------------------------------------------------------------------------
MODULE                  :       MarkitWireTradeCorrection
PROJECT                 :       AMWI (Markit Wire Interface)
PURPOSE                 :       AMWI serves the purpose of integration between Markit Wire and Front Arena for a given set of product types
                            
DEPARTMENT AND DESK     :       Prime Services and IRD desk
REQUESTER               :       Manus van den Berg
DEVELOPER               :       Arthur Grace
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2014-06-20      TBA  Arthur Grace                    Initial Implementation - Once off

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    This module serves the purpose of updating or rolling back the legacy Markit Wire trades on the Synthesis adapter. In turn, the legacy 
                                trades will then be updated via the new AMWI adapter
'''

import acm
import ael

#clean our the trade id of legacy Markit Wire trades
def MarkitWireID(value, trd):
    #the various versions of the concatenated entry for MW deals
    value = value.replace('MW', '')
    value = value.replace('S1', '')
    value = value.replace('S2', '')
    value = value.replace('S3', '')
    value = value.replace('S4', '')
    value = value.replace('V1', '')
    value = value.replace('V2', '')
    value = value.replace('V3', '')
    value = value.replace('V4', '')
    value = value.replace('V5', '')
    value = value.replace('V6', '')
    value = value.replace('V7', '')
    value = value.replace('aa', '')
    value = value.replace('ab', '')
    value = value.replace('ac', '')
    value = value.replace('ad', '')
    value = value.replace('ae', '')
    value = value.replace('af', '')
    value = value.replace('ag', '')
    value = value.replace('ah', '')
    value = value.replace('Amended', '')
    value = value.replace('Cancelled', '')
    value = value.replace('New', '')
    value = value.replace('-Novated', '')
    value = value.replace('-PrimeBrokere', '')
    value = value.replace('T', '')
    value = value.replace('d', '')
    value = value.replace('Clearing', '')
    value = value.replace('-Match', '')
    value = value.replace('*', '')
    value = value.replace('**', '')
    value = value.replace('ai', '')
    value = value.replace('V8', '')
    value = value.replace('Novate', '')
    value = value.replace('-Partial', '')
    value = value.replace('New-Clearing', '')
    value = value.replace('-', '')
    print 'Value allocated is *******', value
    return int(value)
                        
def addAddInfoUpdate(generateFileName, runForFirst, logFileOnly, rollBackOnly):
    index = 0
    
    #the CCPmiddleware_id is the new add info field that AMWI makes use of to version and update a trade
    #this add info entry will only exist once the AMWI has been installed according to the Release Plan
    addInfoNameCCP='CCPmiddleware_id'
    addInfoNameVer='CCPmiddleware_versi'

    #ASQL query to select all the current Markit Wire trades prior to going live on the AMWI
    
    q = """select t.trdnbr,i.instype,ais.field_name,ai.value, \
      t.optional_key,t.status,t.time,usr.name,port.prfid \
      from trade t,instrument i,AdditionalInfo ai,AdditionalInfoSpec ais,User usr,portfolio port \ 
      where t.insaddr = i.insaddr \
      and ai.recaddr = t.trdnbr and ai.addinf_specnbr = ais.specnbr \
      and ais.field_name = 'MarkitWire' and ai.value like 'MW%' \
      and t.creat_usrnbr = usr.usrnbr \
      and i.instype in ('FRA','Swap') and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed') \
      and t.prfnbr = port.prfnbr \
      and t.optional_key ~= '' \
      order by 7"""
    
    #if no number of trades are specified at first, don't run the extract  
    if runForFirst == 0:
        print 'Run for first cannot ', runForFirst
        return
        
    selection = ael.asql(q)
    
    #the cleanedMWTradeId receives the cleaned Markit Wire trade id from the concatenated one populated by Synthesis
    cleanedMWTradeId = 0
    
    #the log file serves as a log of the run of all trades from a specific date to date, prior to going live with the AMWI
    f=open(generateFileName, 'a')
    f.write('Open the file to begin the update')
    #step through the trades retrieved in the ASQL query: q
    for j in selection[1][0]:
        index = index + 1 #build a count of each trade read for the log. This will assist in determining a missed number caught by exception
        #although the query does filter out status, make sure at the point of commit a trade is not missed in ASQL
        #terminated and void trades will not be updated. This will prevent any strange scenarios from Markit Wire AMWI
        if j[5] in ('BO Confirmed', 'BO-BO Confirmed', 'FO Confirmed'):
            #initialize the trade object
            trd = acm.FTrade[j[0]]
            
            #the following portfolios cause problems on commit: Unable to move a trade into the Graveyard portfolio tree
            if trd.Portfolio().Name() not in ('Archive Swap Flow 1', 'Conduit Trading', 'Archive Swap Flow', 'GK_SWAPS', 'RAJ - FRA Trading'):
            
                cleanedMWTradeId = MarkitWireID(trd.AdditionalInfo().MarkitWire(), trd)
                
                print index, cleanedMWTradeId, trd.Oid(), trd.Portfolio().Name(), trd.TradeTime()
                
                if isinstance(cleanedMWTradeId, int):
                
                    f.write(str(index) + ') \t Cleaned trade id: ' + str(cleanedMWTradeId) + ' \t Oid of trade found: ' + str(trd.Oid()) + '\t ' + trd.Status() + ' \t Portfolio: ' + trd.Portfolio().Name() + ' \t Trade time: ' + trd.TradeTime() + '\n')
                    specCCP = acm.FAdditionalInfoSpec[addInfoNameCCP]
                    addInfoCCP = acm.FAdditionalInfo.Select01('recaddr='+ str(trd.Oid()) +' and addInf=' + str(specCCP.Oid()), '')
                    specVer = acm.FAdditionalInfoSpec[addInfoNameVer]
                    addInfoVer = acm.FAdditionalInfo.Select01('recaddr='+ str(trd.Oid()) +' and addInf=' + str(specVer.Oid()), '')
                    
                    if not rollBackOnly:
                        if not logFileOnly:
                            if not addInfoCCP:
                                addInfoCCP = acm.FAdditionalInfo()
                                addInfoCCP.AddInf(specCCP)
                                addInfoCCP.Recaddr(trd)
                                
                            if not addInfoVer:
                                addInfoVer = acm.FAdditionalInfo()
                                addInfoVer.AddInf(specVer)
                                addInfoVer.Recaddr(trd)
                                
                            addInfoCCP.FieldValue(cleanedMWTradeId)
                            addInfoVer.FieldValue('<1\\1>')
                            #print 'Trade reflection',trd.Oid()
                            try:
                                addInfoCCP.Commit()
                                addInfoVer.Commit()
                                f.write('Successful commit of trade ' + str(trd.Oid()) + '\n')
                            except Exception, e:
                                print 'Trade reflection', trd.Oid(), str(e)
                                f.write('Error: cannot write trade add info '+str(trd.Oid())+'\n'+str(e))
                            #print index,'Committed the trade',trd.Oid()
                    else:
                        addInfoCCP = acm.FAdditionalInfo.Select('recaddr = %i' %trd.Oid())
                        for i in addInfoCCP:
                            if i.AddInf().Name() == addInfoNameCCP:
                                print i.AddInf().Name()
                                i.Delete()
                            if i.AddInf().Name() == addInfoNameVer:
                                print i.AddInf().Name()
                                i.Delete()
                            f.write('Successful deletion of trade' + str(trd.Oid()) + '\n')
                    if trd.AdditionalInfo().CCPmiddleware_id():
                        if trd.AdditionalInfo().CCPmiddleware_id() != '':
                            f.write('\t *** Updated CCPmiddleware_id: ' + trd.AdditionalInfo().CCPmiddleware_id() + '\n\n')
                        else:
                            f.write('\t *** Add info created, but not udpated (probably no trade number found)\n')
                    else:
                        f.write(str(index) + ') *** Add info for new Markit Wire field CCPmiddleware_id not instanced\n')
                else:
                    f.write(str(index) + ') *** Careful, the following trade did not update due to cleaned trade id cleansing from MW add info: ' + str(trd.Oid()) + '\n')
            else:
                f.write(str(index) + ') *** Careful, the following trade ' + str(trd.Oid()) + ' did not update due to the portfolio ' + trd.Portfolio().Name() + '\n')
        else:
            f.write(str(index) + ') *** Careful, the following trade did not update due to the status: ' + j[5])
        if runForFirst!=999:    
            if index == runForFirst:
                f.close()
                break
    f.close()        
    return 

#variables for running the update
#if 999 entered for Run For First then generate all the trades and update them
#Log only, no commit will aid in retrieving a record of the trades to be updated firstly

ael_variables = \
    [
        ['OutputFile', 'Output file', 'string', None, 'C:\\zzMWTradeCorrectionFile.txt', 1],
        ['RunForFirst', 'Run for first (999 run all)', 'int', None, 1, 1],
        ['LogFileOnly', 'Log only, no commit', 'bool', [True, False], True, 0, 0, 'Log file only', None, 1],
        ['Rollback', 'Rollback trade correction', 'bool', [True, False], False, 0, 0, 'Roll back', None, 1]
    ]

def ael_main(parameters):
    addAddInfoUpdate(parameters['OutputFile'], parameters['RunForFirst'], parameters['LogFileOnly'], parameters['Rollback'])
