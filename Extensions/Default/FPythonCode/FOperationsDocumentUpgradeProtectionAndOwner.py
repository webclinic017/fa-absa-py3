""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/upgrade/FOperationsDocumentUpgradeProtectionAndOwner.py"
import acm
import FOperationsUtils as Utils

ael_variables = [('run_upgrade', 'Upgrade OperationsDocuments to inherit Protection And Owner from Settlement/Confirmation', 'bool', [False, True], False)]

def UpgradeProtectionAndOwner():
    counter = 0
    opdocs = acm.FOperationsDocument.Select('')

    for opdoc in opdocs:
        try:
            inheritFrom = opdoc.Settlement()
            if not inheritFrom:
                inheritFrom = opdoc.Confirmation()

            if inheritFrom and inheritFrom.ArchiveStatus():
                continue

            if (inheritFrom and (opdoc.Owner() != inheritFrom.Owner() or opdoc.Protection() != inheritFrom.Protection())):
                opdoc.Owner(inheritFrom.Owner())
                opdoc.Protection(inheritFrom.Protection())
                opdoc.Commit()
                counter += 1
                if (counter % 100 == 0):
                    Utils.Log(True, '%d operationdocuments updated, please wait ...' % counter)

            if counter:
                return

        except Exception as error:
            Utils.Log(True, 'Error when upgrading OperationsDocument %d: %s' % (opdoc.Oid(), error))
    Utils.Log(True, 'Totaly %d operationdocuments updated' % counter)

def ael_main(parameterDictionary):
    run_upgrade = parameterDictionary['run_upgrade']
    if (False == run_upgrade):
        Utils.Log(True, 'OperationsDocument protection and owner upgrade not performed')
    else:
        Utils.Log(True, 'OperationsDocument protection and owner upgrade commenced ...')
        UpgradeProtectionAndOwner()
        Utils.Log(True, 'OperationsDocument protection and owner upgrade completed ...')
