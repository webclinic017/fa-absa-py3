""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeAccounts.py"
import acm
import FOperationsUtils as Utils

ael_variables = [('run_upgrade', 'Remove EBA/TARGET2 as subnetwork from accounts with currency other than EUR', 'bool', [False, True], False)]

def UpgradeAccountSubnetwork():
    counter = 0
    accounts = acm.FAccount.Select('')
    for account in accounts:
        try:
            if account.SubNetworkChlItem():
                subnetwork = account.SubNetworkChlItem().Name()
                if subnetwork == 'EBA' or subnetwork == 'TARGET2':
                    if (account.Currency() and account.Currency().Name() != 'EUR') or not account.Currency():
                        account.SubNetworkChlItem(None)
                        account.Commit()
                        counter += 1
                        if (counter % 100 == 0):
                            Utils.Log(True, '%d accounts upgraded, please wait ...' % counter)
        except Exception as error:
            Utils.Log(True, 'Error when updating account %d: %s' % (account.Oid(), error))

def ael_main(parameterDictionary):
    run_upgrade = parameterDictionary['run_upgrade']
    if (False == run_upgrade):
        Utils.Log(True, 'Account upgrade not performed')
    else:
        Utils.Log(True, 'Account upgrade commenced ...')
        UpgradeAccountSubnetwork()
        Utils.Log(True, 'Account upgrade completed ...')