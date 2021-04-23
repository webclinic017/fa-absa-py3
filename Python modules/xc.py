import ael, string


#try:
f = open('C:\\Adhov\\trades.csv')
#    print '.......Trades Numbers Upload Process Begin....... \n'
tfnew = ael.TradeFilter.new()
   
#except:
#    print 'File not opened'

#print dir(tfnew)
    
line = (f.readline()).strip()
print tfnew.get_query()
q = []
#q[0] = tfnew.set_query([('','','Trade number','equal to',line,'')])
#q[0] = tfnew.set_query([('Or','','Portfolio','equal to',name,'')])
while line != '':
    #print line
    l = []
    l = string.split(line, ',')
    #party = ael.Party[l[0]]
    line = (f.readline()).strip()
#    tfnew.set_query([('Or','','Trade number *','equal to',line,'')])


#failed_list = []
#p1 = ael.Party['Funding Desk']
#while line != '':
#tfnew.set_query([('','','Trade number *','equal to',line,'')])

