import os

import XMLReport
from XMLReport import mkcaption

class Report(XMLReport.StatementReportBase):
    def client_address(self):
        return { 'name': 'Dear client', 'address': ['99 Grayston Drive', 'Sandton'] }
    
    def statement_detail(self):
        yield mkcaption('Hello world!')

ael_variables = [['path', 'Output folder', 'string', None, 'C:/', 1, 0]]

def ael_main(params):
    report = Report()
    xml = report.create_report()
    gen = XMLReport.XMLReportGenerator(params['path'])
    pdffile = gen.create(xml, 'report')
    os.startfile(pdffile)
