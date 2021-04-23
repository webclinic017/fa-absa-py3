"""-------------------------------------------------------------------------------------------------------
MODULE
    FTradeTicket - alter XML by adding query results to output
    
    The module first tries to find the queries in FSource as a FASQLQuery
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""

import acm
import ael
import xml.etree.cElementTree as ET
import FLogger

logger = FLogger.FLogger( 'FAReporting' )
    
def getASQL(asqlname):
    """Fetch a ASQL query"""
    ext = acm.GetDefaultContext().GetExtension('FSource', 'FASQLQuery', asqlname)
    if ext:
        logger.LOG( "Using ASQL Extension (FSource): %s", asqlname )
        return ext.Value()
    else:
        asql = ael.TextObject.read('type="SQL Query" and name="%s"' % asqlname )
        if asql:
            logger.LOG( "Using ASQL: %s", asqlname )
            return asql.get_text()

    logger.LOG( "ASQL Query %s not found", asqlname )

    raise LookupError("ASQL Query %s not found" % asqlname)

def generate_query(asqlname, insid):
    """Build the Query and append macro values"""
    
    #mList=['@insid{ANY}','@insid{ANY}']
    #mValue=["'%s'"%(str(insid)),"'%s'"%(str(insid))]    

    mList=['@insid{ANY}']
    mValue=["'%s'"%(str(insid))]

    asql=getASQL(asqlname)

    asqlres=ael.asql(asql, 0, mList, mValue)
    try:
        columns, data = asqlres
    except:
        logger.WLOG( "ASQL query returned no rows, query will be empty" )
        columns = []
        data = [[]]
        
    querytag=ET.Element("query")
    querytag.set("name", asqlname)
    
    headtag = ET.Element("header")

    querytag.append(headtag)    
    lensum=0
    for col in columns:        
        lensum=+ lensum+len(col.strip())    
    for col in columns:
        column = ET.Element("column")        
        column.set("size", str(int(100*len(col.strip())/lensum)))
        column.text=col
        headtag.append(column)
        
    for datrow in data[0]:
        dattag = ET.Element("data")
        querytag.append(dattag)
        for dat in datrow:
            column = ET.Element("column")
            column.text=str(dat)
            dattag.append(column)
    return querytag

def parse_TTBS(reportObj, param, XMLreport):
    """ Invoked by FReportAPI.__additionalProcessing. 
        This function can be specified in the FWorksheetReport GUI, Processing tab, preprocess XML.
    """
    
    et=ET.ElementTree(ET.XML(XMLreport))

    for table in et.findall("//Table"):        
        queries=[]
        for column in table.findall("Columns/Column"):
            colnam=column.find("ColumnId").text
            if colnam.startswith('TTBS_'):
                queries.append(colnam)
        if queries:            
            for row in table.findall("Rows/Row"):                
                rowid=row.find("Label").text #tradenbr
                insid=row.find("Instrument/Name").text
                dqueries=ET.Element("Queries")
                for query in queries:
                    dquery=generate_query(query, insid)
                    if dquery:
                        dqueries.append(dquery) 
                row.append(dqueries)
    return ET.tostring(et.getroot(), 'ISO-8859-1')
