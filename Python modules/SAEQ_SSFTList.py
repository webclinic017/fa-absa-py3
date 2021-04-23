import ael, SAEQ_CreateVolPoints
try:
    f = open('C:\sec_unds3.csv')
except:
    print('Could not open')
line = f.readline()
while line:
    line = line.rstrip()
    list = []
    list = line.split(',')
    dict = {}
    dict['underlying'] = list[0]
    dict['vn'] = list[0] + '_Skew'
    dict['cons'] = 1
    dict['vols'] = list[3]
    dict['utype'] = 'SSFT'
    SAEQ_CreateVolPoints.ael_main(dict)

    line = f.readline()
    print(line)
f.close()
