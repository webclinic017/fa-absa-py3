import acm


portfolios = ['40592',
'41020',
'41046',
'41053',
'41079_RAFRES',
'41087_RAFIND',
'41095_RAFFIN',
'Mapps Growth 41129',
'Mapps Protector 41137',
'NewFunds Equity Momentum ETF',
'NewFunds GOVI ETF',
'NewFunds ILBI ETF',
'NewFunds SWIX 40 ETF',
'NewFunds Tradable Money Market Index ET',
'43083',
'43067 EQ_SA_Pairs',
'45005',
'45039',
'45088 MSCI',
'45112 USD Breakable SS',
'45146 ZAR Breakable SS',
'45153 SSF1',
'45161 SSF2',
'45195 Bespoke Structures',
'Delta One 2 45070',
'42002',
'46136',
'42010 Straddles',
'42036 Single Stock Hedge',
'46094 Delta Hedge Exotics',
'Corporate/Hedge',
'Exotics',
'Vanilla',
'46003',
'46029',
'46078',
'46128',
'47373',
'43117 EQ_SA_PairsOption',
'46037 EQ_SS_Directional',
'46052 Book Build',
'48363 Index Flow',
'44081',
'44032 - LEIPs',
'44040 - Oasis',
'40659_Syndicate trades',
'40147',
'40188',
'40196',
'40238',
'40246',
'40428',
'40436',
'40584',
'40865',
'41012',
'41038',
'41111',
'41210',
'47258',
'60574']

for portfolio in portfolios:
    acm_portfolio =  acm.FPhysicalPortfolio[portfolio]
    
    if acm_portfolio is not None:
        try:
            acm_portfolio.AdditionalInfo().RTMRestricted('Yes')
            acm_portfolio.Commit()
            print('%s marked as an RTM resctriced portfolio' %acm_portfolio.Name())
        except Exception as e:
            
            print('Failed to commit RTM changes for portfolio %s' %acm_portfolio.Name())
    else:
        print('Error: %s - No acm object exist' %portfolio)
    
