import ael
import csv
import math
import time

filterSize = 400

FILTER_PREFIX = "Max_"

tradeNumbers_input = """

132445181
132445180
132445179
132445178
"""

tradeNumbers = tradeNumbers_input.split('\n')
tradeNumbers = [ x.replace(",", "") for x in tradeNumbers if x ]

org = []
org.append([])

# Create a dummy trade filter    
def CreateTradeFilter(ptfName):

    tradeFilter = ael.TradeFilter.new()
    tradeFilter.fltid = ptfName
    tradeFilter.set_query([('', '', 'Trade Number', 'equal to', '-999', '')])
    tradeFilter.commit()
    
    return tradeFilter    
    
def CheckAndCreateTradeFilters(filelen, filterSize=400):

    numOfFilters = int(math.ceil(float(filelen)/filterSize))

    filters = { 'Org' : numOfFilters }  # Update this if more then 400 Partial
    
    filterNames = {}
    
    for eachType in filters.keys():
        filtersCount = filters[eachType]
        #print "%s,%s" % (eachType, filtersCount)
        _filters = []
        
        for batchNum in range(1, (filtersCount+1)):
            filter = "%s%s" % (FILTER_PREFIX, batchNum)
            tf = ael.TradeFilter[filter]
            if tf:
                print(("Checking %s: Ok" % (filter)))
            else:
                print(("Checking %s: Not found" % (filter)))
                tf = CreateTradeFilter(filter)

                if tf:
                    print(("Filter created, Checking %s : Ok" % (filter)))
                else:
                    print(("Checking %s : Failed." % (filter)))
                    return (False, None)

            _filters.append(filter)
        filterNames[eachType] = _filters
    return (True, filterNames)    

# Populating the trade filters back.
# Original trade filters
(retcode, tfs) = CheckAndCreateTradeFilters(len(tradeNumbers), filterSize)

#print(tfs)

trdcnt = 0
for et in tradeNumbers:

    #org[batch].append((or_str, '', 'Trade number', 'equal to', TRADE_ID, ''))


    trdcnt = trdcnt + 1
    batch = ((trdcnt - 1) / filterSize) + 1
    trdi = trdcnt % filterSize
    or_str = 'Or'
    # If beginning of a new filter
    if trdi == 1:
        or_str = ''
        org.append([])
    
    org[batch].append((or_str, '', 'Trade number', 'equal to', '%s' % (et), ''))

for ef in tfs['Org']:
    num = int(ef.split('_')[-1])
    tf = ael.TradeFilter[ef].clone()
    tf.set_query(org[num])
    tf.commit()
    
print("Done.")
