'''

CHG0093277 - 14 April 2020  Anil Parbhoo scipt that reads task names from a csv file so that they can be renamed for subsequent deletion

'''

import ael, acm, csv

ael_variables = [('path', 'Output Path', 'string', ['c:\\Temp\\'], 'c:\\Temp\\', 1, 0, 'Enter only full path of file, not filename.'),
                 ('name', 'File Name', 'string', ['rename_tasks.csv'], 'rename_tasks.csv', 1, 0, 'Enter only filename, not path of file.')]

def ael_main(dict):

    filename = dict['path'] + dict['name']
    
    print 'file name and path = ', filename

    rename_list = []
    
    with open(filename, "rb") as f:
        reader = csv.reader(f)
        reader.next() 
        for line in reader:
            task_name = line[0].strip()
            rename_list.append(task_name)
            
    print rename_list

    for n in rename_list:
        #TBR = To Be Removed
        if acm.FAelTask[n]:
            t = acm.FAelTask[n]
            print 'before', t.Name()
        
            try:
                s = t.Name()
                t.Name('TBR_'+s)
                t.Commit()
                print 'after', t.Name()
            except:
                print 'CANNOT rename', t.Name()
        else:
            print n, ' is not a valid task name'


            

        

        
    
