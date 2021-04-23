""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/../SwiftIntegration/RegulatoryInfo/RegulatoryInfoLib/FRegulatoryCfiCodeGeneration.py"
"""------------------------------------------------------------------------
MODULE
    FRegulatoryCfiCodeGeneration -
DESCRIPTION:
    This file consists of the functions to generate the CfiCode for instruments that do not have CfiCode present on them
VERSION: %R%
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end
--------------------------------------------------------------------------"""
import acm
import ael
option_style_type_lookup = {
    'European-Call': 'A',
    'American-Call': 'B',
    'Bermudan-Call': 'C',
    'European-Put': 'D',
    'American-Put': 'E',
    'Bermudan-Put': 'F',
}
exotic_lookup = {
    'Digital European Vanilla': 'D',
    'Vanilla': 'V',
    'Asian': 'A',
    'Barrier': 'B',
    'Digital European Barrier': 'G',
    'Digital American': 'D',
    'KIKO': 'G',
    'Lookback': 'L',
    'Range Accrual': 'P',
    'Misc': 'M',
}
#COMMODITY SUB PRODUCT CLASSIFICATION NOT IN REGSUPPORT: 'CSHP', 'DLVR', 'NDLV', 
seniority_lookup = {'SNRFOR' : 'N', 'SUBLT2' : 'Q', 'JRSUBUT2' : 'J'}
exercise_type_lookup = {'European' : 'E', 'American' : 'A', 'Amer GA' : 'A', 'Bermudan' : 'B'}
commodity_classification = {'A': ["AGRI", 'DIRY', 'FRST', 'LSTK', 'GROS',  'SEAF', 'GRIN', 'POTA', \
                                'OOLI', 'SOFT', 'MHWT', 'CORN', 'RICE', 'SOYB', 'RPSD', 'LAMP', 'CCOA',\
                                'ROBU', 'BRWN', 'WHSG', 'FWHT'],
                            'E': ["NRGY", 'COAL', 'DIST', 'INRG', 'LGHT', 'NGAS', 'OILP', 'BAKK', \
                                'BDSL', 'BRNT', 'BRNX', 'CNDA', 'COND', 'DSEL', 'DUBA', 'ESPO', \
                                'ETHA', 'FUEL', 'FOIL', 'GOIL', 'GSLN', 'HEAT', 'JTFL', 'KERO', \
                                'LLSO', 'MARS', 'NAPH', 'NGLO', 'TAPI', 'WTIO', 'URAL', 'ALUM', \
                                'ALUA', 'CBLT', 'COPR', 'IRON', 'LEAD', 'MOLY', 'NASC', 'NICK', \
                                'STEL', 'TINN', 'ZINC', 'GASP', 'LNGG', 'NBPG', 'NCGG', 'TTFG', \
                                'NPRM', 'PRME', 'GOLD', 'PLDM', 'PTNM', 'SLVR', 'METL',],
                            'I': ["PAPR", 'CBRD', 'NSPT', 'PULP', 'RCVP', "INDP", 'CSTR', 'MFTG',],
                            'P': ["POLY", 'PLST',],
                            'H': ['ELEC', 'RNNG', 'BSLD', 'FITR', 'PKLD', 'OFFP',],
                            'N': ["ENVR",  'EMIS', 'CERE', 'ERUE', 'EUAE', 'EUAA', 'CRBR',  'WTHR',],
                            'M': ["FRTL", 'AMMO', 'DAPH', 'PTSH', 'SLPH', 'UREA', 'UAAN', 'INFL', 'MCEX', 'OEST', 'OTHR'],
                            'S': ["FRGT", 'DRYF', 'WETF', 'DBCR', 'TNKR']}

swap_classification = {
'Float-Float': 'A',
'Fixed-Floating': 'C',
'Fixed-Fixed': 'D',
'Inflation rate index': 'G',
'Overnight Index Swap': 'H',
'Zero coupon': 'Z',
}
'''#DONT KNOW WHY THIS ISNT USED - NEED TO CHECK
underlyer_classification = {
'Float-Float' : 'A',
'Fixed-Floating' : 'C',
'Fixed-Fixed' : 'D',
'Inflation rate index' : 'G',
'Overnight Index Swap' : 'H',
'Option' : 'O',
'Future/Forward' : 'R',
}
'''
commodity_classification_for_swaps = {
'A': ["AGRI", 'DIRY', 'FRST', 'LSTK', 'GROS',  'SEAF', 'GRIN', 'POTA', \
     'OOLI', 'SOFT', 'MHWT', 'CORN', 'RICE', 'SOYB', 'RPSD', 'LAMP', 'CCOA',\
     'ROBU', 'BRWN', 'WHSG', 'FWHT'],
'S': ["FRTL", 'AMMO', 'DAPH', 'PTSH', 'SLPH', 'UREA', 'UAAN',],
'G': ["FRGT", 'DRYF', 'WETF', 'DBCR', 'TNKR'],
'P': ["POLY", 'PLST',],
'T': ["PAPR", 'CBRD', 'NSPT', 'PULP', 'RCVP',],
'N': ["ENVR",  'EMIS', 'CERE', 'ERUE', 'EUAE', 'EUAA', 'CRBR',  'WTHR',],
'K': ['ALUM', 'ALUA', 'CBLT', 'COPR', 'IRON', 'LEAD', 'MOLY', 'NASC', 'NICK', \
     'STEL', 'TINN', 'ZINC', 'GASP', 'LNGG', 'NBPG', 'NCGG', 'TTFG', \
     'NPRM', 'PRME', 'GOLD', 'PLDM', 'PTNM', 'SLVR', 'METL',], 
'J': ["NRGY", 'COAL', 'DIST', 'INRG', 'LGHT', 'NGAS', 'OILP', 'BAKK', \
     'BDSL', 'BRNT', 'BRNX', 'CNDA', 'COND', 'DSEL', 'DUBA', 'ESPO', \
     'ETHA', 'FUEL', 'FOIL', 'GOIL', 'GSLN', 'HEAT', 'JTFL', 'KERO', \
     'LLSO', 'MARS', 'NAPH', 'NGLO', 'TAPI', 'WTIO', 'URAL',]}


def is_non_deliverable_swap(instrument):
    settlement_char = 'X'
    if instrument.NonDeliverable():
        settlement_char = 'C'
    else:
        settlement_char = 'P'
    return settlement_char

def is_underlyer_curr_different(instrument):
    ins_currency = instrument.Currency().Name()
    diff_currency = False
    if instrument.InsType() in ['Swap', 'IndexLinkedSwap', 'TotalReturnSwap', 'CreditDefaultSwap']:
        for leg in instrument.Legs():
            try:
                if (leg.InflationScalingRef() and leg.InflationScalingRef().Currency().Name() != ins_currency) or \
                    (leg.IndexRef() and leg.IndexRef().Currency().Name() != ins_currency) or \
                    (leg.FloatRateReference() and leg.FloatRateReference().Currency().Name() != ins_currency) or \
                    (leg.FloatRateReference2() and leg.FloatRateReference2().Currency().Name() != ins_currency) or \
                    (leg.CreditRef() and leg.CreditRef().Currency().Name() != ins_currency):
                    diff_currency = True
                    break
            except:
                if (leg.IndexRef() and leg.IndexRef().Currency().Name() != ins_currency) or \
                    (leg.FloatRateReference() and leg.FloatRateReference().Currency().Name() != ins_currency) or \
                    (leg.FloatRateReference2() and leg.FloatRateReference2().Currency().Name() != ins_currency) or \
                    (leg.CreditRef() and leg.CreditRef().Currency().Name() != ins_currency):
                    diff_currency = True
                    break    
    if instrument.InsType() in ['VolatilitySwap', 'VarianceSwap']:
        if instrument.Underlying() and instrument.Underlying().Currency().Name() != ins_currency:
            diff_currency = True
    if instrument.InsType() in ['CurrSwap']:
        curr1 = instrument.Legs()[0].Currency().Name()
        curr2 = instrument.Legs()[1].Currency().Name()
        if curr1 != curr2:
            diff_currency = True
    return diff_currency

def get_credit_category(instrument):
    category_char = 'C'
    ins = instrument
    if instrument and instrument.Underlying():
        ins = instrument.Underlying()
    if ins and ins.Issuer() and ins.Issuer().BusinessStatus():
        business_status = ins.Issuer().BusinessStatus().Name()
        if 'GOVERNMENT' in business_status.upper():
            category_char = 'S'
        elif 'MUNICIPAL' in business_status.upper():
            category_char = 'L'
        else:
            category_char = 'C'
    return category_char

def commodity_classify(instrument):
    cmdty_classify = None
    cmdty_swap_classify = 'M'
    cmdty_classify = get_commodity_details(instrument)
    if cmdty_classify:       
        for each_commodity_classify in commodity_classification_for_swaps:
            commodity_key = each_commodity_classify
            if cmdty_classify in commodity_classification_for_swaps[commodity_key]:
                cmdty_swap_classify = commodity_key
                break
    '''
    if instrument.RegulatoryInfo().CommodityProduct():
        if instrument.RegulatoryInfo().CommodityProduct().Name() == 'OTHR':
            if instrument.RegulatoryInfo().CommoditySubProduct().Name() == 'OTHR':
                cmdty_classify = instrument.RegulatoryInfo().CommodityBaseProduct().Name()
            else:
                cmdty_classify = instrument.RegulatoryInfo().CommoditySubProduct().Name()
        else:
            cmdty_classify = instrument.RegulatoryInfo().CommodityProduct().Name()
        for each_commodity_classify in commodity_classification_for_swaps:
            commodity_key = each_commodity_classify
            if cmdty_classify in commodity_classification_for_swaps[commodity_key]:
                cmdty_swap_classify = commodity_key
                break
    '''
    return cmdty_swap_classify

def get_commodity_classification_for_swaps(instrument):
    cmdty_swap_classify = None
    cmdty_swap_classify = 'M'
    if instrument.InsType() in ['PriceSwap']:
        for leg in instrument.Legs():
            if leg.FloatRateReference():
                float_rate_ref = leg.FloatRateReference()
                if float_rate_ref.RegulatoryInfo().CommodityBaseProduct() or \
                    float_rate_ref.RegulatoryInfo().CommoditySubProduct() or \
                    float_rate_ref.RegulatoryInfo().CommodityFurtherSubProduct():
                #if float_rate_ref.RegulatoryInfo().CommodityProduct():
                    cmdty_swap_classify = commodity_classify(float_rate_ref)
                    
                else:
                    if float_rate_ref.InsType() == 'Commodity Index':
                        cmdty_swap_classify = 'I'
                    elif float_rate_ref.InsType() == 'Commodity Variant':
                        cmdty_swap_classify = commodity_classify(float_rate_ref.Underlying())
                    elif float_rate_ref.InsType() == 'Combination' and get_combination_classification(float_rate_ref)[1]:
                        cmdty_swap_classify = 'Q'
    if instrument.InsType() in ['Future/Forward']:
        underlyer = instrument.Underlying()
        if underlyer.RegulatoryInfo().CommodityBaseProduct() or \
            underlyer.RegulatoryInfo().CommoditySubProduct() or \
            underlyer.RegulatoryInfo().CommodityFurtherSubProduct():
            cmdty_swap_classify = commodity_classify(underlyer)
        else:
            if underlyer.InsType() == 'Commodity Index':
                cmdty_swap_classify = 'I'
    return cmdty_swap_classify

def get_swap_classification(instrument):
    float_leg_count = 0
    fixed_leg_count = 0
    zc_fixed_leg_count = 0
    ois = False
    swap_classify = None
    swap_classify_char = 'M'
    if instrument.InsType() == 'IndexLinkedSwap':
        swap_classify = 'Inflation rate index'
    elif instrument.InsType() == 'TotalReturnSwap':
        leg_counter = 0
        for leg in instrument.Legs():
            leg_counter = leg_counter + 1
            if leg_counter > 2:
                break
            if leg.LegType() in ['Fixed', 'Fixed Accretive']:
                fixed_leg_count = fixed_leg_count + 1
            elif leg.LegType() in ['Zero Coupon Fixed']:
                zc_fixed_leg_count = zc_fixed_leg_count + 1
            elif leg.LegType() in ['Float', 'Total Return']:
                float_leg_count = float_leg_count + 1               
                if leg.FloatRateReference() and leg.FloatRateReference().Legs() and leg.FloatRateReference().Legs()[0].EndPeriod() == '1d':
                    ois = True
            elif leg.LegType() in ['Capped Float', 'Floored Float', 'Collared Float', \
                'Reverse Float', 'Target Redemption', 'Range Accrual', 'Snowball', \
                'Collared LPI', 'Floored LPI', 'Capped LPI']:
                pass
    else:
        for leg in instrument.Legs():
            if leg.LegType() in ['Fixed', 'Fixed Accretive']:
                fixed_leg_count = fixed_leg_count + 1
            elif leg.LegType() in ['Zero Coupon Fixed']:
                zc_fixed_leg_count = zc_fixed_leg_count + 1
            elif leg.LegType() in ['Float', 'Total Return']:
                float_leg_count = float_leg_count + 1
                if leg.FloatRateReference() and leg.FloatRateReference().Legs()[0].EndPeriod() == '1d':
                    ois = True
            elif leg.LegType() in ['Capped Float', 'Floored Float', 'Collared Float', \
                'Reverse Float', 'Target Redemption', 'Range Accrual', 'Snowball', \
                'Collared LPI', 'Floored LPI', 'Capped LPI']:
                pass
    if not swap_classify:
        if ois:
            swap_classify = 'Overnight Index Swap'
        elif float_leg_count == 2:
            swap_classify = 'Float-Float'
        elif fixed_leg_count == 2:
            swap_classify = 'Fixed-Fixed'
        elif float_leg_count == fixed_leg_count:
            swap_classify = 'Fixed-Floating'
        elif zc_fixed_leg_count > 0:
            swap_classify = 'Zero coupon'
    if swap_classify and swap_classification.has_key(swap_classify):
        swap_classify_char = swap_classification[swap_classify]
    if not swap_classify_char:
        swap_classify_char = 'M'
    return swap_classify_char

def get_commodity_details(instrument):
    cmdty_classify = None
    if instrument.RegulatoryInfo().CommodityBaseProduct():
        if instrument.RegulatoryInfo().CommodityFurtherSubProduct():
            if instrument.RegulatoryInfo().CommodityFurtherSubProduct().Name() == 'OTHR':
                if instrument.RegulatoryInfo().CommoditySubProduct().Name() == 'OTHR':
                    cmdty_classify = instrument.RegulatoryInfo().CommodityBaseProduct().Name()
                else:
                    cmdty_classify = instrument.RegulatoryInfo().CommoditySubProduct().Name()
            else:
                cmdty_classify = instrument.RegulatoryInfo().CommodityFurtherSubProduct().Name()
        elif instrument.RegulatoryInfo().CommoditySubProduct():
            if instrument.RegulatoryInfo().CommoditySubProduct().Name() == 'OTHR':
                cmdty_classify = instrument.RegulatoryInfo().CommodityBaseProduct().Name()
            else:
                cmdty_classify = instrument.RegulatoryInfo().CommoditySubProduct().Name()
        else:
            cmdty_classify = instrument.RegulatoryInfo().CommodityBaseProduct().Name()
    return cmdty_classify

def get_commodity_classification(instrument):
    commodity_classify_val = 'M'
    commodity_classify = get_commodity_details(instrument)
    if commodity_classify:
        for each_commodity_classify in commodity_classification:
            commodity_key = each_commodity_classify
            if commodity_classify in commodity_classification[commodity_key]:
                commodity_classify_val = commodity_key
                break
    return commodity_classify_val

def get_delivery_char(instrument):
    delivery_char = 'X'
    if instrument.SettlementType () == 'Physical Delivery':
        delivery_char = 'P'
    else:
        delivery_char = 'C'
    return delivery_char

def get_tenure(instrument):
    start_date = ael.date_from_string(instrument.StartDate())
    end_date = ael.date_from_string(instrument.EndDate())
    tenure = start_date.days_between(end_date)
    return tenure

def get_exercise_type_char(instrument):
    exercise_type_char = 'X'
    if exercise_type_lookup.has_key(instrument.ExerciseType()):
        exercise_type_char = exercise_type_lookup[instrument.ExerciseType()]
    return exercise_type_char

def get_option_callable_char(instrument):
    callable_char = 'X'
    if instrument.IsCallOption():
        callable_char = 'C'
    else:
        callable_char = 'P'
    return callable_char

def get_seniority_char(instrument):
    seniority_char = 'X'
    if instrument.Seniority() and seniority_lookup.has_key(instrument.Seniority().Name()):
        seniority_char = seniority_lookup[instrument.Seniority().Name()]
    return seniority_char

def get_instrument_type(instrument):
    return instrument.InsType()
        
def get_first_char_in_cfi_code(instrument, ins_type):
    first_char = 'X'
    if instrument.InsType() in ['Rolling Schedule', 'FRA', 'FXOptionDatedFwd']:
        first_char = 'J'
    elif instrument.InsType() in ['Certificate', 'Combination']:
        first_char = 'M'
    elif instrument.InsType() in ['Commodity Index', 'Dividend Point Index', 'Curr', 'EquityIndex', 'RateIndex', 'CreditIndex', 'PriceIndex']:
        first_char = 'T'
    elif instrument.InsType() in ['Stock', 'Depositary Receipt']:# and (not instrument.Otc()) :
        first_char = 'E'
    elif instrument.InsType() in ['ETF', 'Fund']:# and (not instrument.Otc()) :
        first_char = 'C'
    elif instrument.InsType() in ['Bond', 'Convertible', 'FRN', 'MBS/ABS', 'PromisLoan', 'Zero', \
        'Bill', 'DualCurrBond', 'CLN', 'IndexLinkedBond', 'CD', 'Deposit', 'Flexi Bond']:# and (not instrument.Otc()):
        first_char = 'D'
    elif instrument.InsType() in ['Warrant']:
        first_char = 'R'
    elif instrument.InsType() in ['Option']:
        if is_otc_option(instrument):
            first_char = 'H'
        else:
            first_char = 'O'
    elif instrument.InsType() in ['Future/Forward', 'Average Future/Forward', 'CFD']:
        if (not instrument.Otc()):
            first_char = 'F'
        else:
            first_char = 'J'
    elif instrument.InsType() in ['Swap', 'CurrSwap', 'TotalReturnSwap', 'VarianceSwap', 'CreditDefaultSwap', 'IndexLinkedSwap', 'PriceSwap', 'VolatilitySwap']:
        first_char = 'S'
    elif instrument.InsType() in ['Cap', 'Floor']:
        first_char = 'H'
    elif instrument.InsType() in ['SecurityLoan', 'Repo/Reverse', 'BasketSecurityLoan', 'BasketRepo/Reverse', 'BuySellback']:
        first_char = 'L'
    elif instrument.InsType() in ['Commodity', 'Commodity Variant']:
        first_char = 'I'
    return first_char

def get_combination_classification(instrument):
    is_equity = False
    is_commodity = False
    is_credit = False
    is_rate = False
    is_curr = False
    equity_counter = 0
    cmdty_counter = 0
    credit_counter = 0
    rate_counter = 0
    curr_counter = 0
    misc_counter = 0
    for ins_map in instrument.InstrumentMaps():
        if ins_map.Instrument().InsType() in ['EquityIndex', 'Stock', 'Dividend Point Index']:
            equity_counter = equity_counter + 1
        elif ins_map.Instrument().InsType() in ['Average Future/Forward', 'Commodity', 'Commodity Index', 'Commodity Variant', \
    'Precious Metal Rate', 'Rolling Schedule']:
            cmdty_counter = cmdty_counter + 1
        elif ins_map.Instrument().InsType() in ['CreditIndex']:
            credit_counter = credit_counter + 1
        elif ins_map.Instrument().InsType() in ['Bill', 'Bond', 'Convertible', 'Deposit', 'FRA', 'FRN', 'RateIndex', 'Zero', 'IndexLinkedBond', 'Swap']:
            rate_counter = rate_counter + 1
        elif ins_map.Instrument().InsType() in ['Curr']:
            curr_counter = curr_counter + 1
        else:
            misc_counter = misc_counter + 1
    if equity_counter > 0 and cmdty_counter == 0 and credit_counter == 0 and misc_counter == 0 and rate_counter == 0 and curr_counter == 0:
        is_equity = True
    elif cmdty_counter > 0 and equity_counter == 0 and credit_counter == 0 and misc_counter == 0 and rate_counter == 0 and curr_counter == 0:
        is_commodity = True
    elif credit_counter > 0 and equity_counter == 0 and cmdty_counter == 0 and misc_counter == 0 and rate_counter == 0 and curr_counter == 0:
        is_credit = True
    elif rate_counter > 0 and equity_counter == 0 and cmdty_counter == 0 and misc_counter == 0 and credit_counter == 0 and curr_counter == 0:
        is_rate = True
    elif curr_counter > 0 and equity_counter == 0 and cmdty_counter == 0 and misc_counter == 0 and credit_counter == 0 and rate_counter == 0:
        is_curr = True
    return is_equity, is_commodity, is_credit, is_rate, is_curr

def get_TRS_float_rate_ref_classification(instrument):
    classification_char = 'M'
    if instrument:
        if instrument.InsType() in ['Combination']:
            classification_char = get_combination_classification_char(instrument)
        if (instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['EquityIndex', 'Stock']) or \
           (instrument.InsType() in ['EquityIndex', 'Stock', 'Dividend Point Index', 'Depositary Receipt']) :
            classification_char = 'E'
        if instrument.InsType() in ['Average Future/Forward', 'Commodity', 'Commodity Index', 'Commodity Variant', \
            'Precious Metal Rate', 'Rolling Schedule', 'PriceSwap', 'PriceIndex']:
            classification_char = 'T'
        if instrument.InsType() in ['BasketRepo/Reverse', 'BasketSecurityLoan', 'Bill', 'Bond', 'BondIndex', 'BuySellback', \
            'CallAccount', 'CD', 'Certificate', 'CLN', 'Convertible', 'Deposit', 'Flexi Bond', \
            'FRA', 'FRN', 'IndexLinkedBond', 'PromisLoan', 'RateIndex', 'Repo/Reverse', 'SecurityLoan', 'Zero', 'DualCurrBond']:
            classification_char = 'R'
        if instrument.InsType() in ['CreditIndex']:
            classification_char = 'C'
        #if instrument.InsType() in ['Curr']:
        #    classification_char = 'F'
    return classification_char

def get_combination_classification_char(instrument):
    cmdty_classify_char = 'M'
    is_equity, is_commodity, is_credit, is_rate, is_curr = get_combination_classification(instrument)
    if is_equity:
        cmdty_classify_char = 'E'
    if is_commodity:
        cmdty_classify_char = 'T'
    if is_credit:
        cmdty_classify_char = 'C'
    if is_rate:
        cmdty_classify_char = 'R'
    if is_curr:
        cmdty_classify_char = 'F'
    return cmdty_classify_char

def get_second_char_in_cfi_code(instrument, ins_type):
    second_char = 'X'
    if instrument.InsType() in ['Rolling Schedule', 'Commodity', 'Commodity Variant']:
        second_char = 'T'
    elif instrument.InsType() in ['Certificate', 'CD', 'Deposit', 'Flexi Bond']:
        second_char = 'M'
    elif instrument.InsType() in ['Commodity Index', 'CreditIndex']:
        second_char = 'I'
    elif instrument.InsType() in ['Stock', 'SecurityLoan', 'BasketSecurityLoan', 'CLN']:# and (not instrument.Otc()) :
        second_char = 'S'
    elif instrument.InsType() in ['Depositary Receipt', ]:# and (not instrument.Otc()) :
        second_char = 'D'
    elif instrument.InsType() in ['Dividend Point Index']:
        second_char = 'D'
    elif instrument.InsType() in ['ETF']:
        second_char = 'E'
    elif instrument.InsType() in ['Bill']:
        second_char = 'Y'
    elif instrument.InsType() in ['Bond', 'FRN', 'PromisLoan', 'Zero']:# and (not instrument.Otc()) :
        if instrument.Issuer() and instrument.Issuer().BusinessStatus() and 'MUNICIPAL' in instrument.Issuer().BusinessStatus().Name().upper():
            second_char = 'N'
        else:
            tenure = get_tenure(instrument)
            if tenure > 366:
                second_char = 'B'
            else:
                second_char = 'Y'
    elif instrument.InsType() in ['Convertible', 'Curr', 'Combination']:# and (not instrument.Otc()) :
        second_char = 'C'
    elif instrument.InsType() in ['MBS/ABS']:# and (not instrument.Otc()) :
        second_char = 'A'
    elif instrument.InsType() in ['Warrant']:
        second_char = 'W'
    elif instrument.InsType() in ['Option']:
        if is_otc_option(instrument):
            second_char = 'M'
            if instrument.Underlying().InsType() in ['VarianceSwap']:
                if instrument.Underlying().Underlying().InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt',]:
                    second_char = 'E'
                elif instrument.Underlying().Underlying().InsType() in ['Curr']:
                    second_char = 'F'
            elif instrument.Underlying().InsType() in ['Bill', 'Bond', 'FRN', 'Convertible', 'Deposit',  'Zero', 'PromisLoan', 'Swap', \
                'IndexLinkedSwap', 'Cap', 'Floor', 'FRA', 'CurrSwap', 'RateIndex']:
                second_char = 'R'
            elif instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index', 'Average Future/Forward']:
                second_char = 'T'
            elif instrument.Underlying().InsType() in ['TotalReturnSwap']:
                for leg in instrument.Underlying().Legs():
                    if leg.LegType() == 'Total Return':
                        second_char = get_TRS_float_rate_ref_classification(leg.FloatRateReference())
            elif instrument.Underlying().InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt', 'Dividend Point Index'] or \
                (instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['Stock', 'EquityIndex']):
                second_char = 'E'
            elif instrument.Underlying().InsType() in ['Combination']:
                second_char = get_combination_classification_char(instrument.Underlying())
            elif instrument.Underlying().InsType() in ['CreditDefaultSwap', 'CLN']:
                second_char = 'C'
            elif instrument.Underlying().InsType() in ['Curr']:
                second_char = 'F'
            elif instrument.Underlying().InsType() in ['Option', 'Warrant', 'CFD']:
                underlyer = instrument.Underlying().Underlying()
                if underlyer.InsType() in ['Bill', 'Bond', 'FRN', 'Convertible', 'Deposit',  'Zero', 'PromisLoan', 'Swap', \
                    'IndexLinkedSwap', 'VarianceSwap', 'Cap', 'Floor', 'FRA', 'CurrSwap', 'RateIndex']:
                    second_char = 'R'
                elif underlyer.InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index', 'Average Future/Forward']:
                    second_char = 'T'
                elif underlyer.InsType() in ['Curr']:
                    second_char = 'F'
                elif underlyer.InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt', 'Dividend Point Index'] or \
                (underlyer.InsType() in ['CFD'] and underlyer.Underlying().InsType() in ['Stock', 'EquityIndex']):
                    second_char = 'E'
            elif instrument.Underlying().InsType() in ['Future/Forward']:
                underlyer = instrument.Underlying().Underlying()
                if underlyer.InsType() in ['Average Future/Forward', 'Commodity', 'Commodity Variant', 'Commodity Index']:
                    second_char = 'T'
                elif underlyer.InsType() in ['Bill', 'Bond', 'Convertible', 'Deposit', 'FRA', 'FRN', 'RateIndex', 'Zero', 'IndexLinkedBond', 'Swap', 'PromisLoan']:
                    second_char = 'R'
                elif underlyer.InsType() in ['Combination']:
                    second_char = get_combination_classification_char(underlyer)
                elif underlyer.InsType() in ['CreditDefaultSwap', 'CLN', ]:
                    second_char = 'C'
                elif underlyer.InsType() in ['Curr']:
                    second_char = 'F'
                elif underlyer.InsType() in ['Dividend Point Index', 'EquityIndex', 'Stock', 'Depositary Receipt']:
                    second_char = 'E'
        else:
            second_char = get_option_callable_char(instrument)

    elif instrument.InsType() in ['Future/Forward', 'Average Future/Forward', 'CFD']:
        if not instrument.Otc():
            second_char = 'C'
            if instrument.InsType() in ['Future/Forward'] and instrument.Underlying().InsType() not in ['Average Future/Forward', 'Commodity', 'Commodity Variant',]:
                second_char = 'F'
            elif instrument.InsType() in ['Future/Forward'] and instrument.Underlying().InsType() in ['Combination']:
                if get_combination_classification(instrument.Underlying())[1]:
                    second_char = 'C'
                else:
                    second_char = 'F'
            elif instrument.InsType() in ['CFD']:
                second_char = 'F'
        else:
            underlyer = None
            if instrument.InsType() == 'Average Future/Forward':
                underlyer = instrument.Legs()[0].FloatRateReference()
            else:
                underlyer = instrument.Underlying()
            if (underlyer.InsType() in ['Stock', 'EquityIndex', 'Dividend Point Index', 'Depositary Receipt']) or \
                (instrument.InsType() in ['CFD'] and underlyer.InsType() in ['Stock', 'EquityIndex']):
                second_char = 'E'
            elif underlyer.InsType() in ['Curr']:
                second_char = 'F'
            elif underlyer.InsType() in ['CreditDefaultSwap', 'CLN']:
                second_char = 'C'
            elif underlyer.InsType() in ['RateIndex', 'Bill', 'Bond', 'FRN', 'Deposit', 'Zero', 'PromisLoan', 'FRA', 'IndexLinkedBond', 'Convertible', 'Swap']:
                second_char = 'R'
            elif underlyer.InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index', \
                                    'Average Future/Forward', 'Precious Metal Rate', 'Rolling Schedule']:
                second_char = 'T'
            elif underlyer.InsType() in ['Combination']:
                second_char = get_combination_classification_char(underlyer)
    elif instrument.InsType() in ['Swap', 'CurrSwap', 'IndexLinkedSwap', 'FRA', 'Cap', 'Floor', 'RateIndex', 'Repo/Reverse', 'BasketRepo/Reverse', 'BuySellback', 'PriceIndex']:
        second_char = 'R'
    elif instrument.InsType() in ['CreditDefaultSwap']:
        second_char = 'C'
    elif instrument.InsType() in ['VarianceSwap', 'VolatilitySwap', ]:
        second_char = 'M'
        if instrument.Underlying().InsType() in ['Stock', 'EquityIndex', 'Depositary Receipt'] or \
            (instrument.Underlying().InsType() in ['Combination'] and get_combination_classification(instrument.Underlying())[0]):
            second_char = 'E'
    elif instrument.InsType() in ['PriceSwap']:
        second_char = 'T'
    elif instrument.InsType() in ['TotalReturnSwap']:
        second_char = 'M'
        for leg in instrument.Legs():
            if leg.LegType() == 'Total Return':
                second_char = get_TRS_float_rate_ref_classification(leg.FloatRateReference())
    elif instrument.InsType() in ['EquityIndex']:
        second_char = 'I'
    elif instrument.InsType() in ['DualCurrBond', 'IndexLinkedBond']:
        second_char = 'B'
    elif instrument.InsType() in ['FXOptionDatedFwd']:
        second_char = 'F'
    return second_char

def get_third_char_in_cfi_code(instrument, ins_type):
    third_char = 'X'
    if instrument.InsType() in ['Rolling Schedule', 'Cap', 'Floor', 'BasketSecurityLoan', 'Flexi Bond', 'CreditIndex']:
        third_char = 'M'
    elif instrument.InsType() in ['Commodity Index']:
        third_char = 'T'
    elif instrument.InsType() in ['Depositary Receipt', 'Certificate', 'Dividend Point Index', 'Repo/Reverse', 'BuySellback']:# and (not instrument.Otc()) :
        third_char = 'S'
    elif instrument.InsType() in ['Bill']:
        third_char = 'Z'
    elif instrument.InsType() in ['Bond', 'Convertible', 'FRN', 'MBS/ABS', 'PromisLoan', 'Zero']:#and (not instrument.Otc()) :
        if instrument.Legs()[0].LegType() in ['Fixed', 'Fixed Accretive']:
            third_char = 'F'
        elif instrument.Legs()[0].LegType() == 'Zero Coupon Fixed':
            third_char = 'Z'
        elif instrument.Legs()[0].LegType() in ['Float', 'Capped Float', 'Floored Float', 'Collared Float', 'Reverse Float']:
            third_char = 'V'
    elif instrument.InsType() in ['Warrant'] and instrument.Underlying() and (not instrument.Otc()) :
        if instrument.Underlying().InsType() in ['Combination', 'ETF', 'Fund']:
            third_char = 'B'
        elif instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
            third_char = 'S'
        elif instrument.Underlying().InsType() in ['Bill', 'Bond', 'FRN', 'Convertible', 'Deposit', 'Zero', 'PromisLoan']:
            third_char = 'D'
        elif instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Average Future/Forward']:
            third_char = 'T'
        elif instrument.Underlying().InsType() in ['Curr',]:
            third_char = 'C'
        elif instrument.Underlying().InsType() in ['EquityIndex', 'RateIndex', 'Commodity Index']:
            third_char = 'I'
        elif instrument.Underlying().InsType() in ['Cap', 'CFD', 'CLN', \
                        'CreditDefaultSwap', 'CurrSwap', 'Floor', 'FreeDefCF', 'FRA', \
                        'Future/Forward', 'IndexLinkedSwap', 'Option', 'Swap', \
                        'TotalReturnSwap', 'VarianceSwap', 'Warrant', ]:
            third_char = 'M'
    elif instrument.InsType() in ['Option']:
        if is_otc_option(instrument):
            third_char = 'M'
            underlying = instrument.Underlying()
            if underlying.InsType() in ['Swap', 'IndexLinkedSwap', 'CurrSwap']:
                third_char = get_swap_classification(underlying)
            elif underlying.InsType() in ['TotalReturnSwap']:
                second_char = get_second_char_in_cfi_code(instrument, instrument.InsType()) 
                if second_char in ['T', 'C']:
                    third_char = 'W'
                elif second_char in ['R']:
                    third_char = get_swap_classification(underlying)
            elif underlying.InsType() == 'FRA':
                third_char = 'R'
            elif underlying.InsType() in ['Cap', 'Floor']:
                third_char = 'O'
            elif underlying.InsType() in ['Option', 'Warrant']:
                third_char = 'O'
                if underlying.Underlying().InsType() in ['Curr']:
                    third_char = 'M'
                elif underlying.Underlying().InsType() in ['Combination'] :
                    if get_second_char_in_cfi_code(instrument, instrument.InsType()) == 'M':
                        third_char = 'M'
            elif underlying.InsType() in ['Future/Forward']:
                underlyer = underlying.Underlying()
                if underlyer.InsType() in ['Bill', 'Bond', 'Convertible', 'Deposit', 'FRA', 'FRN', 'RateIndex', 'Zero', \
                    'Average Future/Forward', 'Commodity', 'Commodity Variant', 'Commodity Index', 'Curr', 'Stock', 'EquityIndex']:
                    if underlying.Otc():
                        third_char = 'R'
                    else:
                        third_char = 'F'
            elif underlying.InsType() in ['Combination'] :
                combination_classification = get_combination_classification_char(underlying)
                if combination_classification == 'T':
                    third_char = 'Q'
                elif combination_classification == 'E':
                    third_char = 'B'
                elif combination_classification =='C':#, 'R', 'F']:#TODO: Should this be M? if yes, there is no need to call it. comment the code
                    third_char = get_credit_default_swap_classification(underlying)
            elif underlying.InsType() in ['Commodity', 'Commodity Variant']:
                und_ins = underlying
                if underlying.InsType() != 'Commodity':
                    und_ins = underlying.Underlying()
                third_char = commodity_classify(und_ins)
            elif underlying.InsType() in ['Commodity Index', 'Dividend Point Index', 'EquityIndex'] or \
                (instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['EquityIndex']):
                third_char = 'I'
            elif underlying.InsType() in ['Stock', 'Depositary Receipt'] or \
                (instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['Stock']):
                third_char = 'S'
            elif underlying.InsType() in ['CreditDefaultSwap']:
                if underlying.Legs()[0].CreditRef().InsType() in ['EquityIndex', 'CreditIndex']:
                    third_char = 'I'
                elif underlying.Legs()[0].CreditRef().InsType() in ['Bill', 'Bond', 'Convertible', 'Deposit', 'FRN', 'Zero']:
                    third_char = 'U'
            elif underlying.InsType() in ['Average Future/Forward']:
                third_char = 'R'
            elif underlying.InsType() in ['Curr']:
                if instrument.Otc():
                    third_char = 'R'
                else:
                    third_char = 'F'
        else:
            third_char = get_exercise_type_char(instrument)
    elif instrument.InsType() in ['Future/Forward'] and (not instrument.Otc()) :
        if instrument.Underlying().InsType() in ['Combination', 'ETF']:
            third_char = 'B'
        elif instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
            third_char = 'S'
        elif instrument.Underlying().InsType() in ['Bill', 'Bond', 'FRN', 'Convertible', 'Deposit', 'Zero', 'PromisLoan', 'IndexLinkedBond']:
            third_char = 'D'
        elif instrument.Underlying().InsType() in ['Curr',]:
            third_char = 'C'
        elif instrument.Underlying().InsType() in ['EquityIndex', 'Commodity Index', 'Dividend Point Index']:
            third_char = 'I'
        elif instrument.Underlying().InsType() in [ 'RateIndex']:
            third_char = 'N'
        elif instrument.Underlying().InsType() in ['Swap']:
            third_char = 'W'
        elif instrument.Underlying().InsType() in ['FRA']:
            third_char = 'N'
        elif instrument.Underlying().InsType() in ['FreeDefCF', 'CLN', 'CreditDefaultSwap']:
            third_char = 'M'
        elif instrument.Underlying().InsType() in ['Average Future/Forward', 'Commodity', 'Commodity Variant',]:
            third_char = 'M'
            underlyer = instrument.Underlying()
            final_underlyer = None
            while underlyer:
                final_underlyer = underlyer
                underlyer = underlyer.Underlying()
            third_char = get_commodity_classification(final_underlyer)
    elif instrument.InsType() in ['Average Future/Forward'] and (not instrument.Otc()) :
        third_char = 'M'
        underlyer = instrument.Legs()[0].FloatRateReference()
        final_underlyer = None
        while underlyer:
            final_underlyer = underlyer
            try:
                underlyer = underlyer.Legs()[0].FloatRateReference()
            except:
                underlyer = None
                pass
        third_char = get_commodity_classification(final_underlyer)

    elif instrument.InsType() in ['Future/Forward', 'Average Future/Forward', 'CFD'] and (instrument.Otc()):
        underlyer = None
        if instrument.InsType() == 'Average Future/Forward':#Average Future/Forward
            underlyer = instrument.Legs()[0].FloatRateReference()
        else:
            underlyer = instrument.Underlying()
        if underlyer.InsType() in ['Stock', 'Depositary Receipt']:
            third_char = 'S'
        elif underlyer.InsType() in ['EquityIndex', 'Dividend Point Index', 'RateIndex']:
            third_char = 'I'
        elif underlyer.InsType() in ['Combination']:
            if get_combination_classification(underlyer)[0] or get_combination_classification(underlyer)[1] or get_combination_classification(underlyer)[2]:
                third_char = 'B'
            elif get_combination_classification(underlyer)[4]:
                third_char = 'R'
        elif underlyer.InsType() in ['CreditDefaultSwap']:
            third_char = get_credit_default_swap_classification_FutureForward(underlyer)
        elif underlyer.InsType() in ['Bill', 'Bond', 'FRN', 'Deposit', 'Zero', 'PromisLoan', 'FRA', 'IndexLinkedBond', 'Convertible', 'Swap', 'BasketSecurityLoan']:
            third_char = 'M'
        elif underlyer.InsType() in ['Commodity', 'Commodity Variant', 'Commodity Index', 'Average Future/Forward', 'Precious Metal Rate', 'Rolling Schedule']:
            third_char = get_commodity_classification_for_swaps(instrument)#.Underlying())
        elif underlyer.InsType() in ['Curr']:
            third_char = 'R'
    elif instrument.InsType() in ['Swap', 'CurrSwap', 'IndexLinkedSwap']:
        third_char = get_swap_classification(instrument)
    elif instrument.InsType() in ['PriceSwap']:
        third_char = get_commodity_classification_for_swaps(instrument)
    elif instrument.InsType() in ['TotalReturnSwap']:    
        third_char = 'M'
        for leg in instrument.Legs():
            if leg.LegType() == 'Total Return':
                reference = leg.FloatRateReference()
                if reference.InsType() in ['EquityIndex']:
                    third_char = 'I'
                elif reference.InsType() in ['Stock']:
                    third_char = 'S'
                elif reference.InsType() in ['CFD']:
                    if reference.Underlying().InsType() in ['EquityIndex']:
                        third_char = 'I'
                    elif reference.Underlying().InsType() in ['Stock']:
                        third_char = 'S'
                elif reference.InsType() in ['Average Future/Forward', 'Commodity', 'Commodity Variant', \
                        'Precious Metal Rate', 'Rolling Schedule']:
                    third_char = get_commodity_classification_for_swaps(reference)
                elif reference.InsType() in ['CreditIndex', 'Commodity Index']:
                    third_char = 'I'
                elif reference.InsType() in ['Combination']:
                    is_equity, is_commodity, is_credit, is_rate, is_curr = get_combination_classification(reference)
                    third_char = 'M'
                    if is_commodity:
                        third_char = 'Q'
                    elif is_equity:
                        third_char = 'B'
                    elif is_credit:
                        third_char = 'B'
                elif reference.InsType() in ['Bond', 'Convertible', 'DualCurrBond', \
                    'Flexi Bond', 'FRN', 'PromisLoan', 'BasketRepo/Reverse', 'BasketSecurityLoan', \
                    'Bill', 'BuySellback', 'CD', 'CLN', 'Deposit', 'IndexLinkedBond', 'RateIndex', \
                    'Repo/Reverse', 'SecurityLoan', 'Zero']:
                    third_char = get_swap_classification(instrument)
    elif instrument.InsType() in ['VarianceSwap', 'VolatilitySwap', ]:
        third_char = 'M'
        if instrument.Underlying().InsType() in ['EquityIndex']:
            third_char = 'I'
        elif instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
            third_char = 'S'
        elif instrument.Underlying().InsType() in ['Combination'] and get_combination_classification(instrument.Underlying())[0]:
            third_char = 'B'
    elif instrument.InsType() in ['CreditDefaultSwap']:
        third_char = 'M'
        credit_ref = None
        for leg in instrument.Legs():
            if leg.CreditRef():
                credit_ref = leg.CreditRef()
                break
        if credit_ref:
            if credit_ref.InsType() in ['Bill', 'Bond', 'Deposit', 'Flexi Bond', 'Zero', 'PromisLoan', 'Certificate', 'FRN']:
                third_char = 'U'
            elif credit_ref.InsType() in ['CreditIndex']:
                third_char = 'I'
            elif credit_ref.InsType() in ['Combination']:
                third_char = 'B'
    elif instrument.InsType() in ['Warrant']:
        if instrument.Underlying().InsType() in ['VarianceSwap', 'Warrant', 'TotalReturnSwap', \
            'Future/Forward', 'Option', 'FreeDefCF', 'Floor', 'Bond', 'CreditDefaultSwap', \
            'CFD', 'Cap', 'Bill', 'ETF']:
            third_char = 'M'
        elif instrument.Underlying().InsType() in ['Zero', 'Swap', 'PromisLoan', 'IndexLinkedSwap', \
            'FRN', 'FRA', 'Deposit', 'CurrSwap', 'Convertible', 'CLN']:
            third_char = 'D'
        elif instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
            third_char = 'S'
        elif instrument.Underlying().InsType() in ['RateIndex', 'EquityIndex', 'Commodity Index']:
            third_char = 'I'
        elif instrument.Underlying().InsType() in ['Curr']:
            third_char = 'C'
        elif instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Average Future/Forward']:
            third_char = 'T'
        elif instrument.Underlying().InsType() in ['Combination']:
            third_char = 'B'
    elif instrument.InsType() in ['FRA']:
        third_char = 'I'
    elif instrument.InsType() in ['EquityIndex']:
        third_char = 'E'
    elif instrument.InsType() in ['RateIndex']:
        third_char = 'V'
    elif instrument.InsType() in ['SecurityLoan']:
        if instrument.Underlying():
            if instrument.Underlying().InsType() in ['Deposit']:
                third_char = 'C'
            elif instrument.Underlying().InsType() in ['Bill']:
                third_char = 'K'
            elif instrument.Underlying().InsType() in ['CD']:
                third_char = 'D'
            elif instrument.Underlying().InsType() in ['CLN', 'Combination', 'Commodity', 'Commodity Variant', \
                    'Dividend Point Index', 'ETF', 'FreeDefCF', 'IndexLinkedBond', 'MBS/ABS', 'Swap']:
                third_char = 'M'
            elif instrument.Underlying().InsType() in ['Convertible']:
                third_char = 'T'
            elif instrument.Underlying().InsType() in ['Depositary Receipt', 'EquityIndex', 'Stock', ]:
                third_char = 'E'
            elif instrument.Underlying().InsType() in ['Bond', 'DualCurrBond', 'Flexi Bond', 'FRN', 'PromisLoan', 'Zero']:
                third_char = 'X'
                if instrument.Underlying().Issuer() and instrument.Underlying().Issuer().BusinessStatus():
                    business_status = instrument.Underlying().Issuer().BusinessStatus().Name()
                    if 'GOVERNMENT' in business_status.upper():
                        third_char = 'G'
                    elif 'MUNICIPAL' in business_status.upper():
                        third_char = 'P'
    elif instrument.InsType() in ['CLN']:
        third_char = 'A'
    elif instrument.InsType() in ['BasketRepo/Reverse']:
        third_char = 'G'
    elif instrument.InsType() in ['IndexLinkedBond', 'DualCurrBond']:
        third_char = 'V'
    elif instrument.InsType() in ['CD']:
        third_char = 'P'
    elif instrument.InsType() in ['Deposit']:
        third_char = 'B'
    elif instrument.InsType() in ['CFD'] and (not instrument.Otc()):
        if instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
            third_char = 'S'
        elif instrument.Underlying().InsType() in ['EquityIndex']:
            third_char = 'I'
        elif instrument.Underlying().InsType() in ['Bond']:
            third_char = 'B'
        elif instrument.Underlying().InsType() in ['ETF', 'Warrant']:
            third_char = 'M'
    elif instrument.InsType() in ['Commodity', 'Commodity Variant']:
        third_char = commodity_classify(instrument)
    elif instrument.InsType() in ['FXOptionDatedFwd']:
        third_char = 'R'
    elif instrument.InsType() in ['Combination']:
        b_shares = False
        b_bonds = False
        b_warrants = False
        b_funds = False
        b_others = False
        for ins_map in instrument.InstrumentMaps():
            if ins_map.Instrument().InsType() in ['Bill', 'Bond', 'DualCurrBond', \
                'Flexi Bond', 'FRN', 'PromisLoan', 'Zero', 'IndexLinkedBond', \
                'Convertible']:
                b_bonds = True
            elif ins_map.Instrument().InsType() in ['Depositary Receipt', 'Stock']:
                b_shares = True
            elif ins_map.Instrument().InsType() in ['CLN', 'Combination', 'Commodity', 'Commodity Variant', \
                    'Dividend Point Index', 'FreeDefCF', 'MBS/ABS', 'Swap', \
                    'VarianceSwap', 'TotalReturnSwap', 'Future/Forward', 'Option', 'Floor', \
                    'CreditDefaultSwap', 'CFD', 'Cap', 'IndexLinkedSwap', 'FRA', 'Deposit', 'CurrSwap', \
                    'CLN', 'RateIndex', 'Commodity Index', 'Curr', 'Average Future/Forward', \
                    'Combination', 'EquityIndex', ]:
                b_others = True
            elif ins_map.Instrument().InsType() in ['Warrant']:
                b_warrants = True
            elif ins_map.Instrument().InsType() in ['ETF']:
                b_funds = True
        if b_others:
            third_char = 'M'
        else:
            if b_funds:
                if b_shares or b_bonds or b_warrants:
                    third_char = 'M'
                else:
                    third_char = 'U'
            else:
                if b_bonds and b_warrants:
                    third_char = 'M'
                elif b_shares and b_bonds:
                    third_char = 'H'
                elif b_shares and b_warrants:
                    third_char = 'A'
                elif b_shares:
                    third_char = 'S'
                elif b_bonds:
                    third_char = 'B'
                elif b_warrants:
                    third_char = 'W'
        
    return third_char

def get_credit_default_swap_classification_FutureForward(instrument):
    leg_ref = None
    if instrument.InsType() == 'CreditDefaultSwap':
        for leg in instrument.Legs():
            if leg.LegType() == 'Credit Default':
                leg_ref = leg
                break
    elif instrument.InsType() == 'CLN':
        leg_ref = instrument.Legs()[0]
    if leg_ref:
        instrument = leg_ref.CreditRef()        
    cds_classify = 'X'
    if instrument.InsType() in ['Bill', 'Bond', 'Deposit', 'Flexi Bond', 'Zero', 'PromisLoan']:
        cds_classify = 'C'
    if instrument.InsType() in ['CreditIndex']:
        cds_classify = 'D'
    if instrument.InsType() in ['Combination'] and get_combination_classification(instrument)[2]:
        cds_classify = 'I'
    return cds_classify
    
def get_credit_default_swap_classification(instrument):
    leg_ref = None
    if instrument.InsType() == 'CreditDefaultSwap':
        for leg in instrument.Legs():
            if leg.LegType() == 'Credit Default':
                leg_ref = leg
                break
    elif instrument.InsType() == 'CLN':
        leg_ref = instrument.Legs()[0]
    if leg_ref:
        instrument = leg_ref.CreditRef()        
    cds_classify = 'M'
    if instrument.InsType() in ['Bill', 'Bond', 'Deposit', 'Flexi Bond', 'Zero', 'PromisLoan']:
        cds_classify = 'C'
    if instrument.InsType() in ['CreditIndex']:
        cds_classify = 'D'
    if instrument.InsType() in ['Combination'] and get_combination_classification(instrument)[2]:
        cds_classify = 'I'
    return cds_classify

def get_otc_option_style_type(instrument):
    option_type = None
    option_style = ''
    option_style_type_classification = 'X'
    if instrument.IsCallOption():
        option_type = 'Call'
    else:
        option_type = 'Put'
    if instrument.ExerciseType():
        if instrument.ExerciseType() in ['American', 'Amer GA']:
            option_style = 'American'
        if instrument.ExerciseType() == 'Bermudan':
            option_style = 'Bermudan'
        if instrument.ExerciseType() == 'European':
            option_style = 'European'
    if option_style_type_lookup.has_key(option_style + '-' + option_type):
        option_style_type_classification = option_style_type_lookup[option_style + '-' + option_type]
    return option_style_type_classification
        
def is_otc_option(instrument):
    otc_option = False
    exotic_char = get_exotic_char(instrument)
    if instrument.Otc() or instrument.Underlying().InsType() in ['CLN', 'CreditDefaultSwap', 'CFD'] or (instrument.Underlying().InsType() == 'Curr' and exotic_char != 'V'):
        otc_option = True
    return otc_option
    
def get_fourth_char_in_cfi_code(instrument, ins_type):
    fourth_char = 'X'
    if instrument.InsType() in ['Bond', 'Convertible', 'FRN', 'MBS/ABS', 'PromisLoan', 'Zero', 'Bill', 'IndexLinkedBond']: #and (not instrument.Otc()) :
        fourth_char = get_seniority_char(instrument)
    elif instrument.InsType() in ['Warrant'] and (not instrument.Otc()):
        fourth_char = 'T'
    elif instrument.InsType() in ['Option']:
        if is_otc_option(instrument):
            fourth_char = get_otc_option_style_type(instrument)
        else:
            if instrument.Underlying().InsType() in ['Combination', 'ETF', 'Fund', ]:
                fourth_char = 'B'
            if instrument.Underlying().InsType() in ['Stock', 'Depositary Receipt']:
                fourth_char = 'S'
            if instrument.Underlying().InsType() in ['Bill', 'Bond', 'FRN', 'Convertible', 'Deposit',  'Zero', 'PromisLoan']:
                fourth_char = 'D'
            if instrument.Underlying().InsType() in ['Commodity', 'Commodity Variant', 'Average Future/Forward', ]:
                fourth_char = 'T'
            if instrument.Underlying().InsType() in ['Curr',]:
                fourth_char = 'C'
            if instrument.Underlying().InsType() in ['EquityIndex', 'RateIndex', 'Commodity Index', ]:
                fourth_char = 'I'
            if instrument.Underlying().InsType() in ['Option', 'Warrant']:
                fourth_char = 'O'
            if instrument.Underlying().InsType() in ['Future/Forward']:
                fourth_char = 'F'
            if instrument.Underlying().InsType() in ['CurrSwap', 'Swap', 'IndexLinkedSwap', 'TotalReturnSwap', 'VarianceSwap', 'CreditDefaultSwap']:
                fourth_char = 'W'
            if instrument.Underlying().InsType() in ['Cap', 'Floor', 'FRA']:
                fourth_char = 'N'
            if instrument.Underlying().InsType() in ['CFD', 'CLN', 'FreeDefCF', 'PromisLoan', ]:#TODO: Discuss with Ishan for CLN
                fourth_char = 'M'
    elif instrument.InsType() in ['Future/Forward', 'Average Future/Forward'] and (not instrument.Otc()):
        fourth_char = get_delivery_char(instrument)
    elif instrument.InsType() in ['Swap', 'CurrSwap' 'IndexLinkedSwap']:
        fourth_char = 'X'
    elif instrument.InsType() in ['VarianceSwap']:
        fourth_char = 'X'
        if instrument.Underlying().InsType() in ['EquityIndex', 'Stock', 'Depositary Receipt'] or (instrument.Underlying().InsType() in ['Combination'] and get_combination_classification(instrument.Underlying())[0]):
            fourth_char = 'V'
    elif instrument.InsType() in ['VolatilitySwap', ]:
        fourth_char = 'X'
        if instrument.Underlying().InsType() in ['EquityIndex', 'Stock', 'Depositary Receipt'] or (instrument.Underlying().InsType() in ['Combination'] and get_combination_classification(instrument.Underlying())[0]):
            fourth_char = 'L'
    elif instrument.InsType() in ['CreditDefaultSwap']:
        fourth_char = 'C'
    elif instrument.InsType() in ['PriceSwap']:
        fourth_char = 'X'#TODO: discuss with Thomas
    elif instrument.InsType() in ['TotalReturnSwap']:
        fourth_char = 'X'
        for leg in instrument.Legs():
            if leg.LegType() == 'Total Return' and leg.FloatRateReference():#Tell Thomas
                if leg.FloatRateReference().InsType() in ['EquityIndex', 'Stock'] or \
                    (leg.FloatRateReference().InsType() in ['CFD'] and leg.FloatRateReference().Underlying().InsType() in ['EquityIndex', 'Stock']):
                    #if leg.PassingType() != 'None':
                    fourth_char = 'T'
                    #else:
                    #    fourth_char = 'P'
                if leg.FloatRateReference().InsType() in ['Dividend Point Index']:
                    fourth_char = 'D'
                if leg.FloatRateReference().InsType() in ['Depositary Receipt']:
                    fourth_char = 'T'
                if leg.FloatRateReference().InsType() in ['Average Future/Forward', 'Commodity', 'Commodity Index', 'Commodity Variant', \
                        'Precious Metal Rate', 'Rolling Schedule']:
                    fourth_char = 'X'#TODO: discuss with Thomas
                if leg.FloatRateReference().InsType() in ['CreditIndex']:
                    fourth_char = 'C'
                if leg.FloatRateReference().InsType() in ['Combination']:
                    is_equity, is_commodity, is_credit, is_rate, is_curr = get_combination_classification(leg.FloatRateReference())
                    if is_equity:
                        if leg.PassingType() != 'None':
                            fourth_char = 'T'
                        else:
                            fourth_char = 'P'
                    if is_commodity:
                        fourth_char = 'X'#TODO: discuss with Thomas
                    if is_credit:
                        fourth_char = 'T'
                break
    elif instrument.InsType() in ['Cap']:
        fourth_char = 'A'
    elif instrument.InsType() in ['Floor']:
        fourth_char = 'D'
    elif instrument.InsType() in ['CLN']:
        if instrument.Legs()[0].LegType() == 'Fixed':
            fourth_char = 'F'
        else:
            fourth_char = 'V'
    elif instrument.InsType() in ['SecurityLoan', 'Repo/Reverse', 'BasketSecurityLoan', 'BasketRepo/Reverse']:
        if instrument.OpenEnd():
            fourth_char = 'X'
            if instrument.OpenEnd() == 'Open End':
                fourth_char = 'O'
        else:
            end_date = ael.date_from_string(instrument.EndDate())
            start_date = ael.date_from_string(instrument.StartDate())
            date_diff = start_date.days_between(end_date)
            if abs(date_diff) == 1:
                fourth_char = 'N'
            else:
                fourth_char = 'T'
    elif instrument.InsType() in ['BuySellback']:
        fourth_char = 'T'
        end_date = ael.date_from_string(instrument.ExpiryDateOnly())
        start_date = ael.date_from_string(instrument.StartDate())
        date_diff = start_date.days_between(end_date)
        if abs(date_diff) == 1:
            fourth_char = 'N'
    elif instrument.InsType() in ['Depositary Receipt']:
        fourth_char = 'N'
    elif instrument.InsType() in ['CFD'] and (not instrument.Otc()):
        fourth_char = 'C'
    return fourth_char

def get_exotic_char(instrument):
    valuation_method = 'M'
    exotic_type = None
    if instrument.Exotics() and instrument.Exotics()[0].Oid() > 0:
        if instrument.Exotics()[0].AverageMethodType() != 'None':
            exotic_type = 'Asian'
        elif instrument.Exotics()[0].LookbackOptionType() != 'None':
            exotic_type = 'Lookback'
        elif instrument.Exotics()[0].RangeAccrualAmount():
            exotic_type = 'Range Accrual'
        elif instrument.Exotics()[0].BarrierOptionType():
            if 'KIKO' in instrument.Exotics()[0].BarrierOptionType():
                exotic_type = 'KIKO'
            else:
                exotic_type = 'Barrier'
        if instrument.Exotics()[0].DigitalBarrierType():
            if instrument.Exotics()[0].DigitalBarrierType() == 'Barrier & Strike':
                exotic_type = 'Digital European Barrier'
            elif instrument.Exotics()[0].DigitalBarrierType() == 'Barrier':
                exotic_type = 'Digital American'
    else:
        if instrument.Digital():
            exotic_type = 'Digital European Vanilla'
        else:
            if instrument.ExerciseType().upper() == 'NONE':
                exotic_type = 'Custom'
            else:
                exotic_type = 'Vanilla'
    if exotic_type and exotic_lookup.has_key(exotic_type):
        valuation_method = exotic_lookup[exotic_type]
    return valuation_method
            
def get_fifth_char_in_cfi_code(instrument, ins_type):
    fifth_char = 'X'
    if instrument.InsType() in ['Rolling Schedule', 'FRA', 'FXOptionDatedFwd']:
        fifth_char = 'F'
    elif instrument.InsType() in ['ETF']:
        if instrument.Underlying().InsType() == 'Stock':
            fifth_char = 'E'
        elif instrument.Underlying().InsType() == 'Bond':
            fifth_char = 'B'
        elif instrument.Underlying().InsType() == 'Combination':
            fifth_char = 'L'
        elif instrument.Underlying().InsType() == 'Commodity':
            fifth_char = 'C'
        elif instrument.Underlying().InsType() in ['EquityIndex', 'RateIndex']:
            fifth_char = 'F'
        elif instrument.Underlying().InsType() == 'Future/Forward':
            fifth_char = 'D'
    elif instrument.InsType() in ['Future/Forward', 'Average Future/Forward'] and (instrument.Otc()):
        fifth_char = 'F'
    elif instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['Stock', 'EquityIndex'] and (instrument.Otc()):
        fifth_char = 'C'

    elif instrument.InsType() in ['ETFXYZ'] and (not instrument.Otc()) :
        if instrument.Underlying().InsType() in ['Stock', 'EquityIndex']:
            fifth_char = 'E'
        if instrument.Underlying().InsType() in ['Bond']:
            fifth_char = 'B'
        if instrument.Underlying().InsType() in ['Combination']:
            fifth_char = 'M'
        if instrument.Underlying().InsType() in ['Commodity']:
            fifth_char = 'C'
        if instrument.Underlying().InsType() in ['RateIndex', 'Future/Forward']:
            fifth_char = 'D'

    elif instrument.InsType() in ['Bond', 'Convertible', 'FRN', 'MBS/ABS', 'PromisLoan', 'Zero', 'DualCurrBond', 'IndexLinkedBond']:# and (not instrument.Otc()):
        if instrument.Callable() and instrument.Putable():
            fifth_char = 'D'
        elif instrument.Callable():
            fifth_char = 'G'
        elif instrument.Putable():
            fifth_char = 'C'
        else:
            fifth_char = 'F'
    elif instrument.InsType() in ['Warrant']:
        fifth_char = get_option_callable_char(instrument)
    elif instrument.InsType() in ['Option']:
        if is_otc_option(instrument):
        #if instrument.Otc() or instrument.Underlying().InsType() in ['CLN', 'CreditDefaultSwap']:
            fifth_char = 'V'
            if instrument.Underlying().InsType() in ['Curr'] or \
                (instrument.Underlying().InsType() in ['Future/Forward'] and instrument.Underlying().Underlying().InsType() == 'Curr') or \
                (instrument.Underlying().InsType() in ['Combination'] and get_combination_classification_char(instrument.Underlying()) == 'F'):
                    fifth_char = get_exotic_char(instrument)

        else:
            fifth_char = get_delivery_char(instrument)
    elif instrument.InsType() in ['Future/Forward', 'Average Future/Forward'] and (not instrument.Otc()):
        fifth_char = 'S'
    elif instrument.InsType() in ['Swap', 'CurrSwap', 'IndexLinkedSwap']:
        fifth_char = 'S'
        if is_underlyer_curr_different(instrument):
            fifth_char = 'C'
    elif instrument.InsType() in ['PriceSwap']:
        fifth_char = 'X'
    elif instrument.InsType() in ['CreditDefaultSwap']:
        credit_ref = None
        for leg in instrument.Legs():
            if leg.CreditRef():
                credit_ref = leg.CreditRef()
                break
        fifth_char = get_credit_category(credit_ref)
    elif instrument.InsType() in ['CurrSwap', ]:
        fifth_char = 'C'
    elif instrument.InsType() in ['VolatilitySwap', 'VarianceSwap',]: 
        fifth_char = 'X'
    elif instrument.InsType() in ['TotalReturnSwap']:
        if get_second_char_in_cfi_code(instrument, instrument.InsType()) == 'R':
            fifth_char = 'S'
            if is_underlyer_curr_different(instrument):
                fifth_char = 'C'
        else:
            float_rate_ref = None
            for leg in instrument.Legs():
                if leg.FloatRateReference():
                    float_rate_ref = leg.FloatRateReference()
                    break
            if float_rate_ref.InsType() in ['Combination']:
                is_equity, is_commodity, is_credit, is_rate, is_curr = get_combination_classification(float_rate_ref)
                if is_credit:
                    fifth_char = get_credit_category(float_rate_ref)
            if float_rate_ref.InsType() in ['CreditIndex']:
                fifth_char = get_credit_category(float_rate_ref)
    elif instrument.InsType() in ['Cap', 'Floor']:
        fifth_char = 'V'
    elif instrument.InsType() in ['Depositary Receipt']:
        fifth_char = 'D'
    elif instrument.InsType() in ['CLN']:
        fifth_char = 'M'  
    elif instrument.InsType() in ['CFD'] and (not instrument.Otc()):
        fifth_char = 'S'     
            
    return fifth_char

def get_sixth_char_in_cfi_code(instrument, ins_type):
    sixth_char = 'X'
    if instrument.InsType() in ['Rolling Schedule', 'FRA']:
        sixth_char = 'C'
    elif instrument.InsType() in ['FXOptionDatedFwd']:
        sixth_char = 'P'
    elif instrument.InsType() in ['ETF']:
        sixth_char = 'U'
        if instrument.Underlying().InsType() == 'Stock':
            sixth_char = 'S'
    elif instrument.InsType() in ['Warrant']:
        sixth_char = get_exercise_type_char(instrument)
    elif instrument.InsType() in ['Swap', 'IndexLinkedSwap', 'PriceSwap', 'VolatilitySwap', 'VarianceSwap']:
        sixth_char = 'C'
    elif instrument.InsType() in ['TotalReturnSwap', 'CreditDefaultSwap']:
        sixth_char = get_delivery_char(instrument)
    elif instrument.InsType() in ['Future/Forward', 'Average Future/Forward'] and instrument.Otc():
        sixth_char = get_delivery_char(instrument)
    elif instrument.InsType() in ['CFD'] and instrument.Underlying().InsType() in ['Stock', 'EquityIndex'] and instrument.Otc():
        sixth_char = get_delivery_char(instrument)
    elif instrument.InsType() in ['CurrSwap']:
        sixth_char = is_non_deliverable_swap(instrument)
    #elif (instrument.InsType() in ['Option'] and (instrument.Otc() or instrument.Underlying().InsType() in ['CLN', 'CreditDefaultSwap'])):
    elif instrument.InsType() in ['Option'] and is_otc_option(instrument):
        sixth_char = get_delivery_char(instrument)
    elif instrument.InsType() in ['Cap', 'Floor']:
        sixth_char = 'C'
    elif instrument.InsType() in ['CLN']:
        if instrument.Legs()[0].CreditRef().InsType() in ['Average Future/Forward', 'Commodity', 'Commodity Variant', 'Rolling Schedule']:
            sixth_char = 'T'
        elif instrument.Legs()[0].CreditRef().InsType() in ['BasketRepo/Reverse', 'Repo/Reverse', 'FxSwap', 'Swap', \
            'CurrSwap', 'IndexLinkedSwap', 'SecurityLoan', 'BasketSecurityLoan', 'BuySellback', ]:
            sixth_char = 'N'
        elif instrument.Legs()[0].CreditRef().InsType() in ['Combination', 'ETF', 'Fund', ]:
            sixth_char = 'B'
        elif instrument.Legs()[0].CreditRef().InsType() in ['Bill', 'Bond', 'Convertible', 'Deposit', \
            'FRA', 'FRN', 'IndexLinkedBond', 'PromisLoan', 'CLN', \
            'DualCurrBond', 'CD', 'Flexi Bond', 'MBS/ABS']:
            sixth_char = 'D'
        elif instrument.Legs()[0].CreditRef().InsType() in ['Commodity Index', 'RateIndex', 'CreditIndex', \
            'Dividend Point Index', 'EquityIndex', 'PriceIndex', 'BondIndex']:
            sixth_char = 'I'
        
        elif instrument.Legs()[0].CreditRef().InsType() in ['Stock', 'Depositary Receipt']:
            sixth_char = 'S'
        elif instrument.Legs()[0].CreditRef().InsType() in ['Curr', ]:
            sixth_char = 'C'
        else:
            sixth_char = 'M'
    return sixth_char

def get_first_char_in_cfi_code_trade(trade):
    first_char = 'X'
    if trade.Instrument().InsType() == 'Curr':
        if trade.IsFxSwap():
            first_char = 'S'
        elif trade.IsFxSpot():
            first_char = 'I'
        elif trade.IsFxForward():
            first_char = 'J'
        else:
            first_char = 'F'
    elif (trade.Instrument().InsType() == 'Option' and trade.Instrument().Underlying().InsType() == 'Curr'):
        first_char = 'H'
    elif trade.Instrument().InsType() == 'Future/Forward' and trade.Instrument().Underlying().InsType() == 'Curr':
        if trade.Instrument().Otc():
            first_char = 'J'
        else:
            first_char = 'F'
    return first_char

def get_second_char_in_cfi_code_trade(trade):
    second_char = 'X'
    if (trade.Instrument().InsType() == 'Curr') or \
        (trade.Instrument().InsType() in ['Option', 'Future/Forward'] and trade.Instrument().Underlying().InsType() == 'Curr'):
        second_char = 'F'
    return second_char

def get_third_char_in_cfi_code_trade(trade):
    third_char = 'X'
    if trade.Instrument().InsType() == 'Curr' and trade.IsFxSwap():
        value_day = ael.date_from_string(trade.ValueDay())
        calendar = ael.Calendar[trade.Currency().Legs()[0].PayCalendar().Name()]
        far_leg_value_day = ael.date_from_string(trade.FxSwapFarLeg().ValueDay())
        trade_date = ael.date_from_string(str(trade.TradeTime()).split(' ')[0])
        spot_day = trade_date.add_banking_day(calendar, trade.Instrument().SpotBankingDaysOffset())
        if value_day == spot_day:
            third_char = 'A'
        elif value_day > spot_day:
            third_char = 'C'
        else:
            third_char = 'M'
    elif trade.Instrument().InsType() == 'Curr' and trade.IsFxForward():
        third_char = 'R'
    elif trade.Instrument().InsType() == 'Option' and trade.Instrument().Underlying().InsType() == 'Curr':
        expiry_date = ael.date_from_string(trade.Instrument().ExpiryDateOnly())
        calendar = ael.Calendar[trade.Currency().Legs()[0].PayCalendar().Name()]
        delivery_date = expiry_date.add_banking_day(calendar, trade.Instrument().PayDayOffset())
        trade_date = ael.date_from_string(str(trade.TradeTime()).split(' ')[0])
        spot_day = ael.date_from_string(trade_date.add_banking_day(calendar, trade.Instrument().SpotBankingDaysOffset()))
        if delivery_date == spot_day:
            third_char = 'T'
        else:
            if trade.Instrument().PayType() == 'Future':
                third_char = 'F'
            else:
                third_char = 'R'
        
    elif trade.Instrument().InsType() == 'Future/Forward' and trade.Instrument().Underlying().InsType() == 'Curr':
        if trade.Instrument().Otc():
            expiry_date = ael.date_from_string(trade.Instrument().ExpiryDateOnly())
            calendar = ael.Calendar[trade.Currency().Legs()[0].PayCalendar().Name()]
            delivery_date = ael.date_from_string(trade.Instrument().LastPayDay())
            trade_date = ael.date_from_string(str(trade.TradeTime()).split(' ')[0])
            spot_day = ael.date_from_string(trade_date.add_banking_day(calendar, trade.Instrument().SpotBankingDaysOffset()))
            if delivery_date == spot_day:
                third_char = 'T'
            else:
                if trade.Instrument().PayType() in ['Forward', 'Contingent']:
                    third_char = 'R'
                else:
                    third_char = 'F'
        else:
            third_char = 'C'        
    return third_char

def get_fourth_char_in_cfi_code_trade(trade):
    fourth_char = 'X'
    if trade.Instrument().InsType() == 'Option' and trade.Instrument().Underlying().InsType() == 'Curr':
        fourth_char = get_otc_option_style_type(trade.Instrument())
    elif trade.Instrument().InsType() == 'Future/Forward' and trade.Instrument().Underlying().InsType() == 'Curr':
        if not trade.Instrument().Otc():
            fourth_char = get_delivery_char(trade.Instrument())
    return fourth_char

def get_fifth_char_in_cfi_code_trade(trade):
    fifth_char = 'X'
    if trade.Instrument().InsType() == 'Option' and trade.Instrument().Underlying().InsType() == 'Curr':
        fifth_char = get_exotic_char(trade.Instrument())
    elif trade.Instrument().InsType() == 'Future/Forward' and trade.Instrument().Underlying().InsType() == 'Curr':
        if trade.Instrument().Otc():
            fifth_char = 'F'
        else:
            fifth_char = 'S'
    return fifth_char

def get_sixth_char_in_cfi_code_trade(trade):
    sixth_char = 'X'
    if trade.Instrument().InsType() == 'Curr':
        sixth_char = 'P'
        if trade.IsFxForward():
            sixth_char = 'C'
    elif trade.Instrument().InsType() == 'Option' and trade.Instrument().Underlying().InsType() == 'Curr':
        sixth_char = get_delivery_char(trade.Instrument())
    elif trade.Instrument().InsType() == 'Future/Forward' and trade.Instrument().Underlying().InsType() == 'Curr':
        if trade.Instrument().Otc():
            sixth_char = get_delivery_char(trade.Instrument())
    return sixth_char

def compute_cfi_code(acm_object):
    if acm_object.IsKindOf(acm.FInstrument):
        ins_type = get_instrument_type(acm_object)
        cfi_code = get_first_char_in_cfi_code(acm_object, ins_type) + 'XXXXX'
        cfi_code = cfi_code[0] + get_second_char_in_cfi_code(acm_object, ins_type) + 'XXXX'
        cfi_code = cfi_code[0:2] + get_third_char_in_cfi_code(acm_object, ins_type) + 'XXX'
        cfi_code = cfi_code[0:3] + get_fourth_char_in_cfi_code(acm_object, ins_type) + 'XX'
        cfi_code = cfi_code[0:4] + get_fifth_char_in_cfi_code(acm_object, ins_type) + 'X'
        cfi_code = cfi_code[0:5] + get_sixth_char_in_cfi_code(acm_object, ins_type)
    elif acm_object.IsKindOf(acm.FTrade):
        if (acm_object.Instrument().InsType() == 'Curr') or \
            (acm_object.Instrument().InsType() in ['Option', 'Future/Forward'] and acm_object.Instrument().Underlying().InsType() == 'Curr'):
            cfi_code = get_first_char_in_cfi_code_trade(acm_object) + 'XXXXX'
            cfi_code = cfi_code[0] + get_second_char_in_cfi_code_trade(acm_object) + 'XXXX'
            cfi_code = cfi_code[0:2] + get_third_char_in_cfi_code_trade(acm_object) + 'XXX'
            cfi_code = cfi_code[0:3] + get_fourth_char_in_cfi_code_trade(acm_object) + 'XX'
            cfi_code = cfi_code[0:4] + get_fifth_char_in_cfi_code_trade(acm_object) + 'X'
            cfi_code = cfi_code[0:5] + get_sixth_char_in_cfi_code_trade(acm_object)
        else:
            cfi_code = None
    return cfi_code
