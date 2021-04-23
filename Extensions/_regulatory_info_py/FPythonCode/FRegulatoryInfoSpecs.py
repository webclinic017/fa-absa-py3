""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/General/Adaptations/FRegulatoryInfoSpecs.py"
import acm
import string
import FIntegrationUtils

addInfoSpecsDescrOnTrade = {
    'regClearingHouse': 'Clearing house or CCP where trade is cleared',
    'regClearingBroker': 'Clearing member used to clear',
    'regMiddleware': 'Middleware Party',
    'regOriginalCpty': 'For tri-party brokerage deals and for Novations',
    'regRepository': 'Repository where trade is/shall be reported',
    'regTradingCapacity': 'TradingCapacity',
    'regComplexTrdCmptId': 'Identifies groups of trades',
    'regWaiver': 'Waiver',
    'regOurOrg': 'Our side Buyer/Seller of the Financial instrument',
    'regOurTransmitOrg': 'Firm transmitting the order on our side.',
    'regOurInvesDecider': 'Identifies who makes the decision of the financial instrument on our side.',
    'regOurTrader': 'Our Trader buying/selling the financial instrument',
    'regExecutingEntity': 'Entity executing the transaction',
    'regVenue': 'Identification of the venue where the transaction was executed',
    'regBranchMemberShip': 'Investment firms market membership for transaction execution',
    'regTheirOrg': 'Their Disposer/Buyer of the financial instrument.',
    'regTheirInvDecider': 'Identifies who makes the decision to buy/sell the financial instrument on their side.',
    'regTheirTrader': 'Trader selling/buying the financial instrument on their side',
    'regReportingEntity': 'Entity submitting the transaction report to the competent authority',
    'regOTCPostTradeInd': 'OTC Post Trade Indicator',
    'regComdtyDerivInd': 'Indicates whether the transaction reduces risk',
    'regSecFinTransInd': 'Indicates whether the entity identified is an investment firm covered by Directive 2004/39/EC or Directive 2014/65/EU.',
    'regMicroSeconds': 'High precision trade time (microseconds)',
    'is_tdr': 'Is the Party a Trade Documenation Repository',
    'regRepositoryId': 'Id issued by Approved Publication Arrangement when the trade is reported',
    'regIsHedge': 'indicates whether the transaction reduces risk in an objectively measurable way',
    'regExchangeId': 'The identification number from the exchange',
    'regAlgoId': 'Name of Algorithm used to trade the trade',
    'regDirectedOrder': 'Boolean indicating whether the order was open to be traded on any exchange, or directed to a specific exchange',
    'regProvideLiquidity': 'Describes if the order was providing liquidity, taking liquidity, or none of these (or not known)',
    'regConfirmationTime': 'Time when trade was confirmed, if Confirmation records are not used',
    'regClearingTime': 'Time when trade was cleared, if Settlement records are not used',
    'regRptDeferToTime': 'If a deferral has been waived by us on the trade, until when is the reporting deferred.',
    'regInvesDecidrCrmId': 'Customer Relationship Management Id of the investment decider',
    'regInsCfiCode': 'CFI Code on the instrument being linked on FX trades',
    'regInsIsin': 'Isin of the instrument being linked on FX trades',
    'regLegIsin': 'Leg Isin of the trade Applicable only for FX Swaps',
    'regNearLegIsin': 'Near Leg Isin of the trade Applicable only for FX Swaps',
    'regFarLegIsin': 'Far Leg Isin of the trade Applicable only for FX Swaps',
    'regTransmOfOrder': 'Indicator of whether the conditions for order transmission are satisfied.',
    'regShortSell': 'ShortSellIndicator',
}

addInfoSpecsDescrOnInstrument = {
    'regTransactionType': 'TransactionType',
    'regFinalPriceType': 'FinalPriceType',
    'regClearingIsMandat': 'Is clearing mandatory',
    'regCFICode': 'CFI Code',
    'ESMAIndex': 'ESMAIndex',
    'regLargeInScale': 'The (Pre) Nominal amount where an order will be deemed large in scale, affecting pre and post trade reporting requirements',
    'regPostLargeInScale': 'The (Post) Nominal amount where an order will be deemed large in scale, affecting pre and post trade reporting requirements',
    'regSSTI': '(Pre) Size specific to a bond, structured finance product, emission allowance or derivative traded on a Trading Venue',
    'regPostSSTI': '(Post) Size specific to a bond, structured finance product, emission allowance or derivative traded on a Trading Venue',
    'regSMS': 'Average values of orders executed on a Trading Venue, per instrument class, during previous year',
    'regIsLiquid': 'Liquidity is a judgement call from authorities',
    'regIsSysInternalizr': 'Is the bank a Systematic Internaliser in this instrument',
    'regTrdAdmisAppTime': 'Date and time the issuer has approved admission to trading on a Trading Venue',
    'regTrdAdmisReqTime': 'Date and time of the request for admission to trading on a Trading Venue',
    'regFirstTradeTime': 'Date and time of the admission to, or the first quote, order or trade on a Trading Venue',
    'regTrdTerminateDate': 'Date when Instrument ceases to be traded on Trading Venue',
    'regCmdty': 'Classfication for the commodity instruments into their Sub and Further Sub Products',
    'regHasTrdObligation': 'Must this instrument be traded on a regulated exchange, or can it be traded OTC as well [tri-state]',
    'regAvgDailyTO': 'The average daily turnover in the instrument, as reported by authorities.',
    'regSimilarIsin': 'Link to ISIN similar to this one',
    'regToTV': 'Is this instrument being traded on the trading venue',
    'regLiquidityBand': 'LiquidityBand of the instrument',
    'regPrimaryMktMic' : 'Primary Market MIC',
    'regMaterialMktMic' : 'Material Market MIC',
    'regDarkCapStatus' : 'DarkCapStatus',
    'regDarkCapMic' : 'Dark trading venue MIC',
    'regTickSize' : 'Minimum price movement of a trading instrument',
    'regDblVolCapStatus' : 'Limiting the total amount of trading that can be done in any particular equity instrument under these waivers.',
    'regMiFIDTransparent' : 'Is the instrument MiFID Transparent',
    'regFISN' : 'Financial Instrument Short Name'
}

addInfoSpecsDescrOnParty = {
    'regIsInvestmentFirm': 'Indicates whether the entity is an investment firm',
    'regPossibleReporter': 'Possible reporter',
    'regFinancialCategor': 'FinancialCategory',
    'regIsAlgorithm': 'Party within the firm executing as an algorithm to execute transactions automatically without human intervention',
    'regPtyExchangeId': 'The identifier used towards/by an exchange to identify a person or legal entity, before the actual national id or the LEI is divulged.',
    'regPtyCrmId': 'Customer Relationship Management Id',
    'regMifidCategory': 'MiFIDCategory',
    'regIsVenue': 'Indicates whether the party is a Venue or not',
}

addInfoSpecsDescrOnContact = {
    'dateOfBirth': 'Date of Birth of the contact',
    'firstName': 'First Name of the contact',
    'lastName': 'Last Name of the contact',
    'nationalId': 'National Id of the contact',
    'regContactCrmId': 'Customer Relationship Management Id',
    'uniqueName': 'An optional unique name, if specified there can only be one contact with this name for each party.',
    'regContExchangeId': 'The identifier used towards/by an exchange to identify a person or legal entity, before the actual national id or the LEI is divulged.',
    'regGeneralPartner': "General partner has responsibility for the actions of the business, can legally bind the business and is personally liable for all the business's debts and obligations"
}
addInfoSpecsDescrOnUser = {
    'regDiscreteTrader': 'The discretionaryTrader Contact linked to the FUser',
}
choicelistVal = {
'TradingCapacity':          [{'name': 'DEAL', 'description': 'Dealing on own account(MiFID-II Ref Data)'},
                            {'name': 'MTCH', 'description': 'Matched principal(MiFID-II Ref Data)'},
                            {'name': 'AOTC', 'description': 'Any other capacity(MiFID-II Ref Data)'}],
'Waiver':                   [{'name': 'RFPT', 'description': 'Reference price(MiFID-II Ref Data)'},
                            {'name': 'NLIQ', 'description': 'Negotiated (liquid)(MiFID-II Ref Data)'},
                            {'name': 'OILQ', 'description': 'Negotiated (illiquid)(MiFID-II Ref Data)'},
                            {'name': 'PRIC', 'description': 'Negotiated  (conditions)(MiFID-II Ref Data)]'},
                            {'name': 'SIZE', 'description': 'Above specified size(MiFID-II Ref Data)'},
                            {'name': 'ILQD', 'description': 'Illiquid instrument(MiFID-II Ref Data)'}],
'OTCPostTradeIndicator':    [{'name': 'BENC', 'description': 'Benchmark(MiFID-II Ref Data)'},
                            {'name': 'ACTX', 'description': 'Agency cross(MiFID-II Ref Data)'},
                            {'name': 'LRGS', 'description': 'Large in scale(MiFID-II Ref Data)'},
                            {'name': 'ILQD', 'description': 'Illiquid instrument(MiFID-II Ref Data)'},
                            {'name': 'SIZE', 'description': 'Above specified size(MiFID-II Ref Data)'},
                            {'name': 'CANC', 'description': 'Cancellations(MiFID-II Ref Data)'},
                            {'name': 'AMND', 'description': 'Amendments(MiFID-II Ref Data)'},
                            {'name': 'SDIV', 'description': 'Special dividend(MiFID-II Ref Data)'},
                            {'name': 'RPRI', 'description': 'Price improvement(MiFID-II Ref Data)'},
                            {'name': 'DUPL', 'description': 'Duplicative(MiFID-II Ref Data)'},
                            {'name': 'TNCP', 'description': 'Not contributing to the price discovery process(MiFID-II Ref Data)'},
                            {'name': 'TPAC', 'description': 'Package(MiFID-II Ref Data)'},
                            {'name': 'XFPH', 'description': 'Exchange for Physical(MiFID-II Ref Data)'}],
'CommodityBaseProduct':     [{'name': 'AGRI', 'description': 'Agricultural(MiFID-II Ref Data)'},
                            {'name': 'NRGY', 'description': 'Energy(MiFID-II Ref Data)'},
                            {'name': 'ENVR', 'description': 'Environmental(MiFID-II Ref Data)'},
                            {'name': 'FRGT', 'description': 'Freight(MiFID-II Ref Data)'},
                            {'name': 'FRTL', 'description': 'Fertilizer(MiFID-II Ref Data)'},
                            {'name': 'INDP', 'description': 'Industrial products(MiFID-II Ref Data)'},
                            {'name': 'METL', 'description': 'Metals(MiFID-II Ref Data)'},
                            {'name': 'MCEX', 'description': 'Multi Commodity Exotic(MiFID-II Ref Data)'},
                            {'name': 'PAPR', 'description': 'Paper(MiFID-II Ref Data)'},
                            {'name': 'POLY', 'description': 'Polypropylene(MiFID-II Ref Data)'},
                            {'name': 'INFL', 'description': 'Inflation(MiFID-II Ref Data)'},
                            {'name': 'OEST', 'description': 'Official economic statistics(MiFID-II Ref Data)'},
                            {'name': 'OTHC', 'description': 'Other C10(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'}, ],
'AGRI':                     [{'name': 'GROS', 'description': 'Grains Oil Seeds(MiFID-II Ref Data)'},
                            {'name': 'SOFT', 'description': 'Softs(MiFID-II Ref Data)'},
                            {'name': 'OOLI', 'description': 'Olive oil(MiFID-II Ref Data)'},
                            {'name': 'DIRY', 'description': 'Dairy(MiFID-II Ref Data)'},
                            {'name': 'FRST', 'description': 'Forestry(MiFID-II Ref Data)'},
                            {'name': 'SEAF', 'description': 'Seafood(MiFID-II Ref Data)'},
                            {'name': 'LSTK', 'description': 'Livestock(MiFID-II Ref Data)'},
                            {'name': 'GRIN', 'description': 'Grain(MiFID-II Ref Data)'},
                            {'name': 'POTA', 'description': 'Potato(MiFID-II Ref Data)'}, ],
'NRGY':                     [{'name': 'ELEC', 'description': 'Electricity(MiFID-II Ref Data)'},
                            {'name': 'NGAS', 'description': 'Natural Gas(MiFID-II Ref Data)'},
                            {'name': 'OILP', 'description': 'Oil(MiFID-II Ref Data)'},
                            {'name': 'COAL', 'description': 'Coal(MiFID-II Ref Data)'},
                            {'name': 'INRG', 'description': 'Inter Energy(MiFID-II Ref Data)'},
                            {'name': 'RNNG', 'description': 'Renewable energy(MiFID-II Ref Data)'},
                            {'name': 'LGHT', 'description': 'Light ends(MiFID-II Ref Data)'},
                            {'name': 'DIST', 'description': 'Distillates(MiFID-II Ref Data)'}, ],
'ENVR':                     [{'name': 'EMIS', 'description': 'Emissions(MiFID-II Ref Data)'},
                            {'name': 'WTHR', 'description': 'Weather(MiFID-II Ref Data)'},
                            {'name': 'CRBR', 'description': 'Carbon related(MiFID-II Ref Data)'}, ],
'FRGT':                     [{'name': 'WETF', 'description': 'Wet(MiFID-II Ref Data)'},
                            {'name': 'DRYF', 'description': 'Dry(MiFID-II Ref Data)'}],
'FRTL':                     [{'name': 'AMMO', 'description': 'Ammonia(MiFID-II Ref Data)'},
                            {'name': 'DAPH', 'description': 'DAP(Diammonium Phosphate)(MiFID-II Ref Data)'},
                            {'name': 'PTSH', 'description': 'Potash(MiFID-II Ref Data)'},
                            {'name': 'SLPH', 'description': 'Sulphur(MiFID-II Ref Data)'},
                            {'name': 'UREA', 'description': 'Urea(MiFID-II Ref Data)'},
                            {'name': 'UAAN', 'description': 'UAN(urea and ammonium nitrate)(MiFID-II Ref Data)'}, ],
'INDP':                     [{'name': 'CSTR', 'description': 'Construction(MiFID-II Ref Data)'},
                            {'name': 'MFTG', 'description': 'Manufacturing(MiFID-II Ref Data)'}, ],
'METL':                     [{'name': 'NPRM', 'description': 'Non Precious(MiFID-II Ref Data)'},
                            {'name': 'PRME', 'description': 'Precious(MiFID-II Ref Data)'}, ],
'PAPR':                     [{'name': 'CBRD', 'description': 'Containerboard(MiFID-II Ref Data)'},
                            {'name': 'NSPT', 'description': 'Newsprint(MiFID-II Ref Data)'},
                            {'name': 'PULP', 'description': 'Pulp(MiFID-II Ref Data)'},
                            {'name': 'RCVP', 'description': 'Recovered paper(MiFID-II Ref Data)'}, ],
'POLY':                     [{'name': 'PLST', 'description': 'Plastic(MiFID-II Ref Data)'}],
'GROS':                     [{'name': 'FWHT', 'description': 'Feed Wheat(MiFID-II Ref Data)'},
                            {'name': 'SOYB', 'description': 'Soybeans(MiFID-II Ref Data)'},
                            {'name': 'CORN', 'description': 'Corn(MiFID-II Ref Data)'},
                            {'name': 'RPSD', 'description': 'Rapeseed(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'},
                            {'name': 'RICE', 'description': 'Rice(MiFID-II Ref Data)'}, ],
'SOFT':                     [{'name': 'CCOA', 'description': 'Cocoa(MiFID-II Ref Data)'},
                            {'name': 'ROBU', 'description': 'Robusta Coffee(MiFID-II Ref Data)'},
                            {'name': 'WHSG', 'description': 'White Sugar(MiFID-II Ref Data)'},
                            {'name': 'BRWN', 'description': 'Brown Sugar(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'}, ],
'OOLI':                     [{'name': 'LAMP', 'description': 'Lampante(MiFID-II Ref Data)'}],
'GRIN':                     [{'name': 'MWHT', 'description': 'Milling Wheat(MiFID-II Ref Data)'}],
'ELEC':                     [{'name': 'BSLD', 'description': 'Base load(MiFID-II Ref Data)'},
                            {'name': 'FITR', 'description': 'Financial Transmission Rights(MiFID-II Ref Data)'},
                            {'name': 'PKLD', 'description': 'Peak load(MiFID-II Ref Data)'},
                            {'name': 'OFFP', 'description': 'Off-peak(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'}, ],
'NGAS':                     [{'name': 'GASP', 'description': 'GASPOOL(MiFID-II Ref Data)'},
                            {'name': 'LNGG', 'description': 'LNG(MiFID-II Ref Data)'},
                            {'name': 'NBPG', 'description': 'NBP(MiFID-II Ref Data)'},
                            {'name': 'NCGG', 'description': 'NCG(MiFID-II Ref Data)'},
                            {'name': 'TTFG', 'description': 'TTF(MiFID-II Ref Data)'}, ],
'OILP':                     [{'name': 'BAKK', 'description': 'Bakken(MiFID-II Ref Data)'},
                            {'name': 'BDSL', 'description': 'Biodiesel(MiFID-II Ref Data)'},
                            {'name': 'BRNT', 'description': 'Brent(MiFID-II Ref Data)'},
                            {'name': 'BRNX', 'description': 'Brent NX(MiFID-II Ref Data)'},
                            {'name': 'CNDA', 'description': 'Canadian(MiFID-II Ref Data)'},
                            {'name': 'COND', 'description': 'Condensate(MiFID-II Ref Data)'},
                            {'name': 'DSEL', 'description': 'Diesel(MiFID-II Ref Data)'},
                            {'name': 'DUBA', 'description': 'Dubai(MiFID-II Ref Data)'},
                            {'name': 'ESPO', 'description': 'ESPO(MiFID-II Ref Data)'},
                            {'name': 'ETHA', 'description': 'Ethanol(MiFID-II Ref Data)'},
                            {'name': 'FUEL', 'description': 'Fuel(MiFID-II Ref Data)'},
                            {'name': 'FOIL', 'description': 'Fuel Oil(MiFID-II Ref Data)'},
                            {'name': 'GOIL', 'description': 'Gasoil(MiFID-II Ref Data)'},
                            {'name': 'GSLN', 'description': 'Gasoline(MiFID-II Ref Data)'},
                            {'name': 'HEAT', 'description': 'Heating Oil(MiFID-II Ref Data)'},
                            {'name': 'JTFL', 'description': 'Jet Fuel(MiFID-II Ref Data)'},
                            {'name': 'KERO', 'description': 'Kerosene(MiFID-II Ref Data)'},
                            {'name': 'LLSO', 'description': 'Light Louisiana Sweet(LLS)(MiFID-II Ref Data)'},
                            {'name': 'MARS', 'description': 'Mars(MiFID-II Ref Data)'},
                            {'name': 'NAPH', 'description': 'Naptha(MiFID-II Ref Data)'},
                            {'name': 'NGLO', 'description': 'NGL(MiFID-II Ref Data)'},
                            {'name': 'TAPI', 'description': 'Tapis(MiFID-II Ref Data)'},
                            {'name': 'URAL', 'description': 'Urals(MiFID-II Ref Data)'},
                            {'name': 'WTIO', 'description': 'WTI(MiFID-II Ref Data)'}, ],
'EMIS':                     [{'name': 'CERE', 'description': 'CER(MiFID-II Ref Data)'},
                            {'name': 'ERUE', 'description': 'ERU(MiFID-II Ref Data)'},
                            {'name': 'EUAE', 'description': 'EUA(MiFID-II Ref Data)'},
                            {'name': 'EUAA', 'description': 'EUAA(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'}, ],
'WETF':                     [{'name': 'TNKR', 'description': 'Tankers(MiFID-II Ref Data)'}, ],
'DRYF':                     [{'name': 'DBCR', 'description': 'Dry bulk carriers(MiFID-II Ref Data)'}, ],
'NPRM':                     [{'name': 'ALUM', 'description': 'Aluminium(MiFID-II Ref Data)'},
                            {'name': 'ALUA', 'description': 'Aluminium Alloy(MiFID-II Ref Data)'},
                            {'name': 'CBLT', 'description': 'Cobalt(MiFID-II Ref Data)'},
                            {'name': 'COPR', 'description': 'Copper(MiFID-II Ref Data)'},
                            {'name': 'IRON', 'description': 'Iron ore(MiFID-II Ref Data)'},
                            {'name': 'LEAD', 'description': 'Lead(MiFID-II Ref Data)'},
                            {'name': 'MOLY', 'description': 'Molybdenum(MiFID-II Ref Data)'},
                            {'name': 'NASC', 'description': 'NASAAC(MiFID-II Ref Data)'},
                            {'name': 'NICK', 'description': 'Nickel(MiFID-II Ref Data)'},
                            {'name': 'STEL', 'description': 'Steel(MiFID-II Ref Data)'},
                            {'name': 'TINN', 'description': 'Tin(MiFID-II Ref Data)'},
                            {'name': 'ZINC', 'description': 'Zinc(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'}, ],
'PRME':                     [{'name': 'GOLD', 'description': 'Gold(MiFID-II Ref Data)'},
                            {'name': 'SLVR', 'description': 'Silver(MiFID-II Ref Data)'},
                            {'name': 'PTNM', 'description': 'Platinum(MiFID-II Ref Data)'},
                            {'name': 'PLDM', 'description': 'Palladium(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'}, ],
'TransactionType':          [{'name': 'FUTR', 'description': 'Futures(MiFID-II Ref Data)'},
                            {'name': 'OPTN', 'description': 'Options(MiFID-II Ref Data)'},
                            {'name': 'TAPO', 'description': 'TAPOS(MiFID-II Ref Data)'},
                            {'name': 'SWAP', 'description': 'SWAPS(MiFID-II Ref Data)'},
                            {'name': 'MINI', 'description': 'Minis(MiFID-II Ref Data)'},
                            {'name': 'OTCT', 'description': 'OTC(MiFID-II Ref Data)'},
                            {'name': 'ORIT', 'description': 'Outright(MiFID-II Ref Data)'},
                            {'name': 'CRCK', 'description': 'Crack(MiFID-II Ref Data)'},
                            {'name': 'DIFF', 'description': 'Differential(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'}, ],
'FinalPriceType':           [{'name': 'ARGM', 'description': 'Argus/McCloskey(MiFID-II Ref Data)'},
                            {'name': 'BLTC', 'description': 'Baltic(MiFID-II Ref Data)'},
                            {'name': 'EXOF', 'description': 'Exchange(MiFID-II Ref Data)'},
                            {'name': 'GBCL', 'description': 'GlobalCOAL(MiFID-II Ref Data)'},
                            {'name': 'IHSM', 'description': 'IHS McCloskey(MiFID-II Ref Data)'},
                            {'name': 'PLAT', 'description': 'Platts(MiFID-II Ref Data)'},
                            {'name': 'OTHR', 'description': 'Other(MiFID-II Ref Data)'}, ],
'FinancialCategory':        [{'name': 'FC', 'description': 'Financial Cpty(MiFID-II Ref Data)'},
                            {'name': 'NFC', 'description': 'NonFinancial Cpty(MiFID-II Ref Data)'},
                            {'name': 'NFC+', 'description': 'NFC exceeding clearing threshold(MiFID-II Ref Data)'},
                            {'name': 'NFC-',
                               'description': 'NFC not exceeding clearing threshold(MiFID-II Ref Data)'}, ],
'ESMAIndex':                [{'name': 'EONA', 'description': 'EONIA(MiFID-II Ref Data)'},
                            {'name': 'EONS', 'description': 'EONIA SWAP(MiFID-II Ref Data)'},
                            {'name': 'EURI', 'description': 'EURIBOR(MiFID-II Ref Data)'},
                            {'name': 'EUUS', 'description': 'EURODOLLAR(MiFID-II Ref Data)'},
                            {'name': 'EUCH', 'description': 'EuroSwiss(MiFID-II Ref Data)'},
                            {'name': 'GCFR', 'description': 'GCF REPO(MiFID-II Ref Data)'},
                            {'name': 'ISDA', 'description': 'ISDAFIX(MiFID-II Ref Data)'},
                            {'name': 'LIBI', 'description': 'LIBID(MiFID-II Ref Data)'},
                            {'name': 'LIBO', 'description': 'LIBOR(MiFID-II Ref Data)'},
                            {'name': 'MAAA', 'description': 'Muni AAA(MiFID-II Ref Data)'},
                            {'name': 'PFAN', 'description': 'Pfandbriefe(MiFID-II Ref Data)'},
                            {'name': 'TIBO', 'description': 'TIBOR(MiFID-II Ref Data)'},
                            {'name': 'STBO', 'description': 'STIBOR(MiFID-II Ref Data)'},
                            {'name': 'BBSW', 'description': 'BBSW(MiFID-II Ref Data)'},
                            {'name': 'JIBA', 'description': 'JIBAR(MiFID-II Ref Data)'},
                            {'name': 'BUBO', 'description': 'BUBOR(MiFID-II Ref Data)'},
                            {'name': 'CDOR', 'description': 'CDOR(MiFID-II Ref Data)'},
                            {'name': 'CIBO', 'description': 'CIBOR(MiFID-II Ref Data)'},
                            {'name': 'MOSP', 'description': 'MOSPRIM(MiFID-II Ref Data)'},
                            {'name': 'NIBO', 'description': 'NIBOR(MiFID-II Ref Data)'},
                            {'name': 'PRBO', 'description': 'PRIBOR(MiFID-II Ref Data)'},
                            {'name': 'TLBO', 'description': 'TELBOR(MiFID-II Ref Data)'},
                            {'name': 'WIBO', 'description': 'WIBOR(MiFID-II Ref Data)'},
                            {'name': 'TREA', 'description': 'Treasury(MiFID-II Ref Data)'},
                            {'name': 'SWAP', 'description': 'SWAP(MiFID-II Ref Data)'},
                            {'name': 'FUSW', 'description': 'Future SWAP(MiFID-II Ref Data)'}, ],
'MiFIDCategory':            [{'name': 'Professional', 'description': 'expert clients with experience & knowledge'},
                            {'name': 'Retail', 'description': 'clients with most regulatory protection'},
                            {'name': 'Eligible', 'description': 'institutions/investors/capital market participants'},
                            ],
'DoubleVolumeCapStatus':    [{'name' : 'Exceeded', 'description' : 'value exceeding the relevant threshold'},
                             {'name' : 'Near', 'description' : 'value near the relevant threshold'},
                             {'name' : 'Normal', 'description' : 'value within the relevant threshold'}
                            ],
'DarkCapStatus':            [{'name' : 'Exceeded', 'description' : 'value exceeding the relevant threshold'},
                             {'name' : 'Near', 'description' : 'value near the relevant threshold'},
                             {'name' : 'Normal', 'description' : 'value within the relevant threshold'}
                            ],
'ShortSellIndicator':       [{'name' : 'Sell Short', 'description' : ''},
                             {'name' : 'Buy Cover', 'description' : ''},
                             {'name' : 'Sell Short Exempt', 'description' : ''},
                             {'name' : 'Sell Short Undi', 'description' : ''},
                             ]}
choicelist_description = {
'AGRI': 'Agricultural(MiFID-II Ref Data)',
'NRGY': 'Energy(MiFID-II Ref Data)',
'ENVR': 'Environmental(MiFID-II Ref Data)',
'FRGT': 'Freight(MiFID-II Ref Data)',
'FRTL': 'Fertilizer(MiFID-II Ref Data)',
'INDP': 'Industrial products(MiFID-II Ref Data)',
'METL': 'Metals(MiFID-II Ref Data)',
'PAPR': 'Paper(MiFID-II Ref Data)',
'POLY': 'Plastic(MiFID-II Ref Data)',
'GROS': 'Grains Oil Seeds(MiFID-II Ref Data)',
'SOFT': 'Softs(MiFID-II Ref Data)',
'OOLI': 'Olive oil(MiFID-II Ref Data)',
'GRIN': 'Grain(MiFID-II Ref Data)',
'ELEC': 'Electricity(MiFID-II Ref Data)',
'NGAS': 'Natural Gas(MiFID-II Ref Data)',
'OILP': 'Oil(MiFID-II Ref Data)',
'EMIS': 'Emissions(MiFID-II Ref Data)',
'WETF': 'Wet(MiFID-II Ref Data)',
'DRYF': 'Dry(MiFID-II Ref Data)',
'NPRM': 'Non Precious(MiFID-II Ref Data)',
'PRME': 'Precious(MiFID-II Ref Data)',
'OTCPostTradeIndicator': 'Transaction type ind(MiFID-II Ref Data)',
'TradingCapacity': 'TradingCapacity(MiFID-II Ref Data)',
'Waiver': 'Waiver Options(MiFID-II Ref Data)',
'CommodityBaseProduct': 'CommodityBaseProduct(MiFID-II Ref Data)',
'TransactionType': 'As per trading venue(MiFID-II Ref Data)',
'FinalPriceType': 'As per trading venue(MiFID-II Ref Data)',
'FinancialCategory': 'Cpty categorization into Financial Cpty',
'ESMAIndex': '4 char for Index(MiFID-II Ref Data)',
'MiFIDCategory': 'Client Categorisation under MiFID',
'DoubleVolumeCapStatus': 'Limit trdg amt for equity under waivers',
'DarkCapStatus' : 'DarkCapStatus(MiFID-II Ref Data)',
'ShortSellIndicator' : 'ShortSecurityTrdType(MiFID-II Ref Data)'
}
# cl_not_in_master_list = ['AGRI', 'GROS', 'SOFT', 'GRIN', 'NRGY', 'ELEC', 'NGAS', 'OILP', 'NRGY', 'ENVR', 'EMIS', 'FRGT', 'WETF', 'DRYF', 'FRTL', 'INDP', 'METL', 'NPRM', 'PRME', 'PAPR', 'POLY']


add_info_specs = [
{'FieldName': 'regComplexTrdCmptId',
 'Description': addInfoSpecsDescrOnTrade['regComplexTrdCmptId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regRepositoryId',
 'Description': addInfoSpecsDescrOnTrade['regRepositoryId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regOurTrader',
 'Description': addInfoSpecsDescrOnTrade['regOurTrader'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regExecutingEntity',
 'Description': addInfoSpecsDescrOnTrade['regExecutingEntity'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regVenue',
 'Description': addInfoSpecsDescrOnTrade['regVenue'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regReportingEntity',
 'Description': addInfoSpecsDescrOnTrade['regReportingEntity'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regComdtyDerivInd',
 'Description': addInfoSpecsDescrOnTrade['regComdtyDerivInd'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Trade'},
{'FieldName': 'regSecFinTransInd',
 'Description': addInfoSpecsDescrOnTrade['regSecFinTransInd'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Trade'},
{'FieldName': 'regExchangeId',
 'Description': addInfoSpecsDescrOnTrade['regExchangeId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regAlgoId',
 'Description': addInfoSpecsDescrOnTrade['regAlgoId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'is_tdr',
 'Description': addInfoSpecsDescrOnTrade['is_tdr'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Party'},
{'FieldName': 'regTransactionType',
 'Description': addInfoSpecsDescrOnInstrument['regTransactionType'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Instrument',
 'Values': choicelistVal['TransactionType']},
{'FieldName': 'regFinalPriceType',
 'Description': addInfoSpecsDescrOnInstrument['regFinalPriceType'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Instrument',
 'Values': choicelistVal['FinalPriceType'],},
{'FieldName': 'ESMAIndex',
 'Description': addInfoSpecsDescrOnInstrument['ESMAIndex'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Instrument',
 'Values': choicelistVal['ESMAIndex'],},
{'FieldName': 'regMifidCategory',
 'Description': addInfoSpecsDescrOnParty['regMifidCategory'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Party',
 'Values': choicelistVal['MiFIDCategory'],},
{'FieldName': 'regHasTrdObligation',
 'Description': addInfoSpecsDescrOnInstrument['regHasTrdObligation'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Instrument'},
{'FieldName': 'regIsInvestmentFirm',
 'Description': addInfoSpecsDescrOnParty['regIsInvestmentFirm'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Party'},
{'FieldName': 'regPossibleReporter',
 'Description': addInfoSpecsDescrOnParty['regPossibleReporter'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Party'},
{'FieldName': 'regFinancialCategor',
 'Description': addInfoSpecsDescrOnParty['regFinancialCategor'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Party',
 'Values': choicelistVal['FinancialCategory']},
{'FieldName': 'dateOfBirth',
 'Description': addInfoSpecsDescrOnContact['dateOfBirth'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Date',
 'Table': 'Contact'},
{'FieldName': 'firstName',
 'Description': addInfoSpecsDescrOnContact['firstName'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Contact'},
{'FieldName': 'lastName',
 'Description': addInfoSpecsDescrOnContact['lastName'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Contact'},
{'FieldName': 'nationalId',
 'Description': addInfoSpecsDescrOnContact['nationalId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Contact'},
{'FieldName': 'regContactCrmId',
 'Description': addInfoSpecsDescrOnContact['regContactCrmId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Contact'},
{'FieldName': 'regInvesDecidrCrmId',
 'Description': addInfoSpecsDescrOnTrade['regInvesDecidrCrmId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regPtyCrmId',
 'Description': addInfoSpecsDescrOnParty['regPtyCrmId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Party'},
{'FieldName': 'regSMS',
 'Description': addInfoSpecsDescrOnInstrument['regSMS'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Double',
 'Table': 'Instrument'},
{'FieldName': 'regTrdAdmisAppTime',
 'Description': addInfoSpecsDescrOnInstrument['regTrdAdmisAppTime'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Time',
 'Table': 'Instrument'},
{'FieldName': 'regTrdAdmisReqTime',
 'Description': addInfoSpecsDescrOnInstrument['regTrdAdmisReqTime'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Time',
 'Table': 'Instrument'},
{'FieldName': 'regFirstTradeTime',
 'Description': addInfoSpecsDescrOnInstrument['regFirstTradeTime'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Time',
 'Table': 'Instrument'},
{'FieldName': 'regTrdTerminateDate',
 'Description': addInfoSpecsDescrOnInstrument['regTrdTerminateDate'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Date',
 'Table': 'Instrument'},
{'FieldName': 'regProvideLiquidity',
 'Description': addInfoSpecsDescrOnTrade['regProvideLiquidity'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Trade'},
{'FieldName': 'regToTV',
 'Description': addInfoSpecsDescrOnInstrument['regToTV'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Instrument'},
{'FieldName': 'regSimilarIsin',
 'Description': addInfoSpecsDescrOnInstrument['regSimilarIsin'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Instrument'},
{'FieldName': 'regIsAlgorithm',
 'Description': addInfoSpecsDescrOnParty['regIsAlgorithm'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Party'},
{'FieldName': 'regPtyExchangeId',
 'Description': addInfoSpecsDescrOnParty['regPtyExchangeId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Integer',
 'Table': 'Party'},
{'FieldName': 'regLiquidityBand',
 'Description': addInfoSpecsDescrOnInstrument['regLiquidityBand'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Integer',
 'Table': 'Instrument'},
{'FieldName': 'regLegIsin',
 'Description': addInfoSpecsDescrOnTrade['regLegIsin'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regNearLegIsin',
 'Description': addInfoSpecsDescrOnTrade['regNearLegIsin'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regFarLegIsin',
 'Description': addInfoSpecsDescrOnTrade['regFarLegIsin'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regInsCfiCode',
 'Description': addInfoSpecsDescrOnTrade['regInsCfiCode'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regInsIsin',
 'Description': addInfoSpecsDescrOnTrade['regInsIsin'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regContExchangeId',
 'Description': addInfoSpecsDescrOnContact['regContExchangeId'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Integer',
 'Table': 'Contact'},
{'FieldName': 'regGeneralPartner',
 'Description': addInfoSpecsDescrOnContact['regGeneralPartner'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Contact'},
{'FieldName': 'regTransmOfOrder',
 'Description': addInfoSpecsDescrOnTrade['regTransmOfOrder'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Trade'},
{'FieldName': 'regPrimaryMktMic',
 'Description': addInfoSpecsDescrOnInstrument['regPrimaryMktMic'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Instrument'},
{'FieldName': 'regMaterialMktMic',
 'Description': addInfoSpecsDescrOnInstrument['regMaterialMktMic'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Instrument'},
{'FieldName': 'regDarkCapStatus',
 'Description': 'DarkCapStatus',
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Instrument',
 'Values': choicelistVal['DarkCapStatus']},
{'FieldName': 'regDarkCapMic',
 'Description': addInfoSpecsDescrOnInstrument['regDarkCapMic'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Instrument'},
{'FieldName': 'regTickSize',
 'Description': addInfoSpecsDescrOnInstrument['regTickSize'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Double',
 'Table': 'Instrument'},
{'FieldName': 'regDblVolCapStatus',
 'Description': 'DoubleVolumeCapStatus',
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Instrument',
 'Values': choicelistVal['DoubleVolumeCapStatus']},
{'FieldName': 'regMiFIDTransparent',
 'Description': addInfoSpecsDescrOnInstrument['regMiFIDTransparent'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Instrument'},
{'FieldName': 'regFISN',
 'Description': addInfoSpecsDescrOnInstrument['regFISN'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Instrument', },
{'FieldName': 'regPostLargeInScale',
 'Description': addInfoSpecsDescrOnInstrument['regPostLargeInScale'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Double',
 'Table': 'Instrument'},
{'FieldName': 'regPostSSTI',
 'Description': addInfoSpecsDescrOnInstrument['regPostSSTI'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Double',
 'Table': 'Instrument'},
]
add_info_specs_version_16_4 = [
{'FieldName': 'regMicroSeconds',
 'Description': 'regMicroSeconds',
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Integer',
 'Table': 'Trade'},
{'FieldName': 'regClearingHouse',
 'Description': 'regClearingHouse',
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regClearingIsMandat',
 'Description': addInfoSpecsDescrOnInstrument['regClearingIsMandat'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Instrument'},
{'FieldName': 'regCFICode',
 'Description': addInfoSpecsDescrOnInstrument['regCFICode'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Instrument'},]

add_info_specs_version_16_5 = [
{'FieldName': 'regClearingBroker',
 'Description': addInfoSpecsDescrOnTrade['regClearingBroker'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regMiddleware',
 'Description': addInfoSpecsDescrOnTrade['regMiddleware'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regOriginalCpty',
 'Description': addInfoSpecsDescrOnTrade['regOriginalCpty'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regRepository',
 'Description': addInfoSpecsDescrOnTrade['regRepository'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regIsHedge',
 'Description': 'indicates whether the transaction reduces risk in an objectively measurable way',
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Trade'},
{'FieldName': 'regLargeInScale',
 'Description': addInfoSpecsDescrOnInstrument['regLargeInScale'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Double',
 'Table': 'Instrument'},
{'FieldName': 'regSSTI',
 'Description': addInfoSpecsDescrOnInstrument['regSSTI'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Double',
 'Table': 'Instrument'},
{'FieldName': 'regDiscreteTrader',
 'Description': addInfoSpecsDescrOnUser['regDiscreteTrader'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'User'},
]

add_info_specs_version_17_1 = [
{'FieldName': 'regTradingCapacity',
 'Description': 'TradingCapacity',
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Trade',
 'Values': choicelistVal['TradingCapacity']},
{'FieldName': 'regWaiver',
 'Description': addInfoSpecsDescrOnTrade['regWaiver'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Integer',
 'Table': 'Trade',},
{'FieldName': 'regOTCPostTradeInd',
 'Description': addInfoSpecsDescrOnTrade['regOTCPostTradeInd'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Integer',
 'Table': 'Trade',},
{'FieldName': 'regOurOrg',
 'Description': addInfoSpecsDescrOnTrade['regOurOrg'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regOurTransmitOrg',
 'Description': addInfoSpecsDescrOnTrade['regOurTransmitOrg'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regOurInvesDecider',
 'Description': addInfoSpecsDescrOnTrade['regOurInvesDecider'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regBranchMemberShip',
 'Description': addInfoSpecsDescrOnTrade['regBranchMemberShip'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regTheirOrg',
 'Description': addInfoSpecsDescrOnTrade['regTheirOrg'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'Party',
 'Table': 'Trade'},
{'FieldName': 'regTheirInvDecider',
 'Description': addInfoSpecsDescrOnTrade['regTheirInvDecider'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regTheirTrader',
 'Description': addInfoSpecsDescrOnTrade['regTheirTrader'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Trade'},
{'FieldName': 'regDirectedOrder',
 'Description': addInfoSpecsDescrOnTrade['regDirectedOrder'],
 'Default': 'False',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Trade'},
{'FieldName': 'regClearingTime',
 'Description': addInfoSpecsDescrOnTrade['regClearingTime'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Time',
 'Table': 'Trade'},
{'FieldName': 'regConfirmationTime',
 'Description': addInfoSpecsDescrOnTrade['regConfirmationTime'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Time',
 'Table': 'Trade'},
{'FieldName': 'regIsLiquid',
 'Description': addInfoSpecsDescrOnInstrument['regIsLiquid'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Instrument'},
{'FieldName': 'regIsSysInternalizr',
 'Description': addInfoSpecsDescrOnInstrument['regIsSysInternalizr'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Instrument'},
{'FieldName': 'regCmdty',
 'Description': addInfoSpecsDescrOnInstrument['regCmdty'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Integer',
 'Table': 'Instrument'},

]

add_info_specs_version_17_2 = [
{'FieldName': 'regShortSell',
 'Description': addInfoSpecsDescrOnTrade['regShortSell'],
 'Default': '',
 'TypeGroup': 'RecordRef',
 'Type': 'ChoiceList',
 'Table': 'Trade'},
{'FieldName': 'uniqueName',
 'Description': addInfoSpecsDescrOnContact['uniqueName'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'String',
 'Table': 'Contact'},
{'FieldName': 'regRptDeferToTime',
 'Description': addInfoSpecsDescrOnTrade['regRptDeferToTime'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Time',
 'Table': 'Trade'},
{'FieldName': 'regAvgDailyTO',
 'Description': addInfoSpecsDescrOnInstrument['regAvgDailyTO'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Double',
 'Table': 'Instrument'},
]

add_info_specs_version_17_4 = [{'FieldName': 'regIsVenue',
 'Description': addInfoSpecsDescrOnParty['regIsVenue'],
 'Default': '',
 'TypeGroup': 'Standard',
 'Type': 'Boolean',
 'Table': 'Party'},
]
 
add_info_spec_filter = {
'regCmdty': ['Average Future/Forward', 'Combination', \
             'Commodity', 'Commodity Index', 'Commodity Variant', \
             'Future/Forward', 'Precious Metal Rate', 'PriceSwap', \
             'Option', 'Rolling Schedule'],
'regFinalPriceType': ['Average Future/Forward', 'Combination', \
                      'Commodity', 'Commodity Index', 'Commodity Variant', \
                      'Future/Forward', 'Precious Metal Rate', 'PriceSwap', \
                      'Option', 'Rolling Schedule'],
'regIsHedge': ['Average Future/Forward', 'Combination', \
               'Commodity', 'Commodity Index', 'Commodity Variant', \
               'Future/Forward', 'Precious Metal Rate', 'PriceSwap', \
               'Option', 'Rolling Schedule'],
'regInsSimilarIsin': ['Curr'],
'regInsCfiCode': ['Curr'],
'regInsIsin': ['Curr'],
'regShortSell' : ['Stock', 'Zero', 'PromisLoan', 'MBS/ABS', \
                  'IndexLinkedBond', 'FRN', 'Flexi Bond', 'DualCurrBond', \
                  'Convertible', 'Commodity', 'CLN', 'Bond', 'Bill']
}




def move_alias_to_add_info():
    aliases = acm.FInstrumentAlias.Select("type = 'FISN'")
    for alias in list(aliases):
        ins = alias.Instrument()
        try:
            if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5:
                reg = ins.RegulatoryInfo()
                reg.AdditionalInfo().RegFISN(alias.Alias())
            else:
                ins.AdditionalInfo().RegFISN(alias.Alias())
            alias.Delete()   
        except Exception, e:
            print "Error while copying FISN alias <%s> for instrument <%s>. Error : <%s>"%(alias.Alias(), ins.Name(), str(e))
    
    aliases = acm.FInstrumentAlias.Select("type = 'FISN'")
    if not aliases:#it means all the aliases have been migrated
        try:
            alias_typ = acm.FInstrAliasType['FISN']
            if alias_typ:
                alias_typ.Delete()
        except Exception, e:
            print "Error while deleting the Instrumetn alias FISN. Error: <%s>"%str(e)

def get_table_for_add_info_spec(add_info_spec):
    if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() >= 2016.5 and add_info_spec['Table'] in ['Trade',
                                                                                                      'Instrument']:
        if add_info_spec['Table'] == 'Trade' and add_info_spec['FieldName'] != 'regShortSell':
            add_info_spec['Table'] = 'TradeRegulatoryInfo'
        if add_info_spec['Table'] == 'Instrument' and add_info_spec['FieldName'] != 'ESMAIndex':
            add_info_spec['Table'] = 'InstrRegulatoryInfo'
    return add_info_spec


integrationUtils = FIntegrationUtils.FIntegrationUtils()

def rename_add_info_spec():
    """rename the AddInfoSpecs that are used for support Regulatory information"""
    rename_add_info_specs = {   'miFIDCategory': 'regMifidCategory',
                                'cRMid': 'regContactCrmId',
                                'regCrmId': 'regPtyCrmId',
                                'regExchgId': 'regPtyExchangeId',
                                'exchangeId': 'regContExchangeId',
                                'regIsTrdgObligation': 'regHasTrdObligation',
                                'regAggressPassive' : 'regProvideLiquidity',
                                'regTrdTerminateTime' : 'regTrdTerminateDate'
                                }
    change_data_type = {'regTrdTerminateDate': 'Date',}
    for rename_add_info_spec in rename_add_info_specs:
        existing_addinfo = rename_add_info_spec
        new_addinfo = rename_add_info_specs[rename_add_info_spec]
        add_info = acm.FAdditionalInfoSpec[existing_addinfo]
        if add_info:
            try:
                date_type_changed = False
                add_info.Name(new_addinfo)
                if new_addinfo in change_data_type.keys() and \
                    add_info.DataTypeType() != integrationUtils.get_data_type_type(change_data_type[new_addinfo]):
                    add_info.DataTypeType(integrationUtils.get_data_type_type(change_data_type[new_addinfo]))
                    date_type_changed = True
                add_info.Commit()
                if date_type_changed:
                    ais = acm.FAdditionalInfoSpec['regTrdTerminateDate']
                    rec_type = None
                    rec_ids = []
                    aiSels = acm.FAdditionalInfo.Select("addInf = %d"%ais.Oid())
                    rec_type = aiSels[0].RecType()
                    for aiSel in aiSels:
                        rec_ids.append(aiSel.Recaddr())
                    for rec_id in rec_ids:
                        obj = None
                        if rec_type == 'InstrRegulatoryInfo':
                            obj = acm.FInstrumentRegulatoryInfo[rec_id]
                        elif rec_type == 'Instrument':
                            obj = acm.FInstrument[rec_id]
                        obj.AdditionalInfo().RegTrdTerminateDate(obj.AdditionalInfo().RegTrdTerminateDate())
                        obj.Commit()
                        print "Changing on <%s> with Oid <%d>"%(rec_type, rec_id)
            except:
                pass

def rename_choice_lists():
    """rename the choicelists that are used to support Regulatory information"""
    rename_choice_lists = {'MHWT': 'MWHT',}
    for rename_choice_list in rename_choice_lists:
        existing_choice_list = rename_choice_list
        new_choice_list = rename_choice_lists[existing_choice_list]
        choice_list = acm.FChoiceList[existing_choice_list]
        if choice_list:
            try:
                choice_list.Name(new_choice_list)
                choice_list.Commit()
            except:
                pass
def remove_add_info_specs():
    """remove the AddInfoSpecs that are no longer used to support Regulatory information"""
    remove_add_info_specs = ['regInsSimilarIsin', 'regJointAccount']
    for add_info_spec in remove_add_info_specs:
        try:
            integrationUtils.delete_add_info_spec(add_info_spec)
            print "Successfully deleted AddInfoSpec <%s>"%add_info_spec
        except Exception, e:
            if 'does not exist in database' not in str(e):
                print e

def remove_choice_lists():
    """remove obsolete choicelist entries"""
    remove_obsolete_choice_entries_otc_post_trade_ind = ['LGRS', 'NPFT', 'RFPT', 'NLIQ', 'OILQ', 'PRIC', 'ALGO']
    for each_choicelist in remove_obsolete_choice_entries_otc_post_trade_ind:
        try:
            integrationUtils.remove_choicelist_entry([each_choicelist], ['OTCPostTradeIndicator'])
        except Exception, e:
            if "does not exist in" not in str(e):
                print str(e)

    remove_obsolete_choice_entries_waiver = ['LRGS']
    for each_choicelist in remove_obsolete_choice_entries_waiver:
        try:
            integrationUtils.remove_choicelist_entry([each_choicelist], ['Waiver'])
        except Exception, e:
            if "does not exist in" not in str(e):
                print str(e)
    try:
        integrationUtils.delete_choice_list('CommodityFurtherSubProduct')
    except Exception, e:
        print e
    try:
        integrationUtils.delete_choice_list('CommoditySubProduct')
    except Exception, e:
        print e

def create_add_info_specs():
    """create the AddInfoSpecs that are required for supporting Regulatory information"""
    for add_info_spec in add_info_specs:
        filter_val = None
        if add_info_spec_filter.has_key(add_info_spec['FieldName']):
            filter_val = add_info_spec_filter[add_info_spec['FieldName']]
    
        try:
            add_info_spec = get_table_for_add_info_spec(add_info_spec)
            integrationUtils.set_additional_info_spec(add_info_spec, filter_val)
        except Exception, e:
            print e
    version_specdict = {2016.4: add_info_specs_version_16_4,
                        2016.5: add_info_specs_version_16_5,
                        2017.1: add_info_specs_version_17_1,
                        2017.2: add_info_specs_version_17_2,
                        2017.4: add_info_specs_version_17_4,}
    for version in version_specdict:
        if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() < version:
            for add_info_spec in version_specdict[version]:
                filter_val = None
                if add_info_spec_filter.has_key(add_info_spec['FieldName']):
                    filter_val = add_info_spec_filter[add_info_spec['FieldName']]
                try:
                    add_info_spec = get_table_for_add_info_spec(add_info_spec)
                    integrationUtils.set_additional_info_spec(add_info_spec, filter_val)
                except Exception, e:
                    print e
def create_choice_list():
    """create the choicelists that are required for supporting Regulatory information"""
    for choise_list in choicelistVal:
        description = None
        if choicelist_description.has_key(choise_list):
            description = choicelist_description[choise_list]
        try:
            integrationUtils.create_choice_list(choise_list, choicelistVal[choise_list], description, True, True)
        except Exception, e:
            print e
def create_alias_types():
    """create alias types that are required for supporting Regulatory information"""
    try:
        integrationUtils.create_alias_type('Party', 'MIC Code on the Party', 'MIC', 'MIC')
    except Exception, e:
        print e

def upgrade_for_changes():
    remove_choice_lists()
    rename_choice_lists()
    remove_add_info_specs()
    rename_add_info_spec()
    move_alias_to_add_info()

def upgrade_for_additions():
    create_alias_types()
    create_choice_list()
    create_add_info_specs()
