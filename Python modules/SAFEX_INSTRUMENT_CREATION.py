import ael
try:
    f = open('\\\\v036syb004001\\Development\\Safex\\SAFEX_Instrument_Data.csv')
except:
    print('Could not open the file')
line = f.readline()
while line:
    line = line.rstrip()
    list = []
    list = line.split(',')
    ins = list[0]
    und_ins = list[1]
    io = ael.Instrument[ins]
    uio = ael.Instrument[und_ins]
    if not uio:
        print('Could not find underlying instrument')
    else: 
        if not io:
            new_ins = ael.Instrument.new('Option')
            new_ins.insid = ins
            new_ins.und_insaddr = ael.Instrument[und_ins]
            new_ins.instype = 'Option'
            new_ins.curr = ael.Instrument['ZAR']
            new_ins.quote_type = 'Per Contract'
            new_ins.settlement = 'Cash'
            new_ins.exp_day = ael.date(list[3][0:10])
            if list[6] == 'C': 
                call = 1
            else: 
                call = 0
            new_ins.call_option = call
            new_ins.exercise_type = 'American'
            new_ins.strike_type = 'Absolute'
            new_ins.otc = 0
            ALSIcl = ael.ChoiceList.read('list = "ValGroup" and entry = "EQ_ALSI_Opt_Blk"')
            Stockcl = ael.ChoiceList.read('list = "ValGroup" and entry = "SAEQ_FUT"')
            pricefcl = ael.ChoiceList.read('list = "PriceFindingGroup" and entry = "EQ_Deriv"')
            new_ins.price_finding_chlnbr = pricefcl
            if list[1][4:8] == 'ALSI':
                new_ins.strike_price = (float)(list[2])
                new_ins.product_chlnbr = ALSIcl
                new_ins.contr_size = 10
                new_ins.paytype = 'Spot'
                new_ins.pay_day_offset = 0
            else:
                new_ins.strike_price = (float)(list[2]) * 100.00
                new_ins.product_chlnbr = Stockcl
                new_ins.contr_size = 100
                new_ins.paytype = 'Future'
                new_ins.pay_day_offset = 3
            try:
                new_ins.commit()
            except:
                print('Could not create instrument')
            
        
    line = f.readline()
    
f.close()
