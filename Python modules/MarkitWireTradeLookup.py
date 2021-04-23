import acm
import ael
import csv
import os.path

def find_fa_trade(mwTrade):
    #Check if the trade actually exists on Front Arena
    trades = acm.FDictionary()
    query = """select distinct t.trdnbr,i.instype, ai.value \
          from trade t,instrument i,AdditionalInfo ai,AdditionalInfoSpec ais \
          where t.insaddr = i.insaddr \
          and ai.recaddr = t.trdnbr and ai.addinf_specnbr = ais.specnbr \
          and ais.field_name = 'CCPmiddleware_id'   \
          and i.instype in ('FRA','Swap','CurrSwap') \
          and t.status in ('FO Confirmed','BO-BO Confirmed','BO Confirmed','Terminated') \
          and ai.value = '"""+str(mwTrade)+"""' \
          order by t.trdnbr desc"""
    selection = ael.asql(query)
    for selectionFA in selection[1][0]:
        if selectionFA[0] > 0:
            return selectionFA[0], selectionFA[1], selectionFA[2]            
    
    return '', '', mwTrade

def write_fa_trades(s, read_path, write_path, *rest):
    try:    
        with open(write_path, 'wb') as out_file:
            with open(read_path) as source_file:
                output = csv.writer(out_file, dialect = 'excel')   
                header = ['FA Trade', 'Instrument', 'MW Trade']
                output.writerow(header)

                source_file = open(read_path)  

                line = (source_file.readline()).strip()

                while line != '':
                    data = find_fa_trade(line)   
                    print data
                    output.writerow([data[0], data[1], data[2]])
                    line = (source_file.readline()).strip()
         
                print 'Success: Data written to file ' + str(write_path)
                return 'Success: Data written to file ' + str(write_path)  
                  
    except Exception, e:
        print 'Error: generating files: ' + str(e)
        return 'Error: generating files: ' + str(e)
