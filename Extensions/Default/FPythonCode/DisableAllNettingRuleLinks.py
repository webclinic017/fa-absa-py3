
import acm
import FOperationsUtils


def DisableAllNettingRuleLinks(nettingRule):
    nettingRuleLinks = nettingRule.NettingRuleLinks()
    acm.BeginTransaction()
    
    try:
        for aNettingRuleLink in nettingRuleLinks:
            aNettingRuleLink.Enabled(False)
            aNettingRuleLink.Commit()
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        FOperationsUtils.LogAlways("Error while committing transaction: " + str(e))
    

def OpenDisableLinksDialog(nettingRule):
    func=acm.GetFunction('msgBox', 3)
    msgstr = "This operation will disable all netting rule links referencing"
    msgstr += " this nettingrule.\n'%s'.\n\n" % (nettingRule.Name())
    msgstr += "Do you want to continue?"
    selVal = func("Disable All Netting Rule Links", msgstr, 4)
    if(selVal == 6):
        DisableAllNettingRuleLinks(nettingRule)


def OpenDialog(eii):
    nettingRule = eii.ExtensionObject()[0]
    OpenDisableLinksDialog(nettingRule)
