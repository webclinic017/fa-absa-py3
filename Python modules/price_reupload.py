# This one time script was created to reupload prices which have been deleted
# by FDeletePrice script on 16/03/2015. This caused a break on the 
# PB_SETTLEMENTS reports which are used by PCG for the recons. Until we find
# a good solution for funding calculations, we need to keep the prices in 
# Front.

import ael, acm
import csv

price_queue = list()
fieldnames = ["day", "ask", "bid", "high", "low", "settle", "last", "n_ask", "n_bid", "volume_last", "volume_nbr", "bits", "curr", "insaddr"]

def commit_in_transaction(log):
    global price_queue
    ael.abort_transaction()
    ael.begin_transaction()
    try:
        for prc in price_queue:
            prc.commit()
            
            csv_fields = list()
            for field in fieldnames:
                if field in ("insaddr", "curr"):
                    attr = getattr(prc, field).insid
                else:
                    attr = str(getattr(prc, field))
                csv_fields.append(attr)
            log.write(",".join(csv_fields) + "\n")
            
        ael.commit_transaction()
        price_queue = list()
        ael.poll()
        acm.PollAllEvents()
        acm.PollDbEvents()
    except Exception as e:
        ael.abort_transaction()
        log.close()
        print("Error committing price %s" % (e))
        raise

ael_variables = [
    ['input_file', 'Input price file', 'string', None, '', 1, 0, 'Input file with prices', None, 1],
    ['output_log', 'Output log', 'string', None, '', 1, 0, 'File where the output log will be written', None, 1],
]

def ael_main(parameters):
    log = open(parameters['output_log'], 'w')
    with open(parameters['input_file'], 'r') as prices:
        csv_reader = csv.DictReader(prices, fieldnames)
        market = acm.FParty['internal'].Oid()
        batch_size = 250
        for record in csv_reader:
            if len(price_queue) > (batch_size-1):
                commit_in_transaction(log)
            
            ins = ael.Instrument[record["insaddr"]]
            # prices for these instypes have not been deleted 
            if ins.instype == "Stock" or ins.instype == "CFD" or ins.instype == "Deposit":
                continue
            acm_date = record["day"][6:] + '-' + record["day"][3:5] + '-' + record["day"][0:2]
            query1 = "instrument='%s' and day='%s' and market='%s'" \
                                    % (ins.insaddr, 
                                       acm_date, 
                                       market)
    
            prc = acm.FPrice.Select(query1)
            ins_name = ins.insid
            if prc:
                print("Price found for %s %s" % (ins_name, ael.date(record["day"])))
            else:
                prc = ael.Price.new()
                for prop_name in fieldnames:
                    if prop_name == "day":
                        setattr(prc, prop_name, ael.date(acm_date))
                    elif (prop_name == "curr" or prop_name == "insaddr"):
                        setattr(prc, prop_name, ael.Instrument[record[prop_name]])
                    else:
                        setattr(prc, prop_name, float(record[prop_name]))
                prc.ptynbr = market
                price_queue.append(prc)
                print("New price created for %s %s %s" % (ins_name, ael.date(record["day"]), prc.settle))
        # commit the last batch even if it is smaller than batch_size
        commit_in_transaction(log)    
    print("Completed successfully")
