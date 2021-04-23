import acm
from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()
ael_variables.add("alias",
                  label="Alias",
                  cls="string",
                  default="",
                  mandatory=True,
                  alt=("Alias of a new GPP client."))


def create_tasks(alias):    
    tasks = acm.FAelTask.Select('name like "PB_GPP_SWEEP_MAP501*"')
    for t in tasks:
        new_name = t.Name().replace("MAP501", alias)
        ntask = acm.FAelTask[new_name]
        if not ntask:
            ntask = t.Clone()
            ntask.Name(new_name)
        
        p = ntask.Parameters().Clone()    
        p.AtPutStrings('alias', alias)
        ntask.Parameters(p)
        ntask.Commit()
        print("Task: '%s'" % ntask.Name())


def ael_main(ael_dict):
    alias = ael_dict['alias']
    
    create_tasks(alias)
    
    print("Completed Successfully.")
