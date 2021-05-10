import acm, ael#, SAEQ_DIVUPLOAD_TOOLS
'''
strm = ael.DividendStream['ABL1']
#divs = str.div_
growth = 10
end = ael.date('2015-01-01')
streams = ael.DividendStream.select()
for strm in streams:
    dates = []
    year = ael.date_today().to_ymd()[0]
    for i in strm.estimates():
        if i.description != 'Special':
            
            if i.ex_div_day.to_ymd()[0] > year:
                year = i.ex_div_day.to_ymd()[0]
                dates = [[i.ex_div_day,i.dividend]]
            else:
                if i.ex_div_day.to_ymd()[0] == year:
                    dates.append([i.ex_div_day,i.dividend])
                
    #print year, dates
    if len(dates) < strm.div_per_year:
        print strm.name, ':  dividends in final years: ',len(dates),'dividends per year on stream: ',  strm.div_per_year





s = 'BotsFleming,DELETE_EQ_ALSI_LONG,DELETE_EQB&S_impdiv,DELETE_EqCliquetEnd,DELETE_EqCliquetGo,DELETE_EqDoubleBarr,Delete_s,DELETE_SAEQ_ OPTS1,DELETE_SAEQ_ALSI_AV,DELETE_SAEQ_FDiv,Delete_Safex Index,Delete_Safex Op,Delete_Safex Opt,Delete_Variance,EQ_EUR,SAIRD CPI DISC+15,SAIRD CPI DISC+20,SAIRD CPI DISC+25,SAIRD CPI DISC+27,SAIRD CPI DISC+27.5,SAIRD CPI DISC+30,SAIRD CPI DISC+35,SAIRD DISC+15,SAIRD DISC+20,SAIRD DISC+25,SAIRD DISC+27,SAIRD DISC+27.5,SAIRD DISC+30,SAIRD DISC+35,SAIRD Test,SANLD EURHUF,SANLD EURPLN,SANLD GBPCHF,SANLD_SAFEX_YMAZ'

todel = s.split(',')

for cl in ael.ChoiceList:
    nm = cl.entry
    
    if nm in todel and cl.list == 'ValGroup':
        print nm
        try:
            cl.delete()
        except:
            print nm, 'Not Deleted'
'''
#SAEQ_DIVUPLOAD_TOOLS.grow_divs(10, 2020)
