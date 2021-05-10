
# ####################################################################
# Script for upgrading FX Target Redemption Forwards from a Prime
# version earlier than 18.3.
#
# In 18.3 the Deal Package Definition Name for FX Target Redemption
# Forwards changed from SP_TargetRedemptionForwards to 
# SP_FxTargetRedemptionForwards. In order for the FX TARFS entered
# in an earlier version to work in Prime 18.3 or later, all FX TARF
# instrument packages need to have the attribute DefinitionName updated.
#
# Usage:
#   Call the method UpgradeDefinitionName in this script.
#
# Parameters:
#   do_commit: Changes will only be committed to teh database if this
#              parameter is set to True.
# ####################################################################


import acm

def UpgradeDefinitionName(doCommit = False):

    acm.LogAll("")
    acm.LogAll("==================================================")
    acm.LogAll("UPDATING DEAL PACKAGE DEFINITION NAME FOR FX TARFS")
    acm.LogAll("==================================================")

    updateCount = 0
    updateSucceded = 0
    updateFailed = 0

    allIps = list(acm.FInstrumentPackage.Select("definitionName='SP_TargetRedemptionForward'"))
    for ip in allIps:
        updateCount += 1
        acm.LogAll("")
        acm.LogAll("Updating %s" % ip.Name())
        ipClone = ip.StorageImage()
        ipClone.DefinitionName('SP_FxTargetRedemptionForward')
        if doCommit:
            try:
                ipClone.Commit()
            except:
                pass
            if ip.DefinitionName() == 'SP_FxTargetRedemptionForward':
                updateSucceded += 1
                acm.LogAll("Successfully updated instrument package %s" % ip.Name())
            else:
                updateFailed += 1
                acm.LogAll('Failed to update instrument package %s' % ip.Name())

    acm.LogAll("")
    acm.LogAll("=======================================================")
    acm.LogAll("DONE UPDATING DEAL PACKAGE DEFINITION NAME FOR FX TARFS")
    acm.LogAll("    Statistics:")
    acm.LogAll("    Packages found: %i" % updateCount)
    acm.LogAll("    Packages updated: %i" % updateSucceded)
    acm.LogAll("    Packages failed: %i" % updateFailed)
    acm.LogAll("=======================================================")
