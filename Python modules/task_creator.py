import acm


class TaskCreator(object):
    """Creates new set of modified tasks.

    Base class for creation of new tasks as a replica of existings ones with
    modified parameters.

    """
    def run(self):
        """Run creation of modified tasks.

        Filter tasks you want to modify
            1. copy original tasks (clone)
            2. update copied task
            3. create new task (commit)        

        """
        tasks = filter(self._task_filter, acm.FAelTask.Select(''))
        for task in tasks:
            try:
                new_task = task.Clone()
                self._update(new_task)
                new_task.Commit()
                print("Created task %s" % new_task.Name())
            except Exception as ex:
                print("Skipping %s: %s" % (task.Name(), ex))

    def _task_filter(self, task):
        """Return True if task meets conditions. Otherwise return False."""
        raise NotImplementedError("Subclasses should implement this!")

    def _update(self, task):
       """Update task."""
       raise NotImplementedError("Subclasses should implement this!")


class TaskCreatorExample(TaskCreator):
    """Example usage of TaskCreator class.

    Copies every task with name signature PS_Reporting_<CLIENT>_SERVER and
    changes output path to /services/frontnt/Task/MyTest/

    Created tasks are named by adding extra string after current names.

    Example code to execute this task creator:

    task_creator = TaskCreatorExample("TEST")
    task_creator.run()

    """

    def __init__(self, name_modifier):
        super(TaskCreatorExample, self).__init__()
        self.name_modifier = name_modifier

    def _task_filter(self, task):
        """Return True if task meets conditions. Otherwise return False.

        Tasks with signature PS_Reporting_<CLIENT>_SERVER.

        """
        name = task.Name()
        if name.startswith("PS_Reporting_") and name.endswith("_SERVER"):
            return True
        return False

    def _update(self, task):
        """Update task."""
        self._update_name(task)
        self._update_params(task)

    def _update_name(self, task):
        """Set new name."""
        task.Name('_'.join([task.Name(), self.name_modifier]))

    def _update_params(self, task):
        """Update task parameters."""
        params = task.Parameters()
        params.AtPutStrings('OutputPath', "/services/frontnt/Task/MyTest/")
        params.Commit()
        task.Parameters(params)
