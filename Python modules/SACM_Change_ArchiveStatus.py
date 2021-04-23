import ael
def change_arch():
    trd = ael.Trade[64149].clone()
    print(trd.pp())
    trd.archive_status = 1
    trd.aggregate_trdnbr = 268021
    trd.commit()

def change_aggr():
    trd = ael.Trade[268021].clone()
    trd.aggregate = 1
    print(trd.pp())
    trd.commit()
    
change_aggr()
change_arch()
