

import acm
import IntraDayLimitMonitoring as limits

def getDeskNames():
    desk_names = []
    data = limits.getData()
    if data:    
        desks = data.desks
        for key in sorted(desks.iterkeys()):
            desk = desks[key]            
            desk_names.append(desk.desk_name) 
        return desk_names

ael_variables = [
                ['outputfile_csv', 'CSV Output File', 'string', None, 'C:\Temp\IntraDayLimitMonitoring_Report001.csv'],
                ['email_address', 'Email Address', 'string', None, 'christo.rautenbach@absacapital.com'],
                ['desks', 'Desks', 'string', getDeskNames(), None, 1, 1, 'Select Desks', None, 1],
                ['date', 'Date', 'string', None, 'Today'],
                ] 
 
def ael_main(dict):
    date = dict['date']
    if date =='Today':
        date = acm.Time.DateToday()
        print 'Using date:', date
    desk_names = dict['desks']
    outputfile_csv = dict['outputfile_csv']
    email_address = dict['email_address']
    limits.runReport(desk_names, outputfile_csv, email_address, date)
    print 'Completed Successfully'
    print 'Wrote secondary output to:::' + outputfile_csv
