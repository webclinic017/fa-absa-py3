""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSInsClassification.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSInsClassification

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm

'''These methods are used to determine if an instrument is to be included in certain groups. Do not customise in this file,
use the inherited class in FUCITSHooks instead'''
class InstrumentDeterminationMethodsBase(object):

    @staticmethod
    def IsKindOf(obj, clsObj):
        try:
            return obj.IsKindOf(clsObj)
        except Exception as e:
            logger.ELOG('Could not determine if %s is of type %s. Reason: %s'%(str(obj), str(clsObj), str(e)))
            return False

    @classmethod
    def IsInstrument(cls, obj):
        return cls.IsKindOf(obj, acm.FInstrument)

    @classmethod
    def IsNormalBond(cls, obj):
        return cls.IsKindOf(obj, acm.FBond)

    @classmethod
    def IsZero(cls, obj):
        return cls.IsKindOf(obj, acm.FZeroBond)

    @classmethod
    def IsFlexiBond(cls, obj):
        return cls.IsKindOf(obj, acm.FFlexiBond)

    @classmethod
    def IsSecurityLoan(cls, obj):
        return cls.IsKindOf(obj, acm.FSecurityLoan)

    @classmethod
    def IsDerivative(cls, obj):
        return cls.IsKindOf(obj, acm.FDerivative)

    @classmethod
    def IsConvertible(cls, obj):
        return cls.IsKindOf(obj, acm.FConvertible)
        
    @classmethod
    def IsCombination(cls, obj):
        return cls.IsKindOf(obj, acm.FCombination)

    @classmethod
    def IsStock(cls, obj):
        return cls.IsKindOf(obj, acm.FStock)

    @classmethod
    def IsETF(cls, obj):
        return cls.IsKindOf(obj, acm.FETF)

    @classmethod
    def IsFundIns(cls, obj):
        return cls.IsKindOf(obj, acm.FFund)

    @classmethod
    def IsBill(cls, obj):
        return cls.IsKindOf(obj, acm.FBill)

    @classmethod
    def IsRepoReverse(cls, obj):
        return cls.IsKindOf(obj, acm.FRepo)

    @classmethod
    def IsCertificateOfDeposit(cls, obj):
        return cls.IsKindOf(obj, acm.FCertificateOfDeposit)
        
    @classmethod
    def IsOption(cls, obj):
        return cls.IsKindOf(obj, acm.FOption)
        
    @classmethod
    def IsFutureForward(cls, obj):
        return cls.IsKindOf(obj, acm.FFuture)   
     
    @classmethod
    def IsSwap(cls, obj):
        return cls.IsKindOf(obj, acm.FSwap)
        
    @classmethod
    def IsCurrencySwap(cls, obj):
        return cls.IsKindOf(obj, acm.FCurrencySwap)
        
    @classmethod
    def IsTRS(cls, obj):
        return cls.IsKindOf(obj, acm.FTotalReturnSwap)
        
    @classmethod
    def IsCFD(cls, obj):
        return cls.IsKindOf(obj, acm.FCfd)
        
    @classmethod
    def IsCDS(cls, obj):
        return cls.IsKindOf(obj, acm.FCreditDefaultSwap)

    @classmethod
    def IsBond(cls, obj):
        return cls.IsNormalBond(obj) or cls.IsZero(obj) or cls.IsFlexiBond(obj) or cls.IsConvertible(obj)

    @classmethod
    def IsEquity(cls, obj):
        return cls.IsStock(obj) or cls.IsETF(obj)

    @classmethod
    def IsTransferableSecurity(cls, obj):
        return cls.IsEquity(obj) or cls.IsBond(obj) or cls.IsSecurityLending(obj)

    @classmethod
    def IsSecurityLending(cls, obj):
        return cls.IsSecurityLoan(obj) or cls.IsRepoReverse(obj)

    @classmethod
    def IsMoneyMarketInstrument(cls, obj):
        return cls.IsBill(obj) or cls.IsCertificateOfDeposit(obj)

    @classmethod
    def IsFund(cls, obj):
        return cls.IsETF(obj) or cls.IsFundIns(obj)

    @classmethod
    def IsTSMM(cls, obj):
        return cls.IsTransferableSecurity(obj) or cls.IsMoneyMarketInstrument(obj)

    @classmethod
    def IsDebtSecurity(cls, obj):
        return cls.IsMoneyMarketInstrument(obj) or cls.IsBond(obj)