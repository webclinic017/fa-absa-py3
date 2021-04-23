
"""
Purpose: New python script that uses the python script 'Generate_CPI_NACS' as a point of reference 
Department : PCG Price Testing
Desk : Interest Rate Derivatives
Requester :  Mtoko, Khaya: ABSA (JHB)
Developer : Anil Parbhoo
CR Number : 470649
Book of Work / Jira Reference Number : ABITFA-295 
Previous CR Numbers relating to this deployment


"""

"""
This script is used to calculate the nacs cpi points and also populate the benchmarks
the function update_cpi_nacs takes one param which determines whether the update
is commited or only simulated - a value of -1 will simulate only 
and any other value will commit
Dirk Strauss    -       2007-10-04
CR 211432
"""






import ael

import acm


debug = 1

def update_cpi_nacs(simulate_only):    
    yc_real = acm.FYieldCurve['ZAR-REAL/PriceTesting']
    yc_swap = acm.FYieldCurve['ZAR-SWAP/PriceTesting']
    
    if yc_real.RealTimeUpdated():
        yc_real.Calculate()
        yc_real.Simulate()
    if yc_swap.RealTimeUpdated():
        yc_swap.Calculate()
        yc_swap.Simulate()
    
    

    yc_cpi = acm.FYieldCurve['ZAR-CPI/PriceTesting']
    mkt = acm.FParty['SPOT']
    
    bms = []    
    prcs = []
    
    yc_cpi_bms = yc_cpi.Benchmarks()
    
    for bm in yc_cpi_bms:
        inst = bm.Instrument()
        datePeriod = inst.maturity_date()
        tpl = (datePeriod, inst)#tuple = (maturity date , instrument object)
        bms.append(tpl)
        
    bms.sort()    

    today = acm.Time().DateToday()

    for bm in bms:
        mat = bm[0]
        days = acm.Time().DateDifference( mat, today )

        tf = 182.5 / days
        
        df1 = yc_real.IrCurveInformation().Rate( today, mat, 'Annual Comp', 'Act/365', 'Discount', None, 0 )
        df2 = yc_swap.IrCurveInformation().Rate( today, mat, 'Annual Comp', 'Act/365', 'Discount', None, 0 )
        
        cpi_yield = (((df1/df2) ** tf) - 1) * 2
        cpi_yield = cpi_yield * 100            
        
        print 'cpi_yield', cpi_yield
        print 'df1', df1
        print 'df2', df2
        print 'tf', tf
        
        if debug == 1:
            print today, mat, days, tf, cpi_yield, bm[1].Name(), df1, df2        
    
        bm_ins = bm[1]

        if len(bm_ins.Prices()) > 0:
            for p in bm_ins.Prices():
                if p.Market() == mkt:
                    prc = p                    
    
            if prc.Settle() <> cpi_yield or prc.Last() <> cpi_yield:
                prcC = prc.Clone()
                prcC.Last( cpi_yield )
                prcC.Settle( cpi_yield )
                prcC.Day( today )               
                if simulate_only == -1:
                    prc.Apply( prcC )
                else:
                    prc.Apply( prcC )
                    prc.Commit()
                prcs.append( prcC )
            else:
                print '====>', bm_ins.Name(), ' not updated - no change in cpi'
        else:
            prcN = acm.FPrice()            
            prcN.Last( cpi_yield )            
            prcN.Settle( cpi_yield )
            prcN.Instrument( bm_ins ) 
            prcN.Day( today )
            prcN.Market( mkt )
            prcN.Currency( bm_ins.Currency() )
            if simulate_only == -1:
                prcN.Apply()
            else:
                prcN.Commit()
            prcs.append(prcN)
            
    yc_cpi.Calculate()
    yc_cpi.Simulate()


# ==========================================================


mylist = [0, -1]


ael_variables = [('selectedInput', 'input_Data', 'int', mylist, '0', 1, 0, 'input to simulate is -1 whereas any other value will commit spot price to benchmarks')]




def ael_main(dict):
    id = dict["selectedInput"]
    update_cpi_nacs(id)
    return
    
    
