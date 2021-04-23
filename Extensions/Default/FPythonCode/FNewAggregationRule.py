""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/FNewAggregationRule.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import FOpenAggregationRule
import importlib
importlib.reload(FOpenAggregationRule)


ael_gui_parameters = FOpenAggregationRule.makeGuiParameters(
        windowCaption='New Aggregation Rule')


ael_variables = FOpenAggregationRule.AggRuleVariablesInstance(
        lock_possible=False).aggrule_variables


def ael_main(execParam):

    FOpenAggregationRule.newAggRule(execParam)
