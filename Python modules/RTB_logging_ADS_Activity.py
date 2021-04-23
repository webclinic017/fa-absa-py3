"""Module to log ADS activity. The purpose of the monitoring to is to determine
    what db updates might be floading the ADS at what times during the day.
    
    2019-09-06  Jaco Swanepoel
"""

import acm
import ael
import Queue
import time
import datetime
import at_time
import csv
import FBDPCommon


#List of DB tales to monitor
subscription_list = (ael.DividendEstimate,
                    ael.Dividend,
                    ael.DividendStream,
                    ael.Trade,
                    ael.Instrument,
                    ael.Price,
                    ael.YieldCurve,
                    ael.YieldCurvePoint,
                    ael.VolPoint,
                    ael.VolatilitySkew,
                    ael.Volatility,
                    ael.TimeSeries,
                    ael.TimeSeriesDv,
                    ael.Settlement,
                    ael.Party,
                    ael.Confirmation,
                    ael.TextObject)
 
#Output settings
output = {'file': False,
            'db': True,
            'standard_log': False}
 
#Event queue
entityActionQueue = Queue.Queue()
 
  
if output['db'] == True:
    try:
        import pyodbc
    except Exception, ex:
        print('Failed to load pyodbc.', ex)
        raise
 
   
#Date & time formatting
def format_hour_bucket(entity_create_time):
    '''Extract the hour from the time
    '''
    hour = entity_create_time.hour
    return '{0}'.format(hour, hour + 1)
   
def format_minute_bucket(entity_create_time):
    '''Extract the 10min time bucket for the time param
    '''
    minute = (entity_create_time.minute / 10)*10
    minute_bucket_high_value = minute + 10 if minute < 60 else minute
    return '{0}-{1}'.format(minute, minute_bucket_high_value)
 

           
def ads_event_handler(obj, entity, arg, operation):
    '''Event handler for db object events
    '''
    
    
    entity_id = 0
    entity_record_type = ''
    entity_update_user = ''
    
    if entity:
        try:
            entity_record_type = entity.record_type
            entity_update_user = entity.updat_usrnbr.userid
            
            obj = FBDPCommon.ael_to_acm(entity)
            entity_id = obj.Oid()
            
        except:
            print('ERROR converting entity to ACM:', ael_obj)
    
    #update_time = at_time.to_datetime(obj.UpdateTime())
    update_time = at_time.to_datetime(datetime.datetime.now())
    hour_bucket = format_hour_bucket(update_time)
    minute_bucket = format_minute_bucket(update_time)
    
    event_details = "'{0}','{1}',{2},'{3}','{4}','{5}',{6},'{7}'".format(entity_record_type, operation, entity_id, entity_update_user, update_time.date(), update_time, hour_bucket, minute_bucket)
    
    
    
    #Add events into queue for processing
    entityActionQueue.put(event_details)
       
    #If the code is run from a PRIME session, manually
    # invoke the work function. Not ideal for high volume events.
    if str(acm.ObjectServer().Class()) == 'acm.FTmServer':
        work()

     
        
            
def start():
    '''ATS start
    '''
    
    #Add subscriptions
    for subscription_type in subscription_list:
        subscription_type.subscribe(ads_event_handler, None)
    
    
    
def stop():
    '''ATS stop
    '''
    
    #Remove subscriptions
    for subscription_type in subscription_list:
        subscription_type.unsubscribe(ads_event_handler)
    
    
def work():
    '''ATS work function
    '''
 
    #Create and open DB connection for logging
    if output['db'] == True:
        conn = pyodbc.connect('DRIVER={SQL Server};'
                              'Server=.\SQL2012;'
                              'Database=AdsActivityLog;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        
    
    if output['file'] == True:
        csv_file = 'C:\Temp\ADS_event_log.csv'
        list_of_events = []

    
    #Process event queue 
    while entityActionQueue.qsize() > 0:
        #ael_obj, operation = entityActionQueue.get(False)
        event_details = entityActionQueue.get(False)
        
        
        if output['db'] == True:
            sql_string =  """INSERT INTO [dbo].[FrontDBActivityLog]
                            ([Entity],[Operation],[Oid],[UpdateUser],[UpdateDate],[UpdateTime],[UpdateHour],[UpdateMinuteBucket])
                            VALUES
                            ({0})"""\
                            .format(event_details)
     
            #write to DB
            try:
                cursor.execute(sql_string)
                conn.commit()
            except Exception, ex:
                print('Error writing to SQL:', ex)
                print(sql_string)
                
                
        #Print to log
        if output['standard_log'] == True:
            print(event_details)
            
        #build csv file output 
        if output['file'] == True:
            list_of_events.append('[,]'.join(event_details))
       
    
    #write block to CSV
    if output['file'] == True:
        with open(csv_file, 'a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            
            for line in list_of_events:
                csv_writer.writerow(line)
       
       
    #close DB connection
    if output['db'] == True:
        conn.close()
    
    #take a breather
    time.sleep(3)



#If manually executed from PRIME, kick of the start manually
if str(acm.ObjectServer().Class()) == 'acm.FTmServer':
    start()
