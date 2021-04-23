import ael
def Valgroup(filename):
    print filename
    try:
    	infile = open(filename)
    except:
        print 'Could Not Open the file'
    line = infile.readline()
    while line:
    	insid = line.rstrip()
        ins = ael.Instrument[insid]
        print ins.insid, ' ', ins.otc, ' ', ins.instype
        id = ins.insid
        White = id.find('WMAZ')
        Yellow = id.find('YMAZ')
        Wheat = id.find('WHEAT')
        Weat = id.find('WEAT')
        Sunflw = id.find('SUNS')
        Sunf = id.find('SUNF')
        insclone = ins.clone()
        if ins.instype == 'Option':
            insclone.otc = 1
        if White != -1:
            insclone.product_chlnbr = 1242
        if Yellow != -1:
            insclone.product_chlnbr = 1243
        if Wheat != -1:
            insclone.product_chlnbr = 1244
        if Weat != -1:
            insclone.product_chlnbr = 1244
        if Sunflw != -1:
            insclone.product_chlnbr = 1245
        if Sunf != -1:
            insclone.product_chlnbr = 1245
        insclone.commit()
	line = infile.readline()
Valgroup('C:\\options.csv')
