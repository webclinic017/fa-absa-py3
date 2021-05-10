#Department and Desk:    PCG
#Requester:              Sipho Ndlalane
#Developer:              Douglas Finkel
#CR Number:              C000000835961
#Description:            The purpose of this AEL is to create a list of Valid Portfolio and check against that list

import ael, string, acm

portfolioTree = acm.FList()
MR_Portfolio = acm.FList()

def PortfolioSearch():
    queryFolderList = acm.FTradeSelection['CAP_MARKET_Portfolio']
    for i in queryFolderList.FilterCondition():
        if i[4] not in MR_Portfolio:
            MR_Portfolio.Add(i[4])

def get_port_struc(port, portfolioTree):
    portfolioTree.Add(port.Name())
    for item in port.MemberLinks():
        ownerPort = item.OwnerPortfolio()
        if ownerPort:
            get_port_struc(ownerPort, portfolioTree)

    
def PortfolioStructure(portfolio):
    ValidPortfolio = 0
    portfolioTree = acm.FList()

    port = acm.FPhysicalPortfolio[portfolio.prfid]
    get_port_struc(port, portfolioTree)
    for Portfolio in MR_Portfolio:

        if str(Portfolio) in portfolioTree:
            return 1
    
def ValidPortfolio(portfolio, *rest):
    if len(MR_Portfolio) == 0:
        PortfolioSearch()
    if PortfolioStructure(portfolio) == 1:
        return 'yes'
    else:
        return 'no'
