import ael
try:
    infile = open('C:\\Documents and Settings\\abhj106\\My Documents\\EersteFloerwerk\\changedeals.csv')
except:
    print('Error opening file')
newCp = ael.Party['DMX INTERNAL FX']
print('New: ', newCp.ptyid)
line = infile.readline()
while line:
    trdn = line.rstrip()
    trd = ael.Trade[(int)(trdn)]
    #print trd.counterparty_ptynbr.ptyid
    trdclone = trd.clone()
    trdclone.counterparty_ptynbr = newCp
    print('old: ', trd.counterparty_ptynbr.ptyid)
    print('New: ', trdclone.counterparty_ptynbr.ptyid)
    trdclone.commit()
    line = infile.readline()
infile.close()
