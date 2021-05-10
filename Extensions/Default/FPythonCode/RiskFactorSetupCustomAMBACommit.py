
import acm

class TempRiskFactorSetup( object ):
    def __init__( self, rfSetup ):
        self.m_instancesByCollName = {}
        
        tmpCollections = []
        tmpCollections.extend( rfSetup.RiskFactorCollections() )
            
        self.m_toCommit = rfSetup.Clone()
        self.m_toCommit.RiskFactorCollections().Clear()
        self.m_toCommit.RegisterInStorage()
        
        self.m_toCommit.Commit()
        
        for coll in tmpCollections:     
            tmpInstances = []
            tmpInstances.extend( coll.RiskFactorInstances() )
            
            cClone = coll.Clone()
            cClone.RiskFactorInstances().Clear()
            cClone.RegisterInStorage()
            self.m_toCommit.RiskFactorCollections().Add( cClone )
            
            instances = []
            for instance in tmpInstances:
                instanceClone = instance.Clone()
                instances.append( instanceClone )
                
            self.m_instancesByCollName[ coll.DisplayName() ] = instances

        self.m_toCommit.Commit()
        
    def Commit( self, batchSize ):
        try:
            self.m_toCommit.Commit()
            
            count = 0
            acm.BeginTransaction()
            
            for coll in self.m_toCommit.RiskFactorCollections():
                instances = self.m_instancesByCollName[ coll.DisplayName() ]

                for instance in instances:
                    count += 1
                    instance.RiskFactorCollection( coll )
                    instance.RegisterInStorage()
                        
                    if count % batchSize == 0:
                        self.m_toCommit.Commit()
                        acm.CommitTransaction()
                        acm.BeginTransaction()

            self.m_toCommit.Commit()
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            self.Delete()

    def Delete( self ):
        print("deleting")
        self.m_toCommit.Delete()
        
def Commit( riskFactorSetup, batchSize ):
    if riskFactorSetup.IsKindOf( acm.FRiskFactorSetup ):
        #copy data to temporary structure
        tmp = TempRiskFactorSetup( riskFactorSetup )

        #delete original clone to release data in datahandler
        riskFactorSetup.Delete()

        acm.PollAllDbEvents()

        #commit
        tmp.Commit( batchSize )
    else:
        raise Exception( "Only valid for objects of type FRiskFactorSetup" )
