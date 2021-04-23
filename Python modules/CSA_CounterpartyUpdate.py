'''
Script is used to run through all parties which have BarCap_SMS_CP_SDSID and/or BarCap_SMS_LE_SDSID and validates the correctness of this detail against an external file.

Date            CR              Developer               Requesteor              Change
==========      =========       ======================  ======================  ========================================================
2012-08-10      CHNG0000357072  Willie van der Bank     Dirk Strauss            Minor changes by Dirk Strauss
'''

import ael, csv, sys, time

ael_variables = [ 
                ('FileName', 'File Name: ', 'string', None, 'c:\\temp\\CSA_Data_2012-03-06.tab', 1),
                ('update_pty', 'Update Party: ', 'string', ['Yes', 'No'], 'No', 1)
                ]
                
csv_template = csv.get_dialect('excel-tab')
global p_update_pty

#-----------------------------------------------------------------------------------------------------
def PadStr(s, n):
    s = str(s)
    
    k = len(s)
    
    if k >= n:
        ret = s[0:n]
    else:
        ret = s + ' ' * (n-k)
        
    return ret

#-----------------------------------------------------------------------------------------------------
def delete_addinfo(entity, ai_name):
    # Sets an additional info field for a given entity
    global p_update_pty    
    
    print PadStr(entity.display_id(), 50), ' - Deleting add_info : ', ai_name
    
    if p_update_pty:
        ent_clone = entity.clone()
        
        # Clone the additional info entity if it exists, otherwise create a new additional info
        for ai in ent_clone.additional_infos():
            if ai.addinf_specnbr.field_name == ai_name:            
                ai.delete()            
        try:
            ent_clone.commit()
            ael.poll()
        except:
            print '\n', '-' * 20, '\nError: Could not delete additional info value %s' %(ai_name), '\n', sys.exc_info(),  '\n', '-' * 20, '\n'


#-----------------------------------------------------------------------------------------------------
def set_addinfo(entity, ai_name, ai_value):    
    # Sets an additional info field for a given entity   
    
    if ai_value:
        global p_update_pty        
        
        ent_clone = entity.clone()
        
        # Clone the additional info entity if it exists, otherwise create a new additional info
        for ai in entity.additional_infos():
            if ai.addinf_specnbr.field_name == ai_name:
                if ai.value == ai_value:
                    return
                    
                new_ai = ai.clone()
                break
        else:
            new_ai = ael.AdditionalInfo.new(ent_clone)
            new_ai.addinf_specnbr = ael.AdditionalInfoSpec[ai_name]
        
        print PadStr(entity.display_id(), 50), ' - add_info :', ai_name, '  :  *' + new_ai.value + '*  ===>>>  *' + ai_value + '*'

        if p_update_pty:        
            new_ai.value = str(ai_value)
            
            try:
                new_ai.commit()
                ael.poll()
                #       ent_clone.commit()
            except:
                print '\n', '-' * 20, '\nError: Could not Update additional info value %s' %(ai_name), '\n', sys.exc_info(),  '\n', '-' * 20, '\n'

#-----------------------------------------------------------------------------------------------------
def ael_main(data):
    print time.ctime()
    print 'Start....'

    global p_update_pty
    
    sfile = data['FileName']
    p_update_pty = [0, 1][data['update_pty'] == 'Yes']
    
    print 'Reading data from : ', sfile
    print 'commit changes : ', p_update_pty
    
    # read CAS data from file
    f_in = csv.reader( open(sfile, 'r'), csv_template)

    dat = {}
    k = 0

    for row in f_in:
        k += 1
        
        if k > 1:
            sds = row[0]
            csa_name = row[1]
            ccy = row[2]
            csa_type = row[3]
            csa_switch_date = ''
            if row[4]:
                csa_switch_date = row[4]
            csa_ccy2 = ''
            if row[5]:
                csa_ccy2 = row[5]
            
            if dat.has_key(sds):
                print 'ERROR - Duplicate SDS : ', sds
            else:
                dat[sds] = [csa_name, ccy, csa_type, csa_switch_date, csa_ccy2]

    ptys = ael.Party    

    print '\n'
    print '-' * 75
    
    # loop through Party objects and update if data in file
    for pty in ptys:
        ptyid = pty.ptyid
        
        #       print '-' * 50
        #       print ptyid
        
        cp_sds = pty.add_info('BarCap_SMS_CP_SDSID')
        le_sds = pty.add_info('BarCap_SMS_LE_SDSID')
        
        if cp_sds == le_sds:
            le_sds = 0
            
        if dat.has_key(cp_sds):
            csa_dat = dat[cp_sds]
            #   print 'Match on CP sds - ', cp_sds
        elif dat.has_key(le_sds):
            csa_dat = dat[le_sds]
            #   print 'Match on LE sds - ', le_sds
        else:
            csa_dat = None
            #   print 'No match'
            
        if csa_dat:
            #   print 'Setting add_info'
            set_addinfo(pty, 'CSA', 'Yes')
            set_addinfo(pty, 'CSA Name', csa_dat[0][0:39].rstrip(' '))
            set_addinfo(pty, 'CSA Collateral Curr', csa_dat[1])
            set_addinfo(pty, 'CSA Type', csa_dat[2])
            if csa_dat[3]:
                set_addinfo(pty, 'CSA Switch Date', csa_dat[3].strip())
            if csa_dat[4]:
                set_addinfo(pty, 'CSA CollateralCurr2', csa_dat[4].strip())
        else:
            if pty.add_info('CSA') == 'Yes':
                #       print 'Party set as CSA but not found in source data - clearing fields'
                delete_addinfo(pty, 'CSA')
                delete_addinfo(pty, 'CSA Name')
                delete_addinfo(pty, 'CSA Collateral Curr')
                delete_addinfo(pty, 'CSA Type')                
                delete_addinfo(pty, 'CSA Switch Date')
                delete_addinfo(pty, 'CSA CollateralCurr2')

        #       print '-' * 50
        #       print '\n' * 2            
    
    print '-' * 75
    print '\n'
    print time.ctime()
    print 'Completed successfully.'

#-----------------------------------------------------------------------------------------------------
