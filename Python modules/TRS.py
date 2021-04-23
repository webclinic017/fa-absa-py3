import ael, string

def tf_Search(searchstring, searchcolumn, newinstrument,*rest):        

    tfs = ael.TradeFilter.select()

    for tf in tfs:
        query = tf.get_query()
        for q_line in query:
            for line_entity in q_line:
                try:
                    ind = string.index(string.lower(line_entity), string.lower(sstring))
                except:
                    ind = -1
                if ind >= 0:
                    tradefilter = ael.TradeFilter[tf.fltid]
                    query = tradefilter.get_query()
                    for singlequery in query:
                        if singlequery[2] == searchcolumn:
                            if singlequery[4] == searchstring:
                                ond = string.index(str(query), str(sstring))
                                newq = str(query)[0:ond]  + newinstrument + str(query)[ond+len(str(sstring)):len(str(query))]
                                list = eval(newq)

#                                print 'NewQ: ' , newq
#                                print 'OldQ: ' , query

#                                tc_clone = tf.clone()
#                                tc_clone.set_query(list)
#                                tc_clone.commit()
#                                ael.poll()

sstring =  'EquitySwap'
newinstrument = 'TotalReturnSwap'
scolumn = 'Instrument.Type'
tf_Search(sstring, scolumn, newinstrument)
