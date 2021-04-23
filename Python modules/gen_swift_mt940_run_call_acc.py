"""-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Runs SWIFT MT940 messages on Call Accounts
DEPATMENT AND DESK      :
REQUESTER               :
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date            Change no            Developer                 Description
--------------------------------------------------------------------------------
2011-03-25      XXXXXX               Francois Truter           Initial Implementation
2011-06-30      XXXXXX               Rohan van der Walt        Change to only select call account trade from Reporting portfolio
2011-07-07      707904               Rohan van der Walt        Generalise Call Account locating query folder
2013-03-08      857456               Peter Basista             Remove _getCallAccounts function
                                                               and use the one from the
                                                               PS_Functions module
                                                               (getCallAccounts function).
2015-09-02      CHNG0003153228       Lawrence Mucheka          Call to place message directly on MQ
2016-02-05      CHNG0003427057       Gabriel Marko             MT940 Recipient loaded from MT940RecipientBIC PartyAlias
2016-02-29      CHNG0003480353       Gabriel Marko             Refactoring: WriteCallAccountMt940ToQueue moved
2016-10-31      CHNG0004075040      Gabriel Marko             Fix 28C tag logic - increment daily.
"""

import acm
import gen_swift_mt940


from gen_ael_variables_date_param import (
    DateParameter,
    DateEnum
)

import FOperationsUtils as Utils
import gen_mq
import pymqi


ALL_PARTIES = 'All Parties set up for MT940'


def _getPartyFromAddInfo(addInfo):
    additionalInfos = acm.FAdditionalInfo.Select("addInf = '%s'" % addInfo)
    return set(additionalInfo.Recaddr()
               for additionalInfo in additionalInfos)


def _getPartyFromAlias(alias):
    aliases = acm.FPartyAlias.Select(
        "type= '%s'" % gen_swift_mt940.MT940BICALIAS
    )
    return set(alias.Party().Oid() for alias in aliases)


def _getPartyList():
    print('Loading parties...')

    mt940Recipients = _getPartyFromAlias('MT940Recipient')
    busEntity = _getPartyFromAddInfo('MeridianSwiftBusEnt')
    parties = mt940Recipients & busEntity

    partyNames = []
    for addr in parties:
        party = acm.FParty[addr]
        if party:
            partyNames.append(party.Name())

    partyNames.sort()
    partyNames.insert(0, ALL_PARTIES)
    return partyNames


def getCallAccounts(counterparty):
    query = acm.CreateFASQLQuery('FTrade', 'AND')

    query.AddAttrNode(
        'Counterparty.Oid',
        'EQUAL',
        counterparty.Oid()
    )

    query.AddAttrNode(
        'Instrument.InsType',
        'EQUAL',
        acm.EnumFromString('InsType', 'Deposit')
    )

    query.AddAttrNode(
        'Instrument.OpenEnd',
        'EQUAL',
        acm.EnumFromString('OpenEndStatus', 'Open End')
    )

    # Exclude 'Void', 'Confirmed Void', 'Simulated', 'Terminated' trades
    for status in ['Void', 'Confirmed Void', 'Simulated', 'Terminated']:
        query.AddAttrNode(
            'Status',
            'NOT_EQUAL',
            acm.EnumFromString('TradeStatus', status)
        )

    callAccounts = list(set(trade.Instrument() for trade in query.Select()))

    return callAccounts


def WriteCallAccountMt940ToQueue(account, startDate, endDate, onlyIfTransactions):

    statement_number = gen_swift_mt940.get_next_statement_number(account, endDate)
    if statement_number is None:
        gen_swift_mt940.set_next_statement_number(account, endDate, 0)
        statement_number = gen_swift_mt940.get_next_statement_number(account, endDate)

    statement_number += 1

    result = gen_swift_mt940.GetRawMessage(
        account,
        startDate,
        endDate,
        statement_number,
        onlyIfTransactions
    )

    if not result:
        return False

    message = str(result[1])

    try:
        # Place on MQ
        mq_mess = gen_mq.MqMessenger('MeridianOutMq')
        mq_mess.Put(message)
    except Exception as ex:
        Utils.Log(True, "Could not place swift message on MQ\nError:%s" % ex)
        return False

    # Log result
    Utils.Log(True, '--------------------------------Start Message--------------------------------')
    Utils.Log(True, message)
    Utils.Log(True, '---------------------------------End Message---------------------------------')
    Utils.Log(True, 'Message queued...')

    # Increment statement number
    try:
        gen_swift_mt940.set_next_statement_number(
            account,
            endDate,
            statement_number
        )
    except Exception as ex:
        Utils.Log(True, "Could not increment the statement number\nError:%s" % ex)
        return False

    return True


# AEL parameters and variables

PARTY_KEY = 'PARTY'
PARTY_LIST = _getPartyList()

START_DATE_KEY = 'START_DATE'
END_DATE_KEY = 'END_DATE_KEY'
ONLY_IF_TRANSACTIONS_KEY = 'ONLY_IF_TRANSACTIONS'

boolDict = {'Yes': True, 'No': False}
boolDictDisplay = sorted(boolDict.keys())

ael_gui_parameters = {
    'windowCaption': 'Run Daily SWIFT MT940 statements for Call Accounts'
}


# Variable Name, Display Name, Type, Candidate Values,
# Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [
        PARTY_KEY,
        'Parties',
        'string',
        PARTY_LIST,
        ALL_PARTIES,
        1,
        1,
        'The parties for whom MT940 statements should be sent. Note that the additional infos MeridianSwiftBusEnt and MT940Recipient must be completed on the client.',
        None,
        1
    ],
    [
        ONLY_IF_TRANSACTIONS_KEY,
        'Only send if there were transactions',
        'string',
        boolDictDisplay,
        'Yes',
        1,
        0,
        'Should a statement only be sent if there were transactions?',
        None,
        1
    ]
]

startDateParemeter = DateParameter.AddParameter(
    ael_variables,
    1,
    'START_DATE',
    'Start Date',
    DateEnum.Unselected,
    False,
    'Start date of statement. Could be left out for daily statement.'
)

endDateParemeter = DateParameter.AddParameter(
    ael_variables,
    3,
    'END_DATE',
    'End Date',
    DateEnum.Today,
    True,
    'End date of statement.'
)


def ael_main(parameters):
    try:

        startDate = startDateParemeter.GetAcmDate(parameters)
        endDate = endDateParemeter.GetAcmDate(parameters)

        onlyIfTransactions = boolDict[parameters[ONLY_IF_TRANSACTIONS_KEY]]
        selectedPartyNames = parameters[PARTY_KEY]

        if ALL_PARTIES in selectedPartyNames:
            selectedPartyNames = PARTY_LIST[:]
            selectedPartyNames.remove(ALL_PARTIES)

        for name in selectedPartyNames:
            party = acm.FParty[name]

            if not party:
                raise Exception('Could not load party [%s].' % name)

            callAccounts = getCallAccounts(party)

            messagesSent = 0
            for account in callAccounts:
                try:
                    if WriteCallAccountMt940ToQueue(account, startDate, endDate, onlyIfTransactions):
                        messagesSent += 1
                except Exception as ex:
                    print('An exception occurred while running the MT940 statment for %s, account %s: %s' % (party.Name(), account.Name(), ex))

            if callAccounts:
                print('%i account(s) processed for %s and %i statement message(s) sent' % (len(callAccounts), party.Name(), messagesSent))
            else:
                print('no call accounts found for %s' % party.Name())

        if not selectedPartyNames:
            print('no parties found to send statement messages to')

    except Exception as ex:
        print('An exception occurred while running the script: %s ' % ex)
    else:
        print('The script completed successfully')
