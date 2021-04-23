"""-----------------------------------------------------------------------------
MODULE
    FUpgradeCovToCorrMatrix 
        
    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    The script will upgrade the Covariances to CorrelationMatrixes.
    
    All entries with identical legs will be omitted (for instance if an entry is 
    OMX, OMX, corr = 1). This kind of entry is no longer necessary since the 
    default value of the new method used_correlation(OMX,OMX) is 1.
    
    All entries with a currency outside the boundaries [-1,1] will be omitted.
    
    The script will also update all Correlation links so that the link type is
    "Correlation Matrix" instead of "Correlation".

NOTE
    The script is adapted for Equity Traders who often use flat Correlation
    matrixes. Therefore ALL BUCKETS ARE SET TO '0d'. This means that the correct
    corelation is returned from the function used_correlation() when calling it 
    without a bucket argument (which is faculative). 
    
    If another bucket than '0d' is entered in the correlation matrix and this 
    value is not given as an argument to the function used_correlation(), the 
    returned value is 0, even though the correlation is defined.
 -----------------------------------------------------------------------------"""
import ael

def copy_cov_to_corr_mat():
    covs = ael.Covariance.select()
    for cov in covs:
        s = cov.name
        print "Covariance", s
        cm = ael.CorrelationMatrix.new()
        cm.name = s    
        cm.protection = cov.protection
        cm.owner_usrnbr = cov.owner_usrnbr
        cm.four_eye_on = cov.four_eye_on
        cm.authorizer_usrnbr = cov.authorizer_usrnbr
        cm.archive_status = cov.archive_status

        covels = ael.CovarianceElement.select('cov_seqnbr=' + str(cov.seqnbr))
        for covel in covels:
            volcells = ael.VolatilityCell.select('cov_el_seqnbr=' + str(covel.seqnbr))
            for v in volcells:
                ve = ael.VolElement.new(cm)
                ve.recaddr = covel.recaddr
                ve.rec_type = covel.rec_type
                ve.bucket = '0d'
                ve.type = v.type
                ve.vol = v.vol
                ve.archive_status = v.archive_status
        
            corrcells = ael.CorrelationCell.select('cov_el_seqnbr0=' + str(covel.seqnbr))
            for c in corrcells:
                if c.cov_el_seqnbr0.recaddr != c.cov_el_seqnbr1.recaddr:
                    o0 = None; o1 = None
                    
                    if c.cov_el_seqnbr0.rec_type == 'Instrument': o0 = ael.Instrument[c.cov_el_seqnbr0.recaddr]
                    if c.cov_el_seqnbr0.rec_type == 'Party':      o0 = ael.Party[c.cov_el_seqnbr0.recaddr]
                    if c.cov_el_seqnbr0.rec_type == 'Volatility': o0 = ael.Volatility[c.cov_el_seqnbr0.recaddr]
                    if c.cov_el_seqnbr0.rec_type == 'YieldCurve': o0 = ael.YieldCurve[c.cov_el_seqnbr0.recaddr]
                    if c.cov_el_seqnbr0.rec_type == 'ChoiceList': o0 = ael.ChoiceList[c.cov_el_seqnbr0.recaddr]
                    if c.cov_el_seqnbr0.rec_type == 'RiskFactorSpec': o0 = ael.RiskFactorSpec[c.cov_el_seqnbr0.recaddr]

                    if c.cov_el_seqnbr1.rec_type == 'Instrument': o1 = ael.Instrument[c.cov_el_seqnbr1.recaddr]
                    if c.cov_el_seqnbr1.rec_type == 'Party':      o1 = ael.Party[c.cov_el_seqnbr1.recaddr] 
                    if c.cov_el_seqnbr1.rec_type == 'Volatility': o1 = ael.Volatility[c.cov_el_seqnbr1.recaddr]
                    if c.cov_el_seqnbr1.rec_type == 'YieldCurve': o1 = ael.YieldCurve[c.cov_el_seqnbr1.recaddr]
                    if c.cov_el_seqnbr1.rec_type == 'ChoiceList': o1 = ael.ChoiceList[c.cov_el_seqnbr1.recaddr]
                    if c.cov_el_seqnbr1.rec_type == 'RiskFactorSpec': o1 = ael.RiskFactorSpec[c.cov_el_seqnbr1.recaddr]             
                    
                    if o0 != None and o1 != None and -1<= c.corr <= 1:
                        corr = ael.Correlation.new(cm)
                        corr.recaddr0 = c.cov_el_seqnbr0.recaddr
                        corr.rec_type0 = c.cov_el_seqnbr0.rec_type
                        corr.bucket0 = '0d'
                        corr.recaddr1 = c.cov_el_seqnbr1.recaddr
                        corr.rec_type1 = c.cov_el_seqnbr1.rec_type
                        corr.bucket1 = '0d'
                        corr.corr = c.corr
                        corr.archive_status = c.archive_status
        try:
            cm.commit()
            print
        except Exception, msg:
            print "Exception for ", s, ": ", msg
            print  
    return "Corr. Matrix OK"


def move_corr_context_links():
    contexts = ael.Context.select()
    for con in contexts:
        print "Context", con.name
        ctc = con.clone()
        clinks = ctc.links()
        for cl in clinks:
            if cl.type == 'Correlation':
                cl.type = 'Correlation Matrix'
        ctc.commit()
    return "Move Links OK"
    
    
print copy_cov_to_corr_mat()
print
print move_corr_context_links()
