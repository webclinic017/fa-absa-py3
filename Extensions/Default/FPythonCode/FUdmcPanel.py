from __future__ import print_function
"""GUI for working with UDMC valued instruments

 Note use of this module requires the separatly licensed AEF for UDMC module

 To activate add the following as an FUiEventHandlers extension",

 CInsDefAppFrame:FUdmcPanelDockWindow =
  ContentsChanged=
  OnCreate=FUdmcPanel.OnCreate

(c) Copyright 2011 by Sungard FRONT ARENA. All rights reserved.

"""
import traceback
import acm
import FUxCore
import time

class UdmcUtilsLogic:
    """ 'Model' part of the UDMCpanel"""
    
    def __init__(self, ins):
        """Create, basedd on one instrument which should be UDMC valued"""
        self.ins = ins
        ins.AddDependent(self)
        self.context = acm.GetDefaultContext()
        self.calc_space = acm.Calculations().CreateCalculationSpace( self.context, "FOrderBookSheet" )
        self.calc_space.SimulateValue(self.ins, "Underlying Price Source", "ADS")
        self.subscribers = set()
    
    def ClearCalcs(self):
        self.calc_space = acm.Calculations().CreateCalculationSpace( self.context, "FOrderBookSheet" )
        self.calc_space.SimulateValue(self.ins, "Underlying Price Source", "ADS")
    
    def close(self):
        """Close this model and terminate FObject based subscriptions"""
        self.ins.RemoveDependent(self)
        
    def subscribe(self, update_cb):
        """Subscribe to changes in model, update_cb is any callabel"""
        self.subscribers.add(update_cb)
    
    def unsubscribe(self, update_cb):
        """UnSubscribe to changes in model"""
        self.subscribers.remove(update_cb)

    def ServerUpdate(self, sender, aspect, parameter ):
        """Callback from FObjects, in this case only the instruemnt"""
        for subscriber in self.subscribers:
            subscriber()
    
    def Instrument(self):
        return self.ins
            
    def PayoffCode(self):        
        if self.PayoffName():
            userDefPayoff = self.context.GetExtension("FUserDefinedPayoff", "FObject", self.PayoffName() )    
            return userDefPayoff.Value()
        else:
            return None    
            
    def GetEditModule(self):
        editModule = self.context.EditModule()
        if editModule.IsBuiltIn():
            try:
                editModule = [mod for mod in reversed(self.context.Modules()) if not mod.IsBuiltIn()][0]
            except IndexError:
                return None
        return editModule
            
    def SetPayoffCode(self, newcode):
        """Save changes to PEL code and update GUI"""
        func = acm.GetFunction("createUDMCScriptPayoffForParsing", 1)
        func(newcode)
        if self.PayoffName():
            editModule = self.GetEditModule()
            if editModule:
                moduleName = editModule.Name()
                text = '[%s]%s:%s\n%s\n¤' %(moduleName, "FObject", self.PayoffName(), newcode )
                self.context.EditImport('FUserDefinedPayoff', text, False, editModule)
                editModule.Commit()
            else:
                print ("All modules in default context are built-in. Can't save PEL code.")
        else:
            print ("No PEL code is assosciated with this instrument. Can't save.")
    
    def PayoffName(self):
        return self.calc_space.CalculateValue( self.ins, "UDMC Payoff" )

    def Simulations(self):        
        return self.calc_space.CalculateValue( self.ins, "UDMC Simulations" )

    def StandardDeviation(self):
        return self.calc_space.CalculateValue( self.ins, "UDMC Standard Deviation" )

    def Theor(self):        
        try:
            return self.calc_space.CalculateValue( self.ins, "Price Theor" ).Number()
        except Exception as err:            
            print ("FUDMCPanel:Problem calculating theor:",err)
            #value = self.calc_space.CreateCalculation( self.ins, "Price Theor" )
            #acm.StartApplication("Valuation Viewer", value)
            return theor

    def TheorModelDict(self):
        theordict = self.calc_space.CalculateValue( self.ins, "UDMC Theor Model Call" )
        res = []
        for key in sorted(theordict.Keys()):
            res.append( str(key).ljust(15) + " --> " + str(theordict[key]) )
        return "\n".join(res)
    
    def AvailableVars(self):
        vardict = self.calc_space.CalculateValue( self.ins, "UDMC Ext Dict" )
        if vardict:
            return sorted([str(key) + " : " + str(type(vardict[key]).__name__) for key in vardict.Keys()], key=str.upper)
        return [ "No variables available" ]
    
                
class UDMCInsdefPanel (FUxCore.LayoutPanel):
    """ 'View' part of the UDMCPanel """

    def __init__(self, model_class):
        self.clear_variables()
        self._model_class = model_class
        
    def clear_variables(self) :
        self.m_bindings = None
        self.uxPelCode = None
        self.uxDebugInfo = None
        self.uxAllVars = None
        self.layout = None
        self.model = None
        self.saveCode = None
        self.set_model(None)
        self.m_simulations = None
        self.m_payoffName = None
        self.m_stdDev = None
        self.m_theor = None

    def UpdateUI(self):
        try:            
            try:
                ins = self.Owner().OriginalInstrument() 
            except RuntimeError:
                # If this fails we are being or have been closed
                ins = None
            if ins:
                if self.model and self.model.Instrument() != ins:
                    self.set_model(None)                    
                if not self.model:
                    model = self._model_class(ins)
                    if model.PayoffName():
                        self.set_model( model )
                    else:
                        model.close()
            else:
                self.set_model(None)
            if self.model:
                startt = time.clock()
                while time.clock() <  startt + 2:                
                    try:                    
                        self.m_simulations.SetValue( self.model.Simulations() )
                        self.m_payoffName.SetValue( self.model.PayoffName() )
                        self.m_stdDev.SetValue( self.model.StandardDeviation() )
                        self.m_theor.SetValue( self.model.Theor() )
                        self.uxPelCode.SetData( self.model.PayoffCode() )
                        self.uxDebugInfo.SetData( self.model.TheorModelDict() )                
                        self.uxAllVars.Clear()
                        for var in self.model.AvailableVars():
                            self.uxAllVars.AddItem(var)                                                            
                        startt = -9999
                    except Exception as err:
                        if time.clock() >  startt + 2:
                            raise
                        time.sleep(0.1)
            else:
                self.clear_all_fields( "This is not a UDMC instrument" )
        except Exception as err:
            self.clear_all_fields( "Problem with instrument: " + str(err) )
            traceback.print_exc()
    
    def clear_all_fields(self, msg):
        for key, obj in self.__dict__.items():
            if hasattr(obj, "IsKindOf"):                    
                if obj.IsKindOf(acm.FUxControl):
                    obj.Clear()
                if obj.IsKindOf(acm.FUxDataBinder):
                    obj.SetValue("", False)                   
        self.uxPelCode.SetData( msg )

    def set_model(self, newmodel):
        if self.model:
            self.model.unsubscribe(self.OnModelUpdate)
            self.model.close()
        self.model = newmodel
        if self.model:
            self.model.subscribe(self.OnModelUpdate)
    
    def OnModelUpdate(self):
        self.UpdateUI()
        
    def ServerUpdate(self, sender, aspect, parameter ):
        self.UpdateUI()

    def HandleCreate( self ):
        self.m_bindings = acm.FUxDataBindings()
        self.m_simulations = self.m_bindings.AddBinder( 'nbrSimulations', acm.GetDomain('string'), None )
        self.m_payoffName = self.m_bindings.AddBinder( 'payoffName', acm.GetDomain('string'), None )
        self.m_stdDev = self.m_bindings.AddBinder( 'stdDev', acm.GetDomain('string'), None )
        self.m_theor = self.m_bindings.AddBinder( 'theor', acm.GetDomain('string'), None ) 
        self.layout = self.SetLayout( self.CreateLayout() )
        self.m_bindings.AddLayout(self.layout)
        self.m_bindings.AddLayout(self.layout)
        
        # Handle controls which don't have binders
        self.uxAllVars = self.layout.GetControl("allVars")
        self.uxAllVars.AddCallback( "DefaultAction", self.OnVarClicked, 'default')
        self.uxPelCode = self.layout.GetControl("pelCode")
        self.uxPelCode.SetFont("Consolas",10, False, False)
        self.uxPelCode.MaxTextLength(9999)
        self.uxDebugInfo = self.layout.GetControl("debugInfo")        
        self.uxDebugInfo.SetFont("Consolas",8, True, False)
        self.uxDebugInfo.SetColor("Background", acm.UX().Colors().Create(0,0,0) )
        self.uxDebugInfo.SetColor("Text", acm.UX().Colors().Create(0,255,0) )        
        self.saveCode = self.layout.GetControl('saveCode')
        self.saveCode.AddCallback( "Activate", self.OnSaveCodeClicked, None)
        # Add general callback
        self.Owner().AddDependent(self)        
        for ctrl in [self.m_theor, self.m_payoffName, self.m_stdDev, self.m_simulations]: 
            ctrl.Enabled(False)
        self.UpdateUI()
    
    def HandleDestroy(self):
        self.clear_variables()
        
    def CreateLayout( self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()

        b.  BeginHorzBox('EtchedIn', 'Model infor');
        self.   m_payoffName.BuildLayoutPart(b, 'payoffName')
        b.    AddFill()
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn', 'Parameters');
        self.   m_simulations.BuildLayoutPart(b, 'Nbr of sims')
        b.    AddFill()
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Code');        
        b.    BeginHorzBox()        
        b.      AddList("allVars", -1, -1, 20)
        b.      AddText("pelCode", 500, 500, -1, -1)
        b.    EndBox()
        b.    BeginHorzBox()        
        b.      AddFill()
        b.      AddButton('saveCode', 'Save Changes')
        b.    EndBox()
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn', 'Calculations')
        self.   m_theor.BuildLayoutPart(b, 'theor')
        self.   m_stdDev.BuildLayoutPart(b, 'stdDev')        
        b.    AddFill()
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn', 'Debugging');        
        b.    AddText("debugInfo", 500, 200, -1, -1)
        b.  EndBox()        
        b.EndBox()
        return b

    def OnSaveCodeClicked(self, *args):
        try:
            self.model.SetPayoffCode( self.uxPelCode.GetData() )
        except Exception as err:        
            self.uxDebugInfo.SetData( "Error updating PEL code:\n" + str(err) )            
            return                
        acm.PollDbEvents()
        self.set_model(None)
        self.UpdateUI()
        self.Owner().SetContents( self.Owner().OriginalInstrument() )  
        
    def OnRefreshClicked(self, *args):
        self.UpdateUI()
        
    def OnVarClicked(self, *args):
        txt = self.uxAllVars.GetData()
        if txt:
            varname, vartype = txt.split(" : ")
            self.uxPelCode.InsertTextAtCursor(varname)
  
def OnCreate(eii):
    """Called from UIEventHandler when insdef is opened"""
    basicApp = eii.ExtensionObject()
    myPanel = UDMCInsdefPanel(UdmcUtilsLogic)
    showInitialy = False
    basicApp.CreateCustomDockWindow(myPanel, 'udmcPanel', 'UDMC Panel', 'Right', "", False, showInitialy)
