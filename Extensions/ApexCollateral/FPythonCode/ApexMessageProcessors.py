import acm
from datetime import datetime
from time import time
from xml.etree import ElementTree
from ApexCollateralUtils import log, getCounterparty, setAddInfo, handleException, captureMetrics, adjustDeposit, FunctionalError
import ApexParameters
import traceback
import at_addInfo

Params = ApexParameters.load()

class TradeType:
    SecurityCollateralReceive = "3"
    SecurityCollateralDeliver = "4"
    CashCollateralReceive = "20"
    CashCollateralDeliver = "21"


class TradeEventFunction:
    Opening = "1"
    PartialReturn = "2"
    Closing = "3"
    PartialIncrease = "8"


class AccrualType:
    Fee = "1"
    Claim = "2"
    Interest = "3"


class BillingItemDirection:
    Receivable = "1"
    Payable = "2"


def processTradeActivityQueueMessage(message):
    try:
        root = ElementTree.fromstring(message)

        isValid = root.find("IsValid").text
        if (isValid != 'true'):
            return

        messageType = root.find("MessageType").text

        if (messageType == "TradeActivity"):
            processTradeActivityMessage(message)
        elif (messageType == "BillingItem"):
            processBillingItemMessage(message)
        elif (messageType == "TradeExposureCSAFlag"):
            processTradeExposureCSAFlag(message)
        else:
            raise Exception("Unsupported message type %s" % messageType)

    except Exception as e:
        traceback.print_exc()
        handleException(
            "Error processing billing item message", e,
            traceback.format_exc(), []
        )


def processTradeExposureCSAFlag(message):
    logMessages = []
    try:
        start_time = datetime.fromtimestamp(time())
        log(
            "Received trade exposure CSA flag message at %s" % acm.Time.TimeNow(),
            logMessages
        )

        root = ElementTree.fromstring(message)

        tradeId = root.find("TradeID").text
        sourceName = root.find("SourceName").text

        if sourceName.lower() != "frontarena":
            log("%s? Not interested." % sourceName, logMessages)
            return

        trade = acm.FTrade[tradeId]

        if not trade:
            raise Exception("Unable to find trade %s in FA." % tradeId)

        if trade.Aggregate() == 2:
            log("%s is an aggregate, we will not set the flag for it." % tradeId, logMessages)
            return
        if trade.IsFxSwap():
            #Bug that needs to be fixed by FA team
            log("%s is an FX Swap, we will not set the flag for it." % tradeId, logMessages)
            return
        if (at_addInfo.get_value(trade, 'CSA Trade') == 'Yes'):
            log("AddInfo %s for trade %s already set and will not be updated." % ('CSA Trade', tradeId), logMessages)
            return

        #at_addInfo.save(trade, 'CSA Trade', 'Yes')
        trade.AdditionalInfo().CSA_Trade('Yes')
        trade.Commit()
        log("AddInfo %s for trade %s added/updated." % ('CSA Trade', tradeId), logMessages)

        end_time = datetime.fromtimestamp(time())
        captureMetrics(end_time - start_time, True, tradeId)
    except Exception as e:
        traceback.print_exc()
        handleException(
            "Error processing trade exposure CSA flag message", e,
            traceback.format_exc(), logMessages
        )
        log(message)

def processBillingItemMessage(message):
    logMessages = []
    try:
        start_time = datetime.fromtimestamp(time())
        log(
            "Received billing item message at %s" % acm.Time.TimeNow(),
            logMessages
        )

        root = ElementTree.fromstring(message)
        direction = 0
        externalReference = None

        billingItemId = root.find("BillingItemID").text
        log("billingItemId: %s" % billingItemId, logMessages)
        valueDate = root.find("ValueDate").text
        log("valueDate: %s" % valueDate, logMessages)
        amount = float(root.find("Amount").text)
        log("amount: %s" % amount, logMessages)
        directionType = root.find("Direction").text
        log("directionType: %s" % directionType, logMessages)
        accrualType = root.find("AccrualType").text
        log("accrualType: %s" % accrualType, logMessages)
        accountNumber = root.find("AccountNumber").text
        log("accountNumber: %s" % accountNumber, logMessages)

        if accrualType == AccrualType.Fee:
            externalReference = "Fee"
        if accrualType == AccrualType.Claim:
            externalReference = "Claim"
        if accrualType == AccrualType.Interest:
            externalReference = "Interest"

        externalReference = (
            externalReference + Params.ExternalReferenceDelimiter +
            billingItemId
        )
        log("externalReference: %s" % externalReference, logMessages)

        if directionType == BillingItemDirection.Receivable:
            direction = 1
        if directionType == BillingItemDirection.Payable:
            direction = -1

        processedTrade = adjustDeposit(
            accountNumber, valueDate, direction, amount,
            externalReference, logMessages
        )

        end_time = datetime.fromtimestamp(time())
        duration = end_time - start_time
        captureMetrics(duration, True, billingItemId)

        if processedTrade is not None:
            return processedTrade.Oid()

    except Exception as e:
        traceback.print_exc()
        handleException(
            "Error processing billing item message", e,
            traceback.format_exc(), logMessages
        )
        log(message)


def processTradeActivityMessage(message):
    logMessages = []
    try:
        start_time = datetime.fromtimestamp(time())
        log(
            "Received trade activity message at %s" % acm.Time.TimeNow(),
            logMessages
        )
        root = ElementTree.fromstring(message)
        direction = 0
        externalReference = None

        tradeType = root.find("TradeType").text
        log("tradeType: %s" % tradeType)
        tradeEventType = root.find("TradeEventType").text
        log("tradeEventType: %s" % tradeEventType)
        tradeEventFunction = root.find("TradeEventFunction").text
        log("tradeEventFunction: %s" % tradeEventFunction)
        accountNumber = root.find("AccountNumber").text
        log("AccountNumber: %s" % accountNumber, logMessages)

        if tradeType not in [
            TradeType.SecurityCollateralReceive,
            TradeType.SecurityCollateralDeliver,
            TradeType.CashCollateralReceive,
            TradeType.CashCollateralDeliver
         ]:
            log("Unsupported trade type: %s" % tradeType, logMessages)            
            raise FunctionalError(logMessages[-1])
        if tradeType == TradeType.SecurityCollateralReceive:
            log("TradeType: Security Collateral Receive", logMessages)
            direction = 1
        if tradeType == TradeType.SecurityCollateralDeliver:
            log("TradeType: Security Collateral Deliver", logMessages)
            direction = -1
        if tradeType == TradeType.CashCollateralReceive:
            log("TradeType: Cash Collateral Receive", logMessages)
            direction = 1
        if tradeType == TradeType.CashCollateralDeliver:
            log("TradeType: Cash Collateral Deliver", logMessages)
            direction = -1

        if tradeEventFunction not in [
            TradeEventFunction.Opening,
            TradeEventFunction.PartialReturn,
            TradeEventFunction.Closing,
            TradeEventFunction.PartialIncrease
        ]:
            log("Unsupported trade event function: %s" % tradeEventFunction)            
            raise FunctionalError(logMessages[-1])
        if tradeEventFunction == TradeEventFunction.Opening:
            log("TradeEventFunction: Opening", logMessages)
            direction = direction * 1
            externalReference = "Opening"
        if tradeEventFunction == TradeEventFunction.PartialReturn:
            log("TradeEventFunction: Partial Return", logMessages)
            direction = direction * -1
            externalReference = "PartialReturn"
        if tradeEventFunction == TradeEventFunction.Closing:
            log("TradeEventFunction: Closing", logMessages)
            direction = direction * -1
            externalReference = "Closing"
        if tradeEventFunction == TradeEventFunction.PartialIncrease:
            log("TradeEventFunction: Partial Increase", logMessages)
            direction = direction * 1
            externalReference = "PartialIncrease"

        reversal = root.find("Reversal").text
        if reversal == '1':
            log("Reversal", logMessages)
            direction = direction * -1
            externalReference = "Reversal"

        tradeId = root.find("TradeID").text
        log("TradeID: %s" % tradeId, logMessages)
        eventId = root.find("EventID").text
        log("EventID: %s" % eventId, logMessages)
        tradeDate = root.find("TradeDate").text
        log("TradeDate: %s" % tradeDate, logMessages)
        valueDate = root.find("ValueDate").text
        log("ValueDate: %s" % valueDate, logMessages)
        startDate = root.find("StartDate").text
        log("StartDate: %s" % startDate, logMessages)
        eventDate = root.find("EventDate").text
        log("EventDate: %s" % eventDate, logMessages)
        quantity = float(root.find("Quantity").text)
        currency = root.find("TradeCurrency").text
        user = root.find("User").text
        log("User: %s" % user, logMessages)
        agreement = root.find("Agreement").text
        log("Agreement: %s" % agreement, logMessages)
        counterpartySDSID = root.find("Counterparty").text
        reversal = root.find("Reversal").text
        securityIndentifier = root.find("SecurityIndentifier").text


        externalReference = (
            externalReference + Params.ExternalReferenceDelimiter + eventId
        )
        log("ExternalReference: %s" % externalReference, logMessages)

        curr = acm.FCurrency[currency]

        processedTrade = None
        if tradeType in [
            TradeType.SecurityCollateralReceive,
            TradeType.SecurityCollateralDeliver
        ]:
            log("Security Collateral")
            portfolio = acm.FPhysicalPortfolio[
                Params.SecurityCollateralPortfolio
            ]
            acquirer = acm.FParty[Params.SecurityCollateralAcquirer]
            trader = acm.FUser[Params.SecurityCollateralTrader]
            counterparty = getCounterparty(counterpartySDSID)

            if portfolio is None:
                log(
                    "Security Portfolio: %s not found" %
                    Params.SecurityCollateralPortfolio, logMessages
                )
            else:
                log("Security Portfolio: %s" % portfolio.Name(), logMessages)
            if acquirer is None:
                log(
                    "Acquirer: %s not found" %
                    Params.SecurityCollateralAcquirer, logMessages
                )
            else:
                log("Acquirer: %s" % acquirer.Name(), logMessages)
            if trader is None:
                log(
                    "Trader: %s not found" % Params.SecurityCollateralTrader,
                    logMessages
                )
            else:
                log("Trader: %s" % trader.Name(), logMessages)
            if counterparty is None:
                log(
                    (
                        "Cannot find unique counterparty for SDSID: %s, check"
                        " that a party exists in Front Arena with the relevant"
                        " SDSID AddInfo fields and that there are not parties"
                        " with duplicate SDSIDs"
                    ) % counterpartySDSID, logMessages
                )
            else:
                log("Counterparty: %s" % counterparty.Name(), logMessages)

            if (portfolio is None or acquirer is None or trader is None or
                    counterparty is None):                
                raise FunctionalError(logMessages[-1])

            result = acm.FInstrument.Select(
                "isin = '%s'" % securityIndentifier
            )

            if len(result) != 1:
                log(
                    "Cannot find instrument with ISIN %s" %
                    securityIndentifier, logMessages
                )                
                raise FunctionalError(logMessages[-1])
            else:
                ins = result[0]

                log("Creating security trade for %s" % ins.Name(), logMessages)
                trade = acm.FTrade()
                trade.Portfolio(portfolio)
                trade.Instrument(ins)
                trade.Counterparty(counterparty)
                trade.Acquirer(acquirer)
                trade.Quantity(direction * abs(quantity) / ins.ContractSize())
                trade.Price(ins.used_price())
                trade.ValueDay(valueDate)
                trade.AcquireDay(valueDate)
                trade.TradeTime(eventDate)
                trade.Currency(curr)
                trade.Status(Params.SecurityCollateralTradeStatus)
                trade.Trader(trader)
                trade.TradeCategory("Collateral")
                trade.Text1(externalReference)
                trade.Commit()
                log("Security trade created: %s" % trade.Oid(), logMessages)
                print trade
                processedTrade = trade

        if tradeType in [
            TradeType.CashCollateralReceive,
            TradeType.CashCollateralDeliver
        ]:
            log("Cash Collateral")
            processedTrade = adjustDeposit(
                accountNumber, valueDate, direction, quantity,
                externalReference, logMessages
            )

        end_time = datetime.fromtimestamp(time())
        duration = end_time - start_time
        captureMetrics(duration, True, eventId)
        if processedTrade is not None:
            return processedTrade.Oid()

    except Exception as e:
        traceback.print_exc()
        log(message)
        handleException(
            "Error processing trade activity message", e,
            traceback.format_exc(), logMessages
        )
        


def processCsaAgreementItemMessage(message):
    logMessages = []
    try:
        log("Recieved CSA Agreement item message at %s" % acm.Time.TimeNow())        
        root = ElementTree.fromstring(message)
        Counterparty = None

        agreementType = root.find("AgreementType").text
        active = root.find("IsActive").text

        id = root.find("AgreementId").text
        internalId = root.find("AgreementInternalId").text

        if(agreementType.lower() != 'isda csa'):
            log('Agreement Id ' + id + ' is not a csa agreement and will not be proceesed [Apex ID-' + internalId + ']')
            return
        if(active != '1'):
            log('Agreement Id ' + id + ' is not active will not be proceesed [Apex ID-' + internalId + ']')
            return

        counterpartySDSID = root.find("CounterpartyExternalKey").text
        log("counterpartySDSID: %s" % counterpartySDSID)
        csaCollateralCurrency = root.find("CollateralCurrency").text
        log("CSA Collateral Curr: %s" % csaCollateralCurrency)
        csaType = root.find("CsaRating").text
        log("CSA Type: %s" % csaType)

        Counterparty = getCounterparty(counterpartySDSID)
        log("SDS: %s" % counterpartySDSID)
        if Counterparty:
            log('Updating add infos of agreement ' + id + ' [internal_id: ' + internalId + ']')
            #Upgrade 2017 - add info commit validation changed
            Counterparty.AdditionalInfo().CSA('Yes')
            Counterparty.AdditionalInfo().CSA_Type(csaType)
            Counterparty.AdditionalInfo().CSA_Collateral_Curr(csaCollateralCurrency)
            Counterparty.AdditionalInfo().CSA_Name(id)
            Counterparty.Commit()
            #at_addInfo.save(Counterparty, 'CSA', 'Yes')
            #at_addInfo.save_or_delete(Counterparty, 'CSA Type', csaType)
            #at_addInfo.save_or_delete(Counterparty, 'CSA Collateral Curr', csaCollateralCurrency)
            #at_addInfo.save_or_delete(Counterparty, 'CSA Name', id)
            log('Successfully updated add infos of agreement ' + id + ' [internal_id: ' + internalId + ']')
        else:
            log("Counterparty: %s, could not be found. No Changes committed." % counterpartySDSID)
        return Counterparty

    except Exception as e:
        traceback.print_exc()
        log(message)
        handleException(
            "Error processing CSA Agreement item message", e,
            traceback.format_exc(), logMessages
        )
