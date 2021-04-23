"""-----------------------------------------------------------------------------------------
2006-11-30 - Tina Viljoen (Sungard)
Module
    Amendment Listener
    (c) Copyright 2006 by Front Capital Systems. All rights reserved

DESCRIPTION     
Amendment Diary     

2007-09-01      Aaeda Salejee           Added buildColumns function to build Column xml tag.
2007-10-01      Aaeda Salejee           Stopped certain amendments from being logged as per business request
-----------------------------------------------------------------------------------------"""

import ael
import time 
import shutil
import os

def start():        
    print 'Start in main'
    date =  ael.date_today().to_ymd()
    newdate = str(date[0])+str(date[1])+str(date[2])
    path  = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/TradeAmendments_Final' +  newdate
    #path  = 'c://AmendmentDairy/TradeAmendments_Final' +  newdate

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
    
def stop():
    print "Stopping..."
    newdate = ''
    date =  ael.date_today().to_ymd()
    newdate = str(date[0])+str(date[1])+str(date[2])
    path = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/TradeAmendments_Final' +  newdate + '.xml'
    #oldpath = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/TradeAmendments' +  newdate +  '.xml'
    #path = 'c://AmendmentDairy/TradeAmendments_Final' +  newdate + '.xml'
    #oldpath = 'c://AmendmentDairy/TradeAmendments' +  newdate +  '.xml'    
    '''
    try:
        print "Copy " + str(oldpath) + " to " + str(path) 
        shutil.copyfile(oldpath,path)
    except:
        print "Copy file " + str(oldpath) + " to " + str(path) + " failed..."
    '''
    amendment_new = open(path, 'a')
    amendment_new.write('</TODAY>\n')
    amendment_new.close
    
    #Convert to HTML
    #xsltName = 'c//services/front/scripts/management/TradeAmendment'
    #xsltName = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/Amendment.xsl'    

    '''        
    xslt = open(xsltName).read()
    xml = open(path).read()
    xml = xml + '</TODAY>\n'
    processor = Processor.Processor()
    transform = InputSource.DefaultFactory.fromString(xslt, "http://pythonworld.net/4Suite/catalog.xslt")
    processor.appendStylesheet(transform)
    source = InputSource.DefaultFactory.fromString(xml, "http://pythonworld.net/4Suite/catalog.xml")
    result = processor.run(source,1)
    '''
    '''
    cfd = open(path.replace('.xml', '.html') ,'w')
    #cfd.write(result)
    cfd.close
    print "HTML file created: " + path.replace('.xml', '.html')
    '''
    print 'Process Stopped'

    return
    
    
    
def status():
    print 'Status:AmendmentListerner active'



def listener(o, e, arg, op):
    SessionInsertIgnoreCounterStart = 0
    newdate = ''
    date =  ael.date_today().to_ymd()
    newdate = str(date[0])+str(date[1])+str(date[2])

    #path  = '//services/front/scripts/management/TradeAmendment/TradeAmendment' +  newdate 
    path  = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/TradeAmendments_Final' +  newdate     
    #path  = 'c://AmendmentDairy/TradeAmendments_Final' +  newdate
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
    x = 0
    flag_time = 0
    flag_key = 0
    flag = 0
    
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
    
    output = ''
    counter = 0
   
    results = []
    
    inst_str = ''
    original = ''
    current = ''
    
    currentUpdateTime  = ''
    key12 =  ''
    
    if op in ('update'):
        e_clone = e.clone()
        
        #USER
        if e.updat_usrnbr.grpnbr.grpid not in ('Integration Process', 'System Processes'):
        
            #INSTRUMENT
            old_entity=ael.get_old_entity()
            new_entity=e
            
            x = 0


            #RESET        
            if e.record_type ==  'Reset':
                #try:
                    if  ael.get_old_entity().pp() <> None:
                        if e.pp() <>   ael.get_old_entity().pp():
                            output = ''
                            output = output + ('\n<Entity>\n')

                            if e.cfwnbr.legnbr.insaddr.trades() == None:
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''
                            elif e.cfwnbr.legnbr.insaddr.trades()[0].status != 'Simulated':
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''
                            else:
                                prf = e.cfwnbr.legnbr.insaddr.trades()[0].prfnbr.prfid
                                reltrd = str(e.cfwnbr.legnbr.insaddr.trades()[0].trdnbr)
                                stat = e.cfwnbr.legnbr.insaddr.trades()[0].status
                                confoDate = str(e.cfwnbr.legnbr.insaddr.trades()[0].add_info('Confo Date Sent'))
                                confoText = e.cfwnbr.legnbr.insaddr.trades()[0].add_info('Confo Text')
                                acq = e.cfwnbr.legnbr.insaddr.trades()[0].acquirer_ptynbr.ptyid
                                trd_time = str(ael.date_from_time(e.cfwnbr.legnbr.insaddr.trades()[0].time))                                                                

                            
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


        
            #CASHFLOW        
            if e.record_type ==  'CashFlow':
                #try:
                    if  ael.get_old_entity().pp() <> None:
                        if e.pp() <>   ael.get_old_entity().pp():
                            output = ''
                            output = output + ('\n<Entity>\n')
                            
                            if e.legnbr.insaddr.trades() == None:
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''
                            elif e.legnbr.insaddr.trades()[0].status != 'Simulated':
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''                            
                            else:
                                prf = e.legnbr.insaddr.trades()[0].prfnbr.prfid
                                reltrd = str(e.legnbr.insaddr.trades()[0].trdnbr)
                                stat = e.legnbr.insaddr.trades()[0].status
                                confoDate = str(e.legnbr.insaddr.trades()[0].add_info('Confo Date Sent'))
                                confoText = e.legnbr.insaddr.trades()[0].add_info('Confo Text')
                                acq = e.legnbr.insaddr.trades()[0].acquirer_ptynbr.ptyid
                                trd_time = str(ael.date_from_time(e.legnbr.insaddr.trades()[0].time))                                
                            
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
                            amendnew[e.cfwnbr] =  e.pp().split('\n') 
                            
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
                            key12 =              '   <Key>' +  str(e.cfwnbr) + '</Key>\n'

                #except:
                #    print 'Error pp in Cashflow line 261',op
        


        
            #LEG        
            if e.record_type == 'Leg':
                #try:
                    if ael.get_old_entity().pp() <> None:
                        if e.pp() <> ael.get_old_entity().pp():
                            output = ''
                            output = output + ('\n<Entity>\n')

                            if e.insaddr.trades() == None:
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''
                            elif e.insaddr.trades()[0].status != 'Simulated':
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''                            
                            else:
                                prf = e.insaddr.trades()[0].prfnbr.prfid
                                reltrd = str(e.insaddr.trades()[0].trdnbr)
                                stat = str(e.insaddr.trades()[0].status)
                                confoDate = str(e.insaddr.trades()[0].add_info('Confo Date Sent'))
                                confoText = e.insaddr.trades()[0].add_info('Confo Text')
                                acq = e.insaddr.trades()[0].acquirer_ptynbr.ptyid
                                trd_time = str(ael.date_from_time(e.insaddr.trades()[0].time))                                

                            
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
                            key12 =              '   <Key>' +  str(e.legnbr) + '</Key>\n'

                #except:
                #    print "Error pp in LEG line 295",op
                       
                    
             
                   
            #INSTRUMENT     
            if e.record_type ==  'Instrument':
                #try:
                    if  ael.get_old_entity().pp() <> None:
                        if e.pp() <> ael.get_old_entity().pp():
                            output = ''
                            output = output + ('\n<Entity>\n')
                        
                            if e.trades() == None: 
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''
                            elif e.trades()[0].status != 'Simulated':
                                prf = ''
                                reltrd = ''
                                stat = ''
                                confoDate = ''
                                confoText = ''
                                acq = ''
                                trd_time = ''                            
                            else:
                                prf = e.trades()[0].prfnbr.prfid
                                reltrd = str(e.trades()[0].trdnbr)
                                stat = str(e.trades()[0].status)
                                confoDate = str(e.trades()[0].add_info('Confo Date Sent'))
                                confoText = e.trades()[0].add_info('Confo Text')
                                acq = e.trades()[0].acquirer_ptynbr.ptyid
                                trd_time = str(ael.date_from_time(e.trades()[0].time))
                        
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
                            amendnew[e.insaddr] =  e.pp().split('\n') 
                        
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
                            key12 =              '   <Key>' +  str(e.insaddr) + '</Key>\n'
                #except:
                #    print "Error in INSTRUMENT code line 472",op

                
            #TRADE
            if e.record_type ==  'Trade':
                #try:
                    #print e.pp() == ael.get_old_entity().pp()
                    if e.pp() <> ael.get_old_entity().pp():
                        output = ''
                        output = output + ('\n<Entity>\n')
                        #print e.trdnbr ,e_clone.original().trdnbr , '@@@@@@@@'
                        #print e.pp().split('\n') 
                        
                        if e.status != 'Simulated':
                            
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
                            key12 =              '   <Key>' +  str(e.trdnbr) + '</Key>\n'

                        else:
                            output = ''
                            return
                        
                        
                #except:
                #    print "Error in Trade code line 458.",op
                    
        else:
            #'Admin / IT feed update'
            pass
            
    else:
        SessionInsertIgnoreCounterStart = SessionInsertIgnoreCounterStart + 1
        #print "Entity insert ignored."

    if not os.path.exists(path + '.xml'):
        amendment = open(path + '.xml', 'w')
        amendment.writelines('<TODAY>')
        amendment.writelines(output)
        amendment.close
    else:
        
        amendmentRead  = open(path + '.xml', 'r')
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
            if name in ('premium', 'quantity', 'price'):
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
#start()
#stop()
