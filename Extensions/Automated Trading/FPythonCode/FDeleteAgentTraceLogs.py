
import acm

"""----------------------------------------------------------------------------

MODULE

    FDeleteAgentTraceLogs: Delete old agent trace logs
    
    (C) Copyright 2011 Front Capital Systems AB. All rights reserved.

DESCRIPTION


NOTES:
    
     
    
------------------------------------------------------------------------------"""
       
ael_variables = [['agentTypes', 'Agent Types', 'string', acm.FAgentClass.Instances(), None,  1, 1, 'Trace logs for agents of this type will be deleted', None, None],
                 ['daysBack', 'Days Old', 'int', None, None, 1, 0, 'Trace logs older than this number of days will be deleted', None, None]]

def ael_main(dictionary):
    types = dictionary['agentTypes']
    daysBack = dictionary['daysBack']
    dateLimit = acm.Time.DateAdjustPeriod(acm.Time.TimeNow(), '-' + str(daysBack) + 'd')
    
    print ('Delete agent trace logs before ', dateLimit)
    traceLogs = acm.FAgentTrace.Select('createTime < ' + dateLimit)
    if traceLogs:
        i = traceLogs.Size() - 1
        nbr = 0
        while i > 0:
            log = traceLogs[i]
            if log.Type() in types:
                try:
                    
                    log.Delete()
                    nbr = nbr + 1
                except:
                    print ('Failed to delete ', log)
            i = i - 1
        
        if nbr > 0:
            print ('Deleted ' + str(nbr) + ' agent trace logs')
        else:
            print ('No agent trace logs found satisfying condition')
    else:
        print ('No agent trace logs found')
