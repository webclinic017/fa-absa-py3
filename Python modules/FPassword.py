'''-----------------------------------------------------------------------
MODULE
  FPassword

DESCRIPTION
  The FPassword module must be activated by checking the Password Hook Installation checkbox
  under Admin>Administration Console>Control Parameters, before it will be invoked. 
 
  The validate_password function is then called whenever a user changes his/her password. 

History:
Date            Who                     What
2009-03-05	Herman Hoon             CR: 373907: SOX Passwords - Password requirements: alphanumeric and at least 6 characters long.

ENDDESCRIPTION
-----------------------------------------------------------------------'''

import re
import ael
import datetime

def set_user_addinf(e, spec_string, new_value):
    try:
        ael.begin_transaction()

        spec = ael.AdditionalInfoSpec[spec_string]
        if e.add_info(spec_string):
            # Add Info already exists
            for ai in e.additional_infos():
                if ai.addinf_specnbr == spec:
                    ai_c = ai.clone()
                    ai_c.value = str(new_value)
                    ai_c.commit()
        else:
            # Create new additional Info record for this entity
            e_c = e.clone()
            ai = ael.AdditionalInfo.new(e_c)
            ai.addinf_specnbr = spec
            ai.value = str(new_value)
            ai.commit()
        ael.commit_transaction()

    except:
	ael.abort_transaction()
        print spec_string + ' not resetted for user ' + e.userid
	
    	
def validate_password (password, user):
    if ((user.grpnbr.orgnbr != 162) or (user.grpnbr.orgnbr == 162 and user.grpnbr in (494, 495))):
    
        upperpass   = re.compile("[A-Z]+").search(password)
        lowerpass   = re.compile("[a-z]+").search(password)
        numericpass = re.compile("[0-9]+").search(password)
        letterpass  = re.compile("[a-zA-Z]+").search(password)
        
        if len(password) < 8:
            return [0, 'The password must contain at least 8 characters']
        elif upperpass == None  or lowerpass == None:
            return [0, 'Password must contain upper and lower case letters']
        elif numericpass == None  or letterpass == None:
            return [0, 'Password should be alphanumeric (letters and numbers)']
        else:
            set_user_addinf(user, 'PasswordResetDate', datetime.date.today())
            return [1, 'Password changed successfully']

