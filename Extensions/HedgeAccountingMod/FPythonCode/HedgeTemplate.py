'''
===================================================================================================
PURPOSE: This module handles the logic pertaining to the Hedge Effectiveness Test settings.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
===================================================================================================
'''

from xml.dom.minidom import parseString

import acm
import ael
import FLogger

import HedgeAccountingStorage
import HedgeConstants
import HedgeTimeBucketUtils
import HedgeUtils

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)


def get_templates():
    query_text = "select to.name from textobject to where to.type = 'Customizable' "\
                 "and name like 'HT_%'"
    _, data = ael.asql(query_text)
    result = []
    for element in data[0]:
        filename = element[0]
        m_id = filename[3:]
        template = HedgeTemplate(m_id)
        template.read()
        # result.append(template.GetName())
        result.append(m_id)
    return result


def get_statusses():
    return HedgeConstants.LST_HR_TEMPLATE_STATUSES


def get_default_status():
    return get_statusses()[0]


def get_test_settings(self):
    testsettings = {}
    testsettings['Properties'] = {
        'HedgeType': self.m_HedgeTemplate_optionHedgeType.GetData(),
        'HedgeSubType': self.m_HedgeTemplate_optionHedgeSubType.GetData(),
        'HedgeRiskType': self.m_HedgeTemplate_optionHedgeRiskType.GetData(),
        'HedgeObjective': self.m_HedgeTemplate_inputHedgeObjective.GetData(),
    }
    testsettings['ProDollarOffset'] = {
        'Enabled': self.m_HedgeTemplate_checkboxProDollarOffset.Checked(),
        'LoLimit': HedgeConstants.DBL_PRO_DO_LO_LIMIT,
        'HiLimit': HedgeConstants.DBL_PRO_DO_HI_LIMIT,
        'LoWarning': self.m_HedgeTemplate_inputProDOLoWarning.GetData(),
        'HiWarning': self.m_HedgeTemplate_inputProDOHiWarning.GetData(),
    }
    testsettings['Regression'] = {
        'Enabled': self.m_HedgeTemplate_checkboxRegression.Checked(),
        'HiBetaLimit': HedgeConstants.DBL_PRO_REG_HI_B_LIMIT,
        'LoBetaLimit': HedgeConstants.DBL_PRO_REG_LO_B_LIMIT,
        'R2Limit': HedgeConstants.DBL_PRO_REG_R2_LIMIT,
        'PValueLimit': HedgeConstants.DBL_PRO_REG_P_LIMIT,
        'HiBetaWarning': self.m_HedgeTemplate_inputPRHiBetaWarning.GetData(),
        'LoBetaWarning': self.m_HedgeTemplate_inputPRLoBetaWarning.GetData(),
        'R2Warning': self.m_HedgeTemplate_inputPRR2Warning.GetData(),
        'PValueWarning': self.m_HedgeTemplate_inputPRPValueWarning.GetData(),
    }
    testsettings['CriticalTerms'] = {
        'Enabled': self.m_HedgeTemplate_checkboxCriticalTerms.Checked(),
    }
    testsettings['ProVRM'] = {
        'Enabled': self.m_HedgeTemplate_checkboxProVRM.Checked(),
        'Limit': HedgeConstants.DBL_PRO_VRM_LIMIT,
        'Warning': self.m_HedgeTemplate_inputProVRMWarning.GetData(),
    }
    testsettings['RetroDollarOffset'] = {
        'Enabled': self.m_HedgeTemplate_checkboxRetroDollarOffset.Checked(),
        'LoLimit': HedgeConstants.DBL_RETRO_DO_LO_LIMIT,
        'HiLimit': HedgeConstants.DBL_RETRO_DO_HI_LIMIT,
        'LoWarning': self.m_HedgeTemplate_inputRetroDOLoWarning.GetData(),
        'HiWarning': self.m_HedgeTemplate_inputRetroDOHiWarning.GetData(),
    }
    testsettings['RetroVRM'] = {
        'Enabled': self.m_HedgeTemplate_checkboxRetroVRM.Checked(),
        'Limit': HedgeConstants.DBL_RETRO_VRM_LIMIT,
        'Warning': self.m_HedgeTemplate_inputRetroVRMWarning.GetData(),
    }
    testsettings['TimeBuckets'] = {
        'TimeBuckets': self.m_HedgeTemplate_timeBuckets.GetData(),
    }

    return testsettings


def set_test_settings_default(self):
    testsettings = {}
    testsettings['Properties'] = {
        'HedgeType': HedgeUtils.get_hedge_types()[0],
        'HedgeSubType': HedgeUtils.get_hedge_sub_types()[0],
        'HedgeRiskType': HedgeUtils.get_risk_types()[0],
        'HedgeObjective': '',
    }
    testsettings['ProDollarOffset'] = {
        'Enabled': False,
        'LoWarning': HedgeConstants.DBL_PRO_DO_LO_WARNING,
        'HiWarning': HedgeConstants.DBL_PRO_DO_HI_WARNING,
    }
    testsettings['Regression'] = {
        'Enabled': False,
        'HiBetaWarning': HedgeConstants.DBL_PRO_REG_HI_B_WARNING,
        'LoBetaWarning': HedgeConstants.DBL_PRO_REG_LO_B_WARNING,
        'R2Warning': HedgeConstants.DBL_PRO_REG_R2_WARNING,
        'PValueWarning': HedgeConstants.DBL_PRO_REG_P_WARNING,
    }
    testsettings['CriticalTerms'] = {
        'Enabled': False,
    }
    testsettings['ProVRM'] = {
        'Enabled': False,
        'Warning': HedgeConstants.DBL_PRO_VRM_WARNING,
    }
    testsettings['RetroDollarOffset'] = {
        'Enabled': False,
        'LoWarning': HedgeConstants.DBL_RETRO_DO_LO_WARNING,
        'HiWarning': HedgeConstants.DBL_RETRO_DO_HI_WARNING,
    }
    testsettings['RetroVRM'] = {
        'Enabled': False,
        'Warning': HedgeConstants.DBL_RETRO_VRM_WARNING,
    }
    testsettings['TimeBuckets'] = {
        'TimeBuckets': HedgeConstants.STR_DEFAULT_TIME_BUCKETS,
    }

    set_test_settings(self, testsettings)


def set_test_settings(self, testsettings):
    try:
        self.m_HedgeTemplate_optionHedgeType.SetData(
            testsettings['Properties']['HedgeType']
        )
        self.m_HedgeTemplate_optionHedgeSubType.SetData(
            testsettings['Properties']['HedgeSubType']
        )
        self.m_HedgeTemplate_optionHedgeRiskType.SetData(
            testsettings['Properties']['HedgeRiskType']
        )
        self.m_HedgeTemplate_inputHedgeObjective.SetData(
            testsettings['Properties']['HedgeObjective']
        )
        self.m_HedgeTemplate_checkboxProDollarOffset.Checked(
            testsettings['ProDollarOffset']['Enabled']
        )
        self.m_HedgeTemplate_inputProDOLoWarning.SetData(
            testsettings['ProDollarOffset']['LoWarning']
        )
        self.m_HedgeTemplate_inputProDOHiWarning.SetData(
            testsettings['ProDollarOffset']['HiWarning']
        )

        self.m_HedgeTemplate_checkboxRegression.Checked(
            testsettings['Regression']['Enabled']
        )
        self.m_HedgeTemplate_inputPRHiBetaWarning.SetData(
            testsettings['Regression']['HiBetaWarning']
        )
        self.m_HedgeTemplate_inputPRLoBetaWarning.SetData(
            testsettings['Regression']['LoBetaWarning']
        )
        self.m_HedgeTemplate_inputPRR2Warning.SetData(
            testsettings['Regression']['R2Warning']
        )
        self.m_HedgeTemplate_inputPRPValueWarning.SetData(
            testsettings['Regression']['PValueWarning']
        )

        self.m_HedgeTemplate_checkboxCriticalTerms.Checked(
            testsettings['CriticalTerms']['Enabled']
        )

        self.m_HedgeTemplate_checkboxProVRM.Checked(
            testsettings['ProVRM']['Enabled']
        )
        self.m_HedgeTemplate_inputProVRMWarning.SetData(
            testsettings['ProVRM']['Warning']
        )

        self.m_HedgeTemplate_checkboxRetroDollarOffset.Checked(
            testsettings['RetroDollarOffset']['Enabled']
        )
        self.m_HedgeTemplate_inputRetroDOLoWarning.SetData(
            testsettings['RetroDollarOffset']['LoWarning']
        )
        self.m_HedgeTemplate_inputRetroDOHiWarning.SetData(
            testsettings['RetroDollarOffset']['HiWarning']
        )

        self.m_HedgeTemplate_checkboxRetroVRM.Checked(
            testsettings['RetroVRM']['Enabled']
        )
        self.m_HedgeTemplate_inputRetroVRMWarning.SetData(
            testsettings['RetroVRM']['Warning']
        )

        self.m_HedgeTemplate_timeBuckets.SetData(
            testsettings['TimeBuckets']['TimeBuckets']
        )

    except Exception as e:
        logger.ELOG('Error in set_test_settings %s' % str(e))


def set_fields_enabled(self, enabled):
    self.m_HedgeTemplate_checkboxProDollarOffset.Enabled(enabled)
    self.m_HedgeTemplate_checkboxRegression.Enabled(enabled)
    self.m_HedgeTemplate_checkboxCriticalTerms.Enabled(enabled)
    self.m_HedgeTemplate_checkboxProVRM.Enabled(enabled)
    self.m_HedgeTemplate_checkboxRetroDollarOffset.Enabled(enabled)
    self.m_HedgeTemplate_checkboxRetroVRM.Enabled(enabled)
    self.m_HedgeTemplate_timeBuckets.Enabled(enabled)
    on_hedgetemplate_testsetting_change(self, enabled)


def on_hedgetemplate_testsetting_change(self, cd):
    show = True
    self.invalid_tests_selected = False
    if cd is False:  # Template is selected - do not enable fields
        show = False

    # Enforce selection of precisely one retro test and precisely one pro test
    if show:
        if self.m_HedgeTemplate_checkboxProDollarOffset.Checked():
            self.m_HedgeTemplate_checkboxRegression.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxRegression.Checked(False)
            self.m_HedgeTemplate_checkboxProVRM.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxProVRM.Checked(False)
            self.m_HedgeTemplate_checkboxCriticalTerms.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxCriticalTerms.Checked(False)
        elif self.m_HedgeTemplate_checkboxRegression.Checked():
            self.m_HedgeTemplate_checkboxProDollarOffset.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxProDollarOffset.Checked(False)
            self.m_HedgeTemplate_checkboxProVRM.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxProVRM.Checked(False)
            self.m_HedgeTemplate_checkboxCriticalTerms.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxCriticalTerms.Checked(False)
        elif self.m_HedgeTemplate_checkboxProVRM.Checked():
            self.m_HedgeTemplate_checkboxProDollarOffset.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxProDollarOffset.Checked(False)
            self.m_HedgeTemplate_checkboxRegression.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxRegression.Checked(False)
            self.m_HedgeTemplate_checkboxCriticalTerms.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxCriticalTerms.Checked(False)
        elif self.m_HedgeTemplate_checkboxCriticalTerms.Checked():
            self.m_HedgeTemplate_checkboxProDollarOffset.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxProDollarOffset.Checked(False)
            self.m_HedgeTemplate_checkboxRegression.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxRegression.Checked(False)
            self.m_HedgeTemplate_checkboxProVRM.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxProVRM.Checked(False)
        else:
            self.m_HedgeTemplate_checkboxCriticalTerms.Enabled(True)
            self.m_HedgeTemplate_checkboxProDollarOffset.Enabled(True)
            self.m_HedgeTemplate_checkboxRegression.Enabled(True)
            self.m_HedgeTemplate_checkboxProVRM.Enabled(True)
            self.invalid_tests_selected = True

        if self.m_HedgeTemplate_checkboxRetroDollarOffset.Checked():
            self.m_HedgeTemplate_checkboxRetroVRM.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxRetroVRM.Checked(False)
        elif self.m_HedgeTemplate_checkboxRetroVRM.Checked():
            self.m_HedgeTemplate_checkboxRetroDollarOffset.Enabled(False)
            # Included for test HRs created without selection logic
            self.m_HedgeTemplate_checkboxRetroDollarOffset.Checked(False)
        else:
            self.m_HedgeTemplate_checkboxRetroVRM.Enabled(True)
            self.m_HedgeTemplate_checkboxRetroDollarOffset.Enabled(True)
            self.invalid_tests_selected = True

    # Add User Interface feedback when the enabled checkboxes are (un)toggled
    self.m_HedgeTemplate_optionHedgeType.Enabled(show)
    self.m_HedgeTemplate_optionHedgeSubType.Enabled(show)
    self.m_HedgeTemplate_optionHedgeRiskType.Enabled(show)
    self.m_HedgeTemplate_inputHedgeObjective.Enabled(show)

    self.m_HedgeTemplate_inputProDOLoWarning.Enabled(
        self.m_HedgeTemplate_checkboxProDollarOffset.Checked() and show)
    self.m_HedgeTemplate_inputProDOHiWarning.Enabled(
        self.m_HedgeTemplate_checkboxProDollarOffset.Checked() and show)

    self.m_HedgeTemplate_inputPRHiBetaWarning.Enabled(
        self.m_HedgeTemplate_checkboxRegression.Checked() and show)
    self.m_HedgeTemplate_inputPRLoBetaWarning.Enabled(
        self.m_HedgeTemplate_checkboxRegression.Checked() and show)
    self.m_HedgeTemplate_inputPRR2Warning.Enabled(
        self.m_HedgeTemplate_checkboxRegression.Checked() and show)
    self.m_HedgeTemplate_inputPRPValueWarning.Enabled(
        self.m_HedgeTemplate_checkboxRegression.Checked() and show)

    self.m_HedgeTemplate_inputProVRMWarning.Enabled(
        self.m_HedgeTemplate_checkboxProVRM.Checked() and show)

    self.m_HedgeTemplate_inputRetroDOLoWarning.Enabled(
        self.m_HedgeTemplate_checkboxRetroDollarOffset.Checked() and show)
    self.m_HedgeTemplate_inputRetroDOHiWarning.Enabled(
        self.m_HedgeTemplate_checkboxRetroDollarOffset.Checked() and show)

    self.m_HedgeTemplate_inputRetroVRMWarning.Enabled(
        self.m_HedgeTemplate_checkboxRetroVRM.Checked() and show)

    self.m_HedgeTemplate_timeBuckets.Enabled(show)


def warn_for_foreign_subType(self, cd):
    shell = acm.UX().SessionManager().Shell()
    if self.m_HedgeTemplate_optionHedgeSubType.GetData().startswith('Foreign'):
        warning_msg = 'Consider the creation of two separate Hedge Relationships - ' \
            'one for the Interest Rate risk and another for the Currency risk'
        acm.UX().Dialogs().MessageBoxInformation(shell, warning_msg)


def HandleCreate(self, dlg, layout):
    self.m_HedgeTemplate_optionHedgeType = layout.GetControl('optionHedgeType')
    self.m_HedgeTemplate_optionHedgeSubType = layout.GetControl('optionHedgeSubType')
    self.m_HedgeTemplate_optionHedgeRiskType = layout.GetControl('optionHedgeRiskType')
    self.m_HedgeTemplate_inputHedgeObjective = layout.GetControl('inputHedgeObjective')

    self.m_HedgeTemplate_checkboxProDollarOffset = layout.GetControl('checkboxProDollarOffset')
    self.m_HedgeTemplate_inputProDOLoWarning = layout.GetControl('inputProDOLoWarning')
    self.m_HedgeTemplate_inputProDOHiWarning = layout.GetControl('inputProDOHiWarning')

    self.m_HedgeTemplate_checkboxRegression = layout.GetControl('checkboxRegression')
    self.m_HedgeTemplate_inputPRHiBetaWarning = layout.GetControl('inputPRHiBetaWarning')
    self.m_HedgeTemplate_inputPRLoBetaWarning = layout.GetControl('inputPRLoBetaWarning')
    self.m_HedgeTemplate_inputPRR2Warning = layout.GetControl('inputPRR2Warning')
    self.m_HedgeTemplate_inputPRPValueWarning = layout.GetControl('inputPRPValueWarning')

    self.m_HedgeTemplate_checkboxCriticalTerms = layout.GetControl('checkboxCriticalTerms')

    self.m_HedgeTemplate_checkboxProVRM = layout.GetControl('checkboxProVRM')
    self.m_HedgeTemplate_inputProVRMWarning = layout.GetControl('inputProVRMWarning')

    self.m_HedgeTemplate_checkboxRetroDollarOffset = layout.GetControl('checkboxRetroDollarOffset')
    self.m_HedgeTemplate_inputRetroDOLoWarning = layout.GetControl('inputRetroDOLoWarning')
    self.m_HedgeTemplate_inputRetroDOHiWarning = layout.GetControl('inputRetroDOHiWarning')

    self.m_HedgeTemplate_checkboxRetroVRM = layout.GetControl('checkboxRetroVRM')
    self.m_HedgeTemplate_inputRetroVRMWarning = layout.GetControl('inputRetroVRMWarning')

    self.m_HedgeTemplate_timeBuckets = layout.GetControl('timeBuckets')

    # populate popuplists
    for hedgeType in HedgeUtils.get_hedge_types():
        self.m_HedgeTemplate_optionHedgeType.AddItem(hedgeType)

    for hedgeSubType in HedgeUtils.get_hedge_sub_types():
        self.m_HedgeTemplate_optionHedgeSubType.AddItem(hedgeSubType)

    for hedgeRiskType in HedgeUtils.get_risk_types():
        self.m_HedgeTemplate_optionHedgeRiskType.AddItem(hedgeRiskType)

    userOwnedTimeBucketList = HedgeTimeBucketUtils.get_all_timebuckets_per_owner(acm.User())
    for timeBucketName in userOwnedTimeBucketList:
        self.m_HedgeTemplate_timeBuckets.AddItem(timeBucketName)

    # Add Callbacks
    self.m_HedgeTemplate_optionHedgeSubType.AddCallback('Changed',
                                                        warn_for_foreign_subType,
                                                        self)
    self.m_HedgeTemplate_checkboxProDollarOffset.AddCallback('Activate',
                                                             on_hedgetemplate_testsetting_change,
                                                             self)
    self.m_HedgeTemplate_checkboxRegression.AddCallback('Activate',
                                                        on_hedgetemplate_testsetting_change,
                                                        self)
    self.m_HedgeTemplate_checkboxCriticalTerms.AddCallback('Activate',
                                                           on_hedgetemplate_testsetting_change,
                                                           self)
    self.m_HedgeTemplate_checkboxProVRM.AddCallback('Activate',
                                                    on_hedgetemplate_testsetting_change,
                                                    self)
    self.m_HedgeTemplate_checkboxRetroDollarOffset.AddCallback('Activate',
                                                               on_hedgetemplate_testsetting_change,
                                                               self)
    self.m_HedgeTemplate_checkboxRetroVRM.AddCallback('Activate',
                                                      on_hedgetemplate_testsetting_change,
                                                      self)

    set_test_settings_default(self)


def CreateLayout(b):
    b.BeginVertBox('None', '')
    b.  BeginVertBox('EtchedIn', 'Hedge Properties')
    b.    BeginHorzBox('None', '')
    b.      AddOption('optionHedgeType', 'Hedge Type', 26, -1)
    b.      AddOption('optionHedgeSubType', 'Hedge Sub Type', 22, -1)
    b.    EndBox()
    b.    AddOption('optionHedgeRiskType', 'Hedge Risk Type', 22, -1)
    b.    AddInput('inputHedgeObjective', 'Hedge Objective', 26, -1)
    b.  EndBox()
    b.  BeginVertBox('EtchedIn', 'Prospective Test Criteria')
    b.      BeginVertBox('EtchedIn', 'Dollar Offset: Effectiveness LIMITS => (%s <= DO <= %s)'
                         % (HedgeConstants.DBL_PRO_DO_LO_LIMIT, HedgeConstants.DBL_PRO_DO_HI_LIMIT))
    b.        AddCheckbox('checkboxProDollarOffset', 'Enabled')
    b.        BeginHorzBox('None', '')
    b.          AddInput('inputProDOLoWarning', 'Lo Warning', 10, 10)
    b.          AddFill()
    b.          AddInput('inputProDOHiWarning', 'Hi Warning', 10, 10)
    b.        EndBox()
    b.      EndBox()
    b.      BeginVertBox('EtchedIn', 'Regression: Effectiveness LIMITS => (%s <= Beta <= %s), '
                         '(R2 >= %s), (p <= %s)' % (HedgeConstants.DBL_PRO_REG_LO_B_LIMIT,
                                                    HedgeConstants.DBL_PRO_REG_HI_B_LIMIT,
                                                    HedgeConstants.DBL_PRO_REG_R2_LIMIT,
                                                    HedgeConstants.DBL_PRO_REG_P_LIMIT))
    b.        AddCheckbox('checkboxRegression', 'Enabled')
    b.        BeginHorzBox('None', '')
    b.          AddInput('inputPRHiBetaWarning', 'Hi Beta Warning', 10, 10, -1, 'Vertical')
    b.          AddInput('inputPRLoBetaWarning', 'Lo Beta Warning', 10, 10, -1, 'Vertical')
    b.          AddInput('inputPRR2Warning', 'R2 Warning', 10, 10, -1, 'Vertical')
    b.          AddInput('inputPRPValueWarning', 'p-value Warning', 10, 10, -1, 'Vertical')
    b.        EndBox()
    b.      EndBox()
    b.      BeginVertBox('EtchedIn', 'Critical Terms')
    b.        AddCheckbox('checkboxCriticalTerms', 'Enabled')
    b.      EndBox()
    b.      BeginVertBox('EtchedIn', 'Variable Reduction Method: Effectiveness LIMIT => '
                         '(VRM >= %s)' % HedgeConstants.DBL_PRO_VRM_LIMIT)
    b.        AddCheckbox('checkboxProVRM', 'Enabled')
    b.        BeginHorzBox('None', '')
    b.          AddInput('inputProVRMWarning', 'Warning', 10, 10)
    b.        EndBox()
    b.      EndBox()
    b.  EndBox()
    b.  BeginVertBox('EtchedIn', 'Retrospective Test Criteria')
    b.    BeginVertBox('EtchedIn', 'Dollar Offset: Effectiveness LIMITS => (%s <= DO <= %s)'
                       % (HedgeConstants.DBL_RETRO_DO_LO_LIMIT,
                          HedgeConstants.DBL_RETRO_DO_HI_LIMIT))
    b.        AddCheckbox('checkboxRetroDollarOffset', 'Enabled')
    b.        BeginHorzBox('None', '')
    b.          AddInput('inputRetroDOLoWarning', 'Lo Warning', 10, 10)
    b.          AddFill()
    b.          AddInput('inputRetroDOHiWarning', 'Hi Warning', 10, 10)
    b.      EndBox()
    b.    EndBox()
    b.    BeginVertBox('EtchedIn', 'Variable Reduction Method: Effectiveness LIMIT => (VRM >= %s)'
                       % HedgeConstants.DBL_RETRO_VRM_LIMIT)
    b.        AddCheckbox('checkboxRetroVRM', 'Enabled')
    b.        BeginHorzBox('None', '')
    b.          AddInput('inputRetroVRMWarning', 'Warning', 10, 10)
    b.      EndBox()
    b.    EndBox()
    b.  EndBox()
    b.  BeginVertBox('EtchedIn', 'Testing Schedule')
    b.    AddOption('timeBuckets', 'Time Buckets', 50, -1)
    b.  EndBox()
    b.EndBox()


class HedgeTemplate():
    def __init__(self, m_id=None):
        self.new()
        self.m_id = m_id
        self.m_xml = None
        self.m_root = None

    def get_file_name(self, m_id=None):
        if m_id:
            return 'HT_' + str(m_id)
        if self.m_id:
            return 'HT_' + self.m_id
        return None

    def read(self, m_id=None):
        if not m_id:
            m_id = self.get_file_name()

        if m_id:
            text_object = HedgeAccountingStorage.TextObjectManager.get_textobject(m_id,
                                                                                  'Customizable')

            if not text_object:
                logger.WLOG('Unable to find Hedge Template: %s' % m_id)
                # Return False, no existing textobject was found
                return False

            self.m_xml = parseString(text_object.get_text())
            self.m_root = self.m_xml.getElementsByTagName('hedge')[0]
        # Return True, an existing relationship was found
        return True

    def new(self):
        # Initialize Object
        data = '<?xml version="1.0" ?><xml><hedge></hedge></xml>'
        self.m_xml = parseString(data)
        self.m_root = self.m_xml.getElementsByTagName('hedge')[0]
        self.m_id = None

    def save(self):
        filename = self.get_file_name()
        m_id = self.get_id()
        if filename:
            HedgeAccountingStorage.TextObjectManager.set_textobject(filename,
                                                                    'Customizable',
                                                                    self.m_xml.toxml())
        else:
            self.save_new()
        logger.LOG('Saved Hedge Template %s' % m_id)

    def delete(self):
        filename = self.get_file_name()
        m_id = self.get_id()
        if filename:
            HedgeAccountingStorage.TextObjectManager.del_textobject(filename, 'Customizable')
            logger.LOG('Deleted Hedge Template %s' % m_id)

    def get_id(self):
        if self.m_id:
            return self.m_id

        return ''

    def set_id(self, value):
        self.m_id = value
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'id', value)

    def SetName(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'name', value)

    def GetName(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'name')

    def get_status(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'status')

    def set_status(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'status', value)

    def get_test_settings(self):
        result = {}

        for testsettings in HedgeAccountingStorage.get_elements(self.m_root, 'testsettings'):
            for testNode in testsettings.childNodes:
                settings = {}
                for settingNode in testNode.childNodes:
                    settings[str(settingNode.tagName)] = HedgeAccountingStorage.\
                        get_element_tag_value(testNode,
                                              settingNode.tagName)
                result[str(testNode.tagName)] = settings
        return result

    def set_test_settings(self, settings):
        # Expect a dictionary of settings
        # First remove all test settings, then create new
        for testsetting in HedgeAccountingStorage.get_elements(self.m_root, 'testsettings'):
            self.m_root.removeChild(testsetting)

        testsettings = self.m_xml.createElement('testsettings')
        self.m_root.appendChild(testsettings)

        for test in settings.keys():
            testnode = self.m_xml.createElement(test)
            testsettings.appendChild(testnode)
            for setting in settings[test].keys():
                value = settings[test][setting]
                HedgeAccountingStorage.set_element_tag_value(self.m_xml, testnode, setting, value)
