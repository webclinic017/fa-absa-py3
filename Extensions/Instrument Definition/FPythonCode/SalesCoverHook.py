
import acm
from SalesCoverHookUtils import IsFixedDeposit, PostAllocateRisk_Deposit

def PreAllocateRisk(parameters):
    '''
    After parameters are set in the trade capture screen, before risk allocation is run.
    Return: args to pass into PostAllocateRisk
    '''
    pass
    
def PostAllocateRisk(artifacts, args):
    '''
    After risk allocation is run, before artifacts (trades, instruments, business events etc) are committed.
    '''
    if artifacts.ArtifactsToBeCommitted().IsEmpty():
        return
        
    if IsFixedDeposit(artifacts):
        PostAllocateRisk_Deposit(artifacts, args)
    
def InitializeParameters(parameters):
    '''
    After default initialization of sales cover paramters from persisted trade, before presentation in the 
    trade capture screen.
    '''
    pass
    
