"""Released Settlement Tool initially created by Gavin Wienand (SunGard Code)

Purpose:
    Track down all Released Settlements that have not changed status for a
specific time - Send out notification.

Department and Desk:
    Operations - for IT Assistance

Requester:
    RTB Front Arena Support

Developer:
    Gavin Wienand

Changes:
    CHNG0004167453 - Detect NACKs due to Adaptiv run time error or
    disconnection. Requested by Zain Beg and implemented by Marcelo G. Almiron
"""

import string
import smtplib
from collections import defaultdict
from datetime import datetime, timedelta, time
import acm
from at_ael_variables import AelVariableHandler


HOST = 'SMTPRELAY.barcapint.com'
FROM = "FrontArenaTaskServer"


def _list_set_or_conf_by_acquirer(set_or_conf_dict):
    """Create text list of settlements or confirmations grouped by acquirer

    The function receives a dictionary of acquirers containing a list of 
    settlements or confirmations.
    """
    set_or_conf_msg = ''
    for acq in set_or_conf_dict:
        set_or_conf_msg += '\t%s:\n' % acq
        for set_or_conf in set_or_conf_dict[acq]:
            oid = set_or_conf.Oid()
            trd = set_or_conf.Trade().Oid() if set_or_conf.Trade() else 0
            set_or_conf_msg += '\t\t%s --> %s\n' % (oid, trd)
        set_or_conf_msg += '\n'
    return set_or_conf_msg


def _is_false_nack(op_document):
    """Analyse status to decide if settlement or confirmation has a not valid
    NACK

    The function receives an FOperationsDocument object that has a
    nacked settlement or confirmation. False NACKs are detected
    according to Status and StatusExplanation fields. Rules are
    gradually incorporated as more cases are detected in Production
    environment.
    """

    if op_document.Status() in ['Exception', 'Send failed']:
        msgs = ['Interface failure connection refused',
                'Timed out while waiting for reply from Document service',
                "Document 0: 'NoneType' object has no attribute 'GetXML'"]
        for msg in msgs:
            if msg in op_document.StatusExplanation():
                return True
    return False


def recently_changed(obj, mins=0):
    """Returns True if `obj` changed in the last `mins` minutes
    """

    upper_bound = datetime.now() - timedelta(minutes=mins)
    lower_bound = datetime.combine(upper_bound, time(0, 0, 0, 0))

    # Use the timestamp without timezone shift
    last_update = datetime.fromtimestamp(obj.UpdateTime())

    return lower_bound <= last_update <= upper_bound


def detect_false_nacks(email):
    """Detect false NACKs from Adaptiv

    The function receives an email address to send alerts in case of detection
    of false NACKs within the day, i.e. NACKs from Adaptiv instead of SWIFT.
    """

    false_nacked_list = []

    ops_query = acm.CreateFASQLQuery(acm.FOperationsDocument, 'OR')
    ops_query.AddAttrNode('Settlement.Status', 'EQUAL', 'Not Acknowledged')
    ops_query.AddAttrNode('Confirmation.Status', 'EQUAL', 'Not Acknowledged')
    ops_query.AddAttrNode('Confirmation.Status', 'EQUAL', 'Exception')

    ops_list = ops_query.Select()

    for i in ops_list:
        set_or_conf = i.Settlement() if i.Settlement() else i.Confirmation()
        if _is_false_nack(i) and recently_changed(set_or_conf, 0):
            false_nacked_list.append(i)

    if false_nacked_list:
        subject = 'URGENT - Front Arena Settlements need to be Resubmitted' \
                  ' in Production'

        # Create dictionaries {'Acquirer' : [List of Settlement/Confirmation
        #                                    Objects]}

        sttl_dict = defaultdict(list)
        conf_dict = defaultdict(list)

        for i in false_nacked_list:
            if i.Settlement():
                sttl = i.Settlement()
                acq = sttl.Acquirer().Name()
                sttl_dict[acq].append(sttl)
            else:
                conf = i.Confirmation()
                acq = conf.Acquirer().Name()
                conf_dict[acq].append(conf)

        # Create message of email for settlements
        sttl_msg = 'Settlements (Settlement --> Trade):\n'
        sttl_msg += _list_set_or_conf_by_acquirer(sttl_dict)

        # Create message of email for confirmations
        conf_msg = 'Confirmations (Confirmation --> Trade):\n'
        conf_msg += _list_set_or_conf_by_acquirer(conf_dict)

        # Grammar string
        msg_intro = 'The settlement(s)/confirmation(s) below received ' \
                    'Adaptiv NACKs and need to be handled. In the case of ' \
                    'settlements, they need to be resubmitted since these ' \
                    'NACKs are not valid SWIFT NACKs.\n\n'
        msg_body = '%s\n%s\n%s\n' % (sttl_msg, conf_msg, '-'*51)
        msg_end = 'Python Script: %s.' % __name__
        message = msg_intro + msg_body + msg_end
        send_mail(subject, message, email)


def detect_all_nacks(email):
    """Notifies about settlements and confirmations with `Not Acknowledged`
    status
    """

    settl_query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    settl_query.AddAttrNode('Status', 'EQUAL', 'Not Acknowledged')
    settl_list = settl_query.Select()

    conf_query = acm.CreateFASQLQuery(acm.FConfirmation, 'AND')
    conf_query.AddAttrNode('Status', 'EQUAL', 'Not Acknowledged')
    conf_list = conf_query.Select()    

    nacked_settl_list = filter(recently_changed, settl_list)
    nacked_conf_list = filter(recently_changed, conf_list)
    nacked_list = nacked_settl_list + nacked_conf_list

    if nacked_list:
        subject = "URGENT - Front Arena Settlements/Confirmations received a" \
                  " 'Not Acknowledged' in Production"

        # Create dictionaries {'Acquirer' : [List of Settlement/Confirmation
        #                                    Objects]}

        sttl_dict = defaultdict(list)
        conf_dict = defaultdict(list)

        for i in nacked_settl_list:
            acq = i.Acquirer().Name()
            sttl_dict[acq].append(i)

        for i in nacked_conf_list:
            acq = i.Acquirer().Name()
            conf_dict[acq].append(i)

        # Create message of email for settlements
        sttl_msg = 'Settlements (Settlement --> Trade):\n'
        sttl_msg += _list_set_or_conf_by_acquirer(sttl_dict)

        # Create message of email for confirmations
        conf_msg = 'Confirmations (Confirmation --> Trade):\n'
        conf_msg += _list_set_or_conf_by_acquirer(conf_dict)

        # Grammar string
        msg_intro = 'The settlement(s)/confirmation(s) below received ' \
                    'received NACKs and need to be handled.\n\n'
        msg_body = '%s\n%s\n%s\n' % (sttl_msg, conf_msg, '-'*51)
        msg_end = 'Python Script: %s.' % __name__
        message = msg_intro + msg_body + msg_end
        send_mail(subject, message, email)    


def detect_released_settlements(mins, email):
    """Notifies about stagnant settlements

    Only settlements in `Released` status with value day `today`
    """
    
    date_format = '%Y/%m/%d %I:%M:%S %p'

    # Select settlement that have been released within a time (mins) interval
    released_sttlmnts = []
    query = acm.CreateFASQLQuery(acm.FSettlement, 'AND')
    query.AddAttrNode('Status', 'EQUAL', 'Released')
    query.AddAttrNode('ValueDay', 'EQUAL', acm.Time.DateToday())
    settlements = query.Select()

    for settlmnt in settlements:
        if recently_changed(settlmnt, mins):
            released_sttlmnts.append(settlmnt)

    if released_sttlmnts:
        subject = 'URGENT - Front Arena Settlements Stuck in Released status' \
                  ' in Production'
        # Create dictionary {'Acquirer' : [List of Settlement Objects]}
        sttl_dict = defaultdict(list)
        for sttl in released_sttlmnts:
            acq = sttl.Acquirer().Name()
            sttl_dict[acq].append(sttl)

        # Create message of email
        data_msg = ''

        for acq in sttl_dict:
            data_msg += acq + ':\n'
            for sttl in sttl_dict[acq]:
                # Settle Id, Trade Id, Update Time, payId
                oid = sttl.Oid()
                trd = sttl.Trade().Oid() if sttl.Trade() else 0
                upt_raw = datetime.fromtimestamp(sttl.UpdateTime())
                upt = upt_raw.strftime(date_format)
                data_msg += '\t%s --> %s\t%s\n' % (oid, trd, upt)
            data_msg += '\n'

        # Grammar string
        g_s = ['The Settlements below', 'were released more than', 'have']
        if len(released_sttlmnts) == 1:
            g_s = ['The Settlement below', 'was released more than', 'has']
        s_min = '%s mins ago and' % mins
        if mins == 1:
            s_min = '%s min ago and' % mins

        intro_tmpl = '%s %s %s %s not received an ACK/NACK.\n\n'
        msg_intro = intro_tmpl % (g_s[0], g_s[1], s_min, g_s[2])
        msg_body = '%s\n%s\n' % (data_msg, '-'*51)
        limit_raw = datetime.now() - timedelta(minutes=mins)
        limit = limit_raw.strftime(date_format)
        end_tmpl = 'Settlements released before %s.\nPython Script: %s.'
        msg_end = end_tmpl % (limit, __name__)
        message = msg_intro + msg_body + msg_end

        send_mail(subject, message, email)
    print('Completed Successfully')


def send_mail(subject, msg, email):
    """Send email"""
    body = string.join((
        "From: %s" % FROM,
        "To: %s" % email,
        "Subject: %s" % subject,
        "", msg), "\r\n")
    try:
        server = smtplib.SMTP(HOST)
        server.set_debuglevel(1)
        server.sendmail(FROM, email.split(','), body)
        server.quit()
    except smtplib.SMTPException as smtp_exception:
        print(smtp_exception)


ael_gui_parameters = {'closeWhenFinished': True}

ael_variables = AelVariableHandler()
ael_variables.add(
    'minutes',
    label='Age of event (mins)',
    cls='int',
    default=30)
ael_variables.add(
    'email',
    label='Email(s)',
    cls='string',
    multiple=True
)


def ael_main(dictionary):
    """Main function

    Load parameters from `ael_variables` and notifies RTB when (i) settlements
    are stagnated in `Released` status,  and/or (ii) settlements and/or
    confirmations receive a not valid SWIFT NACK.
    """
    mins = dictionary['minutes']
    email = ','.join(dictionary['email'])
    detect_released_settlements(mins, email)
    detect_false_nacks(email)
    detect_all_nacks(email)
