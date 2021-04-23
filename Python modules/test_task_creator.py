import acm
from at_ael_variables import AelVariableHandler


class NewTaskCreatorException(Exception):
    """General exception."""
    pass


class TestTasksCreator(object):        
    """Base class for test task creator."""    
    def run(self):
        """Run creation of desired (modified) tasks.

        - filter tasks you want to modify (from all available tasks).
            - copy original tasks (clone)
            - modify copied task
            - create new task (commit)        
    
        """
        modify_tasks = filter(self._task_filter, acm.FAelTask.Select(''))
        print([task.Name() for task in modify_tasks])
        for task in modify_tasks:
            #new_task = task.Clone()
            self._update(task)
            try:
                task.Commit()
            except:
                print('Skipping: Task already exists')
        
    def _task_filter(self, task):
        """Return True if task meets conditions. Otherwise return False."""
        raise NotImplementedError("Subclasses should implement this!")
        
    def _update(self, task):
        """Update task based on requirements."""
        raise NotImplementedError("Subclasses should implement this!")



class EnableReRun(TestTasksCreator):
    def __init__(self, override):
        super(EnableReRun, self).__init__()
        self.override = override

    def _task_filter(self, task):
        """Return true if tasks meets your conditions."""
        name = task.Name()
        if name.startswith('PS_CallAccountReports') and name.endswith('SERVER'):
            return True
        return False

    def _update(self, task):
        """Update task."""
        self._update_params(task)

    def _update_params(self,  task):
        params = task.Parameters()
        #print params
        params.AtPutStrings('override', self.override)
        params.Commit()
        task.Parameters(params)



def ael_main(config):
    override = "Yes" if config["override"] else "No"
    task_creator = EnableReRun(config["override"])
    task_creator.run()
