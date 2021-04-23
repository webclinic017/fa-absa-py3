"""
This module contains functionality  to Automate specific middle office

queries (monthly) in order to operationalise Basel 3 reporting requirement

in relation to direct and indirect regulated financial entity equity holdings.

"""

import ael
import FRunScriptGUI
import os
import csv
import time

tb = '\t'
nl = '\n'
outputSelection = FRunScriptGUI.DirectorySelection()

lookin = []
exceptions = []
stocks = [
            'ZAR/ABL',
			'ZAR/ADW',
			'ZAR/ASA',
			'ZAR/BFS',
			'ZAR/BK1P',
			'ZAR/BRT',
			'ZAR/CDZ',
			'ZAR/CLI',
			'ZAR/CML',
			'ZAR/CND',
			'ZAR/CPI',
			'ZAR/DSY',
			'ZAR/EFG',
			'ZAR/FCPD',
			'ZAR/FGL',
			'ZAR/FSR',
			'ZAR/GAM',
			'ZAR/IDQ',
			'ZAR/INL',
			'ZAR/INP',
			'ZAR/JDH',
			'ZAR/JSE',
			'ZAR/LBH',
			'ZAR/MMI',
			'ZAR/NED',
			'ZAR/NFEMOM',
			'ZAR/NFSWIX',
			'ZAR/OAS',
			'ZAR/OML',
			'ZAR/PCT',
			'ZAR/PGR',
			'ZAR/PPE',
			'ZAR/PREFEX',
			'ZAR/PSG',
			'ZAR/RACP',
			'ZAR/RMBMID',
			'ZAR/RMH',
			'ZAR/RMI',
			'ZAR/SBK',
			'ZAR/SBV',
			'ZAR/SFN',
			'ZAR/SKJ',
			'ZAR/SLM',
			'ZAR/SNT',
			'ZAR/STA',
			'ZAR/STX40',
			'ZAR/STXFIN',
			'ZAR/STXSWX',
			'ZAR/TCP',
			'ZAR/TTO',
			'ZAR/VUN',
			'ZAR/ZSA'
          ]

headers = [
            'Trade',
            'Instrument',
            'Underlying',
            'Type',
            'Expiry',
            'Call Option',
            'Strike',
            'Quantity',
            'Counterparty',
            'OTC',
            'Contract Size',
            'Quote Type',
            'Used Price',
            'Present Value',
            'Settlement Type',
			'Delta',
            'Portfolio',
			'Portfolio Owner'            
           ]
          
def get_kids(parent, exceptions):
    kids = []
    links = ael.PortfolioLink.select('owner_prfnbr = %s' % parent.prfnbr)
    for link in links:
        if not link.member_prfnbr.compound:
            kids.append(link.member_prfnbr.prfid)
        else:
            if link.member_prfnbr.prfid not in exceptions:
                p = link.member_prfnbr
                kids.extend(get_kids(p, exceptions))
    return kids
    
def get_parents(child):
    parents = []
    directs = ael.Instrument.select('und_insaddr = ' + str(child.insaddr))
    if len(directs) > 0:
        for direct in directs:
            if direct.exp_day > ael.date_today():
                parents.append(direct.insid)
    links = ael.CombinationLink.select('member_insaddr = %s' % child.insaddr)
    if len(links) > 0:
        for link in links:
            if link.owner_insaddr.exp_day > ael.date_today() or link.owner_insaddr.exp_day == None:
                parents.append(link.owner_insaddr.insid)
    return parents
    
def get_ai(entity, ai):
    for addinf in entity.additional_infos():
        if addinf.addinf_specnbr.field_name == ai:
            return addinf.value
    return ''
    
def gen_head(headers, delimiter, breaker):
    head = ''
    for header in headers:
        head += str(header) + delimiter
    head = head[:(len(head) - len(delimiter))] + breaker
    return head

def portfolioFilter():
    Ports = []
    for p in ael.Portfolio.select():
        Ports.append(p.prfid)
    Ports.sort()
    return Ports
    
def addStock(stock):
    slash = '/'
    #check if the stock is in a valid format
    if stock.find(slash)> -1 and stock.count(slash)== 1:
        s = stock.upper()
        if s not in stocks:
            stocks.append(s)
    else:
         raise Exception("The stock entered is not in the correct format.")

def getFilepath(directory):
    return os.path.join(directory, 'ABCAP_FA_QUALIFYING_CAPITAL_%s.csv' % time.strftime('%Y%m%d%H%M%S'))

def writeFile(filepath, prfset, insset):
    with open(filepath, 'w') as csvFile:
        writer = csv.writer(csvFile, lineterminator = nl)
        writer.writerow(headers)
        for prf in prfset:
            trades = ael.Portfolio[prf].trades()
            if len(trades) > 0:
                for trd in trades:
                    if (trd.insaddr.insid in stocks or trd.insaddr.insid in insset) and (trd.status not in ('Void', 'Simulated')):
                            if trd.insaddr.und_insaddr:
                                under = trd.insaddr.und_insaddr.insid
                            else:       
                                under = 'None'
                            writer.writerow([
                                str(trd.trdnbr),
                                trd.insaddr.insid,
                                under,
                                trd.insaddr.instype,
                                str(trd.insaddr.exp_day),
                                str(trd.insaddr.call_option),
                                str(trd.insaddr.strike_price),
                                str(trd.quantity),
                                trd.counterparty_ptynbr.ptyid,
                                str(trd.insaddr.otc),
                                str(trd.insaddr.contr_size),    
                                trd.insaddr.quote_type,
                                str(trd.insaddr.mtm_price()),
                                str(trd.present_value()),
                                str(trd.insaddr.settlement),
								str(trd.insaddr.delta_explicit()),
                                str(trd.prfnbr.prfid),
                                str(trd.prfnbr.owner_ptynbr.ptyid)
                            ])
                

ael_variables = [('stock', 'Add Another Stock:', 'string', None, '', 0, 01, 'Leave blank to run default stocks'),
                ('portfolio', 'Portfolio:', 'string', portfolioFilter(), 'SECONDARY MARKETS TRADING', 0, 1, 'Add more portfolio'),
                ('exceptions', 'Exclude Portfolio:', 'string', portfolioFilter(), '', 0, 1, 'Add more portfolio to exclude'),
                ('output', 'Output Directory', outputSelection, None, outputSelection, 1, 1, 'Directory where the file will be created.', None, 1)
                ]
    
def ael_main(dict):  
    prfset = []
    insset = []
    insset2 = []
    
    for stock in dict['stock']:
        addStock(stock)  
 
    for port in dict['portfolio']:
        lookin.append(port)
    
    for port in dict['exceptions']:
        exceptions.append(port)

    for stock in stocks:
        if ael.Instrument[stock]:
            insset.extend(get_parents(ael.Instrument[stock]))
        insset = list(set(insset))        

        for ins in insset:
            insset2.extend(get_parents(ael.Instrument[ins]))
        insset2 = list(set(insset2))
        insset = insset + insset2

        for prf in lookin:
            prfset.extend(get_kids(ael.Portfolio[prf], exceptions))
        prfset = list(set(prfset)) 

        filepath = getFilepath(dict['output'].SelectedDirectory().Text())

    writeFile(filepath, prfset, insset)
    print 'Wrote secondary output to:::' + filepath
    
