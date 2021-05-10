"""
Entry point for FA -> Apex integration.

The below jobs gets all the respective objects FX rates, Bond prices,...
from FA and sending them to MQ.

Contact mail group: CIB Africa MAPEX BTB
"""

import acm

from  ApexEntityProcessors import EquityPositionProcessor, BondPositionProcessor, InstrumentProcessor, BondPriceProcessor, \
EquityPriceProcessor, IndexRateProcessor, FXRateProcessor, PositionAmountType

from ApexCollateralUtils import log, process, MessageHandler, positionFilter
import ApexParameters

ael_variables = [
    # Name, Text, Type, Values, Default, Mandatory, Multi, Tip, Callable, Enabled
    ('date', 'Date', 'string', None, None, 0, 0, 'Date', None, 1),
    (
        'command', 'Command', 'string',
        [
            'SEND_FX_RATE_MESSAGES', 'SEND_INDEX_RATE_MESSAGES',
            'SEND_BOND_PRICE_MESSAGES', 'SEND_EQUITY_PRICE_MESSAGES',
            'SEND_BOND_INSTRUMENT_MESSAGES', 'SEND_EQUITY_INSTRUMENT_MESSAGES',
            'SEND_BOND_POSITION_MESSAGES', 'SEND_EQUITY_POSITION_MESSAGES'
        ],
        None, 0, 0, 'Command', None, 1
    ),
]

Params = ApexParameters.load()

commandToQueueMap = {
    'SEND_FX_RATE_MESSAGES': Params.FXRateQueueName,
    'SEND_INDEX_RATE_MESSAGES': Params.IndexRateQueueName,
    'SEND_BOND_PRICE_MESSAGES': Params.BondPriceQueueName,
    'SEND_EQUITY_PRICE_MESSAGES': Params.EquityPriceQueueName,
    'SEND_BOND_INSTRUMENT_MESSAGES': Params.BondSecurityQueueName,
    'SEND_EQUITY_INSTRUMENT_MESSAGES': Params.EquitySecurityQueueName,
    'SEND_BOND_POSITION_MESSAGES': Params.BondPositionQueueName,
    'SEND_EQUITY_POSITION_MESSAGES': Params.EquityPositionQueueName,
}

def getMessageHandler(command):
    return MessageHandler(commandToQueueMap[command])

def ael_main(dictionary):
    log(acm.TaskParameters())
    if acm.TaskParameters().Size() < 0:
        log("TaskParameters: %s" % acm.TaskParameters())
        dictionary = acm.TaskParameters()['taskParameters']
    else:
        log("Dict: %s" % dictionary)

    date = dictionary['date']
    if date == "":
        cal = acm.FCalendar[Params.DefaultCalendar]
        date = cal.AdjustBankingDays(acm.Time.DateNow(), -1)

    log("Running for: %s" % date)
    command = dictionary['command']
    log("command: %s" % command)

    with getMessageHandler(command) as messageHandler:

        if command == 'SEND_FX_RATE_MESSAGES':
            process(
                Params.CollateralCurrenciesStoredQuery, date,
                FXRateProcessor(messageHandler)
            )
        if command == 'SEND_INDEX_RATE_MESSAGES':
            process(
                Params.CollateralRateIndicesStoredQuery, date,
                IndexRateProcessor(messageHandler)
            )
        if command == 'SEND_BOND_PRICE_MESSAGES':
            with BondPriceProcessor(messageHandler) as processor:
                process(Params.CollateralBondInstrumentsStoredQuery, date, processor)

        if command == 'SEND_EQUITY_PRICE_MESSAGES':
            process(
                Params.CollateralEquityInstrumentsStoredQuery, date,
                EquityPriceProcessor(messageHandler)
            )
        if command == 'SEND_BOND_INSTRUMENT_MESSAGES':
            process(
                Params.CollateralBondInstrumentsStoredQuery, date,
                InstrumentProcessor(messageHandler)
            )
        if command == 'SEND_EQUITY_INSTRUMENT_MESSAGES':
            process(
                Params.CollateralEquityInstrumentsStoredQuery, date,
                InstrumentProcessor(messageHandler)
            )
        if command == 'SEND_BOND_POSITION_MESSAGES':
            process(
                Params.CollateralBondInventoryTradesStoredQuery, date,
                BondPositionProcessor(messageHandler, PositionAmountType.Balance), positionFilter
            )
        if command == 'SEND_EQUITY_POSITION_MESSAGES':
            process(
                Params.CollateralEquityInventoryTradesStoredQuery, date,
                EquityPositionProcessor(messageHandler, PositionAmountType.Balance), positionFilter
            )

def StartDialog(eii):
    context = acm.GetDefaultContext()
    acm.RunModuleWithParameters("ApexCollateral", context)
