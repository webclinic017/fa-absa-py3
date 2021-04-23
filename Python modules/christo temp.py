import ael

sql = "select count(t.trdnbr),p.prfid, e.tag from trade t,portfolio p, instrument i,ds_enums e where e.name = 'InsType' and e.value = i.instype and t.prfnbr = p.prfnbr and t.archive_status = 0 and t.insaddr = i.insaddr group by p.prfid,  e.tag having  count(t.trdnbr) > 1000 "

res = ael.dbsql(sql)

r =  res[0]

for cnt, port, instype in r:
    print port, '#', instype, '#', cnt
