'''-----------------------------------------------------------------------
MODULE
  NonZAR_Deal_Ticket_PDF

DESCRIPTION
  The NonZAR_Deal_Ticket_PDF is called from the trading manager, when the save deal ticket button is clicked. 
  This script creates the PDF deal ticket and saves it to the shared drive.

History:
Date            Who                     What
2009-03-26	Herman Hoon             CR 381305: Non ZAR Funding - Print the PDF deal ticket to the shared drive.

ENDDESCRIPTION
-----------------------------------------------------------------------'''

import ael, acm, os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm, inch
from reportlab.lib.colors    import black 
from zak_funcs import formnum

def setSaved(trdnbr, status):
        entity = ael.Trade[trdnbr]
        found = 0
        spec = ael.AdditionalInfoSpec['NonZAR_Status']
        for ai in entity.additional_infos():
            if ai.addinf_specnbr == spec:
                found = 1
                break
                
        if found == 1:
            ai_c = ai.clone()
            ai_c.value = status
            ai_c.commit()
        else:
            e_c = entity.clone()
            ai_new = ael.AdditionalInfo.new(e_c)
            ai_new.value = status
            ais = ael.AdditionalInfoSpec['NonZAR_Status']
            ai_new.addinf_specnbr = ais
            ai_new.commit()
        ael.poll()
        return

            
def dynamic(c, trdnbr, y):
    #GET THE DYNAMIC DATA#
    #Trade data
    t = ael.Trade[trdnbr]
    dealDate    = ael.date_from_time(t.time)
    #valueDate   = t.value_day
    amount      = formnum(abs(t.nominal_amount()))
    counterParty= t.counterparty_ptynbr.ptyid
    midasNumber = t.counterparty_ptynbr.add_info('Midas_Nbr')
    dealer      = t.trader_usrnbr.name
    dealMethod  = t.add_info('NonZAR_Deal Method')
    dealType    = t.add_info('NonZAR_Deal Type')
    branchMargin= t.add_info('NonZAR_BranchMargin')
    costOfFunds = t.add_info('NonZAR_CostOfFunds')
    liborRate   = t.add_info('NonZAR_Libor Rate')
    branch      = t.add_info('NonZAR_Branch')
    centreCode  = t.add_info('NonZAR_Centre Code')
    comments    = t.add_info('NonZAR_Comments')
    
    #Instrument data
    i = t.insaddr
    #matDate     = i.exp_day
    currency    = i.curr.insid
    
    #Leg data
    l = i.legs()[0]
    fixedRate   = l.fixed_rate
    valueDate   = l.start_day
    matDate     = l.end_day
    
    #CashFlow data
    interest = 0
    for cf in i.cash_flows():
        if cf.type == 'Fixed Rate':
            interest =  formnum(abs(cf.projected_cf()*t.quantity))
    
    #Dealer data
    today =ael.date_today().to_string('%d/%m/%Y')
    
    #List of dynamic output
    list = [
            [('Front Arena Trade Nbr', trdnbr, 2)],
            
            [('Deal Method', dealMethod, 0),
             ('Deal Type', dealType, 0)],
            
            [('Customer', counterParty, 0),
            ('Customer Midas', midasNumber, 0)],
            
            [('Deal Date', dealDate, 0),
            ('Value Date', valueDate, 0),
            ('Maturity Date', matDate, 0)],
            
            [('Currency', currency, 0),
            ('Amount', amount, 0),
            ('Total Interest', interest, 0)],
            
            [('Branch Margin', branchMargin, 1),
            ('Cost of Funds', costOfFunds, 1),
            ('Libor Rate', liborRate, 1),
            ('Fixed Rate', fixedRate, 1)],
            
            [('Branch', branch, 0),
             ('Centre Code', centreCode, 0)],
             
            [('Additional comments', comments, 0)],               
             
            [('Deal booked by', dealer, 0),
             ('Deal ticket printed on ', today, 0)] 
            ]
            
    #Coordinates
    x1 = 2*cm
    x2 = 7*cm
    
    #Print the output
    c.setFont("Helvetica", 12.0)
    for l1 in list:
        for l in l1:
            #Normal output
            if l[2] == 0:
                c.drawString(x1, y*cm, l[0])
                c.drawString(x2, y*cm, ': ' + str(l[1]))
                y = y - 0.5
            #Rates
            elif l[2] == 1:
                c.drawString(x1, y*cm, l[0])
                c.drawString(x2, y*cm, ': ' + str(l[1]) + '%')
                y = y - 0.5
            #Deal ticket number
            elif l[2] == 2:
                c.setFont("Helvetica", 12.0)
                c.drawString(x1, y*cm, l[0])
                c.drawString(7*cm, y*cm, ': ' + str(l[1]))
                c.setFont("Helvetica", 12.0)
                y = y - 1
        y = y - 0.5
    
    return (c, y)

def static(c, y):
    x1 = 2
    x2 = 6
    x3 = 13
    y = y-2
    c.drawString(x1*cm, y*cm, 'Deal captured by  : ')
    c.drawString(x2*cm, y*cm, '_________________________  on ')
    c.drawString(13*cm, y*cm, '______________________')
    y = y - 0.5
    c.drawString(x2*cm, y*cm, 'Name')
    c.drawString(13*cm, y*cm, 'Date')
    y = y - 2
    c.drawString(x3*cm, y*cm, '______________________')
    y = y - 0.5
    c.drawString(x3*cm, y*cm, 'Signature')
    return (c, y)

       
def main(tradeNumber):
    #SHARED DRIVE LOCATION
    dir = 'Y:\\JHB\\FrontArena NonZar Deal Tickets\\'
    #dir = 'F:\\FrontArena NonZar Deal Tickets\\'
    #get back office deal number
    t = ael.Trade[tradeNumber]
    dealNumber = t.add_info('NonZAR_Deal Number')
    
    pdfDir = dir + 'NonZAR_Deal Ticket_' + str(dealNumber) + '_v1.pdf'
    
    #Check if the file already exists
    #Create new version if the file already exists
    i = 1
    while os.path.isfile(pdfDir):
        i = i + 1
        pdfDir = dir + 'NonZAR_Deal Ticket_' + str(dealNumber) + '_v'+ str(i) +'.pdf'

    #Create PDF
    c = Canvas(pdfDir, pagesize = A4)
    c.setFillColor(black)
    c.setFont("Helvetica", 10.0)

    #Title
    y = 26
    c.setFont("Helvetica", 20.0)
    c.drawString(2*cm, y*cm, 'Non ZAR Loans & Deposits Deal Ticket  ' + str(dealNumber))
    y = y-1
    c.setFont("Helvetica", 20.0)
    c.drawString(2*cm, y*cm, 'Version ' + str(i))
    y = y-2
    #Create dynamic and static data
    (c, y) = dynamic(c, tradeNumber, y)
    (c, y) = static(c, y)
    c.showPage()
    
    try:
        #set status to saved
        c.save()
        setSaved(tradeNumber, 'Saved')
    except:
        func = acm.GetFunction('msgBox', 3) 
        msg = 'Unable to save PDF File.\nPlease make sure the file is not in use.\nOr make sure you have access to ' + dir
        ret = func('Warning', msg, 0)
        return
    
    os.startfile(pdfDir)
