""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/PortfolioTrading/etc/FToggleButtons.py"
"""--------------------------------------------------------------------------
MODULE    
    FToggleButtons

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
Helps ribbons to set/unset parameters and refresh actions afterwards
It does not commit anything to the ADS

-----------------------------------------------------------------------------"""
import acm
import FTradeProgramMenuItem
from FIntegratedWorkbenchLogging import logger


def RestrictToLimits(eii):
    try: 
        return ToggleParameter(eii, parameterName = 'Restrict Program To Limits')
    except StandardError as e:
        logger.error(e, exc_info=True)

class ToggleParameter(FTradeProgramMenuItem.TradeProgramMenuItem):
    no = 'No'
    yes = 'Yes'
    def __init__(self, extObj, parameterName, event=None, refresh = False,
                  parameterExtension = 'TradeProgramSettings'):
        FTradeProgramMenuItem.TradeProgramMenuItem.__init__(self, extObj)
        self.parameterName = str(parameterName)
        self.parameters = acm.GetDefaultContext().GetExtension('FParameters',
                                                                'FObject',
                                                                 parameterExtension)
        self.checked = self.IsYes()
        self.refresh = refresh
        self._event = event
    
    def ReadParameter(self):
        try:
            return self.parameters.Value().GetString(self.parameterName, '')
        except AttributeError as e:
            logger.error(str(e))
            return ''
        
    def IsYes(self):
        return self.ReadParameter().strip().capitalize() == ToggleParameter.yes
    
    def SetParameter(self, value):
        self.parameters.Value().AtPutParsed(self.parameterName, str(value))

    def ToggleParameter(self):
        self.SetParameter(ToggleParameter.no if self.IsYes() else ToggleParameter.yes)
        self.checked = self.IsYes()
    
    def InvokeAsynch(self, eii):
        self.ToggleParameter()
        if self.refresh:
            event = self._event(self.checked)
            self._Dispatcher().Update(event)

    def Checked(self):
        return self.checked