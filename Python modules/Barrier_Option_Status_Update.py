import ael
''' Update the crossed status of barrier options if their barriers have been breached.
    If a barrier has been breached during the day the trader will set the settle price
    of the option to 0.000001.
    
    Scheduled script to be run at 19h00 each day
    
    Paul Jacot-Guillarmod   2009-07-24
'''
    
def updateBarrierStatus():
    
    # Generate a list of all un-expired barrier options that have trades booked against them.
    barrier_options = [e.insaddr for e in ael.Exotic if e.insaddr and e.barrier_option_type not in ('None') \
                and e.insaddr.exp_day >= ael.date_today() and len(e.insaddr.trades()) > 0]
                
    for ins in barrier_options:
        if ins.exotic().barrier_crossed_status not in ('Confirmed'):
            for p in ins.prices():
                if p.ptynbr.ptyid == 'SPOT' and p.settle == 0.000001 and ael.date_from_time(p.updat_time) == ael.date_today():
                    try:
                        e_clone = ins.exotic().clone()
                        e_clone.barrier_crossed_status = 'Confirmed'
                        e_clone.barrier_cross_date = ael.date_today()
                        e_clone.commit()
                    except:
                        print(ael.log('Error: Failed to set barrier crossed status for ' + ins.insid))                   
           
updateBarrierStatus()
    
