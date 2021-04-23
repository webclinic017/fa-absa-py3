import acm
import FUxCore
import FRunScriptGUI

PRICE_MARKETS = ['SPOT']

def Valuationparams():
    #Parameter override and valuation param
    pars   = []
    params = []
    pars.extend(acm.FParameterMapping.Select('overrideLevel="Global"'))
    paramTypes = ['Valuation Par']
    for pm in pars:
        for pmi in pm.ParMappingInstances():
            if pmi.ParameterType() in paramTypes:
                if pmi.ValuationParameters():
                    params.append(pmi.ValuationParameters())
    return params

def ParameterMapping():
    params = acm.FParameterMapping.Select('overrideLevel="Global"')
    if params:
        return params.At(0)
    return None
    
def GetUsedContext():
    #May need to remove User,Group and Org.
    user = acm.User()
    pars=[]
    context     = []
    pars.extend(acm.FParameterMapping.Select('overrideLevel="User" and user="%s"'%(user.Name())))
    pars.extend(acm.FParameterMapping.Select('overrideLevel="Group" and userGroup="%s"'%(user.UserGroup().Name())))
    pars.extend(acm.FParameterMapping.Select('overrideLevel="Organisation" and organisation="%s"'%(user.UserGroup().Organisation().Name())))
    pars.extend(acm.FParameterMapping.Select('overrideLevel="Global"'))
    paramType   ='Context Par'
    for pm in pars:
        for pmi in [pmi for pmi in pm.ParMappingInstances() if pmi.ParameterType() == paramType]:     
            c = pmi.Context()
            if c not in context:
                context.append(c)
    return context

def GetPrices(instruments):
    ins_prices = []
    for i in instruments:
        prices  = i.Prices()
        if prices:
            for p in prices:
                if p.Market().Name() in PRICE_MARKETS:
                    ins_prices.append(p)
    return ins_prices
    
def VolaBenchmarkInstruments(volas):
    instruments             = []
    for v in volas:
        type                    = v.StructureType()
        points                  = v.Points()
        if type in ("Benchmark", "Benchmark Call/Put", "Benchmark Spread", "Benchmark Spread Call/Put"):
              if points:
                for p in points:
                    b = p.Benchmark()
                    if b:
                        instruments.append(b.Instrument())
    return instruments
    
def BenchmarkInstruments(yield_curves):
    instruments         = []
    for curve in yield_curves:
        type                = curve.Type()
        if type in ("Benchmark", "Price"):
            benchmarks              = curve.BenchmarkInstruments()
            if benchmarks:
                for b in benchmarks:
                    ins             = b.Instrument()
                    instruments.append(ins)
                         
        elif type in ("Attribute Spread", "Benchmark Spread", "Spread"):
            benchmarks              = curve.Benchmarks()
            if benchmarks:
                for b in benchmarks:
                    ins             = b.Instrument()
                    instruments.append(ins)
                    
        elif type in ("Instrument Spread Bid/Ask", "Instrument Spread"):
            instrumentSpreads = curve.InstrumentSpreads()
            for s in instrumentSpreads:
                ins = s.Instrument()
                if ins:
                    instruments.append(ins)
    return instruments
    
def Mappings():
    contextLinks = []
    contexts     = GetUsedContext()
    for i in contexts:
        links = i.ContextLinks()
        if links:
            contextLinks.extend(links.AsList())
    return contextLinks

def ContextLinks(objects):
    contextLinks        = Mappings()
    objectNames         = [o.Name() for o in objects]
    mappings            = []
    for l in contextLinks:
        if l.Name() in objectNames:
            mappings.append(l)    
    return mappings
    
def ActionOnCurrClicked(self, *params):
    curves              = acm.FArray()
    volas               = acm.FArray()
    currs               = [r.GetData().Name() for r in self._currs.GetCheckedItems()]
    for c in currs:
        query           = "currency = '%s'" %(c)
        yc              = acm.FYieldCurve.Select(query)
        vs              = acm.FVolatilityStructure.Select(query)
        curves.AddAll(yc)
        volas.AddAll(vs)
        
    self._curves        = self.currecyLayout.GetControl('_curves')
    self._volas         = self.currecyLayout.GetControl('_volas')
    
    self._curves.ShowGridLines()
    self._curves.EnableMultiSelect()
    self._curves.ShowCheckboxes(True)
    self._curves.Populate(curves)  

  
    self._volas.ShowGridLines()
    self._volas.EnableMultiSelect()
    self._volas.ShowCheckboxes(True)
    self._volas.Populate(volas)   

def ActionOnCheckCheckAllCurrPairs(self, *params):
    currParisChecked  = self._check_all_currpairs.Checked()
    if currParisChecked:
        for item in list(self._currPairs.GetRootItem().Children()):
            item.Check(True)
    else:
        for item in list(self._currPairs.GetRootItem().Children()):
            item.Check(False)
        
        
def ActionOnCheckAllVolasClicked(self, *params):
    volaIsChecked  = self._check_all_volas.Checked()
    if self._curves:
        rootItem        = self._volas.GetRootItem()
        if volaIsChecked:
            for item in list(rootItem.Children()):
                item.Check(True)
        else:
            for item in list(rootItem.Children()):
                item.Check(False)
                
def ActionOnCheckAllCurvesClicked(self, *params):
    curveIsChecked  = self._check_all_curves.Checked()
    if self._curves:
        rootItem        = self._curves.GetRootItem()
        if curveIsChecked:
            for item in list(rootItem.Children()):
                item.Check(True)
        else:
            for item in list(rootItem.Children()):
                item.Check(False)
    
def ActionOnCheckAllCurrClicked(self, *params):
    currIsChecked   = self._check_all_curr.Checked()
    if currIsChecked:
        for item in list(self._currs.GetRootItem().Children()):
            item.Check(True)
    else:
        self._check_all_curves.Checked(False)
        self._check_all_volas.Checked(False)
        for item in list(self._currs.GetRootItem().Children()):
            item.Check(False)

def ActionOnPopulatePackage(self):
    objects                             = []
    curves                              = []
    volas                               = []
    
    if self._valpars:
        if self._valpars.GetCheckedItems():
            valpars                         = [r.GetData() for r in self._valpars.GetCheckedItems()]
            objects.extend(valpars)
            
    if self._accpars:
        if self._accpars.GetCheckedItems():
            accpars                         = [r.GetData() for r in self._accpars.GetCheckedItems()]
            objects.extend(accpars)
    """        
    if self._tasks:
        if self._tasks.GetCheckedItems():
            tasks                           = [r.GetData() for r in self._tasks.GetCheckedItems()]
            objects.extend(tasks)
    """
    if self._currs.GetCheckedItems():
        currency                        = [r.GetData() for r in self._currs.GetCheckedItems()]
        objects.extend(currency)
    """
    if self._portfolios.GetCheckedItems():
        portfolios                        = [r.GetData() for r in self._portfolios.GetCheckedItems()]
        objects.extend(portfolios)

    if self._users.GetCheckedItems():
        users                             = [r.GetData() for r in self._users.GetCheckedItems()]
        objects.extend(users)
    
    if self._parties.GetCheckedItems():
        parties                           = [r.GetData() for r in self._parties.GetCheckedItems()]
        objects.extend(parties)
    """    
    if self._curves:
        if self._curves.GetCheckedItems():
            curves                          = [r.GetData() for r in self._curves.GetCheckedItems()]
            curve_links                     = ContextLinks(curves)
            curveBenchmarks                 = BenchmarkInstruments(curves)
            curve_prices                    = GetPrices(curveBenchmarks)
            if curve_prices:
                market                      = curve_prices[0].Market()
                objects.extend(curve_prices)
                objects.append(market)
            objects.extend(curves)
            objects.extend(curve_links)
        
    if self._volas:
        if self._volas.GetCheckedItems():
            volas                           = [r.GetData() for r in self._volas.GetCheckedItems()]
            vola_links                      = ContextLinks(volas)
            volaBenchmarks                  = VolaBenchmarkInstruments(volas)
            vola_prices                     = GetPrices(volaBenchmarks)
            if vola_prices:
                objects.extend(vola_prices)
            objects.extend(volas)
            objects.extend(vola_links)
    
    if self._currPairs:
        if self._currPairs.GetCheckedItems():
            currpairs                       = [r.GetData() for r in self._currPairs.GetCheckedItems()]
            objects.extend(currpairs)
    
    
    valpars = Valuationparams()
    if valpars:
        objects.extend(valpars)
    #Parameter obeverides
    params  = ParameterMapping()
    if params:
        objects.append(params)
    return objects
        
class BuildPackageUIAcc (FUxCore.LayoutTabbedDialog):
    def __init__(self):
        self._currs              = None
        self._currPairs          = None
        self._check_all_curr     = None
        self._curves             = None
        self._volas              = None
        self._include_prices     = None
        
    def HandleCancel(self):
        return True
        
    def HandleApply(self):
        objects          =  ActionOnPopulatePackage(self)
        return objects
    """  
    def Tasks(self):
        tasks           = acm.FAelTask.Select('').SortByProperty('ModuleName',True)
        self._tasks     = self.adminLayout.GetControl('_tasks')
        self._tasks.ShowGridLines()
        self._tasks.EnableMultiSelect()
        self._tasks.ShowCheckboxes(True)
        self._tasks.Populate(tasks)
    """
    def ValPars(self):
        valpars         = acm.FValuationParameters.Select('')
        self._valpars     = self.adminLayout.GetControl('_valpars')
        self._valpars.ShowGridLines()
        self._valpars.EnableMultiSelect()
        self._valpars.ShowCheckboxes(True)
        self._valpars.Populate(valpars)
        
    def AccPars(self):
        accparams         = acm.FAccountingParameters.Select('')
        self._accpars     = self.adminLayout.GetControl('_accpars')
        self._accpars.ShowGridLines()
        self._accpars.EnableMultiSelect()
        self._accpars.ShowCheckboxes(True)
        self._accpars.Populate(accparams)
    """
    def Portfolios(self):
        portfolios            = acm.FCompoundPortfolio.Select('').AsList().AddAll(acm.FPhysicalPortfolio.Select(''))
        self._portfolios      = self.adminLayout.GetControl('_portfolios')
        self._portfolios.ShowGridLines()
        self._portfolios.EnableMultiSelect()
        self._portfolios.ShowCheckboxes(True)
        self._portfolios.Populate(portfolios) 

    def Users(self):
        users                 = acm.FUser.Select('').SortByProperty('UserGroup',True)
        self._users           = self.adminLayout.GetControl('_users')
        self._users.ShowGridLines()
        self._users.EnableMultiSelect()
        self._users.ShowCheckboxes(True)
        self._users.AddColumn('User',-1,'')
        self._users.AddColumn('User Group',-1,'')
        self._users.ShowColumnHeaders(True)
        rootItem = self._users.GetRootItem()
        
        for u in users:    
            child = rootItem.AddChild()
            child.Label(u.StringKey())
            child.Icon(u.Icon())
            child.SetData(u)
            child.Label(u.UserGroup().StringKey(),1)
        self._users.AdjustColumnWidthToFitItems(0)
        self._users.AdjustColumnWidthToFitItems(1)

    def Parties(self):
        parties                 = acm.FParty.Select('').SortByProperty('Type',True)
        self._parties           = self.adminLayout.GetControl('_parties')
        self._parties.ShowGridLines()
        self._parties.EnableMultiSelect()
        self._parties.ShowCheckboxes(True)
        self._parties.AddColumn('Party',-1,'')
        self._parties.AddColumn('Type',-1,'')
        self._parties.ShowColumnHeaders(True)
        rootItem = self._parties.GetRootItem()
        
        for u in parties:    
            child = rootItem.AddChild()
            child.Label(u.StringKey())
            child.Icon(u.Icon())
            child.SetData(u)
            child.Label(u.Type(),1)
        self._parties.AdjustColumnWidthToFitItems(0)
        self._parties.AdjustColumnWidthToFitItems(1)
    """
    def Currencies(self):
        currs           = acm.FCurrency.Select('')
        self._currs     = self.currecyLayout.GetControl('_currs')
        self._currs.ShowGridLines()
        self._currs.EnableMultiSelect()
        self._currs.ShowCheckboxes(True)
        self._currs.Populate(currs)
        
    def CurrencyParis(self):
        currPairs           = acm.FCurrencyPair.Select('')
        self._currPairs     = self.currecyLayout.GetControl('_currPairs')
        self._currPairs.ShowGridLines()
        self._currPairs.EnableMultiSelect()
        self._currPairs.ShowCheckboxes(True)
        self._currPairs.Populate(currPairs)
        
    def HandleCreate(self, dlg, layout):
        
        self.m_fuxDlg                   = dlg
        self._layout                    = layout

        self.m_fuxDlg.Caption('')
        #TopLayout
        topBuilder = acm.FUxLayoutBuilder()
        topBuilder.BeginVertBox('None')
        topBuilder.    AddLabel('BasicInfo', '')
        topBuilder.EndBox()
        topLayout = dlg.AddTopLayout( "Top", topBuilder )
        
        #Currency selection layout
        b = acm.FUxLayoutBuilder()
        b.BeginHorzBox('None')
        b.BeginVertBox('EtchedIn', 'Currency')
        b.  AddCheckbox('check_all_curr', 'Check/Un-check all')
        b.AddList('_currs', 25, -1, 30, -1);
        b.EndBox()
        b.BeginVertBox('EtchedIn', 'Curves')
        b.  AddCheckbox('check_all_curves', 'Check/Un-check all')
        b.AddList('_curves', 25, -1, 30, -1);
        b.EndBox()
        b.BeginVertBox('EtchedIn', 'Volatility')
        b.  AddCheckbox('check_all_volas', 'Check/Un-check all')
        b.AddList('_volas', 25, -1, 30, -1);
        b.EndBox()
        b.BeginVertBox('EtchedIn', 'Currency Pairs')
        b.  AddCheckbox('check_all_currpairs', 'Check/Un-check all')
        b.AddList('_currPairs', 25, -1, 30, -1);
        b.EndBox()
        b.EndBox()
     
        self.currecyLayout = dlg.AddPane('Currency, Yield Curve && Volatility', b ) 
        
        #Admin selection layout
        c = acm.FUxLayoutBuilder()
        c.BeginHorzBox('None')
        c.BeginVertBox('EtchedIn', '')
        c.BeginVertBox('EtchedIn', 'Valuation Paramters')
        c.AddList('_valpars', 10, -1, 15, -1);
        c.EndBox()
        c.BeginVertBox('EtchedIn', 'Accounting Paramters')
        c.AddList('_accpars', 10, -1, 15, -1);
        c.EndBox()
        c.EndBox()
        """
        c.BeginVertBox('EtchedIn', '')
        c.BeginVertBox('EtchedIn', 'Tasks')
        c.AddList('_tasks', 15 , -1, 15, -1);
        c.EndBox()
        c.BeginVertBox('EtchedIn', 'Portfolios')
        c.AddList('_portfolios', 15 , -1, 15, -1);
        c.EndBox()
        c.EndBox()
        c.BeginVertBox('EtchedIn', '')
        c.BeginVertBox('EtchedIn', 'Users')
        c.AddList('_users', 15 , -1, 15, -1);
        c.EndBox()
        c.BeginVertBox('EtchedIn', 'Parties')
        c.AddList('_parties', 15 , -1, 15, -1);
        c.EndBox()
        c.EndBox()
        """
        c.EndBox()
        
        self.adminLayout = dlg.AddPane('Administration', c) 

        
        self._check_all_curr            = self.currecyLayout.GetControl('check_all_curr')
        self._check_all_curves          = self.currecyLayout.GetControl('check_all_curves')
        self._check_all_volas           = self.currecyLayout.GetControl('check_all_volas')
        self._check_all_currpairs       = self.currecyLayout.GetControl('check_all_currpairs')
       
        self.Currencies()
        self.CurrencyParis()
        #self.Tasks()
        self.ValPars()
        self.AccPars()
        #self.Portfolios()
        #self.Users()
        #self.Parties()
       
        self._currs.AddCallback("ItemCheckStateChanged", ActionOnCurrClicked, self )
        self._check_all_curr.AddCallback("Activate", ActionOnCheckAllCurrClicked, self )
        self._check_all_curr.AddCallback("Activate", ActionOnCheckAllCurvesClicked, self )
        self._check_all_curves.AddCallback("Activate", ActionOnCheckAllCurvesClicked, self )
        self._check_all_volas.AddCallback("Activate", ActionOnCheckAllVolasClicked, self )
        self._check_all_currpairs.AddCallback("Activate", ActionOnCheckCheckAllCurrPairs, self )

def BuildLayout():
    b = acm.FUxLayoutBuilder()
    b.  BeginVertBox('None')
    b.    AddFill()
    b.    AddButton('ok', 'OK')
    b.    AddButton('cancel', 'Cancel')
    b.  EndBox()
    return b
    
def StartIIExtendedCB():
    shell               = acm.UX().SessionManager().Shell()
    #get shell from other than SessionManger?, re-do and create an Application
    builder             = BuildLayout()
    customLayout        = BuildPackageUIAcc()
    cd                  = acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, customLayout)
    return cd
