"""
This is a once-off script which should fix the funding records 
on PB_MAP109_CE pswap. 

Bg: First, trades were booked on ZAR/NGPLT instrument. Later on, 
it was decided that the trades should be booked on ZAR/NGPLT/MTM instrument.
And finally, there is a script right now which rebooks all trades from 
non-MTM instruments to MTM instruments (for certain instypes). 
As a consequence, we've lost the row for the non-mtm instrument on the reports
and the funding we charged for this instrument is missing now.

Here is the plan how to fix the issue:
1. Find NGPLT and NGPLT/MTM legs on MAP109 pswap
2. Update resets on the NGPLT/MTM leg
3. Remove the resets from NGPLT leg
So let's go
"""
import acm
import at_time
from collections import namedtuple


ResetRecord = namedtuple('ResetRecord', 'date, start_date, end_date, type, value')
cal = acm.FCalendar['ZAR Johannesburg']

def find_reset(leg, reset_rec):
    """ Find a reset on the leg equal to reset record 
    """
    for reset in leg.Resets():
        if reset.ResetType() == reset_rec.type\
        and reset.StartDate() == reset_rec.start_date\
        and reset.EndDate() == reset_rec.end_date\
        and reset.Day() == reset_rec.date:
            return reset

def update_reset(reset, reset_rec):
    """ Update reset with data from reset record reset_rec
    """
    reset.Day(reset_rec.date)
    reset.StartDate(reset_rec.start_date)
    if at_time.is_banking_day(cal, reset_rec.start_date):
        read_date = reset_rec.start_date
    else:
        read_date = cal.AdjustBankingDays(reset_rec.start_date, 1)
    
    reset.ReadTime(read_date + " 00:00:00")
    reset.EndDate(reset_rec.end_date)
    reset.FixingValue(reset_rec.value)
    reset.Commit()


reset_changes = [
    # NGPLT resets only -> move to NGPLT/MTM
    ResetRecord(date='2013-08-15', start_date='2013-08-15', end_date='2013-08-16', type='Nominal Scaling', value='-2099.748506'), ResetRecord(date = '2013-08-15', start_date = '2013-08-15', end_date = '2013-08-16', type = 'Simple Overnight', value = '3.871'),
    ResetRecord(date='2013-08-16', start_date='2013-08-16', end_date='2013-08-17', type='Nominal Scaling', value='5101.076462'), ResetRecord(date = '2013-08-16', start_date = '2013-08-16', end_date = '2013-08-17', type = 'Simple Overnight', value = '5.57'),
    ResetRecord(date='2013-08-19', start_date='2013-08-17', end_date='2013-08-20', type='Nominal Scaling', value='9019.8986'), ResetRecord(date='2013-08-19', start_date='2013-08-17', end_date='2013-08-20', type='Simple Overnight', value='5.57'), 
    ResetRecord(date='2013-08-20', start_date='2013-08-20', end_date='2013-08-21', type='Nominal Scaling', value='14638.49333'), ResetRecord(date='2013-08-20', start_date='2013-08-20', end_date='2013-08-21', type='Simple Overnight', value='5.562'), 
    ResetRecord(date='2013-08-21', start_date='2013-08-21', end_date='2013-08-22', type='Nominal Scaling', value='17080.9944'), ResetRecord(date='2013-08-21', start_date='2013-08-21', end_date='2013-08-22', type='Simple Overnight', value='5.57'), 
    ResetRecord(date='2013-08-22', start_date='2013-08-22', end_date='2013-08-23', type='Nominal Scaling', value='511552.9863'), ResetRecord(date='2013-08-22', start_date='2013-08-22', end_date='2013-08-23', type='Simple Overnight', value='5.558'), 
    ResetRecord(date='2013-08-23', start_date='2013-08-23', end_date='2013-08-24', type='Nominal Scaling', value='518416.8047'), ResetRecord(date='2013-08-23', start_date='2013-08-23', end_date='2013-08-24', type='Simple Overnight', value='5.573'), 
    ResetRecord(date='2013-08-26', start_date='2013-08-24', end_date='2013-08-27', type='Nominal Scaling', value='520471.9381'), ResetRecord(date='2013-08-26', start_date='2013-08-24', end_date='2013-08-27', type='Simple Overnight', value='5.58'), 
    ResetRecord(date='2013-08-27', start_date='2013-08-27', end_date='2013-08-28', type='Nominal Scaling', value='518945.6421'), ResetRecord(date='2013-08-27', start_date='2013-08-27', end_date='2013-08-28', type='Simple Overnight', value='5.583'), 
    ResetRecord(date='2013-08-28', start_date='2013-08-28', end_date='2013-08-29', type='Nominal Scaling', value='530494.6231'), ResetRecord(date='2013-08-28', start_date='2013-08-28', end_date='2013-08-29', type='Simple Overnight', value='5.6'), 
    ResetRecord(date='2013-08-29', start_date='2013-08-29', end_date='2013-08-30', type='Nominal Scaling', value='521687.2979'), ResetRecord(date='2013-08-29', start_date='2013-08-29', end_date='2013-08-30', type='Simple Overnight', value='5.592'), 
    ResetRecord(date='2013-08-30', start_date='2013-08-30', end_date='2013-08-31', type='Nominal Scaling', value='520230.5206'), ResetRecord(date='2013-08-30', start_date='2013-08-30', end_date='2013-08-31', type='Simple Overnight', value='5.586'), 
    ResetRecord(date='2013-09-02', start_date='2013-08-31', end_date='2013-09-03', type='Nominal Scaling', value='513318.7682'), ResetRecord(date='2013-09-02', start_date='2013-08-31', end_date='2013-09-03', type='Simple Overnight', value='5.574'), 
    ResetRecord(date='2013-09-03', start_date='2013-09-03', end_date='2013-09-04', type='Nominal Scaling', value='511745.6453'), ResetRecord(date='2013-09-03', start_date='2013-09-03', end_date='2013-09-04', type='Simple Overnight', value='5.57'), 
    ResetRecord(date='2013-09-04', start_date='2013-09-04', end_date='2013-09-05', type='Nominal Scaling', value='522292.8163'), ResetRecord(date='2013-09-04', start_date='2013-09-04', end_date='2013-09-05', type='Simple Overnight', value='5.576'), 
    ResetRecord(date='2013-09-05', start_date='2013-09-05', end_date='2013-09-06', type='Nominal Scaling', value='506719.707'), ResetRecord(date='2013-09-05', start_date='2013-09-05', end_date='2013-09-06', type='Simple Overnight', value='5.567'), 
    ResetRecord(date='2013-09-06', start_date='2013-09-06', end_date='2013-09-07', type='Nominal Scaling', value='500724.1251'), ResetRecord(date='2013-09-06', start_date='2013-09-06', end_date='2013-09-07', type='Simple Overnight', value='5.575'), 
    ResetRecord(date='2013-09-09', start_date='2013-09-07', end_date='2013-09-10', type='Nominal Scaling', value='499796.1804'), ResetRecord(date='2013-09-09', start_date='2013-09-07', end_date='2013-09-10', type='Simple Overnight', value='5.557'), 
    ResetRecord(date='2013-09-10', start_date='2013-09-10', end_date='2013-09-11', type='Nominal Scaling', value='490737.7765'), ResetRecord(date='2013-09-10', start_date='2013-09-10', end_date='2013-09-11', type='Simple Overnight', value='5.557'), 
    ResetRecord(date='2013-09-11', start_date='2013-09-11', end_date='2013-09-12', type='Nominal Scaling', value='481599.1242'), ResetRecord(date='2013-09-11', start_date='2013-09-11', end_date='2013-09-12', type='Simple Overnight', value='5.546'), 
    ResetRecord(date='2013-09-12', start_date='2013-09-12', end_date='2013-09-13', type='Nominal Scaling', value='480883.9869'), ResetRecord(date='2013-09-12', start_date='2013-09-12', end_date='2013-09-13', type='Simple Overnight', value='5.573'), 
    ResetRecord(date='2013-09-13', start_date='2013-09-13', end_date='2013-09-14', type='Nominal Scaling', value='443411.1233'), ResetRecord(date='2013-09-13', start_date='2013-09-13', end_date='2013-09-14', type='Simple Overnight', value='5.556'), 
    ResetRecord(date='2013-09-16', start_date='2013-09-14', end_date='2013-09-17', type='Nominal Scaling', value='433898.5535'), ResetRecord(date='2013-09-16', start_date='2013-09-14', end_date='2013-09-17', type='Simple Overnight', value='5.537'), 
    ResetRecord(date='2013-09-17', start_date='2013-09-17', end_date='2013-09-18', type='Nominal Scaling', value='413101.9325'), ResetRecord(date='2013-09-17', start_date='2013-09-17', end_date='2013-09-18', type='Simple Overnight', value='5.55'), 
    ResetRecord(date='2013-09-18', start_date='2013-09-18', end_date='2013-09-19', type='Nominal Scaling', value='986005.8796'), ResetRecord(date='2013-09-18', start_date='2013-09-18', end_date='2013-09-19', type='Simple Overnight', value='5.564'), 
    ResetRecord(date='2013-09-19', start_date='2013-09-19', end_date='2013-09-20', type='Nominal Scaling', value='962903.1661'), ResetRecord(date='2013-09-19', start_date='2013-09-19', end_date='2013-09-20', type='Simple Overnight', value='5.554'), 
    ResetRecord(date='2013-09-20', start_date='2013-09-20', end_date='2013-09-21', type='Nominal Scaling', value='2332510.733'), ResetRecord(date='2013-09-20', start_date='2013-09-20', end_date='2013-09-21', type='Simple Overnight', value='5.562'), 
    ResetRecord(date='2013-09-23', start_date='2013-09-21', end_date='2013-09-24', type='Nominal Scaling', value='2349029.023'), ResetRecord(date='2013-09-23', start_date='2013-09-21', end_date='2013-09-24', type='Simple Overnight', value='5.55'), 
    ResetRecord(date='2013-09-25', start_date='2013-09-24', end_date='2013-09-26', type='Nominal Scaling', value='2487659.844'), ResetRecord(date='2013-09-25', start_date='2013-09-24', end_date='2013-09-26', type='Simple Overnight', value='5.548'), 
    ResetRecord(date='2013-09-26', start_date='2013-09-26', end_date='2013-09-27', type='Nominal Scaling', value='2495178.019'), ResetRecord(date='2013-09-26', start_date='2013-09-26', end_date='2013-09-27', type='Simple Overnight', value='5.58'), 
    ResetRecord(date='2013-09-27', start_date='2013-09-27', end_date='2013-09-28', type='Nominal Scaling', value='2732816.314'), ResetRecord(date='2013-09-27', start_date='2013-09-27', end_date='2013-09-28', type='Simple Overnight', value='5.577'), 
    ResetRecord(date='2013-09-30', start_date='2013-09-28', end_date='2013-10-01', type='Nominal Scaling', value='2759993.267'), ResetRecord(date='2013-09-30', start_date='2013-09-28', end_date='2013-10-01', type='Simple Overnight', value='5.56'), 
    ResetRecord(date='2013-10-01', start_date='2013-10-01', end_date='2013-10-02', type='Nominal Scaling', value='4246942.465'), ResetRecord(date='2013-10-01', start_date='2013-10-01', end_date='2013-10-02', type='Simple Overnight', value='5.578'), 
    # amending MTM for these three, they overlap (ZAR/NGPLT and ZAR/NGPLT/MTM had position on these days, need to sum it up to get the total funding)
    ResetRecord(date='2013-10-02', start_date='2013-10-02', end_date='2013-10-03', type='Nominal Scaling', value='4193632.077'), 
    ResetRecord(date='2013-10-03', start_date='2013-10-03', end_date='2013-10-04', type='Nominal Scaling', value='4278144.581'), 
    ResetRecord(date='2014-03-17', start_date='2014-03-15', end_date='2014-03-18', type='Nominal Scaling', value='8723142.6728615'), 
]

ael_variables = []

def ael_main(vars):
    ps = acm.FInstrument['PB_MAP109_CE']

    ngplt_leg = None
    ngplt_mtm_leg = None

    for leg in ps.Legs():
        # Float legs contain funding cash flows and resets
        if leg.IndexRef().Name() == 'ZAR/NGPLT' and leg.LegType() == 'Float':
            ngplt_leg = leg
        elif leg.IndexRef().Name() == 'ZAR/NGPLT/MTM' and leg.LegType() == 'Float':
            ngplt_mtm_leg = leg

    # find funding cash flow which will referenced by NGPLT/MTM resets we will create
    ngplt_mtm_funding_cf = [cf for cf in ngplt_mtm_leg.CashFlows() 
        if cf.AdditionalInfo().PS_FundWarehouse() == 'Funding'][0]

    acm.BeginTransaction()
    try:
        # NGPLT/MTM amendments
        ngplt_mtm_leg.StartDate('2013-08-15')
        for reset_rec in reset_changes:
            reset = find_reset(ngplt_mtm_leg, reset_rec)
            if not reset:
                reset = acm.FReset()
                reset.Leg(ngplt_mtm_leg)
                reset.CashFlow(ngplt_mtm_funding_cf)
                reset.ResetType(reset_rec.type)
            
            update_reset(reset, reset_rec)
        
        ngplt_mtm_leg.Commit()
        
        # NGPLT removals
        resets = ngplt_leg.Resets()
        for reset in resets[:]:
            reset.Delete()
            
        ngplt_leg.Commit()
        
        acm.CommitTransaction()
    except Exception as e:
        acm.AbortTransaction()
        print("Error: %s" % e)
        raise

    print("Completed successfully")
