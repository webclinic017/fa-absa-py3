""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/corp_actions/etc/FSetPhysicalContractSize.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FSetPhysicalContractSize - Sets the physical contract size of selected
    derivatives.

DESCRIPTION
    This module sets the physical contract size of those derivatives
    selected in the AEL Variables window.
----------------------------------------------------------------------------"""


import string
import re

import ael

import FBDPString
import FBDPGui
from FBDPCurrentContext import Logme
from FBDPCurrentContext import CreateLog


# LOG HANDLING:

# Name of this script used in START, STOP and FINISH messages:

ScriptName = 'SetPhysicalContractSize'

# Specify how extensive logging you desire:

#LogMode = 0       # Messages of type: START, STOP, WARNING, ERROR
LogMode = 1        # Messages of type: START, STOP, WARNING, ERROR, INFO
#LogMode = 2       # Messages of type: START, STOP, WARNING, ERROR, INFO, DEBUG
#LogMode = None    # The default setting from FBDPParameters will be used

# Specify if you want to print to the console:

LogToConsole = 1        # The output will be printed to the console
#LogToConsole = 0       # Output will not be printed to the console
#LogToConsole = None    # The default setting from FBDPParameters will be used

# Specify if you want to print to a file:

#LogToFile = 1          # The output will be printed to the file <LogFile>
LogToFile = 0           # Output will not be printed to file
#LogToFile = None       # The default setting from FBDPParameters will be used

# Specify your logfile:

#Logfile = 'C:\\temp\\BDP_SetPhysicalContractSize.log'

# If you want to use own directory, log file will be placed in default
# directory specified by Logdir in FBDPParameters
Logfile = 'BDP_SetPhysicalContractSize.log'


#Default directory and filename BDP_<ScriptName>.log will be used
#Logfile = None


# The following is a list  of underlying stocks and their contract sizes,
# retreived from a ttt-file. The list should vary depending on which
# instruments
# (from which country, etc) have been traded. If no list is supplied, it is
# possible
# to select via the macro variables window which instruments to set
# phys contr size
# for instead.
corp_act_dict = {
        'ADS.*': 100,
        'ALV.*': 50,
        'BAS.*': 100,
        'BAY.*': 100,
        'BHW.*': 100,
        'BMW.*': 100,
        'HVM.*': 100,
        'CBK.*': 100,
        'CON.*': 100,
        'DCX.*': 100,
        'DBK.*': 100,
        'DHA.*': 100,
        'DOU.*': 100,
        'DRB.*': 100,
        'DTE.*': 100,
        'FRE3.*': 100,
        'GBF.*': 100,
        'HEN3.*': 100,
        'HOE.*': 100,
        'HOZ.*': 10,
        'INN.*': 100,
        'KAR.*': 100,
        'KLK.*': 10,
        'LHA.*': 100,
        'LIN.*': 100,
        'MAN.*': 100,
        'MET.*': 100,
        'MEO.*': 100,
        'MMN.*': 100,
        'MRK.*': 100,
        'MUV2.*': 50,
        'PRS.*': 100,
        'RWE.*': 100,
        'RWE3.*': 100,
        'SAP3.*': 100,
        'SCH.*': 100,
        'SIE.*X$': 150,
        'SIE.*Y$': 150,
        'SIE.*[0-9]$': 100,
        'THY.*': 10,
        'TKA.*': 100,
        'VEB.*': 100,
        'VIA.*Y$': 40,
        'VIA.*X$': 40,
        'VIA.*[0-9]$': 100,
        'VOW.*': 100,
        'VOW3.*': 100,
        'ABB.*': 10,
        'ALUB.*': 10,
        'CIBN.*': 10,
        'CLN.*': 10,
        'CSGN.*': 10,
        'HOL.*': 10,
        'NESN.*': 10,
        'NOVN.*': 100,
        'RA.*': 10,
        'ROG.*': 1,
        'RUKN.*': 10,
        'SBVN.*': 10,
        'SCMN.*': 10,
        'SMHN.*': 10,
        'SRN.*': 10,
        'SUN.*': 10,
        'UHRN.*': 10,
        'WINN.*': 50,
        'ZURN.*': 10
}

instr = ael.asql("""select ui.insid, ia.alias \
    from \
     instrument ui, \
     instrument i, \
     instrumentalias ia, \
     instraliastype iat \
    where \
      i.insaddr = ia.insaddr and \
      ia.type = iat.oid and \
      iat.alias_type_name = 'EUREX' and \
      ui.insaddr = i.und_insaddr and \
      ui.instype = 1""")[1]

if instr == [[]]:
    instr = ael.asql("""select ui.insid, i.insid \
    from \
        instrument ui,
        instrument i
    where \
        ui.insaddr = i.und_insaddr and \
        ui.instype = 1""")[1]

instr_dict = {}
instr_list = []

for i in instr[0]:
    if i[0] in instr_dict:
        instr_dict[i[0]].append(i[1])
    else:
        instr_dict[i[0]] = [i[1]]

instr_list = list(instr_dict.keys())
instr_list.sort()


cvAction = ['Test Mode', 'Set Physical Contract Size', 'Set All']


ael_variables = FBDPGui.LogVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ('und_ins',
                'Underlying Instrument',
                'string', instr_list, '',
                1),
        ('deriv',
                 'Derivative Filter',
                 'string', ['.*', '.*X$', '.*Y$', '.*[0-9]$'], '.*',
                 1),
        ('contrsize',
                'Physical Contract Size',
                'string', [], '',
                0),
        ('action',
                'Action',
                'string', cvAction, 'Test Mode',
                1))


def ael_main(param):
    LogMode = param['Logmode']
    LogToConsole = param['LogToConsole']
    LogToFile = param['LogToFile']
    Logfile = dict.get('Logfile')
    SendReportByMail = param['SendReportByMail']
    MailList = param['MailList']
    ReportMessageType = param['ReportMessageType']

    CreateLog(ScriptName,
                      LogMode,
                      LogToConsole,
                      LogToFile,
                      Logfile,
                      SendReportByMail,
                      MailList,
                      ReportMessageType)
    Logme()(None, 'START')

    if param['action'] == 'Test Mode':
        if param['deriv'] == None or param['und_ins'] == None:
            Logme()('Underlying Instrument and Derivative must be set',
                    'ERROR')
        else:
            Logme()('========================================')
            Logme()('Underlying Instrument: %s \
            PhysContrSize ContrSize' % (param['und_ins']))
            Logme()('========================================')
            for i in instr_dict[param['und_ins']]:
                try:
                    if re.search(param['deriv'], i):
                        n = ael.InstrumentAlias.read("alias = '%s' and "
                                "type.alias_type_name='EUREX'" %
                                i).insaddr.phys_contr_size
                        c = ael.InstrumentAlias.read("alias = '%s' and "
                                "type.alias_type_name='EUREX'" %
                                i).insaddr.contr_size
                        Logme()('%s%-20s %5.2f %5.2f' % ("    ", i, n, c))
                except:
                    if re.search(param['deriv'], i):
                        n = ael.Instrument[i].phys_contr_size
                        c = ael.Instrument[i].contr_size
                        Logme()('%s%-20s %5.2f %5.2f' % ("    ", i, n, c))

    elif param['action'] == 'Set Physical Contract Size':
        if (param['deriv'] == None or param['und_ins'] == None or
                param['contrsize'] == None):
            Logme()('Underlying Instrument, Derivative and Physical Contract '
                    'Size must be set', 'WARNING')
        else:
            for i in instr_dict[param['und_ins']]:
                if re.search(param['deriv'], i):
                    if not ael.Instrument[i]:
                        Logme()('Instrument %s not found' % i, 'WARNING')
                        continue
                    ic = ael.Instrument[i].clone()
                    ic.phys_contr_size = float(param['contrsize'])
                    ic.commit()
                    Logme()('Instrument: %s Updated, phys_contr_size=%.2f' %
                            (i, float(param['contrsize'])))
            Logme()('Update Completed.')
    elif param['action'] == 'Set All':
        und_list = []
        for i in list(instr_dict.keys()):
            for d in instr_dict[i]:
                for cad in list(corp_act_dict.keys()):
                    if re.search(cad, d):
                        und_list.append(i)
                        break
                break
        for u in und_list:
            for d in instr_dict[u]:
                for cad in list(corp_act_dict.keys()):
                    if re.search(cad, d):
                        ins = ael.InstrumentAlias.read("alias= '%s' and "
                                "type.alias_type_name='EUREX'" % (d)).insaddr
                        if ins.phys_contr_size == corp_act_dict[cad]:
                            Logme()('Instrument: %s. Phys contr size already '
                                    'set to %.2f' % (ins.insid,
                                    float(corp_act_dict[cad])))
                            break
                        ic = ins.clone()
                        ic.phys_contr_size = float(corp_act_dict[cad])
                        ic.commit()
                        Logme()('Instrument: %s Updated, phys_contr_size='
                                '%.2f' % (d, float(corp_act_dict[cad])))
                        break
        Logme()('Update Completed')

    Logme()(None, 'FINISH')
