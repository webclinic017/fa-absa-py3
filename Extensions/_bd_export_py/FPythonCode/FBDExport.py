""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/BDExport/./etc/FBDExport.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FBDExport

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import collections
import acm
import base64
import FRunScriptBase
import FExportBase
import FRunScriptGUI
import FUxCore
import tempfile
import datetime
import os
import FExportBaseConfiguration
import FExportUtils
import FLogger
import FCustomExportSetupDialog
logger = FLogger.FLogger.GetLogger("BD Export")
log_level = ['1. Information', '2. Debug', '3. Warnings', '4. Errors']
class SaveDialog():

    def __init__(self):
        pass

    def CSaveDialog(self, shell, params):
        file_path = ''
        if len(params['selected']):
            file_path = params['selected'][0]
        resultDic = acm.FDictionary()
        ff = acm.FFileSelection()
        ff.PickExistingFile(False)
        ff.PickDirectory(True)
        ff.SelectedDirectory = file_path
        selections = acm.UX().Dialogs().BrowseForFile(shell, ff)
        file_path = ff.SelectedDirectory()
        resultDic.AtPut('result', [ff.SelectedDirectory()])
        return resultDic


class HFDialog():

    def CustomDialog(self, shell, params):
        customDlg = Headerfooter(shell, params)
        return acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)

class Headerfooter(FUxCore.LayoutDialog):
    def __init__(self, shell, params):
        self.shell = shell
        self.caption = 'Header\Footer'
        self.params = params
        self.m_fuxDlg = None
        self.m_numEdit1 = None
        self.m_numEdit2 = None

    def HandleApply(self):
        resultDic = acm.FDictionary()
        header = self.m_numEdit1.GetData()
        footer = self.m_numEdit2.GetData()
        header = header.replace(',', '\comma')
        footer = footer.replace(',', '\comma')
        sp = 'Header=' + header + '|Footer=' + footer
        resultDic['result'] = [sp]
        return resultDic

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_numEdit1 = layout.GetControl('edit1')
        self.m_numEdit2 = layout.GetControl('edit2')
        self.m_numEdit1.ToolTip('Header information with predefined variables %DATE_TIME% %EXPORT_DATE%, %EXPORT_TIME%, %SHEET_TEMPLATE%, %NTRADES%, %RECIPIENTS%')
        self.m_numEdit2.ToolTip('Footer information with predefined variables %DATE_TIME% %EXPORT_DATE%, %EXPORT_TIME%, %SHEET_TEMPLATE%, %NTRADES%, %RECIPIENTS%')
        strlist = str(self.params['selected'][0]).split('|Footer=')
        header = strlist[0].split('Header=')[1]
        footer = strlist[1]
        header = header.replace('\comma', ',')
        footer = footer.replace('\comma', ',')
        self.m_numEdit1.InsertTextAtCursor(header)
        self.m_numEdit2.InsertTextAtCursor(footer)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b.AddLabel('label1', 'Header', -1, -1)
        b.AddText('edit1', 320, 120, -1, -1) 
        b.AddLabel('label2', 'Footer', -1, -1)
        b.AddText('edit2', 320, 120, -1, -1)
        b.  AddCustom('Application', 'Party Definition', 640, 480)
        b.  EndBox()
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b


class addinfoDialog():

    def CustomDialog(self, shell, params):
        customDlg = FCustomExportSetupDialog.FCustomExportSetupDialog(shell, params)
        acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)
        return customDlg.return_dictionary

class EMail():

    def CustomDialog(self, shell, params):
        customDlg = E_Mail(shell, params)
        return acm.UX().Dialogs().ShowCustomDialogModal(shell, customDlg.CreateLayout(), customDlg)

class E_Mail(FUxCore.LayoutDialog):
    def __init__(self, shell, params):
        self.shell = shell
        self.params = params
        self.caption = 'E-Mail'
        self.m_fuxDlg = None
        self.m_numEdit1 = None
        self.m_numEdit2 = None
        self.m_numEdit3 = None
        self.m_numEdit4 = None

    def HandleApply(self):
        resultDic = acm.FDictionary()
        sender = self.m_numEdit1.GetData()
        recipient = self.m_numEdit2.GetData()
        subject = self.m_numEdit3.GetData()
        body = self.m_numEdit4.GetData()
        body = "\n".join(body.splitlines())
        body = body.replace(',', '\comma')
        sender = sender.replace(',', '\comma')
        recipient = recipient.replace(',', '\comma')
        subject = subject.replace(',', '\comma')
        sp = 'Sender=' + sender + '|Recipient=' + recipient + '|Subject=' + subject + '|Body=' + body
        resultDic.AtPut('result', [sp])
        return resultDic

    def HandleCreate(self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.caption)
        self.m_numEdit1 = layout.GetControl('Sender')
        self.m_numEdit2 = layout.GetControl('Recipient')
        self.m_numEdit3 = layout.GetControl('Subject')
        self.m_numEdit4 = layout.GetControl('Body')
        self.m_numEdit1.ToolTip('Sender email')
        self.m_numEdit2.ToolTip('Recipient email')
        self.m_numEdit3.ToolTip('Subject text')
        self.m_numEdit4.ToolTip('Body text')
        strlist = str(self.params['selected'][0]).split('|Body=')
        body = strlist[1]
        subject = strlist[0].split('|Subject=')[1]
        recipient = strlist[0].split('|Subject=')[0].split('|Recipient=')[1]
        sender = strlist[0].split('|Subject=')[0].split('|Recipient=')[0].split('Sender=')[1]
        body = body.replace('\comma', ',')
        sender = sender.replace('\comma', ',')
        recipient = recipient.replace('\comma', ',')
        subject = subject.replace('\comma', ',')
        self.m_numEdit1.SetData(sender)
        self.m_numEdit2.SetData(recipient)
        self.m_numEdit3.SetData(subject)
        self.m_numEdit4.SetData(body)

    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b. BeginHorzBox()
        b. AddSpace(3)
        b.  BeginVertBox()
        b. AddInput('Sender', 'Sender', 15, -1, -1, 'Default', False)
        b. AddInput('Recipient', 'Recipient', 15, -1, -1, 'Default', False)
        b. AddInput('Subject', 'Subject', 15, -1, -1, 'Default', False)
        b.  AddLabel('Body_label', 'Body', 240, -1)
        b.  AddText('Body', 320, 120, -1, -1)
        b.  EndBox()
        b. EndBox()
        b. AddSpace(5)
        b. BeginHorzBox()
        b.   AddFill()
        b.   AddButton('ok', 'OK')
        b.   AddButton('cancel', 'Cancel')
        b. AddSpace(3)
        b. EndBox()
        b.EndBox()
        return b

def emailVariables():
    return {'%FILENAME%': 'FileName', '%SHEET_TEMPLATE%': 'tradingSheetTemplateName', '%RECIPIENTS%': 'EmailRecipient', '%TRADE_QUERY%': 'tradeQuery', '%STATE_CHART%': 'stateChartName'}

def encrypt_password(password):
    if not password.startswith('0Ox'):
        encrypted_pwd = base64.b64encode(password)
        encrypted_pwd = "0Ox" + encrypted_pwd
        return encrypted_pwd
    return password

def parse_password(password):
    pos = password.find('* ')
    password = password[pos+1:]
    password = password.replace(' '*500, '')
    return password

class ExportAelVariables(FRunScriptBase.AelVariablesExport):

    def _AddSaveDialogVariable(self):
        tt = "Select file to export trades."
        saveDlg = SaveDialog()
        var = ['FilePath', 'File Path_File settings', 'string', None, None, 0, 0, tt, None, 1, saveDlg.CSaveDialog]
        self.ael_variables.append(var)

    def __init__(self):
        FRunScriptBase.AelVariablesExport.__init__(self)
        self._AddCustommodule()
        self._AddTradesExportCheckBox()
        self._AddTradeQueryDialogVariable()
        self._Addheaderfooter()
        self._AddXSLVariables()
        self._AddSaveDialogVariable()
        self._AddFileSettingVariables()
        self._AddStateChartVariable()
        self._AddSheetTemplateVariable()
        self._AddUpdateExportStateOnlyAdvancedVariable()
        self._AddAlwaysGenerateFileVariable()
        self._AddPostTransformationVariable()
        self._AddParties()
        self._AddFTPSettingVariables()
        self._AddFTPDialogVariable()
        self._AddSFTPSettingVariables()
        self._AddSFTPDialogVariable()
        self._AddEMailSettingVariables()
        self._AddSMTPDialogVariable()
        self._AddSMTP()
        self._AddInstrumentVariables()
        self._AddEnviromentcheck()
        self._Installaddinfo()
        self._Logging()
        self._AddLogVariable()
        self._AddTransHist()
    
    def _AddLogVariable(self):
        pass

    def _Logging(self):
        ttLogMode = 'Select the verbosity of logging output by the export task.'
        vars = [['LogLevel', 'Logging Level_Logging', 'string', log_level, '1. Information', 2, 0, ttLogMode],
                ['logtoconsole', 'Log to Console_Logging', 'string', [True, False], 1, 0, 0, '', None, 1],
                ['logtofile', 'Log to File_Logging', 'string', [True, False], 0, 0, 0, '', self.enableLogtoFile, 1],
                ['logFileName', 'Log File Path_Logging', 'string', None, 'c:\\temp\\logfile.log', False, False, '', '', 0]]
        self.ael_variables.extend(vars)
        
    def _AddTradesExportCheckBox(self):
        ttIESettings = 'Enable trades export...'
        var = ['TradeExport', 'Export Trades', 'string', [True, False], 1, 1, 0, ttIESettings, self._SetEnabled]
        self.ael_variables.append(var)

    def _Installaddinfo(self):
        customDlg = addinfoDialog()
        tt = 'Click button to add instrument alias'
        var = ['Installation', 'Custom Export Setup', 'string', [], 'Custom=|State Chart=', 0, 1, tt, self.customexportCB, 1, customDlg.CustomDialog]
        self.ael_variables.append(var)
    
    def _AddSMTP(self):
        customDlg = EMail()
        ttHF = 'E-Mail'
        var = ['EmailSender', 'Sender_hidden', 'string', None, 'noreply.export@frontarena.com', 0, 0, None, None, 0]
        self.ael_variables.append(var)
        var = ['EmailRecipient', 'Recipient_hidden', 'string', None, None, 0, 0, None, None, 0]
        self.ael_variables.append(var)
        var = ['EmailSubject', 'Subject_hidden', 'string', None, 'Exported file %FILENAME%', 0, 0, None, None, 0]
        self.ael_variables.append(var)
        var = ['EmailBody', 'Body_hidden', 'string', None, None, 0, 0, None, None, 0]
        self.ael_variables.append(var)
        var = ['Email_parameter', 'E-Mail_Transport Settings', 'string', [], 'Sender=noreply.export@frontarena.com|Recipient=|Subject=Exported file %FILENAME%|Body=', 0, 1, ttHF, self.emailCB, 1, customDlg.CustomDialog]
        self.ael_variables.append(var)

    def _AddEnviromentcheck(self):
        ttEnviromentcheck = "Enable Enviroment Setup Check"
        vars = [['Enviromentsetupcheck', 'Environment Setup Check_Advanced', 'string', [True, False], 0, 0, 0, ttEnviromentcheck, None, 1]]
        self.ael_variables.extend(vars)
    
    def _AddTransHist(self):
        ttTransHist = "Using Transaction History"
        vars = [['UsTransHist', 'Use Transaction History_Advanced', 'string', [True, False], 1, 0, 0, ttTransHist, None, 1]]
        self.ael_variables.extend(vars)

    def _Addheaderfooter(self):
        customDlg = HFDialog()
        var = ['header', 'Header_hidden', 'string', None, None, 0, 0, None, None, 1]
        self.ael_variables.append(var)
        var = ['footer', 'Footer_hidden', 'string', None, None, 0, 0, None, None, 1]
        self.ael_variables.append(var)
        ttHF = 'Header/Footer information with predefined variables %DATE_TIME%, %EXPORT_DATE%, %EXPORT_TIME%, %SHEET_TEMPLATE%, %NTRADES%, %RECIPIENTS%'
        var = ['HF', 'Header/Footer_File settings', 'string', [], 'Header=|Footer=', 0, 1, ttHF, self.header_footerCB, 1, customDlg.CustomDialog]
        self.ael_variables.append(var)

    def _AddFTPDialogVariable(self):
        #['FTPUserName', 'FTP Username', 'string', None, 'FTPUser', 0, 0, ttFTPUserName, None, 0]
        var = ['FTP', 'FTP Password_Transport settings',  'string', None, None, 0, 1, '', self.ftpPasswordCB, 1]
        self.ael_variables.append(var)

    def _AddSFTPDialogVariable(self):
        var = ['SFTP', 'SFTP Password_Transport settings', 'string', None, None, 0, 1, '', self.sftpPasswordCB, 1]
        self.ael_variables.append(var)

    def _AddSMTPDialogVariable(self):
        var = ['EmailPassword', 'SMTP Password_Transport settings', 'string', None, None, 0, 1, '', self.smtpPasswordCB, 1]
        self.ael_variables.append(var)
        
    def header_footerCB(self, index, fieldArray):
        strlist = str(fieldArray[index]).split('|Footer=')
        header = strlist[0].split('Header=')[1]
        footer = strlist[1]
        if str(fieldArray[index])[-1] == '"':
            footer = strlist[1][0:-1]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'header']
        el = el[0]
        fieldArray[el] = header
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'footer']
        el = el[0]
        fieldArray[el] = footer
        return fieldArray
        
    def ChangeContactInf(self, index, fieldArray):
        dictionary = self.Load_party(fieldArray[index], fieldArray)
        keys = dictionary.keys()
        for i in range(len(fieldArray)):
            if self.ael_variables[i][0] == 'Email_parameter':
                value = fieldArray[i].split('|Recipient')
                first_part = value[0]
                second_part = value[1].split('|Subject')[1]
                fieldArray[i] = first_part + '|Recipient=' + dictionary[self.ael_variables[i][0]] + '|Subject' + second_part
            elif self.ael_variables[i][0] in keys:
                fieldArray[i] = dictionary[self.ael_variables[i][0]]
            elif self.ael_variables[i][0] == 'defpartiesopen':
                fieldArray[i] = fieldArray[index]
        return fieldArray
    
    def _None_to_string(self, str):
        return '' if str == None else str
    
    def Load_party(self, name, fieldArray):
        party = acm.FParty[name]
        contact_dict = {'FTPPasswordSecret' : '', 'EmailPassword' : '', 'Email_parameter' : '', 'FTP' : '', 'SMTPasswordSecret' : '','EmailUserName' : '', 'EmailPort' : '', 'EmailHostName' : '', 'FTPHostName' : '', 'FTPPortNumber' : '', 'FTPPath' : '', 'FTPUserName' : '', 'SFTPHostName' : '', 'SFTPPath': '', 'SFTPUserName': '', 'SFTPPasswordSecret' :'', 'SFTPPortNumber' : '', 'SFTP' : ''}
        keys = contact_dict.keys()
        if party <> None:
            for contact in party.Contacts():
                contact_dict['EmailUserName'] = contact.AdditionalInfo().SMTP_User_Name()
                contact_dict['EmailPort'] = contact.AdditionalInfo().SMTP_Port()
                contact_dict['EmailHostName'] = contact.AdditionalInfo().SMTP_Server()
                contact_dict['FTPHostName'] = contact.AdditionalInfo().FTP_Hostname()
                contact_dict['FTPPortNumber'] = contact.AdditionalInfo().FTP_Port()
                contact_dict['FTPPath'] = contact.AdditionalInfo().FTP_Path()
                contact_dict['FTPUserName'] = contact.AdditionalInfo().FTP_Username()
                contact_dict['SFTPHostName'] = contact.AdditionalInfo().SFTP_Host_Name()
                contact_dict['SFTPPath'] = contact.AdditionalInfo().SFTP_Path()
                contact_dict['SFTPPortNumber'] = contact.AdditionalInfo().SFTP_Port()
                contact_dict['SFTPUserName'] = contact.AdditionalInfo().SFTP_UserName()
                contact_dict['FTP'] = len(self._None_to_string(contact.AdditionalInfo().FTP_Password()))*'*'
                contact_dict['SFTP'] = len(self._None_to_string(contact.AdditionalInfo().SFTP_Password()))*'*'
                contact_dict['EmailPassword'] = len(self._None_to_string(contact.AdditionalInfo().SMTP_Password()))*'*'
                contact_dict['FTPPasswordSecret'] = encrypt_password(self._None_to_string(contact.AdditionalInfo().FTP_Password()))
                contact_dict['SFTPPasswordSecret'] = encrypt_password(self._None_to_string(contact.AdditionalInfo().SFTP_Password()))
                contact_dict['SMTPasswordSecret'] = encrypt_password(self._None_to_string(contact.AdditionalInfo().SMTP_Password()))
                contact_dict['Email_parameter'] = contact.Email()
        return contact_dict

    def emailCB(self, index, fieldArray):
        strlist = str(fieldArray[index]).split('|Body=')
        body = strlist[1]
        subject = strlist[0].split('|Subject=')[1]
        recipient = strlist[0].split('|Subject=')[0].split('|Recipient=')[1]
        sender = strlist[0].split('|Subject=')[0].split('|Recipient=')[0].split('Sender=')[1]
        if str(fieldArray[index])[0] == '"':
            body = body[0:-1]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'EmailSender']
        el = el[0]
        fieldArray[el] = sender
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'EmailRecipient']
        el = el[0]
        fieldArray[el] = recipient
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'EmailSubject']
        el = el[0]
        fieldArray[el] = subject
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'EmailBody']
        el = el[0]
        fieldArray[el] = body
        return fieldArray

    def enableLogtoFile(self, index, fieldArray):
        nameIndex = FRunScriptGUI.Controls.NAME
        fieldPrefix = "logFileName"
        enableIndex = FRunScriptGUI.Controls.ENABLED
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex].startswith(fieldPrefix):
                self.ael_variables[i][enableIndex] = fieldArray[index]
        return fieldArray

    def custommCB(self, index, fieldArray):
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'stateChartName']
        el = el[0]
        chart_name = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Custommodule']
        el = el[0]
        custom_module = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'tradingSheetTemplateName']
        el = el[0]
        trSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_iSheetTemplateName']
        el = el[0]
        insSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_istateChartName']
        el = el[0]
        insStateChart = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Installation']
        el = el[0]
        fieldArray[el] = 'Custom=' + custom_module + '|State Chart=' + chart_name + '|TradeSheet=' + trSheetTName + '|InsSheet=' + insSheetTName + '|insStateChart=' + insStateChart
        return fieldArray
    
    def ftpPasswordCB(self, index, fieldArray):
        ''' If additional fields are added, remember that the index below may change '''
        password = fieldArray[index]  
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'FTPPasswordSecret']
        el = el[0]
        if password and len(password) > 0:
            if password.count('*') != len(password):
                fieldArray[index] = len(password)*'*'
                fieldArray[el] = encrypt_password(password)
        return fieldArray
        
    def sftpPasswordCB(self, index, fieldArray):
    
        ''' If additional fields are added, remember that the index below may change '''
        password = fieldArray[index]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'SFTPPasswordSecret']
        el = el[0]
        if password and len(password) > 0:
            if password.count('*') != len(password):
                fieldArray[index] = len(password)*'*'
                fieldArray[el] = encrypt_password(password)
        return fieldArray

    def smtpPasswordCB(self, index, fieldArray):
        ''' If additional fields are added, remember that the index below may change '''
        password = fieldArray[index]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'SMTPasswordSecret']
        el = el[0]
        if password and len(password) > 0:
            if password.count('*') != len(password):
                fieldArray[index] = len(password)*'*'
                fieldArray[36] = encrypt_password(password)
        return fieldArray
        
    def StateChart_t(self, index, fieldArray):
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'stateChartName']
        el = el[0]
        chart_name = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Custommodule']
        el = el[0]
        custom_module = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'tradingSheetTemplateName']
        el = el[0]
        trSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_iSheetTemplateName']
        el = el[0]
        insSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_istateChartName']
        el = el[0]
        insStateChart = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Installation']
        el = el[0]
        fieldArray[el] = 'Custom=' + custom_module + '|State Chart=' + chart_name + '|TradeSheet=' + trSheetTName + '|InsSheet=' + insSheetTName + '|insStateChart=' + insStateChart
        return fieldArray
        
    def StateChart_i(self, index, fieldArray):
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'stateChartName']
        el = el[0]
        chart_name = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Custommodule']
        el = el[0]
        custom_module = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'tradingSheetTemplateName']
        el = el[0]
        trSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_iSheetTemplateName']
        el = el[0]
        insSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_istateChartName']
        el = el[0]
        insStateChart = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Installation']
        el = el[0]
        fieldArray[el] = 'Custom=' + custom_module + '|State Chart=' + chart_name + '|TradeSheet=' + trSheetTName + '|InsSheet=' + insSheetTName + '|insStateChart=' + insStateChart
        
        return fieldArray
        
    def sheetCB(self, index, fieldArray):
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'stateChartName']
        el = el[0]
        chart_name = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Custommodule']
        el = el[0]
        custom_module = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'tradingSheetTemplateName']
        el = el[0]
        trSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_iSheetTemplateName']
        el = el[0]
        insSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_istateChartName']
        el = el[0]
        insStateChart = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Installation']
        return fieldArray
        
    def isheetCB(self, index, fieldArray):
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'stateChartName']
        el = el[0]
        chart_name = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Custommodule']
        el = el[0]
        custom_module = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'tradingSheetTemplateName']
        el = el[0]
        trSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_iSheetTemplateName']
        el = el[0]
        insSheetTName = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_istateChartName']
        el = el[0]
        insStateChart = fieldArray[el]
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Installation']
        el = el[0]
        fieldArray[el] = 'Custom=' + custom_module + '|State Chart=' + chart_name + '|TradeSheet=' + trSheetTName + '|InsSheet=' + insSheetTName + '|insStateChart=' + insStateChart
        return fieldArray
        
    def customexportCB(self, index, fieldArray):
        acm.PollAllDbEvents()
        params_dict = self.parse_params(fieldArray[index])
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'stateChartName']
        el = el[0]
        ael_variables[el][3] = self.getStateCharts()
        if params_dict['State Chart'] != '':
            fieldArray[el] = params_dict['State Chart']
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'tradingSheetTemplateName']
        el = el[0]
        ael_variables[el][3] = self.getTradingSheetTemplates()
        if params_dict['TradeSheet'] != '':
            fieldArray[el] = params_dict['TradeSheet']
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_iSheetTemplateName']
        el = el[0]
        ael_variables[el][3] = self.getInstrumentSheetTemplates()
        if params_dict['InsSheet'] != '':
            fieldArray[el] = params_dict['InsSheet']
        el = [i for i in range(len(fieldArray)) if self.ael_variables[i][0] == 'Instrument_istateChartName']
        el = el[0]
        ael_variables[el][3] = self.getStateCharts()
        if params_dict['insStateChart'] != '':
            fieldArray[el] = params_dict['insStateChart']
        return fieldArray
    
    def enable_date_at_beginning_cb(self, index, fieldArray):
        if fieldArray[index]:
            self.ael_variables[index+1][FRunScriptGUI.Controls.ENABLED] = True
        else:
            self.ael_variables[index+1][FRunScriptGUI.Controls.ENABLED] = False
        return fieldArray
        
    def _AddPostTransformationVariable(self):
        ttPostTransformation = 'Select function for post-transformation of file: ModuleName.FunctionName'
        var = ['postTransformationFunction', 'Post-transformation function', 'string', None, '', False, False, ttPostTransformation, None, True]
        self.ael_variables.append(var)   

    def _AddTradeQueryDialogVariable(self):
        ttTradeQuery = 'Select a trade query.'
        var = ['tradeQuery', 'Trade Query', 'string', self.getTradeQueries(), None, 0, 0, ttTradeQuery, None, None]
        self.ael_variables.append(var)        

    def _AddStateChartVariable(self):
        ttStateCharts = 'Select an existing State Chart from the list or create a new one by entering a name.'
        var = ['stateChartName', 'Trade State Chart', 'string', self.getStateCharts(), None, 0, 0, ttStateCharts, self.StateChart_t, None]
        self.ael_variables.append(var)
        
    def _AddParties(self):
        ttParty = 'Select contact from party.'
        vars = ['useparties', 'Define from Party_Transport settings', 'string', [True, False], 0, 1, 0, ttParty, self._SetEnabled]
        self.ael_variables.append(vars)
        var = ['defparties', 'Select Party_Transport settings', 'string', self.getParties(), None, 0, 0, 'Chose party', self.ChangeContactInf, 1]
        self.ael_variables.append(var)

    def _AddSheetTemplateVariable(self):
        ttTradingSheetTemplate = 'Choose a trading sheet template.'
        var = ['tradingSheetTemplateName', 'Trading Sheet Template', 'string', self.getTradingSheetTemplates(), None, 0, 0, ttTradingSheetTemplate, self.sheetCB, None]
        self.ael_variables.append(var)

    def _AddXSLVariables(self):
        ttXMLTemplate = 'Choose which XSL template to use in the transformation from XML. Templates must be added to group aef reporting/print templates to be visible here.'
        var = ['xsltTemplateName', 'XSL Template_File settings', 'string', self.getPrintTemplateNames(), 'FCSVTemplate', 2, 0, ttXMLTemplate]
        self.ael_variables.append(var)

    def _AddTestModeVariable(self):
        ttTestMode = 'If untoggled, the business process will not be moved to "Sent" after export.'
        var = ['UpdateBusinessProcesses', 'Mark trades as sent_Advanced', 'bool', [True, False], True, False, False, ttTestMode, None]
        self.ael_variables.append(var)

    def _AddFTPSettingVariables(self):
        tabName = 'Transport Settings'
        ttFTPSettings = "Use FTP to exported the file"
        ttFTPHostName = 'The path where the file will be saved'
        ttFTPPortNumber = 'The path where the file will be saved'
        ttFTPDirectory = 'The remote FTP directory'
        ttFTPUserName = 'The FTP login user name'
        ttFTPPassword = 'The FTP login password'
        vars = [['EnableFTP', 'Send with FTP_' + tabName, 'string', [True, False], 0, 0, 0, ttFTPSettings, self._SetEnabled],
                ['FTPHostName', 'FTP Host Name_' + tabName, 'string', None, 'internal.sungard.corp', 0, 0, ttFTPHostName, None, 0],
                ['FTPPortNumber', 'FTP Port_' + tabName, 'int', None, 22, 0, 0, ttFTPPortNumber, None, 0],
                ['FTPPath', 'FTP Path_' + tabName, 'string', None, 'incoming/trades', 0, 0, ttFTPDirectory, None, 0],
                ['FTPUserName', 'FTP Username_' + tabName, 'string', None, 'FTPUser', 0, 0, ttFTPUserName, None, 0],
                ['FTPPasswordSecret', 'FTP PasswordSecret_hidden', 'string', None, None, 0, 0, ttFTPPassword, None, 0]]        
        self.ael_variables.extend(vars)

    def _AddSFTPSettingVariables(self):
        tabName = 'Transport Settings'              
        ttSFTPSettings = "Use SMTP to exported the file"
        ttSFTPPHostName = 'The path where the file will be saved'
        ttSFTPPortNumber = 'The path where the file will be saved'
        ttSFTPDirectory = 'The remote SMTP directory'
        ttSFTPUserName = 'The SFTP login user name'
        ttSFTPPassword = 'The SFTP login password'  
        vars = [['EnableSFTP', 'Send with SFTP_' + tabName, 'string', [True, False], 0, 0, 0, ttSFTPSettings, self._SetEnabled],
                ['SFTPHostName', 'SFTP Host Name_' + tabName, 'string', None, 'internal.sungard.corp', 0, 0, ttSFTPPHostName, None, 0],
                ['SFTPPortNumber', 'SFTP Port_' + tabName, 'int', None, 22, 0, 0, ttSFTPPortNumber, None, 0],
                ['SFTPPath', 'SFTP Path_' + tabName, 'string', None, 'incoming/trades', 0, 0, ttSFTPDirectory, None, 0],
                ['SFTPUserName', 'SFTP Username_' + tabName, 'string', None, 'SFTPUser', 0, 0, ttSFTPUserName, None, 0],
                ['SFTPPasswordSecret', 'SFTP PasswordSecret_hidden', 'string', None, None, 0, 0, ttSFTPPassword, None, 0]]
        self.ael_variables.extend(vars)

    def _AddEMailSettingVariables(self):
        tabName = 'Transport Settings'
        variables = emailVariables()
        ttEmail = "Send an email notification with the exported trades."
        ttSMTPServer = 'Use SMTP to exported the file'
        ttSMTPPort = 'SMTP Port'
        ttRecipient = 'The recipients of the email notification'
        ttSender = 'The sender field used in email notifications.'
        ttVariables = 'The following variables may be used: ' + ', '.join(variables)
        ttSubject = 'The subject used in email notifications. ' + ttVariables
        ttBody = 'The body/message used in email notifications. ' + ttVariables
        vars = [['EnableEmail', 'Send with Email_' + tabName, 'string', [True, False], 0, 0, 0, ttEmail, self._SetEnabled],
                ['EmailHostName', 'SMTP Server_' + tabName, 'string', None, None, 0, 0, ttSMTPServer, None, 1],
                ['EmailPort', 'SMTP Port_' + tabName, 'string', None, '25', 0, 0, ttSMTPPort, None, 1],
                ['EmailUserName', 'SMTP User Name_' + tabName, 'string', None, None, 0, 0, '', None, 1],
                ['SMTPasswordSecret', 'SMTP PasswordSecret_hidden', 'string', None, None, 0, 0, None, None, 0]]
        self.ael_variables.extend(vars)

    def _AddInstrumentVariables(self):
        ttInstrumentQuery='Get insttrument query'
        ttInstrumentSheetTemplate = 'Choose a instrument sheet template.'
        ttStateCharts = 'Select an existing State Chart from the list or create a new one by entering a name.'
        ttPostTransformation = 'Select function for post-transformation of file: ModuleName.FunctionName'
        ttIESettings = "Enable Export Instruments"
        ttQueryIntersection = "Inst. and Trade Query Intersectio"
        vars = [['InstrumentExport', 'Export Instrument', 'string', [True, False], 0, 1, 0, ttIESettings, self._SetEnabled],
                ['QueryIntersection', 'Inst. and Trade Query Intersection', 'string', [True, False], 1, 0, 0, ttQueryIntersection, None, 1],
                ['Instrument_iQuery', 'Instrument Query', 'string', self.getInstrumentQueries(), None, 0, 0, ttInstrumentQuery, None, 1],
                ['Instrument_istateChartName', 'Instrument State Chart', 'string', self.getStateCharts(), None, 0, 0, ttStateCharts, self.StateChart_i, 1],
                ['Instrument_iSheetTemplateName', 'Pricing Sheet Template', 'string', self.getInstrumentSheetTemplates(), None, 0, 0, ttInstrumentSheetTemplate, self.isheetCB, 1]]
        self.ael_variables.extend(vars)

    def _AddFileSettingVariables(self):
        ttFilePath = 'The path where the file will be saved' 
        var = ['FilePath', 'File path_File Settings', 'string', None, 'C:\\', False, False, ttFilePath, None, True]      
        variables = ('%DATE_TIME%', '%DATE_TIME%', '%EXPORT_DATE%', '%EXPORT_TIME%')
        ttFilename = 'The following variables may be used for the filename: ' + ', '.join(variables)
        var = ['FileName', 'Trade Filename_File Settings', 'string', None, 'file_trade.csv', False, False, ttFilename, 
                None, True]
        self.ael_variables.append(var)
        var = ['Instrument_iFileName', 'Instrument Filename_File Settings', 'string', None, 'file_instrument.csv', False, False, ttFilename, 
                None, True]
        self.ael_variables.append(var)
        date_format_description = "Select one of the default datetime formats, or define a new one. For a complete list of formatting directives, please see documentation."
        var = ['DateFormat', 'Format of Date Added to File Name_File Settings', 'string', self.get_default_date_formats(), '', False, False, date_format_description, self.enable_date_at_beginning_cb, True]
        self.ael_variables.append(var)
        var = ['DateAtBeginning', 'Date at Beginning of File Name_File Settings', 'string', [True, False], '', False, False, 'Add date at the beginning of file name.', None, True]
        self.ael_variables.append(var)

    def _SetEnabled(self, index, fieldValues):
        nameIndex = FRunScriptGUI.Controls.NAME
        enableIndex = FRunScriptGUI.Controls.ENABLED
        fieldPrefix = ""
        enabled = fieldValues[index]
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex] == 'EnableFTP':
                EnableFTP = fieldValues[i]
            if self.ael_variables[i][nameIndex] == 'EnableSFTP':
                EnableSFTP = fieldValues[i]
            if self.ael_variables[i][nameIndex] == 'EnableEmail':
                EnableEmail = fieldValues[i]
            if self.ael_variables[i][nameIndex] == 'TradeExport':
                EnableTradeExport = fieldValues[i]
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex] == 'useparties':
                enableparty = fieldValues[i]
        for i in range(len(self.ael_variables)):
            if enableparty == 'true':
                if self.ael_variables[i][nameIndex].startswith('FTP') or self.ael_variables[i][nameIndex].startswith('SFTP'):
                    self.ael_variables[i][enableIndex] = 'false' 
                if self.ael_variables[i][nameIndex].startswith('Email') and not self.ael_variables[i][nameIndex].startswith('Email_parameter'):
                    self.ael_variables[i][enableIndex] = 'false' 
            elif self.ael_variables[i][nameIndex].startswith('FTP') and EnableFTP == 'true':
                self.ael_variables[i][enableIndex] = 'true'
            elif self.ael_variables[i][nameIndex].startswith('SFTP') and EnableSFTP == 'true':
                self.ael_variables[i][enableIndex] = 'true'
            elif self.ael_variables[i][nameIndex].startswith('Email') and EnableEmail == 'true':
                self.ael_variables[i][enableIndex] = 'true'
                self.ael_variables[i][enableIndex] = 'true'
        if self.ael_variables[index][nameIndex] == 'InstrumentExport':
            fieldPrefix = 'Instrument_i'
        elif self.ael_variables[index][nameIndex] == 'EnableFTP' and enableparty == 'false':
            fieldPrefix = 'FTP'
        elif self.ael_variables[index][nameIndex] == 'EnableSFTP' and enableparty == 'false':
            fieldPrefix = 'SFTP'
        elif self.ael_variables[index][nameIndex] == 'EnableEmail' and enableparty == 'false':
            fieldPrefix = 'Email'
        elif self.ael_variables[index][nameIndex] == 'EnableEmail' and enableparty == 'true':
            fieldPrefix = 'Email_parameter' 
        elif self.ael_variables[index][nameIndex] == 'useparties':
            fieldPrefix = 'defparties'
        elif self.ael_variables[index][nameIndex] == 'TradeExport':
            _object_names = ['FileName', 'stateChartName', 'tradingSheetTemplateName', 'tradeQuery', 'postTransformationFunction']
            _object_mandatory = ['stateChartName', 'tradingSheetTemplateName']
            for i in range(len(self.ael_variables)):
                if self.ael_variables[i][nameIndex] in _object_names:
                    self.ael_variables[i][enableIndex] = enabled
                if self.ael_variables[i][nameIndex] in _object_mandatory:
                    self.ael_variables[i][FRunScriptGUI.Controls.MANDATORY] = 1 if enabled == 'true' else 0
                if self.ael_variables[i][nameIndex]  in ['tradeQuery']:
                    self.ael_variables[i][FRunScriptGUI.Controls.MANDATORY] = 2 if enabled == 'true' else 0
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex].startswith(fieldPrefix) and fieldPrefix != '':
                self.ael_variables[i][enableIndex] = enabled
        
        ins_export = 'false'
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex] == 'InstrumentExport':
                ins_export = fieldValues[i]

        trade_export = 'false'
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex] == 'TradeExport':
                trade_export = fieldValues[i]
                
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][nameIndex] == 'QueryIntersection':
                if ins_export == 'true' and trade_export == 'true':
                    self.ael_variables[i][enableIndex] = 'true'
                else:
                    self.ael_variables[i][enableIndex] = 'false'
        return fieldValues

    def _UpdateExportStateOnlyCb(self, index, fieldValues):
        for i in range(len(self.ael_variables)):
            if self.ael_variables[i][FRunScriptGUI.Controls.NAME] == 'AlwaysGenerateFile':
                self.ael_variables[i][FRunScriptGUI.Controls.ENABLED] = (fieldValues[index] == 'false')
        return fieldValues

    def _AddForceProcessAllTradesVariable(self):
        pass

    def parse_params(self, params):
        parameters = params.split('|')
        params_dict = {}
        for param in parameters:
            key, value = param.split('=')
            params_dict[key] = value
        return params_dict

    def _AddUpdateExportStateOnlyAdvancedVariable(self):
        ttUpdateExportStateOnly = 'Update the state of exportable trades only. No export will be performed'
        var = ['UpdateExportStateOnly', 'Update trade export states only_Advanced', 'string', [True, False], False, 0, 0, ttUpdateExportStateOnly, self._UpdateExportStateOnlyCb, True]
        self.ael_variables.append(var)

    def _AddUseGUIPartyVariable(self):
        pass

    def _AddPartyVariable(self):
        pass
        
    def _AddCustommodule(self):
        ttcustommodule = 'Select module for custom State chart and Trade Transitions. The module filename is CustomIntegration and should contain funcitons CreateExportStateChart(name), TradeTransitions() and EnviromenatSetuprCheck().'
        var = ['Custommodule', 'Custom Integration', 'string', None, '', False, False, ttcustommodule, self.custommCB, True]
        self.ael_variables.append(var)

    def _AddUpdateExportStateOnlyVariable(self):
        pass

    @staticmethod
    def getTradeQueries():
        return [query.Name() for query in acm.FStoredASQLQuery.Select('subType = FTrade').SortByProperty('Name') if query.User() == None]
        
    @staticmethod
    def getInstrumentQueries():
        return [query.Name() for query in acm.FStoredASQLQuery.Select('subType = FInstrument').SortByProperty('Name') if query.User() == None]

    @staticmethod
    def getStateCharts():
        return [stateChart.Name() for stateChart in acm.FStateChart.Select('').SortByProperty('Name')]

    @staticmethod
    def getParties():
        return [party.Name() for party in acm.FBroker.Select('').SortByProperty('Name')]

    @staticmethod
    def getPrintTemplateNames():
        context = acm.GetDefaultContext()
        extensions = context.GetAllExtensions('FXSLTemplate', 'FObject', True, True, 'aef reporting', 'secondary templates')
        extensionsList = extensions.AsString().replace(']', '').replace('[', '').replace(' ', '').split(',')
        extensionsList.sort()
        return extensionsList

    @staticmethod
    def get_default_date_formats():
        return ['', '%d%m%y', '%y%m%d', '%d%m%y%H%M', '%y%m%d%H%M', '%d%m%y%H%M%S', '%y%m%d%H%M%S']
    
    @staticmethod
    def getTradingSheetTemplates():
        return acm.FTradingSheetTemplate.Select('subType = FTradeSheet').SortByProperty('Name')
        
    @staticmethod    
    def getInstrumentSheetTemplates():
        return acm.FTradingSheetTemplate.Select('subType = FDealSheet').SortByProperty('Name')

    @staticmethod
    def add_datetime_to_filename(filename, datetime, beginning):
        name, extension = os.path.splitext(filename)
        return datetime + name + extension if beginning == 'true' else name + datetime + extension
        
    @staticmethod
    def getParameters(ael_params):
        now = datetime.datetime.now()
        variables = {
        '%DATE_TIME%': now.strftime('%Y-%m-%d %H%M%S'),
        '%EXPORT_DATE%': now.strftime('%Y-%m-%d'),
        '%EXPORT_TIME%': now.strftime('%H-%M-%S'),
        '%SHEET_TEMPLATE%': ael_params['tradingSheetTemplateName'],
        '%RECIPIENTS%': ael_params['EmailRecipient']
        }
        for variable, value in variables.items():
            ael_params['FileName'] = ael_params['FileName'].replace(variable, value)
            ael_params['Instrument_iFileName'] = ael_params['Instrument_iFileName'].replace(variable, value)
            ael_params['header'] = ael_params['header'].replace(variable, value)
            ael_params['footer'] = ael_params['footer'].replace(variable, value)
        variables['%FILENAME%'] = ael_params['FileName']
        for variable, value in variables.items():
            ael_params['EmailBody'] = ael_params['EmailBody'].replace(variable, value)
            ael_params['EmailSubject'] = ael_params['EmailSubject'].replace(variable, value)   
        if len(ael_params['FilePath']):
            ael_params['FilePath'] = ael_params['FilePath']
        else:
            ael_params['FilePath'] = tempfile.gettempdir()
        ael_params['header'] = ael_params['header'].replace('\comma', ',')
        ael_params['footer'] = ael_params['footer'].replace('\comma', ',')
        ael_params['EmailBody'] = ael_params['EmailBody'].replace('\comma', ',')
        ael_params['EmailSubject'] = ael_params['EmailSubject'].replace('\comma', ',')
        ael_params['EmailSender'] = ael_params['EmailSender'].replace('\comma', ',')
        ael_params['EmailRecipient'] = ael_params['EmailRecipient'].replace('\comma', ',')
        
        try:
            datetime_string = now.strftime(ael_params['DateFormat'])
            if ael_params['DateFormat']:
                ael_params['FileName'] = ExportAelVariables.add_datetime_to_filename(ael_params['FileName'], datetime_string, ael_params['DateAtBeginning'])
                ael_params['Instrument_iFileName'] = ExportAelVariables.add_datetime_to_filename(ael_params['Instrument_iFileName'], datetime_string, ael_params['DateAtBeginning'])
        except ValueError:
            logger.warn( "Invalid datetime format {}. Datetime is not added to file name.".format(ael_params['DateFormat']))
            
        paramClass = collections.namedtuple('ExportParameters', ael_params.keys())
        return paramClass(**ael_params)

ael_variables = ExportAelVariables().GetVariables()

def ael_main(params):
    logger_options = {'1. Information': 1, '2. Debug': 2, '3. Warnings': 3, '4. Errors': 4}
    options = ExportAelVariables.getParameters(params)
    if options.logtofile == 'true':
        logger.Reinitialize(level = logger_options[options.LogLevel], logToConsole=options.logtoconsole == 'true',
                            logToFileAtSpecifiedPath=options.logFileName)
    else:
        logger.Reinitialize(level = logger_options[options.LogLevel], logToConsole=options.logtoconsole == 'true')

    custom_integration_module = FExportUtils.import_custom_integration_module(params['Custommodule'])

    if params['Enviromentsetupcheck'] == 'true':
        if custom_integration_module and 'EnvironmentSetupCheck' in dir(custom_integration_module):
            custom_integration_module.EnvironmentSetupCheck()
        else:
            FExportBaseConfiguration.EnviromenatSetupCheck(params['stateChartName'])
    FExportBase.RunExport(options)