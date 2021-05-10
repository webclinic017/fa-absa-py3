""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE

    FBDPPerform.py

DESCRIPTION

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import sys
import traceback
import acm

import FBDPWorld


# Contract for FBDPPerform module
#
#   * Participating BDP scripts should have a 'perform' module.  For example,
#     The BDP script FCashFlowAggregation has a module named
#     FCashFlowAggregationPerform.  The FXXX module deals with the user
#     interface, while the main functional code is contained in FXXXPerform
#     module.
#   * Participating FXXXPerform must have a perform() function and one or
#     more derived classes of FBDPPerform.
#   * The FXXXPerform.perform() must take two arguments.  The first argument
#     is an FBDPWorld instance and the second argument is the ael_variable
#     (a.k.a. execution parameter).
#   * The sole functionality of the FXXXPerform.perform() is -- based on the
#     execParam given, construct the appropriate FBDPPerofrm derived class
#     instance, then call the perform() method followed by end() method on the
#     class, before finally deleting the instance.
#   * The FBDPPerform derived class must implement perform() and end() method.
#   * The FBDPPerform derived class' end() method must invoke
#     FBDPPerform._end() at some point.


def _get_exception():
    """
    Returns last exception as string
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    d = traceback.format_exception(exc_type, exc_value, exc_traceback)
    msg = ''.join(d)
    return msg


def execute_perform(perfFunc, execParam):
    """
    Execute the perform() function.
    """
    world = FBDPWorld.CreateWorld(execParam)
    world.logStart(None)
    try:
        perfFunc(world, execParam)
    except:
        world.logError(_get_exception())
    acm.PollDbEvents()
    world.summarySummarise()
    world.logFinish(None)
    del world


class FBDPPerform(FBDPWorld.WorldInterface):
    """
    The FBDPPerform template class.
    """

    def __init__(self, world):
        FBDPWorld.WorldInterface.__init__(self, world)

    def _end(self):
        """
        Shared tidy up code for the subclasses.
        """
        pass

    def end(self):
        """
        The method tidy up the resources after perform().
        """
        raise NotImplementedError('Must be overridden in the subclass.')

    def perform(self, execParam):
        """
        The main functionality body.
        """
        raise NotImplementedError('Must be overridden in the subclass.')
