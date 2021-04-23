"""-----------------------------------------------------------------------
MODULE
  site-startup

DESCRIPTION

  The site-startup module is invoked automatically when an
  PRIME client is started. Note that this module does not
  need to contain any named functions. The code in this
  module is executed directly.

  The site-startup module can for example be used to set
  up path to the ael extension directory

  In order to use the site-startup module rename this Template module
  to site-startup.

History:
Date            Who                     What
2009-03-05      Herman Hoon             CR 373907: SOX Passwords - notify users to change their passwords 5 days before it expires and when it expires.
2010-07-05      Rohan vd Walt           CR 375280: Updated Password change notification code to check for more users
2010-12-07      Francois Truter         CR 510452: Set Remote Sheet Host
2011-04-14      Heinrich Cronje         CR 662927: Added locations for .NET integrations and Operations .NET dlls.
2011-07-12      Anwar Banoo             Upgrade: Aligned paths to confirm with python 2.6
2013-01-11      Peter Fabian            CR 715317: Only override the settings when logged on from a Prime gui and don't affect the backend default suggestname.ttt file
2013-08-17      Heinrich Cronje         CHNG0001209844: BOPCUS 3 Upgrade - Added Request Handler Proxy
2015-03-24      Vojtech Sidorin         FAU-642 Update paths to 2014 dirs.
2016-03-01      Frantisek Jahoda        ABITFA-2818 Simplify expression with FUser.PasswordCheck, remove FSettlement custom methods
2020-07-29      Cuen Edwards            FAOPS-866: Only allow connections using supported client versions and some small code improvements.
ENDDESCRIPTION
-----------------------------------------------------------------------"""
from itertools import chain
import os
import sys
import traceback

import acm

from password_policy import PasswordPolicy
import importlib


COMMON_LIB_PATH_PROD = r'\\PV01MAPP041.corp.dsarena.com\Arena\CommonLib\2018/'
COMMON_LIB_PATH_OTHER = r'\\PV01MAPP041.corp.dsarena.com\Arena\CommonLib\2018/'


def redirect_stdout():
    """
    Redirect stdout to os.devnull for certain users.
    """
    try:
        userid = acm.UserName()
        if userid == 'EXTRACT':
            sys.stdout = open(os.devnull, 'w')
    except:
        acm.Log("An exception occurred while attempting to redirect stdout:\n{traceback}".format(
            traceback=traceback.format_exc()
        ))


def update_system_path():
    """
    Extend sys.path with paths to additional Python modules on Windows.
    """
    try:
        if os.name != 'nt':
            return
        import EnvironmentFunctions
        is_prod = EnvironmentFunctions.is_production_environment()
        common_prefix = COMMON_LIB_PATH_PROD if is_prod else COMMON_LIB_PATH_OTHER
        pure_python_part = 'pure_python'
        pure_python_paths = _get_subdirectories(common_prefix + pure_python_part)
        binary_part = 'binary/'
        if _is_64bits():
            binary_part += '64bit'
        else:
            binary_part += '32bit'
        binary_paths = _get_subdirectories(common_prefix + binary_part)
        # Inserting to the beginning of sys.path rather than appending so
        # the libraries specified here have higher priority than those in
        # the INI file (i.e. FCS_DIR_PYTHON_LIB and FCS_DIR_PYTHON_EXT)
        for lib_path in chain(pure_python_paths, binary_paths):
            sys.path.insert(1, lib_path)
    except:
        acm.Log("An exception occurred while attempting to update the system path:\n{traceback}".format(
            traceback=traceback.format_exc()
        ))


def ensure_client_version_supported():
    """
    Ensure that the connecting client (Prime, ATS, AMBA, ACM, etc.) version is
    supported by the current environment.
    """
    try:
        import EnvironmentFunctions
        current_client_version = _get_client_version()
        supported_client_versions = EnvironmentFunctions.get_supported_client_versions()
        if current_client_version in supported_client_versions:
            return
        message = _get_unsupported_client_version_message(current_client_version, supported_client_versions)
        _show_message(message)
        _shutdown()
    except:
        message = "An exception occurred while attempting to ensure that the connecting client "
        message += "version is supported by the current environment:\n{traceback}"
        acm.Log(message.format(
            traceback=traceback.format_exc()
        ))


def notify_for_expired_password():
    """
    Check for an expiring/expired password and notify the user if relevant.
    """
    try:
        policy = PasswordPolicy(acm.User())
        if not policy.does_apply():
            return

        if policy.is_password_expired():
            _show_message('Your password has expired.\n\n'
                         'You will not be able to make changes to the database.\n'
                         'Please change your password under File>Preferences>'
                         'Passwords>ADS to regain change permission.')
            return

        expires_in_days = policy.days_to_expiration()
        if expires_in_days < 5:
            # Warn user to change password 5 days before expire
            _show_message('You have %d days left to change your password.\n\n'
                         'You can change your password under '
                         'File>Preferences>Passwords>ADS' % expires_in_days)
    except:
        message = "An exception occurred while attempting to check for an expiring/"
        message += "expired password:\n{traceback}"
        acm.Log(message.format(
            traceback=traceback.format_exc()
        ))


def reload_at_logging():
    """
    Import and reload the at_logging module
    in order to replace its cached version in FA cache.
    """
    try:
        import at_logging
        importlib.reload(at_logging)
    except:
        acm.Log("An exception occurred while attempting to reload at_logging:\n{traceback}".format(
            traceback=traceback.format_exc()
        ))


def _get_subdirectories(directory):
    """
    Return a generator of paths to all subdirectories in the provided directory.
    """
    names = os.listdir(directory)
    # For consistency, forward slash is used as path separator everywhere.
    paths = [directory + '/' + name for name in names]
    return (path for path in paths if os.path.isdir(path))


def _is_64bits():
    return sys.maxsize > 2 ** 32


def _get_client_version():
    # Ideally we should be able to just use acm.ShortVersion()
    # but we have found that not all Front Arena components return
    # version information in a consistent manner.  For instance,
    # calling acm.ShortVersion() within AMBA (on Linux at least)
    # returns the version number with (64-bit) appended.
    return acm.ShortVersion().replace(" (64-bit)", "")


def _get_unsupported_client_version_message(current_client_version, supported_client_versions):
    import EnvironmentFunctions
    import SessionFunctions
    client_description = _get_client_description()
    message = "{client_description} version {current_client_version} is not supported in {environment_name}.\n\n"
    message = message.format(
        client_description=client_description,
        current_client_version=current_client_version,
        environment_name=EnvironmentFunctions.get_environment_name()
    )
    if SessionFunctions.is_prime():
        message += _get_unsupported_prime_version_remediation_message(supported_client_versions)
    else:
        message += _get_unsupported_other_client_version_remediation_message(supported_client_versions)
    return message


def _get_client_description():
    import SessionFunctions
    if SessionFunctions.is_prime():
        # Return a user-friendly description.
        return "Front Arena"
    # Return a more specific description if possible.
    if acm.GetConfigVar('amba_name') is not None:
        return "AMBA"
    if acm.GetConfigVar('ats_name') is not None:
        return "ATS"
    executable_name = os.path.basename(sys.executable).lower()
    if executable_name.startswith("arena_python"):
        return "Arena Python"
    if executable_name.startswith("python"):
        return "ACM"
    return "Front Arena"


def _get_unsupported_prime_version_remediation_message(supported_client_versions):
    if len(supported_client_versions) == 1:
        return "Please contact IT support to obtain version {supported_client_version}.".format(
            supported_client_version=supported_client_versions[0]
        )
    message = "Please contact IT support to obtain one of the following supported versions:"
    for supported_client_version in supported_client_versions:
        message += "\n- {supported_client_version}".format(
            supported_client_version=supported_client_version
        )
    return message


def _get_unsupported_other_client_version_remediation_message(supported_client_versions):
    import EnvironmentFunctions
    message = "To resolve:\n"
    message += "- Determine whether or not the currently installed version is correct.\n"
    message += "- If correct, review and amend the list of supported versions for {environment_settings} "
    message += "in FExtensionValue 'Client_Version_Config_Settings'.\n"
    message = message.format(
        environment_settings=EnvironmentFunctions.get_environment_settings_name()
    )
    if len(supported_client_versions) == 1:
        message += "- If incorrect, install version {supported_client_version}.".format(
            supported_client_version=supported_client_versions[0]
        )
    else:
        message += "- If incorrect, install the appropriate version from the following list:"
        for supported_client_version in supported_client_versions:
            message += "\n  - {supported_client_version}".format(
                supported_client_version=supported_client_version
            )
    return message


def _show_message(message):
    import SessionFunctions
    if SessionFunctions.is_prime():
        acm.GetFunction("msgBox", 3)("Warning", message, 0)
    acm.Log(message)


def _shutdown():
    try:
        import psutil
        process = psutil.Process(os.getpid())
        process.terminate()
    except:
        acm.Log("An exception occurred while attempting to shutdown:\n{traceback}".format(
            traceback=traceback.format_exc()
        ))


redirect_stdout()
update_system_path()
ensure_client_version_supported()
notify_for_expired_password()
reload_at_logging()
