''' ======================================================================================================================
    TMS_AssetClasses
    Purpose                 :   This module is used to determine asset class of trades.
                                Currently used to check if conversion of a trade from 
                                one type to another is allowed.
    Department and Desk     :   SM IT Pricing & Risk
    Requester               :   Matthew Berry
    Developer               :   Eben Mare, Peter Kutnik
    CR Number               :   TBD
    
    =======================================================================
    
    Purpose                 : Added TradeWrapper factories for FX Products as well as FX Asset Classes
                            : Configuration.
    Department and Desk     : SM IT Pricing & Risk
    Requester               : Matthew Berry
    Developer               : Babalo Edwana
    CR Number               : 261644
    ==========================================================================================================================
    
    Purpose                 : Removed TradeWrapper factories for Equity Products as well as Equity Asset Classes
                            : Configuration.
    Department and Desk     : SM IT Pricing & Risk
    Developer               : Jan Mach
    CR Number               : CHNG0001177565
    =========================================================================================================================='''
import ael

from TMS_TradeWrapper_FX import TradeWrapperFactories as FXFactories
from TMS_TradeWrapper_IRD import TradeWrapperFactories as IRDFactories

class AssetConfig:
    def _name(self):
        raise NotImpementedError

    def _tradefactories(self):
        raise NotImpementedError

    def _allowableConversions(self):
        raise NotImpementedError

class IRDAssetConfig(AssetConfig):
    def _name(self):
        return "IRD"

    def _tradefactories(self):
        return IRDFactories

    def _allowableConversions(self):
        return ()

class FXAssetConfig(AssetConfig):
    def _name(self):
        return "FXO"

    def _tradefactories(self):
        return FXFactories

    def _allowableConversions(self):
        return ( ("Touch", "Digital"), ("Digital", "Touch") )

TradeFactories = IRDFactories + FXFactories
