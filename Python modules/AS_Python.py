import ael



try:
    f = open('c:\Pone.txt')
except:
    print('File could not be found or opened')
	
line = f.readline()
    
while line:
    print(line)
    l1 = line.replace('k', 'l')
    l2 = l1.replace('o', 'p')
    l3 = l2.replace('e', 'f')
    print(l3)

    line = f.readline()
    

