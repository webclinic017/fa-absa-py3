"""-----------------------------------------------------------------------------
PURPOSE                 :  This script serves as a template for the notification,
                           which will be sent out as an email 
                           to the specified destinations.
DEVELOPER               :  Katerina Frickova
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no       Developer            Description
--------------------------------------------------------------------------------
2021-02-15  FAPE-505        Katerina Frickova    Initial Implementation

"""

import acm
from at_email import EmailHelper
from at_logging import getLogger
from textwrap import dedent
from at_time import to_datetime

LOGGER = getLogger(__name__)
CURRENT_TIME = to_datetime(acm.Time.TimeNow())
DATE_TODAY = acm.Time.DateToday()


class CreateEmailReport(object):
    SUBJECT = '{main_subject} Notification - {date_today} - {env}'
    REPORT_BODY = dedent("""\
        <html>
          <head>
            <style type="text/css">p {{margin:0}}</style>
          </head>
          <body>
            <p>{description}
            <div>{table}</div>
            </p>
          </body>
        </html>
        """)

    def __init__(self, table_header_tuple, table_rows_list):
        self.table_header = table_header_tuple
        self.table_rows = table_rows_list

    def to_html_table(self):
        res_text = '<table style="table-layout: auto" border="2">'
        res_text += "<tr>" + "".join(map("<th>{0}</th>".format, self.table_header)) + "</tr>"
        for row in self.table_rows:
            line = "<tr>" + "".join(map("<td>{0}</td>".format, row)) + "</tr>"
            res_text += line
        return res_text + "</table>"
    
    def to_html_description(self):
        raise NotImplementedError
        
    def get_body(self):
        
        return self.REPORT_BODY.format(
            date_today=DATE_TODAY,
            current_time=CURRENT_TIME.strftime("%Y-%m-%d %H:%M:%S"),
            description=self.to_html_description(),
            table=self.to_html_table())
    
    def get_env_name(self):
        return acm.FInstallationData.Select('').At(0).Name()
    
    def send_mail(self, subject, email_to):
        message = EmailHelper(
            body=self.get_body(),
            subject=self.SUBJECT.format(main_subject=subject, date_today=DATE_TODAY, env=self.get_env_name()),
            mail_to=email_to.split(','),
            sender_type=EmailHelper.SENDER_TYPE_SMTP,
            host=EmailHelper.get_acm_host())
        message.send()
        
        
