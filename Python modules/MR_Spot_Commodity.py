
'''
Purpose                 :Market Risk feed files
Department and Desk     :IT
Requester:              :Natalie Austin
Developer               :Douglas Finkel
CR Number               :264536, 686048

Description             :Added string "nan" for exception handling

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''


import ael, string, acm, PositionFile, MR_MainFunctions

InsL = []



# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()

    del InsL[:]
    InsL[:] = []

    return filename

# OPENFILE ##########################################################################################################



# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
        
    ins = acm.FInstrument[i.insaddr]
    
    
#    trade = acm.FTrade[t.trdnbr]
    context = acm.GetDefaultContext()
    
    if (i.insaddr) not in InsL:
        InsL.append(i.insaddr)

        outfile = open(filename, 'a')

        #Base record
        
        BASFLAG                 =       'BAS'
        HeaderName              =       'Spot Commodity'
        OBJECT                  =       'Spot CommoditySPEC'
        TYPE                    =       'Spot Commodity'
        NAME                =       MR_MainFunctions.NameFix(i.insid)
        IDENTIFIER          =       'insaddr_'+str(i.insaddr)
        
        CurrencyCAL             =       ''
        CurrencyDAYC            =       ''
        CurrencyPERD            =       ''
        CurrencyUNIT            =       i.curr.insid
        
        try:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Curve().Name()
        except:
            DiscountCurveXREF   =       ins.MappedDiscountLink().Value().Link().YieldCurveComponent().Name() 
        
        ForwardCurveXREF        =       str(i.add_info('Agri Forward Curve')) + '_FwdCurve'

        SpotPriceCAL            =       ''
        SpotPriceDAYC           =       ''
        SpotPriceFUNC           =       ''
        SpotPricePERD           =       ''
        SpotPriceUNIT           =       i.curr.insid

        GrowthRateXREF         =       str(i.product_chlnbr.entry)+'_GrowthCurve'

        SpotPriceVAL            =       ''
 	cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        calc = ins.Calculation()
	TheoPrice = calc.TheoreticalPrice(cs)
        
        if str(TheoPrice.Number()) in ('1.#QNAN', 'NaN', 'nan'):
            SpotPriceVAL            = ''
        else:
            SpotPriceVAL            = TheoPrice.Number() #i.mtm_price(ael.date_today())

        SpotPriceSTRG           =       ''
        
        TheoModelXREF           =       'Spot_Commodity'
        MarketModelXREF         =       ''
        FairValueModelXREF      =       ''
        
        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(BASFLAG, HeaderName, OBJECT, TYPE, NAME, IDENTIFIER, CurrencyCAL, CurrencyDAYC, CurrencyPERD, CurrencyUNIT, DiscountCurveXREF, ForwardCurveXREF, GrowthRateXREF, SpotPriceCAL, SpotPriceDAYC, SpotPriceFUNC, SpotPricePERD, SpotPriceUNIT, SpotPriceVAL, SpotPriceSTRG, TheoModelXREF, MarketModelXREF, FairValueModelXREF))
        
        outfile.close()
        
        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################


