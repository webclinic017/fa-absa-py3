'''-----------------------------------------------------------------------------
PROJECT                 :  Money Market Demat amintenance
PURPOSE                 :  To update the authorised amount 
DEPATMENT AND DESK      :  Ops
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Manan Ghosh
CR NUMBER               :  ABITFA - 4776
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------

2017-04-20              Manan Ghosh           To update the quthorised amount of the instrument

'''



import acm, csv

from at_ael_variables import AelVariableHandler

MMSS_ISIN_REQUEST_STATE_CHART_NAME = 'MM ISIN Management'

ael_variables = AelVariableHandler()

ael_variables.add_input_file('file_path', 'CSV Path', mandatory=True)
        
        
def ael_main(ael_dict):

    upload_file = str(ael_dict['file_path'])
    
    print 'upload_file   ', str(upload_file)

    csvfile = open(upload_file, 'r')
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

    sc = acm.FStateChart[MMSS_ISIN_REQUEST_STATE_CHART_NAME]

    try:
        for row in csvreader:

            if len(row) < 2 :
                continue

            amount = float(row[1])

            ins = acm.FInstrument[row[0]]
        
            processes = acm.BusinessProcess.FindBySubjectAndStateChart(ins, sc)
            for proc in processes:
                proc.Delete()

            bp = acm.BusinessProcess.InitializeProcess(ins, sc)
            bp.ForceToState('Active', amount)
            bp.Commit()
        
            print 'Authorised amount changed for the instrument [%s] to amount %d ' % (ins.Name(), amount )

    finally:
        csvfile.close()


