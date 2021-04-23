import ael

def checkPrices(filename, *rest):
    
    try:
    	f = open(filename)
    except:
    	print('File could not be found or opened')
	
    line = f.readline()
    
    while line:
    	print('1', (int)(line))
	p = ael.Price[(int)(line)]
	print(p)
	line = f.readline()
    
    return  
    
    
    
    
#ael_variables = [('filename', 'File Location', 'string')]
    
    
#def ael_main():
#dict):
#    filen = dict["filename"]
filen = 'c:\check3.txt'
checkPrices(filen)
