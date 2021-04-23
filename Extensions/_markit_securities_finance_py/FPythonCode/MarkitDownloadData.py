""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitSecuritiesFinance/etc/MarkitDownloadData.py"
from __future__ import print_function
import acm
import csv
    
def LoadFromFile(address):
    try:
        with open(address, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()
            filtered_reader = filter(lambda row: row[headers.index('Record Type')] == '1', reader)
    except Exception as e:
        print(e)
        return None
    return [headers, filtered_reader]


