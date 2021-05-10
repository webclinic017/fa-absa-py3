''' =====================================================================
    Dividend Extract

    This module exposes functions to extract dividend data from given
    streams as well as build up the index dividend data (converted to
    index points) of a given index.
    
    Note that this module is used in the dividend upload to ME.

    Eben Mare
    
    
    CR492813 - Eben Mare, Convert realised dividends to be outputed in cents (multiply by 100)
    ABITFA-3046: TCU, Type column for dividend estimates wanted for ME contribution
    PRMW787 - CHNG0003297785 : Use FPriceLinkDefinition instead of FPriceDefinition for getting RIC code for instruments
	
    ===================================================================== '''

import ael, acm
import re
from DateUtils import PDate

INDEX_HEADER = ("Stock", "Ex-Date", "Amount", "Pay-Date", "Type", "Comment", "FADivType")
SS_HEADER = ("Stock", "Ex-Date", "Amount", "Pay-Date", "Type", "Comment", "FADivType")
DATE_FORMAT = "%Y-%m-%d"
SPOTMARKET = 10
RICMappings = {}

def MapDivType(div):
    #Maps the dividend type to the BarCap Standard.
    descript = div.description.lower()
    if re.compile("f.*").match(descript):
        return "Final"
    elif re.compile("i.*").match(descript):
        return "Interim"
    else: return "Interim"

def MapFrontTickerToRIC(stock):
    if stock in RICMappings:
        return RICMappings[stock]
    else:
        price_link = acm.FPriceLinkDefinition.Select("instrument = %d and market = %d" % (ael.Instrument[stock].insaddr, SPOTMARKET) ) #Filter on the SPOT market
        
        if price_link:
            ReutersRIC = price_link[0].IdpCode()            
            if len(price_link) > 1:
                if price_link[1].PriceDistributor().Name() == "REUTERS_FEED_1":
                    ReutersRIC = price_link[1].IdpCode()
                    
            RICMappings[stock] = ReutersRIC
            return ReutersRIC and ReutersRIC

def IsValidForME(div):
    #Special divs aren't sent through to ME; Simulated, Final and Interim divs are.
    return re.compile("simulated|(f.*)|(i.*)").match(div.description.lower()) and True or False

def GetInstrActualDivs(insName):
    return list(ael.Dividend.select("insaddr = %d" % ael.Instrument[insName].insaddr))

def GetInstrDivEstimates(insName):
    stream = ael.DividendStream.select("insaddr = %d" % ael.Instrument[insName].insaddr)
    return stream and stream[0].estimates()

def GetInstrWeightInIndex(insName, indexName):
    insaddr = ael.Instrument[insName].insaddr
    for lnk in ael.Instrument[indexName].combination_links():
        if lnk.member_insaddr.insaddr == insaddr: return lnk.weight

def GetIndexConstituents(indexName):
    return [lnk.member_insaddr.insid for lnk in ael.Instrument[indexName].combination_links().members()]

def GetWeightedIndexDivsDetail(indexName):
    divs = []
    index_factor = ael.Instrument[indexName].index_factor
    for insid in GetIndexConstituents(indexName):
        intrWeight = GetInstrWeightInIndex(insid, indexName)
        estimates = GetInstrDivEstimates(insid)
        for est in estimates:
            if est.ex_div_day > ael.date_today() and IsValidForME(est):
                 divs.append( (MapFrontTickerToRIC(indexName), est.ex_div_day, est.dividend * intrWeight / index_factor, est.pay_day, MapDivType(est), MapFrontTickerToRIC(insid)) )

    return divs

def GetInstrActualDivsDetail(insName):
    return [ (MapFrontTickerToRIC(insName), PDate(d.ex_div_day).strftime(), d.dividend*100, PDate(d.pay_day).strftime(), MapDivType(d), "", "") \
                for d in GetInstrActualDivs(insName) if IsValidForME(d)]

def GetInstrDivsEstDetail(insName):
    return [ (MapFrontTickerToRIC(insName), PDate(e.ex_div_day).strftime(), e.dividend*100, PDate(e.pay_day).strftime(), MapDivType(e), "", GetDividentType(e) ) \
                for e in GetInstrDivEstimates(insName) if IsValidForME(e)]

def GetDividentType(div_est):
    val = div_est.dividend_type
    out_val="" 
    
    if  val == "Declared":
        out_val ="Declared"

    return out_val

def _formatDivs(divs):
    return "\n".join([",".join(map(str, div)) for div in divs])
    
def SaveDivsToFile(instrList, filename, divType):
    divs = []
    for insid in instrList:
        if divType == "ssdivs":
            #Add historical divs as well as estimates
            divs.extend(GetInstrActualDivsDetail(insid))
            divs.extend(GetInstrDivsEstDetail(insid))
        elif divType == "indexdivs":
            divs.extend(GetWeightedIndexDivsDetail(insid))
            
    #We will sort the list by stock name and then by ex-div day
    #note python has stable sort so we sort in reverse.
    divs.sort(lambda x, y: cmp(PDate(x[1], DATE_FORMAT), PDate(y[1], DATE_FORMAT))) #Sort by Ex-div Day
    divs.sort(lambda x, y: cmp(x[0], y[0])) #Sort by Stock Name

    #Get Header to use
    if divType == "ssdivs":
        header = SS_HEADER
    elif divType == "indexdivs":
        header = INDEX_HEADER

    file = open(filename, "w")
    try:
        file.write(",".join(header) + "\n" + _formatDivs(divs))
    finally:
        file.close()

def SaveSSDivsToFile(instrList, filename):
    SaveDivsToFile(instrList, filename, "ssdivs")

def SaveIndexDivsToFile(instrList, filename):
    SaveDivsToFile(instrList, filename, "indexdivs")

def test():
    SaveSSDivsToFile(["ZAR/ABL", "ZAR/ACL", "ZAR/GFI", "ZAR/MRP"], r"C:\temp\ssdivs.txt")
    SaveIndexDivsToFile(["ZAR/ALSI", "ZAR/SWIX"], r"C:\temp\indexdivs.txt")
