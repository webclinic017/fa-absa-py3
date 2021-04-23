""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboardUtil.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

import re
import xml.etree.ElementTree
import xml.parsers
import numbers

import acm
import ael


def tryCast(typ, val, default=None):

    castedVal = default
    try:
        castedVal = typ(val)
    except (TypeError, ValueError):
        pass
    except Exception as e:
        print(('tryCast(): {0}'.format(e)))
        raise e
    return castedVal


_ISO_DATE_MATCHER = re.compile('([0-9]{4})-([0-9]{2})-([0-9]{2})')
_DASH_DATE_MATCHER = re.compile('([0-9]{2,4})-([0-9]{1,2})-([0-9]{1,2})')
_SLASH_DATE_MATCHER = re.compile('([0-9]{1,2})/([0-9]{1,2}/([0-9]{2,4}))')


def containsNonIsoDate(strDateIterable):

    for strDate in strDateIterable:
        if not _ISO_DATE_MATCHER.match(strDate):
            return True
    return False


def isDate(strDate):

    if _DASH_DATE_MATCHER.match(strDate):
        return True
    if _SLASH_DATE_MATCHER.match(strDate):
        return True
    return False


def strDateTimeToStrDate(strDateTime):

    return strDateTime[:10].split(' ')[0]


def isResultDataOverLimit(resultData):

    return (resultData.threshold is not None and
            resultData.count > resultData.threshold)


def getLimitColumnName(acmFLimit):

    if not hasattr(acmFLimit, 'IsKindOf') or not acmFLimit.IsKindOf('FLimit'):
        raise ValueError('The given acmFLimit is not an acm FLimit.')
    acmLimitTarget = acmFLimit.LimitTarget()
    if not acmLimitTarget:
        return None
    xmlText = acmLimitTarget.Text()
    try:
        xmlRoot = xml.etree.ElementTree.fromstring(xmlText)
    except xml.etree.ElementTree.ParseError as e:
        print(('Unable to parse the text of acm.FLimitTarget[{0}] as an xml '
                'string.  {1}'.format(acmLimitTarget.Oid(), str(e))))
        return None
    elementList = xmlRoot.findall('./Element/FAssociation/associationValue'
            '/FCalculationSpecification/columnName/FSymbol/Text/string')
    if not elementList:
        return None
    columnName = str(elementList[0].text)
    return columnName


class AcmProxy(object):
    """
    Proxy for getting acm objects.  This class is used for isolating
    dependency to acm for the ease of unit-testing.
    """

    def getFPhysicalPortfolioByOid(self, portOid):

        if not isinstance(portOid, numbers.Integral):
            raise ValueError('The given oid should be an integer, but a {0} '
                    'type object is given.'.format(type(portOid)))
        return acm.FPhysicalPortfolio[portOid]

    def getFPhysicalPortfolioByName(self, portName):

        if not isinstance(portName, str):
            raise ValueError('The given name should be a string, but a {0} '
                    'type object is given.'.format(type(portName)))
        return acm.FPhysicalPortfolio[portName]

    def getFInstrumentByOid(self, insOid):

        if not isinstance(insOid, numbers.Integral):
            raise ValueError('The given oid should be an integer, but a {0} '
                    'type object is given.'.format(type(insOid)))
        return acm.FInstrument[insOid]

    def getFInstrumentByName(self, insName):

        if not isinstance(insName, str):
            raise ValueError('The given name should be an string, but a {0} '
                    'type object is given.'.format(type(insName)))
        return acm.FInstrument[insName]

    def getFPartyByOid(self, partyOid):

        if not isinstance(partyOid, numbers.Integral):
            raise ValueError('The given oid should be an integer, but a {0} '
                    'type object is given.'.format(type(partyOid)))
        return acm.FParty[partyOid]

    def getFPartyByName(self, partyName):

        if not isinstance(partyName, str):
            raise ValueError('The given name should be an string, but a {0} '
                    'type object is given.'.format(type(partyName)))
        return acm.FParty[partyName]

    def getFLimitByOid(self, limitOid):

        if not isinstance(limitOid, numbers.Integral):
            raise ValueError('The given oid should be an integer, but a {0} '
                    'type object is given.'.format(type(limitOid)))
        return acm.FLimit[limitOid]

    def getFLimitByName(self, limitName):

        if not isinstance(limitName, str):
            raise ValueError('The given name should be an string, but a {0} '
                    'type object is given.'.format(type(limitName)))
        return acm.FLimit[limitName]

    def getFEnumerationInsType(self):

        return acm.FEnumeration['enum(InsType)']


class DbSqlProxy(object):

    def execute(self, qryStmt):

        resultRows = ael.dbsql(qryStmt)[0]
        return resultRows
