import acm    
import ael
import IntraDayLimitMonitoring as limits

filename = r'Y:\Jhb\Secondary Markets IT\Christo\patrick\excels\produpdate\ProdLimitsUpdate_FI.csv'

created=[]

def addLimit(data, desk_name, column_name, value):
    desks = data.desks
    if desk_name in desks:
        desk = desks[desk_name]
    
        columns = data.columns
        if columns[column_name]:        
            #print "Setting limit for column %s" % column_name
            limit = limits.Limit(column_name, value)
            desk.limits[column_name] = limit
            
    else:
        desk = limits.Desk(desk_name, [])
        created.append(desk_name)
        
def remove_limit(data, desk_name, column_name):
    desks = data.desks
    if desk_name in desks:
        desk = desks[desk_name]
        columns = data.columns
        if columns[column_name]:  
            if column_name in desk.limits:
                del desk.limits[column_name]
            
        
file = open(filename, 'r')
header = file.readline()
header = header.replace('\n', '')
columns = header.split(',')

data = limits.getData()

for line in file.readlines():
    line = line.replace('\n', '')
    items = line.split(',')
    
    if items[0] == '':
        continue
        
    counter = 0
    for item in items:
        #print item,counter
        
        if counter ==0 :
            desk = item
            counter+=1
            continue
            
        if item <> '':
            print desk, columns[counter], '--->', item
            addLimit(data, desk, columns[counter], item)
        else:
            print 'CLEAN', columns[counter]
            remove_limit(data, desk, columns[counter])
            
            
        counter+=1
    
file.close()
limits.persistData(data)

print 'created', created


