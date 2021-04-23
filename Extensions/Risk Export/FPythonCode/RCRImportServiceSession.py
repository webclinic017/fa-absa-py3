""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/RCRImportServiceSession.py"
import exceptions
import urllib.request, urllib.error, urllib.parse
import RCRImportService
reload(RCRImportService)
from xml.etree import cElementTree

STATUS_KEY_SESSION_ID = "session id"
STATUS_KEY_SESSION_STATUS = "session status"
STATUS_KEY_CUBE_STATUS = "cube status"
STATUS_KEY_JOB_STATUS = "job status"
STATUS_KEY_PARENT = "parent"
STATUS_SOURCE_SYSTEM = "source system"
STATUS_SOURCE_SYSTEM_NAME = "session name"
STATUS_SOURCE_SYSTEM_DATE = "session date"

CLEANUP_DATE = "cleanUpDate"
INCLUDE_DAYS = "includeDays"
DELETE_BINS = "deleteBinaries"
TRUE_FALSE = ['false', 'true']

import FLogger
logger = FLogger.FLogger.GetLogger('FRiskCubeDataUpload')

class CubeResponseError(exceptions.Exception):
    def __init__(self, message, stack_trace=None):
        super(CubeResponseError, self).__init__(message)
        self.stack_trace = stack_trace


class CubeImportSession(object):
    """
    Represents a session node in a session hierarchy.
    """
    def __init__(self, base_url, session_src_system, name,
            session_date, session_snapshot_name, session_snapshot_is_eod,
            session_increment,
            correction_type=None, correction_session=None,
            parent_session=None, username=None,
            password=None):
        self.base_url = base_url
        self.session_src_system = session_src_system
        self.name = name
        self.session_snapshot_name = session_snapshot_name
        self.session_increment = session_increment
        self.session_snapshot_is_eod = session_snapshot_is_eod
        self.parent_session = parent_session
        self.cmp_name = self._compound_name()
        self.session_date = session_date
        self.correction_type = correction_type
        self.correction_session = correction_session
        if username and password:
            self.opener = self._get_url_opener(username, password, base_url)
        else:
            self.opener = urllib.request.urlopen

    def _all_sessions(self):
        if not self.parent_session:
            return [self.name]
        else:
            names = self.parent_session._all_sessions()
            names.append(self.name)
            return names

    def _check_error(self, resp_tree):
        error = resp_tree.find(RCRImportService.RESPONSE_EXCEPTION)
        if error:
            msg = error.find(RCRImportService.RESPONSE_MESSAGE).text
            stack_trace = error.find(RCRImportService.RESPONSE_STACKTRACE).text
            raise CubeResponseError(msg, stack_trace)

    def _compound_name(self):
        return RCRImportService.SESSION_NAME_DELIMITER.join(
                self._all_sessions())

    def _get_correction_session_id_params(self):
        session = self.correction_session
        return {
                RCRImportService.PARAM_CORRECTION_SESSION_SOURCE_SYSTEM:
                        session.session_src_system,
                RCRImportService.PARAM_CORRECTION_SESSION_NAME:
                        session.cmp_name,
                RCRImportService.PARAM_CORRECTION_SESSION_DATE:
                        session.session_date}

    def _get_session_id_params(self):
        params = {
                RCRImportService.PARAM_SESSION_SOURCE_SYSTEM:
                        self.session_src_system,
                RCRImportService.PARAM_SESSION_NAME:
                        self.cmp_name,
                RCRImportService.PARAM_SESSION_DATE:
                        self.session_date}
        return params

    def _get_url_opener(self, username, password, base_url):
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, base_url, username, password)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        return opener

    def _header_dict(self):
        return {"User-Agent":
                "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)"}

    def _parse_status_response(self, xml_response):
        xml_response = xml_response.strip()
        resp_tree = cElementTree.fromstring(xml_response)
        self._check_error(resp_tree)
        session_nd = resp_tree.find(RCRImportService.RESPONSE_SESSION)
        return self._status_response_rec(session_nd)

    def _parse_submit_response(self, xml_response):
        xml_response = xml_response.strip()
        resp_nd = cElementTree.fromstring(xml_response)
        self._check_error(resp_nd)
        if resp_nd is not None and \
            (resp_nd.text == RCRImportService.RESPONSE_VALUE_JOB_SUBMITTED):
            return RCRImportService.RESPONSE_VALUE_JOB_SUBMITTED
        else:
            raise CubeResponseError("Invalid response:\n{0}".format(
                xml_response))

    def _parse_sub_sessions_response(self, xml_response):
        sub_sessions = []
        xml_response = xml_response.strip()
        resp_tree = cElementTree.fromstring(xml_response)
        self._check_error(resp_tree)
        resp_nd = resp_tree.find(RCRImportService.RESPONSE_SESSION)
        sub_session_nd = resp_nd.find(RCRImportService.RESPONSE_SUB_SESSIONS)
        if sub_session_nd:
            for session_nd in sub_session_nd.getchildren():
                sub_sessions.append(self._status_response_rec(session_nd))
        return sub_sessions

    def _send_request(self, req_url):
        url = "".join([self.base_url, req_url])
        req = urllib.request.Request(url, headers=self._header_dict())
        try:
            logger.DLOG("Sending: {0}".format(url))
            res = self.opener(req).read()
            logger.DLOG("Received: {0}".format(res))
            return res
        except urllib.error.URLError as url_error:
            raise url_error

    def _find_tag(self, session_or_parent_nd, tag):
        if not session_or_parent_nd.find(tag) == None:
            return session_or_parent_nd.find(tag).text
        return None

    def _status_response_rec(self, session_or_parent_nd):
        out = {}
        out[STATUS_KEY_SESSION_ID] = self._find_tag(session_or_parent_nd,
                RCRImportService.RESPONSE_ID)
        out[STATUS_SOURCE_SYSTEM] = self._find_tag(session_or_parent_nd,
                RCRImportService.RESPONSE_SOURCE_SYSTEM)
        out[STATUS_SOURCE_SYSTEM_NAME] = self._find_tag(session_or_parent_nd,
                RCRImportService.RESPONSE_SOURCE_SYSTEM_ID)
        out[STATUS_SOURCE_SYSTEM_DATE] = self._find_tag(session_or_parent_nd,
                RCRImportService.RESPONSE_SOURCE_SYSTEM_DATE)
        out[STATUS_KEY_SESSION_STATUS] = self._find_tag(session_or_parent_nd,
                "/".join([RCRImportService.RESPONSE_STATUS,
                RCRImportService.RESPONSE_SESSION]))
        out[STATUS_KEY_JOB_STATUS] = self._find_tag(session_or_parent_nd,
                "/".join([RCRImportService.RESPONSE_STATUS,
                RCRImportService.RESPONSE_JOB]))
        out[STATUS_KEY_CUBE_STATUS] = self._find_tag(session_or_parent_nd,
                "/".join([RCRImportService.RESPONSE_STATUS,
                RCRImportService.RESPONSE_CUBE]))
        if session_or_parent_nd.find("Parent"):
            out[STATUS_KEY_PARENT] = self._status_response_rec(
                    session_or_parent_nd.find("Parent"))
        return out

    def create_sub_session(self, name, correction_session=None,
                correction_type=None, overridden_session_increment=None):
        if self.is_started():
            subsessions = self.sub_sessions(name)
            index = len(subsessions)
            name += "_" + str(index)

        if overridden_session_increment is not None:
            session_increment = overridden_session_increment
        else:
            session_increment = self.session_increment

        sub_session = CubeImportSession(self.base_url, self.session_src_system,
                name, self.session_date, self.session_snapshot_name,
                self.session_snapshot_is_eod, session_increment,
                correction_type, correction_session, self)
        sub_session.opener = self.opener
        return sub_session

    def file_submit(self, file_path):
        params = self._get_session_id_params()
        params.update({RCRImportService.PARAM_FILE_PATH: file_path})
        req_url = RCRImportService.construct_request(
            RCRImportService.COMMAND_FILE_SUBMIT, **params)
        response = self._send_request(req_url)
        return self._parse_submit_response(response)

    def cleanUp(self, args):
        params = {RCRImportService.PARAM_INCLUDE_DAYS: str(args[INCLUDE_DAYS]),
                RCRImportService.PARAM_CLEANUP_DATE: args[CLEANUP_DATE],
                RCRImportService.PARAM_DELETE_BINARIES:
                    TRUE_FALSE[args[DELETE_BINS]]}
        request = RCRImportService.construct_request(
                RCRImportService.COMMAND_CLEANUP, **params)
        return self._send_request(request)

    def is_correction_session(self):
        return (self.correction_type and
                self.correction_type != RCRImportService.PAR_VALUE_NONE)

    def cancel(self):
        req_url = RCRImportService.construct_request(
                RCRImportService.COMMAND_SESSION_CANCEL,
                **self._get_session_id_params())
        response = self._send_request(req_url)
        return self._parse_submit_response(response)

    def complete(self):
        params = self._get_session_id_params()
        req_url = RCRImportService.construct_request(
            RCRImportService.COMMAND_SESSION_COMPLETE, **params)
        response = self._send_request(req_url)
        return self._parse_submit_response(response)

    def drop(self):
        req_url = RCRImportService.construct_request(
                RCRImportService.COMMAND_SESSION_DROP,
                **self._get_session_id_params())
        response = self._send_request(req_url)
        return self._parse_submit_response(response)

    def id(self):
        return self.status()[STATUS_KEY_SESSION_ID]

    def identifier(self):
        return "|".join(self._all_sessions() + [self.session_date,
            self.session_src_system])

    def is_started(self):
        try:
            self.status()
        except CubeResponseError:
            return False
        return True

    def job_status(self):
        status = self.status()
        return status[STATUS_KEY_JOB_STATUS]

    def session_name(self):
        return self.name

    def start(self):
        params = self._get_session_id_params()
        params.update({
                RCRImportService.PARAM_CORRECTION_TYPE: self.correction_type})
        params.update({
                RCRImportService.PARAM_SESSION_SNAPSHOT:
                        self.session_snapshot_name})
        params.update({
                RCRImportService.PARAM_SESSION_INCREMENT:
                        self.session_increment})
        params.update({
                RCRImportService.PARAM_SESSION_SNAPSHOT_IS_EOD:
                        self.session_snapshot_is_eod})

        req_url = RCRImportService.construct_request(
            RCRImportService.COMMAND_SESSION_START, **params)
        response = self._send_request(req_url)
        return self._parse_status_response(response)

    def status(self):
        req_url = RCRImportService.construct_request(
                RCRImportService.COMMAND_SESSION_STATUS,
                **self._get_session_id_params())
        response = self._send_request(req_url)
        return self._parse_status_response(response)

    def sub_sessions(self, name_filter=None, status_exlusion_filter=None):
        req_url = RCRImportService.construct_request(
                RCRImportService.COMMAND_SUB_SESSIONS,
                **self._get_session_id_params())
        response = self._send_request(req_url)
        sessions = self._parse_sub_sessions_response(response)

        if name_filter is not None:
            sessions = filter(
                    lambda x: name_filter in x["session name"], sessions)
        if status_exlusion_filter is not None:
            sessions = filter(
                    lambda x: x["session status"] != status_exlusion_filter,
                    sessions)
        return sessions

    def _create_session_from_dict(self, d, session_creator, parent):
        return session_creator(d["session name"], None, None, parent)

    def actual_active_sub_sessions(self, session_creator, name_filter=None):
        active_sub_sessions = self.sub_sessions(name_filter,
                RCRImportService.RESPONSE_VALUE_JOB_STATUS_CANCELED)
        sessions = []
        for active_sub_session in active_sub_sessions:
            sessions.append(self._create_session_from_dict(active_sub_session,
                    session_creator, self))
        return sessions


def create_session_wrapper(base_url, session_src_system, session_date,
    session_snapshot_name, session_snapshot_is_eod, session_increment):
    def create_session(name, correction_type=None, correction_session=None,
        parent_session=None, username=None, password=None):
        return CubeImportSession(base_url, session_src_system, name,
                session_date, session_snapshot_name, session_snapshot_is_eod,
                session_increment, correction_type, correction_session,
                parent_session, username, password)
    return create_session
