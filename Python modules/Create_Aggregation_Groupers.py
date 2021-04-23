import acm

list = ['Agg_Default', 'Agg_Default_InsOverride', 'Agg_Default_IssuerSector', 'Agg_Default_OpenEnd', 'Agg_Default_Underlying_OTC', 'Agg_Default_Underlying_OTC_InsOverride', 'Agg_InsTypePrfCpty', 'Agg_InsType_CcyPair_Prf', 'PortfolioCurrPairInsOverrideMSI', 'PortfolioCurrPairMSI', 'RootPrfInsTypeCptyMirPrf', 'RootPrfInsTypeInsOverCptyMirPrf']

for group in list:
    grouper = acm.FStoredPortfolioGrouper.Select01('name=%s' %group, '')

    newGrouper = grouper.Clone()
    try:
        newGrouper.Commit()
    except Exception, e:
        print group, str(e)

