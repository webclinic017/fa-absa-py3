'''
Description : Once off script to clean up email addresses - Data provided by OPS
              Only updates contact rules for deposits

'''

import csv
import ael, acm
import FBDPGui
import re
from at_time import to_date

def PopulatePartyDetails(filePath, instype):

    with open(filePath, 'r') as csvFile:
        reader = csv.DictReader(csvFile, delimiter=',')
        for row in reader:
            try:
                if(row['instype'].upper() == instype.upper()):
                    PopulatePartyContactEntry(row)                    
            except Exception, e:
                print 'ERROR:', str(e), row['ptyid'], ' -- ', row['fullname']
                    
    print 'Completed email address clean up!'


def IsValidEmailAddress(emailAddress):

    return re.match(r"[^@]+@[^@]+\.[^@]+", emailAddress)


def PopulatePartyContactEntry(dict):
    """ Add or update contact entry with new email address """

    party = acm.FParty[dict['ptyid']]
    
    if(party):
        if party.Contacts():
            for contact in party.Contacts():                
                if(contact.Fullname().upper() == dict['fullname'].upper()
                    and contact.Email().upper() == dict['email'].upper()
                        and dict['newemail'] and IsValidEmailAddress(dict['newemail'])): 
                                                                                    
                            strippedEmail = dict['newemail'].strip()
                            if strippedEmail.endswith(';'):
                                strippedEmail = strippedEmail[:-1]

                            a, b = strippedEmail, {"/":",", " ":"", "'":""}
                                        
                            newEmail = "".join([b.get(c, c) for c in strippedEmail]).replace(';', ',')

                            contactClone = contact.Clone()
                            oldEmail = contactClone.Email()                                            
                            contactClone.Email = newEmail
                                                                                              
                            try:
                                contact.Apply(contactClone)                                                
                                contact.Commit()
                                print 'Party updated:', dict['ptyid'], ' -- ', dict['fullname'].upper(), ' From Email:', oldEmail, '  To Email:', contact.Email()
                            except Exception, e:
                                contact.Undo()
                                print 'Could not update party:', dict['ptyid'], ' -- ', dict['fullname'].upper(), '.  Details:', str(e)           
        
    else:
        print 'Party not found:', dict['ptyid']
            
'''
AEL Variables :
Variable Name, Display Name, Type, Candidate Values, Default, 
Mandatory, Multiple, Description, Input Hook, Enabled
'''

ael_variables = FBDPGui.DefaultVariables(
                                            ['filePath', 'File Root', 
                                                'string', None, 'F:\PartyEmailAddresses_15052015.csv',  1, 0, 'Input file', None, 1],                                                
                                            ['instype', 'Instrument Type', 
                                                'string', None, 'Deposit',  1, 0, 'Event', None, 1])    
    
def ael_main(dict):
    """ Main method """
    
    try:
        filePath = dict['filePath']
        instype = dict['instype']
    except:
        return 'Error trying to get parameter values'
    
    PopulatePartyDetails(filePath, instype)

