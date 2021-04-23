import ael, datetime


def updatePasswordReset(user):
    try:
        lastReset = datetime.date.today()
        spec = ael.AdditionalInfoSpec['PasswordResetDate']
        for ai in user.additional_infos():
          if ai.addinf_specnbr == spec:
                ai_c = ai.clone()
                ai_c.value = str(lastReset)
                ai_c.commit()
    except:
        print 'Password last reset date not resetted for user ', user
        

for user in ael.User.select():
    if user.userid[0:2] in ('AB', 'EX') and user.userid != 'EXTRACT': 
        updatePasswordReset(user)
