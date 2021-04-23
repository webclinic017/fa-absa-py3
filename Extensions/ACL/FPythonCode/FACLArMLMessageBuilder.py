""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLArMLMessageBuilder.py"
import acm
import uuid
import xml.etree.ElementTree as ET
import datetime
import FACLAttributeMapper # for getCountryOfRisk
from FACLParameters import ConnectorATSSettings


class FACLArMLMessageBuilder:
    months=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']

    def __init__(self, useMarketPricesVersion = 1):
        if useMarketPricesVersion not in [1,2]:
            raise ValueError('useMarketPricesVersion can only be 1 or 2')
        self._useMarketPricesVersion=useMarketPricesVersion
        self._location = ''
        self._generatingSystem = 'FRONT ARENA'
        self._systemID = 'FACL'

    def CreateMtM(self, params):
        root = self._createRootElement()
        header = self._createMessageHeaderElement()
        root.append(header)
        request =  self._createRequestElement('Deal.PostUpdates')
        param = self._createParamElement('Deal')
        request.append(param)
        entity = ET.SubElement(param, 'Deal')
        adminHeader = ET.SubElement(entity, 'DealHeader')
        ET.SubElement(adminHeader, 'Ref').text = params['Reference']
        dealAttributes = ET.SubElement(entity, 'DealAttributes')

        attrib = ET.SubElement(dealAttributes, 'Attribute')
        ET.SubElement(attrib, 'Name').text = 'Replacement Value'
        valueElement = ET.SubElement(attrib, 'Value')

        replacementValue = self._createReplacementValueElement(params['Replacement Value'])
        valueElement.append(replacementValue)        

        root.append(request)
        return self._getAsXML(root)

    def CreateMarketPrice(self, params):    
        return self._CreateRequestAdminBase(params, 'AssetSecurity', 'Admin.Push', None)

    def CreateRequestDealAdd(self, params, confirmationRequired = True):
        actionFlags = ['VerboseSnapshot']
        if confirmationRequired:
            actionFlags.append('ConfirmRequired')
        return self._CreateRequestDealBase(params, 'Deal.Add', actionFlags)
        
    def CreateRequestDealModify(self, params, confirmationRequired = True):
        actionFlags = ['VerboseSnapshot']
        if confirmationRequired:
            actionFlags.append('ConfirmRequired')
        return self._CreateRequestDealBase(params, 'Deal.Modify', actionFlags)
    
    def CreateRequestDealConfirm(self, params):
        return self._CreateRequestDealBase(params, 'Deal.Confirm', None)

    def CreateRequestDealChangeReference(self, currentReference, params):
        root = self._createRootElement()
        header = self._createMessageHeaderElement()
        root.append(header)

        req = self._createRequestElement('Deal.ChangeReference')
        
        newReference = params['Reference']        
        param = self._createParamElement('Old Reference', '0')
        p = dict(params)
        p['Reference'] = currentReference
        deal = self._createDealElement(p, includeAttributes = False)
        param.append(deal)
        req.append(param)

        param = self._createParamElement('New Reference', '1')
        p = dict(params)
        p['Reference'] = newReference
        deal = self._createDealElement(p, includeAttributes = False)
        param.append(deal)
        req.append(param)
        
        root.append(req)
        
        return self._getAsXML(root)
    
    def CreateRequestDealReject(self, params):
        return self._CreateRequestDealBase(params, 'Deal.Reject', None)

    def CreateRequestDealReverse(self, params):
        return self._CreateRequestDealBase(params, 'Deal.Reverse', None)
        
    def CreateRequestDealAvailability(self, params):
        if 'Replacement Value' in params:
            params = params.copy()
            del params['Replacement Value']
        return self._CreateRequestDealBase(params, 'Deal.Availability', None)
    
    def CreatePing(self, params={ 'ClientDate' : 'T', 'Attempts' : '0', 'Successes' : '0' }):
        root = self._createRootElement()
        header = self._createMessageHeaderElement()
        root.append(header)

        req = self._createRequestElement('Deal.Ping')                
        param = self._createParamElement('Ping')
        
        p = dict(params)                
        ping = self._createPingElement(p)
        param.append(ping)
        req.append(param)
        
        root.append(req)
        
        return self._getAsXML(root)
        
    def CreateAddTrialCheck(self, params):
        return self._CreateRequestDealBase(params, 'Deal.Add', ['TRIALCHECK', 'VerboseSnapshot'])
    
    def CreateModifyTrialCheck(self, params):
        return self._CreateRequestDealBase(params, 'Deal.Modify', ['TRIALCHECK', 'VerboseSnapshot'])
    
    def CreateGivePermission(self):
        acquirers = [ str(x.FACLgetReference()) for x in acm.FParty.Select("type='Intern Dept'") if FACLAttributeMapper.getCountryOfRisk(x) != None ]
        
        params = {        
            'Reference' : ConnectorATSSettings.windowsUserName,
            'Security Rights\Branches' : acquirers,
            'Type' : 'User\User'
        }    

        return self._CreateRequestAdminBase(params, 'UserSecurity', 'Admin.Push', None)
    
    def CreateCounterparty(self, params):
        return self._CreateRequestAdminBase(params, 'Customer', 'Admin.Push', None)
    
    def CreateInstrument(self, params):
        return self._CreateRequestAdminBase(params, 'Asset', 'Admin.Push', None)
    
    def _CreateRequestDealBase(self, params, action = 'Deal.Add', actionFlags = None):
        root = self._createRootElement()
        header = self._createMessageHeaderElement()
        root.append(header)
        req = self._createRequestDealElement(params, action, actionFlags)
        root.append(req)
        return self._getAsXML(root)
    
    def _CreateRequestAdminBase(self, params, paramName, action = 'Admin.Push', actionFlags = None):
        root = self._createRootElement()
        header = self._createMessageHeaderElement()
        root.append(header)
        req = self._createRequestAdminElement(params, paramName, action, actionFlags)
        root.append(req)
        return self._getAsXML(root)

    def _getAsXML(self,root):
        return ET.tostring(root, encoding='UTF-8')

    def _createRootElement(self):
        root = ET.Element('ArMessage')
        root.set('xmlns','http://www.sungard.com/Adaptiv/Crs/Schema')
        return root
    
    def _createMessageHeaderElement(self):
        
        head = ET.Element('MsgHeader')
        ET.SubElement(head, 'MessageID').text = str(uuid.uuid4())
        source = ET.SubElement(head, 'MessageSource')
        ET.SubElement(source, 'SystemID').text = self._systemID
        ET.SubElement(source, 'Location').text = self._location
        ET.SubElement(head, 'CorrelationID').text = str(uuid.uuid4())
        ET.SubElement(head, 'TimeZone').text = self._getTimeZone()
        ET.SubElement(head, 'DateTimeForm').text = 'CRS'
        ET.SubElement(head, 'GeneratedTime').text = datetime.datetime.today().strftime('%d%b%Y %H:%M:%S').upper()
        ET.SubElement(head, 'Acknowledge').text = 'false'
        
        return head
    
    def _createFlags(self, parentElement, actionFlags):
        if actionFlags:
            actionFlagselement = ET.SubElement(parentElement, 'ActionFlags')
            
            for flag in actionFlags:
                ET.SubElement(actionFlagselement, 'Flag').text = flag
        
    def _createRequestDealElement(self, params, action = 'Deal.Add', actionFlags = None, responseRequired = 'Yes'):
        req = self._createRequestElement(action, actionFlags, responseRequired)
        param = self._createParamElement('Deal')
        includeAttributes = action not in ['Deal.Reject', 'Deal.Reverse', 'Deal.ChangeReference']
        deal = self._createDealElement(params, includeAttributes)
        param.append(deal)
        req.append(param)
        
        return req
    
    def _createRequestAdminElement(self, params, paramName, action = 'Admin.Push', actionFlags = None, responseRequired = 'Yes'):
        req = self._createRequestElement(action, actionFlags, responseRequired)
        param = self._createParamElement(paramName)
        deal = self._createAdminEntityElement(params)
        param.append(deal)
        req.append(param)
        
        return req
    
    def _createDealElement(self, paramsOriginal, includeAttributes = True):
        params = paramsOriginal.copy()
        deal = ET.Element('Deal')
        reference = params.pop('Reference') if params.has_key('Reference') else ''
        product = params.pop('Product') if params.has_key('Product') else ''
        branch = params['Booking Branch'] if params.has_key('Booking Branch') else ''
        comments = params.pop('Comments') if params.has_key('Comments') else ''

        dealHeader = self._createDealHeaderElement(reference, product, [branch], comments) 
        deal.append(dealHeader)
        if includeAttributes and len(params) > 0:
            dealAttributes = self._createAttributes('DealAttributes', params)
            deal.append(dealAttributes)
        
        return deal
    
    def _createResponseDataCounter(self, parent, name):        
        head = ET.SubElement(parent, name)
        
        for counter in range(1, 16):
            ET.SubElement(head, 'Counter').set('Value', str(counter))
        
        return head
    
    def _createPingElement(self, paramsOriginal):
        params = paramsOriginal.copy()
        ping = ET.Element('Ping')

        pingHeader = self._createPingHeaderElement() 
        ping.append(pingHeader)
        if len(params) > 0:
            pingAttributes = self._createAttributes('PingAttributes', params)
            
            attrib = ET.Element('Attribute')
            name = ET.SubElement(attrib, 'Name').text = 'ResponseData'
            value = ET.SubElement(attrib, 'Value')
            responseData = ET.SubElement(value, 'ResponseData')
            self._createResponseDataCounter(responseData, 'Deal')
            self._createResponseDataCounter(responseData, 'Avail')
            self._createResponseDataCounter(responseData, 'Trial')
            
            pingAttributes.append(attrib) 
            ping.append(pingAttributes)
                    
        return ping

    def _createAdminEntityElement(self, paramsOriginal):
        params = paramsOriginal.copy()
        admin = ET.Element('AdminEntity')

        reference = params.pop('Reference') if params.has_key('Reference') else ''
        type = params.pop('Type') if params.has_key('Type') else ''
        adminHeader = self._createAdminHeaderElement(reference, type) 
        admin.append(adminHeader)
        adminAttributes = self._createAttributes('AdminAttributes', params)
        admin.append(adminAttributes)
        
        return admin
        
    def _createRequestElement(self, action, actionFlags = None, responseRequired = 'Yes'):
        reqId = str(uuid.uuid4())
        req = ET.Element('Request')
        reqHeader = self._createRequestHeaderElement(action, reqId, actionFlags, responseRequired) 
        req.append(reqHeader)
        
        return req

    def _createCurrencyRequest(self, currencyName, rate, updateDate):
        request = self._createRequestElement('Admin.Push',None,'Yes')
        param = self._createParamElement('Asset')
        request.append(param)
        entity = ET.SubElement(param, 'AdminEntity')
        adminHeader = ET.SubElement(entity, 'AdminHeader')
        ET.SubElement(adminHeader, 'Ref').text = currencyName
        ET.SubElement(adminHeader, 'Type').text = 'Currency\Currency'
        adminAttributes = ET.SubElement(entity, 'AdminAttributes')
        adminAttributes.append(self._createAttributeElement(['Market Data\Spot Rate', self._floatToACR(rate)]))
        adminAttributes.append(self._createAttributeElement(['Market Data\Show Spot As Reciprocal', 'No']))
        adminAttributes.append(self._createAttributeElement(['Information\Fixing Date', updateDate]))
        return request

    def _createRequestHeaderElement(self, action, reqId, actionFlags, responseRequired):
        if responseRequired not in ['Yes','No']:
            raise ValueError('responseRequired should either be Yes or No')
        header = ET.Element('RequestHeader')
        ET.SubElement(header, 'RequestID').text = str(reqId)            
        ET.SubElement(header, 'Action').text = action
        self._createFlags(header, actionFlags)
        ET.SubElement(header, 'ResponseRequired').text = str(responseRequired)
        
        return header
    
    def _createDealHeaderElement(self, ref, prod, branches, comments):
        dealHeader = ET.Element('DealHeader')
        ET.SubElement(dealHeader, 'Ref').text = str(ref) if ref else ''
        ET.SubElement(dealHeader, 'Product').text = str(prod)
        
        if branches:
            branchElement = ET.SubElement(dealHeader, 'Branches')
            for b in branches:
                ET.SubElement(branchElement, 'Branch').text = str(b)

        ET.SubElement(dealHeader, 'Comments').text = str(comments) if comments else ''
                
        return dealHeader
    
    def _createPingHeaderElement(self, machineName=''):
        pingHeader = ET.Element('PingHeader')
        ET.SubElement(pingHeader, 'MachineName').text = machineName                
        return pingHeader

    def _createAdminHeaderElement(self, ref, adminType, branches = []):
        adminHeader = ET.Element('AdminHeader')
        ET.SubElement(adminHeader, 'Ref').text = str(ref)
        if adminType:
            ET.SubElement(adminHeader, 'Type').text = str(adminType)
        
        if branches:
            branchElement = ET.SubElement(adminHeader, 'Branches')
            for b in branches:
                ET.SubElement(branchElement, 'Branch').text = str(b)
                
        return adminHeader
    
    def _createAttributes(self, name, params):
        attributes = ET.Element(name)
        for att in params.items():
            attributes.append(self._createAttributeElement(att))
        return attributes
            
    def _createAttributeElement(self, att):
        attrib = ET.Element('Attribute')
        ET.SubElement(attrib, 'Name').text = str(att[0])
        attribValueElement = self._createAttributeValueElement(att[0], att[1])
        attrib.append(attribValueElement)
        
        return attrib
            
    def _createAttrList(self, list):
        res = ET.Element('List')
        
        for e in list:
            item = ET.Element('Item')
            attr = ET.Element('Attr')
            attr.text = e
            item.append(attr)
            res.append(item)
                
        return res
            
    def _createAttributeValueElement(self, valueName, value):
        valueElement = ET.Element('Value') 
        
        if valueName == 'Replacement Value':
            replacementValue = self._createReplacementValueElement(value)
            valueElement.append(replacementValue)
        elif not isinstance(value, str):
            list = self._createAttrList(value)
            valueElement.append(list)
            return valueElement        
        else:
            valueElement.text = value
        
        return valueElement
            
    def _createReplacementValueElement(self, values):
        riskValue = ET.Element('RiskValue')
        header = ET.SubElement(riskValue, 'Header')
        
        ET.SubElement(header, 'RiskAttributeName').text = 'Replacement Value'
        ET.SubElement(header, 'Type').text = 'rvhSingle'
        ET.SubElement(header, 'GeneratingSystem').text = self._generatingSystem
        ET.SubElement(header, 'CalculatedDate').text = values['CalculatedDate']
        ET.SubElement(header, 'ExpiryDate').text = ''
        ET.SubElement(header, 'IsActive').text = 'true'
        ET.SubElement(header, 'AssetCode').text = values['AssetCode']
        ET.SubElement(riskValue, 'SingleValue').text = values['SingleValue']
        
        return riskValue
    
    def _createParamElement(self, name, seq = '0'):
        param = ET.Element('Param')
        param.set('Name', name)
        param.set('Seq', seq)
        
        return param
        
    def _floatToACR(self, d):
        return '{0:f}'.format(d)

    def _getTimeZone(self):
        toReturn = 'GMT'
        delta = datetime.datetime.now() - datetime.datetime.utcnow()
        
        if abs(delta.seconds) >= 60:
            if delta.seconds > 0:
                toReturn += '+'
            else:
                toReturn += '-'
            
            hours, remainder = divmod(abs(delta.seconds), 3600)
            minutes, remainder = divmod(remainder, 60)
            
            toReturn += '%02d:%02d' % (hours, minutes) 
        
        return toReturn
