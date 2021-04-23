import ael, SAGEN_str_functions, time, TMS_Functions, SAGEN_Functions

'''------------------------------------------------------------------------------
Create Date:    2008-06-03

Developer:      Neil Retief

Description:    This AEL will check for expired trades on the day, if the trade expires today it will go into an expired state

---------------------------------------------------------------------------------'''

def ael_main(ael_dict):

    ReportDate = ael_dict["ReportDate"]
    TradeFilter = ael_dict["TradeFilter"]

    TMS_Send_Trade(1, TradeFilter, ReportDate)
    
ael_variables = [('ReportDate', 'ReportDate', 'date', None, ael.date_today().add_days(-1), 1),
                  ('TradeFilter', 'TradeFilter', 'string', None, 'TMS_NLDIR_Opt', 1)]

def TMS_Send_Trade(temp,TrdFilter,ReportDate,*rest):

    #Get todays date
    Timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print 'Touching trades with timestamp: %s' % Timestamp

    #Run through all the trades in the filter
    for t in ael.TradeFilter[TrdFilter].trades():

        #Get the trade and instrument objects
        TObject = ael.Trade[(int)(t.trdnbr)]
        IObject = ael.Instrument[TObject.insaddr.insaddr]
    
        #Check whether the trade should be sent through
        if TMS_Functions.TMS_Filter(TObject, IObject) == 1 and t.insaddr.exp_day == ReportDate:

            try:
                SAGEN_Functions.set_trade_addinf(t, 'TMS_Gen_Message', Timestamp)
                print 'Trade sent through to TMS: %s' % t.trdnbr
                
            except:
                print 'Trade cannot be updated: %s' % t.trdnbr
