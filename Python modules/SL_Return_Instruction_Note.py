'''
Purpose:    [Creates PDF return or receipt note for security loan],[Changed dynamics to run for specific date],[Changed to include AddInfo dynamics],
            [Updated ASQL filter],[Updated to Add_Info update function],[Sort trades by UndIns, format quantities]
Department: [Securities Lending],[SL OPS],[SL OPS],[SL OPS],[SL OPS],[SL OPS]
Requester:  [Linda Breytenbach],[Halima Malick],[Halima Malick],[Halima Malick],[Halima Malick],[Halima Malick]
Developer:  [Willie van der Bank],[Willie van der Bank],[Willie van der Bank],[Willie van der Bank],[Willie van der Bank],[Willie van der Bank]
CR Number:  [C656249 (19/05/2011)],[838797 (24/11/2011)],[852482 08/12/2011],[871448 12/01/2012],[890126 09/02/2012],[892082 17/02/2012]
'''

import ael, reportlab.lib.pagesizes, os, acm, time

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.units     import cm, inch
from reportlab.lib           import colors
from reportlab.lib.colors    import black, red
from STATIC_TEMPLATE         import Securities_Header, Securities_Footer
from zak_funcs               import formnum

def Top_Part(PartyID, Term, Type, Partyname):
    Securities_Header(Term)
    Term.setFont("Helvetica", 10.0)
    Term.drawString(1.0 *cm, 25.5*cm, 'Absa Capital Custody and Trustees')
    Term.drawString(1.0 *cm, 25.0*cm, 'STRATE Settlement Department')    
    Term.drawString(1.1 *cm, 21.0*cm, 'Counterparty details')
    
    Term.drawString(1.1 *cm, 20.5*cm, 'Counterparty Name                ABSA lending desk')
    Term.drawString(1.1 *cm, 20.0*cm, 'Counterparty CSDP                ABSA Bank')
    Term.line(1.0 *cm, 20.8 *cm, 9.0 *cm, 20.8 *cm)     #Top line
    Term.line(1.0 *cm, 19.9 *cm, 9.0 *cm, 19.9 *cm)     #Bottom line
    Term.line(1.0 *cm, 20.8 *cm, 1.0 *cm, 19.9 *cm)     #Left vertical
    Term.line(9.0 *cm, 20.8 *cm, 9.0 *cm, 19.9 *cm)     #Right vertical
    Term.line(4.7 *cm, 20.8 *cm, 4.7 *cm, 19.9 *cm)     #Centre vertical
    Term.line(1.0 *cm, 20.35 *cm, 9.0 *cm, 20.35 *cm)   #Centre line
    
    Term.drawString(1.1 *cm, 18.0 *cm, 'Link Ref')
    Term.drawString(3.1 *cm, 18.0 *cm, 'ISIN')
    Term.drawString(5.8 *cm, 18.0 *cm, 'JSE Code')
    Term.drawString(7.6 *cm, 18.0 *cm, 'Quantity')
    Term.drawString(10.6 *cm, 18.0 *cm, 'Trade Date')
    Term.drawString(12.6 *cm, 18.0 *cm, 'Settlement Date')
    Term.drawString(15.6 *cm, 18.0 *cm, 'Delivery Mode')
    Term.setStrokeColorRGB(0, 0, 0)
    Term.line(1.0 *cm, 18.4 *cm, 20.5 *cm, 18.4 *cm)     #Top line
    Term.line(1.0 *cm, 17.9 *cm, 20.5 *cm, 17.9 *cm)     #Bottom line
    Term.line(1.0 *cm, 18.4 *cm, 1.0 *cm, 17.9 *cm)      #Left vertical
    Term.line(20.5 *cm, 18.4 *cm, 20.5 *cm, 17.9 *cm)    #Right vertical
    Term.line(3.0 *cm, 18.4 *cm, 3.0 *cm, 17.9 *cm)      #Inner vertical
    Term.line(5.7 *cm, 18.4 *cm, 5.7 *cm, 17.9 *cm)      #Inner vertical
    Term.line(7.5 *cm, 18.4 *cm, 7.5 *cm, 17.9 *cm)      #Inner vertical
    Term.line(10.5 *cm, 18.4 *cm, 10.5 *cm, 17.9 *cm)    #Inner vertical
    Term.line(12.5 *cm, 18.4 *cm, 12.5 *cm, 17.9 *cm)    #Inner vertical
    Term.line(15.5 *cm, 18.4 *cm, 15.5 *cm, 17.9 *cm)    #Inner vertical
    
    if Type == 'Receipt':
        Line1 = 'RECEIPT OF SHARES BORROWED'
        Line2 = 'Please ACCEPT the following shares:'
        Line3 = 'Shares to be Recieved'
        if Partyname == 'ABCAP SEC ABSA SEC LEND LENDING':
            Line1 = 'SHARES RETURN FROM LENDER'
        
        Term.drawString(18.1 *cm, 18.0 *cm, 'Loan Value')
        Term.line(18.0 *cm, 18.4 *cm, 18.0 *cm, 17.9 *cm)    #Inner vertical
    else:
        Line1 = 'RETURN OF SHARES BORROWED'
        Line2 = 'Please RETURN the following shares:'
        Line3 = 'Shares to be Delivered'
        if Partyname == 'ABCAP SEC ABSA SEC LEND LENDING':
            Line1 = 'SHARES BORROWED TO LENDER'
    
    Term.drawString(1.0 *cm, 23.5*cm, Line1)
    Term.drawString(1.0 *cm, 22.0*cm, Line2)
    Term.drawString(1.0 *cm, 19.0 *cm, Line3)
                
def Bottom_Part(Term, HPlace, Type):
    Securities_Footer(Term)
    Term.setFont("Helvetica", 10.0)
    Term.drawString(1.0 *cm, HPlace *cm, 'Change in beneficial ownership:')
    if Type == 'Receipt':
        Term.drawString(9.0 *cm, HPlace *cm, 'No - Securities Return')
    else:
        Term.drawString(9.0 *cm, HPlace *cm, 'No - Securities Loan')
    Term.drawString(1.0 *cm, (HPlace-1) *cm, 'Please only act on these instructions if signed in terms of the authorized signatories mandate in your possession.')
    Term.drawString(1.0 *cm, (HPlace-2) *cm, 'Yours sincerely')
    Term.drawString(1.0 *cm, (HPlace-3) *cm, '____________________')
    Term.drawString(9.0 *cm, (HPlace-3) *cm, '____________________')
    Term.drawString(2.0 *cm, (HPlace-3.5) *cm, '"A" Signature')
    Term.drawString(10.0 *cm, (HPlace-3.5) *cm, '"B" Signature   ')

def AllTrades(RepDate, Partyname, Filter):
    
    selectASQL = """select
    t.trdnbr,
    t.contract_trdnbr,
    t.value_day  = to_date(@Date) ? 'Start' : 'End'    'Date',
    p.ptyid,
    i.open_end,
    add_info(t,'SL_Instruction_Note')   'AddInfo',
    display_id(i,'und_insaddr') 'JSECode'
into trades
from
    trade t,
    instrument i,
    party p,
    leg l
where
        t.insaddr = i.insaddr
    and l.insaddr = i.insaddr
    /*and i.instype = 'SecurityLoan'
    and t.status = 'BO Confirmed'
    and (t.quantity > 0
    or t.quantity < 0)*/
    and match_filter(t, @Filter)
    and t.counterparty_ptynbr = p.ptynbr
    and p.ptyid = @Party
    and (t.value_day = to_date(@Date)
    /*or i.exp_day = to_date(@Date))*/
    or l.end_day = to_date(@Date))

select
    t.contract_trdnbr,
    count(*)    'Count'
into Parents
from
    trades t
group by t.contract_trdnbr

select
    t.trdnbr,
    t.contract_trdnbr,
    p.Count,
    t.Date,
    t.ptyid,
    t.open_end,
    t.AddInfo,
    t.JSECode
into final
from
    trades t,
    trade tt,
    parents p
where
        t.contract_trdnbr *= p.contract_trdnbr
    and tt.trdnbr = t.trdnbr
    and ((p.Count ~= 1 and t.Date = 'Start') or p.Count = 1)
order by t.contract_trdnbr

select
    f.trdnbr,
    f.contract_trdnbr,
    f.Count,
    f.Date,
    f.ptyid,
    f.open_end,
    f.AddInfo,
    f.JSECode
from
    final f
where
        f.AddInfo ~= 'Sent'
    and ((f.Date = 'End' and f.open_end = 'Terminated') or f.Date ~= 'End')
    and ((f.AddInfo = 'Partial' and f.Date = 'End') or f.AddInfo ~= 'Partial')
    order by f.JSECode,f.contract_trdnbr"""
    
    trades = ael.asql(selectASQL, 0, ['@Date', '@Party', '@Filter'], ["'" + str(RepDate) + "'", "'" + Partyname + "'", "'" + Filter + "'"])[1][0]

    return trades
    
def Instruction_Note(Partyname, path, RepDate, DeliveryMode, TradeDate, Filter, UpdateAddInfoYesNo):
    Receipt = []
    Return = []
    Trades = AllTrades(RepDate, Partyname, Filter)
    NoTrades = 'Yes'
    for trd in Trades:
        asqlDate = trd[3]
        acmtrd = acm.FTrade[trd[0]]
        Amount = acmtrd.QuantityInUnderlying()
        acmtrdTrans = acmtrd.TrxTrade()
        DiffAmount = abs(Amount - acmtrdTrans.QuantityInUnderlying())
        if trd[2] == 2:  #Check the number of connected trades
            if Amount > 0:
                Return.append([acmtrd, DiffAmount, asqlDate])
            else:
                Receipt.append([acmtrd, DiffAmount, asqlDate])
        elif trd[2] == 1:
            if (Amount > 0 and trd[3] == 'Start') or (Amount < 0 and trd[3] == 'End'):
                Receipt.append([acmtrd, Amount, asqlDate])
            else:
                Return.append([acmtrd, Amount, asqlDate])
    if len(Receipt) > 0:
        Type = 'Receipt'
        PDFBuild(Partyname, path, Type, Receipt, DeliveryMode, TradeDate, RepDate, UpdateAddInfoYesNo)
        NoTrades = 'No'
    
    if len(Return) > 0:
        Type = 'Return'
        PDFBuild(Partyname, path, Type, Return, DeliveryMode, TradeDate, RepDate, UpdateAddInfoYesNo)
        NoTrades = 'No'
        
    if NoTrades == 'Yes':
        print 'No matching trades.'
        func=acm.GetFunction('msgBox', 3)
        func("Note", "No matching trades found.", 0)
    
def PDFBuild(Partyname, path, Type, Quant, DeliveryMode, TradeDate, RepDate, UpdateAddInfoYesNo):
    #Today = ael.date_today()
    t_list = time.localtime()
    nowtime = (str)(t_list[3]) + (str)(t_list[4]) + (str)(t_list[5])
    filename = Type + " instruction Note " + str(Partyname) + ' ' + RepDate.to_string("%d %B %Y") + ' ' + nowtime
    
    pdf = PDFCreate(filename, path, Type)
    if pdf == '':
        return
        
    Top_Part(Partyname, pdf, Type, Partyname)
    
    counter = 17.6
    bottom = 8.5
    
    for acmtrd in Quant:
        if counter <= (bottom - 5):         #When more than one page is required, footer will be replaced by trade data.
            pdf.showPage()
            Top_Part(Partyname, pdf, Type, Partyname)
            counter = 17.5            
        ListTrades(pdf, counter, acmtrd[0], acmtrd[1], Type, DeliveryMode, RepDate, TradeDate)
        counter = counter - 0.4
            
    if counter <= bottom:
        pdf.showPage()
        Top_Part(Partyname, pdf, Type, Partyname)
    Bottom_Part(pdf, bottom, Type)

    pdf.save()
    print 'File ' + path + filename + '.pdf created.'
    
    #Only after PDF gets saved successfully, Trade Add_Infos will be updated
    
    if UpdateAddInfoYesNo == 'yes':
        UpdateAddInfo(Quant)
    
        
def ListTrades(Term, HPlace, acmtrd, qty, Type, DeliveryMode, RepDate, TradeDate):
    Term.setFont("Helvetica", 8.0)
    Term.drawString(1.1 *cm, HPlace *cm, str(acmtrd.ContractTrdnbr()))                                                                  #Link Ref
    Term.drawString(3.1 *cm, HPlace *cm, acmtrd.Instrument().Underlying().Isin())                                                       #ISIN
    Term.drawString(5.8 *cm, HPlace *cm, acmtrd.Instrument().Underlying().Name()[4:len(acmtrd.Instrument().Underlying().Name())])       #JSE Code
    Term.drawString(7.6 *cm, HPlace *cm, str(formnum(qty)[0:len(formnum(qty))-3]))                                                      #Quantity
    Term.drawString(10.6 *cm, HPlace *cm, acm.Time.AsDate(TradeDate))                                                                   #Trade Date
    Term.drawString(12.6 *cm, HPlace *cm, acm.Time.AsDate(RepDate))                                                                     #Settlement Date
    Term.drawString(15.6 *cm, HPlace *cm, DeliveryMode)                                                                                 #Delivery Mode
    
    #Frame
    Term.line(1.0 *cm, (HPlace - 0.08) *cm, 20.5 *cm, (HPlace - 0.08) *cm)     #Bottom line
    Term.line(1.0 *cm, (HPlace + 0.4) *cm, 1.0 *cm, (HPlace - 0.08) *cm)       #Left vertical
    Term.line(20.5 *cm, (HPlace + 0.4) *cm, 20.5 *cm, (HPlace - 0.08) *cm)     #Right vertical
    Term.line(3.0 *cm, (HPlace + 0.4) *cm, 3.0 *cm, (HPlace - 0.08) *cm)       #Inner vertical
    Term.line(5.7 *cm, (HPlace + 0.4) *cm, 5.7 *cm, (HPlace - 0.08) *cm)       #Inner vertical
    Term.line(7.5 *cm, (HPlace + 0.4) *cm, 7.5 *cm, (HPlace - 0.08) *cm)       #Inner vertical
    Term.line(10.5 *cm, (HPlace + 0.4) *cm, 10.5 *cm, (HPlace - 0.08) *cm)     #Inner vertical
    Term.line(12.5 *cm, (HPlace + 0.4) *cm, 12.5 *cm, (HPlace - 0.08) *cm)     #Inner vertical
    Term.line(15.5 *cm, (HPlace + 0.4) *cm, 15.5 *cm, (HPlace - 0.08) *cm)     #Inner vertical
    
    if Type == 'Receipt':
        LoanVal = qty * acmtrd.RefPrice() * acmtrd.Instrument().Underlying().Quotation().QuotationFactor()
        Term.drawString(18.1 *cm, HPlace *cm, str(formnum(LoanVal)))
        Term.line(18.0 *cm, (HPlace + 0.4) *cm, 18.0 *cm, (HPlace - 0.08) *cm)     #Inner vertical
    
def UpdateAddInfo(Quant):       
    for trdlist in Quant:
        if trdlist[2] == 'End':
            AddInfo = 'Sent'
        else:
            AddInfo = 'Partial'
        
        UdateAddInfoMacro(1, AddInfo, trdlist[0].Oid())
        
def UdateAddInfoMacro(temp,AddInfo,trade,*rest):
    try:
        trd = ael.Trade[trade]
        found = 0
        for ai in trd.additional_infos():
            if ai.addinf_specnbr.field_name == 'SL_Instruction_Note':
                found = 1
                ai_found = ai
        if found == 1:
            aicln = ai_found.clone()
            aicln.value = AddInfo
            aicln.commit()
        else:
            tcln = trd.clone()
            ai_new = ael.AdditionalInfo.new(tcln)
            ais = ael.AdditionalInfoSpec['SL_Instruction_Note']
            ai_new.addinf_specnbr = ais
            ai_new.value = AddInfo
            ai_new.commit()
        print 'Add_Info(SL_Instruction_Note) on trade', trd.trdnbr, 'set to "' + AddInfo + '".'
        ael.poll()
        
        return 'Updated'
        
    except:
        return 'Failed'
        
def PDFCreate(filename, path, Type):
    if ael.user().grpnbr.grpid not in ('Integration Process', 'System Processes'):
        if os.path.exists(path):
            tmppdf = path + filename + ".pdf"
            if os.path.exists(tmppdf):
                print 'File already exists.'
                func=acm.GetFunction('msgBox', 3)
                func("File already exists.", "Please delete file or select different path.", 0)
                return ''
        else:
            try:
                os.mkdir(path)
                tmppdf = path + filename + ".pdf"
                print 'Folder ' + path + ' created.'
            except:
                'Path "' + path + '" can not be created!'

    tmppdf = path + filename + ".pdf"
    pdf = Canvas(tmppdf, pagesize = A4 )
    return pdf

def parties():
    parties = []
    for p in ael.Party:
        parties.append(p.ptyid)
    parties.sort()
    return parties
    
def filters():
    filters = []
    for f in ael.TradeFilter:
        filters.append(f.fltid)
    filters.sort()
    return filters

ael_variables = [('PartyID', 'Counter Party', 'string', parties(), ''),
                 ('RepDate', 'Settlement Date', 'date', [ael.date_today()], ael.date_today(), 1),
                 ('tf', 'TradeFilter_Trade Filter', 'string', filters(), 'SL_Return_Instruction_Note'),
                 ('Folder', 'Output Path_Path', 'string', '', 'f://', 1),
                 ('DeliveryMode', 'Delivery Mode_Static Fields', 'string', ['On Market'], 'On Market'),
                 ('UpdateAddInfoYesNo', 'Update additional info?', 'string', ['yes', 'no'], 'yes'),
                 ('TradeDate', 'Trade Date_Static Fields', 'string', [ael.date_today()], ael.date_today())]

def ael_main(dict):
    Partyname = dict['PartyID']
    path = dict['Folder']
    tf = dict['tf']
    RepDate = dict['RepDate']
    TradeDate = dict['TradeDate']
    DeliveryMode = dict['DeliveryMode']
    UpdateAddInfoYesNo = dict['UpdateAddInfoYesNo']
    print 'Loading...'
    Instruction_Note(Partyname, path, RepDate, DeliveryMode, TradeDate, tf, UpdateAddInfoYesNo)
    print 'Done...'

def ASQL(*rest):
    acm.RunModuleWithParameters('SL_Return_Instruction_Note', 'Standard')
    return 'Done'
