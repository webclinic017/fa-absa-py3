'''
===================================================================================================
PURPOSE: The HedgeRelation class is an in memory representation of the complete Hedge Relationship.
            The Hedge Relationship properties are managed and stored in XML that can be persisted
            into a Front Arena Text Object. The class provide accessors to update and retrieve
            Hedge Relationship properties from the XML representation.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016      FIS Team                Initial implementation
28-08-2018      Jaysen Naicker          Change touch trades to touch trade dealpcakages as work 
                                        around for archived trades.
18-03-2021      Qaqamba Ntshobane       Added termination nominal getter and setter
===================================================================================================
'''

from xml.dom.minidom import parseString

import acm
import ael
import FLogger

import HedgeAccountingStorage
import HedgeTemplate
from HedgeValidation import UserAccess
import HedgeConstants
import HedgeUtils

userAccess = UserAccess(acm.User())
logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)


def custom_method_text_object_status(text_object):
    try:
        hr = HedgeRelation('HR/' + str(text_object.Oid()))
        hr.read()
        return hr.get_status()
    except:
        return None


def get_hedge_accounting_filenames():
    query_text = "select to.name from textobject to where to.type = 'Customizable' "\
                 "and name like 'HR/%'"
    _, data = ael.asql(query_text)
    result = []
    for element in data[0]:
        filename = element[0]
        result.append(filename)
    return result


def get_hedge_relations():
    relations = []
    for filename in get_hedge_accounting_filenames():
        relations.append(filename)
    return relations


def find_relation_for_trade(trade):
    # For CustomMethod
    trade = trade.OriginalOrSelf()
    result = []
    for filename in get_hedge_accounting_filenames():
        h = HedgeRelation(filename)
        h.read()
        if str(trade.Oid()) in list(h.get_trades().keys()):
            result.append(filename)
    return result


class HedgeRelation():
    def __init__(self, m_id):
        self.m_id = m_id
        self.m_xml = None
        self.m_root = None
        self.m_testSettings = None
        data = '<?xml version="1.0" ?><xml><hedge></hedge></xml>'
        self.m_xml = parseString(data)
        self.m_root = self.m_xml.getElementsByTagName('hedge')[0]

    def get_file_name(self, m_id=None):
        if m_id:
            return str(m_id)
        if self.m_id:
            return self.m_id
        return None

    def read(self, m_id=None):
        if not m_id:
            m_id = self.get_file_name()

        if m_id:
            text_object = HedgeAccountingStorage.TextObjectManager.get_textobject(m_id,
                                                                                  'Customizable')
            if not text_object:
                logger.WLOG('Unable to find Hedge Relation: %s' % m_id)
                return False  # Return False, no existing relationship was found

            self.m_xml = parseString(text_object.get_text())
            self.m_root = self.m_xml.getElementsByTagName('hedge')[0]
            self.m_id = HedgeAccountingStorage.get_element_tag_value(self.m_root, 'id')
        # Return True, an existing relationship was found
        return True

    def new(self):
        data = '<?xml version="1.0" ?><xml><hedge></hedge></xml>'
        self.m_xml = parseString(data)
        self.m_root = self.m_xml.getElementsByTagName('hedge')[0]
        self.m_id = None

    def save(self):
        filename = self.get_file_name()
        hedge_id = self.get_id()
        if filename:
            self.set_audit_details()
            HedgeAccountingStorage.TextObjectManager.set_textobject(filename,
                                                                    'Customizable',
                                                                    self.m_xml.toxml())
        else:
            self.save_new()
        self.touch_trades()  # used to ensure that the columns update in real time
        logger.LOG('Saved Hedge Relation %s' % hedge_id)

    def touch_trades(self):
        # touch and commit dealpackages on chilfd trades
        trades = self.get_trades()
        for tradeOid in trades:
            _, _, childOid = trades[tradeOid]
            if childOid:
                child = acm.FTrade[childOid].DealPackage()
                if child:
                    child.Touch()
                    child.Commit()

    def save_new(self):
        tmpFileName = HedgeConstants.STR_DEALPACKAGE_NAME_PREFIX

        if not self.m_xml:
            self.new()
        textObject = HedgeAccountingStorage.TextObjectManager.set_textobject(tmpFileName,
                                                                             'Customizable',
                                                                             self.m_xml.toxml())

        # Update the name after saving
        if textObject:
            self.set_id(textObject.name)

        logger.LOG('Saved Hedge Relation %s' % id)

    def delete(self, delete_package=False):
        filename = self.get_file_name()
        if filename:
            m_id = self.get_id()
            HedgeAccountingStorage.TextObjectManager.del_textobject(filename, 'Customizable')
            if delete_package:
                ins_package = acm.FInstrumentPackage[filename]
                if ins_package:
                    for deal_package in ins_package.DealPackages():
                        deal_package.Delete(True, False)  # delete child DPs but not trades
                    ins_package.Delete()
            logger.LOG('Deleted Hedge Relation %s' % m_id)

    def get_id(self):
        if self.m_id:
            return str(self.m_id).strip()

        return ''

    def set_id(self, value):
        value = str(value).strip()
        self.m_id = value
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'id', value)

    def get_HR_reference(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'hr_reference')

    def set_HR_reference(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'hr_reference',
                                                     value)

    def get_status(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'status')

    def set_status(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'status', value)

    def get_statusses(self):
        result = []

        result = userAccess.get_valid_statuses()
        return result

    def get_type(self):
        settings = self.get_test_settings()
        try:
            return settings['Properties']['HedgeType']
        except:
            return None

    def set_type(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'HedgeType', value)

    def get_sub_type(self):
        settings = self.get_test_settings()
        try:
            return settings['Properties']['HedgeSubType']
        except:
            return None

    def set_sub_type(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'HedgeSubType',
                                                     value)

    def get_pro_reg_enabled(self):
        settings = self.get_test_settings()
        try:
            return settings['Regression']['Enabled']
        except:
            return 'False'

    def set_pro_reg_enabled(self, value):
        proRegRoot = self.m_xml.getElementsByTagName('Regression')
        if not proRegRoot:
            return 'False'
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, proRegRoot[0], 'Enabled', value)

    def get_pro_do_enabled(self):
        settings = self.get_test_settings()
        try:
            return settings['ProDollarOffset']['Enabled']
        except:
            return 'False'

    def set_pro_do_enabled(self, value):
        proDORoot = self.m_xml.getElementsByTagName('ProDollarOffset')
        if not proDORoot:
            return 'False'
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, proDORoot[0], 'Enabled', value)

    def get_pro_cv_enabled(self):
        settings = self.get_test_settings()
        try:
            return settings['CriticalTerms']['Enabled']
        except:
            return 'False'

    def set_pro_cv_enabled(self, value):
        ctRoot = self.m_xml.getElementsByTagName('CriticalTerms')
        if not ctRoot:
            return 'False'
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, ctRoot[0], 'Enabled', value)

    def get_ret_do_enabled(self):
        settings = self.get_test_settings()
        try:
            return settings['RetroDollarOffset']['Enabled']
        except:
            return 'False'

    def set_ret_do_enabled(self, value):
        retDORoot = self.m_xml.getElementsByTagName('RetroDollarOffset')
        if not retDORoot:
            return 'False'
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, retDORoot[0], 'Enabled', value)

    def get_pro_vrm_enabled(self):
        settings = self.get_test_settings()
        try:
            return settings['ProVRM']['Enabled']
        except:
            return 'False'

    def set_pro_vrm_enabled(self, value):
        proVRMRoot = self.m_xml.getElementsByTagName('ProVRM')
        if not proVRMRoot:
            return 'False'
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, proVRMRoot[0], 'Enabled', value)

    def get_ret_vrm_enabled(self):
        settings = self.get_test_settings()
        try:
            return settings['RetroVRM']['Enabled']
        except:
            return 'False'

    def set_ret_vrm_enabled(self, value):
        retVRMRoot = self.m_xml.getElementsByTagName('RetroVRM')
        if not retVRMRoot:
            return 'False'
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, retVRMRoot[0], 'Enabled', value)

    def get_start_date(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'startdate')

    def set_start_date(self, value):
        value = value.replace('/', '-')
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'startdate', value)

    def get_end_date(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'enddate')

    def set_end_date(self, value):
        value = value.replace('/', '-')
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'enddate', value)

    def get_termination(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'termination')

    def set_termination(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'termination', value)

    def get_nominal(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'terminationNominal')

    def set_nominal(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml, self.m_root, 'terminationNominal', value)

    def get_termination_date(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'terminationDate')

    def set_termination_date(self, value):
        value = value.replace('/', '-')
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'terminationDate',
                                                     value)

    def get_inception_date(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'inceptiondate')

    def set_inception_date(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'inceptiondate',
                                                     value)

    def get_date_method(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'datemethod')

    def set_date_method(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'datemethod',
                                                     value)

    def get_time_bucket_name(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'timebucket')

    def set_time_bucket_name(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'timebucket',
                                                     value)

    def get_objective(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'objective')

    def set_objective(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'objective',
                                                     value)

    def get_risk_type(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'risktype')

    def set_risk_type(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'risktype',
                                                     value)

    def get_assessment(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'assessment')

    def set_assessment(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'assessment',
                                                     value)

    def get_prospective(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'prospective')

    def set_prospective(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'prospective',
                                                     value)

    def get_retrospective(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'retrospective')

    def set_retrospective(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'retrospective',
                                                     value)

    def get_backdate_reason(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'backdate')

    def set_backdate_reason(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'backdate',
                                                     value)

    def get_audit_details(self):
        '''
            Get the stored Audit details from the hedgerealion xml
        '''
        # Column Widths
        adjust = [12, 23, 20, 20, 20, 15, 25, 15]
        trAdjust = [12, 23, 20, 15]
        endStr = '-'*sum(adjust)
        returnStr = endStr + '\n\n'
        # Headers
        headers = ['User', 'Update Time', 'Status', 'Start Date', 'End Date',
                   'Termination Reason\t', 'Termination Date']
        trHeaders = ['Trade ID', 'Hedge Type', 'Hedge Percentage', 'Child ID']
        # Column formatters
        hrFormatString = ['%s', '%s', '%s', '%s', '%s', '%s', '%s']
        trFormatString = ['%s', '%s', '%s', '%s']
        # Populate headers
        daHeaderStr = ''
        for a in range(0, len(hrFormatString)):
            daHeaderStr = daHeaderStr + headers[a].ljust(adjust[a])
        daHeaderStr = daHeaderStr + '\n'
        trHeaderStr = ''

        for a in range(0, len(trFormatString) - 1):
            trHeaderStr = trHeaderStr + trHeaders[a].ljust(trAdjust[a])
        trHeaderStr = trHeaderStr + '\n'

        # cycle through audit history
        for audit in self.m_xml.getElementsByTagName('audit'):
            # Print hr data headers
            returnStr = returnStr + daHeaderStr
            # Print hr data
            rawData = HedgeAccountingStorage.get_element_tag_value(audit, 'data')
            data = rawData.split('|')
            for a in range(0, len(hrFormatString) - 1):
                returnStr = returnStr + (hrFormatString[a] % data[a]).ljust(adjust[a])
            returnStr = returnStr + '\n\n'

            # Print trade header
            returnStr = returnStr + trHeaderStr

            # Get trade rows
            rawTradeData = HedgeAccountingStorage.get_element_tag_value(audit, 'tradeData')
            tradeData = rawTradeData.split(',')

            # Print trade data
            for trade in tradeData:
                splitTrade = trade.split('|')
                for b in range(0, len(trFormatString) - 1):
                    returnStr = returnStr + (trFormatString[b] % splitTrade[b]).ljust(trAdjust[b])
                returnStr = returnStr + '\n'
            returnStr = returnStr + endStr + '\n\n'
        return returnStr

    def set_audit_details(self):
        '''
            Record the details of the hedge relationship in the xml
        '''
        # Create or find auditDetails node
        auditDetailsNodes = self.m_xml.getElementsByTagName('auditDetails')
        if auditDetailsNodes:
            auditDetailsNode = auditDetailsNodes[0]
        else:
            auditDetailsNode = self.m_xml.createElement('auditDetails')
            self.m_root.appendChild(auditDetailsNode)

        # Get and format hr data
        user = acm.FACMServer().User().Name()
        time = str(acm.Time().TimeNow())
        # if logged in with Date Today set, the time defaults to 00:00:00
        if abs(acm.Time.DateDifference(acm.Time.DateNow(), acm.Time.RealDateNow())) > 0:
            real_date_time = acm.Time.RealTimeNow()
            first_colon_index = real_date_time.find(':')
            real_time = real_date_time[first_colon_index-2:first_colon_index+6]
            time = time.replace('00:00:00', real_time)
        status = self.get_status()
        startDate = self.get_start_date()
        endDate = self.get_end_date()
        if status == HedgeConstants.Hedge_Relation_Status.DeDesignated:
            termination = self.get_termination()
            terminationDate = self.get_termination_date()
        else:
            termination = ''
            terminationDate = ''

        dataArray = [user, time, status, startDate, endDate, termination, terminationDate]
        data = '|'.join(dataArray)

        checkArray = ['', '', status, startDate, endDate, termination, terminationDate]
        check = '|'.join(checkArray)

        # Get and format trade data
        trades = self.get_trades()
        tradeData = ''
        for tradeOid in trades:
            [m_type, percent, childTradeOid] = trades[tradeOid]
            tradeData = tradeData + '|'.join([tradeOid, m_type, percent, childTradeOid]) + ','
        tradeData = tradeData[:-1]

        # Find the last audit node
        auditCnt = 0
        for _ in self.m_xml.getElementsByTagName('audit'):
            auditCnt += 1

        if auditCnt > 1:
            auditNode = self.m_xml.getElementsByTagName('audit')[auditCnt-1]
            lastData = HedgeAccountingStorage.get_element_tag_value(auditNode, 'data')
            lastTradeData = HedgeAccountingStorage.get_element_tag_value(auditNode,
                                                                         'tradeData')
            lastDataArray = lastData.split('|')
            lastDataArray[0] = ''
            lastDataArray[1] = ''
            lastData = '|'.join(lastDataArray)
        else:
            lastData = ''
            lastTradeData = ''

        if lastData != check or lastTradeData != tradeData:
            tag = self.m_xml.createElement('audit')
            auditDetailsNode.appendChild(tag)
            auditNode = self.m_xml.getElementsByTagName('audit')[auditCnt]
            HedgeAccountingStorage.set_element_tag_value(self.m_xml, auditNode, 'data', data)
            HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                         auditNode,
                                                         'tradeData',
                                                         tradeData)

    def overall_pass_achieved(self):
        _, deal_package_name = self.get_deal_package()
        if not deal_package_name:
            return 0
        test_dates = HedgeUtils.get_test_dates(deal_package_name)
        if test_dates:
            latest_date = test_dates[-1]
        else:
            return 0
        deal_package = acm.FDealPackage[deal_package_name]
        if not deal_package:
            return ''
        ts_spec_id = HedgeUtils.get_time_series_spec_id()
        overall_result_id = HedgeUtils.get_overall_result_id()
        overall_result = HedgeUtils.get_time_series_dv_value_date(deal_package.Oid(),
                                                                  ts_spec_id,
                                                                  overall_result_id,
                                                                  latest_date)
        return overall_result

    def get_test_history(self):
        _, deal_package_name = self.get_deal_package()
        test_dates = HedgeUtils.get_test_dates(deal_package_name)
        deal_package = acm.FDealPackage[deal_package_name]
        if not deal_package:
            return ''
        end_string = '-'*150
        ts_spec_id = HedgeUtils.get_time_series_spec_id()
        overall_result_id = HedgeUtils.get_overall_result_id()
        pro_do_result_id = HedgeUtils.get_pro_do_result_id()
        ret_do_result_id = HedgeUtils.get_ret_do_result_id()
        pro_reg_result_id = HedgeUtils.get_pro_reg_result_id()
        pro_vrm_result_id = HedgeUtils.get_pro_vrm_result_id()
        ret_vrm_result_id = HedgeUtils.get_ret_vrm_result_id()
        pro_ct_result_id = HedgeUtils.get_pro_cv_result_id()

        return_string = end_string + '\n\n'
        for test_date in test_dates:
            return_string = return_string + 'Test Date: %s\n\n' % test_date
            overall_result = HedgeUtils.get_time_series_dv_value_date(deal_package.Oid(),
                                                                      ts_spec_id,
                                                                      overall_result_id,
                                                                      test_date)

            if overall_result is not None:
                return_string = return_string + self.get_test_result_string(overall_result,
                                                                            'Overall Result')
                return_string = return_string + '\n'

            pro_do_result = HedgeUtils.get_time_series_dv_value_date(deal_package.Oid(),
                                                                     ts_spec_id,
                                                                     pro_do_result_id,
                                                                     test_date)
            if pro_do_result is not None:
                return_string = return_string +\
                                    self.get_test_result_string(pro_do_result,
                                                                'Prospective Dollar Offset')

            ret_do_result = HedgeUtils.get_time_series_dv_value_date(deal_package.Oid(),
                                                                     ts_spec_id,
                                                                     ret_do_result_id,
                                                                     test_date)
            if ret_do_result is not None:
                return_string = return_string +\
                                        self.get_test_result_string(ret_do_result,
                                                                    'Retrospective Dollar Offset')

            pro_reg_result = HedgeUtils.get_time_series_dv_value_date(deal_package.Oid(),
                                                                      ts_spec_id,
                                                                      pro_reg_result_id,
                                                                      test_date)
            if pro_reg_result is not None:
                return_string = return_string +\
                                        self.get_test_result_string(pro_reg_result,
                                                                    'Regression')

            pro_vrm_result = HedgeUtils.get_time_series_dv_value_date(deal_package.Oid(),
                                                                      ts_spec_id,
                                                                      pro_vrm_result_id,
                                                                      test_date)
            if pro_vrm_result is not None:
                return_string = return_string + self.get_test_result_string(pro_vrm_result,
                                                                            'Prospective VRM')

            ret_vrm_result = HedgeUtils.get_time_series_dv_value_date(deal_package.Oid(),
                                                                      ts_spec_id,
                                                                      ret_vrm_result_id,
                                                                      test_date)

            if ret_vrm_result is not None:
                return_string = return_string +\
                                            self.get_test_result_string(ret_vrm_result,
                                                                        'Retrospective VRM')

            pro_ct_result = HedgeUtils.get_time_series_dv_value_date(deal_package.Oid(),
                                                                     ts_spec_id,
                                                                     pro_ct_result_id,
                                                                     test_date)

            if pro_ct_result is not None:
                return_string = return_string +\
                                            self.get_test_result_string(pro_ct_result,
                                                                        'Critical Terms')

            return_string = return_string + '\n%s\n\n' % end_string

        return return_string

    def get_test_result_string(self, result_value, text):
        return_string = ('%s: ' % text).ljust(35)
        if result_value == 1:
            result = 'Pass'
        elif result_value == 0:
            result = 'Fail'
        elif result_value == 2:
            result = 'Warning'
        else:
            result = ''
        return_string = return_string + result + '\n'
        return return_string

    def get_deal_package(self):
        '''Get the dealpackage details from hedgerelation xml
        '''

        dealPackageDetailsNodeList = HedgeAccountingStorage.get_elements(self.m_root,
                                                                         'dealPackageDetails')

        if dealPackageDetailsNodeList:
            # there should be only 1 in the list
            dealPackageDetailsNode = dealPackageDetailsNodeList[0]
            instrumentPackageName = HedgeAccountingStorage.\
                get_element_tag_value(dealPackageDetailsNode,
                                      'instrumentPackage')

            dealPackageName = HedgeAccountingStorage.get_element_tag_value(dealPackageDetailsNode,
                                                                           'activeDealPackage')

            return [instrumentPackageName, dealPackageName]

        return [None, None]

    def set_dealpackage(self, intrumentPackageName, dealPackageName):
        '''Set dealpackage details in hedgerelation xml
            instrumentPackage [string] -- name of InstrumentPackage
            dealPackage [string] -- name of the latest (Active) DealPackage
            holding the hedge trades
        '''

        # First remove all deal packages, then create new
        for item in HedgeAccountingStorage.get_elements(self.m_root, 'dealPackageDetails'):
            self.m_root.removeChild(item)

        # create dealPackage settings root
        dealPackageDetailsNode = self.m_xml.createElement('dealPackageDetails')
        self.m_root.appendChild(dealPackageDetailsNode)

        instrumentPackage = acm.FInstrumentPackage[intrumentPackageName]

        if instrumentPackage:
            # set instrument package
            instrumentPackageNode = self.m_xml.createElement('instrumentPackage')
            dealPackageDetailsNode.appendChild(instrumentPackageNode)
            HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                         dealPackageDetailsNode,
                                                         'instrumentPackage',
                                                         instrumentPackage.Name())

            # setup dealPackage structure - current & historic
            currentDealPackageNode = self.m_xml.createElement('activeDealPackage')
            dealPackageDetailsNode.appendChild(currentDealPackageNode)

            dealPackageHistoryNode = self.m_xml.createElement('dealPackageHistory')
            dealPackageDetailsNode.appendChild(dealPackageHistoryNode)

            for dealPackage in instrumentPackage.DealPackages():
                if dealPackage.OptionalId() == dealPackageName:
                    HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                                 dealPackageDetailsNode,
                                                                 'activeDealPackage',
                                                                 dealPackage.OptionalId())
                else:
                    HedgeAccountingStorage.append_element_with_value(self.m_xml,
                                                                     dealPackageHistoryNode,
                                                                     'dealPackageName',
                                                                     dealPackage.OptionalId())

    def get_trades(self):
        # Return dictionary of trades [oid] = [type, percent, childTradeOid]
        trades = {}

        for trade in HedgeAccountingStorage.get_elements(self.m_root, 'trade'):
            oid = HedgeAccountingStorage.get_element_tag_value(trade, 'oid')
            m_type = HedgeAccountingStorage.get_element_tag_value(trade, 'type')
            percent = HedgeAccountingStorage.get_element_tag_value(trade, 'percent')
            childTradeId = HedgeAccountingStorage.get_element_tag_value(trade, 'childTradeId')

            t = acm.FTrade[oid]
            if t:
                trades[oid] = [m_type, percent, childTradeId]

        return trades

    def set_trades(self, trades):
        # Expect a dictionary of trades [oid] = [type, percent, childTradeOid]

        # First remove all hedge trades, then create new
        for trade in HedgeAccountingStorage.get_elements(self.m_root, 'trade'):
            self.m_root.removeChild(trade)

        # Create new
        for oid in list(trades.keys()):
            [m_type, percent, childTradeId] = trades[oid]
            trade = self.m_xml.createElement('trade')
            self.m_root.appendChild(trade)
            HedgeAccountingStorage.set_element_tag_value(self.m_xml, trade, 'oid', oid)
            HedgeAccountingStorage.set_element_tag_value(self.m_xml, trade, 'type', m_type)
            HedgeAccountingStorage.set_element_tag_value(self.m_xml, trade, 'percent', percent)

            HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                         trade,
                                                         'childTradeId',
                                                         childTradeId)

    def GetReportData(self):
        result = {}
        trades = self.get_trades()
        for trdnbr in trades:
            trade = acm.FTrade[trdnbr]
            hedgetype, _ = trades[trdnbr]
            if hedgetype == 'Original':
                result['currency'] = trade.Instrument().Currency().Name()
                result['notional'] = trade.Nominal()
                result['bondISIN'] = trade.Instrument().Isin()
                result['bondName'] = trade.Instrument().Name()

                # field empty on trade
                if trade.Counterparty():
                    result['bondCounterparty'] = trade.Counterparty().Name()

            else:
                if trade.Counterparty():
                    result['irsCounterparty'] = trade.Counterparty().Name()
                else:
                    result['irsCounterparty'] = ''

        result['hedgeStartDate'] = self.get_start_date()
        result['hedgeEndDate'] = self.get_end_date()

        return result

    def get_test_settings(self):
        # Check if a template is used, or if the standalone ones should be used
        result = {}
        if self.get_template_name():
            template = HedgeTemplate.HedgeTemplate()
            template.set_id(self.get_template_name())
            template.read()
            result = template.get_test_settings()
        else:
            for testsettings in HedgeAccountingStorage.get_elements(self.m_root, 'testsettings'):
                for testNode in testsettings.childNodes:
                    settings = {}
                    for settingNode in testNode.childNodes:
                        settings[str(settingNode.tagName)] = HedgeAccountingStorage.\
                                                                get_element_tag_value(
                                                                    testNode,
                                                                    settingNode.tagName
                                                                )
                    result[str(testNode.tagName)] = settings
        self.m_testSettings = result
        return result

    def set_test_settings(self, settings):
        # Expect a dictionary of settings

        # First remove all test settings, then create new
        for testsetting in HedgeAccountingStorage.get_elements(self.m_root, 'testsettings'):
            self.m_root.removeChild(testsetting)

        testsettings = self.m_xml.createElement('testsettings')
        self.m_root.appendChild(testsettings)

        for test in list(settings.keys()):
            testnode = self.m_xml.createElement(test)
            testsettings.appendChild(testnode)
            for setting in list(settings[test].keys()):
                value = settings[test][setting]
                HedgeAccountingStorage.set_element_tag_value(self.m_xml, testnode, setting, value)
        self.m_testSettings = None
        self.get_test_settings()

    def get_days(self):
        try:
            testsettings = self.get_test_settings()
            return int(testsettings['General']['DaysBack'])
        except:
            return 32

    def get_template_name(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'templatename')

    def set_template_name(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'templatename',
                                                     value)

    def get_last_test_date(self):
        return HedgeAccountingStorage.get_element_tag_value(self.m_root, 'lasttestdate')

    def set_last_test_date(self, value):
        HedgeAccountingStorage.set_element_tag_value(self.m_xml,
                                                     self.m_root,
                                                     'lasttestdate',
                                                     value)

    def find_relation_for_trade(self, trade):
        result = []
        for filename in get_hedge_accounting_filenames():
            m_id = filename[3:]
            hedge_relation = HedgeRelation(m_id)
            hedge_relation.read()
            if str(trade.Oid()) in list(hedge_relation.get_trades().keys()):
                result.append(m_id)

        if not result:
            logger.WLOG('Unable to find existing Hedge Relation for Trade %d' % trade.Oid())
            return None
        if len(result) == 1:
            m_id = result[0]
            self.set_id(m_id)
            self.read()
            return True

        logger.WLOG('Found multiple Hedge Relations for Trade %d' % trade.Oid())
        logger.WLOG(result)
        return None

    def set_hedge_trades_accounting_flag(self, flag):
        trades = self.get_trades()
        spec = acm.FAdditionalInfoSpec['UseHedgeAccounting']
        for trdnbr in trades:
            t = acm.FTrade[trdnbr]
            if t:
                HedgeUtils.save_additional_info(spec, t, flag)

    def is_valid_hedge_relation(self):
        ''' Check if Hedge Relation is valid to perform tests:
            * At least 1 "Original" trade
            * At least 1 "External" trade
        '''

        trades = self.get_trades()
        hedges = []
        originals = []
        for trade in trades:
            if trades[trade][0] == 'Original':
                originals.append(trade)
            if trades[trade][0] == 'External':
                hedges.append(trade)

        if len(hedges) < 1 or len(originals) < 1:
            logger.WLOG('Not enough Original or External trades specified.')
            return False
        return True
