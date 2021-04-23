import ael

try:
    infile = open('c:\cp.txt', 'r')

except:
    print('Error opening file')
    

line = infile.readline()
ptys = ''
while line:
    line = line.rstrip('\n')
    ptys = ptys + line
    
    line = infile.readline()
    
print(ptys)
    
infile.close()
