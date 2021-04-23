""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceLinkApplicationStates.py"

MandatoryColumns = ["", "!", "Instrument", "Currency", "Market", "Market Code(Ticker/RIC/Alpha Code)"]
AvailableColumns = ["Ins Type", "Price Distributor", "Service", "Semantic", "Start Time", "Stop Time", "Update Interval", "Addition Addend", "Multiplication Factor", "Last Follow Interval", "Error Message", "Discard Negative Price", "Discard Zero Price", "Discard Zero Quantity", "Force Update", "Do Not Reset Fields", "XML Data",
"Is Delayed", "Ignore Clear Price"]

CurrentColumns = []

SemanticColumns = [" ", "ADM Field", "IDP Field", "Comment"]
ADMFields = [
                 "ASK", 
                 "ASK_DATE",
                 "BID",
                 "BID_DATE", 
                 "CLOSE", 
                 "DAY",
                 "DIFF_DATE",
                 "HIGH",
                 "HIGH_DATE",
                 "LAST",
                 "LAST_DATE",
                 "LOW",
                 "LOW_DATE",
                 "N_ASK",
                 "N_ASK_DATE",
                 "N_BID",
                 "N_BID_DATE",
                 "N_OPEN",
                 "OPEN",
                 "OPEN_DATE",
                 "SETTLE",
                 "SETTLE_DATE",
                 "TIME_CLOSE", 
                 "TIME_OPEN", 
                 "TIME_LAST",
                 "TIME_LAST_DATE",
                 "TRADE_DATE",
                 "TRADE_TIME",
                 "VOLUME_LAST",
                 "VOLUME_LAST_DATE",
                 "VOLUME_NBR",
                 "VOLUME_NBR_DATE"
            ]

PermittedDistributorTypes = ["AMS", "Reuters", "Bloomberg", "MarketMap", "Open Price Feed", "Custom 1", "Custom 2", "Custom 3"]

class PriceLinkSpecificationStates:
    PLDOpen             = 0
    PLDPopulated        = 1
    PLDSelected         = 2
    PLDMultiSelected    = 4
    PLDChanged          = 8
    PLDUpdated          = 16
    PLDAdded            = 32

class PriceDistributorStates:
    PDOpened   = 0
    PDSelected = 1
    PDChanged  = 2

class PriceSemanticStates:
    PSOpened           = 0
    PSPopulated        = 1
    PSSelected         = 2
    PSMultiSelected    = 4
    PSChanged          = 8
    PSUpdated          = 16
    PSAdded            = 32
    PSModified         = 64