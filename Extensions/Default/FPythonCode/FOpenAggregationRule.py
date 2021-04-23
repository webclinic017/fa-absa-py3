""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/FOpenAggregationRule.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import time
import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FAggGeneral
importlib.reload(FAggGeneral)


def makeGuiParameters(windowCaption):

    guiParameters = {
            'runButtonLabel': '&&Save',
            'hideExtraControls': True,
            'windowCaption': windowCaption
    }
    return guiParameters


### Aggrules Tooltips
ordernbr_tooltip = ('Rule number. Trades are selected in rule number order.  '
        'Trades selected by one rule will not be selected again by another '
        'rule with a greater order number.')
instype_tooltip = ('Trades in instruments of these instrument type(s) are '
        'selected')
instrument_tooltip = 'Trades in these instruments are selected. (Max 400)'
underlyingInstype_tooltip = ('Trades in instruments that are derivatives of '
        'instruments of these instrument types are selected.')
underlying_tooltip = ('Trades in instruments that are derivatives of these '
        'instruments are selected.')
onlyExpired_tooltip = 'Select only trades in expired instruments.'
otc_tooltip = 'Include/Exclude OTC instruments.'
t_g_c_tooltip = ('The selected trades are grouped into several split '
        'positions defined by these criteria.')
portfolio_tooltip = 'Trades in these portfolios are selected.'
counterparty_tooltip = ('Trades with these counterparties are selected.  '
        'Applicable only if Counterparty is selected as Grouping Criteria.')
acquirer_tooltip = ('Trades with this/these acquierer are selected.  '
        'Applicable only if Acquirer is selected as Grouping Criteria.')
excludeHook_tooltip = ('Name of your own python function defined in the AEL '
        'module FBDPHooks.  Extra posibility to exclude trades from the '
        'selection.')
aggregate_tooltip = ('Aggregation rule is active and locked by an '
        'aggregation process.')
open_days_tooltip = ('Trades with trade time <= (today - AggregateOpenDays) '
        'will be aggregated')
periodic_daily_tooltip = ('Number of days back in time, where daily profit '
        'and loss can be viewed for the aggregated positions.')
periodic_monthly_tooltip = ('Number of months back in time, where monthly '
        'profit and loss can be viewed for the aggregated positions.')
periodic_yearly_tooltip = ('Number of years back in time, where yearly '
        'profit and loss can be viewed for the aggregated positions.')
### End of aggrule Tooltips


def insTypes():
    return [typ for typ in acm.FEnumeration['enum(InsType)'].Enumerators()
            if typ and typ != 'None']


def otc_alternatives():
    return ['All',
            'Only OTC',
            'Only Non OTC']


def groupingCriteria():
    return ['Acquirer',
            'Counterparty',
            'Market',
            'Trader',
            'Broker',
            'Trade Currency',
            'Contract Trade',
            'Trade Key 1',
            'Trade Key 2',
            'Trade Key 3',
            'Trade Key 4',
            #'Owner',
            #'Free Text 1',
            #'Free Text 2',
            'Buy/Sell']


class AggRuleVariablesInstance:

    def __init__(self, lock_possible=True):
        self.lock_possible = lock_possible
        self.aggrule_variables = aggrule_default_variables(self, lock_possible)

    def name_cb(self, index, fieldValues):
        """
        this callback is a workaround so that aggregate_cb is called even if
        it is not enabled.  This is neccessary since the state of this
        instance is reused as long as FBDPGui is not reloaded.
        """
        fieldValues = self.aggregation_cb(index, fieldValues)
        return fieldValues

    def grouping_cb(self, index, fieldValues):
        seqNr = self.aggrule_variables.trade_grouping_criteria.sequenceNumber
        grouping = fieldValues[seqNr].upper()
        for gpstr in ['Counterparty', 'Acquirer']:
            enabled = gpstr.upper() in grouping
            getattr(self.aggrule_variables, gpstr).enable(enabled)
        return fieldValues

    def aggregation_cb(self, index, fieldValues):
        lock_time_seq = self.aggrule_variables.lock_time.sequenceNumber
        enabled = (fieldValues[index] == '0')
        for var in self.aggrule_variables:
            if not var.sequenceNumber in [index, lock_time_seq]:
                var.enable(enabled)

        self.aggrule_variables.aggregate.enable(not enabled)
        if enabled:
            fieldValues = (self.aggrule_variables.trade_grouping_criteria.
                    callbackIfEnabled(fieldValues))
            fieldValues[lock_time_seq] = ''
        else:
            seq = self.aggrule_variables.ordernbr.sequenceNumber
            ordernbr = int(fieldValues[seq])
            ar = acm.FAggregationRule.Select('name = {0}'.format(ordernbr))
            if ar:
                fmt = '%Y-%m-%d %H:%M:%S'
                dTime = time.strftime(fmt, time.gmtime(ar[0].UpdateTime()))
                fieldValues[lock_time_seq] = dTime

        return fieldValues


def aggrule_default_variables(inst, lock_possible=True):

    name_cb = inst.name_cb
    grouping_cb = inst.grouping_cb
    aggregation_cb = inst.aggregation_cb

    variables = [
            # [VariableName,
            #       DisplayName,
            #       Type, CandidateValues, Default,
            #       Mandatory, Multiple, Description, InputHook, Enabled]
            ['ordernbr',
                    'Name',
                    'string', None, '01',
                    1, None, ordernbr_tooltip, None],
            ['Portfolio',
                    'Portfolio',
                    'FPhysicalPortfolio', None, None,
                    None, 1, portfolio_tooltip, None, 1],
            ['Instype',
                    'Instype',
                    'string', insTypes(), None,
                    None, 1, instype_tooltip, None, 1],
            ['Instrument',
                    'Instrument',
                    'FInstrument', None, None,
                    None, 1, instrument_tooltip, None, 1],
            ['UnderlyingInstype',
                    'UnderlyingInstype',
                    'string', insTypes(), None,
                    None, 1, underlyingInstype_tooltip, None, 1],
            ['Underlying',
                    'Underlying',
                    'FInstrument', None, None,
                    None, 1, underlying_tooltip, None, 1],
            ['OnlyExpired',
                    'OnlyExpired',
                    'int', ['0', '1'], None,
                    None, None, onlyExpired_tooltip],
            ['OTC',
                    'OTC',
                    'string', otc_alternatives(), otc_alternatives()[0],
                    2, None, otc_tooltip],
            ['open_trade_days',
                    'AggregateOpenDays_Aggregation',
                    'int', None, '0', None,
                    None, open_days_tooltip, None, 1],
            ['aggregate_periodic_daily',
                    'Daily_Aggregation',
                    'int', None, '0',
                    None, None, periodic_daily_tooltip, None, 1],
            ['aggregate_periodic_monthly',
                    'Monthly_Aggregation',
                    'int', None, '0',
                    None, None, periodic_monthly_tooltip, None, 1],
            ['aggregate_periodic_yearly',
                    'Yearly_Aggregation',
                    'int', None, '0',
                    None, None, periodic_yearly_tooltip, None, 1],
            ['trade_grouping_criteria',
                    'GroupingCriteria_Advanced',
                    'string', groupingCriteria(), None,
                    None, 1, t_g_c_tooltip, grouping_cb],
            ['Counterparty',
                    'Counterparty_Advanced',
                    'FCounterParty', None, None,
                    None, 1, counterparty_tooltip, None, 1],
            ['Acquirer',
                    'Acquirer_Advanced',
                    'FInternalDepartment', None, None,
                    None, 1, acquirer_tooltip, None, 1],
            ['exclude_hook',
                    'ExcludeHook_Advanced',
                    'string', None, None,
                    None, None, excludeHook_tooltip, None, 1],
            ['seqnbr',
                    'Oid_hidden',
                    'string', None, None,
                    None, None, '', None, 0]]

    if lock_possible:
        variables.extend([
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['aggregate',
                        'Locked_Advanced',
                        'int', ['0', '1'], 1,
                        None, None, aggregate_tooltip, aggregation_cb],
                ['lock_time',
                        'Locked Time_Advanced',
                        'string', None, '',
                        0, 0, 'tooltip', None, 0]])
        variables[0][8] = name_cb

    parameter = FBDPGui.AelVariables(*variables)
    return parameter


def modifyAggRule(execParam):

    ordernbr = int(execParam['ordernbr'])
    aggRuleOid = int(execParam['seqnbr'])
    origAggRule = acm.FAggregationRule[aggRuleOid]
    aggRule = origAggRule.Clone()
    if aggRule.Fltnbr():
        flt = aggRule.TradeFilter()
        q = FAggGeneral.Query(execParam, flt.FilterCondition())
    else:
        flt = acm.FTradeSelection()
        q = FAggGeneral.Query(execParam)
    aggRule = FAggGeneral.setFields(aggRule, flt, q, execParam)
    origAggRule.Apply(aggRule)
    origAggRule.Commit()
    aggRule.Changed()
    acm.PollDbEvents()
    aggRuleOid = aggRule.Oid()
    FAggGeneral.changeOrderNumber(ordernbr, aggRuleOid)


def copyAggRule(execParam):

    ordernbr = int(execParam['ordernbr'])
    aggRule = acm.FAggregationRule()
    if aggRule.Fltnbr():
        flt = aggRule.TradeFilter()
        q = FAggGeneral.Query(execParam, flt.FilterCondition())
    else:
        flt = acm.FTradeSelection()
        q = FAggGeneral.Query(execParam)
    aggRule = FAggGeneral.setFields(aggRule, flt, q, execParam)
    aggRule.Commit()
    aggRule.Changed()
    acm.PollDbEvents()
    aggRuleOid = aggRule.Oid()
    FAggGeneral.changeOrderNumber(ordernbr, aggRuleOid)


def newAggRule(execParam):

    ordernbr = int(execParam['ordernbr'])
    aggRule = acm.FAggregationRule()
    if aggRule.Fltnbr():
        flt = aggRule.TradeFilter()
        q = FAggGeneral.Query(execParam, flt.FilterCondition())
    else:
        flt = acm.FTradeSelection()
        q = FAggGeneral.Query(execParam)
    aggRule = FAggGeneral.setFields(aggRule, flt, q, execParam)
    aggRule.Commit()
    aggRule.Changed()
    acm.PollDbEvents()
    aggRuleOid = aggRule.Oid()
    FAggGeneral.changeOrderNumber(ordernbr, aggRuleOid)
