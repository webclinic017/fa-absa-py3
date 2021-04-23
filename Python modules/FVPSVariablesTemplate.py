""" VPS:1.0.0 """

"""----------------------------------------------------------------------------
MODULE
    FVPSVariables - Module with variables needed by the FVPSExecute script.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    In this module are some VPS variables that can be chosen by 
    the customer.
    
NOTE
    Please rename the module to FVPSVariables
    
    
----------------------------------------------------------------------------"""
import ael

# Defines the selection of  yield curves to be stored
# YieldCurveBase = 0 - No yield curves will be stored
# YieldCurveBase = 1 - All live yield curves will be stored  
# YieldCurveBase = 2 - All yield curves defined in FMTMVariables in the
#                      YieldCurves python list will be stored.
YieldCurveBase = 1
# YieldCurveInclusions - A list of yield curves that should be stored.
#                        If YieldCurveBase = 1 this option will be ignored
YieldCurveInclusions = []
# YieldCurveExclusions - A list of yield curves that should not be stored.
#                        If YieldCurveBase = 0 this option will be ignored.
YieldCurveExclusions = []

# Defines the selection of volatilities to be stored
# VolatilityBase = 0 - No volatilities will be stored
# VolatilityBase = 1 - All live volatilities will be stored  
# VolatilityBase = 2 - All volatilities defined in FMTMVariables in the
#                      VolSurfaces python list will be stored.
VolatilityBase = 1
# VolatilityInclusions - A list of volatilities that should be stored.
#                        If VolatilityBase = 1 this option will be ignored
VolatilityInclusions = []
# VolatilityExclusions - A list of volatilities that should not be stored.
#                        If VolatilityBase = 0 this option will be ignored.
VolatilityExclusions = []
# VolatilityIncludeWithSuffix - 1 or 0.
#                               If 1, volatilities with a suffix defined in
#                               FMtMVariables will be included. Otherwise
#                               they will be excluded.
VolatilityIncludeWithSuffix = 1

# Defines the selection of instruments of type equity index
# for which combination links should be stored.
# CombinationLinkBase = 0 - No combination links will be stored
# CombinationLinkBase = 1 - Combination links for all equity indices will be stored
CombinationLinkBase = 1
# CombinationLinkInclusions - A list of instruments that should be stored.
#                             If CombinationLinkBase = 1 this option will be ignored
CombinationLinkInclusions = []
# CombinationLinkExclusions - A list of instruments that should not be stored.
#                             If CombinationLinkBase = 0 this option will be ignored
CombinationLinkExclusions = []


# Defines the selection of correlation matrices to be stored
# CorrelationMatrixBase = 0 - No correlations will be stored
# CombinationMatrixBase = 1 - All correlations will be stored 
CorrelationMatrixBase = 1
# The below two arguments are the same as for CombinationLinks
CorrelationMatrixInclusions = []
CorrelationMatrixExclusions = []

# Defines the selection of instruments for which
# ratings should be stored
# InstrumentCreditHistoryBase = 0 - No ratings will be stored
# InstrumentCreditHistoryBase = 1 - Ratings for all instruments with instype
#                                   defined below will be stored
InstrumentCreditHistoryBase = 1
# InstrumentCreditHistoryInclusions
# - A list of instruments for which ratings should be stored. 
# If InstrumentCreditHistoryBase = 1 this option will be ignored.
InstrumentCreditHistoryInclusions = []
# InstrumentCreditHistoryExclusions
# - A list of instruments for which ratings should not be stored.
# If InstrumentCreditHistoryBase = 0 this option will be ignored
InstrumentCreditHistoryExclusions = []
# InstrumentCreditHistoryIncludeInstype
# - A list of instrument types for which ratings should be stored.
InstrumentCreditHistoryIncludeInstype = ['Bond', 'Zero']
# InstrumentCreditHistoryExcludeInstype
# - A list of instrument types for which ratings should not be stored
InstrumentCreditHistoryExcludeInstype = []

# Defines the selection of parties for which
# credit events should be stored
# PartyCreditHistoryBase = 0 - No credit events will be stored
# PartyCreditHistoryBase = 1 - Credit events for all parties will be stored
PartyCreditHistoryBase = 1
PartyCreditHistoryInclusions = []
PartyCreditHistoryExclusions = []


# Defines the selection of dividend streams that should be stored
# DividendStreamBase = 0 - No dividend streams will be stored
# DividendStreamBase = 1 - All dividend streams will be stored
DividendStreamBase = 1
DividendStreamInclusions = []
DividendStreamExclusions = []

# LOG HANDLING:

# Name of this script used in START, STOP and FINISH messages:

ScriptName = 'ValuationParameterStorage'

# Specify how extensive logging you desire:

#LogMode = 0	    	#Messages of type: START, STOP, WARNING, ERROR
LogMode = 1	    	#Messages of type: START, STOP, WARNING, ERROR, INFO 
#LogMode = 2 	    	#Messages of type: START, STOP, WARNING, ERROR, INFO, DEBUG 
#LogMode = None     	#The default setting from FBDPParameters will be used

# Specify if you want to print to the console:

LogToConsole = 1   	#The output will be printed to the console
#LogToConsole = 0    	#Output will not be printed to the console
#LogToConsole = None	#The default setting from FBDPParameters will be used

# Specify if you want to print to a file:

LogToFile = 1	    	#The output will be printed to the file <LogFile>
#LogToFile = 0	    	#Output will not be printed to file
#LogToFile = None   	#The default setting from FBDPParameters will be used

# Specify your logfile:

Logfile = 'C:\\VPS.log'     	    #If you want to use own directory
#Logfile = 'VPS.log'		    #Will be placed in default directory
    	    	    	    	    #specified by Logdir in FBDPParameters
#Logfile = None     	    	    #Default directory and filename 
    	    	    	    	    #BDP_<ScriptName>.log will be used 
