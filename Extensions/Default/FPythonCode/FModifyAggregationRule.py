""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/FModifyAggregationRule.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import FOpenAggregationRule
import importlib
importlib.reload(FOpenAggregationRule)


ael_gui_parameters = FOpenAggregationRule.makeGuiParameters(
        windowCaption='Modify Aggregation Rule')


ael_variables = FOpenAggregationRule.AggRuleVariablesInstance(
        lock_possible=True).aggrule_variables


def ael_main(execParam):

    FOpenAggregationRule.modifyAggRule(execParam)
