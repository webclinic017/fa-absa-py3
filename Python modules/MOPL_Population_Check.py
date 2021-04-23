'''
Purpose              	: Report on all portfolios whose add_info - Mopl_Population is not set to Yes. Excludes Compound portfolios.
Department and Desk	: PCG
Requester            	: Dirk Strauss
Developer            	: Bhavnisha Sarawan
CR Number            	: C548413
'''


import ael, acm

# Function to use multiple portfolios
def Ports():
    Ports=[]
    for t in ael.Portfolio:
        Ports.append(t.prfid)
    Ports.sort()
    return Ports
 
# Main variables   
ael_variables = [ ['Portfolio', 'Portfolio', 'string', acm.FPhysicalPortfolio.Select(''), None, 0, 1],
                  ['Path', 'Path', 'string', None, '', 1],
                  ['Filename', 'Filename', 'string', None, '', 0]  ]

# List to store the portfolio tree
portTree = []



#Recursive function to check if a portfolio is in a specified portfolio in the portfolio tree. Portfolio tree is added to the list.    
def get_Port_Struct(portLinkLst,checkPort,match=0):
    if match != 1:
        for portLink in portLinkLst:
            if portLink.member_prfnbr.prfid != checkPort:
                if portLink.owner_prfnbr:
                    if portLink.owner_prfnbr.prfid == checkPort:
                        portTree.append(portLink.owner_prfnbr.prfid)
                        match = 1
                    else:
                        portTree.append(portLink.owner_prfnbr.prfid)
                        match = get_Port_Struct(ael.PortfolioLink.select('member_prfnbr=%i' %portLink.owner_prfnbr.prfnbr), checkPort, match)
            else:
                match = 1
    return match

#Function that calls the recursive portfolio tree climber function
def get_Port_Struct_from_Port(port, checkPort):
    portTree.append(port.Name())
    p = ael.Portfolio[port.Name()].prfnbr
    try:   
        portLink = ael.PortfolioLink.select('member_prfnbr=%i' %p)
        match = get_Port_Struct(portLink, checkPort)
    except:
        match = 0   
    return match

#Main Function to select non MoPL_Population portfolios and match them to user selected portfolios. Returns the portfolio tree.
def ael_main(parameter, *rest):

# Output setup
    inputPort = parameter['Portfolio']
    outputPath = parameter['Path']
    outputName = parameter['Filename']
    fileName = outputPath + outputName
    header = 'Portfolio Tree, Portfolio\n'

    outfile =  open(fileName, 'w')
    outfile.write(header)

# Portfolio selection and returns the portfolio tree    
    for pname in inputPort:
        pn = acm.FPhysicalPortfolio['pname']
        portlist = acm.FPhysicalPortfolio.Select(pn)
        for p in portlist:
            if not p.Portfolio().AdditionalInfo().MoPL_Population() and not p.Portfolio().Compound():
                if get_Port_Struct_from_Port(p, pname.strip()) == 1:
                    portTree.reverse()
                    output = ",".join(portTree).replace(",", "  >>  ")
                    outfile.write('%s,%s\n' % (output, p.Name()))
                    #print output
                del portTree[:]
                portTree[:] = []

    outfile.close
    ael.log('Wrote secondary output to:::' + fileName)


