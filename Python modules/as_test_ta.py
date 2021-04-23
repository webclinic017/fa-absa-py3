"""-----------------------------------------------------------------------------------------
2006-11-30 - Tina Viljoen (Sungard)
Module
    Amendment Listener
    (c) Copyright 2006 by Front Capital Systems. All rights reserved

DESCRIPTION     
Amendment Diary     

2007-09-01      Aaeda Salejee           Added buildColumns function to build Column xml tag.
2007-10-01      Aaeda Salejee           Stopped certain amendments from being logged as per business request
2007-11-30      Aaeda Salejee           Added payments.
-----------------------------------------------------------------------------------------"""

import ael
import time 
import shutil
import os

def start():        
    print 'Start in main'
    #date =  ael.date_today().to_ymd()
    #newdate = str(date[0])+str(date[1])+str(date[2])
    newdate = ael.date_today().to_string('%Y%m%d')   
    #path  = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/TradeAmendments_Final' +  newdate
    path  = 'c://AmendmentDairy/TradeAmendments_Final' +  newdate

    # Create initial file for the day.
    if not os.path.exists(path + '.xml'):
        amendment = open(path + '.xml', 'w')
        line = '<?xml version=' + "'1.0'" + ' encoding=' + "'utf-8'" + '?>\n'
        amendment.writelines(line)
        amendment.writelines('<?xml-stylesheet type="text/xsl" href="\\\\v036syb004001\Atlas-End-Of-Day\TradeAmendment\XSL\Amendment.xsl"?>\n')
        amendment.writelines('<TODAY>')
        amendment.close
    
    ael.Instrument.subscribe(listener)
    ael.Leg.subscribe(listener)
    ael.CashFlow.subscribe(listener)
    ael.Reset.subscribe(listener)
    ael.Trade.subscribe(listener)
    ael.Payment.subscribe(listener)





    
def stop():
    print "Stopping..."
    newdate = ''
    #date =  ael.date_today().to_ymd()
    #newdate = str(date[0])+str(date[1])+str(date[2])
    newdate = ael.date_today().to_string('%Y%m%d')   
    #path = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/TradeAmendments_Final' +  newdate + '.xml'
    #oldpath = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/TradeAmendments' +  newdate +  '.xml'
    path = 'c://AmendmentDairy/TradeAmendments_Final' +  newdate + '.xml'
    #oldpath = 'c://AmendmentDairy/TradeAmendments' +  newdate +  '.xml'    
    amendment_new = open(path, 'a')
    amendment_new.write('</TODAY>\n')
    amendment_new.close
    
    ael.Instrument.unsubscribe(listener)
    ael.Leg.unsubscribe(listener)
    ael.CashFlow.unsubscribe(listener)
    ael.Reset.unsubscribe(listener)
    ael.Trade.unsubscribe(listener)
    ael.Payment.unsubscribe(listener)
    
    print 'Process Stopped'

    return
    
    

#def status():
#    print 'Status:AmendmentListerner active'



def listener(o, e, arg, op):
    #SessionInsertIgnoreCounterStart = 0
    #newdate = ''
    #date =  ael.date_today().to_ymd()
    #newdate = str(date[0])+str(date[1])+str(date[2])
    newdate = ael.date_today().to_string('%Y%m%d')   
    #path  = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/TradeAmendments_Final' +  newdate     
    path  = 'c://AmendmentDairy/TradeAmendments_Final' +  newdate
    #print path + '.xml'

    # Create initial file for the day.
    if not os.path.exists(path + '.xml'):
        amendment = open(path + '.xml', 'w')
        line = '<?xml version=' + "'1.0'" + ' encoding=' + "'utf-8'" + '?>\n'
        amendment.writelines(line)
        amendment.writelines('<?xml-stylesheet type="text/xsl" href="\\\\v036syb004001\Atlas-End-Of-Day\TradeAmendment\XSL\Amendment.xsl"?>\n')        
        amendment.writelines('<TODAY>')
        amendment.close

    amendold = {}
    amendnew = {}
    #x = 0
    #flag_time = 0
    #flag_key = 0
    flag = 0
    '''
    dict = {}
    dict[0] = 'one'
    dict[1] = 'two'
    dict[2] = 'three'
    dict[3] = 'four'
    dict[4] = 'five'
    dict[5] = 'six'
    dict[6] = 'seven'
    dict[7] = 'eight'
    dict[8] = 'nine'
    dict[9] = 'ten'
    '''
    output = ''
    counter = 0
    '''
    results = []
    
    inst_str = ''
    original = ''
    current = ''
    '''
    #currentUpdateTime  = ''
    #key12 =  ''
    #print 'AAAAAAAAAA', e, op
    
    
    
    '''
    if e.record_type == 'Payment' and op == 'insert':


        e_clone = e.clone()
        
        #USER
        if e.creat_usrnbr.grpnbr.grpid not in ('Integration Process', 'System Processes'):

            #INSTRUMENT
            #old_entity=ael.get_old_entity()
            #new_entity=e

            x = 0

            #ADDITIONAL PAYMENTS
            if e.record_type == 'Payment':
                #print e.pp()
                #try:
                    #print 'HERE', ael.get_old_entity()
                    #if  ael.get_old_entity().pp() <> None:
                    #    if e.pp() <> ael.get_old_entity().pp():
                output = ''
                output = output + ('\n<Entity>\n')
            
                if e.trdnbr.status != 'Simulated':
                    try:
                        prf = e.trdnbr.prfnbr.prfid
                        reltrd = str(e.trdnbr.trdnbr)
                        stat = str(e.trdnbr.status)
                        confoDate = str(e.trdnbr.add_info('Confo Date Sent'))
                        confoText = e.trdnbr.add_info('Confo Text')
                        acq = e.trdnbr.acquirer_ptynbr.ptyid
                        trd_time = str(ael.date_from_time(e.trdnbr.time))
                    except:
                        prf = ''
                        reltrd = ''
                        stat = ''
                        confoDate = ''
                        confoText = ''
                        acq = ''
                        trd_time = ''
                else:
                    prf = ''
                    reltrd = ''
                    stat = ''
                    confoDate = ''
                    confoText = ''
                    acq = ''
                    trd_time = ''                            
                    
            
                #Write static fields
                output = output + '   <Name>' + e.record_type + '</Name>\n'
                output = output + '   <Key>' +  str(e.paynbr) + '</Key>\n'
                output = output + '   <UpdatedUser>' + e.display_id('updat_usrnbr') + '</UpdatedUser>\n'
                output = output + '   <UpdatedTime>' + str(ael.date_from_time(e.updat_time)) + '</UpdatedTime>\n'
                output = output + '   <CreateTime>' + str(ael.date_from_time(e.creat_time)) + '</CreateTime>\n'
                output = output + '   <TradeTime>' + trd_time + '</TradeTime>\n'                            
                output = output + '   <Portfolio>' + prf + '</Portfolio>\n'
                output = output + '   <RelTrade>' + reltrd + '</RelTrade>\n'
                output = output + '   <Status>' + stat + '</Status>\n'
                output = output + '   <RelInstrument>' + e.trdnbr.insaddr.insid + '</RelInstrument>\n'
                output = output + '   <ConfoSent>' + confoDate + '</ConfoSent>\n'
                output = output + '   <ConfoText>' + confoText + '</ConfoText>\n'
                output = output + '   <Acquirer>' + acq + '</Acquirer>\n'
                output = output + '   <Columns>\n'
            
                #Loop through changes and add to output xml
                amendold[e.paynbr] = '' #ael.get_old_entity().pp().split('\n') 
                amendnew[e.paynbr] = e.pp().split('\n') 
            
                #cols = buildColumns(amendold, amendnew, e.record_type, e.paynbr)


                #Add new fields
                cols = ''
                x = 0
                status_change = 'no'

                while x < len(amendnew[e.paynbr]):
                    if amendnew[e.paynbr][x] <> None: 
                        #splits each line by a double space and removes any whitespace.
                        #e_old = amendold[k][x].split('  ')
                        e_new = amendnew[e.paynbr][x].split('  ')
                        name = e_new[0].strip()
                        val_old = ''
                        if name in ('premium', 'quantity', 'price', 'amount'):
                            val_new = (str)((float)(e_new[len(e_new)-1].strip()))
                        elif name == 'ptynbr':
                            #print (int)(e_new[len(e_new)-1].strip())
                            try:
                                val_new = ael.Party[e_new[len(e_new)-1].strip()].ptyid
                            except:
                                val_new = ''
                        elif name == 'curr':
                            val_new = ael.Instrument[e_new[len(e_new)-1].strip()].insid
                        else:
                            val_new = e_new[len(e_new)-1].strip()
                        
                        if name not in ('record_type', 'creat_time', 'creat_usrnbr', 'updat_time', 'updat_usrnbr', 'paynbr', 'trdnbr', 'archive_status', 'oringal_curr', 'version_id', 'bo_trdnbr', 'execution_time', 'your_ref', 'optional_key'):    
                            if val_new in ('', 0):
                                cols = cols + '      <Column>\n'
                                cols = cols + '         <Name>' + name + '</Name>\n'
                                cols = cols + '         <Original>\n            <Value>' + val_old + '</Value>\n         </Original>\n'
                                cols = cols + '         <Current>\n            <Value>' + val_new + '</Value>\n         </Current>\n'
                                cols = cols + '      </Column>\n'
                                                
                    x = x + 1
        
                if cols != '':
                    output = output + cols
                    output = output + '   </Columns>\n'
                    output = output + '</Entity>\n'
                else:
                    output = ''
                    return
                
                #print output        

                currentUpdateTime  = '   <UpdatedTime>' + str(e.updat_time) + '</UpdatedTime>\n'
                key12 =              '   <Key>' +  str(e.paynbr) + '</Key>\n'
                
                #except:
                #    print "Error in PAYMENT code line 226",op
        
   
    '''
    
    if op in ('update'): # or (e.record_type == 'Payment' and op in ('insert', 'update')):
        #print 'XXXXXXXXXXXX', e, op
        e_clone = e.clone()
        
        #USER
        if e.updat_usrnbr.grpnbr.grpid not in ('Integration Process', 'System Processes'):
        
            #INSTRUMENT
            old_entity=ael.get_old_entity()
            new_entity=e
            
            #x = 0
            '''
            #ADDITIONAL PAYMENTS
            if e.record_type == 'Payment':
                #try:
                    #print 'HERE', ael.get_old_entity()
                    if  ael.get_old_entity().pp() <> None:
                        if e.pp() <> ael.get_old_entity().pp():
                            output = ''
                            output = output + ('\n<Entity>\n')
                        
                            if e.trdnbr.status != 'Simulated':
                                try:
                                    prf = e.trdnbr.prfnbr.prfid
                                    reltrd = str(e.trdnbr.trdnbr)
                                    stat = str(e.trdnbr.status)
                                    confoDate = str(e.trdnbr.add_info('Confo Date Sent'))
                                    confoText = e.trdnbr.add_info('Confo Text')
                                    acq = e.trdnbr.acquirer_ptynbr.ptyid
                                    trd_time = str(ael.date_from_time(e.trdnbr.time))
                                except:
                                    prf = ''
                                    reltrd = ''
                                    stat = ''
                                    confoDate = ''
                                    confoText = ''
                                    acq = ''
                                    trd_time = ''
                            else:
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''                            
                                
                        
                            #Write static fields
                            output = output + '   <Name>' + e.record_type + '</Name>\n'
                            output = output + '   <Key>' +  str(e.paynbr) + '</Key>\n'
                            output = output + '   <UpdatedUser>' + e.display_id('updat_usrnbr') + '</UpdatedUser>\n'
                            output = output + '   <UpdatedTime>' + str(ael.date_from_time(e.updat_time)) + '</UpdatedTime>\n'
                            output = output + '   <CreateTime>' + str(ael.date_from_time(e.creat_time)) + '</CreateTime>\n'
                            output = output + '   <TradeTime>' + trd_time + '</TradeTime>\n'                            
                            output = output + '   <Portfolio>' + prf + '</Portfolio>\n'
                            output = output + '   <RelTrade>' + reltrd + '</RelTrade>\n'
                            output = output + '   <Status>' + stat + '</Status>\n'
                            output = output + '   <RelInstrument>' + e.trdnbr.insaddr.insid + '</RelInstrument>\n'
                            output = output + '   <ConfoSent>' + confoDate + '</ConfoSent>\n'
                            output = output + '   <ConfoText>' + confoText + '</ConfoText>\n'
                            output = output + '   <Acquirer>' + acq + '</Acquirer>\n'
                            output = output + '   <Columns>\n'
                        
                            #Loop through changes and add to output xml
                            amendold[e_clone.original().paynbr] = ael.get_old_entity().pp().split('\n') 
                            amendnew[e.paynbr] = e.pp().split('\n') 
                        
                            cols = buildColumns(amendold, amendnew, e.record_type, e.paynbr)

                            if cols != '-1':
                                output = output + cols
                                output = output + '   </Columns>\n'
                                output = output + '</Entity>\n'
                            else:
                                output = ''
                                return
                            
                            #print output        

                            currentUpdateTime  = '   <UpdatedTime>' + str(e.updat_time) + '</UpdatedTime>\n'
                            key12 =              '   <Key>' +  str(e.paynbr) + '</Key>\n'
                #except:
                #    print "Error in PAYMENT code line 226",op


            #RESET        
            if e.record_type ==  'Reset':
                #try:
                    if  ael.get_old_entity().pp() <> None:
                        if e.pp() <>   ael.get_old_entity().pp():
                            output = ''
                            output = output + ('\n<Entity>\n')

                            if (e.cfwnbr.legnbr.insaddr.trades() == None) or (e.cfwnbr.legnbr.insaddr.trades().members() == []):
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''
                            elif e.cfwnbr.legnbr.insaddr.trades()[0].status != 'Simulated':
                                try:
                                    prf = e.cfwnbr.legnbr.insaddr.trades()[0].prfnbr.prfid
                                    reltrd = str(e.cfwnbr.legnbr.insaddr.trades()[0].trdnbr)
                                    stat = e.cfwnbr.legnbr.insaddr.trades()[0].status
                                    confoDate = str(e.cfwnbr.legnbr.insaddr.trades()[0].add_info('Confo Date Sent'))
                                    confoText = e.cfwnbr.legnbr.insaddr.trades()[0].add_info('Confo Text')
                                    acq = e.cfwnbr.legnbr.insaddr.trades()[0].acquirer_ptynbr.ptyid
                                    trd_time = str(ael.date_from_time(e.cfwnbr.legnbr.insaddr.trades()[0].time))                                                                
                                except:
                                    prf = ''
                                    reltrd = ''
                                    stat = ''
                                    confoDate = ''
                                    confoText = ''
                                    acq = ''
                                    trd_time = ''
                            else:
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''


                            
                            #Write static fields
                            output = output + '   <Name>' + e.record_type + '</Name>\n'
                            output = output + '   <Key>' +  str(e.resnbr) + '</Key>\n'
                            output = output + '   <UpdatedUser>' + e.display_id('updat_usrnbr') + '</UpdatedUser>\n'
                            output = output + '   <UpdatedTime>' + str(ael.date_from_time(e.updat_time)) + '</UpdatedTime>\n'
                            output = output + '   <CreateTime>' + str(ael.date_from_time(e.creat_time)) + '</CreateTime>\n'
                            output = output + '   <TradeTime>' + trd_time + '</TradeTime>\n'                              
                            output = output + '   <Portfolio>' + prf + '</Portfolio>\n'
                            output = output + '   <RelTrade>' + reltrd + '</RelTrade>\n'
                            output = output + '   <Status>' + stat + '</Status>\n'
                            output = output + '   <RelInstrument>' + e.cfwnbr.legnbr.insaddr.insid + '</RelInstrument>\n'
                            output = output + '   <ConfoSent>' + confoDate + '</ConfoSent>\n'
                            output = output + '   <ConfoText>' + confoText + '</ConfoText>\n'
                            output = output + '   <Acquirer>' + acq + '</Acquirer>\n'
                            output = output + '   <Columns>\n'

                            #Loop through changes and add to output xml
                            amendold[e_clone.original().resnbr] = ael.get_old_entity().pp().split('\n') 
                            amendnew[e.resnbr] =  e.pp().split('\n') 
                            
                            cols = buildColumns(amendold, amendnew, e.record_type, e.resnbr)

                            if cols != '-1':
                                output = output + cols
                                output = output + '   </Columns>\n'
                                output = output + '</Entity>\n'
                            else:
                                output = ''
                                return
                            
                            #print output        

                            currentUpdateTime  = '   <UpdatedTime>' + str(e.updat_time) + '</UpdatedTime>\n'
                            key12 =              '   <Key>' +  str(e.resnbr) + '</Key>\n'

                #except:
                #    print "Error pp in Reset line 230",op


            '''
            #CASHFLOW        
            if e.record_type == 'CashFlow':
                #try:
                    if  ael.get_old_entity().pp() <> None:
                        if e.pp() <>   ael.get_old_entity().pp():

                            hastrades = 0
                            for t in e.legnbr.insaddr.trades():
                                if t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                                    hastrades = hastrades + 1
                                    
                            if hastrades > 0:
                                output = ''
                                output = output + ('\n<Entity>\n')                                    

                                try:
                                    prf = e.legnbr.insaddr.trades()[0].prfnbr.prfid
                                    reltrd = str(e.legnbr.insaddr.trades()[0].trdnbr)
                                    stat = e.legnbr.insaddr.trades()[0].status
                                    confoDate = str(e.legnbr.insaddr.trades()[0].add_info('Confo Date Sent'))
                                    confoText = e.legnbr.insaddr.trades()[0].add_info('Confo Text')
                                    acq = e.legnbr.insaddr.trades()[0].acquirer_ptynbr.ptyid
                                    trd_time = str(ael.date_from_time(e.legnbr.insaddr.trades()[0].time))                                
                                except:
                                    prf = ''
                                    reltrd = ''
                                    stat = ''
                                    confoDate = ''
                                    confoText = ''
                                    acq = ''
                                    trd_time = '' 

                            
                                #Write static fields
                                output = output + '   <Name>' + e.record_type + '</Name>\n'
                                output = output + '   <Key>' +  str(e.cfwnbr) + '</Key>\n'
                                output = output + '   <UpdatedUser>' + e.display_id('updat_usrnbr') + '</UpdatedUser>\n'
                                output = output + '   <UpdatedTime>' + str(ael.date_from_time(e.updat_time)) + '</UpdatedTime>\n'
                                output = output + '   <CreateTime>' + str(ael.date_from_time(e.creat_time)) + '</CreateTime>\n'
                                output = output + '   <TradeTime>' + trd_time + '</TradeTime>\n'                              
                                output = output + '   <Portfolio>' + prf + '</Portfolio>\n'
                                output = output + '   <RelTrade>' + reltrd + '</RelTrade>\n'
                                output = output + '   <Status>' + stat + '</Status>\n'
                                output = output + '   <RelInstrument>' + e.legnbr.insaddr.insid + '</RelInstrument>\n'
                                output = output + '   <ConfoSent>' + confoDate + '</ConfoSent>\n'
                                output = output + '   <ConfoText>' + confoText + '</ConfoText>\n'
                                output = output + '   <Acquirer>' + acq + '</Acquirer>\n'
                                output = output + '   <Columns>\n'
    
                                #Loop through changes and add to output xml
                                amendold[e_clone.original().cfwnbr] = ael.get_old_entity().pp().split('\n') 
                                amendnew[e.cfwnbr] = e.pp().split('\n') 
                                
                                cols = buildColumns(amendold, amendnew, e.record_type, e.cfwnbr)
    
                                if cols != '-1':
                                    output = output + cols
                                    output = output + '   </Columns>\n'
                                    output = output + '</Entity>\n'
                                else:
                                    output = ''
                                    return
                                
                                #print output        
                                currentUpdateTime  = '   <UpdatedTime>' + str(e.updat_time) + '</UpdatedTime>\n'
                                #key12 =              '   <Key>' +  str(e.cfwnbr) + '</Key>\n'

                #except:
                #    print 'Error pp in Cashflow line 261',op
        


        
            #LEG        
            if e.record_type == 'Leg':
                #try:
                    if ael.get_old_entity().pp() <> None:
                        if e.pp() <> ael.get_old_entity().pp():
                        
                            hastrades = 0
                            for t in e.insaddr.trades():
                                if t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                                    hastrades = hastrades + 1
                                    
                            if hastrades > 0:
                                output = ''
                                output = output + ('\n<Entity>\n')

                                try:
                                    prf = e.insaddr.trades()[0].prfnbr.prfid
                                    reltrd = str(e.insaddr.trades()[0].trdnbr)
                                    stat = str(e.insaddr.trades()[0].status)
                                    confoDate = str(e.insaddr.trades()[0].add_info('Confo Date Sent'))
                                    confoText = e.insaddr.trades()[0].add_info('Confo Text')
                                    acq = e.insaddr.trades()[0].acquirer_ptynbr.ptyid
                                    trd_time = str(ael.date_from_time(e.insaddr.trades()[0].time))                                
                                except:
                                    prf = ''
                                    reltrd = ''
                                    stat = ''
                                    confoDate = ''
                                    confoText = ''
                                    acq = ''
                                    trd_time = ''                            
                            
                                #Write static fields
                                output = output + '   <Name>' + e.record_type + '</Name>\n'
                                output = output + '   <Key>' +  str(e.legnbr) + '</Key>\n'
                                output = output + '   <UpdatedUser>' + e.display_id('updat_usrnbr') + '</UpdatedUser>\n'
                                output = output + '   <UpdatedTime>' + str(ael.date_from_time(e.updat_time)) + '</UpdatedTime>\n'
                                output = output + '   <CreateTime>' + str(ael.date_from_time(e.creat_time)) + '</CreateTime>\n'
                                output = output + '   <TradeTime>' + trd_time + '</TradeTime>\n'  
                                output = output + '   <Portfolio>' + prf + '</Portfolio>\n'
                                output = output + '   <RelTrade>' + reltrd + '</RelTrade>\n'
                                output = output + '   <Status>' + stat + '</Status>\n'
                                output = output + '   <RelInstrument>' + e.insaddr.insid + '</RelInstrument>\n'
                                output = output + '   <ConfoSent>' + confoDate + '</ConfoSent>\n'
                                output = output + '   <ConfoText>' + confoText + '</ConfoText>\n'
                                output = output + '   <Acquirer>' + acq + '</Acquirer>\n'
                                output = output + '   <Columns>\n'
    
    
                                #Loop through changes and add to output xml
                                amendold[e_clone.original().legnbr] = ael.get_old_entity().pp().split('\n') 
                                amendnew[e.legnbr] =  e.pp().split('\n') 
                                
                                cols = buildColumns(amendold, amendnew, e.record_type, e.legnbr)
    
                                if cols != '-1':
                                    output = output + cols
                                    output = output + '   </Columns>\n'
                                    output = output + '</Entity>\n'
                                else:
                                    output = ''
                                    return
                                
                                #print output        
    
                                currentUpdateTime  = '   <UpdatedTime>' + str(e.updat_time) + '</UpdatedTime>\n'
                                #key12 =              '   <Key>' +  str(e.legnbr) + '</Key>\n'

                #except:
                #    print "Error pp in LEG line 295",op
                       
                    
             
                   
            #INSTRUMENT     
            if e.record_type ==  'Instrument':
                #try:
                    if  ael.get_old_entity().pp() <> None:
                        if e.pp() <> ael.get_old_entity().pp():
                        
                            hastrades = 0
                            for t in e.trades():
                                if t.status in ('FO Confirmed', 'BO Confirmed', 'BO-BO Confirmed'):
                                    hastrades = hastrades + 1
                                    
                            if hastrades > 0:
                                output = ''
                                output = output + ('\n<Entity>\n')
                            
                                #print 'INDEXXXXXXXXXXXXXXXXXXXXXX', e.trades().members()
                                try:
                                    prf = e.trades()[0].prfnbr.prfid
                                    reltrd = str(e.trades()[0].trdnbr)
                                    stat = str(e.trades()[0].status)
                                    confoDate = str(e.trades()[0].add_info('Confo Date Sent'))
                                    confoText = e.trades()[0].add_info('Confo Text')
                                    acq = e.trades()[0].acquirer_ptynbr.ptyid
                                    trd_time = str(ael.date_from_time(e.trades()[0].time))
                                except:
                                    prf = ''
                                    reltrd = ''
                                    stat = ''
                                    confoDate = ''
                                    confoText = ''
                                    acq = ''
                                    trd_time = ''                            
                            
                        
                                #Write static fields
                                output = output + '   <Name>' + e.record_type + '</Name>\n'
                                output = output + '   <Key>' +  str(e.insaddr) + '</Key>\n'
                                output = output + '   <UpdatedUser>' + e.display_id('updat_usrnbr') + '</UpdatedUser>\n'
                                output = output + '   <UpdatedTime>' + str(ael.date_from_time(e.updat_time)) + '</UpdatedTime>\n'
                                output = output + '   <CreateTime>' + str(ael.date_from_time(e.creat_time)) + '</CreateTime>\n'
                                output = output + '   <TradeTime>' + trd_time + '</TradeTime>\n'                            
                                output = output + '   <Portfolio>' + prf + '</Portfolio>\n'
                                output = output + '   <RelTrade>' + reltrd + '</RelTrade>\n'
                                output = output + '   <Status>' + stat + '</Status>\n'
                                output = output + '   <RelInstrument>' + e.insid + '</RelInstrument>\n'
                                output = output + '   <ConfoSent>' + confoDate + '</ConfoSent>\n'
                                output = output + '   <ConfoText>' + confoText + '</ConfoText>\n'
                                output = output + '   <Acquirer>' + acq + '</Acquirer>\n'
                                output = output + '   <Columns>\n'
                            
                                #Loop through changes and add to output xml
                                amendold[e_clone.original().insaddr] = ael.get_old_entity().pp().split('\n') 
                                amendnew[e.insaddr] = e.pp().split('\n') 
                            
                                cols = buildColumns(amendold, amendnew, e.record_type, e.insaddr)
    
                                if cols != '-1':
                                    output = output + cols
                                    output = output + '   </Columns>\n'
                                    output = output + '</Entity>\n'
                                else:
                                    output = ''
                                    return
                                
                                #print output        
                                currentUpdateTime  = '   <UpdatedTime>' + str(e.updat_time) + '</UpdatedTime>\n'
                                #key12 =              '   <Key>' +  str(e.insaddr) + '</Key>\n'
                #except:
                #    print "Error in INSTRUMENT code line 472",op

                
            #TRADE
            if e.record_type ==  'Trade':
                #try:
                    #print e.pp() == ael.get_old_entity().pp()
                    if e.pp() <> ael.get_old_entity().pp():
                        if e.status != 'Simulated':
                            output = ''
                            output = output + ('\n<Entity>\n')
                            #print e.trdnbr ,e_clone.original().trdnbr , '@@@@@@@@'
                            #print e.pp().split('\n') 
                        
                            #Write static fields
                            output = output + '   <Name>' + e.record_type + '</Name>\n'
                            output = output + '   <Key>' +  str(e.trdnbr) + '</Key>\n'
                            output = output + '   <UpdatedUser>' + e.display_id('updat_usrnbr') + '</UpdatedUser>\n'
                            output = output + '   <UpdatedTime>' + str(ael.date_from_time(e.updat_time)) + '</UpdatedTime>\n'
                            output = output + '   <CreateTime>' + str(ael.date_from_time(e.creat_time)) + '</CreateTime>\n'
                            output = output + '   <TradeTime>' + str(ael.date_from_time(e.time)) + '</TradeTime>\n'
                            output = output + '   <Portfolio>' + e.prfnbr.prfid + '</Portfolio>\n'
                            output = output + '   <RelTrade>' + str(e.trdnbr) + '</RelTrade>\n'
                            output = output + '   <Status>' + e.status + '</Status>\n'
                            output = output + '   <RelInstrument>' + e.insaddr.insid + '</RelInstrument>\n'
                            output = output + '   <ConfoSent>' + str(e.add_info('Confo Date Sent')) + '</ConfoSent>\n'
                            output = output + '   <ConfoText>' + e.add_info('Confo Text') + '</ConfoText>\n'
                            output = output + '   <Acquirer>' + e.acquirer_ptynbr.ptyid + '</Acquirer>\n'
                            output = output + '   <Columns>\n'
                        
                            #Loop through changes and add to output xml
                            amendold[e_clone.original().trdnbr] = ael.get_old_entity().pp().split('\n') 
                            amendnew[e.trdnbr] = e.pp().split('\n') 
    
                            cols = buildColumns(amendold, amendnew, e.record_type, e.trdnbr)

                            if cols != '-1':
                                output = output + cols
                                output = output + '   </Columns>\n'
                                output = output + '</Entity>\n'
                            else:
                                output = ''
                                return
                                    
                            #print output
                            currentUpdateTime  = '   <UpdatedTime>' + str(e.updat_time) + '</UpdatedTime>\n'
                            #key12 =              '   <Key>' +  str(e.trdnbr) + '</Key>\n'

                        else:
                            output = ''
                            return
                #except:
                #    print "Error in Trade code line 458.",op
                    
        else:
            #'Admin / IT feed update'
            pass
            
    else:
        #SessionInsertIgnoreCounterStart = SessionInsertIgnoreCounterStart + 1
        pass
        #print "Entity insert ignored."

    if not os.path.exists(path + '.xml'):
        amendment = open(path + '.xml', 'w')
        amendment.writelines('<TODAY>')
        amendment.writelines(output)
        amendment.close
    else:
        '''
        amendmentRead  = open(path + '.xml','r')
        text = amendmentRead.readlines()
        amendmentRead.close()
        
        if e.record_type  <> 'Instrument':
            for line in text:
                if line == key12  and flag_key == 0:
                    flag_key  = 1
                if line == currentUpdateTime  and flag_time == 0: 
                    flag_time = 1
                if flag_key == 1 and flag_time == 1:
                    flag  = 1
                    break
        '''
        if flag == 0:
            #If the entity already exist do not write to file
            amendment = open(path + '.xml', 'a')
            amendment.writelines(output)
            amendment.close




def buildColumns(amendold, amendnew, type, k, *rest):
    '''
    if type == 'Trade':
        k = e.trdnbr
    elif type == 'Instrument':
        k = e.insaddr
    elif type == 'Leg':
        k = e.legnbr
    elif type == 'Cashflow':
        k = e.cfwnbr
    elif type == 'Reset':
        k = e.resnbr
    else:
        #print type, ' not a valid type'
        return '-1'
    '''        
    cols = ''
    x = 0
    status_change = 'no'
    while x < len(amendold[k]):
        if amendold[k][x] <> amendnew[k][x]: 
            #splits each line by a double space and removes any whitespace.
            e_old = amendold[k][x].split('  ')
            e_new = amendnew[k][x].split('  ')
            name = e_old[0].strip()
            if name in ('premium', 'quantity', 'price', 'amount'):
                val_old = (str)((float)(e_old[len(e_old)-1].strip()))
                val_new = (str)((float)(e_new[len(e_new)-1].strip()))
            else:
                val_old = e_old[len(e_old)-1].strip()
                val_new = e_new[len(e_new)-1].strip()
                
            if type == 'Trade' and name == 'status':
                status_change = 'yes'
           
            if name not in ('updat_time', 'updat_usrnbr', 'version_id', 'bo_trdnbr', 'execution_time', 'your_ref', 'optional_key'):
                cols = cols + '      <Column>\n'
                cols = cols + '         <Name>' + name + '</Name>\n'
                cols = cols + '         <Original>\n            <Value>' + val_old + '</Value>\n         </Original>\n'
                cols = cols + '         <Current>\n            <Value>' + val_new + '</Value>\n         </Current>\n'
                cols = cols + '      </Column>\n'
                                    
            #original = original  + '\n      <' + dict[counter] + '> ' +  amendold[e.trdnbr][x] + '</' + dict[counter] + '>'
            #current  = current   + '\n      <' + dict[counter] + '> ' + amendnew[e.trdnbr][x] + '</' + dict[counter] + '>'
            #counter = counter+1
    
        x = x + 1
        

    if type == 'Trade' and status_change == 'yes':
        if cols.count('<Column>') >= 2:
            return cols
        else:
            #print 'Only Status Change'
            return '-1'
    else:
        if cols == '':
            return '-1'
        else:
            return cols


#main
start()
#stop()
