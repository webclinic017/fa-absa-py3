import ael, time

"""
Please note front system "feature":
    futures have to be updated before options and warrants else we stand the 
    risk of the future expiry time being set earlier as to accomodate
    option expiry date < future expiry date.
"""

print "Started."

trades = ael.TradeFilter["NLD_All_Trades"].trades()
p = 0
histList = []
updateTime = 17 * 60 * 60 + 00 * 60

for t in trades:
    if t.insaddr.insid not in histList:
        if t.insaddr.instype == 'Option': 
            if t.insaddr.und_insaddr.instype == 'Curr':
                eto = t.insaddr.exp_time
                et = t.insaddr.exp_day.to_time() + updateTime
                histList.append(t.insaddr.insid)
                tc = t.insaddr.clone()
                tc.exp_time = et
                tc.commit()
                p += 1

print str(p) + " Instruments updated."

#Testing procedure
outFile2 = "C:\\expUnchanged.csv"
report2 = open(outFile2, 'w')

Headers = ['Instrument ID', 'Instrument Type']
cnt = 0

for i in Headers:
    report2.write((str)(i))
    report2.write(',')

report2.write('\n')

ael.poll()

for t in trades:
    if (t.insaddr.exp_time % (60*60*24) != updateTime - 60*60*2):
        report2.write(t.insaddr.insid + "," + t.insaddr.instype)
        report2.write('\n')
        cnt += 1

report2.close()

print "See the unchanged list, C:\expUnchanged.csv, for a list of the %i changes not done." %(cnt)
print "Done."
