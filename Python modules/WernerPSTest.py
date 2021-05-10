import ael
 
update = r'''
UPDATE leg
SET archive_status = 0, updat_usrnbr = 968, updat_time = GETDATE()
WHERE legnbr in (2534056, 2534059)
'''
ael.dbsql(update)
update = r'''
UPDATE cash_flow
SET archive_status = 0, updat_usrnbr = 968, updat_time = GETDATE()
WHERE cfwnbr in (21205158, 21205159, 21205163, 21205164)
'''
ael.dbsql(update)
update = r'''
UPDATE additional_info
SET archive_status = 0, updat_usrnbr = 968, updat_time = GETDATE()
WHERE valnbr in (221877495, 221877791)
'''
ael.dbsql(update)
update = r'''
UPDATE instrument
SET archive_status = 0, updat_usrnbr = 968, updat_time = GETDATE()
WHERE insaddr in (5740962, 5740965)
'''
ael.dbsql(update)
