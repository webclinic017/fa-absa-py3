""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/etc/FPackagesProcessing.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FPackagesProcessing - Instrument/deal packages tasks GUI base

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPGui
import FBDPCustomPairDlg
import importlib
importlib.reload(FBDPCustomPairDlg)
import FBDPCustomSingleDlg
importlib.reload(FBDPCustomSingleDlg)
glob_vars = {
    'deal_pkgs': None,
    'ins_pkgs': None,
    'ins_pkg_name_to_oid': {},
    'deal_pkg_name_to_oid': {},
}

#Tooltips
ttDate = (
    'Action will be performed on instrument/deal package(s) that '
    'whose instruments expired before this date (time < date).'
)
ttInsPkgs = 'Select instrument package(s) on which to perform action'
ttDealPkgs = 'Select deal package(s) on which to perform action.'
ttOpenTradeDays = (
    'Only trades with trade time < (date - Trade open days) will be modified.'
)
days = [
    acm.Time.DateToday(),
    'Today',
    'First of Month',
    'First of Quarter',
    'First of Year'
]

def inputCb(index, field_values):
    input_hook_cb = glob_vars.get('input_hook_cb')
    if input_hook_cb:
        field_values = input_hook_cb(index, field_values)

    is_deal_pkg = glob_vars['ael_variables'][index][0] == 'DealPkgs'
    return packagesCb(field_values, index, is_deal_pkg)

def packagesCb(field_values, index, isDealPkg):
    input_pkgs = field_values[index]
    if (not input_pkgs) or (not len(input_pkgs)):
        input_pkgs = False

    glob_vars_key = 'deal_pkgs' if isDealPkg else 'ins_pkgs'
    glob_vars[glob_vars_key] = input_pkgs
    if not input_pkgs:
        field_values[index] = None
    else:
        input_pkgs = str(input_pkgs)
        is_first_call = glob_vars[glob_vars_key] is None
        pkg_type = 'deal' if isDealPkg else 'instrument'
        for name in input_pkgs.split(','):
            name = name.strip()
            if (not len(name)) and not is_first_call:
                msg = (
                    'Ensure all selected %s packages '
                    'have their name fields specified' % pkg_type
                )
                raise Exception(msg)

    return field_values

def customArchivedInstrumentPackageDialog(shell, params):
    dialog = FBDPCustomSingleDlg.SelectArchivedInstrumentPackagesCustomDialog(
        shell=shell, params=params,
        name_to_oid_dict=glob_vars['ins_pkg_name_to_oid']
    )
    return dialog.Create()

def customArchivedDealPackageDialog(shell, params):
    dialog = FBDPCustomPairDlg.SelectArchivedDealPackagesCustomDialog(
        shell=shell, params=params,
        name_to_oid_map=glob_vars['deal_pkg_name_to_oid']
    )
    return dialog.Create()

def performOnArchivedObjectsCb(perform_on_archived_objs, field_values):
    # Reset selection options accordingly and empty field values
    ins_pkgs_var = glob_vars['ael_variables'].InsPkgs
    deal_pkgs_var = glob_vars['ael_variables'].DealPkgs
    if perform_on_archived_objs:
        # InsPkgs will be a list of string names
        ins_pkgs_var.type = 'string'
        ins_pkgs_var.default_value = None
        ins_pkgs_var.selectionDialog = customArchivedInstrumentPackageDialog
        # DealPkgs will be a list of string names
        deal_pkgs_var.type = 'string'
        deal_pkgs_var.default_value = None
        deal_pkgs_var.selectionDialog = customArchivedDealPackageDialog
    else:
        # InsPkgs will be a list of FInstrumentPackage
        ins_pkgs_var.type = 'FInstrumentPackage'
        ins_pkgs_var.default_value = FBDPGui.insertInstrumentPackage()
        ins_pkgs_var.selectionDialog = None
        # DealPkgs will be a list of string oids
        deal_pkgs_var.type = 'FDealPackage'
        deal_pkgs_var.default_value = FBDPGui.insertDealPackage()
        deal_pkgs_var.selectionDialog = None

    glob_vars['perform_on_archived_objs'] = perform_on_archived_objs
    return field_values

def init(
        script_name, input_hook_cb=None,
        ael_variables_to_prepend=tuple(),
        ael_variables_to_append=tuple()
):
    #Setup GUI with default parameters
    glob_vars.update({
        'input_hook_cb': input_hook_cb,
        'perform_on_archived_objs': False,
        'script_name': script_name
    })
    FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters(
        'FBDPParameters', script_name
    )

    #Setup intended AEL variables
    if isinstance(ael_variables_to_prepend, (list, set)):
        ael_variables_to_prepend = tuple(ael_variables_to_prepend)

    if isinstance(ael_variables_to_append, (list, set)):
        ael_variables_to_append = tuple(ael_variables_to_append)

    assert isinstance(ael_variables_to_prepend, tuple)
    assert isinstance(ael_variables_to_append, tuple)

    variables = ael_variables_to_prepend + (
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled, Dialog]
        ['Date',
                'Date',
                'string', days, 'Today',
                1, False, ttDate, None, True, None],
        ['InsPkgs',
                'Instrument packages',
                'string', None, None,
                0, True, ttInsPkgs, inputCb, True, None],
        ['DealPkgs',
                'Deal packages',
                'string', None, None,
                0, True, ttDealPkgs, inputCb, True, None],
        ['OpenTradeDays',
               'Trade open days',
               'int', None, 0,
               0, False, ttOpenTradeDays, None, True, None],
    ) + ael_variables_to_append
    ael_variables = FBDPGui.TestVariables(*variables)
    glob_vars['ael_variables'] = ael_variables
    performOnArchivedObjectsCb(False, None)
    return ael_variables

def aelMain(performer_module, params):
    # ensure params['InsPkgs'] and params['DealPkgs'] consist of a
    # list of strings and not actual acm entities.
    pkgs = params['InsPkgs']
    if len(pkgs):
        if isinstance(pkgs[0], str):
            name_to_oid = glob_vars['ins_pkg_name_to_oid']
            params['ins_pkg_oids'] = [name_to_oid[name] for name in pkgs]
        else:
            params['ins_pkg_oids'] = [pkg.Oid() for pkg in pkgs]
            params['InsPkgs'] = [pkg.Name() for pkg in pkgs]
    else:
        params['InsPkgs'] = []

    pkgs = params['DealPkgs']
    if len(pkgs):
        if isinstance(pkgs[0], str):
            name_to_oid = glob_vars['deal_pkg_name_to_oid']
            params['deal_pkg_oids'] = [name_to_oid[name] for name in pkgs]
        else:
            params['deal_pkg_oids'] = [pkg.Oid() for pkg in pkgs]
            params['DealPkgs'] = [pkg.Name() for pkg in pkgs]
    else:
        params['DealPkgs'] = []

    script_name = glob_vars['script_name']
    params['ScriptName'] = script_name

    #Import Front modules
    import FBDPCommon
    import FBDPCurrentContext

    #Create logger
    FBDPCurrentContext.CreateLog(
        ScriptName=script_name,
        LogMode=params['Logmode'],
        LogToConsole=params['LogToConsole'],
        LogToFile=params['LogToFile'],
        Logfile=params['Logfile'],
        SendReportByMail=params['SendReportByMail'],
        MailList=params['MailList'],
        ReportMessageType=params['ReportMessageType']
    )
    #Execute relevant perform script
    FBDPCommon.execute_script(performer_module.perform, params)
