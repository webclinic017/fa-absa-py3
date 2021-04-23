"""
Script for replacing underlying module of tasks.

Requestor: Ridwaan Arbee
Developer: Jakub Tomaga
Date: July 2016

"""

import acm
from at_ael_variables import AelVariableHandler


def python_modules_hook(selected_variable):
    """Display module names of selected tasks."""
    python_modules = []
    if selected_variable.value:
        for name in selected_variable.value.split(','):
            task = acm.FAelTask[name]
            if task:
                python_modules.append(task.ModuleName())
    current_modules = ael_variables.get('current_modules')
    current_modules.value = ','.join(set(python_modules))


ael_variables = AelVariableHandler()
ael_variables.add("tasks",
                  label="Tasks",
                  cls=acm.FAelTask,
                  multiple=True,
                  hook=python_modules_hook)
ael_variables.add("current_modules",
                  label="Current modules",
                  enabled=False)
ael_variables.add("new_module",
                  label="New Python module",
                  cls=acm.FAel,
                  collection=sorted(acm.FAel.Select("")))
ael_variables.add_bool("dry_run",
                       label="Dry run",
                       default=True)


def ael_main(config):
    """Entry point of the script."""
    tasks = config["tasks"]
    new_module = config["new_module"]
    dry_run = config["dry_run"]
    
    acm.BeginTransaction()
    try:
        for task in tasks:
            print("Changing module in task {0} from {1} to {2}".format(
                task.Name(), task.ModuleName(), new_module.Name()))
            task.ModuleName(new_module.Name())
            task.Commit()
        if not dry_run:
            acm.CommitTransaction()
        else:
            acm.AbortTransaction()
    except Exception as ex:
        acm.AbortTransaction()
        print("Error while changed task module: {0}".format(ex))
