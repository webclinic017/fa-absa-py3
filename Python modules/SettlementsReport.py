import acm
import csv
import os
import calendar
import ChorusHierarchy
import at_logging
from at_ael_variables import AelVariableHandler

TODAY = acm.Time().DateToday()
LASTMONTH = acm.Time().DateAdjustPeriod(TODAY, "-1m")
FIRSTOFLASTMONTH = acm.Time().FirstDayOfMonth(LASTMONTH)
year, month, day = FIRSTOFLASTMONTH.split('-')
LASTDAYOFFLASTMONTH = "%s-%s-%s" % (year, month, calendar.monthrange(int(year), int(month))[1])
OUTPUTLOCATION = 'C:\\'
FILENAME = 'SettlementsWithChorusHierarchy_%s-%s' % (year, month)
LOGOUTPUT = True
LOGGER = at_logging.getLogger()



def changeMode(varMode):
    varStartDate = ael_variables.get('start')
    varEndDate = ael_variables.get('end')

    if varMode.value == 'true':
        varStartDate.enabled = False
        varEndDate.enabled = False
    else:
        varStartDate.enabled = True
        varEndDate.enabled = True

ael_variables = AelVariableHandler()

ael_variables.add_bool('lastmonth',
                       label='Generate for last month',
                       default=True,
                       hook=changeMode)

ael_variables.add('start',
                  label='Start date',
                  default=FIRSTOFLASTMONTH,
                  enabled=False,
                  cls='date')

ael_variables.add('end',
                  label='End date',
                  default=LASTDAYOFFLASTMONTH,
                  enabled=False,
                  cls='date')

ael_variables.add_directory('outputLocation',
                            label='Output location',
                            default=OUTPUTLOCATION)


def log(message):
    if LOGOUTPUT:
        LOGGER.info(message)


def getSettlements(startDate, endDate):
    log("Getting settlements from %s to %s" % (startDate, endDate))
    settlements = acm.FSettlement.Select("valueDay>='%s' and valueDay<='%s'" % (startDate, endDate))
    result = [sett.Oid() for sett in settlements]
    return result


def writeOutput(data, outputFile):
    emptyCell = 'N/A'
    if len(data) > 0:
        outputFile = "%s.csv" % outputFile
        outfile = open(outputFile, 'wb')
        writer = csv.writer(outfile, dialect='excel')

        head = ["Settlement", "Parent settlement", "Trade", "Amount", "Currency",
                "Value Day", "Status", "Trans Ref", "Trade Counterparty", "Acquirer",
                "Portfolio", "Instrument Type", "Underlying instrument",
                "Funding InsType", "Counterparty type", "Cashflow type"]
        chorusHeader = ["MasterBookName", "MinorDeskName", "DeskName", "SubProductName"]
        head.extend(chorusHeader)
        writer.writerow(head)

        for row in data:
            formattedRow = [cell if cell else emptyCell for cell in row]
            writer.writerow(formattedRow)
        outfile.close()
        log('Wrote output to %s' % outputFile)
    else:
        log("No data to write.")


def isValid(settlement):
    if settlement.Amount() == 0.0:
        return False
    elif settlement.Status() == "Void":
        return False
    elif settlement.Trade() and (settlement.Trade().Instrument().OpenEnd() == "Terminated"):
        return False
    else:
        return True


def checkIfName(obj):
    return obj.Name() if obj else ''


def getReport(settlements):
    log("Generating report.")
    report = []
    if len(settlements) > 0:
        log("Getting Chorus Hierarchy.")
        chorus = ChorusHierarchy.ChorusDelegate()

        for settlementNumber in settlements:
            settlement = acm.FSettlement[settlementNumber]

            if isValid(settlement):
                trade = settlement.Trade()
                tradeCounterparty = trade.Counterparty() if trade else None
                portfolio = trade.Portfolio() if trade else None
                instype = trade.Instrument().InsType() if trade else None
                underlying = trade.Instrument().Underlying() if trade else None
                settlementCPType = settlement.Counterparty().Type() if settlement.Counterparty() else None
                cashflowType = settlement.CashFlow().CashFlowType() if settlement.CashFlow() else None
                transref = trade.TrxTrade().Name() if trade and trade.TrxTrade() else None
                fundingIns = trade.add_info("Funding Instype") if trade else None
                parentSettlement = settlement.Parent().Oid() if settlement.Parent() else None

                row = [settlementNumber,
                       parentSettlement,
                       checkIfName(trade),
                       settlement.Amount(),
                       checkIfName(settlement.Currency()),
                       settlement.ValueDay(),
                       settlement.Status(),
                       transref,
                       checkIfName(tradeCounterparty),
                       checkIfName(settlement.Acquirer()),
                       checkIfName(portfolio),
                       instype,
                       checkIfName(underlying),
                       fundingIns,
                       settlementCPType,
                       cashflowType,
                       chorus.getMasterbook(portfolio),
                       chorus.getMinordesk(portfolio),
                       chorus.getDesk(portfolio),
                       chorus.getSubproduct(portfolio)]

                report.append(row)

        return report
    else:
        log('No settlements for report.')
        return []


def ael_main(aelDict):
    log("-----START-----")
    if aelDict['lastmonth'] == 1:
        start = FIRSTOFLASTMONTH
        end = LASTDAYOFFLASTMONTH
    else:
        start = aelDict['start']
        end = aelDict['end']
    path = aelDict['outputLocation'].SelectedDirectory().AsString()
    output = os.path.join(path, FILENAME)
    settlements = getSettlements(start, end)
    report = getReport(settlements)
    writeOutput(report, output)
    log("-----DONE-----")
