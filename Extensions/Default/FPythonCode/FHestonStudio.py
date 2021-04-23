from __future__ import print_function

""" 
    A module that contains all the Heston Studio GUI code. The GUI was built using the AUX.
    
    Contents:
        1) Function ReallyStartDialog: This is the function that instantiates the GUI, by creating an instance of the classes described in (3) and (4) below.
        
        2) Function StartDialog: This is called from the menu choice, calls (1) to instantiate GUI.        
        
        3) Class HestonStudioDialog: This Class that contains all the GUI logic
            3a) Method HandleCreate calls a number of other methods to connect class attributes to GUI fields. Also calls CreateCallbacks to create callcks from GUI fields.
            3b) Method PopulateData calls a number of other methods to set default values to fields and add choices to drop-down lists.
            3c) All the information needed in the call to the calibration algorithm is gathered in the method OnCalibrateClicked 
            3d) The Calibration algorithm is called from the Method Calibrate(...), this is where an external custom algorithm should be plugged in.
            3e) OnPlotClicked plots the surface by changing the heston parameters of the volatility structure.
            3f) OnCommitClicked commits Heston parameters to the database, as well as commiting implied volatility values to the volatility points in the structure.
            
                        
        4) Class HestonStudioLayout: This Class builds the layout of the GUI           
            4a) The method HandleCreate calls a number of other methods that creates the layout for the different sections of the GUI.
    
"""


import acm
import math
import FUxCore

def ReallyStartDialog(shell, object):
    builder   = CreateLayout()
    customDlg = myCustomDialog(shell, object)
    acm.UX().Dialogs().ShowCustomDialog(shell, builder, customDlg)

def StartDialog(eii):   
    shell     = eii.ExtensionObject().Shell()
    object    = eii.ExtensionObject().CurrentObject()
    
    if object == None:
        message = 'No Surface Loaded: Please open an existing Volatility Structure or define and save a new one before trying to calibrate the Heston Parameters'
        acm.UX().Dialogs().MessageBoxInformation(shell, message)
        return 0
    
    if object.ReferenceInstrument() == None:
        message = 'No reference instrument in structure: Calibration is not possible without a reference (underlying) instrument. Please specify a reference (underlying) instrument for the structure'
        acm.UX().Dialogs().MessageBoxInformation(shell, message)
        return 0
        
    
    ReallyStartDialog(shell, object)
   
class myCustomDialog (FUxCore.LayoutTabbedDialog):
    def __init__(self, shell, object):
        self.m_parentObject    = object
        self.m_shell           = shell
        self.m_data            = None
        self.m_errorEst        = None
        self.m_hestonParams    = None
        self.m_startValuesDone = 0
        
    def HandleCreate( self, dlg, *dummy):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption("Heston Studio")
        
        """ Create Layouts for the Top Dialog and the tabs """
        topDialog = self.CreateTopDlg()
        resPane   = self.CreateResultPane()
        paramPane = self.CreateParameterPane()
        advPane   = self.CreateAdvancedPane()

        """ Add the Top Layout """
        topLayout = dlg.AddTopLayout( "top", topDialog )      
           
        """ Add the Tabs """
        resLayout      = dlg.AddPane( "Results", resPane ) 
        paramLayout    = dlg.AddPane( "Parameter Settings", paramPane ) 
        advancedLayout = dlg.AddPane( "Algorithm Settings", advPane ) 
        
        """ Create Bindings for controls in the different tabs """
        self.CreateTopLinks(topLayout)
        self.CreateResultLinks(resLayout)
        self.CreateParameterLinks(paramLayout)
        self.CreateAdvancedLinks(advancedLayout)
        
        """ Create Data Structures, Populate the the fields with default values and create callbacks """
        self.PopulateTopData()
        self.GetCalibrationSettings()
        self.AddCallbacks()
        self.ReadHestonParameterValues()
        self.GetCurrentParameters()
                                                                                                              
    def ReadHestonParameterValues(self):
        self.kappaIni.SetData(self.m_parentObject.SpeedOfMeanReversion())
        self.v0Ini.SetData(self.m_parentObject.InitialVolatility())
        self.thetaIni.SetData(self.m_parentObject.LongTermMeanVol())
        self.volVolIni.SetData(self.m_parentObject.VolOfVol())
        self.rhoIni.SetData(self.m_parentObject.UndVolCorr())    
    
    def GetCalibrationSettings(self):
        name      = "HestonCalibrationSettings"
        context   = acm.GetDefaultContext()

        extension = context.GetExtension("FParameters", "FObject", name)
        
        if extension:
            template = extension.Value()
        else:
            """ if no extension, default: Should never happen """
            template = acm.FDictionary()
        
        """ template is a dictionary """
        
        """ 1. Top Level Settings """
        if template.At("algorithm"):
            self.algorithm.SetData(template.At("algorithm"))
        else:
            self.algorithm.SetData("Levenberg-Marquardt (Local)")
                
        if template.At("formula"):
            self.formula.SetData(template.At("formula"))
        else:
            self.formula.SetData("Semi-Analytical (Numerical Integration)")
        
        if template.At("benchmark"):
            self.benchmark.SetData(template.At("benchmark"))
        else:
            self.benchmark.SetData("Market Prices")            
      
        if template.At("logging"):
            if type(template.At("logging")) == str:
                if template.At("logging") == "True":
                    self.logging.SetCheck(1)
                else:
                    self.logging.SetCheck(0)
            else:
                if template.At("logging").AsString() == "True":
                    self.logging.SetCheck(1)
                else:
                    self.logging.SetCheck(0)

        else:
            self.logging.SetCheck(1)
            
            
        """ 2. Parameter Tab Settings """
        if template.At("otmOnly"):
            if type(template.At("otmOnly")) == str:
                if template.At("otmOnly") == "True":
                    self.otmOnly.SetCheck(1)
                else:
                    self.otmOnly.SetCheck(0)
            else:
                if template.At("otmOnly").AsString() == "True":
                    self.otmOnly.SetCheck(1)
                else:
                    self.otmOnly.SetCheck(0)
        else:
            self.otmOnly.SetCheck(0)
            
        if template.At("strikeRange"):
            self.strikeRange.SetData(template.At("strikeRange"))
        else:
            self.strikeRange.SetData(80.0)
            
        if template.At("expiryLimit"):
            self.expiryLimit.SetData(template.At("expiryLimit"))
        else:
            self.expiryLimit.SetData(0.05)
            
        if template.At("longExpiryLimit"):
            self.longExpiryLimit.SetData(template.At("longExpiryLimit"))
        else:
            self.longExpiryLimit.SetData(10.0)
            
        """ Kappa Ranges """
        if template.At("kappaMin"):
            self.kappaMin.SetData(template.At("kappaMin"))
        else:
            self.kappaMin.SetData(0.1)
            
        if template.At("kappaMax"):
            self.kappaMax.SetData(template.At("kappaMax"))
        else:
            self.kappaMax.SetData(3.0)
            
        """ V0 Ranges """
        if template.At("v0Min"):
            self.v0Min.SetData(template.At("v0Min"))
        else:
            self.v0Min.SetData(0.05)
            
        if template.At("v0Max"):
            self.v0Max.SetData(template.At("v0Max"))
        else:
            self.v0Max.SetData(1.5)
            
        """ Theta Ranges """
        if template.At("thetaMin"):
            self.thetaMin.SetData(template.At("thetaMin"))
        else:
            self.thetaMin.SetData(0.05)
            
        if template.At("thetaMax"):
            self.thetaMax.SetData(template.At("thetaMax"))
        else:
            self.thetaMax.SetData(1.5)
            
        """  VolVol Ranges """
        if template.At("volVolMin"):
            self.volVolMin.SetData(template.At("volVolMin"))
        else:
            self.volVolMin.SetData(0.1)
            
        if template.At("volVolMax"):
            self.volVolMax.SetData(template.At("volVolMax"))
        else:
            self.volVolMax.SetData(2.0)
            
        """  Rho Ranges """
        if template.At("rhoMin"):
            self.rhoMin.SetData(template.At("rhoMin"))
        else:
            self.rhoMin.SetData(-0.95)
            
        if template.At("rhoMax"):
            self.rhoMax.SetData(template.At("rhoMax"))
        else:
            self.rhoMax.SetData(0.95)
        
        """ Algorithm Settings """
        if template.At("deTol"):
            self.deTol.SetData(template.At("deTol"))
        else:
            self.deTol.SetData(0.001)
            
        if template.At("deIter"):
            self.deIter.SetData(template.At("deIter"))
        else:
            self.deIter.SetData(200)
            
        if template.At("popSize"):
            self.popSize.SetData(template.At("popSize"))
        else:
            self.popSize.SetData(50)
            
        if template.At("crProb"):
            self.crProb.SetData(template.At("crProb"))
        else:
            self.crProb.SetData(0.7)
            
        if template.At("diffWeight"):
            self.diffWeight.SetData(template.At("diffWeight"))
        else:
            self.diffWeight.SetData(0.9)
            
        if template.At("lmTol"):
            self.lmTol.SetData(template.At("lmTol"))
        else:
            self.lmTol.SetData(0.001)
            
        if template.At("lmIter"):
            self.lmIter.SetData(template.At("lmIter"))
        else:
            self.lmIter.SetData(100)
            
        if template.At("lmTau"):
            self.lmTau.SetData(template.At("lmTau"))
        else:
            self.lmTau.SetData(0.001)

        if template.At("lmDiffStep"):
            self.lmDiffStep.SetData(template.At("lmDiffStep"))
        else:
            self.lmDiffStep.SetData(0.001)
            
        if template.At("glTol"):
            self.glTol.SetData(template.At("glTol"))
        else:
            self.glTol.SetData("1e-006")
            
        if template.At("glUpperBound"):
            self.glUpperBound.SetData(template.At("glUpperBound"))
        else:
            self.glUpperBound.SetData(1000.0)

    def OnSaveSettings(self, *more):
        name      = "HestonCalibrationSettings"
        context   = acm.GetDefaultContext()

        extension = context.GetExtension("FParameters", "FObject", name)
        clone     = extension.Clone()
        template  = clone.Value()

        """ 1. Top Level Settings """
        template.AtPut("algorithm", self.algorithm.GetData())
        template.AtPut("formula", self.formula.GetData())
        template.AtPut("benchmark", self.benchmark.GetData())
        
        if self.logging.Checked():
            template.AtPut("logging", "True")
        else:
            template.AtPut("logging", "False")
            
            
        """ 2. Parameter Tab Settings """
        if self.otmOnly.Checked():
            template.AtPut("otmOnly", "True")
        else:
            template.AtPut("otmOnly", "False")
            
        template.AtPut("strikeRange", self.strikeRange.GetData())
        template.AtPut("expiryLimit", self.expiryLimit.GetData())
        template.AtPut("longExpiryLimit", self.longExpiryLimit.GetData())
            
        """ Kappa Ranges """
        template.AtPut("kappaMin", self.kappaMin.GetData())
        template.AtPut("kappaMax", self.kappaMax.GetData())
        template.AtPut("v0Min", self.v0Min.GetData())
        template.AtPut("v0Max", self.v0Max.GetData())
        template.AtPut("thetaMin", self.thetaMin.GetData())
        template.AtPut("thetaMax", self.thetaMax.GetData())
        template.AtPut("volVolMin", self.volVolMin.GetData())
        template.AtPut("volVolMax", self.volVolMax.GetData())
        template.AtPut("rhoMin", self.rhoMin.GetData())
        template.AtPut("rhoMax", self.rhoMax.GetData())
        
        """ Algorithm Settings """
        template.AtPut("deTol", self.deTol.GetData())
        template.AtPut("deIter", self.deIter.GetData())
        template.AtPut("popSize", self.popSize.GetData())
        template.AtPut("crProb", self.crProb.GetData())
        template.AtPut("diffWeight", self.diffWeight.GetData())
        
        template.AtPut("lmTol", self.lmTol.GetData())
        template.AtPut("lmIter", self.lmIter.GetData())
        template.AtPut("lmTau", self.lmTau.GetData())
        template.AtPut("lmDiffStep", self.lmDiffStep.GetData())
        
        template.AtPut("glTol", self.glTol.GetData())
        template.AtPut("glUpperBound", self.glUpperBound.GetData())        
        
        module = context.EditModule()
        module.AddExtension(clone)
        module.Commit()
            
    def GetCurrentParameters(self):
        kappa  = float(self.kappaIni.GetData())
        v0     = float(self.v0Ini.GetData())
        theta  = float(self.thetaIni.GetData())
        volVol = float(self.volVolIni.GetData())
        rho    = float(self.rhoIni.GetData())
        
        self.m_hestonParams = [kappa, v0, theta, volVol, rho]            
        
    def CreateTopLinks(self, layout):
        """ Create Binding for the controls in the "top" part of the GUI """
        self.algorithm    = layout.GetControl("algorithm")
        self.formula      = layout.GetControl("formula")
        self.benchmark    = layout.GetControl("benchmark")
        self.logging      = layout.GetControl("logging")
        self.calibrate    = layout.GetControl("calibrate")
        self.initialVal   = layout.GetControl("initialValues")
        self.saveSettings = layout.GetControl("saveSettings")
        
    def CreateResultLinks(self, layout):
        """ Create Binding for the controls in the "standard" part of the GUI """    
        self.kappaIni     = layout.GetControl("kappaIni")
        self.v0Ini        = layout.GetControl("v0Ini")
        self.thetaIni     = layout.GetControl("thetaIni")
        self.volVolIni    = layout.GetControl("volVolIni")
        self.rhoIni       = layout.GetControl("rhoIni")
        self.kappaRes     = layout.GetControl("kappaRes")
        self.v0Res        = layout.GetControl("v0Res")
        self.thetaRes     = layout.GetControl("thetaRes")
        self.volVolRes    = layout.GetControl("volVolRes")
        self.rhoRes       = layout.GetControl("rhoRes")
        self.maxRelError  = layout.GetControl("maxRelError")
        self.avgRelError  = layout.GetControl("avgRelError")
        self.minimumError = layout.GetControl("minimumError")
        self.timeTaken    = layout.GetControl("timeTaken")
        self.iterations   = layout.GetControl("iterations")
        self.simulate     = layout.GetControl("simulate")
        self.unsimulate   = layout.GetControl("unsimulate")
        self.commit       = layout.GetControl("commit")
                
    def CreateParameterLinks(self, layout):
        """ Create Binding for the controls in the parameter part of the GUI """    
        self.otmOnly         = layout.GetControl("otmOnly")
        self.strikeRange     = layout.GetControl("strikeRange")
        self.expiryLimit     = layout.GetControl("expiryLimit")
        self.longExpiryLimit = layout.GetControl("longExpiryLimit")
        
        self.kappaMin        = layout.GetControl("kappaMin")
        self.v0Min           = layout.GetControl("v0Min")
        self.thetaMin        = layout.GetControl("thetaMin")
        self.volVolMin       = layout.GetControl("volVolMin")
        self.rhoMin          = layout.GetControl("rhoMin")
        
        self.kappaMax        = layout.GetControl("kappaMax")
        self.v0Max           = layout.GetControl("v0Max")
        self.thetaMax        = layout.GetControl("thetaMax")
        self.volVolMax       = layout.GetControl("volVolMax")
        self.rhoMax          = layout.GetControl("rhoMax")
        
        
    def CreateAdvancedLinks(self, layout):
        self.deTol        = layout.GetControl("deTol")
        self.deIter       = layout.GetControl("deIter")
        self.popSize      = layout.GetControl("popSize")
        self.crProb       = layout.GetControl("crProb")
        self.diffWeight   = layout.GetControl("diffWeight")
        self.lmTol        = layout.GetControl("lmTol")
        self.lmIter       = layout.GetControl("lmIter")        
        self.lmTau        = layout.GetControl("lmTau")        
        self.lmDiffStep   = layout.GetControl("lmDiffStep")        
        self.glTol        = layout.GetControl("glTol")        
        self.glUpperBound = layout.GetControl("glUpperBound")
        
        
    def PopulateTopData(self):
        """ Add info to algorithm list """
        self.algorithm.AddItem("Levenberg-Marquardt (Local)")
        self.algorithm.AddItem("Differential Evolution (Global)")
        
        """ Add info to formula list """
        self.formula.AddItem("Semi-Analytical (Numerical Integration)")
        self.formula.AddItem("Closed Form (Expansion Based)")
        
        """ Add Info to benchmark list """
        self.benchmark.AddItem("Market Prices")
        self.benchmark.AddItem("Implied Volatilities")

        
    def CreateTopDlg(self):
        top = acm.FUxLayoutBuilder()
        top.BeginVertBox('None')
        top.  BeginVertBox('EtchedIn', 'General Settings')
        top.    AddOption('algorithm', 'Algorithm')
        top.    AddOption('formula', 'Formula')
        top.    AddOption('benchmark', 'Benchmarks')
        top.  EndBox()
        top.  BeginHorzBox('EtchedIn', None)
        top.    AddCheckbox('logging', 'Logging')
        top.    AddFill()
        top.    AddButton( 'saveSettings', 'Save Settings')
        top.    AddButton( 'initialValues', 'Calc Initial Values')
        top.    AddButton( 'calibrate', 'Calibrate')
        top.  EndBox()
        top.EndBox()
        
        return top
        
    def CreateResultPane(self):
        std = acm.FUxLayoutBuilder()
        std.BeginVertBox('None')        
        std.  BeginHorzBox('None')
        std.    BeginVertBox('EtchedIn', 'InitialValues')
        std.      AddInput( 'kappaIni', 'Speed of Mean Reversion')
        std.      AddInput( 'v0Ini', 'Initial Volatility')
        std.      AddInput( 'thetaIni', 'Long Term Volatility')
        std.      AddInput( 'volVolIni', 'Vol of Vol')
        std.      AddInput( 'rhoIni', 'Correlation')
        std.    EndBox()
        std.    BeginVertBox('EtchedIn', 'Error Measures')
        std.      AddInput( 'maxRelError', 'Max Rel Error')
        std.      AddInput( 'avgRelError', 'Avg Rel Error')
        std.      AddInput( 'minimumError', 'Least Squares Error')
        std.      AddInput( 'timeTaken', 'Time Taken')
        std.      AddInput( 'iterations', 'Iterations')
        std.    EndBox()
        std.  EndBox()
        std.  BeginHorzBox('EtchedIn', 'Calibration Results')
        std.    BeginVertBox('EtchedIn', '')
        std.      AddInput( 'kappaRes', 'Speed of Mean Reversion')
        std.      AddInput( 'v0Res', 'Initial Volatility')
        std.      AddInput( 'thetaRes', 'Long Term Volatility')
        std.      AddInput( 'volVolRes', 'Vol of Vol')
        std.      AddInput( 'rhoRes', 'Correlation')
        std.    EndBox()
        std.  EndBox()
        std.  BeginHorzBox('None')
        std.    AddFill()
        std.    AddButton( 'simulate', 'Simulate')
        std.    AddButton( 'unsimulate', 'Unsimulate')
        std.    AddButton( 'commit', 'Commit')
        std.  EndBox()
        std.EndBox()
        
        
        return std
            
    def CreateParameterPane(self):
        param = acm.FUxLayoutBuilder()
        param.BeginVertBox('EtchedIn', '')
        param.  BeginHorzBox('EtchedIn', 'Benchmark Settings')
        param.    BeginVertBox('EtchedIn', 'Benchmark Selection Settings')    
        param.      AddCheckbox('otmOnly', 'Use OTM Options Only')
        param.      AddInput('strikeRange', 'Strike Range (% from ATM)')
        param.      AddInput('expiryLimit', 'Short Expiry Limit')
        param.      AddInput('longExpiryLimit', 'Long Expiry Limit')
        param.    EndBox() 
        param.  EndBox()
        
        param.  BeginHorzBox('EtchedIn', 'Parameter Ranges')
        param.    BeginVertBox('EtchedIn', 'Min Values')
        param.      AddInput('kappaMin', 'Speed of Mean Reversion')
        param.      AddInput('v0Min', 'Initial Volatility')
        param.      AddInput('thetaMin', 'Long Term Volatility')
        param.      AddInput('volVolMin', 'Vol of Vol')
        param.      AddInput('rhoMin', 'Correlation')     
        param.    EndBox()
        param.    BeginVertBox('EtchedIn', 'Max Values')
        param.      AddInput('kappaMax', 'Speed of Mean Reversion')
        param.      AddInput('v0Max', 'Initial Volatility')
        param.      AddInput('thetaMax', 'Long Term Volatility')
        param.      AddInput('volVolMax', 'Vol of Vol')
        param.      AddInput('rhoMax', 'Correlation')     
        param.    EndBox()
        param.  EndBox()
        param.EndBox()
        
        return param
        
    def CreateAdvancedPane(self):
        adv = acm.FUxLayoutBuilder()
        
        adv.BeginVertBox('EtchedIn', '')
        adv.  BeginHorzBox('EtchedIn', 'Optimization Settings')
        
        adv.    BeginVertBox('EtchedIn', 'Levenberg-Marquardt Settings')
        adv.      AddInput('lmTol', 'Tolerance')
        adv.      AddInput('lmIter', 'MaxIter' )
        adv.      AddInput('lmDiffStep', 'Shift Size (Jacobian)')
        adv.      AddInput('lmTau', 'Tau')
        adv.    EndBox()  
        
    
        adv.    BeginVertBox('EtchedIn', 'Differential Evolution Settings')
        adv.      AddInput('deTol', 'Tolerance')
        adv.      AddInput('deIter', 'Max Simulations' )
        adv.      AddInput('popSize', 'Population Size')
        adv.      AddInput('crProb', 'Cross Over Probability' )
        adv.      AddInput('diffWeight', 'Differential Weight' )
        adv.    EndBox()
        
        adv.  EndBox()
        
        adv.  BeginHorzBox('EtchedIn', 'Numerical Integration Settings')
        adv.    AddInput('glTol', ' Tolerance')
        adv.    AddInput('glUpperBound', 'Upper Bound')
        adv.  EndBox()
        
        adv.EndBox()
        return adv
       
    def AddCallbacks(self):
        self.calibrate.AddCallback("Activate", self.OnCalibrate, self)
        self.initialVal.AddCallback("Activate", self.OnCalcInitialValues, self)
        self.saveSettings.AddCallback("Activate", self.OnSaveSettings, self)
        self.simulate.AddCallback("Activate", self.OnSimulate, self)
        self.unsimulate.AddCallback("Activate", self.OnUnsimulate, self)
        self.commit.AddCallback("Activate", self.OnCommit, self)
        
    def OnCalibrate(self, *more):
        logging    = 0
        parameters = 0
        
        if self.logging.Checked():
            logging = 1
        
        """ Extract settings for the numerical algorithm from the GUI """
        try:
            lmTol     = float(self.lmTol.GetData())
            lmIter    = int(self.lmIter.GetData())
            deTol     = float(self.deTol.GetData())
            deIter    = int(self.deIter.GetData())
            popSize   = int(self.popSize.GetData())
            crProb    = float(self.crProb.GetData())
            weight    = float(self.diffWeight.GetData())
            diffStep  = float(self.lmDiffStep.GetData())
            lmTau     = float(self.lmTau.GetData())
            
            if self.formula.GetData() == "Closed Form (Expansion Based)":
                useFastForm = 1
            else:
                useFastForm = 0

        except Exception as e:
            message = "Missing or erroneous settings for optimization algorithm: " + str(e)
            acm.UX().Dialogs().MessageBoxInformation(self.m_shell, message)
            return None
            
            
        """ Extract settings for the parameter ranges from the GUI """        
        try:
            kappaMin  = self.kappaMin.GetData()
            kappaMax  = self.kappaMax.GetData()
            thetaMin  = self.thetaMin.GetData()
            thetaMax  = self.thetaMax.GetData()
            v0Min     = self.v0Min.GetData()
            v0Max     = self.v0Max.GetData()
            volVolMin = self.volVolMin.GetData()
            volVolMax = self.volVolMax.GetData()
            rhoMin    = self.rhoMin.GetData()
            rhoMax    = self.rhoMax.GetData()
            
        except Exception as e:
            message = "Missing or erroneous settings for parameter ranges: " + str(e)
            acm.UX().Dialogs().MessageBoxInformation(self.m_shell, message)
            return None
            
        try:
            kappaIni  = self.kappaIni.GetData()
            v0Ini     = self.v0Ini.GetData()
            thetaIni  = self.thetaIni.GetData()
            volVolIni = self.volVolIni.GetData()
            rhoIni    = self.rhoIni.GetData()
            
        except Exception as e:
            message = "Missing or erroneous settings for Initial Value: " + str(e)
            acm.UX().Dialogs().MessageBoxInformation(self.m_shell, message)
            return None
        
        
        """ Write data into structures that are handled by the Calibration Algorithm """
        method      = self.algorithm.GetData() 
        strikeRange  = float(self.strikeRange.GetData())
        expiryLimit  = float(self.expiryLimit.GetData())
        otmOnly         = self.otmOnly.Checked()
        strikeRange     = float(self.strikeRange.GetData())
        expiryLimit     = float(self.expiryLimit.GetData())
        longExpiryLimit = float(self.longExpiryLimit.GetData())
        glTol           = float(self.glTol.GetData())
        glUpperBound    = float(self.glUpperBound.GetData())
        
        calibrationBenchmark = self.benchmark.GetData()
        
        volStruct = self.m_parentObject
        
        glTol = max(1.0e-14, glTol)
        glUpperBound = max(60.0, glUpperBound)
            
        parameterInformation = volStruct.ParameterInformation(method, lmTol, lmIter, deTol, deIter, popSize, crProb, weight, useFastForm, glTol, glUpperBound, calibrationBenchmark, kappaIni, v0Ini, thetaIni, volVolIni, rhoIni, kappaMin, kappaMax, v0Min, v0Max, thetaMin, thetaMax, volVolMin, volVolMax, rhoMin, rhoMax, otmOnly, strikeRange, expiryLimit, longExpiryLimit)

        result = volStruct.Calibrate(parameterInformation) 
        
                    
        parameters = result.At("parameters")
        minimum    = result.At("minimum")
        iter       = result.At("iterations")
        tElapsed   = 0.0
        maxDiff    = result.At("maxRelDiff")
        avDiff     = result.At("avRelDiff")

        if parameters:
            try:
            
                """ The calibration algorithm works with variances so we need to convert to volatility terms before we insert v0 and theta into the GUI fields """
                
                self.kappaRes.SetData(parameters[0])
                self.v0Res.SetData(parameters[1])
                self.thetaRes.SetData(parameters[2])                        
                self.volVolRes.SetData(parameters[3])
                self.rhoRes.SetData(parameters[4])  

                self.minimumError.SetData(minimum)
                self.timeTaken.SetData(tElapsed)
                self.iterations.SetData(iter)
                self.maxRelError.SetData(maxDiff)          
                self.avgRelError.SetData(avDiff)
                
                    
            except Exception as e:
                self.m_parentObject.Undo()
                message = 'Error Applying result to structure: ' + str(e)
                acm.UX().Dialogs().MessageBoxInformation(self.m_shell, message)
                
    def GetExpiryArray(self):
        result = []    
        points = self.m_parentObject.Points()
        for point in points:
            expiry = point.ActualExpiryDay()
            if expiry not in result:
                result.append(expiry)
                
        result.sort()
        
        return result
                
    def OnCalcInitialValues(self, *more):
        expiries        = self.GetExpiryArray()
        if len(expiries) < 3:
            message = 'Error estimating initial values: Need at least 3 skews to estimate initial values from asymptotics' 
            acm.UX().Dialogs().MessageBoxInformation(self.m_shell, message)
            return
            
        otmOnly         = self.otmOnly.Checked()
        strikeRange     = float(self.strikeRange.GetData())
        expiryLimit     = float(self.expiryLimit.GetData())
        longExpiryLimit = float(self.longExpiryLimit.GetData())
        self.startValues = self.m_parentObject.GetStartValues()
        
        self.kappaIni.SetData(self.startValues[0])
        self.v0Ini.SetData(self.startValues[1])
        self.thetaIni.SetData(self.startValues[2])
        self.volVolIni.SetData(self.startValues[3])
        self.rhoIni.SetData(self.startValues[4])

    def OnSimulate(self, *more):
        try:
            kappaRes  = float(self.kappaRes.GetData())
            v0Res     = float(self.v0Res.GetData())
            thetaRes  = float(self.thetaRes.GetData())
            volVolRes = float(self.volVolRes.GetData())
            rhoRes    = float(self.rhoRes.GetData())
        except:            
            try:
                kappaRes  = float(self.kappaIni.GetData())
                v0Res     = float(self.v0Ini.GetData())
                thetaRes  = float(self.thetaIni.GetData())
                volVolRes = float(self.volVolIni.GetData())
                rhoRes    = float(self.rhoIni.GetData())
                print ("Heston Studio: Calibration results are missing, using intitial values")
            except:
                message = 'Missing or erroneous values for Heston Parameters: Cannot simulate parameters'
                acm.UX().Dialogs().MessageBoxInformation(self.m_shell, message)
                return 0          
                    
        if self.m_parentObject.IsSimulated():
            self.m_parentObject.Unsimulate()
            
        clone = self.m_parentObject.Clone()
        clone.SpeedOfMeanReversion(kappaRes)
        clone.InitialVolatility(v0Res)
        clone.LongTermMeanVol(thetaRes)
        clone.VolOfVol(volVolRes)
        clone.UndVolCorr(rhoRes)
        
        print ("Heston Studio: Simulating Heston Parameters...")
        
        self.m_parentObject.Apply(clone)
        
    def OnUnsimulate(self, *more):
        print  ("Heston Studio: Unsimulating Heston Parameters...")
        self.m_parentObject.Undo()
        
    def OnCommit(self, *more):
        try:
            kappaRes  = float(self.kappaRes.GetData())
            v0Res     = float(self.v0Res.GetData())
            thetaRes  = float(self.thetaRes.GetData())
            volVolRes = float(self.volVolRes.GetData())
            rhoRes    = float(self.rhoRes.GetData())
            
            clone = self.m_parentObject.Clone()
            clone.SpeedOfMeanReversion(kappaRes)
            clone.InitialVolatility(v0Res)
            clone.LongTermMeanVol(thetaRes)
            clone.VolOfVol(volVolRes)
            clone.UndVolCorr(rhoRes)
            self.m_parentObject.Apply(clone)
            self.m_parentObject.Commit()
        except:            
            message = 'Missing or erroneous values for Calibrated Heston Parameters: Cannot commit'
            acm.UX().Dialogs().MessageBoxInformation(self.m_shell, message)
            return 0          
        

def CreateLayout():
    builder = acm.FUxLayoutBuilder()
    
    """ Layout for the Bottom part of GUI """
    builder.   BeginHorzBox('None')
    builder.   EndBox()
        
    return builder
    
