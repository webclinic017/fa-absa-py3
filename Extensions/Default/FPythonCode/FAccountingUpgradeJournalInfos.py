""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/upgrade/FAccountingUpgradeJournalInfos.py"
import acm


def UpgradeJournalInformations():
    Utils.LogAlways("Upgrading journal informations with treatment reference. Please wait...")
    journalInformations = acm.FJournalInformation.Select("")
    updatedJIs = 0
    for aJournalInformation in journalInformations:

        try:
            treatment = None
            if(aJournalInformation.AccountingInstruction() and not aJournalInformation.Treatment()):
                treatments = aJournalInformation.Book().Treatments()
                trade = aJournalInformation.Trade()
                accountingInstruction = aJournalInformation.AccountingInstruction()

                for aTreatment in treatments:
                    if(aTreatment.AccountingInstructions().Includes(accountingInstruction)):
                        if(IsMatchingTreatment(trade, aTreatment)):
                            treatment = aTreatment
                            break

            if treatment:
                aJournalInformation.Treatment(treatment)
                aJournalInformation.Commit()
                updatedJIs += 1
                if not updatedJIs % 1000:
                    Utils.LogAlways("Journal informations are being updated. Please wait...")

        except Exception as errorMessage:
            Utils.LogAlways("Warning: Failed to upgrade the journal information " + str(aJournalInformation.Oid()) + " : " + str(errorMessage))
    Utils.LogAlways("Done")


def IsMatchingTreatment(trade, aTreatment):

    matchingTreatment = False
    if(trade and aTreatment.TreatmentMappings().Size()):
        for aMapping in aTreatment.TreatmentMappings():
            if(aMapping.Query()):
                if(aMapping.Query().Query().IsSatisfiedBy(trade)):
                    matchingTreatment = True
            else:
                matchingTreatment = True
    return matchingTreatment


"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    import acm
    import FOperationsUtils as Utils

    ael_variables = []

    def ael_main(dict):
        pr = '<< Accounting Upgrade - %s >>' % (__file__)
        Utils.Log(True, pr)
        UpgradeJournalInformations()

except Exception as e:
    if 'ael_variables' in globals():
        del globals()['ael_variables']
    if 'ael_main' in globals():
        del globals()['ael_main']
    Utils.Log(True, 'Could not run FAccountingUpgradeJournals due to ')
    Utils.Log(True, str(e))
