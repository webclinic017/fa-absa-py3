import FRegulatoryLib
import acm
import FRegulatoryLogger
logger = 'FRegulatoryLibWrapper'

class wrapper(object):
    """base class for all wrapper classes"""
    def __init__(self):
        pass

    def checkAddInfoValueExists(self, acm_object, add_info_spec, acm_object_type, acm_object_name):
        """check of the AddInfo value exists for the given AddInfoSpec and object"""
        addInfoSpec = acm.FAdditionalInfoSpec[add_info_spec]
        add_info_val_exists = False
        add_info_val = acm.FAdditionalInfo.Select01(\
                    "addInf = %d and recaddr = %d"%(addInfoSpec.Oid(), acm_object.Oid()), None)
        if add_info_val in [None, '']:
            FRegulatoryLogger.INFO(logger, "AdditionalInfo <%s> does not have a value set on %s <%s>. Hence, inferring the value"%(add_info_spec, acm_object_type, acm_object_name))
        else:
            add_info_val_exists = True
        return add_info_val_exists

class JurisdictionNRegulatoryAuthority():
    def __init__(self, jurisdiction_lookup = None, regulatory_authority_lookup = None):
        self.__jurisdiction_lookup = jurisdiction_lookup
        self.__regulatory_authority_lookup = regulatory_authority_lookup

    def isJurisdiction(self, acm_object, jurisdiction):
        is_juridiction_val = None
        if acm_object.IsKindOf(acm.FParty):
            is_juridiction_val = FRegulatoryLib.PartyRegInfo(acm_object).is_jurisdiction(jurisdiction, self.__jurisdiction_lookup)
        if acm_object.IsKindOf(acm.FInstrument):
            is_juridiction_val = FRegulatoryLib.InstrumentRegInfo(acm_object).is_jurisdiction(jurisdiction, self.__jurisdiction_lookup)       
        return is_juridiction_val

    def isRegulatoryAuthority(self, acm_object, regulatory_authority):
        regulatory_authority_val = None
        if acm_object.IsKindOf(acm.FParty):
            regulatory_authority_val = FRegulatoryLib.PartyRegInfo(acm_object).is_regulatory_authority(regulatory_authority, self.__regulatory_authority_lookup)
        if acm_object.IsKindOf(acm.FInstrument):
            regulatory_authority_val = FRegulatoryLib.InstrumentRegInfo(acm_object).is_regulatory_authority(regulatory_authority, self.__regulatory_authority_lookup)
        return regulatory_authority_val

class accountWrapper(wrapper):
    """wrapper class for all APIs related to FAccount"""
    def __init__(self):
        pass
    
    def allocated(self, account):
        """return the inferred allocated value""" #TODO:
        pass
        return None

    def is_allocated_getter(self, account):
        """get the value of allocated if set on AddInfo"""
        is_allocated_val = None
        if self.checkAddInfoValueExists(account, 'regIsCmdtyAllocated', 'account', account.Name()):
            is_allocated_val = account.AdditionalInfo().RegIsCmdtyAllocated()
        if not is_allocated_val:
            is_allocated_val = self.allocated(account)
        return is_allocated_val

    def is_allocated_setter(self, account, is_allocated_val):
        """set the value of allocated on AddInfo"""
        account.AdditionalInfo().RegIsCmdtyAllocated(is_allocated_val)

class instrumentWrapper(wrapper):
    """wrapper class for all APIs related to FInstrument"""
    def __init__(self):
        pass

    def floating_rate_index(self, ins):
        float_rate_index = None
        if self.checkAddInfoValueExists(ins, 'ESMAIndex', 'instrument', ins.Name()):
            float_rate_index = ins.AdditionalInfo().ESMAIndex()
        return float_rate_index

    def is_government_guaranteed(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the IsGovernmentGuaranteed value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).is_government_guaranteed()

    def is_government_guaranteed_getter(self, ins):
        """get the value of the IsGovtGuaranteed AdditionalInfo
         value if present, else take it from Provider API"""
        is_govt_guaranteed_val = None
        if self.checkAddInfoValueExists(ins, 'regIsGovtGuaranteed', 'instrument', ins.Name()):
            is_govt_guaranteed_val = ins.AdditionalInfo().RegIsGovtGuaranteed()
        if not is_govt_guaranteed_val:
            is_govt_guaranteed_val = self.is_government_guaranteed(ins)
        return is_govt_guaranteed_val

    def is_government_guaranteed_setter(self, ins, is_govt_guaranteed_val):
        """set the value on the IsGovtGuaranteed AdditionalInfo"""
        ins.AdditionalInfo().RegIsGovtGuaranteed(is_govt_guaranteed_val)

    def is_covered(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the IsCovered value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).is_covered()

    def is_covered_getter(self, ins):
        """get the value of the regIsCovered AdditionalInfo value
         if present, else get it from ProviderData if available"""
        is_covered_val = None
        if self.checkAddInfoValueExists(ins, 'regIsCovered', 'instrument', ins.Name()):
            is_covered_val = ins.AdditionalInfo().RegIsCovered()
        if not is_covered_val:
            is_covered_val = self.is_covered(ins)
        return is_covered_val

    def is_covered_setter(self, ins, is_covered_val):
        """set the value on the IsCovered AdditionalInfo"""
        ins.AdditionalInfo().RegIsCovered(is_covered_val)

    def outstanding_shares(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the OutstandingShares value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).outstanding_shares()

    def outstanding_shares_getter(self, ins):
        """get the value of the regOutStndingShares AdditionalInfo value
         if present, else get it from ProviderData if available"""
        market_cap_val = None
        if self.checkAddInfoValueExists(ins, 'regOutStndingShares', 'instrument', ins.Name()):
            market_cap_val = ins.AdditionalInfo().RegOutStndingShares ()
        if not market_cap_val:
            market_cap_val = self.outstanding_shares(ins)
        return market_cap_val

    def outstanding_shares_setter(self, ins, outstanding_shares_val):
        """set the value on the MarketCap AdditionalInfo"""
        ins.AdditionalInfo().RegOutStndingShares (outstanding_shares_val)

    def issuer_type(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the IssuerType value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).issuer_type()

    def issuer_type_getter(self, ins):
        """get the value of the issuerType AdditionalInfo
         value if present, else get it from ProviderData if available"""
        issuer_type_val = None
        if self.checkAddInfoValueExists(ins, 'regIssuerType', 'instrument', ins.Name()):
            issuer_type_val = ins.AdditionalInfo().RegIssuerType()
        if not issuer_type_val:
            issuer_type_val = self.issuer_type(ins)
        return issuer_type_val

    def issuer_type_setter(self, ins, issuer_type_val):
        """set the value on the IssuerType AdditionalInfo"""
        ins.AdditionalInfo().RegIssuerType(issuer_type_val)

    def country_of_issue(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the CountryOfIssue value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).country_of_issue()

    def country_of_issue_setter(self, ins, country_of_issue_val):
        """set the value on the CountryOfIssue AdditionalInfo"""
        ins.AdditionalInfo().RegCountryOfIssue(country_of_issue_val)

    def country_of_issue_getter(self, ins):
        """get the value of the countryOfIssue AdditionalInfo
         value if present, else infer it if possible"""
        country_of_issue_val = None
        if self.checkAddInfoValueExists(ins, 'regCountryOfIssue', 'instrument', ins.Name()):
            country_of_issue_val = ins.AdditionalInfo().RegCountryOfIssue()
        if not country_of_issue_val:#it means the AddInfo exists, but the value is not set on it.
            country_of_issue_val = self.country_of_issue(ins)
        return country_of_issue_val

    def hi_qlty_liquid_asset_getter(self, ins):
        """get the value of the regHiQltyLqdAsset AdditionalInfo value if present"""
        hi_qlty_lqd_asset_val = ''
        if self.checkAddInfoValueExists(ins, 'regHiQltyLqdAsset', 'instrument', ins.Name()):
            hi_qlty_lqd_asset_val = ins.AdditionalInfo().RegHiQltyLqdAsset()
        return hi_qlty_lqd_asset_val

    def hi_qlty_liquid_asset_setter(self, ins, hi_qlty_liquid_asset_val):
        """set the value on the regHiQltyLqdAsset AdditionalInfo"""
        ins.AdditionalInfo().RegHiQltyLqdAsset(str(hi_qlty_liquid_asset_val))
   
    def bond_type(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the BondType value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).bond_type()

    def bond_type_getter(self, ins):
        """get the value of the regBondType AdditionalInfo
         value if present, else get it from ProviderData
          if available"""
        bond_type_val = ''
        if self.checkAddInfoValueExists(ins, 'regBondType', 'instrument', ins.Name()):
            bond_type_val = ins.AdditionalInfo().RegBondType()
        if not bond_type_val:
            bond_type_val = self.bond_type(ins)
        return bond_type_val

    def bond_type_setter(self, ins, bond_type):
        """set the value on the regBondType AdditionalInfo"""
        ins.AdditionalInfo().RegBondType(bond_type)

    def bbg_collateral_type(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the CollateralType value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).bbg_collateral_type()

    def bbg_collateral_type_getter(self, ins):
        """get the value of the collateralType AdditionalInfo value
         if present, else get it from ProviderData if available"""
        collateral_type_val = ''
        if self.checkAddInfoValueExists(ins, 'regCollateralType', 'instrument', ins.Name()):
            collateral_type_val = ins.AdditionalInfo().RegCollateralType()
        if not collateral_type_val:
            collateral_type_val = self.bbg_collateral_type(ins)
        return collateral_type_val

    def bbg_collateral_type_setter(self, ins, collateral_type):
        """set the value on the regCollateralType AdditionalInfo"""
        ins.AdditionalInfo().RegCollateralType(collateral_type)

    def is_equity_getter(self, ins):
        """get the value of the isEquity AdditionalInfo
         value if present, else infer it"""
        is_equity_val = None
        if self.checkAddInfoValueExists(ins, 'regIsEquity', 'instrument', ins.Name()):
            is_equity_val = ins.AdditionalInfo().RegIsEquity()
        if not is_equity_val:
            is_equity_val = self.is_equity(ins)
        return is_equity_val

    def is_equity_setter(self, ins, is_equity_val):
        """set the value on the IsEquity AdditionalInfo"""
        ins.AdditionalInfo().RegIsEquity(is_equity_val)

    def is_equity(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the EquityType value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).is_equity()

    def fund_type_getter(self, ins):
        """get the value of the fundType AdditionalInfo value if present, else get it from ProviderData if available"""
        fund_type_val = ''
        if self.checkAddInfoValueExists(ins, 'regFundType', 'instrument', ins.Name()):
            fund_type_val = ins.AdditionalInfo().RegFundType()
        if not fund_type_val:
            fund_type_val = self.fund_type(ins)
        return fund_type_val

    def fund_type_setter(self, ins, fund_type):
        """set the value on the FundType AdditionalInfo"""
        ins.AdditionalInfo().RegFundType(fund_type)

    def fund_type(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the FundType value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).fund_type()

    def main_trading_place_getter(self, ins):
        """get the value of the mainTradinPlace AdditionalInfo value if present, else infer it from ProviderData if available"""
        main_trading_place = ''
        if self.checkAddInfoValueExists(ins, 'regMainTradingPlace', 'instrument', ins.Name()):
            main_trading_place = ins.AdditionalInfo().RegMainTradingPlace()
        if not main_trading_place:
            main_trading_place = FRegulatoryLib.InstrumentRegInfo(ins).main_trading_place()
        return main_trading_place

    def main_trading_place_setter(self, ins, main_trading_place):
        """set the value on the MainTradingPlace AdditionalInfo"""
        ins.AdditionalInfo().RegMainTradingPlace(main_trading_place)

    def main_trading_place(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred MainTradingPlace value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).main_trading_place()

    def sftr_security_type(self, ins):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred SFTRSecurityType value"""
        return FRegulatoryLib.InstrumentRegInfo(ins).sftr_security_type()

    def sftr_security_type_getter(self, ins):
        """get the value of the sFTRSecurityType AdditionalInfo value
         if present, else get it from ProviderData if available"""
        SFTR_security_type = ''
        if self.checkAddInfoValueExists(ins, 'regSFTRSecurityType',\
                                         'instrument', ins.Name()):
            SFTR_security_type = ins.AdditionalInfo().RegSFTRSecurityType()
        if not SFTR_security_type:
            SFTR_security_type = self.sftr_security_type(ins)
        return SFTR_security_type

    def sftr_security_type_setter(self, ins, sftr_security_type):
        """set the value on the SFTRSecurityType AdditionalInfo"""
        ins.AdditionalInfo().RegSFTRSecurityType(sftr_security_type)

  
class sftrWrapper(wrapper):
    def __init__(self):
        pass

    def date_period_unit(self, acm_object):
        pass

    def day_count_method(self, acm_object):
        pass

        
        
        
class tradeWrapper(wrapper):
    """wrapper class for all APIs related to FTrade"""
    def __init__(self):
        pass

    def is_cleared_getter(self, trd):
        """get the value of the IsCleared AdditionalInfo
         value if present, else infer it"""
        is_cleared_val = None
        if self.checkAddInfoValueExists(trd, 'regIsCleared', 'trade', trd.Oid()):
            is_cleared_val = trd.AdditionalInfo().RegIsCleared()
        else:
            is_cleared_val = self.is_cleared(trd)
        return is_cleared_val

    def is_cleared_setter(self, trd, is_cleared_val):
        """set the value on isCleared AdditionalInfo"""
        trd.AdditionalInfo().RegIsCleared(is_cleared_val)

    def is_cleared(self, trd):
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the IsCleared value"""
        return FRegulatoryLib.TradeRegInfo(trd).is_cleared()

    def sftr_is_collateral_provider(self, trd):#
        """if the AdditionalInfo or the AdditionalInfoSpec does
         not exist, return the inferred the SFTRIsCollateralProvider value"""
        return FRegulatoryLib.TradeRegInfo(trd).sftr_is_collateral_provider()

    def sftr_is_collateral_provider_getter(self, trd):
        """get the value of the isCollateralProvdr AdditionalInfo
         value if present, else get it from ProviderData if available"""
        is_collateral_proivder_val = None
        if self.checkAddInfoValueExists(trd, 'regIsCollatrlPrvdr', 'trade', trd.Name()):
            is_collateral_proivder_val = trd.AdditionalInfo().RegIsCollatrlPrvdr()
        if not is_collateral_proivder_val:
            is_collateral_proivder_val = self.sftr_is_collateral_provider(trd)
        return is_collateral_proivder_val

    def sftr_is_collateral_provider_setter(self, trd, is_coll_provider_val):
        """set the value on the IsCollateralProvdr AdditionalInfo"""
        trd.AdditionalInfo().RegIsCollatrlPrvdr(is_coll_provider_val)

    def sftr_type(self, trd):
        return FRegulatoryLib.SFTRLib(trd).sftr_type()

    def sftr_type_getter(self, trd):
        """get the value of the sFTTRype AdditionalInfo value
         if present, else get it from fallback"""
        sf_type = ''
        if self.checkAddInfoValueExists(trd, 'regSFTRType',\
                                         'trade', trd.Name()):
            sf_type = trd.AdditionalInfo().RegSFTRType()
        if not sf_type:
            sf_type = self.sftr_type(trd)
        return sf_type

    def sftr_type_setter(self, trd, sftype_val):
        """set the value on the SFTRType AdditionalInfo"""
        trd.AdditionalInfo().RegSFTRType(sftype_val)

    def sftr_asset(self, trd):
        return FRegulatoryLib.SFTRLib(trd).sftr_asset_type()

    def sftr_asset_getter(self, trd):
        """get the value of the sFTRAsset AdditionalInfo value
         if present, else get it from fallback"""
        sftr_asset = ''
        if self.checkAddInfoValueExists(trd, 'regSFTRAsset',\
                                         'trade', trd.Name()):
            sftr_asset = trd.AdditionalInfo().RegSFTRAsset()
        if not sftr_asset:
            sftr_asset = self.sftr_asset(trd)
        return sftr_asset


    def sftr_asset_setter(self, trd, sftr_asset_val):
        """set the value on the SFTRAsset AdditionalInfo"""
        trd.AdditionalInfo().SFTRAsset(sftr_asset_val)

    def sftr_security_quality(self, trd):
        return FRegulatoryLib.SFTRLib(trd).sftr_security_quality()

    def sftr_security_quality_getter(self, trd):
        """get the value of the regSFTRSecurityQlty AdditionalInfo value
         if present, else get it from fallback"""
        sftr_security_quality = ''
        if self.checkAddInfoValueExists(trd, 'regSFTRSecurityQlty',\
                                         'trade', trd.Name()):
            sftr_security_quality = trd.AdditionalInfo().RegSFTRSecurityQlty()
        if not sftr_security_quality:
            sftr_security_quality = self.sftr_security_quality(trd)
        return sftr_security_quality

    def sftr_security_quality_setter(self, trd, sec_qlty_val):
        """set the value on the regSFTRSecurityQlty AdditionalInfo"""
        trd.AdditionalInfo().RegSFTRSecurityQlty(sec_qlty_val)

    def product_sub_group_getter(self, trd):
        """get the value of the regProductSubGroup AdditionalInfo value
         if present, else get it from fallback"""
        product_sub_group = ''
        if self.checkAddInfoValueExists(trd, 'regProductSubGroup',\
                                         'trade', trd.Name()):
            product_sub_group = trd.AdditionalInfo().RegProductSubGroup()
        if not product_sub_group:
            product_sub_group = self.product_sub_group(trd)
        return product_sub_group

    def product_sub_group_setter(self, trd, product_sub_group_val):
        """set the value on the regProductSubGroup AdditionalInfo"""
        trd.AdditionalInfo().RegProductSubGroup(product_sub_group_val)

    def product_sub_group(self, trd):
        return FRegulatoryLib.MMSLib(trd).product_sub_group()

    def asset_class_getter(self, trd):
        """get the value of the regAssetClass AdditionalInfo value
         if present, else get it from fallback"""
        asset_class = ''
        if self.checkAddInfoValueExists(trd, 'regAssetClass',\
                                         'trade', trd.Name()):
            asset_class = trd.AdditionalInfo().RegAssetClass()
        if not asset_class:
            asset_class = self.asset_class(trd)
        return asset_class

    def asset_class_setter(self, trd, asset_class_val):
        """set the value on the regAssetClass AdditionalInfo"""
        trd.AdditionalInfo().RegAssetClass(asset_class_val)

    def asset_class(self, trd):
        return FRegulatoryLib.MMSLib(trd).asset_class()

