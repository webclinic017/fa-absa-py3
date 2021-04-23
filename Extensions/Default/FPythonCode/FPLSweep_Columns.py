""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/pl_processing/etc/FPLSweep_Columns.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------

"""----------------------------------------------------------------------------
MODULE
    FPLSweep_Columns - Module which contains column definitions for FPLSweep.

    Purpose:

    projPL and ThTPL columns by default do not provide valuations when the
    valuation date is set in the future. This module provides overrides to
    P&L values which allow PL Sweep to use future values of projPL and ThTPL
    thus providing support for Spot Next sweeps.

----------------------------------------------------------------------------"""


import collections


import acm


from FBDPCurrentContext import Logme


module = "PLSweep"


def Remove():

    context = acm.GetDefaultContext()
    context.RemoveModule(module)
    Logme()('Successfully removed PL Sweep module definitions for projPL and '
            'ThTPL.')
    return True


def Apply():

    context = acm.GetDefaultContext()
    editModule = acm.FExtensionModule[module]
    if not editModule:
        editModule = acm.FExtensionModule()
        editModule.Name(module)

    ExtList = []
    Ext = collections.namedtuple('Ext', 'className name value')
    ExtList.append(Ext(
            className='FInstrumentAndTrades',
            name='actualCash',
            value='shunt(profitAndLossPeriodType, '
                    '"Inception to Present"->actualCashLive, '
                    '"Inception to Historical"->actualCashEnd, '
                    '"Inception to Future"->actualCashLive, '
                    '"Historical to Present"->'
                            'actualCashLive - actualCashStart, '
                    '"Historical to Historical"->'
                            'actualCashEnd - actualCashStart'
            ');'))

    ExtList.append(Ext(
            className='FCombInstrMapAndTrades',
            name='theoreticalPeriodValue',
            value='nil'))

    ExtList.append(Ext(
            className='FInstrumentAndTrades',
            name='theoreticalPeriodValue',
            value='shunt(profitAndLossPeriodType, '
                    '"Inception to Present"->theoreticalValueEnd, '
                    '"Inception to Historical"->marketValueEndValues, '
                    '"Inception to Future"->theoreticalValueEnd, '
                    '"Historical to Present"->'
                            'theoreticalValueEnd - marketValueStart, '
                    '"Historical to Historical"->'
                            'marketValueEndValues - marketValueStart'
            ');'))

    ExtList.append(Ext(
            className='FLegAndTrades',
            name='theoreticalPeriodValue',
            value='nil'))

    ExtList.append(Ext(
            className='FPriceAggregate',
            name='theoreticalPeriodValue',
            value='switch(singleInstrumentAndTrades, '
                    'nil->0.0, '
                    'default->singleInstrumentAndTrades :*'
                            ' "theoreticalPeriodValue"'
            ');'))

    ExtList.append(Ext(
            className='FTimeBucketAndObject',
            name='theoreticalPeriodValue',
            value='scenarioaxisarray('
                    'rowInstrumentAndTrades:theoreticalPeriodValue ['
                            'profitAndLossSeparateHistorical := true, '
                            'profitAndLossStartDate :=  longTimeAgo, '
                            'profitAndLossEndDate = valuationDate'
                    '], '
                    'timeDistributionPerimeterNames, '
                    '<["timeDistributionBucket"], , ,  timeBucketCollection>'
            ')[timeBucketCollectionIndex];'))

    ExtList.append(Ext(
            className='FInstrumentAndTrades',
            name='groupingSpotFunding',
            value='shunt(profitAndLossPeriodType, '
                    '"Inception to Present"->groupingSpotFundingLive, '
                    '"Inception to Historical"->groupingSpotFundingEnd, '
                    '"Historical to Present"->groupingSpotFundingLive - '
                            'groupingSpotFundingStart, '
                    '"Historical to Historical"->'
                            'groupingSpotFundingEnd - groupingSpotFundingStart'
            ');'))

    ExtList.append(Ext(
            className='FInstrumentAndTrades',
            name='assetUPL',
            value='markToMarketPeriodValue + openValueAdjustment + '
                    'groupingSpotFunding;'))

    ExtList.append(Ext(
            className='FInstrumentAndTrades',
            name='fundingEnd',
            value='collapse(fundingEndValues);'))

    ExtList.append(Ext(
            className='FInstrumentAndTrades',
            name='fundingLive',
            value='collapse(fundingValuesLive);'))

    ExtList.append(Ext(
            className='FInstrumentAndTrades',
            name='fundingStart',
            value='collapse(fundingStartValues);'))

    ExtList.append(Ext(
            className='FObject',
            name='useHistoricalMappingLinkToday',
            value='nilObject:useHistoricalMappingLinkToday;'))

    ExtList.append(Ext(
            className='FUndefinedObject',
            name='useHistoricalMappingLinkToday',
            value='true;'))

    try:
        for ext in ExtList:
            text = '[%s]%s:%s=%s' % (module, ext.className, ext.name,
                    ext.value)
            context.EditImport('FExtensionAttribute', text, 1, editModule)
        editModule.Commit()
        Logme()('Successfully applied PL Sweep module definitions for projPL '
                'and ThTPL.')
    except Exception as e:
        print("Exception:", e)
        Logme()('Failed to apply PL Sweep module definitions for projPL and '
              'ThTPL.')
        return False

    context.AddModule(module)
    return True
