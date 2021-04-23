# Exotic options functions
import ael, string, time
from ael import *
 

#Returns the last date of all the exotic event dates
def LastDate(Instr,*rest):
 
    DateList = []
    
    #Get a list of all the dates in the events table    
    MonitorDates = Instr.exotic_events()
   
    #Get a distinct list of all the barrier dates in the events list 
    for dates in MonitorDates:
        if dates.type == 'Barrier date':
            if DateList.__contains__(dates.date) == 1:
                pass
            else:
                DateList.append(dates.date)
    
    #Sort the list in ascending order
    DateList.sort()
    
    return DateList[len(Instr.exotic_events())-1]
 
#Returns the number of Business days between two dates
def BusDaysBetween(Instr, dateNear, dateFar):
    
    counter = 0
    while dateNear.add_banking_day(Instr.curr, counter) < dateFar:
          counter = counter + 1
    return counter      
 

#Build a list of all the exotic dates connected to an instrument
def ObsFreq(Instr,*rest):
 
    DateList = []
    
    #Get a list of all the dates in the events table    
    MonitorDates = Instr.exotic_events()
    
    #Get a distinct list of all the barrier dates in the events list 
    for dates in MonitorDates:
        if dates.type == 'Barrier date':
            if DateList.__contains__(dates.date) == 1:
                pass
            else:
                DateList.append(dates.date)
    
    #Sort the list in ascending order
    DateList.sort()
    
    #Returns observation frequency
    if len(DateList) == 1 and DateList[0] > date_today():
       return BusDaysBetween(Instr, date_today(), DateList[0]) 
    else:
       return BusDaysBetween(Instr, DateList[0], DateList[1])
