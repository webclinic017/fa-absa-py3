
import acm, ael
import ABSA_Rate
from FBDPCommon import is_acm_object, ael_to_acm, acm_to_ael


def get_factor(time_bucket, ins):
    
    #if not ins:
    #    retun 1.0
        
    if not is_acm_object(ins):
        ins = ael_to_acm(ins)
        
        
     
    
    # Credit curve mapped to ins
    cred_curve = ins.MappedCreditLink().Link().YieldCurveComponent()
    
    # Check for a quanto curve mapped to the instrument otherwise use the quanto curve mapped to the credit reference
    #quanto_curve = get_addinfo(ins, 'CDQuantoCurve') 
    if hasattr(ins.AdditionalInfo(), "CDQuantoCurve"):
        quanto_curve = ins.AdditionalInfo().CDQuantoCurve()
    else:
        quanto_curve = None
        
        

        
    if not quanto_curve:
    
        credit_ref = ins.CreditReference()
        #quanto_curve = get_addinfo(credit_ref, 'CDQuantoCurve')
        
        if credit_ref and hasattr(credit_ref.AdditionalInfo(), "CDQuantoCurve"):
            quanto_curve = credit_ref.AdditionalInfo().CDQuantoCurve()
        else:
            quanto_curve = None
        
    if quanto_curve:     quanto_curve = quanto_curve.Name()
    
  
        
    if hasattr(cred_curve, 'Curve'):     
        cred_curve_name =  cred_curve.Curve().Name()
    else:
        cred_curve_name = None
        
    if cred_curve_name and ins.Currency().Name() == 'ZAR' and quanto_curve and quanto_curve != cred_curve_name:#cred_curve.Curve().Name():
        #if time_bucket == 'Total':
        #    yc_date = acm.Time().BigDate()
        #else:
        #    yc_date = acm.Time().PeriodSymbolToDate(time_bucket)
        
        today = acm.Time().DateToday()
        if time_bucket in ('Rest', 'Total') :
            yc_date = acm.Time().BigDate()
        else:
            yc_date = acm.Time().PeriodSymbolToDate(time_bucket)
        

        
        # Calculate value of attribute spread curve mapped to ins for a given time bucket
        cred_curve_value = ABSA_Rate.ABSA_yc_rate(None, \
                                                    cred_curve.Curve().Name(), \
                                                    ael.date(today), \
                                                    ael.date(yc_date), \
                                                    'Quarterly', \
                                                    'Act/365', \
                                                    'Par CDS Rate', \
                                                    ins.Name())
        
        # Calculate value of quanto curve and adjust bump value accordingly
        quanto_yc = acm.FYieldCurve[quanto_curve]

        

        
        if str(cred_curve.ClassName()) =='FYCAttribute':
            ycatt = quanto_yc.YCAttribute(cred_curve.Issuer(), quanto_yc.Currency(), cred_curve.SeniorityChlItem(), cred_curve.RestructuringType())
        else:
            ycatt = None
 


       
        if ycatt:
            yc = ycatt.Curve()
            underlying_yc = yc.UnderlyingCurve()
            yc_ircurveinfo = ycatt.IrCurveInformation(underlying_yc.IrCurveInformation(today), today)
            quanto_yc_value = yc_ircurveinfo.Rate(ael.date(today), ael.date(yc_date), 'Quarterly', 'Act/365', 'Par CDS Rate', None, 0)

            point_ratio = cred_curve_value / quanto_yc_value
            
            return point_ratio
    
    return 1

def delta_adjust(time_bucket, ins):
    factor = get_factor(time_bucket, ins) 
    return factor * 0.0001
    


buckets = acm.FStoredTimeBuckets.Select("name = 'CDIssuer'")
if len(buckets)==1:     
    buckets=buckets[0]
elif len(buckets)>1:    
    print 'Found more than one Bucket definiton with name CDIssuer, using the first.  Check since this can influence the "adjusted credit par delta total" column'
    buckets=buckets[0]
else:                   
    print 'Time bucket (CDIssuer) not found, this is needed for the "adjusted credit par delta total" column'
    buckets=None

def getFixedBuckets():
    return buckets.TimeBuckets()
    
def sumAxis(ax):
    total=0
    for item in ax:
        try:
            val = item.Value().Number()
        except:
            val = item
        total += val
    return total

def multiplyAxisArray(ax, fac):
    res=[]
    for i in range(len(fac)):
        newval = ax[i].Number() * fac[i]
        res.append(ax[i].Number() * fac[i])
        #print 'created new val', ax[i].Number() ,'* ',fac[i], '  =  ', newval

    return res

    
