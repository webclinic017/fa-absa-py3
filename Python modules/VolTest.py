import ael, string, math

def main(temp,*rest):

    date = ael.date_today()
    date2 = date.add_banking_day(ael.Instrument['ZAR'], -2)
    date1 = date.add_banking_day(ael.Instrument['ZAR'], -1)
 
    #file2 = 'C:/As_End_day/' + date2.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_' + date2.to_string('%y%m%d') + '.csv'
    #file1 = 'C:/As_End_day/' + date1.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_' + date1.to_string('%y%m%d') + '.csv'
   
    file2 = '/services/frontnt/BackOffice/Atlas-End-Of-Day/' + date2.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_' + date2.to_string('%y%m%d') + '.csv'
    file1 = '/services/frontnt/BackOffice/Atlas-End-Of-Day/' + date1.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_' + date1.to_string('%y%m%d') + '.csv'
    #file2 = 'Z:/' + date2.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_' + date2.to_string('%y%m%d') + '.csv'
    #file1 = 'Z:/' + date1.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_' + date1.to_string('%y%m%d') + '.csv'
    
    #Dictionary for 2 business days ago
    dictionary2 = {}
    filename2 = open(file2)
    line2 = filename2.readline()
    line2 = filename2.readline()
    line2 = filename2.readline()

    line2 = line2.rstrip()
    lin2 = string.split(line2, ';')
    
    while lin2[0] != '':
        trdnbr2 = lin2[0]
        vol2 = lin2[1]
        dictionary2[trdnbr2] = vol2
        line2 = filename2.readline()
        line2 = line2.rstrip()
        lin2 = string.split(line2, ';')
    
    #Dictionary for 1 Business day ago
    dictionary1 = {}
    filename1 = open(file1)
    line1 = filename1.readline()
    line1 = filename1.readline()
    line1 = filename1.readline()

    line1 = line1.rstrip()
    lin1 = string.split(line1, ';')
    
    while lin1[0] != '':
        trdnbr1 = lin1[0]
        vol1 = lin1[1]
        dictionary1[trdnbr1] = vol1
        line1 = filename1.readline()
        line1 = line1.rstrip()
        lin1 = string.split(line1, ';')
        
    filename1 = open(file1)
    line1 = filename1.readline()
    line1 = filename1.readline()
    line1 = filename1.readline()

    #fname = 'C:/As_End_day/' + date1.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_Final' + date1.to_string('%y%m%d') + '.csv'    
    fname = '/services/frontnt/BackOffice/Atlas-End-Of-Day/' + date.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_Final' + date.to_string('%y%m%d') + '.csv'    
    #fname = 'Z:/' + date1.to_string('%Y-%m-%d') + '/SAEQ_Exception_Report_Vols_Final' + date1.to_string('%y%m%d') + '.csv'    
    
    outfile = open(fname, 'w')
    outfile.write('TrdNbr' + ',' + 'Vol T-2' + ',' + 'Vol T-1' + ',' + 'Change' + '\n')
    
    for k in dictionary1.keys():
        if dictionary2.has_key(k):
            if dictionary1[k] != dictionary2[k]:
                if dictionary2[k] == 0:
                    vol1 = (float)(dictionary1[k])
                    vol2 = (float)(dictionary2[k])
                    change = vol1
                    outfile.write((str)((str)(k) + ',' + (str)(vol1) + ',' + (str)(vol2) + ',' + (str)(change)) + '\n')
                elif abs(((float)(dictionary1[k])-(float)(dictionary2[k]))/(float)(dictionary2[k])) >= 0.02:
                    vol1 = (float)(dictionary1[k])
                    vol2 = (float)(dictionary2[k])
                    change = abs((vol1-vol2)/vol2)
                    outfile.write((str)((str)(k) + ',' + (str)(vol1) + ',' + (str)(vol2) + ',' + (str)(change)) + '\n')
    outfile.close()
    
    print 'complete'
    return 'complete'
