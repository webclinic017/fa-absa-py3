""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/bdp_dashboard/FBDPDashboardData.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import collections


CHART_TYPE_PIE = 'Pie'
CHART_TYPE_RING = 'Ring'


CHART_TYPE_BAR = 'Bar'
CHART_TYPE_PLOT = 'Plot'
CHART_TYPE_STEPLINE = 'StepLine'


VALID_PIE_CHART_TYPES = (CHART_TYPE_PIE, CHART_TYPE_RING)
VALID_2D_CHART_TYPES = (CHART_TYPE_BAR, CHART_TYPE_PLOT, CHART_TYPE_STEPLINE)


ResultData = collections.namedtuple('ResultData',
        ['categoryName', 'count', 'threshold', 'recommendedActions'])


ConfigData = collections.namedtuple('ConfigData',
        ['name', 'description', 'actionDescription'])


UIData = collections.namedtuple('UIData', ['resultDataList', 'configDataList',
        'XAxisLabel', 'YAxisLabel', 'subTitle', 'chartType', 'viewType',
        'viewLevelNum', 'viewLabel'])
