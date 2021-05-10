""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/upgrade/FConfirmationUpgradeContact.py"
''' 
Script for populating contact references on existing confirmations.
'''

import ael
import acm
import FOperationsUtils as Utils
ael_variables = []

def FindAcquirerContact(conf):
    aelConf = ael.Confirmation[conf.Oid()]
    aelContact = aelConf.contact('Intern Dept')
    if aelContact == None:
        return
    acmContact = acm.FContact[aelContact.seqnbr]
    if acmContact.Fullname() == conf.AcquirerContact():
        conf.AcquirerContactRef(acmContact)

def FindCounterpartyContact(conf):
    aelConf = ael.Confirmation[conf.Oid()]
    aelContact = aelConf.contact('Counterparty')
    if aelContact == None:
        return
    acmContact = acm.FContact[aelContact.seqnbr]
    if acmContact.Fullname() == conf.CounterpartyContact():
        conf.CounterpartyContactRef(acmContact)

def UpgradeConfirmation(confirmation):
    try:
        clone = confirmation.Clone()
        FindAcquirerContact(clone)
        FindCounterpartyContact(clone)

        confirmation.Apply(clone)
        confirmation.Commit()
    except Exception as e:
        Utils.Log(True, str(e))

def ael_main(parameterDictionary):
    Utils.Log(True, 'Upgrade started')
    confirmations = acm.FConfirmation.Select('acquirerContactRef = None or counterpartyContactRef = None').AsArray()
    Utils.Log(True, '%d confirmations to upgrade' % len(confirmations) )

    counter = 0
    for conf in confirmations:
        UpgradeConfirmation(conf)

        counter += 1
        if((counter % 100) == 0):
            Utils.Log(True, '%d upgraded, please wait...' % counter)
    
    Utils.Log(True, 'Upgrade finished')