""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/templates/FOperationsDocumentHooksTemplate.py"
"""----------------------------------------------------------------------------
MODULE: FOperationsDocumentHooksTemplate

DESCRIPTION: This module contains functions called by the core operations
             document scripts. It should NEVER be edited. All functions in
             FOperationsDocumentHooksTemplate can be overridden in a module of
             your own choice. To do so, simply create a module in the Python 
             editor and copy the function declaration of the function you want 
             to override into it. Then you implement the function as desired
             in this module. You might need to import acm when implementing
             your hook. See how the default implementation is done in this
             module to see what inputs and outputs are needed.

             Do not copy the declarations of the functions you do not want to
             override into your hook modules. Remember that the return types
             and the input parameters has to be the same in your hook as in
             FOperationsDocumentHooksTemplate.

             Save your module and register it in FDocumentationParameters.
             To do so add a CustomHook-object into the list named hooks in
             FDocumentationParameters. For example, if you have overridden
             the function SettlementTransportRouter in a module called MyHooks, 
             you would add a CustomHook-object like this:
             hooks = [CustomHook('MyHooks', 'SettlementTransportRouter')]

             The input parameters to a CustomHook-object has to be strings.
             The first string is the name of the module, the second the name
             of the hook.

             Once the hooks have been implemented and registered in
             FDocumentationParameters, the affected Arena Task Servers
             have to be restarted in order to get the desired functionality.

             (c) Copyright 2016 FRONT ARENA . All rights reserved.
----------------------------------------------------------------------------"""

def SettlementTransportRouter(document):
    """
    DESCRIPTION: This function is used to decide which transport method 
                 a settlement document should be sent using.
    INPUT:       An FOperationsDocument. Treat input as read-only.
    OUTPUT:      A String.
    """
    return 'Network'
