
import FFxSpotRolloverSwapFunding, FBDPGui

#ScriptName = 'FxSpotRolloverSwapFunding'
#FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters','FFxPositionRollover')

def customPortDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrpairPortCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def customAcqDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrpairAcqCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

def customInstDialog(shell, params):
    customDlg = FBDPCustomPairDlg.SelectCurrpairInstCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)


ttPortfolioMap = ('Select specific funding portfolios for currency pairs '
        '(select \'CurrencyPair:Portfolio\' pairs from list).')
ttAcquirerMap = ('Select specific funding acquirers for currency pairs '
        '(select \'CurrencyPair:Acquirer\' pairs from list)')
ttFundingMap = ('Select specific funding instruments for currency pairs '
        '(select \'CurrencyPair:Instrument\' pairs from list).  '
        'Default instrument is HISTORICAL_FINANCING.')
ttFundingIns = ('Specify FX swap instruments holding swap points for '
        'overnight, tom next and spot next positions.')
ttDefaultPortfolio = ('Select a default funding portfolio '
        '(only used if no other portfolio is assigned to a currency pair')
ttDefaultAcquirer = ('Select a default funding acquirer '
        '(only used if no other acquirer is assigned to a currency pair)')

xxx = FBDPGui.FxVariables(
['MappedPortfolios', 'Funding portfolios for currency pairs', 'string', [], None, 0, 1, ttPortfolioMap, None, 1, customPortDialog],
['MappedAcquirers', 'Funding acquirers for currency pairs', 'string', [], None, 0, 1, ttAcquirerMap, None, 1, customAcqDialog],
['MappedFundingInstruments', 'Funding instruments for currency pairs_Rates', 'string', [], None, 0, 1, ttFundingMap, None, 1, customInstDialog],
['FundingInstruments', 'Funding instruments_Rates', 'FFxSwap', [], None, 0, 1, ttFundingIns, None, 1, None],
['DefaultPortfolio', 'Default funding portfolio', 'FPhysicalPortfolio', None, FBDPGui.insertPhysicalPortfolio(), 2, 1, ttDefaultPortfolio],
['DefaultAcquirer', 'Default funding acquirer', 'FParty', None, FBDPGui.insertAcquirer(), 2, 1, ttDefaultAcquirer])

print len(xxx)
newlist = ','.join([x[0] for x in xxx])

print newlist
#FBDPGui.ael_main()
