""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/RCRImportService.py"
import exceptions


"""
Connection strings.
"""
COMMAND_STRING = "/default.aspx?Command="
COMMAND_DELIMITER = "&"
PARAM_EQUAL_TOKEN = "="
SESSION_NAME_DELIMITER = "|"

"""
Response tag tokens
"""
RESPONSE_RESPONSE = "Response"
RESPONSE_SESSION = "Session"
RESPONSE_ID = "ID"
RESPONSE_STATUS = "Status"
RESPONSE_JOB = "Job"
RESPONSE_CUBE = "Cube"
RESPONSE_PARENT = "Parent"
RESPONSE_EXCEPTION = "Exception"
RESPONSE_MESSAGE = "Message"
RESPONSE_STACKTRACE = "StackTrace"
RESPONSE_SOURCE_SYSTEM = "SourceSystem"
RESPONSE_SOURCE_SYSTEM_ID = "SourceSystemID"
RESPONSE_SOURCE_SYSTEM_DATE = "SourceSystemDate"
RESPONSE_SUB_SESSIONS = "SubSessions"

"""
Response values
"""
RESPONSE_VALUE_JOB_SUBMITTED = "JobSubmitted"
RESPONSE_CUBE_STATUS_LOADED = "Loaded"
RESPONSE_CUBE_STATUS_DROPPED = "Dropped"
RESPONSE_VALUE_JOB_STATUS_STILL_RUNNING = "StillRunning"
RESPONSE_VALUE_JOB_STATUS_COMPLETED = "Completed"
RESPONSE_VALUE_JOB_STATUS_CANCELED = "Canceled"

"""
Command tokens
"""
COMMAND_SESSION_START = "SessionStart"
COMMAND_FILE_SUBMIT = "FileSubmit"
COMMAND_SESSION_COMPLETE = "SessionComplete"
COMMAND_SESSION_DROP = "SessionDrop"
COMMAND_SESSION_STATUS = "SessionStatus"
COMMAND_SESSION_CANCEL = "SessionCancel"
COMMAND_SUB_SESSIONS = "SessionSubSessions"
COMMAND_CLEANUP = "RunHousekeeping"

"""
Parameter tokens
"""
PARAM_SESSION_SOURCE_SYSTEM = "SessionSourceSystem"
PARAM_SESSION_NAME = "SessionName"
PARAM_SESSION_DATE = "SessionDate"
PARAM_SESSION_ID = "SessionID"
PARAM_CORRECTION_TYPE = "CorrectionType"
PARAM_RESULTS_SOURCE_NAME = "ResultsSourceName"
PARAM_FILE_PATH = "FilePath"
PARAM_DEFAULT_VALUE = "DefaultValue"
PARAM_USE_NULL_DEFAULT = "UseNullDefault"
PARAM_CORRECTION_SESSION_ID = "CorrectionSessionID"
PARAM_CORRECTION_TYPE = "CorrectionType"
PARAM_CORRECTION_SESSION_SOURCE_SYSTEM = "CorrectionSessionSourceSystem"
PARAM_CORRECTION_SESSION_NAME = "CorrectionSessionName"
PARAM_CORRECTION_SESSION_DATE = "CorrectionSessionDate"
PARAM_SESSION_SNAPSHOT = "SessionSnapshot"
PARAM_SESSION_INCREMENT = "SessionIncrement"
PARAM_SESSION_SNAPSHOT_IS_EOD = "SessionSnapshotIsEod"
PARAM_INCLUDE_DAYS = "DaysToInclude"
PARAM_CLEANUP_DATE = "RefDate"
PARAM_DELETE_BINARIES = "DeleteBinaryFiles"

"""
Parameter value tokens
"""
PAR_VALUE_NONE = "None"
PAR_VALUE_CORRECT = "Correct"
PAR_VALUE_BULK_CORRECT = "BulkCorrect"
PAR_VALUE_REMOVE = "Remove"
PAR_VALUE_ADDITIONS = "Additions"

"""
Constants
"""
WHITESPACE = " "
WHITESPACE_REPLACE = "%20"

"""
All valid RPC commands available for risk import task.
"""
REQUIRED_PARAMETERS = "required_parameters"
OPTIONAL_PARAMETERS = "optional_parameters"
command_signatures = {
    COMMAND_SESSION_START: {
        REQUIRED_PARAMETERS:    [PARAM_SESSION_SOURCE_SYSTEM,
                                 PARAM_SESSION_NAME,
                                 PARAM_SESSION_DATE,
                                 PARAM_CORRECTION_TYPE,
                                 PARAM_SESSION_SNAPSHOT,
                                 PARAM_SESSION_INCREMENT,
                                 PARAM_SESSION_SNAPSHOT_IS_EOD],
        OPTIONAL_PARAMETERS:    []
             },
    COMMAND_FILE_SUBMIT: {
        REQUIRED_PARAMETERS:    [PARAM_SESSION_ID],
        OPTIONAL_PARAMETERS:    [PARAM_CORRECTION_TYPE,
                                 PARAM_RESULTS_SOURCE_NAME,
                                 PARAM_FILE_PATH,
                                 PARAM_DEFAULT_VALUE,
                                 PARAM_USE_NULL_DEFAULT]
             },
    COMMAND_SESSION_COMPLETE: {
        REQUIRED_PARAMETERS:    [PARAM_SESSION_SOURCE_SYSTEM,
                                 PARAM_SESSION_NAME,
                                 PARAM_SESSION_DATE],
        OPTIONAL_PARAMETERS:    [PARAM_CORRECTION_TYPE,
                                 PARAM_CORRECTION_SESSION_ID]
             },
    COMMAND_SESSION_DROP: {
        REQUIRED_PARAMETERS:    [PARAM_SESSION_SOURCE_SYSTEM,
                                 PARAM_SESSION_NAME,
                                 PARAM_SESSION_DATE],
        OPTIONAL_PARAMETERS:    []
             },
    COMMAND_SESSION_STATUS: {
        REQUIRED_PARAMETERS:    [PARAM_SESSION_SOURCE_SYSTEM,
                                 PARAM_SESSION_NAME,
                                 PARAM_SESSION_DATE],
        OPTIONAL_PARAMETERS:    []
             },
    COMMAND_SESSION_CANCEL: {
        REQUIRED_PARAMETERS:    [PARAM_SESSION_SOURCE_SYSTEM,
                                 PARAM_SESSION_NAME,
                                 PARAM_SESSION_DATE],
        OPTIONAL_PARAMETERS:    []
            },
    COMMAND_SUB_SESSIONS: {
        REQUIRED_PARAMETERS:    [PARAM_SESSION_SOURCE_SYSTEM,
                                 PARAM_SESSION_NAME,
                                 PARAM_SESSION_DATE],
        OPTIONAL_PARAMETERS:    []
            },
    COMMAND_CLEANUP: {
            REQUIRED_PARAMETERS: [PARAM_INCLUDE_DAYS,
                                    PARAM_CLEANUP_DATE,
                                    PARAM_DELETE_BINARIES],
            OPTIONAL_PARAMETERS: []
            },
    }


class CubeRPCError(exceptions.Exception):
    pass


def _validate_command(cname, **kwargs):
    if cname not in command_signatures:
        raise CubeRPCError("No remote procedure named '{0}".format(cname))
    return True


def construct_request(command, **kwargs):
    _validate_command(command, **kwargs)
    params = COMMAND_DELIMITER.join(
        (PARAM_EQUAL_TOKEN.join([p,
         v.replace(WHITESPACE, WHITESPACE_REPLACE)]) \
         for p, v in list(kwargs.items())))
    return COMMAND_STRING + COMMAND_DELIMITER.join([command, params])
