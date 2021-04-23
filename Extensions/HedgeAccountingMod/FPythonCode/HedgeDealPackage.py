'''
===================================================================================================
PURPOSE: This module encapsulate all logic pertaining to the management of deal packages with in
            the scope of the Hedge Effectiveness Testing Suite.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''
import re

import ael
import acm
import FLogger

import HedgeConstants
import HedgeChildTradeUtils
import importlib

importlib.reload(HedgeConstants)

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)


def get_deal_package(name):
    '''Retrieve a dealpackage from the ADS
    '''

    dealPackage = acm.FDealPackage[name]

    return dealPackage


def get_next_dealpackage_name(baseName):
    '''Built a standarised name for the Hedge Effectiveness
        Deal Package to be used when creating new Hedge Relationships.
    '''

    dealPackageBaseNamePattern = HedgeConstants.STR_DEALPACKAGE_BASENAME_PATTERN
    dealPackageFullNamePattern = HedgeConstants.STR_DEALPACKAGE_FULLNAME_PATTERN
    nameSeperator = HedgeConstants.STR_DEALPACKAGE_NAME_SEPERATOR

    baseNameValidationResult = re.match(dealPackageBaseNamePattern, baseName)

    if baseNameValidationResult:

        query = r"""select
                        dp.*
                    from
                        DealPackage dp
                    where
                        dp.optional_id like '{0}%'""".\
                            format(baseName)
        columns, data = ael.asql(query)

        # default to 1
        nextInstanceNumber = 1

        if data[0]:

            listOfNameInstanceNumbers = []

            namePropertyIndex = columns.index('name')

            for row in data[0]:
                # only look at the names matching the Hedge
                # effectiveness solution naming conventions
                hedgeNameMatchResult = re.match(dealPackageFullNamePattern,
                                                row[namePropertyIndex])

                if hedgeNameMatchResult:
                    nameCompnents = row[namePropertyIndex].split('/')
                    nameIncrement = nameCompnents[len(nameCompnents)-1]
                    listOfNameInstanceNumbers.append(int(nameIncrement))

            maxInstanceNumber = max(listOfNameInstanceNumbers)
            nextInstanceNumber = int(maxInstanceNumber) + 1

        newName = '{0}{1}{2}'.format(baseName, nameSeperator, nextInstanceNumber)

        return newName
    else:
        raise Exception('Invalid name pattern detected.')


def get_dealpackage_trade_list(hedgeTradeList, hedgeStartDate):
    '''Returns list of DealPackageTradeItem items containing
        - dealPackageTrade, childTrade, originalTrade, percentage

        hedgeTradeList [dictionary] of trades [oid] = [type, percent, childTradeId]
                -Dictionary of trades to add into the dealpackage.
    '''

    # collection of trades that should be included in deal package
    # based on the Hedge Effectiveness trade type
    dealPackageTradeList = []

    for tradeId in hedgeTradeList:
        trade = acm.FTrade[tradeId]

        if trade:
            [tradeType, percent, childTradeId] = hedgeTradeList[tradeId]

            childTrade = None

            # if a childTrade ID is specified, try to retrieve the child trade
            if childTradeId:
                childTrade = acm.FTrade[childTradeId]

            # if childTrade is not yet created or found, create one
            # HedgeChildTradeUtils.create_child_trade() will return None for hedge
            # types that should not be represendted by child trades.
            if not childTrade:

                childTrade = HedgeChildTradeUtils.create_child_trade(trade,
                                                                     hedgeStartDate,
                                                                     tradeType,
                                                                     percent)

            # if child trade exist - use it in deal package
            if childTrade:

                item = DealPackageTradeItem(childTrade.Oid(),
                                            childTrade.Oid(),
                                            tradeId,
                                            percent,
                                            tradeType)
                dealPackageTradeList.append(item)

                # hedgeTradeList format: {'trade.oid' = [type, percent, childTradeId]}
                if len(hedgeTradeList[tradeId]) < 3:
                    hedgeTradeList[tradeId].append(childTrade.Oid())
                else:
                    hedgeTradeList[tradeId][2] = childTrade.Oid()

                logger.debug('%s = %s : Child = %s' % (tradeType, tradeId, childTrade.Oid()))

            # if child trade does not exist - assume it should not be used in deal package
            # -> use original trade instead. (In case of Hypo's & Zero Bonds)
            else:
                item = DealPackageTradeItem(tradeId, None, tradeId, percent, tradeType)
                dealPackageTradeList.append(item)

                logger.debug('%s = %s : Child = none' % (tradeType, tradeId))

        else:
            raise Exception('Failed to create child trade for Trade=%s. Trade not found.'
                            % (tradeId))

    return dealPackageTradeList


def set_dealpackage(shell, hedgeRelationshipName, hedgeTradeList, hedgeStartDate,
                    hedgeRelationStatus, currentActiveDealPackageName=None):
    '''Logic to create or update a Hedge Effectiveness Testing Dealpackage.

        hedgeRelationshipName [string]
            Base name to use for dealpackage, ie. HA/123456789/

        hedgeTradeList [dictionary] of trades [oid] = [type, percent, childTradeId]
            Dictionary of trades to add into the dealpackage.

        hedgeStartDate [datetime]
            Hedge Relationship designation date

        hedgeRelationStatus [HedgeConstants.Hedge_Relation_Status]
            Hedge Relationship current workflow status (Simulated, Proposed, Active, etc.)

        currentActiveDealPackageName [string]
            Name of the latest deal package in the instrument package
    '''

    # only create/update dealpackage if the Hedge Relationship is in 'Simulated' status.
    if hedgeRelationStatus == HedgeConstants.Hedge_Relation_Status.Simulated:

        # check if Instrumentpackage already exist
        instrumentPackage = acm.FInstrumentPackage[hedgeRelationshipName]
        if instrumentPackage:

            # package exist
            if not currentActiveDealPackageName:
                # create new
                return create_new_dealpackage(instrumentPackage.Name(),
                                              hedgeTradeList, hedgeStartDate)

            dealPackage = None
            for dp in instrumentPackage.DealPackages():
                if dp.OptionalId() == currentActiveDealPackageName:
                    dealPackage = dp

            if dealPackage:
                # update existing simulated package
                updatedTradeList = update_dealpackage(dealPackage,
                                                      hedgeTradeList,
                                                      hedgeStartDate)

                return [instrumentPackage.Name(), dealPackage.OptionalId()], updatedTradeList

            # dealpackage specified does not exist in current InstrumentPackage
            # -> thus create new dealpackage in this instrument package.
            return create_new_dealpackage(instrumentPackage.Name(),
                                          hedgeTradeList, hedgeStartDate)

        # Instrument package does not yet exist - create new one.
        return create_new_dealpackage(hedgeRelationshipName,
                                      hedgeTradeList, hedgeStartDate)

    # do not change/update the dealpackge if not in Simulated status.
    return [hedgeRelationshipName, currentActiveDealPackageName], hedgeTradeList


def create_new_dealpackage(instrumentPackageName, hedgeTradeList, hedgeStartDate):
    '''Create a new Deal Package enscapsulating a Hedge Relationship.

        instrumentPackageName -- string
            Base name to use for dealpackage, ie. HA/123456789/

        hedgeTradeList [dictionary] of trades [oid] = [type, percent, childTradeId]
            Dictionary of trades to add into the dealpackage.

        hedgeStartDate [datetime]
            Hedge Relationship designation date

        return the InstrumentPackageName [string], DealPackageName [string]
    '''
    dealPackageTradeList = []

    dealPackageTradeList = get_dealpackage_trade_list(hedgeTradeList, hedgeStartDate)
    tradeList = []

    for item in dealPackageTradeList:
        trade = acm.FTrade[item.DealPackageTrade]
        if trade:
            tradeList.append(trade)

    if instrumentPackageName and tradeList:
        newDealPackageName = get_next_dealpackage_name(instrumentPackageName)

        # check if Instrumentpackage already exist
        instrumentPackage = acm.FInstrumentPackage[instrumentPackageName]

        dealPackage = None
        if instrumentPackage:
            dealPackage = acm.FDealPackage()
            dealPackage.InstrumentPackage(instrumentPackage)
            dealPackage.OptionalId(newDealPackageName)
            dealPackage.DefinitionDisplayName(newDealPackageName)

            for trade in tradeList:
                dealPackage.AddTrade(trade)

            dealPackage.Commit()
            instrumentPackage.Commit()

        else:
            dealPackage = acm.DealPackage().NewFromTrades('FreeForm', tradeList)
            dealPackage.OptionalId(newDealPackageName)
            dealPackage.DefinitionDisplayName(newDealPackageName)
            dealPackage.InstrumentPackage().Name(instrumentPackageName)
            dealPackage.SaveNew()

        logger.debug('InstrumentPackage = %s : DealPackage = %s'
                     % (dealPackage.InstrumentPackage().Name(), dealPackage.OptionalId()))

        return [dealPackage.InstrumentPackage().Name(), dealPackage.OptionalId()], hedgeTradeList
    else:
        logger.ELOG('Invalid Hedge Relationship. Internal trade not specified.')
        return None, None


def update_dealpackage(dealPackage, hedgeTradeList, hedgeStartDate):

    dealPackageTradeList = get_dealpackage_trade_list(hedgeTradeList, hedgeStartDate)

    assert dealPackage, 'Dealpackage does not exist.'

    tradesToUpdate = []
    tradesToCleanup = []
    tradesToAdd = []

    # find trades that should be updated or added to dealpackage
    for dealPackageItem in dealPackageTradeList:
        foundTradeInDealPackage = False

        for existingTrade in dealPackage.Trades():

            if int(dealPackageItem.DealPackageTrade) == existingTrade.Oid():
                tradesToUpdate.append(dealPackageItem)
                foundTradeInDealPackage = True

        if not foundTradeInDealPackage:
            tradesToAdd.append(dealPackageItem)

    # find trades that should be removed from dealPackage
    for existingTrade in dealPackage.Trades():
        foundTradeInDealPackage = False

        for dealPackageItem in dealPackageTradeList:
            if existingTrade.Oid() == int(dealPackageItem.DealPackageTrade):
                foundTradeInDealPackage = True

        if not foundTradeInDealPackage:
            tradesToCleanup.append(existingTrade)

    # Delete trades not included in selection anymore
    for tradeToRemove in tradesToCleanup:
        # Delete trade link
        for tradeLink in dealPackage.TradeLinks():
            if tradeLink.Trade().Oid() == tradeToRemove.Oid():
                tradeLink.Delete()

        # Test if trade is a child trade created by the HedgeEffectiveness Test Suite
        # - Assume that if trade.Text1 is not set to a valid Hedge_Type, then the
        #       was not created by Hedge Eff Testsuite and by implication not a child trade
        #       and should not be voided but only removed from the applicable Deal Packge.
        if tradeToRemove.Text1() and\
                HedgeConstants.Hedge_Trade_Types.test_for_valid_hedge_type(tradeToRemove.Text1()) \
                and tradeToRemove.Text1() != HedgeConstants.Hedge_Trade_Types.Hypo \
                and tradeToRemove.Text1() != HedgeConstants.Hedge_Trade_Types.ZeroBond:

            tradeClone = tradeToRemove.Clone()
            tradeClone.Status('Void')
            tradeToRemove.Apply(tradeClone)
            tradeToRemove.Commit()
        else:
            # call Commit on the trade to make sure the trade is saved to the database
            # with the dealpackageTradeLink removed.
            tradeToRemove.Commit()

    # Add new trades
    for item in tradesToAdd:
        tradeToAdd = acm.FTrade[item.DealPackageTrade]
        if tradeToAdd:
            dealPackage.AddTrade(tradeToAdd)
            tradeToAdd.Commit()

    # Update trades already in deal package
    for item in tradesToUpdate:
        if item.ChildTrade and item.OriginalTrade:

            childTrade = acm.FTrade[item.ChildTrade]
            originalTrade = acm.FTrade[item.OriginalTrade]

            if childTrade and originalTrade:
                HedgeChildTradeUtils.update_child_trade(
                    originalTrade,
                    childTrade,
                    hedgeStartDate,
                    item.HedgeType,
                    item.Percentage
                )

            childTrade.Commit()
    dealPackage.Commit()

    return hedgeTradeList


def delete_instrument_package(name):
    '''Delete a specific instrument package (and Instrument Package with the same name)
    '''

    try:
        instrumentPackage = acm.FInstrumentPackage[name]

        if instrumentPackage:
            # first delete all deal packages linked to the InstrumentPackage
            while instrumentPackage.DealPackages():
                dpToDelete = instrumentPackage.DealPackages()[0]
                dpToDelete.Delete()
            # then delete all references to the InstrumentPackage on the trade level
            trades = acm.FTrade.Select('positionInstrumentPackage = %d' % instrumentPackage.Oid())
            for trade in trades:
                clone = trade.Clone()
                clone.PositionInstrumentPackage(None)
                trade.Apply(clone)
                trade.Commit()

            instrumentPackage.Delete()

        else:
            logger.WLOG('Error deleting Deal Package - %s not found' % name)

    except Exception, ex:
        message = 'Exception deleting Deal Package. Message: %s' % (ex)
        logger.ELOG(message)


class DealPackageTradeItem:

    def __init__(self, dealPackageTrade, childTrade, originalTrade, percentage, hedgeType):
        self.DealPackageTrade = dealPackageTrade
        self.ChildTrade = childTrade
        self.OriginalTrade = originalTrade
        self.Percentage = percentage
        self.HedgeType = hedgeType
