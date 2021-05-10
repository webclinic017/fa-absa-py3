""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAMenusAndButtons.py"
import acm
import FUxCore
import subprocess
import tempfile
import codecs
import AAParamsAndSettingsHelper as settings
import AAUtilFunctions as utilfunctions

LOGGER = settings.getAdaptivAnalyticsLogger()

#---------------- CVA TM Menu ----------------
def CreateCVACalculationMenuItemTM(extObj):
    return CVACalculationMenuItemTM(extObj)

class CVACalculationMenuItemTM(FUxCore.MenuItem):
       
    def __init__(self, extObj):
        self.m_extObj = extObj
    
    def Invoke(self, eii):
        calcName = eii.Definition().At("CalcName").AsString()
        res = GetCVACalculationXML(self.m_extObj, calcName)
        if res['xml']:
            filename = WriteAdaptivXML(res, '.aaj')
            if filename:
                LOGGER.info("Wrote job file to: %s" % (filename))
        else:
            LOGGER.info("No CVA calculation was found.")
    
    def Enabled(self):
        enabled = False
        try:
            cell = self.m_extObj.ActiveSheet().Selection().SelectedCell()
            rowObj = cell.RowObject()
            instrument = rowObj.SingleInstrumentOrSingleTrade()
        except:
            instrument = None
            rowObj = None
        if instrument and rowObj:
            if instrument.IsKindOf(acm.FCreditBalance) and rowObj.Class() == acm.FSingleInstrumentAndTrades:
                enabled = True
        return enabled 
    
    def Applicable(self):
        return True 

#---------------- CVA TM Ribbon ----------------    
def CreateCVACalculationRibbonItemTM(extObj):
    return CVACalculationRibbonItemTM(extObj)

class CVACalculationRibbonItemTM(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_extObj = extObj
    
    def Invoke(self, eii):
        calcName = eii.Definition().At("CalcName").AsString()
        res = GetCVACalculationXML(self.m_extObj, calcName)
        if res['xml']:
            LaunchAdaptiv(res)
        else:
            LOGGER.info("No CVA calculation was found.")
            
    def Enabled(self):
        enabled = False
        try:
            cell = self.m_extObj.ActiveSheet().Selection().SelectedCell()
            rowObj = cell.RowObject()
            instrument = rowObj.SingleInstrumentOrSingleTrade()
        except:
            instrument = None
            rowObj = None
        if instrument and rowObj:
            if instrument.IsKindOf(acm.FCreditBalance) and rowObj.Class() == acm.FSingleInstrumentAndTrades:
                enabled = True
        return enabled
    
    def Applicable(self):
        return True
        
def GetCVACalculationXML(extObj, calcName):
    LOGGER.info("Retrieving CVA calculation...")
    
    xml = None
    try:
        cell = extObj.ActiveSheet().Selection().SelectedCell()
        rowObj = cell.RowObject()
        context = cell.Column().Context()
        ins = rowObj.SingleInstrumentOrSingleTrade()
        if context:
            xml = acm.GetCalculatedValueFromString(rowObj, context, calcName, cell.Tag()).Value()
    except Exception as e:
        errMsg = "Failed obtaining CVA XML for instrument %s." % (ins.Name())
        LOGGER.error(errMsg, exc_info=1)
        
    res = {}
    res['xml'] = xml
    res['ins'] = '%s.' % ins.Name()
    return res
    
#---------------- PFE TM Ribbon ----------------  
def CreatePFECalculationRibbonItemTM(extObj):
    return PFECalculationRibbonItemTM(extObj)

class PFECalculationRibbonItemTM(FUxCore.MenuItem):
    def __init__(self, extObj):
        self.m_extObj = extObj
    
    def Invoke(self, eii):
        calcName = eii.Definition().At("CalcName").AsString()
        res = GetPFECalculationXML(self.m_extObj, calcName)
        if res['xml']:
            LaunchAdaptiv(res)
        else:
            LOGGER.info("No PFE calculation was found.")
            
    def Enabled(self):
        enabled = False
        try:
            cell = self.m_extObj.ActiveSheet().Selection().SelectedCell()
            rowObj = cell.RowObject()
            grouper = rowObj.GrouperOnLevel()
            grouperItem = rowObj.AsSymbol()
        except:
            grouper = None
            rowObj = None
        if grouper and rowObj:
            if (str(grouper.Label()) == 'Credit Entity' and str(grouperItem) != 'No Credit Entity' and rowObj.Class() == acm.FMultiInstrumentAndTrades):
                enabled = True
            elif (rowObj.Class() == acm.FSingleInstrumentAndTrades and "Credit Balance" == rowObj.Instrument().InsType()):
                enabled = True
        return enabled
    
    def Applicable(self):
        return True

def GetPFECalculationXML(extObj, calcName):
    LOGGER.info("Retrieving PFE calculation...")
  
    xml = None
    try:
        cell = extObj.ActiveSheet().Selection().SelectedCell()
        rowObj = cell.RowObject()
        context = cell.Column().Context()
        grouperItem = rowObj.AsSymbol()
        if context:
            xml = acm.GetCalculatedValueFromString(rowObj, context, calcName, cell.Tag()).Value()
    except Exception as e:
        errMsg = "Failed obtaining PFE XML for credit entity %s." % (grouperItem)
        LOGGER.error(errMsg, exc_info=1)
        
    res = {}
    res['xml'] = xml
    res['ins'] = '%s.' % (str(grouperItem))
    return res
    
#---------------- Launch/Write Adaptiv Analytics ----------------          
def LaunchAdaptiv(xml):
    filename = WriteAdaptivXML(xml, '.aaj')
    if not filename is None:
        try:
            subprocess.Popen([settings.getAdaptivAnalyticsStudioPath(), filename])
            LOGGER.info("Opened calculation in Adaptiv Analytics Studio.")
        except:
            LOGGER.error("Failed to launch Adaptiv Analytics Studio from directory %s" % settings.getAdaptivAnalyticsStudioPath(), exc_info=1)

def WriteAdaptivXML(xml, fileExtension):
    with tempfile.NamedTemporaryFile(prefix = utilfunctions.createValidWinFileName(xml['ins']), suffix = fileExtension, delete = False, dir = settings.getExportToFileDir()) as tmp:
        filename = tmp.name
    try:
        with codecs.open(filename, 'w', 'utf-8') as f:
            f.write(xml['xml'].decode('raw-unicode-escape'))
    except Exception as e:
        LOGGER.error("Failed writing to file.", exc_info=1)
        filename = None
    return filename
