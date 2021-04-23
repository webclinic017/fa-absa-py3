import ael
f = open('C:\\noneal.csv')
line = f.readline()
line = f.readline()
while line:
    line = line.rstrip()
    print(line)
    pty = ael.Party[(int)(line)].clone()
    for a in pty.aliases():
    	if a.type == None:
	    a.delete()
    pty.commit()	        	
    line = f.readline()
f.close()
