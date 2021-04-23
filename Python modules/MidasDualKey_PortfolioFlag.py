#Purpose:                Midas Dual Key project
#Department and Desk:    PCG
#Requester:              Nick Bance
#Developer:              Kim Madeley
#CR Number:              627299

import ael, string, acm

def get_port_struc(port, portfolioTree):
    portfolioTree.Add(port.Name())
    for item in port.MemberLinks():
        ownerPort = item.OwnerPortfolio()
        if ownerPort:
            get_port_struc(ownerPort, portfolioTree)
            
def port_tree(temp,portname,*rest):
    port = acm.FPhysicalPortfolio[portname]
    portfolioTree = acm.FList()
    get_port_struc(port, portfolioTree)
    if "ABSA BANK LTD" in portfolioTree:
        return  '1'
    else:
        return  '0'    

def find_root_level(temp,portname,*rest):
    port = acm.FPhysicalPortfolio[portname]
    portfolioTree = acm.FList()
    get_port_struc(port, portfolioTree)
    if "ABSA BANK LTD" in portfolioTree:
        return  '0'
    elif "CLIENT REPORTING" in portfolioTree:
        return '1'
    else:
        return  '9'    
        
def PortfolioClientNbr(temp,portname,*rest):
   
    root_level = find_root_level(1, portname)
    
    if root_level == '1':
    
        port = acm.FPhysicalPortfolio[portname]
        portAddInfo = port.add_info('PSClientCallAcc')
        
        if portAddInfo:
            t = acm.FInstrument[portAddInfo].Trades()[0]
            return str(t.Counterparty().Oid())
        else:
            return '0'
    else:
        return '0'    
 
print PortfolioClientNbr(1, 'CLIENT REPORTING')        
            


