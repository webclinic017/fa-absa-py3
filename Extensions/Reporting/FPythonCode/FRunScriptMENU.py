from __future__ import print_function
"""----------------------------------------------------------------------------
Module
    FRunScriptMENU - Module with code used to start run script guis, tasks and python scripts.

    (c) Copyright 2011 by SunGard Front Arena. All rights reserved.

DESCRIPTION

    To start programs/tasks from a menu it's just an FMenuExtension entry in Extension Manager:

    [MyModule]FFrame:Task =
        Function=FRunScriptMENU.StartTask
        MenuType=Application
        ParentMenu=Tools/ProgramStarter
        TaskName=MyTask

    [MyModule]FFrame:TaskNoGUI =
        Function=FRunScriptMENU.StartTaskWithoutGUI
        MenuType=Application
        ParentMenu=Tools/ProgramStarter
        TaskName=MyTask

    [MyModule]FFrame:Module =
        Function=FRunScriptMENU.StartModule
        MenuType=Application
        ParentMenu=Tools/ProgramStarter
        ModuleName=PythonModule

    [MyModule]FFrame:Function =
        Function=FRunScriptMENU.StartFunction
        MenuType=Application
        ParentMenu=Tools/ProgramStarter
        FunctionName=PythonModule.function
        [Parameter=(None,eii)]

----------------------------------------------------------------------------"""
import acm
import traceback

def StartModule(eii):
    modulename = eii.MenuExtension().At( "ModuleName")
    if modulename:
        try:
            acm.RunModuleWithParameters(str(modulename.AsString()), acm.GetDefaultContext())
        except Exception as msg:
            trace = traceback.format_exc()
            print (trace)
    else:
        acm.Log("FMenuExtension '%s': Missing parameter ModuleName"%(eii.MenuExtension().Name()))
    return

def StartTask(eii):
    taskname = eii.MenuExtension().At( "TaskName")
    if taskname:
        taskname=str(taskname.AsString())
        runtask=acm.FAelTask[taskname]
        if runtask:
            try:
                acm.StartRunScript(runtask, None)
            except Exception as msg:
                trace = traceback.format_exc()
                acm.Log("Error, task '%s': %s"%(taskname, msg))
                print (trace)
        else:
            acm.Log("FMenuExtension '%s': Could not find task with TaskName='%s'"%(eii.MenuExtension().Name(), taskname))
    else:
        acm.Log("FMenuExtension '%s':Missing parameter TaskName"%(eii.MenuExtension().Name()))

def StartTaskWithoutGUI(eii):
    taskname = eii.MenuExtension().At( "TaskName")
    if taskname:
        taskname=str(taskname.AsString())
        runtask=acm.FAelTask[taskname]
        if runtask:
            try:
                runtask.Execute()
            except Exception as msg:
                trace = traceback.format_exc()
                acm.Log("Error, task '%s': %s"%(taskname, msg))
                print (trace)
        else:
            acm.Log("FMenuExtension '%s': Could not find task with TaskName='%s'"%(eii.MenuExtension().Name(), taskname))
    else:
        acm.Log("FMenuExtension '%s':Missing parameter TaskName"%(eii.MenuExtension().Name()))

def StartFunction(eii):
    program = eii.MenuExtension().At( "FunctionName")
    if program:
        program=str(program.AsString())
        pgm=program.split('.')
        if len(pgm) == 2:
            try:
                m=__import__(pgm[0])
                reload(m)
                try:
                    param=str(eii.MenuExtension().At( "Parameter").AsString())
                except AttributeError:
                    param=None
                f = m.__getattribute__(pgm[1])
                if param and param == 'eii':
                    f(eii)
                else:
                    f()
            except Exception as msg:
                trace = traceback.format_exc()
                print ("Error, function '%s':%s"%(program, msg))
                print (trace)
        else:
            acm.Log("FMenuExtension '%s': parameter FunctionName should be in format Module.function"%(eii.MenuExtension().Name()))
    else:
        acm.Log("FMenuExtension '%s':Missing parameter FunctionName"%(eii.MenuExtension().Name()))
