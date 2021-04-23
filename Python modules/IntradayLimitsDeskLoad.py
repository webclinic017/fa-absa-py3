import acm    
import ael
import IntraDayLimitMonitoring as limits

#filename = r'Y:\Jhb\Secondary Markets IT\Christo\patrick\excels\equitylimits.csv'
filename = r'Y:\Jhb\Secondary Markets IT\Christo\patrick\excels\util\Intraday_load_Portfolios_per_Desk_FIFIX.csv'

file = open(filename, 'r')

data = limits.getData()
desks = data.desks

dict={}
missing_port = []
for line in file.readlines():
    line = line.replace('\n', '')
    desk, port = line.split(',')
    port = port.strip()
    exist = acm.FPhysicalPortfolio[port]
    if exist:
        dict.setdefault(desk, []).append(port)
    else:
        missing_port.append(port)

print dict

for desk_name in dict:
    
    if desk_name not in desks:
        desk = limits.Desk(desk_name, dict[desk_name])
        print 'ADDED     ', desk_name, dict[desk_name]
        data.desks[desk_name] = desk
    else:
        print 'SKIPPED ', desk_name, dict[desk_name]
        to_add = dict[desk_name]
        existing_desk = desks[desk_name]
        existing_ports=  existing_desk.portfolio_names
        for new_item in to_add:
            if new_item not in existing_ports:
                existing_ports.append(new_item)
                print '---------Added', new_item, '-----', desk_name
            

file.close()
print 'missing_port', missing_port
limits.persistData(data)
