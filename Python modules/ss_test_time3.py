import acm, time, ael, datetime

def do_it():
    print '------------'
    print   '%-30s %s' % ('acm.DateToday()', acm.DateToday())
    print   '%-30s %s' % ('acm.Time.TimeNow()', acm.Time.TimeNow())
    print   '%-30s %s' % ('time.ctime()', time.ctime())
    print   '%-30s %s' % ('ael.date_today()', ael.date_today())
    print   '%-30s %s' % ('datetime.datetime.now()', datetime.datetime.now())
    print   '%-30s %s' % ('datetime.datetime.utcnow() ', datetime.datetime.utcnow() )
    print '-------------'

    t=acm.FTrade[4453533]
    for column_id in ['Valuation Date', 'Portfolio Profit Loss Price End Date']:

         context = acm.GetDefaultContext()
         sheet_type = 'FTradeSheet'
         calc_space = acm.Calculations().CreateCalculationSpace( context, sheet_type )
         value = calc_space.CalculateValue( t, column_id )
         print '%-30s %s' % (column_id, str(value))

    print '-----'

    for attr in ['valuationDateTimeExtact', 'valuationDateTimeOriginal', 'valuationDateTime']:
         tag = acm.CreateEBTag()
         v = acm.GetCalculatedValueFromString(t, 'Standard', 'object:*"%s"'%attr, tag)
         print '%-30s %s' % (attr, str(v.Value()))

ael_variables=[]

def ael_main(dict):
    cnt=1
    while True:
        do_it()
        time.sleep(cnt)
        cnt+=5

