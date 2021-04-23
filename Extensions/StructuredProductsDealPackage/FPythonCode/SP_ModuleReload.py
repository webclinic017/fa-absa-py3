
# Need to add
#    Additional Info
#    - Participation (DealPackage)
#    - CapitalProtection (DealPackage)
#    - StrikePricePct (Instrument)
#    - BarrierLevelPct (Instrument)
#    - ProductQuantity (Deal Package)
#    - AccumulatorLeverage
#    Exotic Events
#    - Initial Fixing
#    ChoiceLists
#    - AccDec (Val Group)
#    - accDecModelDesc (Valuation Extension)


import SP_DealPackageHelper
import importlib
importlib.reload(SP_DealPackageHelper)

import SP_BusinessCalculations
importlib.reload(SP_BusinessCalculations)

import CompositeComponentBase
importlib.reload(CompositeComponentBase)

import CompositeExoticEventComponents
importlib.reload(CompositeExoticEventComponents)

import CompositeExoticComponents
importlib.reload(CompositeExoticComponents)

import CompositeOptionAdditionComponents
importlib.reload(CompositeOptionAdditionComponents)

import CompositeCashFlowComponents
importlib.reload(CompositeCashFlowComponents)

import CompositeOptionComponents
importlib.reload(CompositeOptionComponents)

import CompositeBasketComponents
importlib.reload(CompositeBasketComponents)

import CompositeBasketOptionComponents
importlib.reload (CompositeBasketOptionComponents)

import CompositeTradeComponents
importlib.reload(CompositeTradeComponents)

import StructuredProductBase
importlib.reload(StructuredProductBase)

import Validation_BarrierReverseConvertible
importlib.reload(Validation_BarrierReverseConvertible)

import SP_BarrierReverseConvertible
importlib.reload(SP_BarrierReverseConvertible)

import SP_CapitalProtectedNote
importlib.reload(SP_CapitalProtectedNote)

import SP_EqStraddle
importlib.reload(SP_EqStraddle)

import SP_CallPutSpread
importlib.reload(SP_CallPutSpread)

import SP_DualCurrencyDeposit
importlib.reload(SP_DualCurrencyDeposit)

import SP_WeddingCakeDeposit
importlib.reload(SP_WeddingCakeDeposit)

import SP_AccumulatorSetup
importlib.reload(SP_AccumulatorSetup)

import SP_AccumulatorCustomInsDef
importlib.reload(SP_AccumulatorCustomInsDef)

import SP_AccumulatorValuation
importlib.reload(SP_AccumulatorValuation)

import SP_AccumulatorModel
importlib.reload(SP_AccumulatorModel)

import SP_AccumulatorDealPackage
importlib.reload(SP_AccumulatorDealPackage)

import SP_Autocall
importlib.reload(SP_Autocall)

import SP_CapitalProtectedCertificate
importlib.reload(SP_CapitalProtectedCertificate)

import SP_CustomTradeActions
importlib.reload(SP_CustomTradeActions)

import SP_InvokeTradeActions
importlib.reload(SP_InvokeTradeActions)

import CustomLifeCycleEvents
importlib.reload(CustomLifeCycleEvents)

