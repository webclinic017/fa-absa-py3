
#Purpose:	Run several tasks in one run subsequentially in the same session.
#Requester:	Andrey Chechin
#Developer:	Marc-Stephan Maenner (marc-stephan.maenner@d-fine.de)
#Shortfalls:	The tasks will run subsequentially in the same session. This is why performance issues could arise if too many tasks are pooled together.


import acm
from at_ael_variables import AelVariableHandler
import FBDPGui

ael_variables = FBDPGui.TestVariables()
ael_variables = AelVariableHandler(ael_variables)
ael_variables.add('taskList',
    label= 'Tasks',
    cls = 'FAelTask',
    mandatory = False,
    multiple = True,
    alt = 'List of tasks'
)
    

def ael_main(dictionary):       
    for task in dictionary['taskList']:
        print("Executing %s" % task.Name())
        if not dictionary['Testmode']:
            task.Execute()
