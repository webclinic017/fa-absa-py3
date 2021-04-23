from __future__ import print_function
""" Module that handles the runscript for downloading ECB currency rates """
import ael
import acm
import FRunScriptGUI
from ECBRatesDownloadRates import StartDownload
from ECBRatesDownloadRates import ReadXMLFile
from ECBRatesDownloadRates import LoadFromFile
from ECBRatesPopulatePriceEntry import PopulatePriceEntry
import ECBHttp

class ECBRatesDownloader(FRunScriptGUI.AelVariablesHandler):
    def __UpdateProxyFlds(self, index, fieldValues):
        useAutoProxy = fieldValues[index]

        proxyFlds = [self.proxyAddr, self.proxyPort, self.proxyUserName, self.proxyPass]
        for fld in proxyFlds:
            fld.enable(useAutoProxy != 'true')
        return fieldValues

    def __DisplayCurrWrng(self, index, fieldValues):
        addCurr = fieldValues[index]
        if addCurr == 'true':
            sessMan = acm.UX().SessionManager()
            shell = sessMan.Shell()
            for app in sessMan.RunningApplications():
                if app.AsString() == "'ECBRatesRunscript - Run Script'":
                    shell = app.Shell()
                    break
            retVal = acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Warning', 'Currencies cretated with this script must be manually managed since they only use a template currency.')
            if retVal == 'Button2':
                self.createCurr.set(fieldValues, False)
            return fieldValues

    def __UseFile(self, index, fieldValues):
        sourceType = fieldValues[index]
        if sourceType == 'Proxy':
            proxy = True
        else : #if sourceType == 'File':
            proxy = False
        self.file.enable(not proxy)
        self.autoProxy.enable(proxy)
        if proxy:
            self.autoProxy.set(fieldValues, True)
        proxyFlds = [self.proxyAddr, self.proxyPort, self.proxyUserName, self.proxyPass]
        for fld in proxyFlds:
            fld.enable(False)
        return fieldValues

    def __init__(self):
        variables = [
            ['createCurr', 'Create currencies that do not exist', 'bool', [False, True], False, 0, 0, 'WARNING! Currencies created must be manually managed as they only use a template currency.', self.__DisplayCurrWrng, 1],
            ['histRates', 'Add historical FX rates (90 days)', 'bool', [False, True], False, 0, 0, '', None, 1],
            ['overwrite', 'Overwrite existing prices', 'bool', [False, True], False, 0, 0, 'If a certain price already exists it will not be overwritten.', None, 1],
            ['sourceType', 'Select source type_Source', 'string', ['Proxy', 'File'], 'Proxy', 1, 0, '', self.__UseFile, 1],
            ['file', 'Enter path to file_Source', 'string', None, '', 0, 0, '', None, 1],
            ['autoProxy', 'Auto detect proxy_Source', 'bool', [False, True], True, 0, 0, 'Detect proxy settings automatically', self.__UpdateProxyFlds, 1],
            ['proxyAddr', 'Proxy Address_Source', 'string', None, None, 1, 0, 'Does not support NTLM proxies', None, 1],
            ['proxyPort', 'Proxy Port_Source', 'int', None, None, 1, 0, '', None, 1],
            ['proxyUserName', 'Proxy user name_Source', 'string', None, '', 0, 0, '', None, 1],
            ['proxyPass', 'Proxy password_Source', 'string', None, '', 0, 0, '', None, 1]
        ]
        FRunScriptGUI.AelVariablesHandler.__init__(self, variables)

ael_variables = ECBRatesDownloader()

def ael_main(dict): #ael_main_ex(dict,data):
    webHost = ('www.ecb.europa.eu', 443)
    address = '/stats/eurofxref/eurofxref-daily.xml'
    histAddr = '/stats/eurofxref/eurofxref-hist-90d.xml'

    addHistRates = False
    createCurr = False
    overwrite = False
    if dict['createCurr'] == 1:
        createCurr = True
    if dict['histRates'] == 1:
        address = histAddr
        addHistRates = True
    if dict['overwrite'] == 1:
        overwrite = True

    proxy = False
    if dict['sourceType'] == 'Proxy':
        proxy = True

    if not proxy: #Download from file
        filePath = dict['file']
        xmldoc = LoadFromFile(filePath)
    elif proxy:
        if dict['autoProxy']:
           xmldoc = ECBHttp.HTTPAutoProxyGetRequest("Prime", "HTTP/1.1", webHost[0], address)
        else:
            proxy_addr = dict['proxyAddr']
            proxy_port = dict['proxyPort']

            proxy = (proxy_addr, proxy_port)

            proxy_user = dict['proxyUserName']
            proxy_pass = dict['proxyPass']
            proxy_cred = None
            if proxy_user and proxy_pass:
                proxy_cred = (proxy_user, proxy_pass)
            xmldoc = StartDownload(webHost, address, proxy, proxy_cred)

    if xmldoc == None:
        if not proxy:
            print ("Invalid file path entered. Check path and file type.")
        else:
            print ("Could not receive document")
        return

    fxDict = ReadXMLFile(xmldoc)
    for day in fxDict:
        PopulatePriceEntry(day, fxDict[day], createCurr, addHistRates, overwrite)
