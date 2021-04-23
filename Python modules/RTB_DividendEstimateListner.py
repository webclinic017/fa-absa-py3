import acm
import Queue
import time
import at_time

divEstimateQueue = Queue.Queue()

def format_hour_bucket(entity_create_time):
    hour = entity_create_time.hour
    return '{0}'.format(hour, hour + 1)
    
def format_minute_bucket(entity_create_time):
    minute = (entity_create_time.minute / 10)*10
    minute_bucket_high_value = minute + 10 if minute < 60 else minute
    return '{0}-{1}'.format(minute, minute_bucket_high_value)


class UpdateHandler(object):
    def ServerUpdate(self, subscribed, operation, obj):
        del subscribed
        
        update_time = at_time.to_datetime(obj.UpdateTime())
        hour_bucket = format_hour_bucket(update_time)
        minute_bucket = format_minute_bucket(update_time)
        
        print('{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|'.format(operation, obj.ClassName(), obj.Oid(), obj.UpdateUser().Name(), obj.UpdateDay(), update_time, hour_bucket, minute_bucket))
        
        #if str(operation) in ['insert', 'remove', 'update']:
        #    divEstimateQueue.put((obj, operation))
            
            
def start():

    objSubscription = acm.FDividendEstimate.Select('')  
    objUpdateHandler = UpdateHandler()
    objSubscription.AddDependent(objUpdateHandler)
    
    
def stop():
    objSubscription = acm.FDividendEstimate.Select('')  
    objUpdateHandler = UpdateHandler()
    objSubscription.RemoveDependent(objUpdateHandler)
    
    
def work():
    while divEstimateQueue.qsize() > 0:
        obj, operation = divEstimateQueue.get(False)
        
        print('{0}|{1}|{2}|{3}|{4}'.format(operation, obj.Oid(), obj.UpdateUser().Name(), obj.UpdateDay(), obj.UpdateTime()))


start()
