""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSSetUpAdditionalInfos.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSSetUpAdditionalInfos

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FAssetManagementUtils import logger

class SetUpAdditionalInfos(object):

    @classmethod
    def SetUp(cls):
        addInfos = cls.GetAddInfoSetUps()
        restart_needed = False
        for ai in addInfos:
            if not ai._GetExisting():
                ai._CreateNew()
                if ai._RestartNeeded():
                    restart_needed = True
        return restart_needed

    @classmethod
    def IsSetUp(cls):
        addInfos = cls.GetAddInfoSetUps()
        for ai in addInfos:
            if not ai._GetExisting():
                return False
        return True

    @staticmethod
    def GetAddInfoSetUps():

        setups = []

        setups.append(AddInfoSetUp( recordType='Party',
                                  fieldName='UCITSIssuerStatus',
                                  dataType='ChoiceList',
                                  description='UCITS_IssuerStatus',
                                  dataTypeGroup='RecordRef',
                                  subTypes=['Issuer', 'CounterParty'],
                                  defaultValue=None,
                                  mandatory=False ))

        setups.append(AddInfoSetUp( recordType='Party',
                                  fieldName='UCITSTotalDebt',
                                  dataType='Double',
                                  description='The total debt from the party, in the currency related to the country of risk of the party',
                                  dataTypeGroup='Standard',
                                  subTypes=['Issuer', 'CounterParty'],
                                  defaultValue=None,
                                  mandatory=False ))

        setups.append(AddInfoSetUp( recordType='Party',
                                  fieldName='UCITSUltimateIssuer',
                                  dataType='String',
                                  description='The ultimate issuer of the party, as string',
                                  dataTypeGroup='Standard',
                                  subTypes=['Issuer', 'CounterParty'],
                                  defaultValue=None,
                                  mandatory=False ))

        setups.append(AddInfoSetUp( recordType='Instrument',
                                  fieldName='UCITSVotingRights',
                                  dataType='Boolean',
                                  description='Does the stock give voting rights to the holder',
                                  dataTypeGroup='Standard',
                                  subTypes=['Stock'],
                                  defaultValue=None,
                                  mandatory=False ))

        setups.append(AddInfoSetUp( recordType='Instrument',
                                  fieldName='UCITSFundType',
                                  dataType='ChoiceList',
                                  description='UCITS_FundType',
                                  dataTypeGroup='RecordRef',
                                  subTypes=['Fund', 'ETF'],
                                  defaultValue=None,
                                  mandatory=False ))


        return setups



'''**************************************************************************
* AddInfoSetUp
**************************************************************************'''
class AddInfoSetUp(object):
    def __init__(self, recordType, fieldName, dataType, description, dataTypeGroup, subTypes, defaultValue, mandatory):
        self._recordType = recordType
        self._fieldName = fieldName
        self._dataType = dataType
        self._descr = description
        self._dataTypeGroup = dataTypeGroup
        self._defaultValue = defaultValue
        self._subTypes = subTypes
        self._dataTypeType = acm.GetDomain('enum(B92%sType)' % dataTypeGroup.replace('Ref', '')).Enumeration(dataType)
        self._mandatory = mandatory

    def _GetExisting(self):
        return acm.FAdditionalInfoSpec[self._fieldName]

    def _CreateNew(self):
        spec = acm.FAdditionalInfoSpec()
        spec.FieldName(self._fieldName)
        spec.DefaultValue(self._defaultValue)
        spec.Description(self._descr)
        spec.RecType(self._recordType)
        for subType in self._subTypes:
            spec.AddSubType(subType)
        spec.DataTypeGroup(self._dataTypeGroup)
        spec.DataTypeType(self._dataTypeType)
        spec.Mandatory(self._mandatory)
        spec.Commit()
        logger.DLOG('Created Additional info %s' % self._fieldName)

    def _RestartNeeded(self):
        restartNeeded = False
        method = self._fieldName.replace(' ', '_')
        if method and len(method):
            method = method[0].upper() + method[1:]
        if self._recordType == "Instrument" and self._subTypes:
            for subType in self._subTypes:
                klass = getattr(acm, 'F%sAdditionalInfo' % subType)
                if not acm.FSymbol(method) in [m.Name() for m in klass.AllMethods()]:
                    restartNeeded = True
        else:
            klass = getattr(acm, 'F%sAdditionalInfo' % self._recordType)
            if not acm.FSymbol(method) in [m.Name() for m in klass.AllMethods()]:
                restartNeeded = True
        return restartNeeded

    def Description(self):
        return 'Addinfo( %s )' % self._fieldName