import ael
 
to = ael.TextObject
tp = ael.Parameter
 
gl = []
for x in to:
    if x.type in ( 'SQL Query', 'SQL Question'):
        m = x.get_text()
        n = m.find('ASQL_log')
        w =[]
        flag = 0
        r = '' 
        if n > 0:
            
            if m.find(x.name) < 0: #no log
                #t_clone = x.clone()
                #p = m.find('ASQL_log')
                #q = m.find('SQL_QUESTION')
                #t = "'ASQL_log','" + str(x.name) + "') 'Name' \n into  ASQL_LOG_TEMP \n from TextObject p \n where p.name = '" + str(x.name) + "' and p.type = '" + str(x.type) + "' \n"
                #print m[0:(p-1)] + t + m[(q+13): (q + 14) ]
                #y = m[0:(p-1)] + t + m[(q+13): ]
                #t_clone.set_text(y)
                #try:
                #    t_clone.commit()
                #    print 'WRONG LOG:      ', 'SUCCESS', x.name, x.type, x.seqnbr
                #except:
                #    print 'WRONG LOG:      ', 'FAIL', x.name, x.type, x.seqnbr

                r = " WRONG LOG NAME  "
                flag = 1
                   
        else:
            
            #t_clone = x.clone()
            #s = str("/* ******************  ASQL USAGE LOG  ********************** */ \n select \n      ael_i(p,'ASQL_log','") + str(x.name) + "') 'Name' \n into  ASQL_LOG_TEMP \n from TextObject p \n where p.name = '" + str(x.name) + "' and p.type = '" + str(x.type) + "' \n \n  "
            #m = s +m
            #t_clone.set_text(m)
            #try:
            #    t_clone.commit()
            #    print 'NO LOG:      ', 'SUCCESS', x.name, x.type, x.seqnbr
            #except:
            #    print 'NO LOG:      ', 'FAIL', x.name, x.type, x.seqnbr
            
            r = " NO LOG  "
            flag = 1
            

    
        if m.find('Parameter p') > 0:
            '''t = m.find('Parameter p')
            s = " TextObject p"
            t_clone = x.clone()
            m = m[0:(t-1)] + s + m[(t+11):]
            t_clone.set_text(m)
            try:
                t_clone.commit()
                print 'PARAM:      ', 'SUCCESS', x.name, x.type, x.seqnbr
            except:
                print 'PARAM:      ', 'FAIL', x.name, x.type, x.seqnbr'''
            #print m[0:(t-1)] + s + m[(t+11):(t+25)]
            r = r + " PARM NOT TEXTOBJECT"
            flag = 1
            
        if m.find("p.type = 'SQL_QUESTION'") > 0:
            '''t = m.find("p.type = 'SQL_QUESTION'")
            s = " p.type = 'SQL Query'"
            t_clone = x.clone()
            m = m[0:(t-1)] + s + m[(t+23):]
            t_clone.set_text(m)
            try:
                t_clone.commit()
                print 'SQL QUESTION:      ', 'SUCCESS', x.name, x.type, x.seqnbr
            except:
                print 'SQL QUESTION:      ', 'FAIL', x.name, x.type, x.seqnbr'''
            #print m[0:(t-1)] + s + m[(t+23):(t+29)]
            r = r + " SQL QUESTION"
            flag = 1
            #w = []
        if flag  == 1:
            w.append(r)
        else:
            w.append("CORRECT")
       
        w.append('TEXT OBJECT')
        w.append(x.type)
        w.append(x.name)
        gl.append(w)
       
outfile = 'F:\Newtestaa.csv'
report = open(outfile, 'w')
Headers = ['LOG STATUS', 'DB OBJECT', 'TYPE', 'NAME']
for i in Headers:
        report.write((str)(i))
        report.write(',')
report.write('\n')
 
for lsts in gl:
        
        for ls in lsts:
            
            report.write((str)(ls))
            report.write(',')
        report.write('\n')
        
report.close()


















