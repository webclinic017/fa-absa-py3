"""Helper classes and functions for sending e-mails from Front Arena.

History
=======
2015-04-02 Andrei Conicov    Initial implementation.
2015-11-09 Vojtech Sidorin   ABITFA-3820: Strip leading and trailing whitespaces from e-mail addresses before sending.
2015-12-09 Evgeniya Baskaeva ABITFA-4010 - at_email module handle exceptions in _get_outlook_mail() and _send_SMTP()
2017-03-23 Gabriel Marko     CHNG0004439301 - Retry functionality added to EmailHelper
2019-02-12 Libor Svoboda     CHG1001362755 - Improve the Retry functionality
2019-06-04 Libor Svoboda     CHG1001834527 - Add SMTP timeout; raise if SMTP fails to send email
2020-01-09 Iryna Shcherbina  FAPE-181 - Make RTB the default sender
"""
import os
import smtplib
import mimetypes
import email.mime
import email.mime.application  # do not remove, email.mime is not enough

import sys
import acm
import time
import at_logging

LOGGER = at_logging.getLogger()
RTB_EMAIL = 'ABCapITRTBAMFrontAre@absa.africa'


class Error(Exception):
    """Base class for other exceptions"""
    pass


class AttachmentError(Error):
    pass


class BodyTypeError(Error):
    pass


class EmailHelper(object):

    SENDER_TYPE_OUTLOOK = "Outlook"
    SENDER_TYPE_SMTP = "SMTP"

    BODY_TYPE_HTML = "html"
    BODY_TYPE_TXT = "txt"

    @staticmethod
    def get_acm_host():
        """Returns the mailServerAddress from acm

        Example: 'smtphost.bzwint.com'
        """
        return acm.GetCalculatedValue(0, acm.GetDefaultContext().Name(),
                                      'mailServerAddress').Value()

    def __init__(self,
                 body,
                 subject,
                 mail_to,
                 mail_from=RTB_EMAIL,
                 attachments=None,
                 body_type=BODY_TYPE_HTML,
                 sender_type=SENDER_TYPE_OUTLOOK,
                 host=None,
                 mail_cc=None,
                 mail_bcc=None,
                 retries=5,
                 smtp_timeout=60,
                 smtp_port=25):
        """
        mail_from = 'PRIME client'  # "andrei.conicov@barclays.com"
        mail_to = ["andrei.conicov@barcap.com"]
        subject = "test email"
        body = "Test body"
        attachments = [r'F:\SAMM\DAILY_100719-10571225_20140312_437.pdf']
        body_type=html || txt
        sender_type = EmailHelper.SENDER_TYPE_OUTLOOK || EmailHelper.SENDER_TYPE_SMTP
        host=smtphost.bzwint.com
        mail_cc = ["andrei.conicov@barcap.com"]
        mail_bcc = ["andrei.conicov@barcap.com"]
        """
        self.retries = retries
        if not mail_cc:
            mail_cc = []
        if not mail_bcc:
            mail_bcc = []
        if not attachments:
            attachments = []
        if not isinstance(mail_to, list):
            raise Exception("The 'mail_to' has to be a list of email addresses.")
        if not isinstance(mail_cc, list):
            raise Exception("The 'mail_cc' has to be a list of email addresses.")
        if not isinstance(mail_bcc, list):
            raise Exception("The 'mail_bcc' has to be a list of email addresses.")
        if not isinstance(attachments, list):
            raise Exception("The 'attachments' has to be a list of file paths.")

        self.body = body
        self.subject = subject
        self.mail_to = [self.validate_email(e) for e in mail_to]
        self.mail_cc = [self.validate_email(e) for e in mail_cc]
        self.mail_bcc = [self.validate_email(e) for e in mail_bcc]
        self.mail_from = self.validate_email(mail_from)
        self.attachments = attachments
        self.body_type = body_type
        self.sender_type = sender_type
        self.host = host
        self.smtp_timeout = smtp_timeout
        self.smtp_port = smtp_port

    def send(self, log=True):
        """Send an email according to the provided sender_type attribute  value"""
        if log:
            LOGGER.info("""'at_email: Using {0} to send email
            TO:{1}, CC:{2}, BCC:{3}
            Attachments: {4}""".format(self.sender_type,
                                       self.mail_to,
                                       self.mail_cc,
                                       self.mail_bcc,
                                       ";".join(self.attachments)))

        if self.sender_type == EmailHelper.SENDER_TYPE_OUTLOOK:
            self._send_outlook()
        elif self.sender_type == EmailHelper.SENDER_TYPE_SMTP:
            return self._send_SMTP()
        else:
            raise Exception("The sender_type attribute has an unexpected value.")

    @staticmethod
    def validate_email(email_address):
        """Validate e-mail address.

         - Strip leading and trailing whitespaces.

        Return the validated e-mail address.
        """
        validated_email = email_address.strip()
        return validated_email

    def _send_SMTP(self):
        """Send the mail using SMTP"""
        # Create a text/plain message
        msg = email.mime.Multipart.MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.mail_from
        msg['To'] = ",".join(self.mail_to)
        msg['CC'] = ",".join(self.mail_cc)
        msg['BCC'] = ",".join(self.mail_bcc)

        # The main body is just another attachment
        body = email.mime.Text.MIMEText(self.body, self.body_type)
        msg.attach(body)

        # attachment
        for file_path in self.attachments:
            fp = open(file_path, 'rb')
            file_type = mimetypes.guess_type(file_path)
            subtype = 'pdf'  # default value
            if file_type and file_type[0]:
                subtype = file_type[0]

            att = email.mime.application.MIMEApplication(fp.read(), subtype)
            fp.close()
            filename = os.path.basename(file_path)
            att.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(att)

        result = None
        for r in range(self.retries):
            try:
                s = smtplib.SMTP(self.host, port=self.smtp_port, timeout=self.smtp_timeout)
            except:
                LOGGER.exception('Failed to connect to %s.' % self.host)
                if r == self.retries - 1:
                    raise
                time.sleep(r)
                LOGGER.info('Retrying to connect...')
                continue

            try:
                result = s.sendmail(self.mail_from, self.mail_to + self.mail_cc + self.mail_bcc, msg.as_string())
                s.quit()
                break
            except smtplib.SMTPServerDisconnected:
                LOGGER.error("Failed to send! (retry: %s)", r)
                if r == self.retries - 1:
                    raise
                time.sleep(r)
        return result

    def _get_outlook_mail(self):
        """Returns an object of the outlook mail type"""
        import win32com.client as win32
        if sys.platform == 'win32':
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = ";".join(self.mail_to)
            mail.CC = ";".join(self.mail_cc)
            mail.BCC = ";".join(self.mail_bcc)
            mail.Subject = self.subject
            if self.body_type == EmailHelper.BODY_TYPE_HTML:
                mail.BodyFormat = 3
                mail.HTMLBody = self.body
            elif self.body_type == EmailHelper.BODY_TYPE_TXT:
                mail.Body = self.body
            else:
                raise BodyTypeError('Unknown body type: {0}'.format(self.body_type))

            for attachment in self.attachments:
                if not os.path.isfile(attachment):
                    raise AttachmentError('Attachment not found {0}'.format(attachment))
                else:
                    mail.Attachments.Add(attachment)

            return mail
        else:
            raise Exception('Cannot create an outlook message if not win32.')

    def save_mail(self, output_file):
        """Save the email to the specified file.

        output_file=c:\tmp\my_email.msg
        """
        mail = self._get_outlook_mail()
        olMSG = 2
        mail.saveAs(output_file, olMSG)

    def _send_outlook(self):
        """Send the email using outlook"""
        mail = self._get_outlook_mail()
        mail.send
