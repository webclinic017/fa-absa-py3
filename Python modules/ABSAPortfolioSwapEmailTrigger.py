"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapEmailTrigger

DESCRIPTION
    Institutional CFD Project

    Date                : 2010-10-23
    Purpose             : Creates an XML trigger file to email CFD Statements from FormScape.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 455227

HISTORY
================================================================================
Date       Change no Developer          Description
--------------------------------------------------------------------------------
2011-09-30 786089    Herman Hoon        Updated the attachment directory
2014-11-05 000000    Andrei Conicov     Have added new functionality. Emails are sent using at_email.
ENDDESCRIPTION
-----------------------------------------------------------------------"""
import ABSAXML
import ael
import acm
from at_email import EmailHelper
import os
import sys

SUBJECT_PREFIX = 'Absa Capital CFD Statement'
EMAIL_BODY = 'Please note: Payments due need to be paid before 12:00pm. Please send your proof of payment to Absa Capital Collateral Management (collateral.management@absacapital.com).'
ATTACHMENT_DIR = '\\\\v036syb004001.ds1.ad.absa.co.za\MoneyMarketStatements\CFDStatements\PDF\\'


def toDetails(emailXML, Node, ael_client):
    send_to = _get_to_details(ael_client)
    flag = len(send_to)
    if flag == 0:
        clientName = ael_client.ptyid
        print('WARNING: %s does not have a contact with a rule set up for Portfolio Swaps. Statement will not be send to client.' % (clientName))
    else:
        for attention, address in send_to:
            toDetailsNode = emailXML.create_tag(Node, 'TO')
            emailXML.create_full_tag(toDetailsNode, 'NAME', attention)
            emailXML.create_full_tag(toDetailsNode, 'ADDRESS', address)

    return flag


def _get_to_details(ael_client):
    send_to = []
    clientName = ael_client.ptyid
    contacts = ael_client.contacts()
    for contact in contacts:
        rules = contact.rules()
        for rule in rules:
            if rule.instype == 'Portfolio Swap':
                address = contact.email
                attention = contact.attention
                if address:
                    send_to.append((attention, address))
                else:
                    print('WARNING: Contact %s of Client %s does not have an email address.' % (contact.fullname, clientName))
    return send_to


def writeTriggerXml(clientName, ael_dict, reportDate, xmlFileName):
    ael_client = ael.Party[clientName]
    bccList = ael_dict['bccAdresses']
    fromAddres = ael_dict['fromAdress']

    emailXML = ABSAXML.ABSAReportXML('EMAIL', clientName, reportDate)

    Node = emailXML.RootNode

    toDetails(emailXML, Node, ael_client)

    fromDetailsNode = emailXML.create_tag(Node, 'FROM')
    emailXML.create_full_tag(fromDetailsNode, 'NAME', fromAddres.split('@')[0])
    emailXML.create_full_tag(fromDetailsNode, 'ADDRESS', fromAddres)

    for bcc in bccList:
        ccDetailsNode = emailXML.create_tag(Node, 'BCC')
        emailXML.create_full_tag(ccDetailsNode, 'NAME', bcc.split('@')[0])
        emailXML.create_full_tag(ccDetailsNode, 'ADDRESS', bcc)

    subject = '%s - %s - %s' % (SUBJECT_PREFIX, clientName, reportDate)
    emailXML.create_full_tag(Node, 'SUBJECT', subject)
    emailXML.create_full_tag(Node, 'BODY', EMAIL_BODY)
    emailXML.create_full_tag(Node, 'ATTACMENT', ATTACHMENT_DIR + xmlFileName)

    reportFileName = emailXML.FileName + '.xml'
    path = ael_dict['triggerOutputPath'].SelectedDirectory()
    xmlfilePath = str(path) + "/" + reportFileName
    xmlfile = open(xmlfilePath, "w")
    xmlfile.write(emailXML.to_string(True))
    xmlfile.close()
    acm.Log('File:' + reportFileName)


def send_statement(client_name, ael_dict, report_date, attachments, test_run):
    """ Send the attached files to the specified email address.
    """
    ael_client = ael.Party[client_name]
    bcc_list = list(ael_dict['bccAdresses'])
    from_address = ael_dict['fromAdress']

    send_to = _get_to_details(ael_client)
    if not send_to:
        client_name = ael_client.ptyid
        print('WARNING: %s does not have a contact with a rule set up for Portfolio Swaps. Statement will not be send to client.' % (client_name))
        return

    mail_to = [address for (_, address) in send_to]
    print('Mail to: {0}'.format(mail_to))
    print('BCC to: {0}'.format(bcc_list))
    if test_run:
        print('Test run. Email will be sent to {0}'.format(from_address))
        mail_to = [from_address]
        bcc_list = []

    if mail_to:
        subject = '%s - %s - %s' % (SUBJECT_PREFIX, client_name, report_date)
        email = EmailHelper(EMAIL_BODY, subject, mail_to, from_address,
                            attachments, mail_bcc=bcc_list)

        # Use outlook to send email from front end
        # Use SMTP to send email from back end
        if str(acm.Class()) == "FACMServer":
            email.sender_type = EmailHelper.SENDER_TYPE_SMTP
            email.host = EmailHelper.get_acm_host()

        try:
            email.send()
        except Exception as e:
            print(("!!! Exception: {0}\n".format(e)))
            exc_type, _exc_obj, exc_tb = sys.exc_info()
            filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print((exc_type, filename, exc_tb.tb_lineno))

            raise e

