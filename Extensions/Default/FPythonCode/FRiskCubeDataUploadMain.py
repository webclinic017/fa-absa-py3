""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FRiskCubeDataUploadMain.py"
from __future__ import print_function
import acm
import time
import exceptions
import FLogger
import RCRImportService
import RCRImportServiceSession
from RCRImportServiceSession import CubeResponseError
import importlib

importlib.reload(RCRImportService)
importlib.reload(RCRImportServiceSession)

logger = FLogger.FLogger.GetLogger('FRiskCubeDataUpload')

CORRECTION_TYPE_CORRECT = RCRImportService.PAR_VALUE_CORRECT
CORRECTION_TYPE_NONE = RCRImportService.PAR_VALUE_NONE
JOB_STATUS_STILL_RUNNING = (RCRImportService.
        RESPONSE_VALUE_JOB_STATUS_STILL_RUNNING)
JOB_STATUS_COMPLETED = RCRImportService.RESPONSE_VALUE_JOB_STATUS_COMPLETED

ACTIONS = ("EOD", "Correction", "Remove EOD", "Remove Correction")

SESSION_SOURCE_SYSTEM = "Front"
MASTER_SESSION_EOD = "EOD_Master"
SUB_SESSION_EOD = "EOD"
SUB_SESSION_CORRECTION = "Correction"
SUB_SESSION_CORRECTION_CONTROL = "Correction_Control"
SESSION_INCREMENT_NAME = "Initial"
SESSION_SNAPSHOT_NAME = "EOD"
SESSION_SNAPSHOT_IS_EOD = "True"
RETRY_TIME_OUT_VALIDATE_JOB = 20
MAX_NUMBER_RETRIES = 1 * 60 * 60 / RETRY_TIME_OUT_VALIDATE_JOB


class JobCompletionError(exceptions.Exception):
    def __init__(self, message, stack_trace=None):
        super(JobCompletionError, self).__init__(message)
        self.stack_trace = stack_trace


def is_gui_client():
    try:
        from acm import FTmServer
        return True
    except:
        return False


def validate_job_completed(session):
    print_progress = is_gui_client()
    job_status = session.job_status()
    if job_status == JOB_STATUS_COMPLETED:
        return
    if print_progress:
        logger.LOG("Waiting for job to complete")
    count = 0
    while (job_status == JOB_STATUS_STILL_RUNNING and
           count < MAX_NUMBER_RETRIES):
        time.sleep(RETRY_TIME_OUT_VALIDATE_JOB)
        job_status = session.job_status()
        count += 1
        print("+", end=' ')
    print(" ")
    if job_status != JOB_STATUS_COMPLETED:
        if count >= MAX_NUMBER_RETRIES:
            msg = "Job failed due to timeout"
        else:
            msg = "Job failed, status: '%s'" % job_status
        raise JobCompletionError(msg)


def cancel_session(session, log=False):
    session.cancel()
    if log:
        logger.LOG("Canceled session '%s'" % session.identifier())


def drop_session(session, log=False):
    session.drop()
    if log:
        logger.LOG("Dropped session '%s'" % session.identifier())


def drop_cancel_session(session, log=True):
    drop_session(session)
    session.cancel()
    if log:
        logger.LOG("Removed session '%s'" % session.identifier())


def file_import(session, target_file):
    try:
        session.file_submit(target_file)
    except CubeResponseError as msg:
        err_msg = "Could not submit file '%s': %s" % (target_file, msg)
        logger.ELOG(err_msg)
    else:
        logger.LOG("Submitted file '%s'" % target_file)


def import_files(target_files, master_session, session, validate_job=False,
        correction_session=None):
    try:
        if session.is_started():
            logger.LOG("Using session %s" % session.identifier())
        else:
            session.start()
            logger.LOG("Created session '%s'" % session.identifier())

        for target_file in target_files:
            file_import(session, target_file)
        if validate_job:
            validate_job_completed(session)
        session.complete()
        logger.LOG("Completed session '%s'" % session.identifier())
        if correction_session:
            correction_session.complete()
            logger.LOG("Completed session '%s'" %
                    correction_session.identifier())
        master_session.complete()
        logger.LOG("Completed session '%s'" % master_session.identifier())

    except Exception as msg:
        logger.ELOG("File upload failed: %s" % msg)
        if session and session.is_started():
            drop_cancel_session(session, False)
            logger.ELOG("Removed session '%s'" % session.identifier())
        raise


def get_correction_session(session_creator, session):
    correction_session = session.create_sub_session(SUB_SESSION_CORRECTION,
        session, CORRECTION_TYPE_CORRECT, session.session_name())
    return correction_session


def get_correction_control_session(session_creator, session):
    correction_control_session = session.create_sub_session(
            SUB_SESSION_CORRECTION_CONTROL, session)
    return correction_control_session


def remove_session(session, session_creator):
    if not session.is_started():
        logger.ELOG("Session to remove '%s' does not exist" %
                session.identifier())
        return
    subsessions = session.actual_active_sub_sessions(session_creator)
    for subsession in subsessions:
        remove_session(subsession, session_creator)
    drop_cancel_session(session)


def remove_sessions(sessions, session_creator):
    for session in sessions:
        remove_session(session, session_creator)


def correct_session(target_files, session, session_creator):
    if not session.is_started():
        logger.ELOG("Session to correct '%s' does not exist" %
                session.identifier())
        return
    correction_control_session = get_correction_control_session(
            session_creator, session)
    correction_session = get_correction_session(session_creator,
            correction_control_session)
    import_files(target_files, session, correction_session, True,
            correction_control_session)


def remove_sub_sessions(session, session_creator, sub_session_filter):

    try:
        sub_sessions = session.actual_active_sub_sessions(session_creator,
                sub_session_filter)
        # Log the special case of having no sub sessions.
        if not sub_sessions:
            raise Exception
    except Exception:
        info_msg = "No data to remove could be found."
        logger.LOG(info_msg)
        return

    try:
        remove_sessions(sub_sessions, session_creator)
    except Exception as msg:
        err_msg = "The removal process failed, reason: %s" % msg
        logger.ELOG(err_msg)


def cleanUp(controlSession, params):
    try:
        logger.LOG("Starting clean up session...")
        subSession = controlSession.create_sub_session(SUB_SESSION_EOD,
                correction_type=CORRECTION_TYPE_NONE)
        subSession.start()
        subSession.cleanUp(params)
        validate_job_completed(subSession)
        subSession.complete()
        controlSession.complete()
        logger.LOG("Done cleaning up. Success!")
    except Exception as ex:
        logger.ELOG("Cube clean up failed: {0}".format(ex))
        if subSession and subSession.is_started():
            drop_cancel_session(subSession, False)
            logger.ELOG("Cancelled session {0}".format(
                subSession.identifier()))


def main(action, reference_date, base_url, port, target_files, **kwargs):
    url = ":".join([base_url, str(port)])
    session_creator = RCRImportServiceSession.create_session_wrapper(url,
            SESSION_SOURCE_SYSTEM, reference_date, SESSION_SNAPSHOT_NAME,
            SESSION_SNAPSHOT_IS_EOD, SESSION_INCREMENT_NAME)
    eod_master = session_creator(MASTER_SESSION_EOD)
    monitor = kwargs.get('Monitor', False)

    if kwargs.get('cleanUp', False):
        cleanUp(eod_master, kwargs)
    elif action == "EOD":
        eod_session = eod_master.create_sub_session(SUB_SESSION_EOD,
                correction_type=CORRECTION_TYPE_NONE)
        import_files(target_files, eod_master, eod_session, monitor)
    elif action == "Correction":
        correct_session(target_files, eod_master, session_creator)
    elif action == "Remove EOD":
        remove_sub_sessions(eod_master, session_creator, SUB_SESSION_EOD)
    elif action == "Remove Correction":
        remove_sub_sessions(eod_master, session_creator,
                SUB_SESSION_CORRECTION_CONTROL)

