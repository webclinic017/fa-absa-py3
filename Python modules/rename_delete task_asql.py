'''

CHG0099556 - 14 May 2020 - Anil Parbhoo - script that reads task/asql names from a csv file so that they can be renamed and subsequently deleted

'''

import ael, acm, csv

ael_variables = [('path', 'Input Path', 'string', ['c:\\Temp\\'], 'c:\\Temp\\', 1, 0, 'Enter only full path of file, not filename.'),
                 ('name', 'File Name', 'string', ['rename_tasks.csv'], 'rename_tasks.csv', 1, 0, 'Enter only csv filename, not path of file.'),
                 ('Rename_Delete', 'Rename or Delete', 'string', ['Rename', 'Delete_Tasks', 'Delete_ASQLs'], 'Rename', 1, 0, 'Select Rename or delete type from the drop down')]




def ael_main(dict):

    filename = dict['path'] + dict['name']
    print 'file name and path = ', filename
    print 'action required = ', dict['Rename_Delete']
    
    list_from_csv_file = []
    
    with open(filename, "rb") as f:
        reader = csv.reader(f)
        reader.next() #row 1 is a header row in csv file so go to next row
        for line in reader:
            name = line[0].strip()
            list_from_csv_file.append(name)
            
    list_from_csv_file = set(list_from_csv_file)
    list_from_csv_file = tuple(list_from_csv_file)
        
    
    for n in list_from_csv_file:
        #TBR = To Be Removed
        if dict['Rename_Delete'] == 'Rename':
            if acm.FAelTask[n]:
                t = acm.FAelTask[n]
                print 'before - task name', t.Name()
            elif acm.FSQL[n]:
                t = acm.FSQL[n]
                print 'before - asql name', t.Name()            
            else:
                print n, ' is NOT a valid task or asql name'
            
            try:
                s = t.Name()
                t.Name('TBR_'+s)
                t.Commit()
                print 'after - task or asql name was changed', t.Name()
            except:
                print 'CANNOT rename task or asql name - ', n
                
        if dict['Rename_Delete'] == 'Delete_Tasks':
            task = acm.FAelTask[n]
            try:
                print 'the task %s will be deleted' % task.Name()
                task.Delete()
            except:
                print 'the task %s could NOT be deleted' % task.Name() 
            
        if dict['Rename_Delete'] == 'Delete_ASQLs':
            asql = acm.FSQL[n]
            try:
                print 'the ASQL %s will be deleted' % asql.Name()
                asql.Delete()
            except:
                print 'the ASQL %s could NOT be deleted' % asql.Name() 
        
    

