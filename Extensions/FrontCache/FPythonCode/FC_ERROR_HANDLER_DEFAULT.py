'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_ERROR_HANDLER_DEFAULT
PROJECT                 :       FX onto Front Arena
PURPOSE                 :       This module will be called if the FC_UTILS module could not be loaded or 
                                initialized or if the FC_EXCEPTION module cannot be imported. The above
                                mentioned modules takes care of error handling. If the setup of the above
                                fails, this module will send an email notification for the BTB Integration team
                                and the RTB team to alert them of errors experienced on the setup.
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       FX onto Front Arena Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
IMPORTANT -- This module should only be called if the error handling modules for Front Cache failed to be
imported and initialized.
-------------------------------------------------------------------------------------------------------------
'''

'''----------------------------------------------------------------------------------------------------------
Importing all relevant Python modules.
----------------------------------------------------------------------------------------------------------'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import StringIO
'''----------------------------------------------------------------------------------------------------------
Importing custom modules.
----------------------------------------------------------------------------------------------------------'''
from FC_EXCEPTION import FC_EXCEPTION as EXCEPTION
from FC_PARAMETERS_ENVIRONMENT import FC_PARAMETERS_ENVIRONMENT as PARAMETERS_ENVIRONMENT
'''----------------------------------------------------------------------------------------------------------
Default variables.
-------------------------------------------------------------------------------------------------------------
'''
SUBJECT = 'FRONT CACHE CRITICAL ERROR'
COMMASPACE = ', '
SMTP_SERVER = str(PARAMETERS_ENVIRONMENT.environment.getElementsByTagName('GENERIC_PARAMETERS')[0].getElementsByTagName('SmtpServer')[0].firstChild.data)

'''----------------------------------------------------------------------------------------------------------
Function to generate a text email to the recipients detailed above.
-------------------------------------------------------------------------------------------------------------
'''

def constructExcpetionMsgString(exception, msg):
    if type(exception) == EXCEPTION:
        errorString = '%s\n\nFRONT CACHE ERROR:\n\nTEXT MESSAGE:\n\n%s\n\nTRACEBACK:\n\n%s\n\nSEVERITY:\n\n%s\n\n' \
                %(msg, exception.TextMsg, exception.Traceback, exception.Severity)
        if exception.InnerException:
            errorString = constructExcpetionMsgString(exception.InnerException, errorString)
    else:
        errorString = '%sException:\n\n%s\n\n' %(msg, str(exception))
    return errorString

def constructEmail(toAddress, subject, exception, traceback, message, stringAsAttach):
    fromAddress = str(PARAMETERS_ENVIRONMENT.environment.getElementsByTagName('GENERIC_PARAMETERS')[0].getElementsByTagName('FromEmail')[0].firstChild.data)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = COMMASPACE.join(toAddress)
    stringMsg = message
    if exception:
        stringMsg = constructExcpetionMsgString(exception, stringMsg)

    if traceback:
        stringMsg = '%sTraceback:\n\n%s\n\n' %(stringMsg, traceback.format_exc())

    msg.attach(MIMEText(stringMsg, 'html'))
    if stringAsAttach is not None:
        string_attachment = StringIO.StringIO()
        string_attachment.write(stringAsAttach)
        string_attachment.seek(0)
        attachment = MIMEText(string_attachment.getvalue())
        attachment.add_header('Content-Disposition', 'attachment', filename='ambMessage.txt')
        msg.attach(attachment)
    smtp = smtplib.SMTP(SMTP_SERVER)
    smtp.sendmail(fromAddress, toAddress, msg.as_string())
    smtp.quit()

    #print 'A %s email has been sent to %s.' %(subject, toAddress)
    #print msg.as_string()

def __construct_notification(type, notificationName='None', batchId='None', requestId='None', topic='None',
                             reportDate='None', msgInfo='None', impact='None'):

    return """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Front Cache Notification</title>
    <style type="text/css">
        /* Default CSS */
        body, #body_style {
            margin: 0;
            padding: 0;
            background: #f1f1f1;
            color: #5b656e;
        }

        a {
            color: #09c;
        }

            a img {
                border: none;
                text-decoration: none;
            }

        table, table td {
            border-collapse: collapse;
        }

        td, h1, h2, h3, p {
            font-family: arial, helvetica, sans-serif;
            color: #313a42;
        }

        h1, h2, h3, h4 {
            color: #313a42 !important;
            font-weight: normal;
            line-height: 1.2;
        }

        h1 {
            font-size: 24px;
        }

        h2 {
            font-size: 18px;
        }

        h3 {
            font-size: 16px;
        }

        p {
            margin: 0 0 1.6em 0;
        }

        /* Force Outlook to provide a "view in browser" menu link. */
        #outlook a {
            padding: 0;
        }

        /* Whitespace (imageless spacer) */
        .whitespace {
            font-family: 0px;
            line-height: 0px;
        }

        /* Header */
        .header {
            background: rgb(22, 140, 204);
        }

        .headerTitle {
            color: #ffffff;
            font-size: 28px;
            padding: 0px 0px 10px 0px;
        }

        .headerContent {
            color: #ffffff;
            font-size: 22px;
        }

        /* One horizontal section of content: e.g. */
        .section {
            padding: 20px 0px 0px 0px;
        }

        .sectionOdd {
            background-color: #f1f1f1;
        }

        .sectionEven {
            background-color: #ffffff;
        }

        .sectionOdd, .sectionEven {
            padding: 30px 0px 30px 0px;
        }

        /* An article */
        .sectionArticleTitle, .sectionArticleContent {
            text-align: center;
        }

        .sectionArticleTitle {
            font-size: 18px;
            padding: 10px 0px 5px;
        }

        .sectionArticleContent {
            font-size: 13px;
            line-height: 18px;
        }

        .sectionArticleImage {
            text-align: center;
        }

            .sectionArticleImage img {
                padding: 0px 0px 0px 0px;
                -ms-interpolation-mode: bicubic;
            }


        .sectionTitle, .sectionSubTitle {
            text-align: center;
        }

        .sectionTitle {
            font-size: 23px;
            padding: 0px 10px 10px 10px;
        }

        .sectionSubTitle {
            padding: 0px 10px 20px 10px;
        }

        /* Footer */
        .footer {
            background: rgb(22, 140, 204);
        }

            .footer a {
                color: #ffffff;
                font-size: 14px;
            }
    </style>
</head>
<body>
    <span id="body_style" style="display:block">
        <table border="0" cellspacing="0" cellpadding="0" width="100%" class="header">
            <tr>
                <td class="section">
                    <table border="0" cellspacing="0" cellpadding="0" width="640" align="center">
                        <tr>
                            <td class="column">
                                <table border="0" cellspacing="0" cellpadding="0" height="80">
                                    <tr>
                                        <td class="headerTitle">
                                            Front Cache | Markets Integration
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="headerContent">
                                            """+str(type)+""" Notification
                                        </td>
                                    </tr>
                                    <tr><td class="whitespace" height="15">&nbsp;</td></tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td class="sectionOdd">
                    <table border="0" cellpadding="0" cellspacing="0" width="640" align="center">
                        <tr>
                            <td class="column" valign="top">
                                <table border="0" cellpadding="0" cellspacing="0" width="200" align="left">
                                    <tr><td class="sectionArticleTitle">Description</td></tr>
                                    <tr><td class="sectionArticleContent">"""+str(notificationName)+"""</td></tr>
                                </table>
                            </td>
                            <td class="column" valign="top">
                                <table border="0" cellpadding="0" cellspacing="0" width="200" align="center">
                                    <tr><td class="sectionArticleTitle">Impact</td></tr>
                                    <tr><td class="sectionArticleContent">"""+str(impact)+"""</td></tr>
                                </table>
                            </td>
                            <td class="column" valign="top">
                                <table border="0" cellpadding="0" cellspacing="0" width="200" align="center">
                                    <tr><td class="sectionArticleTitle">Investigation</td></tr>
                                    <tr><td class="sectionArticleContent">Please contact RTB team to get more detailed information.</td></tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td class="sectionEven">
                    <table border="0" cellpadding="0" cellspacing="0" width="640" align="center">
                        <tr><td class="sectionTitle">Additional Information</td></tr>
                        <tr>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0" width="450" align="center">
                                    <tbody>
                                        <tr>
                                            <td class="sectionArticleContent">Batch Id</td>
                                            <td class="sectionArticleContent"><a href="http://frontcache-prod1/Batch/Detail?batchId="""+str(batchId)+"""" target="_blank">"""+str(batchId)+"""</a></td>
                                        </tr>
                                        <tr>
                                            <td class="sectionArticleContent">Topic</td>
                                            <td class="sectionArticleContent">"""+str(topic)+"""</td>
                                        </tr>
                                        <tr>
                                            <td class="sectionArticleContent">Report Date</td>
                                            <td class="sectionArticleContent">"""+str(reportDate)+"""</td>
                                        </tr>
                                        <tr>
                                            <td class="sectionArticleContent">Info</td>
                                            <td class="sectionArticleContent">"""+str(msgInfo)+"""</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <table border="0" cellspacing="0" cellpadding="0" width="100%" class="footer">
            <tr><td class="whitespace" height="20">&nbsp;</td></tr>
            <tr>
                <td>
                    <table border="0" cellspacing="0" cellpadding="0" align="center">
                        <tr>
                            <td align="center">
                                <a href="mailto:ABCapITRTBAMFrontAre@barclayscapital.com">RTB Front Arena</a>
                            </td>
                            <td style="color:#ffffff;">&nbsp;|&nbsp;</td>
                            <td align="center">
                                <a href="mailto:ABSAFrontCacheDev@barclayscapital.com">ABSA Front Cache Team</a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr><td class="whitespace" height="20">&nbsp;</td></tr>
        </table>
    </span>
</body>
</html>

"""

def handelError(TEXT, exception, traceback):
    errorEmailNotificationGroups = PARAMETERS_ENVIRONMENT.environment.getElementsByTagName('GENERIC_PARAMETERS')[0].getElementsByTagName('EmailNotificationGroups')[0].getElementsByTagName('ErrorEmailNotificationGroup')
    TO_ADDRESSES = [group.firstChild.data for group in errorEmailNotificationGroups]
    constructEmail(TO_ADDRESSES, SUBJECT, exception, traceback, TEXT, None)

def handle(type, subject, group, batchId='None', requestId='None', reportDate="None", topic='None', messageInfo='None',
           impact='None', notificationName='None', textAsAttachment = None):
    warningEmailNotificationGroups = PARAMETERS_ENVIRONMENT.environment.getElementsByTagName('GENERIC_PARAMETERS')[0].getElementsByTagName('EmailNotificationGroups')[0].getElementsByTagName(group)
    TO_ADDRESSES = [group.firstChild.data for group in warningEmailNotificationGroups]
    notification_message = __construct_notification(type, notificationName, batchId=batchId, requestId=requestId, topic=topic,
                                                    reportDate=reportDate, msgInfo=messageInfo, impact=impact)
    constructEmail(TO_ADDRESSES, subject, None, None, notification_message, textAsAttachment)
