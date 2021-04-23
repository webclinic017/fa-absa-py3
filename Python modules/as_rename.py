
import ael, string



import ael, string


filename = 'f:\UnusedTasks1.csv'
print filename

count = 0
fail_list = []

try:
    f = open(filename)
except:
    print 'Could not open file'
    

q_list = []
line = f.readline()
while line:
    l = string.split(line, ',')
    
    name = l[0].strip()

    q_clone = ael.Task[name].clone()
    l = len(q_clone.name)
    temp = q_clone.name[4:l]
    q_clone.name = temp
    print name, ';', q_clone.name

    try:
        q_clone.commit()
        count = count + 1
    except:
        fail_list.append(name)
        print 'could not commit'
        
    line = f.readline()  
    
f.close()

print 'Queries committed : ', count
print 'Queries not committed : ', fail_list
 
