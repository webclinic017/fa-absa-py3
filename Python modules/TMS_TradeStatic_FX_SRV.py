import ael, os
from TMS_Functions import Get_BarCap_Book_ID
from TMS_TradeStatic_FX import SaveTradeStatic
from DateUtils import PDate

''' =====================================================================
    Purpose		: This Module is used as an Interface for running
                        : TMS_TradeStatic_FX
    Department and Desk	:
    Requester		: Mathew Berry
    Developer		: Babalo Edwana
    CR Number		: 261644
   ======================================================================= '''


DATE_FORMAT = "%Y-%m-%d"
TRADE_FILTER = "NLD_All_Trades"
SERVER_LOCATION = r"//services/frontnt/development"
SHOW_HEADER = True

ael_variables = [("repdate", "Reporting Day", "date", None, ael.date_today(), 1, 0), 
                 ("filter", "Trade Filter", "string", [tf.fltid for tf in ael.TradeFilter], TRADE_FILTER, 1, 0),
                 ("server", "Server Location", "string", None, SERVER_LOCATION, 1, 0)]

def ael_main(ael_dict):
    SaveTradeStatic(ael_dict["filter"], ael_dict["server"], SHOW_HEADER, ael_dict["repdate"])
