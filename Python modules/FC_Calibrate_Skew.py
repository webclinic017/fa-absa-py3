import ael

SkewHelper = __import__('FC_ABSA_Safex_Skew')

SkewCal = SkewHelper.SkewCalibrate(2)


#----- Check basic Data Preparation is in place ------------------------------------------------------------------------
try:
    Page = SkewHelper.GetListNode(['Safex Options'])
    if not Page:
	Page = ael.ListNode.new()
	Page.father_nodnbr = 0
	Page.id = 'Safex Options'
	Page.terminal = 0
	Page.commit()
	ael.poll()
except:
    	print '\n\n\n\n\n***************************************************************************************'
    	print 'ERROR: Unable to create root Page List for Safex Skew calculations'
	print '***************************************************************************************'

SkewHelper.GlobalTrace = SkewCal.TraceLevel

SkewHelper.CheckChoiceListValue('Valuation Function', 'FC_SAFEX_Val.pv_BS')
SkewHelper.CheckChoiceListValue('Valuation Function', 'FC_SAFEX_Val.pv_Blk')

SkewHelper.CheckChoiceListValue('ValGroup', 'Safex Option B&S')
SkewHelper.CheckChoiceListValue('ValGroup', 'Safex Opt Core Val')
SkewHelper.CheckChoiceListValue('ValGroup', 'Safex Option Black')
SkewHelper.CheckChoiceListValue('ValGroup', 'Safex Index Future')

SkewHelper.CheckAddInfoSpec('Max Vol', 'Volatility', 'Max volatility allowed', '0.0')
SkewHelper.CheckAddInfoSpec('Min Vol', 'Volatility', 'Min volatility allowed', '0.0')
SkewHelper.CheckAddInfoSpec('AEL Trace Level', 'Instrument', 'Sets AEL feedback', '0.0')

SkewHelper.CheckValGrpContextLink('AIC_E', 'Safex Option Black', 'Volatility', 'Safex Skew')
SkewHelper.CheckValGrpContextLink('AIC_E', 'Safex Option B&S', 'Volatility', 'Safex Skew')
SkewHelper.CheckValGrpContextLink('AIC_E', 'Safex Opt Core Val', 'Volatility', 'Safex Skew')

SkewHelper.CheckValGrpContextLink('AIC_E', 'Safex Option Black', 'Valuation Function', 'FC_SAFEX_Val.pv_Blk')
SkewHelper.CheckValGrpContextLink('AIC_E', 'Safex Option B&S', 'Valuation Function', 'FC_SAFEX_Val.pv_BS')
#-----------------------------------------------------------------------------------------------------------------------


#----- Function to be called from ASQL ---------------------------------------------------------------------------------
def SkewCalibrate(dummy, step, UnderlyingInsid, UnderlyingAuctionPrice, UnderlyingSpotPrice, ATMstrikePrice, ATMimpliedVol, MinVol, MaxVol, *rest):

    if len(UnderlyingInsid) > 24:
    	print '\n\n\n\n\n***************************************************************************************'
    	print 'ERROR: The futures contract name is too long. Rename it with fewer than 25 characters'
	print '***************************************************************************************'
	return
	
    SkewCal.Underlying             = ael.Instrument[UnderlyingInsid]

    # ----- Set up basic config data ----------------------------------------
    SkewCal.AuctionPagePath        = ['Safex Options', '%s Auction' %UnderlyingInsid]
    SkewCal.AuctionVolStructName   = '%s Auction' %UnderlyingInsid
    SkewCal.SkewPagePath           = ['Safex Options', 'Skew Options']
    SkewCal.ListedPagePath         = ['Safex Options', 'Listed Options']
    SkewCal.SkewVolStructName      = 'Safex Skew'
    SkewCal.SpreadVolStructName    = 'Safex Shift'
    SkewCal.SpotATMVolStructName   = 'Safex ATM Options'
    SkewCal.TemplateSkewOptionName = '%s Opt 0 %s' %(UnderlyingInsid, SkewCal.Underlying.exp_day.to_string(ael.DATE_Packed))

    if UnderlyingAuctionPrice != 0.0: SkewCal.UnderlyingAuctionPrice = float(UnderlyingAuctionPrice)
    if UnderlyingSpotPrice    != 0.0: SkewCal.UnderlyingSpotPrice    = float(UnderlyingSpotPrice)
    if ATMstrikePrice         != 0.0: SkewCal.ATMstrikePrice         = float(ATMstrikePrice)
    if ATMimpliedVol          != 0.0: SkewCal.ATMimpliedVol          = float(ATMimpliedVol)/100.0
    if MinVol                 != 0.0: SkewCal.MinVol                 = float(MinVol)/100.0
    if MaxVol                 != 0.0: SkewCal.MaxVol                 = float(MaxVol)/100.0

    ReturnString = step
    
    if   step == '0_Instructions':
    	print '\n\n\nNotes for Safex Option Mark-to-market Volatility Calibration\n'
	print 'Part 1 --- Entering Option Auction Data\n'
	print '   The first 5 variables in the Variable Values window relate to the auction.'
	print 'When required, you will also be prompted to update some Page Definitions and'
	print 'enter some data into Volatility Structures. Follow the steps below in order,'
	print 'and look at the AEL Console window for feedback on progress, errors, and'
	print 'further instructions. If you need to refer to these notes at any stage, set'
	print 'variable 1_Step to "0_Instructions" and click <Apply>. In order to leave a'
	print "variable's value undefined, set it to 0.0\n"
	print "(a) Create a new ARENA Future/Forward instrument to represent the options'\n    underlying futures contract."
	print '(b) Create a new ARENA Option instrument for each option that was auctioned'
	print '(c) Set variable 1_Step to the value "1_Create Basic Entities" and'
	print '    set variable 2_Future to the value of the Future/Forward instrument you'
	print '    created in (a) aboveand click <Apply> to execute the first step'
	print "(d) Set variable 3_Underlying_Auction_Price equal to the auction's future price"
	print '    If Min and Max volatiltiy numbers were set at the auction, enter these values'
	print '    into variables 4 and 5. Otherwise set them to 0.0 Set variable 1_Step equal'
	print '    to "2_Config Vol Surfaces" and click <Apply>. You will be prompted to enter'
	print "    the auction's volatility data"
	print '(e) Having entered and saved the volatility data, set variable 1_Step equal to'
	print '    "3_Calibrate Skew Surface" and click <Apply>\n'
	print "The Skew surface has now been calibrated with the auction's data."
	print '\n\nPart 2 --- Entering Daily Mark to Market Data\n'
	print '   The final 3 variables in the Variable Values window provide the daily'
	print 'calibration process with market data. Variables 1 and 2 control which futures'
	print 'contract is being updated and which method is being used to perform the daily'
	print 'calibration.\n\nMethod 1 --- System looks for the current ATM option'
	print '(a) Set variable 6_Underlying_Spot_Price to the official closing price of the'
	print '    futures contract, and set variables 7_ATM_Strike_Price and 8_ATM_Implied_Vol'
	print '    to zero'
	print '(b) Set variable 1_Step to "4_Config Daily Vol Surface" and click <Apply>'
	print '(c) The system will prompt you to open a Volatility Structure and update the'
	print '    volatility of the option it contains with its official MTM volatility'
	print '    Enter the volatility, then save the Volatility Structure'
	print '(d) Set variable 1_Step to "5_Calibrate Daily Shift and click <Apply>'
	print "\nMethod 2 --- User enters the current ATM's strike price"
	print '(a) Set variable 6_Underlying_Spot_Price to the official closing price of the'
	print '    futures contract, set variable 7_ATM_Strike_Price to the strike level of'
	print '    the official ATM option and set variable 8_ATM_Implied_Vol to its volatility'
	print '(b) Set variable 1_Step to "5_Calibrate Daily Shift and click <Apply>'
	print '\nThe daily calibration is complete.'
	print '\n\n\n'
    
    elif step == '1_Create Basic Entities':
    	SkewCal.CheckBaseEntities()
    	ReturnString = '\n\nEnter the auctioned instruments into Page "%s"' %(SkewCal.AuctionPagePath[len(SkewCal.AuctionPagePath)-1])
	ReturnString = "%s\nand enter the auction's future price into parameter 3_Underlying_Auction_Price\nthen run Step 2..." %ReturnString
	
    elif step == '2_Config Vol Surfaces':
       	SkewCal.EntitiesLoaded = 0
	SkewCal.SyncAuctionVolStructWithPage()
	SkewCal.ResetSkewVolStructAndPage()
	SkewCal.PopulateSkewPage()
	SkewCal.SyncSkewVolStructWithPage()
	
	ReturnString = '\n\nEnter the auctioned options volatilities into Volatility Structure "%s"\nand then run Step 3...' %(SkewCal.AuctionVolStructName)
	 
    elif step == '3_Calibrate Skew Surface':
    	SkewCal.EntitiesLoaded = 0
	SkewCal.CalibrateSkewSurface()
	SkewCal.SetMinMaxVols()
    	ReturnString = '\n\nThe skew surface has been calibrated'
    
    elif step == '4_Config Daily Vol Surface':
    	SkewCal.EntitiesLoaded = 0
    	SkewCal.PopulateListedOptionsSurface()
	try:
	    ReturnString = '\n\nEnter closing vol for Option "%s" into Vol Structure "%s"\nthen run step 5' %(SkewCal.SpotATM.insid, SkewCal.SpotATMVolStructName)
	except:
	    ReturnString = 'Error trying to find Spot ATM option and update the listed option vol structure'
    
    elif step == '5_Calibrate Daily Shift':
    	SkewCal.EntitiesLoaded = 0
    	SkewCal.CalibrateSpreadSurface()
	SkewCal.SetMinMaxVols()
    	ReturnString = '\n\nDaily calibration complete'

    elif step == '6_Delete Auction Data':
        SkewCal.EntitiesLoaded = 0
    	SkewCal.DeleteAuctionEntities()
	ReturnString = '*** Options Deleted ***'
    
    elif step == 'test':
    	#SkewCal.SetMinMaxVols()
	ReturnString = '\n\nTest complete'
	
    else:
    	print 'Not recongised:', ReturnString
	
    print ReturnString
    return step

