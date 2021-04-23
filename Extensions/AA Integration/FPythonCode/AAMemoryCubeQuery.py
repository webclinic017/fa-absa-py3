""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/aa_integration/./etc/AAMemoryCubeQuery.py"
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    AAMemoryCubeQuery

    (c) Copyright 2018 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""

import acm
import System
import AAMemoryCubeConnect
from AAAttributes import CALC_SNAPSHOT_MAP
from AAAttributes import FRTB_GROUPER_DIMENSION_MAP

def ConvertStringToFloat(value):

    if isinstance(value, System.DBNull):
        return None
    try:
        ret = float(value.encode('utf-8'))
        return ret
    except Exception as e:
        return None

def ExtractResults(mdxResults, allResults = False):

    #print mdxResults.Rows.Count, mdxResults.Columns.Count
    resultDict = acm.FDictionary()
    for row in mdxResults.Rows:
        rowDict = acm.FDictionary()
        for column in mdxResults.Columns:
            try:
                if 'MEMBER_CAPTION' in column.ColumnName:
                    if isinstance(row[column], System.DBNull):
                        if not allResults:
                            break
                        else:
                            resultDict['Total' + ''] = rowDict
                    else:
                        rowValue = row[column].encode('ascii', 'ignore')
                        if 'Combined' not in rowValue and not allResults:
                            break
                        rowName = column.ColumnName.encode('ascii', 'ignore').split('.')[-3][1:-1]
                        resultDict[rowName + rowValue] = rowDict
                else:                    
                    measureName = column.ColumnName.encode('ascii', 'ignore').split('.')[1][1:-1]
                    rowDict[measureName] = ConvertStringToFloat(row[column])
                
            except Exception as e:
                print('Extract Results Exception', str(e))

    return resultDict


def printResult(resultDict):
    for key in resultDict.Keys():
        print('******************************************')
        print(key)
        for k in resultDict.At(key).Keys():
            try:
                print(k, '---', resultDict.At(key).At(k))
            except Exception as e:
                print('Print Results Exception', str(e))


def topNodePortfolios(rowObj):
    return ['[Trade].[Portfolio].[{0}]'.format(p.Name()) for p in rowObj.PhysicalPortfolios()]


def buildMdxQueryMeasures(rowObj, attributesToDimension, snapShot):
    
    if rowObj.IsKindOf(acm.FPortfolioInstrumentAndTrades):
        dimensions = ",".join(topNodePortfolios(rowObj))
    else:
        if rowObj.IsKindOf(acm.FSingleInstrumentAndTrades):
            dimensions = '{{ [Trade].[{0}].[{1}] }}'.format(attributesToDimension[acm.FSymbol('Trade.Instrument')], rowObj.Instrument().Name())
        else:
            dimensions = ''

        groupers, topNode = groupersAndTopNodeFromRows(rowObj)
        isGroupedByPort = False
        for grouper in groupers:
            dimensionValue = rowObj.Grouping().GroupingValueAtGrouper(grouper).Name()
            dimensionName = attributesToDimension[grouper.MethodCollection()[0]]
            if rowObj.IsKindOf(acm.FSingleInstrumentAndTrades) and dimensionName == attributesToDimension[acm.FSymbol('Trade.Instrument')]:
                continue
            if dimensionName == attributesToDimension[acm.FSymbol('Trade.Portfolio')]:
                isGroupedByPort = True
            dimension = '{{ [Trade].[{0}].[{1}] }}'.format(dimensionName, dimensionValue)
            if not dimensions:
                dimensions = dimension
            else:
                dimensions = '{0} * {{{1}}}'.format(dimension, dimensions)
        
        if not isGroupedByPort:
            topNodePorts = topNodePortfolios(topNode)
            dimensions = ",".join(['{0} * {{{1}}}'.format(port, dimensions) for port in topNodePorts])

    snapShotdimension = '{{ [Value Date].[Snapshot].[{0}] }}'.format(snapShot)
    dimensions = '{0} * {{{1}}}'.format(snapShotdimension, dimensions)
    mdxQuery = 'WITH MEMBER [Trade].[{0}].[Combined] as aggregate({{{1}}}) SELECT {{ [Measures].MEMBERS }} ON COLUMNS, [Trade].[Portfolio].AllMembers ON ROWS FROM [Default]'.format(attributesToDimension[acm.FSymbol('Trade.Portfolio')], dimensions)
    print(mdxQuery)
    return mdxQuery


def groupersAndTopNodeFromRows(obj):

    if obj.IsKindOf(acm.FSingleInstrumentAndTrades):
        parent = obj.Parent()
    else:
        parent = obj
    groupers = []
    TopNode = None
    while parent:
        if (not parent.GrouperOnLevel().IsKindOf(acm.FChainedGrouper) and
                not parent.GrouperOnLevel().IsKindOf(acm.FDefaultGrouper)):
            grouping = parent.Grouping()            
            groupers.insert(0, grouping.Grouper())
        else:
            TopNode = parent
        parent = parent.Parent()
    return groupers, TopNode

def measureValues(obj, calType):
    snapshotMdx = buildMdxQueryMeasures(obj, FRTB_GROUPER_DIMENSION_MAP, CALC_SNAPSHOT_MAP[calType])
    connection = AAMemoryCubeConnect.CubeConnection()
    mdxResults = connection.ExecuteReader(snapshotMdx)
    resultDict = ExtractResults(mdxResults)
    return resultDict

def artiQColumns(obj, resultDict, columnName):
    result = resultDict['PortfolioCombined'][columnName]
    if not result:
        return 0.0
    return result
