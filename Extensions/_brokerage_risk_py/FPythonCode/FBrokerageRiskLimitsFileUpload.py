""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/FBrokerageRiskLimitsFileUpload.py"

"""--------------------------------------------------------------------------
MODULE
    Brokerage Risk

    (c) Copyright 2016 SunGard Front Arena AB. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm
from csv import DictReader
from xml.dom.minidom import parseString


template = '''
<MESSAGE>
    <TYPE>CONDITION</TYPE>
    <VERSION>1.0</VERSION>
    <TIME>2016-10-18 16:15:13</TIME>
    <SOURCE>LimitsUpload</SOURCE>
    <CONDITION>
        <MODEL_SEQNBR.NAME> __PLACE_HOLDER__ </MODEL_SEQNBR.NAME>
        <CLIENT_PTYNBR.PTYID> __PLACE_HOLDER__ </CLIENT_PTYNBR.PTYID>
        <DEPOT_PTYNBR.PTYID> __PLACE_HOLDER__ </DEPOT_PTYNBR.PTYID>
        <PORTFOLIO_PRFNBR.PRFID> __PLACE_HOLDER__ </PORTFOLIO_PRFNBR.PRFID>
        <VALUECURVE>
            <CALC_MODE>CALC_MODE_PER_AMOUNT</CALC_MODE>
            <CURVE_TYPE>CURVE_TYPE_FLAT</CURVE_TYPE>
            <CURRENCY_INSADDR.INSID> __PLACE_HOLDER__ </CURRENCY_INSADDR.INSID>
            <MIN_VALUE> __PLACE_HOLDER__ </MIN_VALUE>
        </VALUECURVE>
    </CONDITION>
</MESSAGE>
'''



def GetProperties(o):
    return [ m.CallVA( [ o ] ) for m in o.Class().MethodsDefined() if m.Class() == acm.FAccessGetMethod and not m.Domain().IsSubtype( acm.FPersistentSet ) ]

def CheckForDuplicates(cvm, o):
    po = GetProperties(o)
    for c in cvm.Conditions():
        if po == GetProperties(c):
            return c.Apply(o)       # Found entry with the same properties - must use the existing condition or there will be a conflict when we commit
    return o

def GetXmlElement(node, name):
    return node.getElementsByTagName( name )[0]

def GetXmlTextValue(node, name):
    return GetXmlElement(node, name).childNodes[0]

def SetXmlTextValue(node, name, value):
    child = GetXmlElement(node, name)
    if value:
        child.childNodes[0].nodeValue = value
    else:
        child.parentNode.removeChild(child)
    return child


FIXED_COLS = 4
DO_DELETE  = True

def Parse():
    f = open(r'limits.csv', 'r')
    reader = DictReader(f, delimiter=';')
    cndtns = reader.fieldnames[:FIXED_COLS]     # NOTE! Four "fixed" columns, followed by the limits - change here if file format changes
    limits = reader.fieldnames[FIXED_COLS:]     # NOTE! Four "fixed" columns, followed by the limits - change here if file format changes
    rows   = [ row for row in reader ]          # Will re-iterate over collection (once for each limit type), so might as well hold on to the rows
    delete = []
    #
    msg = parseString(template).childNodes[0]
    #
    for lmt in limits:
        cvm = acm.FConditionalValueModel[ lmt ]
        if cvm == None:
            print('Missing model %s in ADS' % lmt)
        else:
            cnd = list( cvm.Conditions() )
            for row in rows:
                if row[ lmt ] == "":
                    continue
                #
                mcp = msg.cloneNode( True )
                mdl = SetXmlTextValue( mcp, 'MODEL_SEQNBR.NAME', lmt )
                clt = SetXmlTextValue( mcp, 'CLIENT_PTYNBR.PTYID', row['Client'] )
                dpt = SetXmlTextValue( mcp, 'DEPOT_PTYNBR.PTYID', row['Depot'] )
                prf = SetXmlTextValue( mcp, 'PORTFOLIO_PRFNBR.PRFID', row['Portfolio'] )
                cur = SetXmlTextValue( mcp, 'CURRENCY_INSADDR.INSID', row['Currency'] )
                val = SetXmlTextValue( mcp, 'MIN_VALUE', row[ lmt ] )
                #
                xml = mcp.toxml()
                #
                o = acm.AMBAMessage.CreateObjectFromMessage( str( xml ) )       # Should decode properly if names would include non-ASCII characters
                o = CheckForDuplicates(cvm, o)                                  # Gets the newly created object, or an already existing one if there already is one with the same properties
                #
                try:
                    o.Commit()
                    print('Commited row: %s %s' % ( lmt, [ '%s: %s' % ( key, value ) for key, value in row.iteritems() if value != "" and key in cndtns ] ))
                except RuntimeError as err:
                    print('Commit failed for %s - %s' % ( row.values(), err ))
                #
                if o in cnd:
                    cnd.remove( o )     # Condition o found in file (and updated as needed) - remove from list of all FConditions for model so that list in the end only holds FConditions NOT found in the current upload file
            #
            # Keep track of any conditions in the ADS which are not found in the upload file
            delete += [ [ lmt, c ] for c in cnd ]
    #
    # Delete the conditions in the ADS which were not found in the upload file
    if DO_DELETE:
        for lmt, c in delete:
            print('Deleting condition no longer found in upload file: %s ( %s )' % ( c.Name(), lmt ))
            c.Delete()


if __name__ == '__main__':
    Parse()


