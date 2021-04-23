"""-----------------------------------------------------------------------
MODULE
    ABSAPSTimeSeries

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Copies the value stored in an additional info field to a time series. 
                          This is done to store a history of the additional info values.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Micheal Klimke
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael

from at_logging import getLogger


LOGGER = getLogger()


'''================================================================================================
This script will look at the value stored in AdditionalInfo's associates with a certain database Object.
================================================================================================'''
def update_time_series(FromDate, ToDate, RecordType, AddInfos, Filter):

    while FromDate <= ToDate:   

        for AddInfo in AddInfos:  # All selected addinfo
            LOGGER.info('INFO: Update timeseries: %s', AddInfo)
            Spec = ael.AdditionalInfoSpec[AddInfo]
            for AI in ael.AdditionalInfo.select('addinf_specnbr =' + str(Spec.specnbr)):  # get All AdditionalInfo's for the current Spec
            
                EntityID = get_entity_for_addinfo(AI)  # Get the Entity that the AddInfo is attached to
                
                if '<ALL>' in Filter or (EntityID in Filter):  # Check if we are filtering 
            
                    TimeSeriesSpec = get_timeseries_spec(Spec)  # Get the TimeSeries Spec/Create it if we don't have it
                    TS = get_last_time_series(AI, TimeSeriesSpec, FromDate)
                        
                    if TS == None:  # Create time series on if one has never been created
                        TS = create_time_series(TimeSeriesSpec, FromDate, AI)

                    if TS.value != float(AI.value):  

                        # MKLIMKE Going to hace to check what data type here ? 
                        # MKLIMKE Presently will only work for float but could use it for database Primary Key
                        # print str(TS.value) + '-' + str(float(AI.value))
                    
                        if TS.day == FromDate:

                            update_single_time_series(TS, AI.value)
                        else:
                            create_time_series(TimeSeriesSpec, FromDate, AI)

        FromDate = FromDate.add_days(1)  # May want to make this business days..
'''================================================================================================
================================================================================================'''
def get_last_time_series(AddInfo, TimeSeriesSpec, aelFromDate):

    TempTimeSeries = None
    string = 'ts_specnbr = ' + str(TimeSeriesSpec.specnbr)

    for TimeSeries in ael.TimeSeries.select(string):

        if AddInfo.recaddr == TimeSeries.recaddr:
           
            if TimeSeries.day <= aelFromDate:  # If the TimeSeries is less or equal to the FromDate

          
                if TempTimeSeries == None:
                
                    TempTimeSeries = TimeSeries

                else:
                        
                    if TimeSeries.day > TempTimeSeries.day:

                        TempTimeSeries = TimeSeries
                        
    return TempTimeSeries
'''================================================================================================
================================================================================================'''
def create_time_series(TimeSeriesSpec, aelDate, AI):
    TS = ael.TimeSeries.new()
    TS.ts_specnbr = TimeSeriesSpec.specnbr
    TS.day = aelDate
    TS.value = float(AI.value)  # must sort this cant do this for anything but double
    TS.run_no = 1  # flag update number
    TS.recaddr = AI.recaddr  
    TS.commit()  
    ael.poll()
    return TS
'''================================================================================================
================================================================================================'''
def update_single_time_series(TS, Value):
    Clone = TS.clone()
    Clone.value = float(Value)
    Clone.commit()
    ael.poll()
    return TS
'''================================================================================================
================================================================================================'''
def get_timeseries_spec(AddInfoSpec):

    TimeSeriesSpec = ael.TimeSeriesSpec[AddInfoSpec.field_name]

    if TimeSeriesSpec == None:
    
        TimeSeriesSpec = ael.TimeSeriesSpec.new()
        TimeSeriesSpec.field_name = AddInfoSpec.field_name
        TimeSeriesSpec.rec_type = AddInfoSpec.rec_type
        TimeSeriesSpec.commit()
        ael.poll()

    return TimeSeriesSpec    
'''================================================================================================
================================================================================================'''
def get_entities_for_additional_infos(spec_list):
    for spec in spec_list:
        aelSpec = ael.AdditionalInfoSpec[spec]
        rectype = aelSpec.rec_type
        aiList = ael.AdditionalInfo.select('addinf_specnbr = ' + str(aelSpec.specnbr))   
        EntityList = [] 
        for AddInfo in aiList:
            EntityList.append(eval('ael.' + rectype + '[' + str(AddInfo.recaddr) + ']').display_id())
        return EntityList
'''================================================================================================
================================================================================================'''
def get_entity_for_addinfo(AddInfo):
    rectype = AddInfo.addinf_specnbr.rec_type
    Entity = eval('ael.' + rectype + '[' + str(AddInfo.recaddr) + ']').display_id()
    return Entity
'''================================================================================================
================================================================================================'''
def check_input_settings(Index, Values):
    if Index == 4:
        ael_variables[5][3] = get_additional_info_specs(Values[4])
    if Index == 5 and Values[5] != '':    
        L = Values[5].split(',')
        X = get_entities_for_additional_infos(L)
        ael_variables[6][3] = X
    return Values
'''================================================================================================
================================================================================================'''
def get_ael_variables_index_from_name(name): 
    for item in ael_variables:
        if item[0] == name:
            LOGGER.info(name)
'''================================================================================================
================================================================================================'''
def get_additional_info_specs(RecordType):
    List = []
    if RecordType != '':
        for Spec in ael.AdditionalInfoSpec.select('rec_type="' + RecordType + '"'):
            List.append(Spec.field_name)
    return List
'''================================================================================================
================================================================================================'''
def all_tables():
    retvec = []
    for x in dir(ael):
        try: 
            if isinstance(eval('ael.' + x), ael.ael_table):
                retvec.append(x)
        except: pass
    return retvec
'''================================================================================================
================================================================================================'''
INCEPTION = ael.date('1970-01-01')
TODAY = ael.date_today()
FIRSTOFYEAR = TODAY.first_day_of_year()
FIRSTOFMONTH = TODAY.first_day_of_month()
PREVBUSDAY = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)  # M.KLIMKE Should really get default calendar
TWOBUSDAYSAGO = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)  # M.KLIMKE Should really get default calendar 
TWODAYSAGO = TODAY.add_days(-2)
YESTERDAY = TODAY.add_days(-1)

StartDateList = { 'Inception':INCEPTION.to_string(ael.DATE_ISO), \
                    'First Of Year':FIRSTOFYEAR.to_string(ael.DATE_ISO), \
                    'First Of Month':FIRSTOFMONTH.to_string(ael.DATE_ISO), \
                    'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO), \
                    'TwoBusinessDaysAgo':TWOBUSDAYSAGO.to_string(ael.DATE_ISO), \
                    'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO),
                    'Yesterday':YESTERDAY.to_string(ael.DATE_ISO),
                    'Custom Date':TODAY, \
                    'Now':TODAY.to_string(ael.DATE_ISO)} 
EndDateList = { 'Now':TODAY.to_string(ael.DATE_ISO), \
                    'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO), \
                    'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO), \
                    'Yesterday':YESTERDAY.to_string(ael.DATE_ISO), \
                    'Custom Date':TODAY.to_string(ael.DATE_ISO)}

ael_variables = \
[
['startDate', 'Start Date:', 'string', StartDateList.keys(), 'Yesterday', 1, 0, None],
['startDateCustom', 'Start Date Custom:', 'string', None, StartDateList['Yesterday'], 1, 0, None],
['endDate', 'End Date:', 'string', EndDateList.keys(), 'Now', 1, 0, None],
['endDateCustom', 'End Date Custom:', 'string', None, EndDateList['Now'], 1, 0, None],
['table', 'Table:', 'string', all_tables(), None, 1, 0, None, check_input_settings],
['addInfo', 'Additional Info:', 'string', None, None, 1, 1, '', check_input_settings, 1],
['filter', 'Filter:', 'string', None, '<ALL>', 1, 1, None, check_input_settings],
]     
'''================================================================================================
================================================================================================'''
def ael_main(ael_dict):

    if ael_dict['startDate'] == 'Custom Date':
        StartDate = ael.date(ael_dict['startDateCustom'])
    else:
        StartDate = ael.date(StartDateList[ael_dict['startDate']])

    if ael_dict['endDate'] == 'Custom Date':
        EndDate = ael.date(ael_dict['endDateCustom'])
    else:
        EndDate = ael.date(EndDateList[ael_dict['endDate']])
    
    update_time_series(StartDate, EndDate, ael_dict['table'], ael_dict['addInfo'], ael_dict['filter']) 
'''================================================================================================
================================================================================================'''
def startRunScript(eii):                
    acm.RunModuleWithParameters('ABSAPSTimeSeries', acm.GetDefaultContext()) 
'''================================================================================================
================================================================================================'''
