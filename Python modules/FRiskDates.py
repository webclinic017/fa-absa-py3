import ael

periods = ['1d', '1w', '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '10m', '11m', '1y', '13m', '14m', '15m', '16m', '17m', '18m', '19m', '20m', '21m', '22m', '23m', '2y', '3y', '4y', '5y', '6y', '7y', '8y', '9y', '10y', '11y', '12y', '13y', '14y', '15y', '20y', '25y']

def get_day(ins,cal,nbr,*rest):
    spot = ins.curr.spot_date()
    day = spot.add_period(periods[nbr])
    day = day.adjust_to_banking_day(cal).to_string()
    return day
