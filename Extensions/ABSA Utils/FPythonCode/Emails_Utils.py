"""--------------------------------------------------------------------------
MODULE
   Emails_Utils

DESCRIPTION
    This module houses a function for creating and sending out emails.

HISTORY 
Date: 2020-02-18
   
-----------------------------------------------------------------------------"""
import acm
from at_logging import getLogger
from at_email import EmailHelper
from collections import OrderedDict


LOGGER = getLogger(__name__)


def send_email(subject, body, recipients, cc_email):
    environment = acm.FDhDatabase['ADM'].InstanceName()
    # subject = "{0} {1} ({2})".format(subject, acm.Time.DateToday(), environment)
    email_helper = EmailHelper(
        body,
        subject,
        recipients,
        "Front Arena {0}".format(environment),
        None,
        "html"
    )
    email_helper.mail_cc = cc_email
    if str(acm.Class()) == "FACMServer":
        email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
        email_helper.host = EmailHelper.get_acm_host()

    try:
        email_helper.send()
    except Exception as exc:
        LOGGER.exception("Error while sending e-mail: %s", exc)


class TableEmail:
    report_data = OrderedDict()
    table_headings = list()
    columns = 1

    def __init__(self, subject, email_addresses, cc_email_addresses, sender=None, attachments=None):
        self.body = None
        self.email_addresses = email_addresses
        self.cc_email_addresses = cc_email_addresses
        self.subject = subject
        self.attachments = attachments
        self.sender = sender

    def add_rows(self, data):
        row_number = 1
        for line in data:
            self.add_row(str(row_number), [str(row_number)] + [str(item) for item in line.values()])
            row_number += 1

    def add_row(self, report_row_number, row_info_list):
        row_data = ''
        open_row = '<tr>'
        close_row = '</tr>'
        open_data_tag = '<td>'
        close_data_tag = '</td>'

        for row_info in row_info_list:
            row_data = row_data + open_data_tag + row_info + close_data_tag

        report_row = open_row + row_data + close_row
        TableEmail.report_data[report_row_number] = report_row

    def add_header(self, table_headings_list):
        table_headings = ''
        open_row = '<tr>'
        close_row = '</tr>'
        open_header_tag = '<th>'
        close_header_tag = '</th>'

        table_headings = open_header_tag + table_headings + close_header_tag

        for table_heading in table_headings_list:
            TableEmail.columns += 1
            table_headings = table_headings + open_header_tag + table_heading + close_header_tag

        header_row = open_row + table_headings + close_row
        TableEmail.table_headings.append(header_row)

    def create_report(self, report_header, table_headers=None, content=None):
        if content is None:
            content = TableEmail.report_data
        if table_headers is None:
            table_headers = TableEmail.table_headings
        report_content = ''

        if len(table_headers) > 0:
            table_headers = table_headers[0]
        else:
            table_headers = ''

        for row in content.keys():
            report_content = report_content + content[row]

        report = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
                "http://www.w3.org/TR/html4/strict.dtd">
                <html dir="ltr" lang="en">
                <head>
                    <meta http-equiv="content-type" content="text/html; charset=utf-8">
                    <meta http-equiv="content-style-type" content="text/css">
                    <title></title>
                    <style type="text/css">
                        table {
                            border-collapse: collapse;
                            font-family: Arial, Brave Sans, sans-serif;
                        }
                        th, td {
                            padding: 4px;
                            border: 1px solid #ddd;
                            white-space: nowrap;
                        }
                        th {
                            background-color: #dc0032;
                            color: white;
                        }
                        h1 {
                            color: 	#870032;
                        }
                        td {
                        }
                        .main_header {
                            background-color: #870032;
                        }
                    </style>
                </head>
                <body>
                    <p>Hi,</p><br>
                    <table>
                        <th class="main_header" colspan="%s">%s</th>
                        %s
                        %s
                    </table>
                    <br>
                    <p>Kind Regards,</p>
                    <p>FAFO - Termination Report</p>
                </body>
                </html>''' % (TableEmail.columns, report_header, table_headers, report_content)

        TableEmail.columns = 1
        self.body = report

    def send_report(self):
        LOGGER.info('Sending emails')
        email_helper = EmailHelper(
            body=self.body,
            subject=self.subject,
            mail_to=list(self.email_addresses),
            mail_cc=list(self.cc_email_addresses),
            mail_from=self.sender,
            attachments=self.attachments)

        if str(acm.Class()) == "FACMServer":
            email_helper.sender_type = EmailHelper.SENDER_TYPE_SMTP
            email_helper.host = EmailHelper.get_acm_host()
        try:
            email_helper.send()
        except Exception as e:
            LOGGER.warning("Exception: {0}\n".format(e))

        TableEmail.report_data.clear()
        TableEmail.table_headings[:] = []
