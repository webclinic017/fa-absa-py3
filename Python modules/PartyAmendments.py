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

import ael, time, os

def start():        
    print 'Start in main'
    newdate = ael.date_today().to_string('%Y%m%d')   
    path  = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/Party_Amendments' +  newdate
    #path  = 'c://AmendmentDairy/Party_Amendments' +  newdate

    if not os.path.exists(path + '.txt'):
        amendment = open(path + '.txt', 'w')
        start_text = 'Party Four-Eyes Audit File ' + str(newdate)
        start_text = start_text + '\n\n' + '=======================================================================================================' + '\n\n\n'
        amendment.writelines(start_text)
        amendment.close

    '''
    ael.Instrument.subscribe(listener)
    ael.Leg.subscribe(listener)
    ael.CashFlow.subscribe(listener)
    ael.Reset.subscribe(listener)
    ael.Trade.subscribe(listener)
    ael.Payment.subscribe(listener)
    '''
    ael.ChangeRequest.subscribe(listener)


    
def stop():
    print "Stopping..."
    newdate = ''
    newdate = ael.date_today().to_string('%Y%m%d')   
    path = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/Party_Amendments' +  newdate + '.xml'
    #path = 'c://AmendmentDairy/Party_Amendments' +  newdate + '.txt'

    amendment_new = open(path, 'a')
    amendment_new.close

    ael.ChangeRequest.unsubscribe(listener)
   
    print 'Process Stopped'
    return
    
    
    
def status():
    print 'Status:Party AmendmentListener active'



def listener(o, e, arg, op):
    SessionInsertIgnoreCounterStart = 0
    newdate = ''
    newdate = ael.date_today().to_string('%Y%m%d')   
    path  = '//services/frontnt/BackOffice/Atlas-End-Of-Day/TradeAmendment/Party_Amendments' +  newdate     
    #path  = 'c://AmendmentDairy/Party_Amendments' +  newdate

    # Create initial file for the day.
    if not os.path.exists(path + '.txt'):
        amendment = open(path + '.txt', 'w')
        start_text = 'Party Four-Eyes Audit File ' + str(newdate)
        start_text = start_text + '\n\n' + '=======================================================================================================' + '\n\n\n'
        amendment.close

    amendold = {}
    amendnew = {}
    x = 0
    flag = 0
    
    output = ''
    counter = 0
    original = ''
    current = ''
    
    if op in ('update', 'insert', 'delete'):
        #print 'XXXXXXXXXXXX', e, op
        e_clone = e.clone()
        
        #USER
        if e.updat_usrnbr.grpnbr.grpid not in ('Integration Process', 'System Processes'):
        
            old_entity=ael.get_old_entity()
            new_entity=e
            
            x = 0
        
            if e.record_type == 'ChangeRequest':
                if op == 'insert':
                    output = output + 'Change Requested by: ' + e.display_id('creat_usrnbr') +  '   ' + 'Request Status : ' + e.status + '\n\n'
                    #output = output + 'Change Request Number: ' + e.seqnbr + '\n\n'
                elif op == 'delete':
                    output = output + 'Change Requested by: ' + e.display_id('creat_usrnbr') +  '   ' + 'Request Status : ' + 'Authorized' + '\n\n'
                    output = output + 'Authorized by: ' + e.display_id('authorizer_usrnbr') + '\n\n'
                    #print e.pp()
                    output = output + 'Change Request Number: ' + str(e.seqnbr) + '\n\n'
                elif op == 'update' and e.status == 'Rejected':
                    output = output + 'Change Requested by: ' + e.display_id('creat_usrnbr') +  '   ' + 'Request Status : ' + e.status + '\n\n'
                    output = output + 'Rejected by: ' + e.authorize_comment + '\n\n'
                    output = output + 'Change Request Number: ' + str(e.seqnbr) + '\n\n'
                
                output = output + e.show_changes() + '\n\n\n'
                output = output + '=======================================================================================================' + '\n\n\n'
                print output
                
            
    else:
        SessionInsertIgnoreCounterStart = SessionInsertIgnoreCounterStart + 1
        #print "Entity insert ignored."

    if not os.path.exists(path + '.txt'):
        amendment = open(path + '.txt', 'w')
    else:
        amendment = open(path + '.txt', 'a')

    amendment.writelines(output)
    amendment.close
    
    '''
    else:    
        amendmentRead  = open(path + '.txt','r')
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
            amendment = open(path + '.txt','a')
            amendment.writelines(output)
            amendment.close
    '''



#def buildColumns(amendold, amendnew, type, k, *rest):
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
    '''


#main
#start()
#stop()
