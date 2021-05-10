import acm
import FUxCore
from math import floor
from math import log10
from math import fabs
import FBDPRollback
import FBDPString


# vvvvvv Ctrl Callback Functions vvvvvv

def OnAmount1Changed( self, cd ):
    self.UpdateAmount2Field()
    
def OnToPortfolioChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        toPortfolio = acm.FPhysicalPortfolio[self.m_toPortfolioCtrl.GetData()]
        self.SetToPortfolio(toPortfolio)
        self.callbackDisabler.Disable(False)
        
def OnToPairChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        newToPair = self.m_toPairBinder.GetValue()
        self.SetToPair(newToPair)
        self.callbackDisabler.Disable(False)
    
def OnFromPairSpotChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateFromPairRate()
        self.UpdateAmount2Field()
        self.UpdateTriangulatedSplitPairPrices()
        self.callbackDisabler.Disable(False)

def OnFromPairPointsChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateFromPairRate()
        self.UpdateAmount2Field()
        self.UpdateTriangulatedSplitPairPrices()
        self.callbackDisabler.Disable(False)
        
def OnFromPairRateChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateFromPairSpot()
        self.UpdateAmount2Field()
        self.UpdateTriangulatedSplitPairPrices()
        self.callbackDisabler.Disable(False)
        
def OnToPairSpotChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateToPairRate()
        self.UpdateTriangulatedSplitPairPrices()
        self.callbackDisabler.Disable(False)

def OnToPairPointsChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateToPairRate()
        self.UpdateTriangulatedSplitPairPrices()
        self.callbackDisabler.Disable(False)

def OnToPairRateChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateToPairSpot()
        self.UpdateTriangulatedSplitPairPrices()
        self.callbackDisabler.Disable(False)

def OnSplitPairSpotChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateSplitPairRate()
        self.UpdateTriangulatedToPairPrices()
        self.callbackDisabler.Disable(False)

def OnSplitPairPointsChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateSplitPairRate()
        self.UpdateTriangulatedToPairPrices()
        self.callbackDisabler.Disable(False)

def OnSplitPairRateChanged( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.UpdateSplitPairSpot()
        self.UpdateTriangulatedToPairPrices()
        self.callbackDisabler.Disable(False)

def OnSplitPortfolioChanged( self, cd ):
    splitPortfolio = acm.FPhysicalPortfolio[self.m_splitPortfolioCtrl.GetData()]
    self.SetSplitPortfolio(splitPortfolio)

def OnFromFwdPortfolioChanged( self, cd ):
    self.UpdateFromPairDefaultFwdAcquirer()
    
def OnToFwdPortfolioChanged( self, cd ):
    self.UpdateToPairDefaultFwdAcquirer()
    
def OnSplitFwdPortfolioChanged( self, cd ):
    self.UpdateSplitPairDefaultFwdAcquirer()
    
def OnUseMainRateMarketClicked( self, cd ):
    if self.callbackDisabler.NotDisabled():
        self.callbackDisabler.Disable(True)
        self.m_useMarketRates = True
        self.SetRates()
        self.callbackDisabler.Disable(False)
    
def OnOkButtonClicked(self, arg):
    self.m_fuxDlg.CloseDialogOK()

# ^^^^^^ Ctrl Callback Functions ^^^^^^
