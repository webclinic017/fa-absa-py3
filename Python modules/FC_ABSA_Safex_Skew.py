'''
Module: FC ABSA Saffex Skew


Initial tests for SAFFEX skew app'''

import ael

"""-----------------------------------------------------------------------------------------"""
class SkewCalibrate:
    '''Helper class that stores state between calls to its methods to update SAFFEX
       auction skew data'''
    
    AuctionPagePath        = []
    SkewPagePath           = []
    ListedPagePath         = []
    AuctionVolStructName   = ''
    SkewVolStructName      = ''
    SpreadVolStructName    = ''
    SpotATMVolStructName   = ''
    TemplateSkewOptionName = ''
    
    UnderlyingAuctionPrice = 0.0
    UnderlyingSpotPrice    = 0.0
    ATMstrikePrice         = 0.0
    ATMimpliedVol          = 0.0
    MinVol                 = 0.0
    MaxVol                 = 0.0
    
    EntitiesLoaded         = 0
    TraceLevel             = 0
    
    AuctionPage        = None
    SkewPage           = None
    ListedPage         = None
    AuctionVolStruct   = None
    SkewVolStruct      = None
    SpreadVolStruct    = None
    SpotATMVolStruct   = None
    TemplateSkewOption = None
    SpotATM            = None
    Underlying         = None
    
    """-----------------------------------------------------------------------------------------"""
    def __init__(self, TraceLevel=0):
    	global GlobalTrace
    	self.TraceLevel = TraceLevel
	GlobalTrace = TraceLevel
	return
    
    """-----------------------------------------------------------------------------------------"""
    def LoadEntities(self):
    	if self.TraceLevel>1: print 'Loading AEL entities'
	try:
    	    self.AuctionPage        = GetListNode(self.AuctionPagePath)
    	    self.SkewPage           = GetListNode(self.SkewPagePath)
    	    self.ListedPage         = GetListNode(self.ListedPagePath)
    	    self.SkewVolStruct      = ael.Volatility[self.SkewVolStructName]
    	    self.SpreadVolStruct    = ael.Volatility[self.SpreadVolStructName]
	    self.AuctionVolStruct   = ael.Volatility[self.AuctionVolStructName]
	    self.SpotATMVolStruct   = ael.Volatility[self.SpotATMVolStructName]
            self.TemplateSkewOption = ael.Instrument[self.TemplateSkewOptionName]
	    self.EntitiesLoaded = 1
	except:
	    print '*** ERROR: Failed to load some or all entities\n            Please re-run basic entities set up routine'
	    self.EntitiesLoaded = 0
	return

    """-----------------------------------------------------------------------------------------"""
    def CheckBaseEntities(self):
    	if self.TraceLevel: print 'Checking basic entities are in place'
    	CheckEndPage(self.AuctionPagePath)
	CheckEndPage(self.SkewPagePath)
	CheckEndPage(self.ListedPagePath)
	
	CheckVolStruct(self.AuctionVolStructName, 'Benchmark', 'Absolute', self.Underlying.curr, '')
    	CheckVolStruct(self.SpreadVolStructName, 'Benchmark', 'Absolute', self.Underlying.curr, '')
    	CheckVolStruct(self.SpotATMVolStructName, 'Benchmark', 'Absolute', self.Underlying.curr, '')
	
	CheckVolStruct(self.SkewVolStructName, 'Benchmark Spread', 'Rel Spot Pct', self.Underlying.curr, self.SpreadVolStructName)
	
    	CheckTemplateSkewOption(self.TemplateSkewOptionName, self.Underlying)
    	return
    
    """-----------------------------------------------------------------------------------------"""
    def DeleteAuctionEntities(self):
    	if not self.EntitiesLoaded: self.LoadEntities()
	if self.TraceLevel: print 'Deleting entities associated with auction of options for %s' %self.Underlying.insid
	
    	ClearPageByUnderlying(self.AuctionPage, self.Underlying)
	ClearPageByUnderlying(self.SkewPage, self.Underlying)
	ael.poll()
	
	if self.TraceLevel>=2: print '\tDeleting Page "%s"' %(self.AuctionPagePath)
	self.AuctionPage.delete()
	
	ClearVolStructByUnderlying(self.SkewVolStruct, self.Underlying)
	ClearVolStructByUnderlying(self.AuctionVolStruct, self.Underlying)
	ClearVolStructByUnderlying(self.SpotATMVolStruct, self.Underlying)
	ClearVolStructByUnderlying(self.SpreadVolStruct, self.Underlying)
	ael.poll()

	if self.TraceLevel>=2: print '\tDeleting Vol Struct "%s"' %(self.AuctionVolStructName)	
	self.AuctionVolStruct.delete()
	ael.poll()
	
	DeleteSyntheticOptions(self.Underlying)
	
    	return
    
    
    """-----------------------------------------------------------------------------------------"""
    def SyncAuctionVolStructWithPage(self):
    	if not self.EntitiesLoaded: self.LoadEntities()

#Call to add extra instruments to page	
#Added by Hardus Jacobs
	AddOuterToPage(self.AuctionPage, self.Underlying)
	self.AuctionPage = GetListNode(self.AuctionPagePath)
	print self.AuctionPagePath
	print '-------AuctionPage-----------'
	for i in self.AuctionPage.leafs():
	    print i.insaddr.insid
	print '-------end Auctionpage-------'
	if self.TraceLevel: print 'Copying Auction Page instruments to Auction Vol Structure'
    	
	SyncVolStructInstruments(self.AuctionPage, self.AuctionVolStruct)
	
	#As we have altered the vol structure, we must reload it
	self.AuctionVolStruct = ael.Volatility[self.AuctionVolStructName]
	
    	return

    """-----------------------------------------------------------------------------------------"""
    def SyncSkewVolStructWithPage(self):
    	if not self.EntitiesLoaded: self.LoadEntities()
	if self.TraceLevel: print 'Copying Skew Page instruments to Skew Vol Structure'
	
	SyncVolStructInstruments(self.SkewPage, self.SkewVolStruct)
    	
	#As we have altered the vol structure, we must reload it
	self.SkewVolStruct = ael.Volatility[self.SkewVolStructName]
	
	return
	
    """-----------------------------------------------------------------------------------------"""
    def ResetSkewVolStructAndPage(self):
    	'''Used to drop references from the vol struct and page to the
	   skew options so that they can be deleted later on, if they are no longer needed'''
    	
	if not self.EntitiesLoaded: self.LoadEntities()
	if self.TraceLevel: print 'Removing references to skew options from Vol Structure "%s" and Page "%s"' %(self.SkewVolStruct.vol_name, self.SkewPage.id)
	
	#Reset the vol surface --------------------------------------------------------------------------------------------
	VolStruct = self.SkewVolStruct.clone()
	VolPoints = [VolPoint for VolPoint in VolStruct.points() if (VolPoint.insaddr.exp_day == self.Underlying.exp_day)]
	
	# ensure template option is linked to the vol surface
	if not(self.TemplateSkewOption in [VolPoint.insaddr for VolPoint in VolPoints]):
    	    VolPoint = ael.VolPoint.new(VolStruct)
	    VolPoint.insaddr = self.TemplateSkewOption
	    VolPoint.commit()

	# delete all other VolPoints
	for VolPoint in VolPoints:
    	    if VolPoint.insaddr != self.TemplateSkewOption: VolPoint.delete()
	
	VolStruct.commit()
	ael.poll()
	#------------------------------------------------------------------------------------------------------------------
	
	# Reset the page --------------------------------------------------------------------------------------------------
	SkewPage = self.SkewPage.clone()
	
    	# Ensure the template option is linked to the page
	if not(self.TemplateSkewOption in GetPageInstruments(SkewPage, '')):
    	    Leaf = ael.ListLeaf.new(SkewPage)
	    Leaf.insaddr = self.TemplateSkewOption
	    Leaf.commit()
	    
    	# remove all the other instruments
	for Leaf in SkewPage.leafs():
    	    if (Leaf.insaddr != self.TemplateSkewOption) and (Leaf.insaddr.exp_day == self.Underlying.exp_day): Leaf.delete()

	SkewPage.commit()
	ael.poll()
	#------------------------------------------------------------------------------------------------------------------
	
	#As we've amended these entities, reload them
	self.SkewPage      = GetListNode(self.SkewPagePath)
    	self.SkewVolStruct = ael.Volatility[self.SkewVolStructName]
	
	return
	
    """-----------------------------------------------------------------------------------------"""
    def PopulateSkewPage(self):
    	if not self.EntitiesLoaded: self.LoadEntities()
	if self.TraceLevel: print 'Populating the Skew Page "%s"' %(self.SkewPage.id)

	#Get a sorted list of all the auctioned options from the page and their strikes ------------------
	AuctionList = [(Ins.strike_price, Ins) for Ins in GetPageInstruments(self.AuctionPage, 'Option')]
	AuctionList.sort()

    	#-------------------------------------------------------------------------------------------------
	
	#find the ATM strike and its position in AuctionList ---------------------------------------------
	ATMList = [(abs(element[0]-self.UnderlyingAuctionPrice), element) for element in AuctionList]
	ATMList.sort()
	ATMstrike = ATMList[0][1][0]
	ATMindex = AuctionList.index(ATMList[0][1])
	if self.TraceLevel>1: print '\tUnderlying Price = %f => ATMstrike = %f' %(self.UnderlyingAuctionPrice, ATMstrike)
	#-------------------------------------------------------------------------------------------------
	

	#Get the root of the name of the skew surface instruments (nasty) --------------------------------
	NameRoot = self.TemplateSkewOption.insid
	NameRoot = NameRoot[0:len(NameRoot)-10]
	if self.TraceLevel>1: print '\tSkew options will have name based on root "%s"' %NameRoot
	#-------------------------------------------------------------------------------------------------

	#build a list of required skew instruments (1:1 with auction) adding new options as required -----
	SkewInsList = []

	i = 0
	for AuctionItem in AuctionList:

	    InsName = '%s%i %s' %(NameRoot, (i-ATMindex), (AuctionItem[1].exp_day.to_string(ael.DATE_Packed)))
	    Ins = ael.Instrument[InsName]

	    if Ins:
	    	if self.TraceLevel>1: print '\tSkew Instrument Name=%s found' %InsName
		Ins = Ins.clone()
	    else:
	    	if self.TraceLevel>1: print '\tCreating new Skew Instrument with Name=%s' %InsName
		Ins = self.TemplateSkewOption.new()
		Ins.insid = InsName
    	    
	    Ins.exp_day = AuctionItem[1].exp_day
	    Ins.generic = 0
	    Ins.otc = 1
	    Ins.strike_price = round((AuctionItem[1].strike_price/self.UnderlyingAuctionPrice - 1), 4) * 100.0
	    Ins.commit()
    	    ael.poll()
	    
	    SkewInsList.append(ael.Instrument[InsName])
	    i = i+1
	
	#-------------------------------------------------------------------------------------------------
	
	#Get a list of all skew options for the current futures contract ---------------------------------
	Records = ael.dbsql("""SELECT insid FROM instrument WHERE otc = 1
			       AND und_insaddr = %i AND strike_type = 4 /*Rel Spot Pct*/"""
				%(self.TemplateSkewOption.und_insaddr.insaddr))[0]
	AllSkewIns = [ael.Instrument[Record[0]] for Record in Records]
		#-------------------------------------------------------------------------------------------------
	
	#Loop through all the skew instruments that aren't supposed to be in the Skew structure ----------
	def NotInSkew(Ins):
    	    #tests if Ins is not in the SkewInsList
    	    return not(Ins in SkewInsList)
    	
	for Ins in filter(NotInSkew, AllSkewIns):
	    if Ins.exp_day == self.Underlying.exp_day:
    	    	try:
		    Ins.delete()
		    print 'delete:', Ins.insid
		    if self.TraceLevel > 1: print '\tFound and deleted unnecessary skew surface option "%s"' %Ins.insid
	    	except:
	    	    try:
		    	print '***** ERROR: Failed to delete unnecessary skew surface option: "%s"' %Ins.insid
			print '             Remove any references to this instrument made in'
			print '             any vol structures or instrument pages and re-try'
		    except:
		    	print '***** ERROR: While trying to delete unnecessary skew surface option'
    	#-------------------------------------------------------------------------------------------------
	
	#Add the skew surface options to their page ------------------------------------------------------
	SkewPage = self.SkewPage.clone()

	for Ins in SkewInsList:
	    print Ins.insid
    	    if Ins != self.TemplateSkewOption:
		Leaf = ael.ListLeaf.new(SkewPage)
		Leaf.insaddr = Ins
		Leaf.commit()
		ael.poll()
	SkewPage.commit()
	ael.poll()
    	#-------------------------------------------------------------------------------------------------
		
	#As we have ammended the skew page, reload it
	self.SkewPage = GetListNode(self.SkewPagePath)
	
	return

    """-----------------------------------------------------------------------------------------"""
    def CalibrateSkewSurface(self):
    	if not self.EntitiesLoaded: self.LoadEntities()
	# ----- Code added to add extra points at the end---------
    	#------- Hardus Jacobs------------------
    	#------ Calculate vols over here for auctionvol
    	#
	set_outerpoint(self.AuctionVolStruct)
	self.AuctionVolstruct = ael.Volatility[self.AuctionVolStructName]
	if self.TraceLevel: print 'Setting skew surface volatilities'
	
	#Find the Exact ATM volatility ------------------------------------------------------------------------------
	Obs = [(VolPoint.insaddr.strike_price, VolPoint.volatility) for VolPoint in self.AuctionVolStruct.points()]
	XATMvol = round(LinearInterpolate(Obs, self.UnderlyingAuctionPrice), 4)
    	if self.TraceLevel>1: print '\tExact ATM vol = %f' %XATMvol
	#------------------------------------------------------------------------------------------------------------
	
	#Get a list of the auctioned options adjusted vols and the skew options and sort them by strike -------------
	AuctionVolPoints = [(VolPoint.insaddr.strike_price, (VolPoint.volatility - XATMvol)) for VolPoint in self.AuctionVolStruct.points()]
	SkewVolPoints = [(VolPoint.insaddr.strike_price, VolPoint) for VolPoint in self.SkewVolStruct.points() if VolPoint.insaddr.exp_day == self.Underlying.exp_day]
	AuctionVolPoints.sort()
	SkewVolPoints.sort()
	#------------------------------------------------------------------------------------------------------------

	#Update the skew vol structure ------------------------------------------------------------------------------
	if (len(SkewVolPoints) != len(AuctionVolPoints)) or (len(SkewVolPoints) == 0) or (len(AuctionVolPoints) == 0):
	    print '\n\n ***** ERROR: Skew Vol Structure and Auction Vol Structure are not in sync for expiry %s\n\n' %(self.Underlying.exp_day.to_string())
	    return
	    
    	i = 0
	for element in SkewVolPoints:
	    VolPoint = element[1].clone()
	    if self.TraceLevel>1: print '\tVolPoint "%s" vol = %f' %(VolPoint.insaddr.insid, AuctionVolPoints[i][1])
	    VolPoint.volatility = AuctionVolPoints[i][1]
	    VolPoint.commit()
	    i = i+1
	#------------------------------------------------------------------------------------------------------------
	
	return
    
    """-----------------------------------------------------------------------------------------"""
    def PopulateListedOptionsSurface(self):
    	if not self.EntitiesLoaded: self.LoadEntities()
	if self.TraceLevel: print 'Updating the Listed Option Vol Structure with the current ATM option'

	#Get a sorted list of the listed options --------------------------------------------------------
	ListedOptions = [(Ins.strike_price, Ins) for Ins in GetPageInstruments(self.ListedPage, 'Option') if Ins.exp_day == self.Underlying.exp_day]

	if len(ListedOptions) == 0:
	    print '**** Error: There are no options listed on Page "%s" ****\n**** Please enter some options written against instrument "%s" and retry' %(self.ListedPage.id, self.Underlying.insid)
	    return
	    
	ListedOptions.sort()
	#------------------------------------------------------------------------------------------------
	
	#find the ATM strike and its position in AuctionList --------------------------------------------
	ATMList = [(abs(element[0]-self.UnderlyingSpotPrice), element) for element in ListedOptions]
	ATMList.sort()
	self.SpotATM = ATMList[0][1][1]
	ATMstrike = ATMList[0][1][0]
	ATMindex = ListedOptions.index(ATMList[0][1])
	
	if self.TraceLevel>1: print '\tATM found to be strike=%f, insid = "%s"' %(ATMstrike, self.SpotATM.insid)
	#------------------------------------------------------------------------------------------------

	#Update the vol structure with the new ATM option------------------------------------------------
	VolStruct = self.SpotATMVolStruct.clone()
	
	if self.TraceLevel: print '\tUpdating VolStruct "%s"' %(VolStruct.vol_name)
	
	#remove old ATM options if present...
	for VolPoint in VolStruct.points():
	    if VolPoint.insaddr.exp_day == self.Underlying.exp_day: VolPoint.delete()
	
	#...and add the new one
	VolPoint = ael.VolPoint.new(VolStruct)
	VolPoint.insaddr = self.SpotATM
	VolPoint.commit()
	ael.poll()
	
	VolStruct.commit()
	ael.poll()
	
	self.SpotATMVolStruct = ael.Volatility[self.SpotATMVolStructName]
	#------------------------------------------------------------------------------------------------
	
	return
    
    """-----------------------------------------------------------------------------------------"""
    def CalibrateSpreadSurface(self):
    	if not self.EntitiesLoaded: self.LoadEntities()
	if self.TraceLevel: print 'Calibrating the spread surface'
	print self.UnderlyingSpotPrice
	#Get ATM strike and volatility ----------------------------------------------------------------------------
	if self.ATMstrikePrice:
	    if self.TraceLevel > 1: print '\tUsing the user-specified ATM strike = %f' %(self.ATMstrikePrice)
	    ATMstrike = self.ATMstrikePrice
	else:
	    ATMVolPoint = [VolPoint for VolPoint in self.SpotATMVolStruct.points() if VolPoint.insaddr.exp_day == self.Underlying.exp_day][0]
	    ATMstrike = ATMVolPoint.insaddr.strike_price
	    if self.TraceLevel > 1: print '\tUsing %s as ATM option' %(ATMVolPoint.insaddr.insid)
	    
    	if self.ATMimpliedVol:
	    if self.TraceLevel > 1: print '\tUsing ATM implied vol = %f, as entered in application parameters' %(self.ATMimpliedVol)
	    ATMvol = self.ATMimpliedVol
	else:
	    if not ATMVolPoint: ATMVolPoint = self.SpotATMVolStruct.points()[0]
	    ATMvol = ATMVolPoint.volatility
	    if self.TraceLevel > 1: print '\tUsing ATM implied vol = %f, taken from Vol Structure "%s"' %(ATMvol, self.SpotATMVolStruct.vol_name)
	#----------------------------------------------------------------------------------------------------------
	
	#Calculate the Volatility parrallel shift needed for the Skew Vol Surface----------------------------------
	Moneydness = 100.0 * (self.UnderlyingSpotPrice/ATMstrike  - 1) # EXAR000 - divisor inverted.
	Obs = [(VolPoint.insaddr.strike_price, VolPoint.volatility) for VolPoint in self.SkewVolStruct.points() if VolPoint.insaddr.exp_day == self.Underlying.exp_day]
	ATMVolOffset = LinearInterpolate(Obs, Moneydness)
	print 'ATMStrike: ', ATMstrike
	print 'Underlying_Spot: ', self.UnderlyingSpotPrice 
	print ' '
	print 'TEST 1 ###################################', ATMVolOffset
	print ' '
	XATMVol = round( (ATMvol + ATMVolOffset), 4) # EXAR000 - subtraction changed to addition
	print 'Exact ATM Vol ', ATMvol
	#----------------------------------------------------------------------------------------------------------
	
	#Check that an ARENA option exists to store the Exact-At-The-Money volatility------------------------------	
	XATMname = self.TemplateSkewOptionName
	XATMname = '%s%s' %(XATMname[0:len(XATMname)-10], 'XATM')
	CheckXATMSpreadOption(XATMname, self.Underlying)
	XATM = ael.Instrument[XATMname]
	#----------------------------------------------------------------------------------------------------------
	
	#Add or Update the VolPoint with the new XATM volatility value --------------------------------------------
	if XATM in [VolPoint.insaddr for VolPoint in self.SpreadVolStruct.points()]:
	    if self.TraceLevel > 1: print '\tUpdating exisABCDEFiting volpoint with vol = %f' %XATMVol
	    for VolPoint in self.SpreadVolStruct.points():
		if VolPoint.insaddr == XATM:
	    	    VolPoint = VolPoint.clone()
	    	    VolPoint.volatility = XATMVol
	    	    VolPoint.commit()
	    	    ael.poll()
	else:
	    if self.TraceLevel > 1: print '\tAdding new vol point to vol structure, and setting vol = %f' %XATMVol
	    VolStruct = self.SpreadVolStruct.clone()
	    
	    VolPoint = ael.VolPoint.new(VolStruct)
	    VolPoint.insaddr = XATM
	    VolPoint.volatility = XATMVol
	    
	    VolPoint.commit()
	    ael.poll()
	    
	    VolStruct.commit()
	    ael.poll()
	#----------------------------------------------------------------------------------------------------------
	
	return

    """-----------------------------------------------------------------------------------------"""
    def SetMinMaxVols(self):
    	if not self.EntitiesLoaded: self.LoadEntities()
    	AddInfos = {}
	SkewStruct = self.SkewVolStruct.clone()
	
	for addinfo in SkewStruct.additional_infos():
	    AddInfos[addinfo.addinf_specnbr.field_name] = addinfo
	
	try:
	    addinfo = AddInfos['Max Vol'].clone()
	    addinfo.value = str(self.MaxVol)
	    addinfo.commit()
	except:
	    addinfo = ael.AdditionalInfo.new(SkewStruct)
	    addinfo.addinf_specnbr = ael.AdditionalInfoSpec['Max Vol']
	    addinfo.value = str(self.MaxVol)
	    addinfo.commit()
	
	try:
	    addinfo = AddInfos['Min Vol'].clone()
	    addinfo.value = str(self.MinVol)
	    addinfo.commit()
	except:
	    addinfo = ael.AdditionalInfo.new(SkewStruct)
	    addinfo.addinf_specnbr = ael.AdditionalInfoSpec['Min Vol']
	    addinfo.value = str(self.MinVol)
	    addinfo.commit()
	
	SkewStruct.commit()
	self.SkewVolStruct = ael.Volatility[self.SkewVolStructName]
	
	return
    
    

"""-----------------------------------------------------------------------------------------"""
def LinearInterpolate(Observations, x):
    #Observations is a list of (x,y) tuples
    Observations.sort()
    last = Observations[0]
    for current in Observations[1:(len(Observations)-1)]:
    	print 'CURRENT', current
	
    for current in Observations[1:(len(Observations)-1)]:
    	if current[0] > x: break
	last = current
    
    if current[0] <= x: current = Observations[len(Observations)-1]
    print 'X ', x, 'last ', last, 'current ', current
    weight = (x - last[0])/(current[0] - last[0])
    
    print "3####################", weight * current[1] + (1-weight) * last[1] 


    return weight * current[1] + (1-weight) * last[1] 


"""-----------------------------------------------------------------------------------------"""
def GetListNode(Path):
    try:
	ChildNodes = ael.ListNode.select('father_nodnbr=0')    
	for NodeName in Path:
    	    for ListNode in ChildNodes:
	    	if ListNode.id == NodeName:
	    	    ChildNodes = ael.ListNode.select('father_nodnbr=%i' %ListNode.nodnbr)
		    break
	if ListNode.id != Path[len(Path)-1] : ListNode = None
    except:
    	ListNode = None	

    return ListNode

"""-----------------------------------------------------------------------------------------"""
def GetPageInstruments(ListNode, InsType):
    return [Link.insaddr for Link in ListNode.leafs() if (InsType == '' or Link.insaddr.instype == InsType)]

"""-----------------------------------------------------------------------------------------"""
def SyncVolStructInstruments(Page, VolStruct):

    if GlobalTrace>=2: print '\tSynch Vol Structure "%s" with the instruments from Page "%s"' %(VolStruct.vol_name, Page.id)

    InsList = GetPageInstruments(Page, 'Option')
    CloneVolStruct = VolStruct.clone()
    VolPoints = CloneVolStruct.points()
    VolPointInsList = []

    #remove volpoints that should not be in the structure...
    for VolPoint in VolPoints:
    	if VolPoint.insaddr in InsList:
    	    VolPointInsList.append(VolPoint.insaddr)
    	else:
    	    VolPoint.delete()

    #... and add any missing volpoints
    for Ins in InsList:
    	if not(Ins in VolPointInsList):
    	    VolPoint = ael.VolPoint.new(CloneVolStruct)
	    VolPoint.insaddr = Ins
	    VolPoint.commit()

    CloneVolStruct.commit()
    for i  in CloneVolStruct.points():
    	print i.insaddr.insid, CloneVolStruct.vol_name
    print 'volstruct Committed'

    return

"""-----------------------------------------------------------------------------------------"""    
def CheckEndPage(Path):
    EndPage = GetListNode(Path)
    if EndPage:
    	if GlobalTrace>=2: print '\tPage "%s" found, %s' %(Path, EndPage.id)
    else:
    	NewPageName = Path[len(Path)-1]
    	Path = Path[:len(Path)-1]
	print '\tCreating page "%s" in "%s"' %(NewPageName, Path)
	ParentPage = GetListNode(Path)
	NewPage = ael.ListNode.new()
	NewPage.father_nodnbr = ParentPage
	NewPage.id = NewPageName
	NewPage.terminal = 1
	NewPage.commit()

    return

"""-----------------------------------------------------------------------------------------"""    
def CheckVolStruct(VolStructName, StructType, StrikeType, Curr, UnderlyingCurveName):
    VolStruct = ael.Volatility[VolStructName]
    if VolStruct:
    	if GlobalTrace>=2: print '\tVol Struct "%s" found' %VolStructName
    	VolStruct = VolStruct.clone()
    else:
	print '\tCreating new VolStruct "%s"' %VolStructName
    	VolStruct = ael.Volatility.new()
    	
    VolStruct.vol_name = VolStructName
    VolStruct.vol_type = StructType
    VolStruct.framework = 'Black & Scholes'
    VolStruct.strike_type = StrikeType
    VolStruct.curr = Curr
    
    if UnderlyingCurveName !='': VolStruct.und_vol_seqnbr = ael.Volatility[UnderlyingCurveName]
    
    VolStruct.commit()
    ael.poll()
    
    return

"""-----------------------------------------------------------------------------------------"""    
def CheckTemplateSkewOption(TemplateSkewOptionName, Underlying):
    Option = ael.Instrument[TemplateSkewOptionName]
    
    if Option:
    	if GlobalTrace>=2: print '\tFound option "%s"' %TemplateSkewOptionName
    
    else:
    	
    	print '\tCreating option "%s"' %TemplateSkewOptionName
	
    	Option = ael.Instrument.new('Option')
	Option.insid = TemplateSkewOptionName
	Option.generic  = 0
    	Option.notional = 0
    	Option.curr = Underlying.curr
    	Option.quote_type = 'Per Contract'
    	Option.otc = 1
    	Option.mtm_from_feed = 0
    	Option.spot_banking_days_offset = 2
    	Option.contr_size = 1
    	Option.und_insaddr = Underlying
    	Option.und_instype = 'Future/Forward'
    	Option.settlement = 'Cash'
    	Option.paytype = 'Spot'
    	Option.exp_day = Underlying.exp_day
    	Option.pay_day_offset = 0
    	Option.call_option = 1
    	Option.exercise_type = 'American'
    	Option.strike_price = 0.0
    	Option.strike_curr = Underlying.curr
    	Option.strike_type = 'Rel Spot Pct'
	Option.commit()
	ael.poll()
    
    return

"""-----------------------------------------------------------------------------------------"""
def CheckXATMSpreadOption(OptionName, Underlying):
    Option = ael.Instrument[OptionName]
    
    if Option:
    	if GlobalTrace>=2: print '\tFound option "%s"' %OptionName
    
    else:
    	print '\tCreating option "%s"' %OptionName
	
    	Option = ael.Instrument.new('Option')
	Option.insid = OptionName
	Option.generic  = 0
    	Option.notional = 0
    	Option.curr = Underlying.curr
    	Option.quote_type = 'Per Contract'
    	Option.otc = 1
    	Option.mtm_from_feed = 0
    	Option.spot_banking_days_offset = 2
    	Option.contr_size = 1
    	Option.und_insaddr = Underlying
    	Option.und_instype = 'Future/Forward'
    	Option.settlement = 'Cash'
    	Option.paytype = 'Spot'
    	Option.exp_day = Underlying.exp_day
    	Option.pay_day_offset = 0
    	Option.call_option = 1
    	Option.exercise_type = 'American'
    	Option.strike_price = 0.0
    	Option.strike_curr = Underlying.curr
    	Option.strike_type = 'Rel Spot'
	Option.commit()
	ael.poll()
    
    return

"""-----------------------------------------------------------------------------------------"""
def CheckChoiceListValue(ChoiceListName, Value):
    ChList = ael.ChoiceList.read("list='%s' AND entry='%s'" %(ChoiceListName, Value))
    
    if ChList:
    	if GlobalTrace>=2: print '\tFound value "%s" in Choice List "%s"' %(Value, ChoiceListName)
    else:
    	print '\tAdding value "%s" to Choice List "%s"' %(Value, ChoiceListName)
    	ChList = ael.ChoiceList.new()
	ChList.list  = ChoiceListName
	ChList.entry = Value
	ChList.commit()
    
    return

"""-----------------------------------------------------------------------------------------"""
def CheckAddInfoSpec(SpecName, Table, Desc, DefaultValue):
    Spec = ael.AdditionalInfoSpec[SpecName]
    if Spec:
    	if GlobalTrace>=2: print '\tFound AddInfoSpec "%s"' %SpecName
    else:
    	print '\tAdding AddInfoSpex "%s"' %SpecName
	
    	Spec = ael.AdditionalInfoSpec.new()
	
    	Spec.field_name = SpecName
    	Spec.rec_type   = Table
    	setattr(Spec, 'data_type.grp', 'Standard')
    	setattr(Spec, 'data_type.type', 4)
    	Spec.description = Desc
    	Spec.mandatory = 0
    	Spec.default_value = DefaultValue
	
	Spec.commit()
	
    return

"""-----------------------------------------------------------------------------------------"""
def CheckValGrpContextLink(ContextName, ValGrpName, ParamType, ValueName):
    
    ChList = ael.ChoiceList.read("list='ValGroup' AND entry='%s'" %(ValGrpName))
    Context = ael.Context[ContextName]
    for Link in ael.ContextLink.select("group_chlnbr = %d" %(ChList.seqnbr)):
    	if Link.type == ParamType and Link.name == ValueName and Link.context_seqnbr == Context:
	    if GlobalTrace>=2: print '\tContext Link found in %s for Val Grp "%s" mapping %s to %s' %(ContextName, ValGrpName, ParamType, ValueName)
	    return
    
    print '\tAdding Context Link to %s for Val Grp "%s" mapping %s to %s' %(ContextName, ValGrpName, ParamType, ValueName)
    
    Context = Context.clone()
    Link = ael.ContextLink.new(Context)
    
    Link.type         = ParamType
    Link.name         = ValueName
    Link.mapping_type = 'Val Group'
    Link.group_chlnbr = ChList
    
    Link.commit()
    Context.commit()
    return

"""-----------------------------------------------------------------------------------------"""
def ClearPageByUnderlying(Page, Underlying):
    Page = Page.clone()
    for Leaf in Page.leafs():
    	if Leaf.insaddr.und_insaddr == Underlying:
	    if GlobalTrace>=2: print '\tRemoving Page entryfor instrument %s' %(Leaf.insaddr.insid)
	    Leaf.delete()
    Page.commit()
    return

"""-----------------------------------------------------------------------------------------"""
def ClearVolStructByUnderlying(VolStruct, Underlying):
    VolStruct = VolStruct.clone()
    for Point in VolStruct.points():
    	if Point.insaddr.und_insaddr == Underlying:
	    if GlobalTrace>=2: print '\tRemoving Vol Point for instrument %s' %(Point.insaddr.insid)
	    Point.delete()
    VolStruct.commit()
    return

"""-----------------------------------------------------------------------------------------"""
def DeleteSyntheticOptions(Underlying):
    Records = ael.dbsql("""SELECT insid FROM instrument WHERE otc = 1
			   AND und_insaddr = %i AND (strike_type = 4 or strike_type = 2) /*Rel Spot Pct*/"""
			    %(Underlying.insaddr))[0]
    AllSkewIns = [ael.Instrument[Record[0]] for Record in Records]
    for Ins in AllSkewIns:
    	if GlobalTrace>=2: print '\tDeleting %s' %(Ins.insid)
	Ins.delete()
    
    return
"""------------------------------------------------------------------------------------------"""
# This will create a new instrument at the outerpoint strikes
# Added by Hardus Jacobs 
def CreateExtraIns(Underlying, strike):
    print Underlying
    ins = ael.Instrument.new('Option')
    ins.und_insaddr = Underlying
    ins.instype = 'Option'
    ins.call_option = 0
    ins.strike_price = strike
    ins.und_instype = 'Future/Forward'
    ins.otc = 0
    ins.contr_size = 10
    ins.exp_day = Underlying.exp_day
    ins.exercise_type = 'American'
    ins.quote_type = 'Per Contract'
    ins.product_chlnbr = 979
    ins.pay_day_offset = 0
    ins.insid = ins.suggest_id()
    print ins.insid
    if ins.insid.rfind('#', 0, len(ins.insid)) == -1:
        ins.commit()
	print 'commited'
	return ins
    else:
    	print 'already there'
	print ins.insid.rstrip('/#1')
    	return ael.Instrument[ins.insid.rstrip('/#1')]
    ael.poll()
"""------------------------------------------------------------------------------"""	
def AddOuterToPage(AuctionPage, Underlying):
        #---This will add the instruments created the the specified Auction Page
    	#---Added by Hardus Jacobs	
    	AuctionClone = AuctionPage.clone()	
    	leafnodes = AuctionClone.leafs()
    	ins_lo = CreateExtraIns(Underlying, 1000)
    	#ael.Instrument['ZAR/ALSI/DEC03']
    	ins_hi = CreateExtraIns(Underlying, 30000)
    	lo = 0
    	hi = 0
    	for leaf in leafnodes:
    	    if leaf.insaddr == ins_lo:
	    	lo = 1
	    if leaf.insaddr == ins_hi:
	    	hi = 1
    	if lo == 0:
    	    nleaf= ael.ListLeaf.new(AuctionClone)
	    nleaf.insaddr = ins_lo
	    print nleaf
	    nleaf.commit()
    	if hi == 0:
    	    nleaf= ael.ListLeaf.new(AuctionClone)
	    nleaf.insaddr = ins_hi    		
    	    print nleaf   
	    nleaf.commit() 	
	AuctionClone.commit()    	    
    	ael.poll()
	return 1


        
#-----Added by Hardus Jacobs-----
#-----This will set the correct value for the outer points on the volstructure using linear interpolatiopn     
def set_outerpoint(volstruct):
    print '*Auction volatility Structure: ', volstruct.vol_name
    list = [(Volpoint.insaddr.strike_price, Volpoint.volatility) for Volpoint in volstruct.points()]
    print list, '\n'
    list.sort()
    lo = get_new_vol(list[0][0], list[1][0], list[2][0], list[1][1], list[2][1])
    hi = get_new_vol(list[(len(list)-1)][0], list[(len(list)-2)][0], list[(len(list)-3)][0], list[(len(list)-2)][1], list[(len(list)-3)][1])
    for vp in volstruct.points():
    	if (vp.insaddr.strike_price == list[0][0]): 
	    print vp.insaddr.strike_price, lo
	    cvp = vp.clone()
	    cvp.volatility = lo
	    print cvp.pp()
	    cvp.commit()
	    
	else: 
	    if (vp.insaddr.strike_price == list[(len(list)-1)][0]):
	    	print vp.insaddr.strike_price, hi
	    	cvp = vp.clone()
	    	cvp.volatility = hi
	    	print cvp.pp()
    	    	cvp.commit()
    ael.poll()    
"""-------------------------------------------------------------------------------------"""

#--------This gets the new value for the volpoint at the specific strike using linear interpolation	    
#--------Added by Hardus Jacobs
def get_new_vol(newx, beforex, afterx, beforey, aftery):
    return (((afterx - newx)* beforey)/(afterx - beforex)) + (((newx - beforex) * aftery)/(afterx - beforex))
    
    
       
    

