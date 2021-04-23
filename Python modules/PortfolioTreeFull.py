'''
Purpose                 : [Created to extract the entire portfolio tree structure],[Updated to only return portfolios belonging to specified Compound portfolios]
Department and Desk     : [PCG],[PCG]
Requester               : [Robert Lloyd],[Diana Rodrigues]
Developer               : [Willie van der Bank],[Willie van der Bank]
CR Number,Date          : [838685 24/11/2011],[287795 05/07/2012]
'''

import ael, SAGEN_IT_Functions, acm

def GetPortTreeForPort(parm, CompoundPortfolios):

    prfnbr = parm[0][0]
    sTree = parm[0][1]
    
    port = ael.Portfolio[prfnbr]
    sport = port.prfid
    s = 'member_prfnbr = ' + str(prfnbr)
    plnk = ael.PortfolioLink.select(s)
    prnts = []    
    
    top = 0
    for lnk in plnk:
        if lnk.owner_prfnbr:
        
            if CompoundPortfolios != ():
                valid = 'false'
                for CompoundPortfolio in CompoundPortfolios:
                    if (SAGEN_IT_Functions.get_Port_Struct_from_Port(lnk.owner_prfnbr, CompoundPortfolio) == 1) or (SAGEN_IT_Functions.get_Port_Struct_from_Port(ael.Portfolio[CompoundPortfolio], lnk.owner_prfnbr.prfid) == 1):
                        valid = 'true'
            else:
                valid = 'true'
                
            if valid == 'true':
                prnts.append( lnk.owner_prfnbr )
        else:
            top = 1
    
    if len(prnts) == 0:
        if sTree == '':
            return '--- Orphan ---'
        if not top:
            return '--- Orphan ---' + ',' + sport + ',' + sTree
        else:
            return sport + ',' + sTree
    else:
        sfx = ''        
        ret = []
        for prnt in prnts:
            if sTree <> '':
                sfx = ',' + sTree
            
            if len(prnts) == 1:
                ret = GetPortTreeForPort([[prnt.prfnbr, sport + sfx]], CompoundPortfolios)                
            else:
                ret.append(GetPortTreeForPort([[prnt.prfnbr, sport + sfx]], CompoundPortfolios))
    return ret

def Create_File(filename):
    outfile = open(filename, 'w')
    outfile.close()

def Portfolio():
    Ports = []
    for p in ael.Portfolio.select():
        Ports.append(p.prfid)
    Ports.sort()
    return Ports

ael_variables = [('Path', 'Path', 'string', ['f:\\'], 'f:\\', 1),
                 ('Filename', 'Filename', 'string', '', 'PortfolioTreeFull', 1),
                 ('CompoundPortfolios', 'CompoundPortfolios', 'string', Portfolio(), '', 0, 1, 'Leave blank to run for all portfolios.')]
                 
def ael_main(dict):

    filename = dict['Path'] + dict['Filename'] + '.csv'
    Create_File(filename)
    outfile = open(filename, 'a')
    ports = ael.Portfolio

    outfile.write('%s,%s,%s\n'%('Prfid', 'Prfnbr', 'Tree'))

    for port in ports:
        if not port.compound:
            if dict['CompoundPortfolios'] != ():
                valid = 'false'
                for CompoundPortfolio in dict['CompoundPortfolios']:
                    if SAGEN_IT_Functions.get_Port_Struct_from_Port(port, CompoundPortfolio) == 1:
                        valid = 'true'
            else:
                valid = 'true'
            if valid == 'true':
                sport = port.prfid
                parm = [[port.prfnbr, '']]
                ret = GetPortTreeForPort(parm, dict['CompoundPortfolios'])
                if type(ret) == type([]):
                    for itm in ret:
                        outfile.write('%s,%s,%s\n'%(sport, str(port.prfnbr), itm))
                else:
                    outfile.write('%s,%s,%s\n'%(sport, str(port.prfnbr), ret))

    outfile.close()
    ael.log('Wrote secondary output to:::' + filename)
