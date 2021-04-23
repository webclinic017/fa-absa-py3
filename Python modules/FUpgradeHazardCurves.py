"""----------------------------------------------------------------------------
MODULE
    FInit_new_yc_fields
	
    (c) Copyright 2002 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    FInit_new_yc_fields copies additional information values for hazard rates
    curves into the new database fields. The additional information fields 
    copied are FSpotDays and FRecoveryRate.

    Curves with the additional information field FHazardCurve set to
    'yes' will be given a format of 'Hazard Rate Curve'. 

    The format is set to 'Hazard Rate Curve' also for all Attribute Spread 
    Curves with Storage Calculation Type 'Par CDS Rate', regardless if
    FHazardCurve is set to 'yes' or not.

    Note that Attribute Spread curves with a different Storage Calculation 
    Type than 'Par CDS Rate' will be given a format of 'Hazard Rate Curve' 
    if FHazardRate is set to 'yes'.
----------------------------------------------------------------------------"""

import ael

def init_new_yc_fields(yc,FHazardCurve_exists,FSpotDays_exists, \
    FRecoveryRate_exists,*self):
    
    try:
	curve_type = yc.yield_curve_type

	if (curve_type == "Spread" or curve_type == "Attribute Spread"):
    	    storage_calc_type = yc.storage_calc_type

	    if(FHazardCurve_exists):
    		is_add_info_hazard = yc.add_info('FHazardCurve')
    	    else:
		is_add_info_hazard = ""

	    if ((curve_type == "Attribute Spread" and \
	    	storage_calc_type == "Par CDS Rate") or \
		is_add_info_hazard == "Yes"):
    		
		curve_name = yc.yield_curve_name
    		curr = yc.curr
		curr_spot_days = yc.curr.spot_banking_days_offset

		if (FRecoveryRate_exists):
	    	    add_info_rec_rate = yc.add_info('FRecoveryRate')
		else:
	    	    add_info_rec_rate = 0

		if (FSpotDays_exists):
    	    	    add_info_spot_days = yc.add_info('FSpotDays')
		else:
	    	    add_info_spot_days = 0

		yc_clone = yc.clone()
    		
		yc_clone.ir_format="Hazard Rate Curve"
				
		if (curve_type == "Attribute Spread" and \
		    storage_calc_type != "Par CDS Rate"):
	    	    print 'Warning: Attribute Spread curve', curve_name,\
		    ', has format Hazard Rate although storage type is\
other than Par CDS Rate.'
		
		if (add_info_spot_days):
    	    	    yc_clone.spot_days=int(add_info_spot_days)
	    	
		else:
	    	    if (curr_spot_days):
	    		yc_clone.spot_days=int(curr_spot_days)
	    	    else:
	    		yc_clone.spot_days=0
		
		if (curve_type == 'Spread'):
	    	    if (add_info_rec_rate):
			yc_clone.rec_rate = float(add_info_rec_rate)
		    else:
			yc_clone.rec_rate = 0.0
		else:
	    	    yc_clone.rec_rate = 0.0
		
		yc_clone.commit()
    		ael.poll()
    except:
    	print 'failed'

def upgrade():
    FHazardCurve_exists = 0
    FSpotDays_exists = 0
    FRecoveryRate_exists = 0

    for ais in ael.AdditionalInfoSpec:
        if (ais.field_name == 'FHazardCurve'):
            FHazardCurve_exists = 1
    
        if (ais.field_name == 'FRecoveryRate'):
            FRecoveryRate_exists = 1
	
        if (ais.field_name == 'FSpotDays'):
            FSpotDays_exists = 1
	
    if (FHazardCurve_exists == 0):
        print 'Additional Information field FHazardCurve does not exist in \
database'
        
    if (FSpotDays_exists == 0):
        print 'Additional Information field FSpotDays does not exist in database'
    
    if (FRecoveryRate_exists == 0):
        print 'Additional Information field FRecoveryRate does not exist in \
database'

    for yc in ael.YieldCurve:
        init_new_yc_fields(yc, FHazardCurve_exists, FSpotDays_exists,
                           FRecoveryRate_exists)
    print 'finished'


if __name__ == "__main__":
    import sys, getopt
     
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'a:u:p:h:')
        if len(opts) != 3:
            raise getopt.error, ''
	    print '''Usage: upgrade_hazard_curves.py -a ads_address -u username
                     -p password'''
    except getopt.error, msg:
        print msg
        print '''Usage: upgrade_hazard_curves.py -a ads_address -u username
        -p password'''
        sys.exit(2)

    atlas_passw = ''
    
    for o, a in opts:
        if o == '-a': ads_address = a
        if o == '-u': atlas_user = a
        if o == '-p': atlas_passw = a

    ael.connect(str(ads_address), str(atlas_user), str(atlas_passw))

    upgrade()
	
    ael.disconnect()

else:
    upgrade()


