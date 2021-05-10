""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSPayoffGraphPanel.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSPayoffGraphPanel

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
from FCalculatedValueGraphPanel import CalculatedValueGraphPanel
import FCTSPayoffPlotter

class CTSPayoffGraphPanel(CalculatedValueGraphPanel):

    def PlotterCollection(self):
        return FCTSPayoffPlotter.Plot.Plotters()
