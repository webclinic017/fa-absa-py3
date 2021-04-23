import ael, TMS_Recon_Extract, TMS_Functions

Date = '2008-07-07'
Srv = 'C:\\'
TradeFilter = 'TMS_Trades_Recon'

TMS_Recon_Extract.ael_main({'ReportDate': Date,'Server': Srv,'TradeFilter':TradeFilter})


'''
Trd = ael.Trade[1520457]

print TMS_Functions.Get_Trade_TMS_ID(Trd,1)
print TMS_Functions.Get_Trade_TMS_ID(Trd,2)
'''

