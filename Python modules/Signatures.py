from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units     import cm
from PIL                     import Image   

def Signatures(canvas, t):

    canvas.setFont("Helvetica", 8.0)    
    canvas.drawString(1.5 * cm, 27.43*cm, 'Yours faithfully,')
    canvas.setFont("Helvetica-Bold", 10.0)
    canvas.drawString(1.5 * cm, 26.5*cm, 'Absa Bank Limited')
        
    canvas.setFont("Helvetica", 10.0)
    canvas.drawInlineImage('Y:/Jhb/Arena/Data/Confirmations/Signatures/LRoux.jpg', 1.5*cm, 24.5 *cm, 2.5*cm, 1.2*cm)
    canvas.drawString(1.5 * cm, 24.5*cm, 'L Roux')
    canvas.drawString(1.5 * cm, 24.0*cm, 'B77785')
    canvas.drawString(1.5 * cm, 23.5*cm, 'Administrator')
    canvas.drawString(1.5 * cm, 23.0*cm, 'Confirmations')
    canvas.drawString(1.5 * cm, 22.5*cm, 'VAT No. 4940112230')
    
    canvas.drawInlineImage('Y:/Jhb/Arena/Data/Confirmations/Signatures/MJacobs.jpg', 1.5*cm, 20.5 *cm, 2.5*cm, 1.2*cm)
    canvas.drawString(1.5 * cm, 20.5*cm, 'M R Jacobs')
    canvas.drawString(1.5 * cm, 20.0*cm, 'A74349')
    canvas.drawString(1.5 * cm, 19.5*cm, 'Team Leader')
    canvas.drawString(1.5 * cm, 19.0*cm, 'Confirmations')
    canvas.drawString(1.5 * cm, 18.5*cm, 'VAT No. 4940112230')
    
    canvas.drawString(1.5 * cm, 17.5*cm, 'Agreed and Accepted By:')
    canvas.setFont("Helvetica-Bold", 10.0)
    canvas.drawString(1.5 * cm, 17.0*cm, t.counterparty_ptynbr.fullname)
    
    canvas.setFont("Helvetica", 10.0)
    canvas.drawString(1.5 * cm, 15.5*cm, 'Name: '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 14.5*cm, 'signed:'+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 13.5*cm, 'Title:    '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 12.5*cm, 'Date:   '+'           '+ '_'*25)
    
    canvas.drawString(1.5 * cm, 11.0*cm, 'Name: '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 10.0*cm, 'signed:'+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 9.0*cm, 'Title:    '+'           '+ '_'*25)
    canvas.drawString(1.5 * cm, 8.0*cm, 'Date:   '+'           '+ '_'*25)
    
    canvas.showPage()  
