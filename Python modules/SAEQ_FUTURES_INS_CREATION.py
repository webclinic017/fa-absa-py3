import ael

ael_variables=[('date', 'Current Close Out Date', 'string', ael.date('2008-12-18'), ael.date('2008-12-18')),
                ('daten', 'Next Close Out Date', 'string', ael.date('2009-03-05'), ael.date('2009-03-05'))]

def ael_main(dict):
    date = ael.date(dict['date'])
    month = {1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}
    d = ael.date(dict['daten'])
    y, m, d = d.to_ymd()
    day = '/' + month[m] + str(y)[2:4]
    print 'in'
    futures = ael.Instrument.select('instype = "Future/Forward"')
    print futures
    updateTime = 23 * 60 * 60 + 50 * 60

    for ins in futures:
        if ins.und_instype in ('Stock', 'EquityIndex') and ins.exp_day == date and ins.und_insaddr.insid != 'ZAR/Dummy':
            #ins = ael.Instrument['ZAR/ABL/DEC08']
            id = str(ins.und_insaddr.insid) + day
            t = ael.Instrument[id]
            if t == None:
                #print type(ins.exp_day)
                ic = ins.new()
                ic.exp_day = ael.date(dict['daten'])
                ic.exp_time = ael.date(dict['daten']).to_time() + updateTime
                ic.insid = id 
                print (ins.exp_time)
                try:
                    ic.commit()
                    print 'Instrument created: ', id 
                except:
                    print 'Instrument not created: ', id
            else:
                print 'Instrument already exists: ', id
