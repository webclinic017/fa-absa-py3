""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FMtMPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FMtMPerform - Module which executes the Mark-to-Market.

DESCRIPTION
    This module executes the Mark-to-Market procedure based on the
    parameters passed from the script FMarkToMarket.
----------------------------------------------------------------------------"""


import os


import ael
import acm


import FBDPCommon
import FBDPWorld
import FMtMCalcVal
import FMtMSelInsCurr
import FMtMTask
import FMtMUtil


def _eval_preferred_markets_spec_string(specStr, specErrMsg):

    try:
        spec = eval(specStr)
    except:
        raise RuntimeError('{0}: {1}.  Format error.'.format(specErrMsg,
                specStr))
    if not isinstance(spec, dict):
        raise RuntimeError('{0}: {1}.  Format error.'.format(specErrMsg,
                specStr))
    return spec


def _getAllPriceFindingNames():

    return [r.Name() for r in acm.FPriceFinding.Select('')]


def _getAllMarketPlaceNames():

    return [acmMkt.Name() for acmMkt in acm.FMarketPlace.Select('')]


def _validate_preferred_markets_spec(specStr):
    """
    Process through the spec string, validated each price finding rule and
    market, and finally return a dictionary of price finding rule to market
    list.
    """
    if not specStr:
        return None
    specErrMsg = 'Invalid preferred market specification'
    spec = _eval_preferred_markets_spec_string(specStr, specErrMsg)
    pfNames = _getAllPriceFindingNames()
    mktNames = _getAllMarketPlaceNames()
    # Iterate through each item in the spec
    for pfrule, markets in spec.items():
        # Check price finding rule
        if pfrule == 'None':
            pfrule = None
        if pfrule and pfrule not in pfNames:
            raise RuntimeError('{0}: {1}.  No such price finding rule '
                    '{2}.'.format(specErrMsg, specStr, pfrule))
        # Check markets
        if not isinstance(markets, list):
            raise RuntimeError('{0}: {1}.  Markets should be specified in '
                    'list.'.format(specErrMsg, specStr))
        for m in markets:
            if m not in mktNames:
                raise RuntimeError('{0}: {1}.  No such market {2}.'.format(
                        specErrMsg, specStr, m))
    # All check had been done, return the spec
    return spec


def _validateMtMMarket(strMtMMarket):

    mtmMarket = acm.FMTMMarket[strMtMMarket]
    if not mtmMarket:
        raise RuntimeError('Unable to find MTM Market \'{0}\'.'.format(
                strMtMMarket))
    return mtmMarket


def _validateInstruments(world, insOidList):

    insList = []
    for insOid in insOidList:
        ins = acm.FInstrument[insOid]
        if ins.IsKindOf(acm.FCurrency):
            world.logWarning('Currency instruments should be defined in the '
                    '\'Pairs of currencies\' field, rather than the '
                    '\'Instruments\' field.  Instrument \'{0}\' is ignored '
                    'from the instrument list.'.format(ins.Name()))
            continue
        insList.append(ins)
    return insList


def _get_backdated_insts(instruments):
    backDatedIns = []
    for insOid in instruments:
        acmIns = acm.FInstrument[insOid]
        if not acmIns:
            continue
        createTime = acmIns.CreateTime()
        createDate = ael.date_from_time(createTime)
        trds = ael.Trade.select('insaddr={0}'.format(insOid))
        for t in trds:
            acmTrd = FBDPCommon.ael_to_acm(t)
            tradeTime = acmTrd.TradeTime()
            tradeDate = FBDPCommon.toDateAEL(tradeTime)
            if tradeDate < createDate:
                backDatedIns.append(acmIns)
                break
    return backDatedIns


def _validatePairsOfCurrencies(strCurrDupletList):

    curr1Curr2DupletNameSet = set()
    selCurr1Curr2DupletNameList = []
    for strCurrDuplet in strCurrDupletList:
        strCurr1, strCurr2 = strCurrDuplet.split('/')[0:2]
        curr1Ins = acm.FCurrency[strCurr1]
        if not curr1Ins:
            raise RuntimeError('Unable to find currency 1 \'{0}\' for the '
                    'pair of currencies \'{1}\'.'.format(strCurr1,
                    strCurrDuplet))
        curr1Name = curr1Ins.Name()
        curr2Ins = acm.FCurrency[strCurr2]
        if not curr2Ins:
            raise RuntimeError('Unable to find currency 2 \'{0}\' for the '
                    'pair of currencies \'{1}\'.'.format(strCurr2,
                    strCurrDuplet))
        curr2Name = curr2Ins.Name()
        if curr1Ins.Oid() == curr2Ins.Oid():
            raise RuntimeError('The currency 1 \'{0}\' and currency 2 \'{1}\' '
                    'of a pair of currencies \'{2}\' should not be referring '
                    'to the same instrument.'.format(strCurr1, strCurr2,
                    strCurrDuplet))
        curr1Curr2DupletName = curr1Name + '/' + curr2Name
        if curr1Curr2DupletName in curr1Curr2DupletNameSet:
            raise RuntimeError('Duplicated pair of currencies selection.  '
                'The pair of currencies \'{0}\' had been included in the '
                'selection.'.format(curr1Curr2DupletName))
        curr2Curr1DupletName = curr2Name + '/' + curr1Name
        if curr2Curr1DupletName in curr1Curr2DupletNameSet:
            raise RuntimeError('Duplicated pair of currencies selection.  The '
                    'reversed pair of currencies \'{0}\' had been included in '
                    'the selection.'.format(curr2Curr1DupletName))
        curr1Curr2DupletNameSet.add(curr1Curr2DupletName)
        selCurr1Curr2DupletNameList.append(curr1Curr2DupletName)
    return selCurr1Curr2DupletNameList


def _selectCurrencyPairs(currPairs, invert=False):
    currPairs = _validatePairsOfCurrencies(currPairs)
    if not invert:
        return currPairs
    allPairs = [cp.Name() for cp in acm.FCurrencyPair.Select('')]
    return list(set(allPairs).difference(currPairs))


def _validateCVAModule(exportCredBalAAJ):

    if not exportCredBalAAJ:
        return None
    modNames = [mod.Name() for mod in acm.GetDefaultContext().Modules()]
    if 'CVA' not in modNames:
        raise RuntimeError('Module "CVA" is not installed.  The '
                'Mark-to-Market script need this module so that it can '
                'export the AAJ files for Credit Balance instruments.')
    return


def _validateExportCredBalAAJPath(exportCredBalAAJ, exportPath):

    if not exportCredBalAAJ:
        return None
    if not os.path.exists(exportPath):
        raise RuntimeError('The given export path "{0}" does not '
                'exists.'.format(exportPath))
    if not os.path.isdir(exportPath):
        raise RuntimeError('The given export path "{0}" is not '
                'a directory.'.format(exportPath))
    if not os.access(exportPath, os.W_OK):
        raise RuntimeError('The given export path "{0}" is not '
                'writable.'.format(exportPath))
    return os.path.abspath(exportPath)


def _setupHookCalculateMtMPrice(world):

    try:
        from FBDPHook import calculate_mtm_price
    except ImportError:
        pass
    else:
        FMtMTask.MtMTaskPrice.setCalcHook(calculate_mtm_price)
        world.logInfo('Loading hook: FBDPHook.calculate_mtm_price')


def _setupHookAdjustMtMPrice(world):

    try:
        from FBDPHook import adjust_mtm_price
    except ImportError:
        pass
    else:
        FMtMTask.MtMTaskPrice.setPostAdjustHook(adjust_mtm_price)
        world.logInfo('Loading hook: FBDPHook.adjust_mtm_price')


def _applyHookTweakUndLastprice(world, undInsList, calcPriceCache):

    try:
        from FBDPHook import tweak_und_lastprice
        insPriceList = []
        for undIns in undInsList:
            undInsOid = undIns.Oid()
            undInsCurrOid = undIns.Currency().Oid()
            if (undInsOid in calcPriceCache and
                    undInsCurrOid in calcPriceCache[undInsOid]):
                mtmCalcPrice = calcPriceCache[undInsOid][undInsCurrOid]
                insPriceList.append((undInsOid, mtmCalcPrice.settle))
        tweak_und_lastprice(insPriceList)
    except ImportError:
        pass


def _findSelInsCurrPairList(world, selInsList, aelMtMDate,
        needAddingRelatedIns):

    # Filter out expired instruments from original selection.
    selInsList = FMtMSelInsCurr.selectMtMInstruments(world,
            insOids=[ins.Oid() for ins in selInsList],
            aelExpDay=aelMtMDate.add_days(-1))
    if not selInsList:
        world.logInfo('    No unexpired instruments selected. Nothing done.')
        return []

    world.logInfo('    There are {0} selected instruments.'.format(
            len(selInsList)))
    # Add combination components, underlyings, and other refered instruments
    relatedInsList = []
    if needAddingRelatedIns:
        world.logDebug('    Adding related instruments into selection...')
        relatedInsList = [relatedIns for selIns in selInsList
                for relatedIns
                in FMtMSelInsCurr.findRelatedInstruments(selIns)]
        relatedInsList = FMtMUtil.uniquifyListByOid(relatedInsList)
        world.logInfo('    Found {0} related instruments to be add into '
                'selection.'.format(len(relatedInsList)))
    selInsList = FMtMUtil.uniquifyListByOid(selInsList + relatedInsList)
    world.logInfo('    Total {0} instruments in the selection.'.format(
                len(selInsList)))
    # Filter the related instruments found.
    world.logInfo('    Filtering instruments to MtM.')
    selInsList = FMtMSelInsCurr.selectMtMInstruments(world,
            insOids=[ins.Oid() for ins in selInsList],
            aelExpDay=aelMtMDate.add_days(-1))
    world.logInfo('    {0} selected instruments remains after '
            'filtering.'.format(len(selInsList)))
    # Transform selected instruments into instrument-currency pair
    world.logDebug('    Finding the currencies of the selected instruments...')
    selInsCurrPairList = (FMtMSelInsCurr.converInsListToInsCurrPairList(
            selInsList))
    world.logDebug('    Found {0} instrument-currency combinations to find '
            'prices in, for the selected instruments'.format(
            len(selInsCurrPairList)))
    return selInsCurrPairList


def _findFxInsCurrPairList(world, selCurrDupletNameList):

    world.logDebug('    Finding selected pairs of currencies...')
    selFxInsCurrPairList = (FMtMSelInsCurr.
            convertCurrDupletNameListToInsCurrPairList(selCurrDupletNameList))
    world.logInfo('    Found {0} pairs of currencies'.format(len(
            selFxInsCurrPairList)))
    return selFxInsCurrPairList


def _findBmInsCurrPairList(world):

    world.logDebug('    Finding yield curve benchmark instruments...')
    bmInsOidList = [ins.Oid() for ins
            in FMtMSelInsCurr.findBenchmarkInstruments()]
    selBmInsList = FMtMSelInsCurr.selectYcBmInstruments(world,
            insOids=bmInsOidList)
    world.logInfo('    Found {0} yield curve benchmarks instruments.'.format(
            len(selBmInsList)))
    world.logDebug('    Adding instruments from Page \'MTM_YIELD_CURVE\'...')
    selMtMYcInsList = FMtMSelInsCurr.selectMtMYcInstruments(world)
    if selMtMYcInsList:
        selBmInsList = FMtMUtil.uniquifyListByOid(
                    selBmInsList + selMtMYcInsList)
        world.logInfo('    Added {0} Zero Coupons instruments from page '
                '\'MTM_YIELD_CURVES\' as yield curve benchmark '
                'instruments'.format(len(selMtMYcInsList)))
    world.logDebug('    Finding the currencies of the yield curve benchmark '
            'instruments...')
    selBmInsCurrPairList = FMtMSelInsCurr.converInsListToInsCurrPairList(
            selBmInsList)
    world.logDebug('    Found {0} instrument-currency combinations to find '
            'prices in, for the yield curve benchmark instruments.'.format(
            len(selBmInsCurrPairList)))
    return selBmInsCurrPairList


def _makeAAJFilename(mtmIsoDate, insName):
    if mtmIsoDate:
        packedDate = mtmIsoDate.replace('-', '')
        fileName = '{0}_{1}'.format(insName, packedDate)
    else:
        fileName = insName

    return FMtMUtil.makeValidFileName(fileName + '.aaj')


def _writeToFile(world, filePath, content):

    errMsg = None
    if not world.isInTestMode():
        with open(filePath, 'w') as f:
            f.write(content)
    return errMsg


def _exportCreditBalanceAAJFiles(world, credBalAAJExportPath, mtmIsoDate,
        credBalInsCurrPairs):

    if not credBalAAJExportPath:
        return
    world.logDebug('    Exporting AAJ files to directory:{0}'.format(
            credBalAAJExportPath))
    calcSpaceMngr = FMtMCalcVal.PortfolioSheetCalcSpaceManager(world)
    for insCurrPair in credBalInsCurrPairs:
        insName = insCurrPair.ins.Name()
        aajFileName = _makeAAJFilename(mtmIsoDate=mtmIsoDate, insName=insName)
        aajFileFullPath = os.path.join(credBalAAJExportPath, aajFileName)
        world.logDebug('        Exporting "{0}"...'.format(aajFileFullPath))
        errMsg = None
        try:
            fileContent = calcSpaceMngr.getCVAXML(insCurrPair.ins)
            _writeToFile(world, filePath=aajFileFullPath, content=fileContent)
        except Exception as e:
            errMsg = str(e)
        if errMsg:
            world.logError(errMsg)
            world.summaryAddFail('Instrument', insCurrPair.ins.Oid(),
                    'ExportAAJ', [errMsg])
        else:
            world.summaryAddOk('Instrument', insCurrPair.ins.Oid(),
                    'ExportAAJ')
    world.logDebug('    Done Exporting')


def _step_recalculateYieldCurves(world, v_recalc_yieldcurve,
        v_all_except_yieldcurve, v_recalc_also_dep_yc, v_recalc_in_dep_order,
        m_date):

    world.logInfo('Recalculating yield curves...')
    selOrigYcNameList = FMtMUtil.findSelectedOriginalYieldCurveNames(world,
            v_recalc_yieldcurve, v_all_except_yieldcurve,
            v_recalc_also_dep_yc)
    world.logDebug('    Total {0} yield curve names selected.'.format(
            len(selOrigYcNameList)))
    hieSortedOrigYcNameList = FMtMUtil.hieSortYieldCurveNamesIfRequried(
            world, selOrigYcNameList,
            isSortingRequired=v_recalc_in_dep_order,
            isToWarnMissingDependency=not(v_recalc_also_dep_yc))
    recalcYcList = FMtMUtil.findOnDateAcmYieldCurveList(world,
            hieSortedOrigYcNameList)
    world.logDebug('    Total {0} yield curves on the date.'.format(
            len(recalcYcList)))
    recalcYCTask = FMtMTask.MtMTaskRecalcYieldCurves(world, m_date,
            recalcYcList)
    recalcYCTask.save()
    world.logInfo('Done recalculating yield curves.')


def _step_recalcVolatilitySurfaces(world, v_recalc_volsurf,
        v_all_except_volsurf, v_remove_zero_volatilities,
        v_apply_filter, m_date):

    world.logInfo('Recalculating volatility structures...')
    recalcVolList = FMtMUtil.findSelectedVolatilityStructures(world,
            v_recalc_volsurf, v_all_except_volsurf)
    recalcVolTask = FMtMTask.MtMTaskRecalcVolStructs(world, m_date,
            recalcVolList, v_remove_zero_volatilities, v_apply_filter)
    recalcVolTask.save()
    world.logInfo('Done recalculating volatility structures.')


def _step_volatilitySurfaceMaintenance(world, v_vol_benchmarks, m_date,
        mtmMarket, calcPriceCache, m_save_zero_price, m_decimals,
        m_override_price, v_vol_base, v_vol_prefix,
        p_bid_ask_prices, p_high_low_prices, p_last_prices,
        p_use_zero_if_missing_prices, v_vol_suffix, v_context,
        v_call_put, m_exclude_vol_ins, v_save_vol_as_price, volMarket,
        v_remove_zero_volatilities):

    world.logInfo('Maintaining volatility structures...')
    world.logInfo('    Finding volatility benchmark instruments...')
    selVolInsList = FMtMSelInsCurr.selectVolBmInstruments(world,
            insOids=v_vol_benchmarks)
    world.logInfo('    Found {0} volatility benchmark instruments'.format(
            len(selVolInsList)))
    if selVolInsList:
        insAndAllUndInsList = FMtMSelInsCurr.findInsAndAllUndInsList(
                selVolInsList)
        volInsCurrPairList = FMtMSelInsCurr.converInsListToInsCurrPairList(
                insAndAllUndInsList)
        volUndAndDersList = FMtMSelInsCurr.findUndAndDersList(selVolInsList)
        undInsList = [undAndDers.undIns for undAndDers in
                volUndAndDersList]
        # Save vol benchmark instrument MtM prices
        world.logInfo('    Calculating and saving MtM prices for '
                'volatility benchmark instruments and underlyings...')
        volPriceTask = FMtMTask.MtMTaskPrice(world, m_date, mtmMarket,
                insCurrPairList=volInsCurrPairList,
                calcPriceCache=calcPriceCache,
                exclude_zero=(not m_save_zero_price),
                bid_and_ask=p_bid_ask_prices,
                high_and_low=p_high_low_prices,
                last=p_last_prices,
                use_zero_prices=p_use_zero_if_missing_prices,
                digits=m_decimals,
                override_price=m_override_price)
        volPriceTask.calculate()
        _applyHookTweakUndLastprice(world, undInsList, calcPriceCache)
        volPriceTask.save()
        world.logInfo('    Done calculated and saved MtM prices for '
                'volatility benchmark instruments and underlyings.')
        # Save vol
        world.logInfo('    Calculating and saving volatilities...')
        volTask = FMtMTask.MtMTaskVol(world, m_date, mtmMarket,
                undAndDersList=volUndAndDersList,
                base=v_vol_base, vol_prefix=v_vol_prefix,
                vol_suffix=v_vol_suffix, context=v_context,
                call_put=v_call_put, ca_adjust_regexp=m_exclude_vol_ins,
                remove_zero_volatilities=v_remove_zero_volatilities)

        volTask.save()
        volsInfo = volTask.getVolsInfo()
        world.logInfo('    Done calculating and saving volatilities.')
        # Save vol as price
        if v_save_vol_as_price:
            world.logInfo('    Saving volatilities in price table')
            saveVolAsPriceTask = FMtMTask.MtMTaskVolPrice(world,
                    m_date, volMarket, undAndDersList=volUndAndDersList,
                    volsInfo=volsInfo)
            saveVolAsPriceTask.calculate()
            saveVolAsPriceTask.save()
            world.logInfo('    Done saving volatilities in price table')
    else:
        world.logWarning('No volatility benchmark instruments found.  '
                'No volatility structure updated')
    world.logInfo('Done maintaining volatility structures.')


def _SelectInsCurrPair(world,
    selInsList,
    date,
    addRelated,
    selCurrDupletNameList,
    addBenchmarks
):
    # Instrument selection and add related instruments
    world.logInfo('Processing instruments and currencies MtM...')
    selInsCurrPairList = []
    if selInsList:
        selInsCurrPairList = _findSelInsCurrPairList(world, selInsList, date,
            bool(addRelated))

    # Pairs of currencies
    selFxInsCurrPairList = []
    if selCurrDupletNameList:
        selFxInsCurrPairList = _findFxInsCurrPairList(world,
            selCurrDupletNameList)

    # Benchmark instruments
    selBmInsCurrPairList = []
    if addBenchmarks:
        selBmInsCurrPairList = _findBmInsCurrPairList(world)

    # Sum up the ins/curr to be MtM from the three list.
    mtmInsCurrPairSet = set()
    for insCurrPair in selInsCurrPairList + selFxInsCurrPairList\
                        + selBmInsCurrPairList:
        mtmInsCurrPairSet.add(insCurrPair)

    world.logDebug('    Total {0} unique instrument-currency combinations to '
        'find prices in.'.
        format(len(mtmInsCurrPairSet)))
    return list(mtmInsCurrPairSet)

def _step_savingMtMPrices(world,
    mtmInsCurrPairList,
    date,
    preferredMarkets,
    mtmMarket,
    pBidAskPrices,
    pHighLowPrices,
    pLastPrices,
    pUseZeroIfMissingPrices,
    calcPriceCache,
    decimals,
    excludeInstypesPm,
    overridePrice,
    saveZeroPrice,
    useYesterday,
    sourceMtmMarket,
    backdated,
    credBalAAJExportPath
):
    # MtM the prices in the ins/curr.
    if mtmInsCurrPairList:
        credBalInsCurrPairs, nonCredBalInsCurrPairs = (
                FMtMSelInsCurr.splitInsCurrPairsByInsTypeCreditBalance(
                mtmInsCurrPairList))
        if preferredMarkets:
            world.logInfo('    Processing MtM task with preferred market '
                    'specifications...')
            descr = [FMtMUtil.PreferredMarketDescr(p_name, markets)
                    for p_name, markets in preferredMarkets.items()]
            prefMarketHandler = FMtMUtil.PreferredMarketHandler(descr)
            credBalPriceTask = FMtMTask.MtMTaskPricePreferredMarket(world,
                    date, mtmMarket, insCurrPairList=credBalInsCurrPairs,
                    calcPriceCache=calcPriceCache,
                    exclude_zero=(not saveZeroPrice),
                    bid_and_ask=pBidAskPrices,
                    high_and_low=pHighLowPrices,
                    last=pLastPrices,
                    use_zero_prices=pUseZeroIfMissingPrices,
                    digits=decimals,
                    pref_handler=prefMarketHandler,
                    exclude_instypes=excludeInstypesPm,
                    override_price=overridePrice,
                    useYesterday=useYesterday,
                    sourceMtmMarket=sourceMtmMarket,
                    backDated=backdated)
            nonCredBalPriceTask = FMtMTask.MtMTaskPricePreferredMarket(world,
                    date, mtmMarket, insCurrPairList=nonCredBalInsCurrPairs,
                    calcPriceCache=calcPriceCache,
                    exclude_zero=(not saveZeroPrice),
                    bid_and_ask=pBidAskPrices,
                    high_and_low=pHighLowPrices,
                    last=pLastPrices,
                    use_zero_prices=pUseZeroIfMissingPrices,
                    digits=decimals,
                    pref_handler=prefMarketHandler,
                    exclude_instypes=excludeInstypesPm,
                    override_price=overridePrice,
                    useYesterday=useYesterday,
                    sourceMtmMarket=sourceMtmMarket,
                    backDated=backdated)
        else:
            world.logInfo('    Processing MtM task...')
            credBalPriceTask = FMtMTask.MtMTaskPrice(world, date, mtmMarket,
                    insCurrPairList=credBalInsCurrPairs,
                    calcPriceCache=calcPriceCache,
                    exclude_zero=(not saveZeroPrice),
                    bid_and_ask=pBidAskPrices,
                    high_and_low=pHighLowPrices,
                    last=pLastPrices,
                    use_zero_prices=pUseZeroIfMissingPrices,
                    digits=decimals,
                    override_price=overridePrice,
                    useYesterday=useYesterday,
                    sourceMtmMarket=sourceMtmMarket,
                    backDated=backdated)
            nonCredBalPriceTask = FMtMTask.MtMTaskPrice(world, date,
                    mtmMarket, insCurrPairList=nonCredBalInsCurrPairs,
                    calcPriceCache=calcPriceCache,
                    exclude_zero=(not saveZeroPrice),
                    bid_and_ask=pBidAskPrices,
                    high_and_low=pHighLowPrices,
                    last=pLastPrices,
                    use_zero_prices=pUseZeroIfMissingPrices,
                    digits=decimals,
                    override_price=overridePrice,
                    useYesterday=useYesterday,
                    sourceMtmMarket=sourceMtmMarket,
                    backDated=backdated)
        if credBalInsCurrPairs:
            world.logInfo('    Calculating Prices for credit balance '
                    'instruments...')
            credBalPriceTask.calculate()
            world.logInfo('    Done calculating prices for credit balance '
                    'instruments.')
            _exportCreditBalanceAAJFiles(world, credBalAAJExportPath,
                    mtmIsoDate=date.to_string(ael.DATE_ISO),
                    credBalInsCurrPairs=credBalInsCurrPairs)
            world.logInfo('    Saving Prices for credit balance instruments..')
            credBalPriceTask.save()
            world.logInfo('    Done saving prices for credit balance '
                          'instruments.')
        world.logInfo('    Calculating Prices...')
        nonCredBalPriceTask.calculate()
        world.logInfo('    Done calculating prices.')
        world.logInfo('    Saving Prices..')
        nonCredBalPriceTask.save()
        world.logInfo('    Done saving prices')


def _step_SEQDataMaintenance(world):

    world.logInfo('Saving SEQ Data...')
    if world.isInTestMode():
        world.logInfo('No testmode possible for SEQ data')
    elif ael.historical_mode():
        world.logInfo('SEQDataMaint is skipped since instrument data '
                'cannot be updated in historical mode.')
    else:
        try:
            import FSEQDataMaint
            if hasattr(FSEQDataMaint, 'UpdateAllExoticOptions') and\
               hasattr(FSEQDataMaint, 'UPDATE_HISTORICAL'):
                world.logInfo('\n Updating Structured Equity related '
                        'data... \n')
                udateHistoricalOld = FSEQDataMaint.UPDATE_HISTORICAL
                FSEQDataMaint.UPDATE_HISTORICAL = True
                try:
                    FSEQDataMaint.UpdateAllExoticOptions()

                except Exception as ex:
                    world.logWarning('\nFSEQDataMaint reported error: {0}'.\
                                     format(str(ex)))
                finally:
                    # Restore original state of FSEQDataMaint
                    FSEQDataMaint.UPDATE_HISTORICAL = udateHistoricalOld
        except ImportError:
            world.logWarning('\nModule FSEQDataMaint could not be found. '
                    'SEQ data not updated')

    world.logInfo('Done saving SEQ Data.')


def perform_mtm(execParam):

    world = FBDPWorld.CreateWorld(execParam)
    world.logStart(None)
    # Call section hook
    FBDPCommon.callSelectionHook(execParam, 'Instruments',
            'mark_to_market_selection')
    # Process parameter
    pInstruments = execParam.get('Instruments')
    pAddBenchmarks = execParam.get('AddBenchmarks')
    pAddRelated = execParam.get('AddRelated')
    pBackdatedInsts = execParam.get('BackDated', 0)
    pPairsOfCurr = execParam.get('PairsOfCurr', [])
    pBidAskPrices = execParam.get('SaveBidAndAsk')
    pHighLowPrices = execParam.get('SaveHighAndLow')
    pLastPrices = execParam.get('SaveLast')
    pUseZeroIfMissingPrices = execParam.get('UseZeroIfPricesMissing', 1)
    pMtmMarket = execParam.get('MtmMarket')
    vVolBenchmarks = execParam.get('VolBenchmarks')
    vVolBase = execParam.get('VolBase')
    vVolPrefix = execParam.get('VolPrefix')
    vVolSuffix = execParam.get('VolSuffix')
    vContext = execParam.get('Context')
    vCallPut = execParam.get('CallPut')
    vRecalcVolsurf = execParam.get('VolSurfaces')
    vRemoveZeroVolatilities = execParam.get('ZeroVolatilities', 1)
    vApplyFilter = execParam.get('ApplyFilter', 0)
    vAllExceptVolsurf = execParam.get('AllExceptVolsurf')
    vSaveVolAsPrice = execParam.get('SaveVolAsPrice')
    vVolMarket = execParam.get('VolMarket', '')
    vRecalcYieldcurve = execParam.get('YieldCurves')
    vAllExceptYieldcurve = execParam.get('AllExceptYieldcurve')
    vRecalcAlsoDepYc = bool(execParam.get('RecalcAlsoDepYc'))
    vRecalcInDepOrder = bool(execParam.get('RecalcYcInDepOrder'))
    exportCredBalAAJ = bool(execParam.get('ExportCredBalAAJ'))
    exportPath = execParam.get('ExportPath', '')
    mDate = FBDPCommon.toDateAEL(execParam.get('Date'))
    mSaveZeroPrice = execParam.get('SaveZeroPrices')
    useYesterday = execParam.get('UseYesterday')
    source_mtm_market = execParam.get('sourceMtmMarket', None)
    if useYesterday:
        if not source_mtm_market:
            raise RuntimeError('Source Mtm market is missing')
        source_mtm_market = _validateMtMMarket(source_mtm_market)
    mDecimals = execParam.get('Decimals')
    if mDecimals != '':
        mDecimals = int(mDecimals)
    mExcludeVolIns = execParam.get('ExcludeInsFromVS')
    mPreferredMarkets = execParam.get('PreferredMarkets')
    if mPreferredMarkets:
        mPreferredMarkets = _validate_preferred_markets_spec(
                mPreferredMarkets)
    mExcludeInstypesPm = execParam.get('ExcludeInstypesPM', [])
    mSaveSeqData = execParam.get('SaveSEQData')
    mOverridePrice = execParam.get('OverridePrice')
    # Validate
    mtmMarket = _validateMtMMarket(pMtmMarket)
    if pBackdatedInsts:
        selInsList = _get_backdated_insts(pInstruments)
    else:
        selInsList = _validateInstruments(world, pInstruments)
    invertCurrencies = execParam.get('AllExceptCurrencies', False)
    selCurrDupletNameList = _selectCurrencyPairs(pPairsOfCurr,
            invertCurrencies)
    if vVolBenchmarks and vSaveVolAsPrice:
        volMarket = _validateMtMMarket(vVolMarket)
    else:
        volMarket = None
    _validateCVAModule(exportCredBalAAJ)
    credBalAAJExportPath = _validateExportCredBalAAJPath(exportCredBalAAJ,
            exportPath)
    # Initialise
    ael.date_set_today(ael.date_today())
    calcPriceCache = FMtMCalcVal.CalculatedPriceCache()
    _setupHookCalculateMtMPrice(world)
    _setupHookAdjustMtMPrice(world)
    # ========================
    # Recalculate yield curves
    # ========================
    if vRecalcYieldcurve:
        _step_recalculateYieldCurves(world, vRecalcYieldcurve,
                vAllExceptYieldcurve, vRecalcAlsoDepYc,
                vRecalcInDepOrder, mDate)
    # ===============================
    # Recalculate volatility surfaces
    # ===============================
    if vRecalcVolsurf:
        _step_recalcVolatilitySurfaces(world, vRecalcVolsurf,
                vAllExceptVolsurf, vRemoveZeroVolatilities,
                vApplyFilter, mDate)
    # ==============================
    # Volatility surface maintenance
    # ==============================
    if vVolBenchmarks:
        _step_volatilitySurfaceMaintenance(world, vVolBenchmarks, mDate,
                mtmMarket, calcPriceCache, mSaveZeroPrice, mDecimals,
                mOverridePrice, vVolBase, vVolPrefix, pBidAskPrices,
                pHighLowPrices, pLastPrices, pUseZeroIfMissingPrices,
                vVolSuffix, vContext, vCallPut, mExcludeVolIns,
                vSaveVolAsPrice, volMarket, vRemoveZeroVolatilities)
    # =================
    # Selecting all needed instruments (related included if it is chacked)
    # =================
    mtmInsCurrPairList = _SelectInsCurrPair(world,
                            selInsList,
                            mDate,
                            pAddRelated,
                            selCurrDupletNameList,
                            pAddBenchmarks
                         )
    if mtmInsCurrPairList:
        # =================
        # Separating exotic and non exotic instruments
        # =================
        exoticInstrumentsList,\
        nonExoticInstrumetsList = FMtMSelInsCurr.\
            SplitInstrumentByInsTypeExotic(mtmInsCurrPairList)
        # =================
        # Saving MtM Prices for non exotic instruments
        # =================
        _step_savingMtMPrices(world,
            nonExoticInstrumetsList,
            mDate,
            mPreferredMarkets,
            mtmMarket,
            pBidAskPrices,
            pHighLowPrices,
            pLastPrices,
            pUseZeroIfMissingPrices,
            calcPriceCache,
            mDecimals,
            mExcludeInstypesPm,
            mOverridePrice,
            mSaveZeroPrice,
            useYesterday,
            source_mtm_market,
            pBackdatedInsts,
            credBalAAJExportPath
        )
        # ====================
        # SEQ Data Maintenance
        # ====================
        if mSaveSeqData:
            _step_SEQDataMaintenance(world)
        # =================
        # Saving MtM Prices for exotic instruments
        # =================
        _step_savingMtMPrices(world,
            exoticInstrumentsList,
            mDate,
            mPreferredMarkets,
            mtmMarket,
            pBidAskPrices,
            pHighLowPrices,
            pLastPrices,
            pUseZeroIfMissingPrices,
            calcPriceCache,
            mDecimals,
            mExcludeInstypesPm,
            mOverridePrice,
            mSaveZeroPrice,
            useYesterday,
            source_mtm_market,
            pBackdatedInsts,
            credBalAAJExportPath
        )
    else:
        world.logWarning('No Instruments match the selection criteria. No '
                'MtM-prices have been saved')

    world.logInfo('Done processing instruments and currencies MtM.')

    # Finalise
    world.summarySummarise()
    world.logFinish(None)
