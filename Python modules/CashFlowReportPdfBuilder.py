'''
Developer   : Ickin Vural, Bhavnisha Sarawan
Module      : CashFlowReportPdfBuilder
Date        : 05/01/2010, 09/05/2011
Description : Generates PDF Report for trades CashFlows, Added a call to function from Disclaimer.
CR	    : C000000537548,C000000542772,C000000554468, C649904
'''

import ael, acm, os, time, re
import reportlab.lib.pagesizes

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm
from STATIC_TEMPLATE         import BuildLogos, BuildAdviceFooter
from reportlab.lib.colors    import black 
from zak_funcs               import formnum
from FBDPCommon              import acm_to_ael
from Disclaimer              import CashflowsDisclaimer



def BuildHeader (temp,t,date,canvas,*rest): 
    
    #Builds Header and Footer
    BuildLogos(canvas)
    BuildAdviceFooter(canvas)
    CashflowsDisclaimer(canvas)
    canvas.setFont("Helvetica", 6.0) 
    canvas.drawString(1.0*cm, 25.0*cm, 'Type')
    canvas.drawString(3.0*cm, 25.0*cm, 'Nominal')
    canvas.drawString(6.0*cm, 25.0*cm, 'Start Day')
    canvas.drawString(9.0*cm, 25.0*cm, 'End Day')
    canvas.drawString(12.0*cm, 25.0*cm, 'Days')
    canvas.drawString(15.0*cm, 25.0*cm, 'Pay Day')
    canvas.drawString(18.0*cm, 25.0*cm, 'Proj')
    
   
def BuildCashFlow(temp,t,date,canvas,*rest):    
    
    Legnbr      = ''
    Type        = ''
    FixedRate   = ''
    Nominal     = ''
    StartDay    = ''
    EndDay      = ''
    Days        = ''
    PayDay      = ''
    Proj        = ''
    Premium     = ''
    ValueDay    = ''
    StartDayTrade    = ''
    EndDayTrade      = ''
    
    
    # ########################## Trade Info ################################## 
    
    Our_Ref   = t.trdnbr
    Your_Ref  = t.your_ref
    TradeDate = ael.date_from_time(t.time)
    
    Notional = round(t.nominal_amount(), 2)
    ValueDay = t.value_day
    Premium  = round(t.premium, 2)
    
    
    
    for l in t.insaddr.legs():
        FixedRate = l.fixed_rate
        StartDayTrade = l.start_day
        EndDayTrade = l.end_day
        leg = acm.FLeg[l.legnbr]
        cashFlowQuery = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
        cashFlowQuery.AddAttrNode('Leg.Oid', 'EQUAL', leg.Oid())
        cashFlows = cashFlowQuery.Select().SortByProperty('PayDate', True) # The last argument is "ascending"
          
    # ########################## Trade detail ##################################
    
    canvas.setFont("Helvetica", 6.0)        
    canvas.drawString(1.0*cm, 25.5*cm, 'Our Ref ')
    canvas.drawString(2.0*cm, 25.5*cm, ': '+ str(Our_Ref))
    canvas.drawString(1.0*cm, 26.0*cm, 'Notional')
    canvas.drawString(2.0*cm, 26.0*cm, ': ' + str(formnum(Notional)))
    canvas.drawString(5.0*cm, 25.5*cm, 'Trade Start Day')
    canvas.drawString(7.0*cm, 25.5*cm, ': '+ str(StartDayTrade))
    canvas.drawString(5.0*cm, 26.0*cm, 'Fixed Rate')
    canvas.drawString(7.0*cm, 26.0*cm, ': '+ str(FixedRate))
    canvas.drawString(9.0*cm, 25.5*cm, 'Value Day')
    canvas.drawString(10*cm, 25.5*cm, ': '+ str(ValueDay))
    canvas.drawString(9.0*cm, 26.0*cm, 'Premium')
    canvas.drawString(10.0*cm, 26.0*cm, ': '+ str(formnum(Premium)))
    canvas.drawString(12.0*cm, 25.5*cm, 'Trade End Day')
    canvas.drawString(14*cm, 25.5*cm, ': '+ str(EndDayTrade))
    
    
    BuildHeader(1, t, date, canvas)
    
    # ########################## Cash Flows ################################## 
    
    count = 1
    
    
    for cfacm in cashFlows:
        cf = acm_to_ael(cfacm)
        
        Type     = cf.type
        StartDay = cf.start_day
        EndDay   = cf.end_day
        try:
            Days = int(cf.start_day.days_between(cf.end_day))
        except:
            print cf.type
        PayDay   = cf.pay_day
        Proj     = round((cf.projected_cf()*t.quantity), 2)
        Nominal  = round((cf.nominal_amount()*t.quantity), 2)
              
        cmx = cm * count  
               
        canvas.drawString(1.0*cm, 25.0*cm - cmx, ''+ str(Type))
        canvas.drawString(3.0*cm, 25.0*cm - cmx, ''+ str(formnum(Nominal)))
        canvas.drawString(6.0*cm, 25.0*cm - cmx, ''+ str(StartDay))
        canvas.drawString(9.0*cm, 25.0*cm - cmx, ''+ str(EndDay))
        canvas.drawString(12.0*cm, 25.0*cm - cmx, ''+ str(Days))
        canvas.drawString(15.0*cm, 25.0*cm - cmx, ''+ str(PayDay))
        canvas.drawString(18.0*cm, 25.0*cm - cmx, ''+ str(formnum(Proj)))
        
        
        count += 0.3
        
        if count > 15:
            canvas.showPage()
            count = 1
            BuildHeader(1, t, date, canvas)
            
