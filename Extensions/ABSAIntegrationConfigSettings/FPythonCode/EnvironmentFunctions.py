"""---------------------------------------------------------------------------------------------------------------------
MODULE
    EnvironmentFunctions.

DESCRIPTION
    This module contains functionality for obtaining information about the current
    Front Arena environment.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer               Description
------------------------------------------------------------------------------------------------------------------------
2018-11-23                      Cuen Edwards            Initial implementation providing central services for logic
                                                        that was duplicated in several places.
2019-04-05      FAOPS-448       Cuen Edwards            Addition of Operations STP parameters.
2019-09-17      FAOPS-460       Cuen Edwards            Addition of Document Processing parameters.
2020-07-29      FAOPS-866       Cuen Edwards            Addition of supported client versions for an environment.
2020-10-21      FAOPS-959       Ncediso Nkambule        Addition of Operations NeoX activity report parameter.
------------------------------------------------------------------------------------------------------------------------
"""

import xml.etree.ElementTree as ElementTree

import acm


def get_environment_name():
    """
    Get the name of the current environment.
    """
    return acm.FDhDatabase['ADM'].InstanceName()


def is_production_environment():
    """
    Determine whether or not the current environment is a production
    environment.

    Please note that while DR uses different environment settings, it
    is also considered a production environment as it becomes the
    production environment in the event of a disaster.
    """
    settings_name = get_environment_settings_name()
    return settings_name in ['PRODSetting', 'DRSetting']


def get_supported_client_versions():
    """
    Get the client versions supported by the current environment.
    """
    return _get_environment_parameters('Client_Version_Config_Settings', 'client version settings',
        'Version', base_xpath='Supported_Versions', minimum_occurrences=1)


def get_environment_settings_name():
    """
    Get the name of the settings to use for the current environment.
    """
    root_element = ElementTree.fromstring(acm.GetDefaultValueFromName(acm.GetDefaultContext(),
        acm.FObject, 'EnvironmentSettings'))
    ads_address = acm.ADSAddress()
    all_host_elements = root_element.findall('Environment/Host')
    ads_host_elements = [
        ads_host_element for ads_host_element in all_host_elements
            if ads_host_element.get('Name').lower() == ads_address.lower()
    ]
    if len(ads_host_elements) == 0:
        raise ValueError('No environment settings name found for ADS address {ads_address}'.format(
            ads_address=ads_address
        ))
    elif len(ads_host_elements) > 1:
        raise ValueError('More than one environment settings name found for ADS address {ads_address}'.format(
            ads_address=ads_address
        ))
    return str(ads_host_elements[0].get('Setting'))


def get_confirmation_parameter(parameter_name):
    """
    Get an FConfirmationParameter for the current environment.
    """
    return _get_single_required_environment_parameter('FConfirmation_Config_Settings', 'confirmation settings',
        parameter_name)


def get_documentation_parameter(parameter_name):
    """
    Get an FDocumentationParameter for the current environment.

    Please note that these parameters are for the core FDocumentationParameters
    and not the custom documentation solution built on top of business processes.
    """
    return _get_single_required_environment_parameter('FDocumentation_Config_Settings', 'documentation settings',
        parameter_name)


def get_settlement_parameter(parameter_name):
    """
    Get an FSettlementParameter for the current environment.
    """
    return _get_single_required_environment_parameter('FSettlement_Config_Settings', 'settlement settings',
        parameter_name)


def get_operations_stp_parameter(parameter_name):
    """
    Get an OperationsSTPParameter for the current environment.
    """
    return _get_single_required_environment_parameter('OperationsSTP_Config_Settings', 'operations STP settings',
        parameter_name)


def get_neox_activity_report_parameter(parameter_name):
    """
    Get an NeoXActivityReportParameters for the current environment.
    """
    return _get_single_required_environment_parameter(
        config_settings_name='NeoXActivityReport_Config_Settings',
        config_settings_display_name='neox activity reports settings',
        parameter_name=parameter_name)


def get_document_processing_parameter(parameter_name):
    """
    Get a DocumentProcessingParameter for the current environment.

    Please note that these parameters are for the custom documentation
    solution built on top of business processes and not the core
    FDocumentationParameters.
    """
    return _get_single_required_environment_parameter('DocumentProcessing_Config_Settings',
        'document processing settings', parameter_name)


def _get_single_required_environment_parameter(config_settings_name, config_settings_display_name, parameter_name):
    """
    Get a single required environment parameter for the current environment.
    """
    return _get_environment_parameters(config_settings_name, config_settings_display_name, parameter_name,
        minimum_occurrences=1, maximum_occurrences=1)[0]


def _get_environment_parameters(config_settings_name, config_settings_display_name, parameter_name, base_xpath='',
        minimum_occurrences=None, maximum_occurrences=None):
    """
    Get environment parameters for the current environment.
    """
    environment_element = _get_environment_config_element(config_settings_name, config_settings_display_name)
    xpath = parameter_name
    if len(base_xpath) > 0:
        xpath = base_xpath + '/' + xpath
    parameter_elements = environment_element.findall(xpath)
    number_of_elements = len(parameter_elements)
    if minimum_occurrences is not None and number_of_elements < minimum_occurrences:
        if number_of_elements == 0:
            error_message = 'No environment {display_name} {parameter_name} parameter found for ADS '
            error_message += 'address {ads_address}.'
            raise ValueError(error_message.format(
                display_name=config_settings_display_name,
                parameter_name=parameter_name,
                ads_address=acm.ADSAddress()
            ))
        else:
            plural_suffix = ''
            if minimum_occurrences > 1:
                plural_suffix = 's'
            error_message = 'Less than {minimum_occurrences} environment {display_name} {parameter_name} '
            error_message += 'parameter{plural_suffix} found for ADS address {ads_address}.'
            raise ValueError(error_message.format(
                minimum_occurrences=minimum_occurrences,
                display_name=config_settings_display_name,
                parameter_name=parameter_name,
                plural_suffix=plural_suffix,
                ads_address=acm.ADSAddress()
            ))
    if maximum_occurrences is not None and number_of_elements > maximum_occurrences:
        plural_suffix = ''
        if maximum_occurrences > 1:
            plural_suffix = 's'
        error_message = 'More than {maximum_occurrences} environment {display_name} {parameter_name} '
        error_message += 'parameter{plural_suffix} found for ADS address {ads_address}.'
        raise ValueError(error_message.format(
            maximum_occurrences=maximum_occurrences,
            display_name=config_settings_display_name,
            parameter_name=parameter_name,
            plural_suffix=plural_suffix,
            ads_address=acm.ADSAddress()
        ))
    return [
        parameter_element.text for parameter_element in parameter_elements
    ]


def _get_environment_config_element(config_settings_name, config_settings_display_name):
    """
    Get the environment element for a particular configuration and
    the current environment.

    Exactly one element is expected to exist for an environment (either
    explicitly defined for the environment, via the settings name mapped
    for the environment, or implicitly defined, via default settings).
    """
    root_element = ElementTree.fromstring(acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject,
        config_settings_name))
    # Look for settings defined for the current environments settings name.
    environment_elements = _get_environment_element(config_settings_display_name, root_element,
        get_environment_settings_name())
    if len(environment_elements) == 0:
        # Fallback on any default settings (if present).
        environment_elements = _get_environment_element(config_settings_display_name, root_element, 'DefaultSetting')
    if len(environment_elements) == 0:
        error_message = 'No environment {display_name} found for ADS address {ads_address}.'
        raise ValueError(error_message.format(
            display_name=config_settings_display_name,
            ads_address=acm.ADSAddress()
        ))
    return environment_elements[0]


def _get_environment_element(config_settings_display_name, root_element, environment_settings_name):
    """
    Get the environment element for a particular configuration and
    settings name.

    Zero or one element is expected to exist for a settings name.
    """
    select_expression = "Environment[@ArenaDataServer='{environment_settings_name}']".format(
        environment_settings_name=environment_settings_name
    )
    environment_elements = root_element.findall(select_expression)
    if len(environment_elements) > 1:
        error_message = 'More than one {display_name} environment element found for settings {settings_name}.'
        raise ValueError(error_message.format(
            display_name=config_settings_display_name,
            settings_name=environment_settings_name
        ))
    return environment_elements
