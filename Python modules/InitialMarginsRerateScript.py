import acm, ael
import xml.dom.minidom as xml

ael_gui_parameters = { 'windowCaption':'InitialMarginsRerateScript'}
ael_variables = []

def getEnvironment():
        arenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort()

        arenaDataServer = arenaDataServer.lower()

        environmentSettings = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, 'EnvironmentSettings')
        environmentSetting = xml.parseString(environmentSettings)
        host = environmentSetting.getElementsByTagName('Host')
        environment = [e for e in host if e.getAttribute('Name').lower() == arenaDataServer]

        if len(environment) != 1:
            print ('ERROR: Could not find environment settings for %s.' % arenaDataServer)
            raise Exception('ERROR: Could not find environment settings for %s.' % arenaDataServer)

        return str(environment[0].getAttribute('Setting'))


def ael_main(dictionary):

    environment_map = {'DE':'Development','PR':'Live','UA':'UserTesting','DR':'DisasterRecovery'}

    environment = environment_map[getEnvironment()[0:2]]

    print 'Rerating started...'

    result_set = ael.asql(acm.FSQL['InitialMarginsQuery'].Text())

    trdList = result_set[1][0]
    
    print 'Trades:', trdList

    for trdOid in trdList:

        trdOid = trdOid[0] 
       
        print 'Processing trade:%s'%trdOid
        
        trd = acm.FTrade[trdOid]
        
        if environment != 'Live':
            print 'FO Confirming trade.'
            trd.Status('FO Confirmed')
                
        date = ael.date_today()

        print 'Rerate date:%s'%date
        
        ins = trd.Instrument()
        
        ael_ins = ael.Instrument[ins.Oid()]
        
        try:
            ael_ins.re_rate(date, 0)
        except :
            print 'Cant rerate'

        try:
            trd.Commit()
        except Exception, e:
            print 'Failed to commit:%s:,%s'%(trdOid, e)
        print trd.Status()
        print '----------------------------------------------------------------------------------'
    print 'Rerating complete...'
