""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/ComplianceRules/./etc/FComplianceNotifications.py"
"""--------------------------------------------------------------------------
MODULE
    FComplianceNotifications

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""
import collections
import datetime

import acm
import FComplianceRulesUtils
from FParameterSettings import ParameterSettingsCreator

logger = FComplianceRulesUtils.logger
EMAIL_REGEX = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
SETTINGS = ParameterSettingsCreator.FromRootParameter('ComplianceRulesNotificationSettings')


def send_email_notification(alerts, options):
    import smtplib
    smtp_server = FEmailTransfer.SMTPServer(SETTINGS.SMTPServer(),
                                            SETTINGS.SMTPPort(),
                                            SETTINGS.SMTPUsername(),
                                            SETTINGS.SMTPPassword(),
                                            SETTINGS.SMTPTLS())

    filtered_alerts = [alert for alert in alerts if alert.Threshold().Type() in options.ThresholdTypeEmail]
    if filtered_alerts:
        subject = _get_notification_subject_string(SETTINGS.Subject(), options)
        body = '\n'.join([
            _get_notification_message_string(SETTINGS.AlertTemplate(), alert)
            for alert in filtered_alerts])
        recipients = _get_email_addresses(options.EmailRecipients)
        message = FEmailTransfer.Message(recipients, subject, SETTINGS.SenderAddress(), body)
        
        try:
            FEmailTransfer(smtp_server, message).Send()
        except (smtplib.SMTPException, smtplib.socket.error, IOError, ValueError) as e:
            logger.error('Failed to send email message. Reason:' + str(e))


def send_message_notification(alerts, options):
    filtered_alerts = [alert for alert in alerts if str(alert.Threshold().Type().Name()) in options.ThresholdTypeMessage]
    if filtered_alerts:
        subject = _get_notification_subject_string(SETTINGS.Subject(), options)
        message = '\n'.join([
            _get_notification_message_string(SETTINGS.AlertTemplate(), alert)
            for alert in filtered_alerts])
        if options.MessageRecipients:
            status = acm.SendUserMessage(options.MessageRecipients, subject, message, None)
            if not status:
                logger.error("Error in sending User Message.")


def _get_notification_message_string(txt, alert):
    variables = (
        ('%THRESHOLD_TYPE%', alert.Threshold().Type().Name()),
        ('%THRESHOLD_COMPARISON%', alert.Threshold().ComparisonType()),
        ('%THRESHOLD_VALUE%', str(alert.Threshold().ThresholdValue())),
        ('%RULE%', alert.AppliedRule().ComplianceRule().Name()),
        ('%ALERT_STATE%', alert.State()),
        ('%ALERT_RULE_TARGET%', alert.AppliedRule().TargetObject().Target().Name()),
        ('%ALERT_SUBJECT%', alert.Subject().Name()),
        ('%ALERT_SUBJECT_TYPE%', alert.Subject().RecordType()),
        ('%ALERT_INFORMATION%', alert.Information()),
        ('%ALERT_OID%', str(alert.Oid())),
    )
    for variable, value in variables:
        txt = txt.replace(variable, value)
    return txt


def _get_notification_subject_string(txt, options):
    now = datetime.datetime.now()
    variables = (
        ('%DATE%', now.strftime('%Y-%m-%d')),
        ('%TIME%', now.strftime('%H:%M:%S')),
        ('%RULES%', options.Rules.AsString()),
        ('%RULE_QUERIES%', options.RuleQueries.AsString()),
    )
    for variable, value in variables:
        txt = txt.replace(variable, value)
    return txt
    
def _get_email_addresses(recipients):
    import re
    emails = []
    for rec in recipients:
        recipient = rec.strip()
        user = acm.FUser[recipient]
        if user:
            email = user.Email()
            if email:
                emails.append(email)
            else:
                logger.warn("User {} doesn't have email address.".format(recipient))
        elif re.match(EMAIL_REGEX, recipient):
            emails.append(recipient)
        else:
            logger.error("{} is not valid user nor email address.".format(recipient))
        
    return emails

class FEmailTransfer(object):

    class SMTPServer(object):
        """Stores SMTP server details."""
        def __init__(self, hostname, port=25, username=None, password=None, tls_mode=False):
            self.hostname = hostname
            self.port = int(port)
            self.username = username
            self.password = password
            self.tls_mode = tls_mode

    class Message(object):
        """Stores common email message details."""
        def __init__(self, recipients, subject, sender, body):
            self.recipients = recipients
            self.subject = subject
            self.sender = sender
            self.body = body

    def __init__(self, server, message):
        self._ValidateSMTPServer(server)
        self._server = server
        self._ValidateMessage(message)
        self._message = message
        if not isinstance(self._message.recipients, collections.Iterable):
            self._message.recipients = [self._message.recipients, ]

    def Send(self):
        import smtplib
        server = smtplib.SMTP()
        server.connect(self._server.hostname, self._server.port)
        if self._server.tls_mode:
            server.starttls()
        if self._server.username:
            server.login(self._server.username, self._server.password)
        server.verify(self._message.recipients)
        msg = self._GetEmailMessage(self._message.recipients, self._message)
        server.sendmail(self._message.sender, self._message.recipients, msg.as_string())
        server.quit()
        logger.info("Email notification successfully sent to: {}".format(self._message.recipients))

    @staticmethod
    def _ValidateSMTPServer(server):
        if (not server or
                server.hostname is None or
                not isinstance(server.port, int)):
            raise ValueError('Invalid SMTP server: ' + str(vars(server)))

    @staticmethod
    def _ValidateMessage(message):
        if (not message or
            not message.recipients or
                message.sender is None):
            raise ValueError('Invalid email message: ' + str(vars(message)))

    @classmethod
    def _GetEmailMessage(cls, recipients, message):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart()
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = message.subject
        msg['From'] = message.sender
        msg.attach(MIMEText(message.body, 'plain'))
        return msg
        