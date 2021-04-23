from __future__ import print_function
import acm
import FExportCalculatedValuesMain, ProfitAndLossExplainGreekWriter

validRiskFactorColumnIDs = [
    'Portfolio Profit And Loss Explain Credit Per Risk Factor',
    'Portfolio Profit And Loss Explain Equity Per Risk Factor',
    'Portfolio Profit And Loss Explain FX Per Risk Factor',
    'Portfolio Profit And Loss Explain Interest Rate Per Risk Factor',
    'Portfolio Profit And Loss Explain Volatility Per Risk Factor',
    'Portfolio Profit And Loss Explain Credit/FX XGamma',
    'Portfolio Profit And Loss Explain Credit/IR XGamma',
    'Portfolio Profit And Loss Explain IR/FX XGamma',
]

validTimeColumnID = 'Portfolio Profit And Loss Explain Time'
trueFalse = ['False', 'True']

def distributedModeCB(index, fieldValues):
    for idx, var in enumerate(ael_variables):
        if var[0] == 'Calculation Environment':
            if trueFalse.index( fieldValues[index] ):
                var[9] = True
            else:
                var[9] = False
                fieldValues[idx] = None
    return fieldValues
        
def ael_var(displayName, acmClass, constraint, toolTip):
    return [displayName, displayName, acmClass.Name(), acmClass.Select(constraint), None, 0, 1, toolTip]

ael_variables = [
    ['Distributed Mode', 'Distributed Mode', 'string', trueFalse, 'False', 0, 0, 'Enable distributed calculations', distributedModeCB],
    ['Calculation Environment', 'Calculation Environment', acm.FStoredCalculationEnvironment, acm.FStoredCalculationEnvironment.Select(""), None, 0, 0, 'Enable distributed calculations', None, False],
    ael_var('Columns', acm.FStoredColumnCreator, '', 'The stored columns that the values will be calculated for'),
    ael_var('Portfolios', acm.FPhysicalPortfolio, '', 'The physical portfolios. Values will be calculated on portfolio level and on instrument level'),
    ael_var('Trade Filters', acm.FTradeSelection, '', 'The trade filters. Values will be calculated on portfolio level and on instrument level'),
    ael_var('Trade Queries', acm.FStoredASQLQuery, 'user=0 and subType="FTrade"', 'The stored ASQL queries, queries shown are shared and of type trade. Values will be calculated on portfolio level and on instrument level'),
]

def ael_main(ael_output):
    writer = ProfitAndLossExplainGreekWriter.ProfitAndLossExplainGreekWriter(validRiskFactorColumnIDs, validTimeColumnID)
    
    grouper = acm.Risk().CreateChainedGrouperDefinition(acm.FTrade, 'Portfolio', True, 'Instrument', True, [])
    columns = []
    for column in ael_output['Columns']:
        cc = column.ColumnCreator()
        columnID = str(cc.OriginalColumnId())
        if (columnID in validRiskFactorColumnIDs) or (validTimeColumnID == columnID):
            columnConfiguration = FExportCalculatedValuesMain.createColumnConfigurationFromStoredColumnCreator(
                                    storedColumnCreator=column)
            columns.append(columnConfiguration)
        else:
            raise Exception('Column: ' + column.Name() + ' is currently not supported. This script only works with Profit and Loss Explain in this release.')

    portfolioNames = [i.Name() for i in ael_output['Portfolios']]
    tradeFilterNames = [i.Name() for i in ael_output['Trade Filters']]
    storedASQLQueryNames = [i.Name() for i in ael_output['Trade Queries']]
    distributedMode = trueFalse.index( ael_output['Distributed Mode'] )
    calcEnvName = ael_output['Calculation Environment']
    FExportCalculatedValuesMain.main(portfolioNames, tradeFilterNames, storedASQLQueryNames, columns, grouper, [writer], distributedMode, calcEnvName)

    filePath = acm.GetDefaultValueFromName(acm.GetDefaultContext(), 'FObject', 'profitAndLossExplainStoredGreekFilePath')
    filePath = filePath.replace('\n', '')
    fileName = 'ProfitAndLossExplainStoredGreeks' + '_' + acm.Time.DateToday() + '.dat'
    toFile = open(filePath + fileName, 'w')
    toFile.writelines(writer.output)
    toFile.close()
    print ('Wrote results to file: ' + filePath + fileName)
