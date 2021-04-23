""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitNotification.py"
from __future__ import print_function
"""--------------------------------------------------------------------------
MODULE
    FLimitNotification

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A collection of functions providing notification actions on limits
    based business process updates.

    These functions should be called within the limits business process
    state chart callbacks and take the business process callback context
    (ctx) as a parameter.

    E.g. In a python modules named the sames as the limits state chart:

    import FLimitNotification
    def on_entry_state_breached(ctx):
        FLimitNotification.EmailNotification(ctx, ['admin@sungard.com',])

-----------------------------------------------------------------------------"""
import datetime
import os
import string   # pylint: disable-msg=W0402

import acm
import FLimitSettings
import FLimitUtils


def EmailNotification(ctx, recipients, subject=None, message=None):
    """Notify the list of recipients through email."""
    # pylint: disable-msg=E1101
    import smtplib
    from email.mime.multipart import MIMEMultipart    
    from email.mime.text import MIMEText

    smtpServer = FLimitSettings.NotificationSMTPServer()
    if not smtpServer:
        print('ERROR: No SMTP mail server defined for sending limit notifications.')
        print('This must be specified in the "Notification SMTP Server" parameter of')
        print('the "FLimitSettings" FParameter extension attribute.')
        return
    try:
        if not subject:
            subject = '[%STATE%] Limit %LIMIT_NAME% has been updated'
        if not message:
            message = _GetDefaultLimitEventDescription(ctx)
        sender = FLimitSettings.NotificationSenderAddress()

        msg = MIMEMultipart()
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = _GetNotificationString(subject, ctx)
        msg['From'] = sender
        msg.attach(MIMEText(_GetNotificationString(message, ctx), 'plain'))

        server = smtplib.SMTP(smtpServer, timeout=FLimitSettings.NotificationSMTPTimeout())
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()
    except Exception as e:
        print('ERROR: Failed to send mail for limit notification:', e)

def LogFileNotification(ctx, logFileName, message=None):
    """Log the limit update to file."""
    try:
        if not message:
            state = ctx.TargetState().Name()
            fields = ('%DATE% %TIME%', '[%STATE%]', 'Limit %LIMIT_NAME%',
                '%ORIGIN_OBJECT%', '"%LIMIT_PATH%"', '"%LIMIT_COLUMN_ID%"', '%CURRENT_VALUE%',
                '%COMPARISON_SYMBOL%', ('%WARNING_VALUE%' if state == 'Warning' \
                else '%THRESHOLD_VALUE%'),
            )
            message = _GetNotificationString('\t'.join(fields), ctx)

        with open(logFileName, 'a') as f:
            f.write(message + os.linesep)
    except Exception as e:
        print('ERROR: Failed to log limit update to file: ', e)

def SendUserMessageNotification(ctx, recipients, subject=None, message=None):
    """Notify a list of recipients through user messages."""
    try:
        if not subject:
            subject = '[%STATE%] Limit %LIMIT_NAME% has been updated'
        if not message:
            message = _GetDefaultLimitEventDescription(ctx)
        subject = _GetNotificationString(subject, ctx)
        message = _GetNotificationString(message, ctx)
        acm.SendUserMessage(recipients, subject, message, [ctx.Subject(), ])
    except Exception as e:
        print('ERROR: Failed to send user message for limit notification:', e)

def PopupNotification(ctx, message=None):
    """Display a popup message box with the limit update information."""
    msgBox = acm.GetFunction('msgBox', 3)
    if msgBox:
        msgBoxFlags = {'Breached': 0x10, 'Warning': 0x30, 'Active': 0x00}
        if not message:
            message = _GetDefaultLimitEventDescription(ctx)
        state = ctx.TargetState().Name()
        msgBox(_GetNotificationString('Limit Manager - %DATE% %TIME%', ctx), 
            _GetNotificationString(message, ctx), msgBoxFlags.get(state, 0x00))
    else:
        print('ERROR: Could not get message box function for limit popup notification.')

def SoundNotification(sound):
    """Play a sound on limit update."""
    try:
        import winsound
        flags = winsound.SND_ASYNC
        if not sound:
            flags |= winsound.MB_ICONEXCLAMATION
        winsound.PlaySound(sound, flags)
    except Exception as e:
        print('ERROR: Failed to play sound for limit notification: ', e)


def _GetDefaultLimitEventDescription(ctx):
    state = ctx.TargetState().Name()
    return 'Limit %LIMIT_NAME% on "%LIMIT_PATH%"' + \
        ' has entered the %STATE% state [%LIMIT_COLUMN_ID% value:' + \
        ' %CURRENT_VALUE% %COMPARISON_SYMBOL% ' + \
        ('%WARNING_VALUE%' if state == 'Warning' else '%THRESHOLD_VALUE%') + '].'

def _GetNotificationString(txt, ctx):
    limit = ctx.Subject()
    bp = limit.BusinessProcess()
    now = datetime.datetime.now()

    variables = (
        ('%DATE%', now.strftime('%Y-%m-%d')),
        ('%TIME%', now.strftime('%H:%M:%S')),
        ('%STATE%', ctx.TargetState().Name()),
        ('%PREVIOUS_STATE%', ctx.CurrentState().Name()),
        ('%EVENT%', ctx.Event().Name()),
        ('%CURRENT_VALUE%', ctx.Parameters().At('Value at checking', '??')),
        ('%THRESHOLD_VALUE%', str(limit.Threshold())),
        ('%WARNING_VALUE%', str(limit.WarningValue())),
        ('%AVAILABLE_VALUE%', str(FLimitUtils.AvailableValue(limit))),
        ('%COMPARISON_TYPE%', limit.ComparisonOperator()),
        ('%COMPARISON_SYMBOL%', FLimitUtils.ComparisonOperatorAsSymbol(limit.ComparisonOperator())),
        ('%ORIGIN_OBJECT%', str(FLimitUtils.OriginObjectName(limit))),
        ('%LIMIT_NAME%', limit.Name()),
        ('%LIMIT_COLUMN_ID%', str(FLimitUtils.ColumnName(limit))),
        ('%LIMIT_PATH%', FLimitUtils.Constraints(limit)),
        ('%LIMIT_PATH_SHORT%', FLimitUtils.ConstraintsSummary(limit)),
        ('%LIMIT_STATECHART%', bp.StateChart().Name()),
    )
    for variable, value in variables:
        txt = string.replace(txt, variable, value)
    return txt
