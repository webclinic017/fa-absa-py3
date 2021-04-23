import ael, string

infile = open('c:\\export_list.csv')
f = open('c:\\Martin_trdfil_backup.txt', 'w')

line = infile.readline()
while line:
    #print line
    l = string.split(line, ',')
    #print l[0].strip()
    try:
        trdfil = ael.TradeFilter[l[0].strip()]
        name = trdfil.fltid + '\n\n'
        f.write(name)
        for list in trdfil.get_query():
            for c in list:
                output = c + ' '
                if output in ('Or ', 'And '):
                    output = '\n' + output
                    f.write(output)
                else:
                    f.write(output)
        '''
        tf_clone = trdfil.clone()
        tf_clone.fltid = 'TBR_' + tf_clone.fltid
        try:
            tf_clone.commit()
        except:
            print 'Could not update ', tf_clone.fltid
        '''
    except:
        print 'Filter not found', l[0]
    
    f.write('\n\n\n\n')
    line = infile.readline()
    
infile.close()    
f.close


