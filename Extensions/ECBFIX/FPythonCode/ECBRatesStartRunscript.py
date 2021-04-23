""" Module that handles starting the runscript. """
import acm

def StartRunscript(eii):
    acm.RunModuleWithParameters('ECBRatesRunscript', acm.GetDefaultContext())
