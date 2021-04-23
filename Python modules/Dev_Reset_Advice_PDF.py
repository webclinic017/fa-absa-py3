'''
This module builds an interface to build Swap,Cap and Floor advice Note in pdf

Changes
Date            Change Number   Developer         Description
02/10/2009                      Tshepo Mabena     Initial deployment
12/01/2010      197005          Tshepo Mabena     Enables the script to generate advice notes for BO-BO Confrimed trades
06/06/2014      CHNG0001770441  Bhavnisha Sarawan Changed the input to use a tradefilter, updated sections not open the pdf or display error pop ups for each run
2014/06/05      CHNG0002015587  Willie vd Bank    Added IndexLinkedSwap
2017                            Willie vd Bank    2017 FA upgrade - Reset start and end dates are not populated anymore
'''

import ael, acm
import os

from reportlab.pdfgen.canvas  import Canvas
from reportlab.lib.pagesizes  import A4
from Dev_Compound_Swap_Advice import BuildCompoundAdvice
from Dev_Compound_Swap_Advice import BuildWeightedAdvice
from Dev_Single_Swap_Advice   import BuildSingleAdvice
from Dev_Cap_Floor_Reset      import BuildAdvice
from Dev_CurrSwap_Advice      import BuildAdviceNote

def ASQL(*rest):
    acm.RunModuleWithParameters('Dev_Reset_Advice_PDF', 'Standard' )
    return 'SUCCESS'

def filters():
    return sorted(tf.fltid for tf in ael.TradeFilter)
default_path = ('Y:/Jhb/Operations Secondary Markets/DERIVATIVES/Swap Cap Floor Advice')
ael_variables = [('trdnbr', 'Trade Number:', 'string', None, 0),
                 ('filter', 'Filter', 'string', filters(), 'Dev_Reset_Advice_All_PDF', 0),
                 ('date', 'Date', 'string', ael.date_today(), ael.date_today(), 1),
                 ('output_folder', 'Output folder root', 'string', None, default_path)]


def ael_main(dict):

    try:
        date = ael.date(dict['date'])
    except:
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Invalid Date!", 0)
        return 'Invalid Date!'

    ClientName = ''
    tradelist = []

    #check that they only input trades or a trade filter. keeping the '0' dur to legacy processing
    if (dict['trdnbr'] != '0' and dict['trdnbr'] != '') and dict['filter'] != '':
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Cannot use both. Please remove either the trades or the trade filter.", 0)
        return 'Cannot use both. Please remove either the trades or the trade filter.'

    #check if trades are the input and add these to a list
    elif dict['trdnbr'] != '0' and dict['trdnbr'] != '':
        for trd in dict['trdnbr'].replace(' ', '').split(','):
            tradelist.append(trd)

    #check if trade filter is the input and add these to a list
    elif dict['filter'] != '':
        filter = dict['filter']
        tf = ael.TradeFilter[filter].trades()
        for trd in tf:
            tradelist.append(trd.trdnbr)

    root_path = dict['output_folder']

    #main processing
    if (dict['trdnbr'] != '0' and dict['trdnbr'] != '') or dict['filter'] != '':
        try:
            for trd in tradelist:
                t = ael.Trade[int(trd)]
                if t.counterparty_ptynbr.business_status_chlnbr is None or t.counterparty_ptynbr.business_status_chlnbr.entry not in ('Interbank'):

                    if t.insaddr.instype in ('Swap'):
                        ClientName = t.counterparty_ptynbr.fullname.replace('/', '')

                        asset_path = 'Swap Reset Advice'
                        file_name = 'SWAP RESET ADVICE' + ' ' + ' - ' + ClientName + ' '+ ' - ' + '(' +str(t.trdnbr)+ ')' + ' - '+ date.to_string('%d %b %Y') + '.pdf'
                        tmp = os.path.join(root_path, asset_path, file_name)

                        #moving this into the if statement so it doesn't open blank pdf where it cannot produce one

                        if t.status in ('BO Confirmed', 'BO-BO Confirmed'):
                            for cf in t.insaddr.cash_flows():
                                for r in cf.resets():
                                    if r.type in ('Weighted'):
                                        if date == r.start_day or date == cf.start_day:
                                            pdf = Canvas(tmp, pagesize = A4)
                                            BuildWeightedAdvice(1, t, date, pdf)
                                            break       #Have  to put a Break since there are many resets under one cash flow
                                    if r.type in ('Compound'):
                                        if date == r.start_day or date == cf.start_day:
                                            pdf = Canvas(tmp, pagesize = A4)
                                            BuildCompoundAdvice(1, t, date, pdf)
                                    if r.type in ('Single '):
                                        if date == r.start_day or date == cf.start_day:
                                            pdf = Canvas(tmp, pagesize = A4)
                                            BuildSingleAdvice(1, t, date, pdf)

                    elif t.insaddr.instype in ('Cap', 'Floor'):

                        ClientName = t.counterparty_ptynbr.fullname.replace('/', '')

                        asset_path = 'Cap Floor Reset Advice'
                        file_name = t.insaddr.instype.upper() + ' ' + ' RESET ADVICE ' + ' '+ ' - ' + ClientName + ' '+ ' - ' + '(' +str(t.trdnbr)+ ')' + ' - '+ date.to_string('%d %b %Y') + '.pdf'
                        tmp = os.path.join(root_path, asset_path, file_name)

                        pdf = Canvas(tmp, pagesize = A4)

                        if t.status not in ('Simulated', 'Terminated', 'Void'):
                            BuildAdvice(1, t, pdf, date)

                    elif t.insaddr.instype in ('CurrSwap'):

                        ClientName = t.counterparty_ptynbr.fullname.replace('/', '')

                        asset_path = 'Curr Swap Advice'
                        file_name = t.insaddr.instype.upper() + ' ' + ' RESET ADVICE '+ ' '+ ' - ' + ClientName + ' '+ ' - ' + '(' +str(t.trdnbr)+ ')' + ' - '+ date.to_string('%d %b %Y') + '.pdf'
                        tmp = os.path.join(root_path, asset_path, file_name)

                        pdf = Canvas(tmp, pagesize = A4)

                        if t.status not in ('Simulated', 'Terminated', 'Void'):
                            BuildAdviceNote(t, pdf, date)

                    elif t.insaddr.instype in ('IndexLinkedSwap'):
                        ClientName = t.counterparty_ptynbr.fullname.replace('/', '')

                        asset_path = 'Swap Reset Advice'
                        file_name = 'INDEX LINKED SWAP RESET ADVICE' + ' ' + ' - ' + ClientName + ' '+ ' - ' + '(' +str(t.trdnbr)+ ')' + ' - '+ date.to_string('%d %b %Y') + '.pdf'
                        tmp = os.path.join(root_path, asset_path, file_name)

                        if t.status in ('BO Confirmed', 'BO-BO Confirmed', 'Terminated'):
                            for cf in t.insaddr.cash_flows():
                                for r in cf.resets():
                                    if r.type in ('Nominal Scaling'):
                                        if date == r.start_day or date == cf.start_day:
                                            pdf = Canvas(tmp, pagesize = A4)
                                            BuildWeightedAdvice(1, t, date, pdf)
                                    if r.type in ('Compound'):
                                        if date == r.start_day or date == cf.start_day:
                                            pdf = Canvas(tmp, pagesize = A4)
                                            BuildCompoundAdvice(1, t, date, pdf)

                    try:
                        pdf.save()
                    except Exception as ex:
                        print "PDF not saved for trade {0}".format(trd)
                        print ex

        except Exception, e:
            # removed the pop up as a trade filter may return many trades that are not applicable resulting in numerous pop ups.
            print e
            print 'Invalid entry. Check Trade number and reset date.'
            raise

