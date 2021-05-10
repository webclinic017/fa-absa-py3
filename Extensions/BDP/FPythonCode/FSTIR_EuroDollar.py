""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/futures_maintenance/FSTIR_EuroDollar.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
#
#Euro dollar definition
#
#This file is stored as a python extension but is not python based
#
#The file format is
#
# <key> = <value>
#
#Spaces inside key and value are kept, surrounding spaces are stripped.
#The format also recognizes # as start of a remark
#

#
#The names here are the internal GUI field names
# Each entry will set a variable in the GUI parameter
#

PageDefBase = IRD
ISIN ID = ED
Strip Length= 10y
Rolling Period=3m
Expiry Day Rule=IMM
Reference Day= 0d
Quote Type = 100-rate
# You can specify the reference instrument if needed
# or if only one instrument exits in a pagelits that will be selected
#Reference Instrument = CHF/CAP/LI/10Y/1.00


LogLevel = Info
#LogEnabled = 1

