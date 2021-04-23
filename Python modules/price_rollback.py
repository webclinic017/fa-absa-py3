# This one time script was created to roll back the price reupload which 
# have been deleted by FDeletePrice script on 16/03/2015. This caused 
# a break on the PB_SETTLEMENTS reports which are used by PCG for the recons.
# Until we find a good solution for funding calculations, we need to keep the 
# prices in Front.

import ael, acm
import csv

price_queue = list()
fieldnames = ["day", "ask", "bid", "high", "low", "settle", "last", "n_ask", "n_bid", "volume_last", "volume_nbr", "bits", "curr", "insaddr"]

def del_in_transaction(log):
    global price_queue
    ael.abort_transaction()
    ael.begin_transaction()
    try:
        for prc in price_queue[:]:
            csv_fields = list()
            for field in fieldnames:
                if field in ("insaddr", "curr"):
                    attr = getattr(prc, field).insid
                else:
                    attr = str(getattr(prc, field))
                csv_fields.append(attr)
            log.write(",".join(csv_fields) + "\n")
            
            prc.delete()
            
        ael.commit_transaction()
        price_queue = list()
        ael.poll()
        acm.PollAllEvents()
        acm.PollDbEvents()
    except Exception as e:
        ael.abort_transaction()
        log.close()
        print("Error deleting price %s" % (e))
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
                del_in_transaction(log)
            
            ins = ael.Instrument[record["insaddr"]]
            # prices for these instypes have not been deleted 
            if ins.instype == "Stock" or ins.instype == "CFD" or ins.instype == "Deposit":
                continue
            acm_date = record["day"][6:] + '-' + record["day"][3:5] + '-' + record["day"][0:2]
            query1 = "instrument='%s' and day='%s' and market='%s'" \
                                    % (ins.insaddr, 
                                       acm_date, 
                                       market)
            
            prcs = acm.FPrice.Select(query1)
            ins_name = ins.insid
            if prcs:
                for prc in prcs:
                    print("Price found for %s %s" % (ins_name, ael.date(record["day"])))
                    price_queue.append(ael.Price[prc.Oid()])
            else:
                print("Price not found for %s %s" % (ins_name, ael.date(record["day"])))
        # commit the last batch even if it is smaller than batch_size
        del_in_transaction(log)    
    print("Completed successfully")
