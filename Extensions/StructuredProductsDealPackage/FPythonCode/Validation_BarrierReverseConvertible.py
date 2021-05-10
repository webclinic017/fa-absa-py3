
from SP_DealPackageHelper import GetInitialFixingValue

# ############################################################
# Called from Product IsValid regardless of whether          #
# a combination is used or not                               #
# ############################################################
def GeneralValidateTradeParts(dp, exceptionAccumulator):
    pass

def GeneralValidate(dp, exceptionAccumulator):

    # Check bond and option contract sizes
    initialFixing = GetInitialFixingValue(dp.Option(), dp.Option().Underlying())
    
    if abs(    dp.Bond().ContractSize()
            - (dp.Option().ContractSize() * initialFixing) ) > 0.01:
        exceptionAccumulator('Bond and option notional amounts must agree.')
        
    # Right instrument types
    allInstruments = dp.DealPackage().Instruments()

# ############################################################
# Called from Product IsValid only if no combination is used #
# ############################################################
def IndividualTradesValidateTradeParts(dp, exceptionAccumulator):

    # Make sure that there are two trades in the package
    allTrades = dp.DealPackage().Trades()
    if len(allTrades) != 2:
        exceptionAccumulator(
                'Barrier Reverse Convertible should have 2 trades' )
    else:
        # And that the trades are option and bond trades
        if not (dp.OptionTrade() and dp.BondTrade()):
            exceptionAccumulator(
                'Product should consist of one option trade and one bond trade' )


def IndividualTradesValidate(dp, exceptionAccumulator):

    # Make sure that there are two instruments in the package
    allInstruments = dp.DealPackage().Instruments()
    if len(allInstruments) != 2:
        exceptionAccumulator(
                'Barrier Reverse Convertible should have 2 instruments' )
    else:
        # And that the instruments are option and bond
        if not (dp.Option() and dp.Bond()):
            exceptionAccumulator(
                'Product should consist of one option and one bond' )



# ############################################################
# Called from Product IsValid only if combination is used    #
# ############################################################

def CombinationValidateTradeParts(dp, exceptionAccumulator):

    # Make sure that there is one trade in the package
    allTrades = dp.DealPackage().Trades()
    if len(allTrades) != 1:
        exceptionAccumulator(
                'Barrier Reverse Convertible should have 1 trade (combination)' )
    else:
        # And that it is a combination trade
        if not (dp.CombinationTrade()):
            exceptionAccumulator(
                'Product should consist of one combination trade' )

def CombinationValidate(dp, exceptionAccumulator):

    allInstruments = dp.DealPackage().Instruments()
    comboInstruments = dp.Combination().Instruments()

    # First, make package validations
    
    # Make sure that there are three instruments (two plus combo) in the package    
    if len(allInstruments) != 3:
        exceptionAccumulator(
                'Barrier Reverse Convertible should have 3 instruments including combination' )

    else:
        # And that they are combination, bond and option
        if not (dp.Option() and dp.Bond() and dp.Combination()):
            exceptionAccumulator(
                'Product should consist of one combination, one option and one bond' )
    

    # Second, make combination validations
    
    # Make sure that the combination instrument contains the right amount of instruments
    rightNbrOfInstruments = True
    if len(comboInstruments) != 2:
        rightNbrOfInstruments = False
        exceptionAccumulator(
                'Barrier Reverse Convertible combination should contain one option and one bond' )

    # Make sure that the combination still contains the true Instrument Package instruments
    rightInstruments = True
    for ins in comboInstruments:
        if not (ins.Originator().Oid() in [x.Originator().Oid() for x in allInstruments]):
            rightInstruments = False
            exceptionAccumulator(
                'Instrument %s is not part of Deal Package and cannot be part of combiantion'
                    % (ins.Name()) )

    # Make sure that the combination weights have not been changed (only check if sure that right instruments are
    # incuded in combination)
    if rightInstruments and rightNbrOfInstruments:

        # SPR 386509
        if dp.Combination().IsStorageImage() == comboInstruments[0].IsStorageImage():
            mapOption = dp.Option()
            mapBond   = dp.Bond()
        else:
            # Combination is always storage image if above if statements is false
            # If the combiation components are not storage images, we need to compare with originals
            mapOption = dp.Option().Originator()
            mapBond   = dp.Bond().Originator()
    
        if dp.Combination().MapAtInstrument(mapOption).Weight() != -1.0:
            exceptionAccumulator(
                'Option weight must be -1.0' )
    
        if dp.Combination().MapAtInstrument(mapBond).Weight() != 1.0:
            exceptionAccumulator(
                'Bond weight must be 1.0' )


    # Make sure that combination contract size agrees to bond contract size
    if rightInstruments:
        if dp.Bond().ContractSize() != dp.Combination().ContractSize():
            exceptionAccumulator(
                'Combination contract size must agree to notional amount of components')
