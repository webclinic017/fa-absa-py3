""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/trade_rollout/FTradeRolloutPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FTradeRolloutPerform - Module which executes the rollout

DESCRIPTION
    This module executes the Trade rollout procedure based on the
    parameters passed from the script FTradeRollout.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import os
import acm

import FBDPCommon
from FBDPValidation import FBDPValidate
from FBDPCurrentContext import Summary, Logme


def perform_rollout(dictionary):
    rollout = FTradeRolloutPerform()
    rollout.perform(dictionary)
    Summary().log(dictionary)
    Logme()(None, 'FINISH')


def perform_rollout_correct(dictionary):
    rollCorrect = FTradeRolloutPerform()
    rollCorrect.perform(dictionary, True)
    Logme()(None, 'FINISH')


class FTradeRolloutPerform(FBDPValidate):
    def validateValuationParams(self):
        return True

    def perform_rollout(self, dictionary):
        self.perform(dictionary)
        Logme()(None, 'FINISH')

    def perform_rollout_correct(self, dictionary):
        self.perform(dictionary, True)
        Logme()(None, 'FINISH')

    def ReadArguments(self, dictionary, correct):
        if 'date' not in dictionary:
            dictionary['date'] = None
        self.todate = dictionary['date'] and \
                        FBDPCommon.toDate(dictionary['date'])
        self.correct = correct
        self.tradeFilters = []
        if dictionary['useAggRules']:
            aggRuleFilters = dictionary['aggRuleFilters']
            for aggRuleFltNbr in aggRuleFilters:
                tradeSelection = acm.FTradeSelection[aggRuleFltNbr]
                self.tradeFilters.append(tradeSelection)
        else:
            tradeFilterNames = dictionary['tradeFilters']
            for name in tradeFilterNames:
                tf = acm.FTradeSelection[name]
                if tf is None:
                    Logme()('No such tradefilter {0}'.format(name), 'ERROR')
                else:
                    self.tradeFilters.append(tf)
            if not self.tradeFilters:
                # None of the given filter names existed
                raise Exception('No Trade Filters given.')

        self.testMode = dictionary['Testmode']

        self.doFastRollout = dictionary['useBatching']
        self.batchSize = dictionary.get(
            'AsgardBatch', dictionary['maxBatchSize']
        )
        if self.doFastRollout and self.batchSize < 1:
            raise Exception('Batch size must be an integer greater than zero')

        self.toAmba = dictionary['rolloutToAMBA']
        self.toXml = dictionary['rolloutToXML']
        if self.toAmba and self.toXml:
            raise Exception('Cannot export to both XML and AMBA')

        if self.doFastRollout:
            if self.toAmba:
                raise Exception('Cannot export to AMBA if batching rollout')
            elif self.toXml:
                raise Exception('Cannot export to XML if batching rollout')

        self.SetFilepath(dictionary.get('filePath'))
        self.maxRunTime = dictionary.get('maxRunTime', 0)

    def SetFilepath(self, fpath):
        if self.toAmba or self.toXml:
            self.filePath = fpath or ''
            if self.filePath == '':
                raise Exception(
                    'filePath must be specified if backing up to AMBA or XML.'
                )

            directory, filename = os.path.split(self.filePath)
            if self.toXml and (not directory or not filename):
                raise Exception('Missing XML file directory or file name.')

            if not os.path.exists(self.filePath) and directory and \
               not os.path.exists(directory):
                Logme()('Directory {0} does not exist, will be '
                        'created'.format(directory), 'INFO')
                try:
                    os.makedirs(directory)
                except:
                    message = ('Could not create directory {0}, '
                               'exiting.'.format(directory))
                    raise Exception(message)

    def perform(self, dictionary, correct=False):
        self.ReadArguments(dictionary, correct)
        result = acm.RolloutTrades\
        (
            rolloutDate=self.todate,
            tradeFilters=self.tradeFilters,
            ambaFilename=self.filePath if not self.doFastRollout else None,
            testmode=self.testMode,
            doFastRollout=self.doFastRollout,
            batchSize=self.batchSize,
            maxRunTime=self.maxRunTime,
            toXml=self.toXml,
            correct=correct
        )
        self.LogResult(result)

    def LogResult(self, result):
        if result['error']:
            Logme()(result['error'], 'ERROR')
            return

        positions = result['positions']
        for pos in positions:
            insid = pos['instrument']
            prfid = pos['portfolio']
            posRolloutTrades = pos['rollout_trades']

            Logme()('Now handling position ({0}, {1})'.format(insid, prfid),
                    'INFO')
            if pos['error']:
                Logme()(pos['error'], 'ERROR')
            if pos['warning']:
                Logme()(pos['warning'], 'WARNING')
            deletedTradesList = []
            for tResult in posRolloutTrades:
                aggTrade = tResult['trade']
                deletedTrades = tResult['deleted_trades']
                if tResult['error']:
                    Logme()(tResult['error'], 'ERROR')
                    if len(deletedTrades) <= 1:
                        continue
                Logme()('The trades represented by aggregate trade {0} was '
                        'rolled out'.format(aggTrade), 'INFO')
                deletedTradesList.extend(deletedTrades)
            if deletedTradesList:
                Logme()('Following trades were rolled out', 'DEBUG')
            for tradeId in deletedTradesList:
                Logme()(tradeId, 'DEBUG')
            Summary().ok('Trade', 'rolled out', None, len(deletedTradesList))

        return
