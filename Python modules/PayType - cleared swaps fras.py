import acm
# once off script to chnage the payType of cleared swaps and fras where the instrument names are defined explictly


ins_list = [
'USD/FRA/LI/140107-140407/0.8000#3',
'USD/FRA/LI/140107-140407/0.8000#2',
'ZAR/IRS/F-JI/130724-140724/5.3900',
'USD/IRS/LI-F/130305-260305/2.3125#1',
'ZAR/IRS/F-JI/130121-140121/5.0150#1']

for ins in ins_list:
    i = acm.FInstrument[ins]
    print('Before', i.Name(), i.InsType(), i.PayType())
    
    i.PayType('Spot')
    i.Commit()
    print('After', i.Name(), i.InsType(), i.PayType())
    
