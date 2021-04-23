import ael

 

def DisplayAggregateInfo(portName):

    port = ael.Portfolio[portName]

    if not port:

        print portName, 'is not a valid portfolio'

        return

        

    for t in port.trades():

        if t.aggregate != 0:

            print t.trdnbr, t.insaddr.insid, t.prfnbr.prfid, t.aggregate, t.type, t.archive_status

            if len(t.additional_infos()) > 0:

                print t.trdnbr, 'has additional infos!'

            

DisplayAggregateInfo('47274')

