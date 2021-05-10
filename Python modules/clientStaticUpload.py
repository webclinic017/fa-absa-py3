'''
As per ABITFA-4841 - Client Service to FA Integration
Business requires the ability to obtain Party and Counterparty data from Client 
static, via the Client Static Service, and integrate it into Front Arena.

Operations requires the ability to check if a Party is an "Internal" type or not
as this affect the process used to settle trades/money_flows

The script below, requests the Client Service via a system user that was created, 
named: sysFAINTERNAL

The service uses NTLM Authentication, as such to run this code, a NTLM package is
required for the python environment this is executed in.

Information returned as "JSON" type (Which can be configured via the headers)

Initial Deployment - 2017-09-06

Date            Change            Developer                     Requester
==========      ===========       ==================            ======================
2017-09-06	ABITFA-4841       Kunal Maharaj/ Bhavik Mistry  Linda Breytenbach
								 
'''

from clientStaticServiceClasses import (ClientServicesRequest, ClientServiceMessageProcessor)
from at_logging import getLogger


LOGGER = getLogger("ClientStaticUpload")

ael_gui_parameters = { 'windowCaption':'Client static'}

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [ ('user', 'user: ', 'string', '', r'intranet\sysFAINTERNALS', 1, 0, 'user'),
                  ('password', 'password: ', 'string', '', '7G7pCTW*', 1, 0, 'password'),
                  ('front_id', 'Enter client ID (blank for all clients)', 'string', ['46062'], '46062', 0, 0, 'Single client ID'),
                  ('base_url', 'Client service URL: ', 'string', ['http://clientsvc-app:20111', 'http://clientsvc-app-uat:20111'], 
                   'http://clientsvc-app:20111', 1, 0, 'Client Static Environment type')]


def ael_main(parameter):
    user = parameter['user']
    password = parameter['password']
    base_url = parameter['base_url']
    front_id = parameter['front_id']

    front_id = '/' + front_id if front_id else front_id
    method_url = 'api/ClientSourceTypeAlias/Frontarena' + front_id

    client_services = ClientServicesRequest(user, password, base_url)
    client_services.authenticate_service()
    json_response = client_services.call_api(method_url)
    
    message_processor = ClientServiceMessageProcessor()
    message_processor.process(json_response)
    LOGGER.info('Completed Succesfully')
