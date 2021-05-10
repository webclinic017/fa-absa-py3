""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeSettleInstructionToUseQueryFilter.py"
import acm
import ael
import FOperationsUtils as Utils

ael_variables = []

class SettleInstructionQueryFilterUpgradeHandler(object):

    def RunUpgradingScript(self):
        Utils.LogAlways("Starting upgrade of SettleInstructions for Settlement Solution")
        if self.QueryFilterColumnExist():
            try:
                parties = acm.FParty.Select("")
                messages = list()
                for party in parties:
                    self.CreateQueryFiltersForSettleInstructions(party, messages)
                self.PrintMessages(messages)
                Utils.LogAlways("\nFinished upgrading SettleInstructions for Settlement Solution")
            except Exception as e:
                Utils.LogAlways("Error: %s" % str(e))
        else:
            Utils.LogAlways("Upgrade cancelled.")
            Utils.LogAlways("This ADS is using an ADM older than 2017.1 and cannot be upgraded.")

    def PrintMessages(self, messages):
        if len(messages) > 0:
            Utils.LogAlways("\n\n")
            for message in messages:
                Utils.LogAlways(message)
                
    def QueryFilterColumnExist(self):
        q = ael.ServerData.select()[0]
        admVersion = q.data_model_nbr
        
        if admVersion < 42800586:
            hasQueryFilterColumn = False
        else:
            hasQueryFilterColumn = True
            
        return hasQueryFilterColumn


    def CreateQueryFiltersForSettleInstructions(self, party, messages):
        Utils.LogAlways("\nProcessing settle instructions for party %s." % party.Name())
        settleInstructions = party.SettleInstructions()
        if settleInstructions.Size() > 0:
            currentSettleInstruction = None
            storedQueries = []
            try:
                acm.BeginTransaction()
                for settleInstruction in settleInstructions:
                    currentSettleInstruction = settleInstruction
                    if settleInstruction.Query():
                        Utils.LogAlways("QueryFilter added. Committing settle instruction '%s'." % settleInstruction.Name())
                        storedQuery = settleInstruction.Query()
                        settleInstruction.QueryFilter(storedQuery.Query())
                        storedQueries.append(storedQuery)
                        settleInstruction.Commit()
                        
                acm.CommitTransaction() 
            except Exception as e:
                acm.AbortTransaction()
                storedQueries = []
                Utils.LogAlways("An error occurred while processing settle instruction '%s': %s." % (currentSettleInstruction.Name(), str(e)))
                Utils.LogAlways("Aborting processing of settle instructions for '%s'. No changes will be saved." % party.Name())
                

            for query in storedQueries:
                try:
                    Utils.LogAlways("Removing referenced TextObject query'%s'." % query.Name())
                    query.Delete()
                except Exception as e:
                    Utils.LogAlways("Could not remove TextObject query'%s' : %s." % (query.Name(), str(e)))
                    Utils.LogAlways("If reference exist, it will be deleted later in this process.")
            
#-------------------------------------------------------------------------------

def ael_main(dictionary):
    upgradeHandler = SettleInstructionQueryFilterUpgradeHandler()
    upgradeHandler.RunUpgradingScript()
