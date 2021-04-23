import ael


def delete(i, *rest):
    
    i_clone = i.clone()    
    i_clone.und_insaddr = 166332

    try:
    	i_clone.commit()
	return 'Success'
    except:
    	return 'Failed'




    
def DayofYear(temp, dat, *rest):
   
    try:
    	d = ael.date_from_string(dat)
    except:
        try:
            d = ael.date_from_string(dat, '%Y/%m/%d')
        except:
            d = dat
	    
    try:
        return d.day_of_year()
    except:
        return 0


#t = '2007/07/22'
#print DayofYear(1, t)
c = ael.ChangeRequest[217599]

p = ael.Party['DALEIN VOERE PTY LTD'].clone()
#DALEIN VOERE PTY LTD
p.ptyid = 'DALEIN VOERE PTY LTD2'
p.commit()
print(p.pp())
#print p.updat_usrnbr.pp()


#print c.pp()
#print dir(c)



'''
new_p = c.get_change_clone()
for t in new_p:
    try:
        t.pp()
    else:
        for t2 in t:
            
    print dir(t), '????'
'''
'''
c.status = 'Rejected'
print c.pp()
c.commit()
'''
