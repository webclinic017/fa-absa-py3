import acm, ael

'''
Purpose                       :  User Feed for Barcap
Department and Desk           :  IT
Requester                     :  Rod Jardine
Developer                     :  Ickin Vural
CR Number                     :  C000000476794

'''

ael_variables = [['FileName', 'File Name', 'string', None, 'BarCap_Latte.txt', 1],
                 ['Path', 'Path', 'string', None, 'F:\\', 1]]

def ael_main(parameter, *rest):
    
        
    path = parameter['Path']
    filename = parameter['FileName']
    
    fileName = path + filename
    
    outfile=  open(fileName, 'w')
    


    users = acm.FUser.Select('recordType = User')

    for user in users:
        try:
            if user.UserGroup().Name() not in ('Previous User', 'AAM Previous User'): 
                
                UserID       = user.Name() 
                if UserID[0:2] in ['AB', 'EX']:
                    if user.AdditionalInfo().AB_Number() != None:
                        UserID   = user.AdditionalInfo().AB_Number()
                    else:
                        UserID       = user.Name() 
                        
                User_Name    = user.Name()
                ProfileName  = user.UserGroup().Name()
                ProfileValue = ''
                updUser      = user.UpdateUser().Name()
                updTime      = ''
                LastUsed     = ''
                EntityName   = ''
                                
                outfile.write('%s|%s|%s|%s|%s|%s|%s|%s\n'%(UserID, User_Name, ProfileName, ProfileValue, updUser, updTime, LastUsed, EntityName))
        
        except:
            pass

    outfile.close()
    print 'Wrote secondary output to:::' + fileName
