"""------------------------------------------------------------------------
MODULE
    FRegulatoryLib -
DESCRIPTION:
    This file is provided to the user to add overrides to the default implementation of the API provided in FRegulatoryLibBase
VERSION: 1.0.25(0.25.7)
--------------------------------------------------------------------------"""
import FRegulatoryLibBase

class InstrumentRegInfo(FRegulatoryLibBase.InstrumentRegInfoBase):

    def __init__(self, instrument=None):
        super(InstrumentRegInfo, self).__init__(instrument)


class ISO3166CountryCode(FRegulatoryLibBase.ISO3166CountryCodeBase):

    def __init__(self, custom_dict={}):
        super(ISO3166CountryCode, self).__init__(custom_dict)


class PartyRegInfo(FRegulatoryLibBase.PartyRegInfoBase):

    def __init__(self, party=None):
        super(PartyRegInfo, self).__init__(party)

class Taxonomy(FRegulatoryLibBase.TaxonomyBase):

    def __init__(self, acm_object=None):
        super(Taxonomy, self).__init__(acm_object)


class TradeRegInfo(FRegulatoryLibBase.TradeRegInfoBase):

    def __init__(self, trade=None):
        super(TradeRegInfo, self).__init__(trade)

class PersonRegInfo(FRegulatoryLibBase.PersonRegInfoBase):
    
    def __init__(self, acm_object):
        super(PersonRegInfo, self).__init__(acm_object)

class UniqueTradeIdentifier(FRegulatoryLibBase.UniqueTradeIdentifierBase):

    def __init__(self, acm_object=None):
        super(UniqueTradeIdentifier, self).__init__(acm_object)

class MMSLib(FRegulatoryLibBase.MMSLibBase):
    def __init__(self, trade=None):
        super(MMSLib, self).__init__(trade)

class SFTRLib(FRegulatoryLibBase.SFTRLibBase):
    def __init__(self, trade=None):
        super(SFTRLib, self).__init__(trade)

