import sys
import ael
import time
import string

ael_variables = []
                

def check_password(user):
    time.sleep(6)
    mailto = user.updat_usrnbr.userid
    msg = 'To change a password go to File -> Preferences -> Passwords -> ADS.'  

    #if  user.updat_usrnbr.userid != ael.User[user.updat_usrnbr].updat_usrnbr.userid.
    
    if ael.User[user.updat_usrnbr.userid].add_info('PasswordResetDate') == '':
        subj = 'Initial Password'
        ael.sendmessage(mailto, subj, msg)
        raise mailto, subj    
    else:
    #Check if password is > 30 days
            ResetDate = ael.date(user.updat_usrnbr.add_info('PasswordResetDate'))
            LatestDate= ael.date_from_time(user.creat_time)           
            
            if ResetDate.days_between(LatestDate) >= 25 and ResetDate.days_between(LatestDate) <= 30:
                subj = 'Password will expire in :' + ResetDate.days_between(LatestDate)
                ael.sendmessage(mailto, subj, msg)
                raise mailto, subj
    
            if ResetDate.days_between(LatestDate) > 30 :
                subj = 'Your password has expired and your userid will be locked please change password now'
                ael.sendmessage(mailto, subj, msg)
                thisuser  = ael.User[mailto].clone()
                thisuser.inactive = 1
                thisuser.commit()
                raise mailto, subj
    
def start():
    #Start subscription on the userlog table
   
    print "Starting UserLog subscription"
    ael.UserLog.subscribe(userlog_update_cb)
    



def stop():
    print "Stopping userlog subscription"
    ael.UserLog.unsubscribe(userlog_update_cb)

def userlog_update_cb(obj, userlog, arg, event): 
    #Check Password if has not expired 

    if event in ['insert', 'update'] and userlog.type in ['Login', 'Logoff']:
#       print obj, userlog.pp(), arg, event
        check_password(userlog)
    
def ael_main(ael_dict):


    if __name__=="__main__":
    # Called from command line, connect first
#   ael.connect('sun23:7771', 'FRED', 'secret', 'TimeSeriesSample')
        start()
        ael.main_loop()
    else:
# Called from GUI client, already connected
        
        stop()
     

