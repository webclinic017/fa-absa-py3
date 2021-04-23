import ael, csv, sys, time

ael_variables = [ 
                ('FileName', 'File Name: ', 'string', None, 'c:\\temp\\csa_data.tab', 1),
                ]
                
csv_template = csv.get_dialect('excel-tab')

#-----------------------------------------------------------------------------------------------------
def delete_addinfo(entity, ai_name):
    # Sets an additional info field for a given entity
    print 'Deleting add_info : ', ai_name
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
def ael_main(data):
    print time.ctime()
    print 'Start....'
    sfile = data['FileName']
    print 'Reading data from : ', sfile
    
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
            
            if dat.has_key(sds):
                print 'DERROR - uplicate SDS : ', sds
            else:
                dat[sds] = [csa_name, ccy, csa_type]
                

    ptys = ael.Party    

    # loop through Party objects and update if data in file
    for pty in ptys:
        ptyid = pty.ptyid
        
        print '-' * 50
        print ptyid
        
        cp_sds = pty.add_info('BarCap_SMS_CP_SDSID')
        le_sds = pty.add_info('BarCap_SMS_LE_SDSID')
        
        if cp_sds == le_sds:
            le_sds = 0
            
        if dat.has_key(cp_sds):
            csa_dat = dat[cp_sds]
            print 'Match on CP sds - ', cp_sds
        elif dat.has_key(le_sds):
            csa_dat = dat[le_sds]
            print 'Match on LE sds - ', le_sds
        else:
            csa_dat = None
            print 'No match'
            
        if pty.add_info('CSA') == 'Yes':
            print 'Clearing CSA Fields'
            delete_addinfo(pty, 'CSA')
            delete_addinfo(pty, 'CSA Name')
            delete_addinfo(pty, 'CSA Collateral Curr')
            delete_addinfo(pty, 'CSA Type')
                            

        print '-' * 50
        print '\n' * 2
        
        print 'done'
        print time.ctime()
        
        
#-----------------------------------------------------------------------------------------------------
