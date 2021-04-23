#  Developer           : Tshepo Mabena
#  Purpose             : To provide daily CPI curves to Group Treasury
#  Department and Desk : PCG
#  Requester           : Gregory Davis
#  CR Number           : 837641

import ael, csv, acm

def write_file(name, data):
    
    f = file(name, 'wb')
    c = csv.writer(f, dialect = 'excel')
    c.writerows(data)
    f.close()
    
def CPI_CurveDaily(path, dt_start, dt_end):     
    
    List = [] 

    ins = ael.Instrument['SACPI']
    Dt_start = ael.date(dt_start)
    Dt_end   = ael.date(dt_end)

    Header = [str(Dt_start)]

    List.append(Header)
        
    while Dt_start < Dt_end:
        
        FwdPrice = ins.forward_price(Dt_start)
        Dt_start = Dt_start.add_days(1)
        
        data = [str(FwdPrice)]
        List.append(data)
    
        
    write_file(path, List) 

def ASQL(*rest):
    acm.RunModuleWithParameters('GT_CPI_DailyCurve', 'Standard' )
    return 'SUCCESS'   
    
ael_variables = [['FileName', 'File Name', 'string', None, 'ZAR_CPI_IND.csv', 1],
                 ['OutputPath', 'Output Path', 'string', None, '/services/frontnt/Task', 1],
                 ['dt_start', 'Start Date', 'string', None, ael.date_today(), 1],
                 ['dt_end', 'End Date', 'string', None, ael.date('2040-01-01'), 1]]

def ael_main(ael_dict):
        
    dt_start   = ael_dict['dt_start']
    dt_end     = ael_dict['dt_end']
    
    path = ael_dict['OutputPath'] + ael_dict['FileName']
    
    try:
        CPI_CurveDaily(path, dt_start, dt_end)
    except Exception, e:
        print e

    print 'Wrote secondary output to::' + path
