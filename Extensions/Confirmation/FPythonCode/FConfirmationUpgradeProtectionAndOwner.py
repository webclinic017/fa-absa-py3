""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/upgrade/FConfirmationUpgradeProtectionAndOwner.py"
import acm
import FOperationsUtils as Utils

ael_variables = [('run_upgrade', 'Upgrade Confirmation Protection And Owner', 'bool', [False, True], False)]

def UpgradeProtectionAndOwner():
    counter = 0
    confirmations = acm.FConfirmation.Select('')
    for confirmation in confirmations:
        try:
            Utils.SetProtectionAndOwnerFromTrade(confirmation, confirmation.Trade())
            confirmation.Commit()
            counter += 1
            if (counter % 100 == 0):
                Utils.Log(True, '%d confirmations updated, please wait ...' % counter)
        except Exception as error:
            Utils.Log(True, 'Error when upgrading confirmation %d: %s' % (confirmation.Oid(), error))

def ael_main(parameterDictionary):
    run_upgrade = parameterDictionary['run_upgrade']
    if (False == run_upgrade):
        Utils.Log(True, 'Confirmation protection and owner upgrade not performed')
    else:
        Utils.Log(True, 'Confirmation protection and owner upgrade commenced ...')
        UpgradeProtectionAndOwner()
        Utils.Log(True, 'Confirmation protection and owner upgrade completed ...')