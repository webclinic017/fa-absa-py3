
import acm, math, CreateHierarchyCommon

ael_variables = [['Hierarchy Name', 'Hierarchy Name', 'string', None, None, 1, 0, 'The desired name of the hierarchy and the hierarchy type.']]

__saLevelTypeChoiceListName = 'FRTB SA Level Type'

__saHierarchyColumns = [
    ['Level Type', 'RecordRef', 32, __saLevelTypeChoiceListName, 'The type describing the level'],
    ['Is Rest Bucket', 'Standard', 5, '', 'Indicates whether the bucket is a rest bucket'],
    ['Delta Shift Size', 'Standard', 4, '', 'Size of Delta shift'],
    ['Delta Risk Weight', 'Standard', 4, '', 'Risk weight of Delta'],
    ['Delta Intra Corr', 'Standard', 4, '', 'Delta correlation between elements inside a bucket'],
    ['Delta Inter Corr', 'Standard', 4, '', 'Delta correlation between buckets in a risk class'],
    ['Delta Corr Info 1', 'Standard', 4, '', 'Extra correlation info 1'],
    ['Delta Corr Info 2', 'Standard', 4, '', 'Extra correlation info 2'],
    ['Delta Corr Info 3', 'Standard', 4, '', 'Extra correlation info 3'],
    ['Vega Shift Size', 'Standard', 4, '', 'Size of Vega shift'],
    ['Vega Risk Weight', 'Standard', 4, '', 'Risk weight of Vega'],
    ['Vega Liq Horiz', 'Standard', 1, '', 'Vega liquidity horizon'],
    ['Vega Intra Corr', 'Standard', 4, '', 'Vega correlation between elements inside a bucket'],
    ['High Corr Scenario', 'Standard', 4, '', 'The high correlation scenario'],
    ['Medium Corr Scenario', 'Standard', 4, '', 'The medium correlation scenario'],
    ['Low Corr Scenario', 'Standard', 4, '', 'The low correlation scenario'],
    ['Loss Given Default', 'Standard', 4, '', 'The loss given default']
]

__saGIRRSpecialCurrencies = ['EUR', 'USD', 'GBP', 'AUD', 'JPY', 'SEK', 'CAD']
accountingCurrency = acm.UsedValuationParameters().AccountingCurrency().Name()
if accountingCurrency not in __saGIRRSpecialCurrencies:
    __saGIRRSpecialCurrencies.append(accountingCurrency)

__saGIRRWeights = [0.017, 0.017, 0.016, 0.013, 0.012, 0.011, 0.011, 0.011, 0.011, 0.011]
__saGIRRInflationAndCCWeight = 0.016

def __GirrIrBuckets():
    def __GirrIrBucket(currency, saGirrWeights):
        return [currency, {'Level Type':'Bucket', 'Delta Risk Weight':max(saGirrWeights)}, [
          ['3M', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[0]}, None],
          ['6M', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[1]}, None],
          ['1Y', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[2]}, None],
          ['2Y', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[3]}, None],
          ['3Y', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[4]}, None],
          ['5Y', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[5]}, None],
          ['10Y', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[6]}, None],
          ['15Y', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[7]}, None],
          ['20Y', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[8]}, None],
          ['30Y', {'Level Type':'Time Bucket', 'Delta Risk Weight':saGirrWeights[9]}, None]
          ]
        ]

    buckets = []
    saGirrWeightsSpecial = [x / math.sqrt(2) for x in __saGIRRWeights]
    for currency in __saGIRRSpecialCurrencies:
        buckets.append(__GirrIrBucket(currency, saGirrWeightsSpecial))
    buckets.append(__GirrIrBucket('Other Currency', __saGIRRWeights))
    return buckets

def __GirrInflationAndCrossCurrencyBuckets():
    buckets = []
    for currency in __saGIRRSpecialCurrencies:
        buckets.append([currency, {'Level Type':'Bucket', 'Delta Risk Weight':__saGIRRInflationAndCCWeight / math.sqrt(2)}, None])
    buckets.append(['Other Currency', {'Level Type':'Bucket', 'Delta Risk Weight':__saGIRRInflationAndCCWeight}, None])
    return buckets

__saHierarchy = [
  ['Standardised Approach', {}, [
    ['Sensitivities-based Method', {'Level Type':'Component', 'Vega Shift Size':0.01, 'Vega Risk Weight':0.55, 'Vega Intra Corr':0.01, 'High Corr Scenario':1.25, 'Medium Corr Scenario':1.00, 'Low Corr Scenario':0.75 }, [
      ['Commodity', {'Level Type':'Risk Class', 'Delta Shift Size':0.01, 'Delta Corr Info 1':0.99, 'Delta Corr Info 2':0.999, 'Vega Liq Horiz':120}, [
        ['1', {'Level Type':'Bucket', 'Delta Risk Weight':0.3, 'Delta Intra Corr':0.55, 'Delta Inter Corr':0.2}, None],
        ['2', {'Level Type':'Bucket', 'Delta Risk Weight':0.35, 'Delta Intra Corr':0.95, 'Delta Inter Corr':0.2}, None],
        ['3', {'Level Type':'Bucket', 'Delta Risk Weight':0.6, 'Delta Intra Corr':0.4, 'Delta Inter Corr':0.2}, None],
        ['4', {'Level Type':'Bucket', 'Delta Risk Weight':0.8, 'Delta Intra Corr':0.8, 'Delta Inter Corr':0.2}, None],
        ['5', {'Level Type':'Bucket', 'Delta Risk Weight':0.4, 'Delta Intra Corr':0.6, 'Delta Inter Corr':0.2}, None],
        ['6', {'Level Type':'Bucket', 'Delta Risk Weight':0.45, 'Delta Intra Corr':0.65, 'Delta Inter Corr':0.2}, None],
        ['7', {'Level Type':'Bucket', 'Delta Risk Weight':0.2, 'Delta Intra Corr':0.55, 'Delta Inter Corr':0.2}, None],
        ['8', {'Level Type':'Bucket', 'Delta Risk Weight':0.35, 'Delta Intra Corr':0.45, 'Delta Inter Corr':0.2}, None],
        ['9', {'Level Type':'Bucket', 'Delta Risk Weight':0.25, 'Delta Intra Corr':0.15, 'Delta Inter Corr':0.2}, None],
        ['10', {'Level Type':'Bucket', 'Delta Risk Weight':0.35, 'Delta Intra Corr':0.4, 'Delta Inter Corr':0.2}, None],
        ['11', {'Level Type':'Bucket', 'Delta Risk Weight':0.5, 'Delta Intra Corr':0.15, 'Delta Inter Corr':0.0}, None]
        ]],
      ['CSR (NS)', {'Level Type':'Risk Class', 'Delta Shift Size':0.0001, 'Delta Intra Corr':0.35, 'Delta Corr Info 1':0.65, 'Delta Corr Info 2':0.999, 'Delta Corr Info 3':0.5, 'Vega Liq Horiz':120}, [
        ['1', {'Level Type':'Bucket', 'Delta Risk Weight':0.005}, [
          ['2', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None],
          ['3', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['2', {'Level Type':'Bucket', 'Delta Risk Weight':0.01}, [
          ['3', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['3', {'Level Type':'Bucket', 'Delta Risk Weight':0.05}, [
          ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['4', {'Level Type':'Bucket', 'Delta Risk Weight':0.03}, [
          ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['5', {'Level Type':'Bucket', 'Delta Risk Weight':0.03}, [
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['6', {'Level Type':'Bucket', 'Delta Risk Weight':0.02}, [
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['7', {'Level Type':'Bucket', 'Delta Risk Weight':0.015}, [
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['8', {'Level Type':'Bucket', 'Delta Risk Weight':0.025}, [
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['9', {'Level Type':'Bucket', 'Delta Risk Weight':0.02}, [
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['10', {'Level Type':'Bucket', 'Delta Risk Weight':0.04}, [
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['11', {'Level Type':'Bucket', 'Delta Risk Weight':0.12}, [
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['12', {'Level Type':'Bucket', 'Delta Risk Weight':0.07}, [
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['13', {'Level Type':'Bucket', 'Delta Risk Weight':0.085}, [
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['14', {'Level Type':'Bucket', 'Delta Risk Weight':0.055}, [
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['15', {'Level Type':'Bucket', 'Delta Risk Weight':0.05}, [
          ['17', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
        ['16', {'Level Type':'Bucket', 'Is Rest Bucket':True, 'Delta Risk Weight':0.12}, None],
        ['17', {'Level Type':'Bucket', 'Delta Risk Weight':0.015, 'Delta Intra Corr':0.8}, [
          ['18', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None]
          ]],
        ['18', {'Level Type':'Bucket', 'Delta Risk Weight':0.05, 'Delta Intra Corr':0.8}, None]
        ]],
      ['CSR (S-C)', {'Level Type':'Risk Class', 'Delta Shift Size':0.0001, 'Delta Intra Corr':0.35, 'Delta Corr Info 1':0.65, 'Delta Corr Info 2':0.99, 'Delta Corr Info 3':0.5, 'Vega Liq Horiz':120}, [
        ['1', {'Level Type':'Bucket', 'Delta Risk Weight':0.04}, [
          ['2', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None],
          ['3', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None]
          ]],
        ['2', {'Level Type':'Bucket', 'Delta Risk Weight':0.04}, [
          ['3', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None]
          ]],
        ['3', {'Level Type':'Bucket', 'Delta Risk Weight':0.08}, [
          ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['4', {'Level Type':'Bucket', 'Delta Risk Weight':0.05}, [
          ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['5', {'Level Type':'Bucket', 'Delta Risk Weight':0.04}, [
          ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['6', {'Level Type':'Bucket', 'Delta Risk Weight':0.03}, [
          ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['7', {'Level Type':'Bucket', 'Delta Risk Weight':0.02}, [
          ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':1.0}, None]
          ]],
        ['8', {'Level Type':'Bucket', 'Delta Risk Weight':0.06}, [
          ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['9', {'Level Type':'Bucket', 'Delta Risk Weight':0.13}, [
          ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None],
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None]
          ]],
        ['10', {'Level Type':'Bucket', 'Delta Risk Weight':0.13}, [
          ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.1}, None]
          ]],
        ['11', {'Level Type':'Bucket', 'Delta Risk Weight':0.16}, [
          ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None],
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['12', {'Level Type':'Bucket', 'Delta Risk Weight':0.1}, [
          ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.2}, None],
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['13', {'Level Type':'Bucket', 'Delta Risk Weight':0.12}, [
          ['14', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.25}, None],
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['14', {'Level Type':'Bucket', 'Delta Risk Weight':0.12}, [
          ['15', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.05}, None]
          ]],
        ['15', {'Level Type':'Bucket', 'Delta Risk Weight':0.12}, None],
        ['16', {'Level Type':'Bucket', 'Is Rest Bucket':True, 'Delta Risk Weight':0.13}, None]
        ]],
      ['Equity', {'Level Type':'Risk Class', 'Delta Corr Info 1':0.999, 'Delta Corr Info 2':0.999}, [
        ['Spot Price', {'Level Type':'Subtype', 'Delta Shift Size':0.01}, [
          ['1', {'Level Type':'Bucket', 'Delta Risk Weight':0.55, 'Delta Intra Corr':0.15, 'Vega Liq Horiz':20}, [
            ['2', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['3', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['2', {'Level Type':'Bucket', 'Delta Risk Weight':0.6, 'Delta Intra Corr':0.15, 'Vega Liq Horiz':20}, [
            ['3', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['3', {'Level Type':'Bucket', 'Delta Risk Weight':0.45, 'Delta Intra Corr':0.15, 'Vega Liq Horiz':20}, [
            ['4', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['4', {'Level Type':'Bucket', 'Delta Risk Weight':0.55, 'Delta Intra Corr':0.15, 'Vega Liq Horiz':20}, [
            ['5', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['5', {'Level Type':'Bucket', 'Delta Risk Weight':0.3, 'Delta Intra Corr':0.25, 'Vega Liq Horiz':20}, [
            ['6', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['6', {'Level Type':'Bucket', 'Delta Risk Weight':0.35, 'Delta Intra Corr':0.25, 'Vega Liq Horiz':20}, [
            ['7', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['7', {'Level Type':'Bucket', 'Delta Risk Weight':0.4, 'Delta Intra Corr':0.25, 'Vega Liq Horiz':20}, [
            ['8', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['8', {'Level Type':'Bucket', 'Delta Risk Weight':0.5, 'Delta Intra Corr':0.25, 'Vega Liq Horiz':20}, [
            ['9', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['9', {'Level Type':'Bucket', 'Delta Risk Weight':0.7, 'Delta Intra Corr':0.075, 'Vega Liq Horiz':60}, [
            ['10', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.15}, None],
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['10', {'Level Type':'Bucket', 'Delta Risk Weight':0.5, 'Delta Intra Corr':0.125, 'Vega Liq Horiz':60}, [
            ['11', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.0}, None],
            ['12', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None],
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.45}, None]
          ]],
          ['11', {'Level Type':'Bucket', 'Is Rest Bucket':True, 'Delta Risk Weight':0.7, 'Delta Intra Corr':0.0, 'Delta Inter Corr':0.0, 'Vega Liq Horiz':60}, None],
          ['12', {'Level Type':'Bucket', 'Delta Risk Weight':0.15, 'Delta Intra Corr':0.8, 'Vega Liq Horiz':20}, [
            ['13', {'Level Type':'Correlation Bucket', 'Delta Inter Corr':0.75}, None]
          ]],
          ['13', {'Level Type':'Bucket', 'Delta Risk Weight':0.25, 'Delta Intra Corr':0.8, 'Vega Liq Horiz':20}, None]
          ]],
        ['Repo Rate', {'Level Type':'Subtype', 'Delta Shift Size':0.0001}, [
          ['1', {'Level Type':'Bucket', 'Delta Risk Weight':0.0055, 'Delta Intra Corr':0.15, 'Vega Liq Horiz':20}, None],
          ['2', {'Level Type':'Bucket', 'Delta Risk Weight':0.006, 'Delta Intra Corr':0.15, 'Vega Liq Horiz':20}, None],
          ['3', {'Level Type':'Bucket', 'Delta Risk Weight':0.0045, 'Delta Intra Corr':0.15, 'Vega Liq Horiz':20}, None],
          ['4', {'Level Type':'Bucket', 'Delta Risk Weight':0.0055, 'Delta Intra Corr':0.15, 'Vega Liq Horiz':20}, None],
          ['5', {'Level Type':'Bucket', 'Delta Risk Weight':0.003, 'Delta Intra Corr':0.25, 'Vega Liq Horiz':20}, None],
          ['6', {'Level Type':'Bucket', 'Delta Risk Weight':0.0035, 'Delta Intra Corr':0.25, 'Vega Liq Horiz':20}, None],
          ['7', {'Level Type':'Bucket', 'Delta Risk Weight':0.004, 'Delta Intra Corr':0.25, 'Vega Liq Horiz':20}, None],
          ['8', {'Level Type':'Bucket', 'Delta Risk Weight':0.005, 'Delta Intra Corr':0.25, 'Vega Liq Horiz':20}, None],
          ['9', {'Level Type':'Bucket', 'Delta Risk Weight':0.007, 'Delta Intra Corr':0.075, 'Vega Liq Horiz':60}, None],
          ['10', {'Level Type':'Bucket', 'Delta Risk Weight':0.005, 'Delta Intra Corr':0.125, 'Vega Liq Horiz':60}, None],
          ['11', {'Level Type':'Bucket', 'Is Rest Bucket':True, 'Delta Risk Weight':0.007, 'Delta Intra Corr':0.0, 'Vega Liq Horiz':60}, None],
          ['12', {'Level Type':'Bucket', 'Delta Risk Weight':0.0015, 'Delta Intra Corr':0.8, 'Vega Liq Horiz':20}, None],
          ['13', {'Level Type':'Bucket', 'Delta Risk Weight':0.0025, 'Delta Intra Corr':0.8, 'Vega Liq Horiz':20}, None]
          ]],
        ]],
      ['FX', {'Level Type':'Risk Class', 'Delta Shift Size':0.01, 'Delta Intra Corr':0.6, 'Vega Liq Horiz':40}, [
        ['All', {'Level Type':'Bucket'}, [
          ['USD/EUR', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/JPY', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/GBP', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/AUD', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/CAD', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/CHF', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/MXN', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/CNY', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/NZD', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/RUB', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/HKD', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/SGD', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/TRY', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/KRW', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/SEK', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/ZAR', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/INR', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/NOK', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['USD/BRL', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['EUR/JPY', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['EUR/GBP', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['EUR/CHF', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['JPY/AUD', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15 / math.sqrt(2)}, None],
          ['Other Currency Pair', {'Level Type':'Currency Pair', 'Delta Risk Weight':0.15}, None]
          ]],
        ]],
      ['GIRR', {'Level Type':'Risk Class', 'Delta Shift Size':0.0001, 'Delta Inter Corr':0.5, 'Vega Liq Horiz':60}, [
        ['Interest Rate', {'Level Type':'Subtype', 'Delta Intra Corr':0.999, 'Delta Corr Info 1':0.03, 'Delta Corr Info 2':0.4}, __GirrIrBuckets()],
        ['Inflation', {'Level Type':'Subtype', 'Delta Intra Corr':0.4}, __GirrInflationAndCrossCurrencyBuckets()],
        ['Cross Currency Basis', {'Level Type':'Subtype', 'Delta Intra Corr':0.0}, __GirrInflationAndCrossCurrencyBuckets()],
        ]],
      ]],
    ['Default Risk Charge', {'Level Type':'Component'}, [
      ['Risk Weights', {}, [
        ['AAA', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':0.005}, None],
        ['AA', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':0.02}, None],
        ['A', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':0.03}, None],
        ['BBB', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':0.06}, None],
        ['BB', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':0.15}, None],
        ['B', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':0.3}, None],
        ['CCC', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':0.5}, None],
        ['Unrated', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':0.15}, None],
        ['Defaulted', {'Level Type':'Credit Quality Category', 'Delta Risk Weight':1.0}, None]
      ]],
      ['Loss Given Default', {}, [
        ['Equity/Non-Senior Debt', {'Level Type':'Seniority', 'Loss Given Default':1.0}, None],
        ['Senior Debt', {'Level Type':'Seniority', 'Loss Given Default':0.75}, None],
        ['Covered Bonds', {'Level Type':'Seniority', 'Loss Given Default':0.25}, None],
        ['Other', {'Level Type':'Seniority', 'Loss Given Default':0.0}, None]
      ]]
    ]],
    ['Residual Risk Add-On', {'Level Type':'Component'}, [
      ['Exotic', {'Level Type':'Residual Risk Type', 'Delta Risk Weight':0.01}, None],
      ['Other', {'Level Type':'Residual Risk Type', 'Delta Risk Weight':0.001}, None],
      ['None', {'Level Type':'Residual Risk Type', 'Delta Risk Weight':0.0}, None]
      ]]
    ]]
  ]

def ael_main(parameters):
    choiceList = acm.FChoiceList.Select01('name="' + __saLevelTypeChoiceListName + '" list="MASTER"', '')
    createChoiceList = None == choiceList
    if createChoiceList:
        choiceList = CreateHierarchyCommon.CreateNewChoiceList(__saLevelTypeChoiceListName, 'MASTER')
        CreateHierarchyCommon.CreateNewChoiceList('Risk Class', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Bucket', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Subtype', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Time Bucket', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Correlation Bucket', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Currency Pair', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Component', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Credit Quality Category', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Seniority', __saLevelTypeChoiceListName)
        CreateHierarchyCommon.CreateNewChoiceList('Residual Risk Type', __saLevelTypeChoiceListName)

    ctxt = acm.ExtensionTools().GetDefaultContext()
    hTypeExt = ctxt.GetExtension('FExtensionValue', 'FObject', 'FRTBSAHierarchyType')
    if hTypeExt:
        hierarchyType = CreateHierarchyCommon.CreateHierarchyType(hTypeExt.Value(), __saHierarchyColumns)
        CreateHierarchyCommon.CreateHierarchy(hierarchyType, parameters['Hierarchy Name'], __saHierarchy, createChoiceList, __saLevelTypeChoiceListName)
    else:
        errorMessage = 'No hierarchy type found for FRTBSAHierarchyType'
        print (errorMessage)
