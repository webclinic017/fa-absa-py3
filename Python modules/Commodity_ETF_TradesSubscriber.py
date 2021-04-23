"""
Purpose                       :  Subscribe to trades in Commodity desk filters
                                 and write to file which is read in
                                 by the market data feeds into solace.
Department and Desk           :  [Commodity]
Requester                     :  [Byron Woods]
Developer                     :  [Edmundo Chissungo]
Jira                          :  [ABITFA-2615]
CR Number                     :  [CHNG0002184583]

-------------------------------------------------------------------------------

HISTORY
===============================================================================
Date       Change no Developer            Description
-------------------------------------------------------------------------------
2015-03-26 XXXXX    Edmundo Chissungo     Bug fix, files written to are locked 
										  by the pricing and risks MDF as it reads
										  in the FA extracted data.
										  The fix is queues and catches python IOErrors

"""

import sys
import xml.dom.minidom as xml
import ael
import acm
import os
import time

path = ""
main_dictStruct = {}
live_trade_filters = []
filter_list_from_config = []


def log(message):
    """Log the message with current date and time."""
    print("{0}: {1}".format(acm.Time.TimeNow(), message))


def retrieve_environment(env_config, filter_config):
    """Determine which FA environment (Dev/Uat/Prod)
    the script is running in.
    Returns the specified path contained in the
    FExtensionValue which differs for each
    environment.

    Also retrieves the list of trade filters separated by ';' in the
    FExtensionValue config file.

    """
    global path, filter_list_from_config

    arena_data_server = acm.FDhDatabase["ADM"].ADSNameAndPort().upper()
    configuration = acm.GetDefaultValueFromName(
        acm.GetDefaultContext(), acm.FObject, env_config)

    filter_list_from_config = acm.GetDefaultValueFromName(
        acm.GetDefaultContext(), acm.FList, filter_config).split(';')

    dom_xml = xml.parseString(configuration)
    tags = dom_xml.getElementsByTagName("Host")
    for element in tags:        
        if element.getAttribute("Name") == arena_data_server:
            path = element.getElementsByTagName(
                "output_path")[0].childNodes[0].data
            print(" path found: ", path)

def trade_cb(obj, trade, arg, operation):
    """The callback function for the trade subscription."""

    if operation in ["insert", "update"]:
        for trade_filter in live_trade_filters:
            if trade.trdnbr in trade_filter.SnapshotTradeNbrs():
                filter_name = trade_filter.Name()
                if filter_name in main_dictStruct.keys() and trade.trdnbr in main_dictStruct[filter_name].keys():
                    runner(filter_name, trade)
                    
                    write_to = os.path.join(path, filter_name + ".txt")
                    safeWriter(write_to, filter_name)
                    break
                else:
                    log(" ***CallBack: " + filter_name +
                        " not in main_dictStruct. Adding...")
                    add_trades(trade_filter)
                    if filter_name in main_dictStruct.keys() and trade.trdnbr in main_dictStruct[filter_name].keys():
                        runner(filter_name, trade)
                        
                        write_to = os.path.join(path, filter_name + ".txt")
                        safeWriter(write_to, filter_name)
                    break


def runner(ETFKey, trade):
    """Add the relevant trades' details to the dictionary structure. output """
    try:
        main_dictStruct[ETFKey][trade.trdnbr].append([
            trade.trdnbr, trade.quantity, trade.price / 100, trade.time])
    except Exception as exc:
        log(exc)

def solace_feed_file_source(file, ETFKey):
    """Write the trade details in the main_dictionary to file."""

    counter = 0
    for itemDict in sorted(main_dictStruct[ETFKey].items()):
        if main_dictStruct[ETFKey][itemDict[0]][0] > 0:
            file.write("%s\t" % main_dictStruct[ETFKey][itemDict[0]][0])
            file.write("%s\t" % main_dictStruct[ETFKey][itemDict[0]][3])
            file.write("%s\t" % main_dictStruct[ETFKey][itemDict[0]][1])
            file.write("%s\n" % main_dictStruct[ETFKey][itemDict[0]][2])
            counter += 1
    file.write("\n %d" % counter)
    
    
def safeWriter( etf_file_name, ETFKey):
    
    while (True) :
        try:
            file = open(etf_file_name, "w")
            file.write("Trade#\tTradeDate\tQuantity\tPrice\n")
            solace_feed_file_source(file, ETFKey)
                
            file.close()
            break
            #time.sleep(1)
        except IndexError, a:
            break    
        except (OSError, IOError) as e:
            time.sleep(1) #back off for one second as lock is replaced by the Market data feeds
        

def initialize_globals():
    """initialize the dictionary structure."""
    for filter_name in filter_list_from_config:
        try:
            trade_filter = acm.FTradeSelection[filter_name]
            live_trade_filters.append(trade_filter)
            add_trades(trade_filter)
        except Exception:
            exc_type, _exc_obj, exc_tb = sys.exc_info()
            log(exc_type)
            log(_exc_obj)
            log(exc_tb.tb_lineno)


def add_trades(trdf):
    """Add the trades already in the filter the global trades dictionary.
    The price is divided by 100 as per how business expects the output.

    """
    trade_list = trdf.Snapshot()
    if len(trade_list) > 0:
        main_dictStruct[str(trdf.Name())] = dict(
            (trade.Oid(), [trade.Oid(), trade.Quantity(), trade.Price() / 100, trade.TradeTime()])
            for trade in trade_list)


def start():
    """Subscribe to trade tables."""

    log("Starting...")

    retrieve_environment("ETFTradeConfigSettings", "FilterConfig")
    initialize_globals()
    for trade_filter in filter_list_from_config:
        ael.TradeFilter[trade_filter].trades().subscribe(trade_cb)
        # ael.Trade.subscribe(trade_cb, None)

    log("output_path: " + path)
    log("Started in main.")


def stop():
    """Unsubscribe from TimeSeries."""

    log("Stopping...")
    for trade_filter in filter_list_from_config:
        ael.TradeFilter[trade_filter].trades().unsubscribe(trade_cb)
        # ael.Trade.unsubscribe(trade_cb, None)
    log("Process stopped")
    return
