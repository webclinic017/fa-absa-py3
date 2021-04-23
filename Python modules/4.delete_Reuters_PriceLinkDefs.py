import acm

delete_list = (
'BWP-USD/FXS/GEN/12M',
'BWP-USD/FXS/GEN/1M',
'BWP-USD/FXS/GEN/1WK',
'BWP-USD/FXS/GEN/2M',
'BWP-USD/FXS/GEN/2Y',
'BWP-USD/FXS/GEN/3M',


'BWP-USD/FXS/GEN/6M',
'BWP-USD/FXS/GEN/9M',
'NZD-USD/FXS/GEN/1M',
'NZD-USD/FXS/GEN/1W',
'NZD-USD/FXS/GEN/1Y',
'NZD-USD/FXS/GEN/2M',
'NZD-USD/FXS/GEN/2Y',
'NZD-USD/FXS/GEN/3M',



'NZD-USD/FXS/GEN/6M',
'NZD-USD/FXS/GEN/9M',

'USD-CAD/FXS/GEN/1M',
'USD-CAD/FXS/GEN/1W',
'USD-CAD/FXS/GEN/1Y',
'USD-CAD/FXS/GEN/2M',
'USD-CAD/FXS/GEN/2Y',
'USD-CAD/FXS/GEN/3M',



'USD-CAD/FXS/GEN/6M',
'USD-CAD/FXS/GEN/9M',

'USD-CAD/FXS/GEN/TN',
'USD-CHF/FXS/GEN/1M',
'USD-CHF/FXS/GEN/1Y',
'USD-CHF/FXS/GEN/2M',
'USD-CHF/FXS/GEN/2Y',
'USD-CHF/FXS/GEN/3M',
'USD-CHF/FXS/GEN/6M',
'USD-CHF/FXS/GEN/9M',
'USD-CNH/FXS/GEN/1M',
'USD-CNH/FXS/GEN/1W',
'USD-CNH/FXS/GEN/2M',
'USD-CNH/FXS/GEN/2W',
'USD-CNH/FXS/GEN/3M',
'USD-CNH/FXS/GEN/6M',



'USD-INR/FXS/GEN/1M',
'USD-INR/FXS/GEN/1W',

'USD-INR/FXS/GEN/2M',
'USD-INR/FXS/GEN/3M',
'USD-INR/FXS/GEN/6M',
'USD-INR/FXS/GEN/9M',
'USD-KES/FXS/0D-12M/',
'USD-KES/FXS/0D-1M/',
'USD-KES/FXS/0D-1W',
'USD-KES/FXS/0D-2M/',
'USD-KES/FXS/0D-2Y/',
'USD-KES/FXS/0D-3M',


'USD-KES/FXS/0D-6M/',
'USD-KES/FXS/0D-9M/',

'USD-KWD/FXS/GEN/1M',

'USD-KWD/FXS/GEN/1y',
'USD-KWD/FXS/GEN/2M',
'USD-KWD/FXS/GEN/2y',
'USD-KWD/FXS/GEN/3M',
'USD-KWD/FXS/GEN/6M',
'USD-KWD/FXS/GEN/9M',
'USD-MUR/FXS/0Y-1M',
'USD-MUR/FXS/0Y-2m',
'USD-MUR/FXS/0Y-3M',
'USD-MUR/FXS/GEN/12M',
'USD-MUR/FXS/GEN/1W',
'USD-MUR/FXS/GEN/6M',
'USD-MUR/FXS/GEN/9M',


















'USD-NGN/FXS/12M',
'USD-NGN/FXS/GEN/1M',
'USD-NGN/FXS/GEN/2M',
'USD-NGN/FXS/GEN/2Y',
'USD-NGN/FXS/GEN/3M',


'USD-NGN/FXS/GEN/6M',
'USD-NGN/FXS/GEN/9M',

'USD-NGN/FXS/GEN/TN',









'USD-QAR/FXS/GEN/1M',
'USD-QAR/FXS/GEN/1W',
'USD-QAR/FXS/GEN/1Y',
'USD-QAR/FXS/GEN/2M',

'USD-QAR/FXS/GEN/3M',
'USD-QAR/FXS/GEN/6M',
'USD-QAR/FXS/GEN/9M',





















'USD-THB/FXS/GEN/1M',
'USD-THB/FXS/GEN/1W',
'USD-THB/FXS/GEN/1Y',
'USD-THB/FXS/GEN/2M',
'USD-THB/FXS/GEN/3M',
'USD-THB/FXS/GEN/6M',
'USD-THB/FXS/GEN/9M',

'USD-TRY/FXS/GEN/1M',
'USD-TRY/FXS/GEN/1WK',
'USD-TRY/FXS/GEN/1Y',
'USD-TRY/FXS/GEN/2M',
'USD-TRY/FXS/GEN/2Y',
'USD-TRY/FXS/GEN/3M',

'USD-TRY/FXS/GEN/6M',
'USD-TRY/FXS/GEN/9M',
'USD-UGX/FXS/0Y-1w/',
'USD-UGX/FXS/GEN/12M',
'USD-UGX/FXS/GEN/1M',
'USD-UGX/FXS/GEN/2M',
'USD-UGX/FXS/GEN/3M',
'USD-UGX/FXS/GEN/6M',
'USD-UGX/FXS/GEN/9M',
'USD-ZAR/FXS/GEN/15M',
'USD-ZAR/FXS/GEN/18M',
'USD-ZAR/FXS/GEN/1M',
'USD-ZAR/FXS/GEN/1WK',
'USD-ZAR/FXS/GEN/1Y',
'USD-ZAR/FXS/GEN/21M',
'USD-ZAR/FXS/GEN/2M',
'USD-ZAR/FXS/GEN/2WK',
'USD-ZAR/FXS/GEN/2Y',
'USD-ZAR/FXS/GEN/3M',
'USD-ZAR/FXS/GEN/3WK',

'USD-ZAR/FXS/GEN/6M',
'USD-ZAR/FXS/GEN/9M',

'USD-ZAR/FXS/GEN/SN',
'USD-ZAR/FXS/GEN/TN')

to_delete = []


PLDs = acm.FPriceLinkDefinition.Select('')
print('before - total number of price link definitions = ', len(PLDs))
a = len(PLDs)

for PLD in PLDs:
    if PLD.PriceDistributor().Name() == 'REUTERS_FEED':
        if PLD.Instrument().InsType() == 'FxSwap' and PLD.Market().Name()=='SPOT':
            if PLD.Instrument().Generic():
                if PLD.Instrument().Name() in delete_list:
                    to_delete.append(PLD.Oid())
                
to_delete = tuple(to_delete)

if len(to_delete)<=118:
    for p in to_delete:
        if acm.FPriceLinkDefinition[p]:
            acm.FPriceLinkDefinition[p].Delete()
        



after_PLDs = acm.FPriceLinkDefinition.Select('')
print('after - total number of price link definitions = ', len(after_PLDs))
b = len(after_PLDs)

print('number of PLDs deleted (should be 118) = ', a-b)


