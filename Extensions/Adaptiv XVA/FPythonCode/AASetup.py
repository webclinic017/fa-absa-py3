""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AASetup.py"
import acm
import CVASetup
import AAParamsAndSettingsHelper
logger = AAParamsAndSettingsHelper.getAdaptivAnalyticsLogger()

def CreateChoiceListItem( name, list ):

    try:
        query = "name='%s' and list='%s'" % ( name, list )
        choiceList = acm.FChoiceList.Select01( query, 'Error using query %s' % query )
        
        if choiceList:
            logger.LOG('Choice %s in choice list %s already exists.' % ( choiceList.Name(), choiceList.List() ))
        else:
            choiceList = acm.FChoiceList( name=name, list=list )
            choiceList.Commit()
            logger.LOG('Created choice %s in choice list %s.' % ( choiceList.Name(), choiceList.List() ))
    except Exception as e:
        logger.ELOG('Failed to create choice %s in choice list %s: %s' % (name, list, e))
        
    return

def Setup():
    
    # ADAPTIV ANALYTICS VALUATION EXTENSIONS
    CreateChoiceListItem( name='Valuation Extension',               list='MASTER'              )
    CreateChoiceListItem( name='modelDescriptionAdaptivCVA',        list='Valuation Extension' )
    CreateChoiceListItem( name='modelDescriptionAdaptivCVAWWR',     list='Valuation Extension' )
    CreateChoiceListItem( name='xVACalculationType',                list='MASTER'              )
    CreateChoiceListItem( name='CVA',                               list='xVACalculationType'  )
    CreateChoiceListItem( name='CVA WWR',                           list='xVACalculationType'  )
    CreateChoiceListItem( name='FVA',                               list='xVACalculationType'  )
    
    # CVA COMMON
    CVASetup.Setup()
