""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPChartData.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import collections
import acm

CHART_TYPE_PIE = 'Pie'
CHART_TYPE_RING = 'Ring'


CHART_TYPE_BAR = 'Bar'
CHART_TYPE_PLOT = 'Plot'
CHART_TYPE_STEPLINE = 'StepLine'


VALID_PIE_CHART_TYPES = (CHART_TYPE_PIE, CHART_TYPE_RING)
VALID_2D_CHART_TYPES = (CHART_TYPE_BAR, CHART_TYPE_PLOT, CHART_TYPE_STEPLINE)


_FCOLOR_RED = acm.UX().Colors().Create(255, 0, 0)
_FCOLOR_GREEN = acm.UX().Colors().Create(0, 255, 0)
_FCOLOR_BLUE = acm.UX().Colors().Create(0, 0, 255)
_FCOLOR_BLACK = acm.UX().Colors().Create(0, 0, 0)


seriesData = collections.namedtuple('seriesData',
        ['name', 'color', 'xList', 'yList'])

UIData = collections.namedtuple('UIData', ['seriesList', 'XAxisLabel', 'YAxisLabel',
        'subTitle', 'chartType', 'viewLabel'])
