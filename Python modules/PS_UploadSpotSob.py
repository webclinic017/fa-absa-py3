'''----------------------------------------------------------------------------------------------------------------
MODULE
    PS_UploadSpotSob
DESCRIPTION
    Developer           : Nidheesh Sharma
    Date                : 2012-08-06
    Purpose             : Updates Spot_SOB for instruments with the /MTM postfix
    Change Number       : C381413
ENDDESCRIPTION
----------------------------------------------------------------------------------------------------------------'''

import acm, FBDPGui

VALID_INSTYPES  = ('Future/Forward', 'Option')
TODAY = acm.Time.DateNow()

#----------------------------------------------------------------------------------------------------------------
#A function to get all the active instruments with the /MTM postfix and MTMFromFeed set to true
#----------------------------------------------------------------------------------------------------------------
def Get_MTM_Instruments(instypes, date):
    query = acm.CreateFASQLQuery('FInstrument', 'AND')
    query.AddAttrNode('Name', 'RE_LIKE_NOCASE', '*/MTM')
    query.AddAttrNode('MtmFromFeed', 'EQUAL', 1)
    query.AddAttrNode('ExpiryDate', 'GREATER_EQUAL', date)
    if instypes:
        op = query.AddOpNode('OR')
        for type in instypes:
            op.AddAttrNode('InsType', 'EQUAL', acm.EnumFromString('InsType', type))
    ins = query.Select()
    return ins

#----------------------------------------------------------------------------------------------------------------
#A function to get the SOB price of an instrument given a date
#----------------------------------------------------------------------------------------------------------------
def Get_SOB_Price(instrument, spotDate):
    for price in instrument.HistoricalPrices():
        if price.Market() != None:
            if price.Market().Name() == 'SPOT' and price.Day() == spotDate:
                return price

#----------------------------------------------------------------------------------------------------------------
#A function to set the SPOT_SOB price of an instrument for a given date using its SPOT price
#----------------------------------------------------------------------------------------------------------------
def Set_SPOT_SOB_Price(instrument, spotPrice, spotDate, sobDate):
    foundSOB = False
    for latestPrice in instrument.Prices():
        if latestPrice.Market() != None:            
            if latestPrice.Market().Name() == 'SPOT_SOB' and spotPrice.Currency() == latestPrice.Currency() and latestPrice.Day() == sobDate:
                foundSOB = True
                if latestPrice.Settle() != spotPrice.Settle():
                    oldLatestSettlePrice = latestPrice.Settle()
                    latestPrice.Bid(spotPrice.Bid())
                    latestPrice.Ask(spotPrice.Ask())
                    latestPrice.Settle(spotPrice.Settle())
                    latestPrice.Last(spotPrice.Last())
                    try:
                        latestPrice.Commit()
                        print 'Updated %s SPOT_SOB for %s successfully. Changed from %s to %s.' % (sobDate, instrument.Name(), oldLatestSettlePrice, latestPrice.Settle())
                    except Exception as e:
                        print 'Could not copy %s SPOT to %s SPOT_SOB for %s: %s' % (spotDate, sobDate, instrument.Name(), e)
                        
    #create spot_sob if it doesnt exist for the instrument for the sobDate
    if not foundSOB:
        try:
            instrumentPrice = acm.FPrice()
            instrumentPrice.Day(sobDate)
            instrumentPrice.Instrument(instrument)
            instrumentPrice.Market(acm.FParty['SPOT_SOB'])
            instrumentPrice.Currency(spotPrice.Currency())
            instrumentPrice.Settle(spotPrice.Settle())
            instrumentPrice.Bid(spotPrice.Bid())
            instrumentPrice.Ask(spotPrice.Ask())
            instrumentPrice.Last(spotPrice.Last())
            instrumentPrice.Commit()
            print 'Created %s SPOT_SOB for %s.' % (sobDate, instrument.Name())
        except Exception as e:
            print 'Error in setting instrument %s SPOT_SOB price for instrument %s: %s' % (sobDate, instrument.Name(), e)
        

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = FBDPGui.LogVariables(['SPOTdate', 'Spot Date', 'string', None, acm.Time.DateAddDelta(TODAY, 0, 0, -1), 1, 0, 'Date of the SPOT that is used to update the SPOT_SOB', None, 1],
                ['SOBdate', 'Spot SOB Date', 'string', None, TODAY, 1, 0, 'Date of SPOT_SOB that needs to be updated.', None, 1],
                )

def ael_main(dictionary):
    spotDate = dictionary['SPOTdate']
    sobDate = dictionary['SOBdate']

    instrumentList = Get_MTM_Instruments(VALID_INSTYPES, spotDate)

    for instrument in instrumentList:
        spotPrice = Get_SOB_Price(instrument, spotDate)
        if spotPrice:
            Set_SPOT_SOB_Price(instrument, spotPrice, spotDate, sobDate)
        else:
            print 'Could not find %s SPOT for %s.' % (spotDate, instrument.Name())
