import acm
import os
import struct
import sys
import platform
import traceback
import socket
import FOperationsUtils as Utils
from xml.etree import ElementTree


class ApexParams(object):
    def __init__(self):
        configurationName = 'ApexCollateral_Config_Settings'
        configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, configurationName)
        if configuration is None:
            Utils.Log(True, "Cannot find %s" % configurationName)
        configurationXML = ElementTree.fromstring(configuration)
        self.ModuleName = configurationXML.findall('.//ModuleName')[0].text
        self.Version = configurationXML.findall('.//ModuleVersion')[0].text
        self.BuildNumber = configurationXML.findall('.//BuildNumber')[0].text
        self.SupportedApexVersion = configurationXML.findall('.//SupportedApexVersion')[0].text
        Utils.Log(True, "%s Version: %s Build: %s Supported Apex Version: %s" % (self.ModuleName, self.Version, self.BuildNumber, self.SupportedApexVersion))
        common = configurationXML.findall('.//Common')[0]
        self.ErrorLogIdentifer = common.findall('.//ErrorLogIdentifer')[0].text
        self.BaseCurrency = common.findall('.//BaseCurrency')[0].text
        self.DefaultCalendar = common.findall('.//DefaultCalendar')[0].text
        self.Market = common.findall('.//Market')[0].text
        self.MessageSource = common.findall('.//MessageSource')[0].text
        self.MessageVersion = common.findall('.//MessageVersion')[0].text

        self.LatestSentMailsDurationInSec = int(common.findall('.//LatestSentMailsDurationInSec')[0].text)
        self.LatestSentMailsDepth = int(common.findall('.//LatestSentMailsDepth')[0].text)

        self.ExternalReferenceDelimiter = common.findall('.//ExternalReferenceDelimiter')[0].text
        self.CollateralCurrenciesStoredQuery = common.findall('.//CollateralCurrenciesStoredQuery')[0].text
        self.CollateralRateIndicesStoredQuery = common.findall('.//CollateralRateIndicesStoredQuery')[0].text
        self.CollateralBondInventoryTradesStoredQuery = common.findall('.//CollateralBondInventoryTradesStoredQuery')[0].text
        self.CollateralEquityInventoryTradesStoredQuery = common.findall('.//CollateralEquityInventoryTradesStoredQuery')[0].text
        self.CollateralBondInstrumentsStoredQuery = common.findall('.//CollateralBondInstrumentsStoredQuery')[0].text
        self.CollateralEquityInstrumentsStoredQuery = common.findall('.//CollateralEquityInstrumentsStoredQuery')[0].text
        self.SecurityCollateralPortfolio = common.findall('.//SecurityCollateralPortfolio')[0].text
        self.SecurityCollateralAcquirer = common.findall('.//SecurityCollateralAcquirer')[0].text
        self.SecurityCollateralTrader = common.findall('.//SecurityCollateralTrader')[0].text
        self.SecurityCollateralTradeStatus = common.findall('.//SecurityCollateralTradeStatus')[0].text
        self.CashCollateralPortfolio = common.findall('.//CashCollateralPortfolio')[0].text
        self.CashCollateralAcquirer = common.findall('.//CashCollateralAcquirer')[0].text
        self.CashCollateralTrader = common.findall('.//CashCollateralTrader')[0].text
        self.CashCollateralTradeStatus = common.findall('.//CashCollateralTradeStatus')[0].text

        self.ArenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort().lower()
        Utils.Log(True, "ArenaDataServer: %s" % self.ArenaDataServer)

        environment = None
        for element in configurationXML.findall('.//Environment'):
            if environment is not None:
                break
            for host in element.get('HostNames').split(';'):
                if host.lower() == socket.gethostname().lower():
                    environment = element
                    break

        if environment is None:
            Utils.Log(True, "No settings defined for %s" % socket.gethostname())
            raise Exception ("No settings defined for %s" % socket.gethostname())

        self.EnvironmentSettingName = environment.get('Name')

        self.AmbHost = environment.findall('.//AMBHost')[0].text
        Utils.Log(True, "AmbHost: %s" % self.AmbHost)
        self.AmbPort = environment.findall('.//AMBPort')[0].text
        Utils.Log(True, "AMBPort: %s" % self.AmbPort)
        self.ReceiverName = environment.findall('.//ReceiverName')[0].text
        Utils.Log(True, "ReceiverName: %s" % self.ReceiverName)
        self.ReceiverSource = environment.findall('.//ReceiverSource')[0].text
        Utils.Log(True, "ReceiverSource: %s" % self.ReceiverSource)

        self.MessageBroker = environment.findall('.//MessageBroker')[0].text
        Utils.Log(True, "MessageBroker: %s" % self.MessageBroker)

        self.TradeActivityQueueName = environment.findall('.//TradeActivityQueueName')[0].text
        self.BillingItemQueueName = environment.findall('.//BillingItemQueueName')[0].text
        self.PnLAccrualQueueName = environment.findall('.//PnLAccrualQueueName')[0].text
        self.ClientCommissionQueueName = environment.findall('.//ClientCommissionQueueName')[0].text
        self.PaymentInstructionQueueName = environment.findall('.//PaymentInstructionQueueName')[0].text
        self.AgreementQueueName = environment.findall('.//AgreementQueueName')[0].text
        self.BondPositionQueueName = environment.findall('.//BondPositionQueueName')[0].text
        self.EquityPositionQueueName = environment.findall('.//EquityPositionQueueName')[0].text
        self.TradeQueueName = environment.findall('.//TradeQueueName')[0].text
        self.BondPriceQueueName = environment.findall('.//BondPriceQueueName')[0].text
        self.EquityPriceQueueName = environment.findall('.//EquityPriceQueueName')[0].text
        self.FXRateQueueName = environment.findall('.//FXRateQueueName')[0].text
        self.IndexRateQueueName = environment.findall('.//IndexRateQueueName')[0].text
        self.BondSecurityQueueName = environment.findall('.//BondSecurityQueueName')[0].text
        self.EquitySecurityQueueName = environment.findall('.//EquitySecurityQueueName')[0].text

        if self.MessageBroker == "ActiveMQ":
            self.ActiveMQBrokerURL = environment.findall('.//ActiveMQBrokerURL')[0].text

        if self.MessageBroker == "WebSphereMQ":
            self.WebSphereMQQueueManager = environment.findall('.//WebSphereMQQueueManager')[0].text
            self.WebSphereMQChannel = environment.findall('.//WebSphereMQChannel')[0].text
            self.WebSphereMQHost = environment.findall('.//WebSphereMQHost')[0].text
            self.WebSphereMQPort = environment.findall('.//WebSphereMQPort')[0].text
            self.WebSphereChannelSecured = environment.findall('.//WebSphereChannelSecured')[0].text

        self.AppendPathElement = environment.findall('.//AppendPath')[0]
        if self.AppendPathElement is not None:
            Utils.Log(True, "AppendPath: %s" % self.AppendPathElement.text)
            sys.path.append(self.AppendPathElement.text)


        self.SleepTime = int(environment.findall('.//SleepTime')[0].text)

        self.EmailHost = environment.findall('.//EmailHost')[0].text
        self.EmailFrom = environment.findall('.//EmailFrom')[0].text
        self.EmailToTechnical = environment.findall('.//EmailToTechnical')[0].text
        self.EmailToFunctional = environment.findall('.//EmailToFunctional')[0].text

        Utils.Log(True, "%s Loaded" % configurationName)


def load():
    Utils.Log(True, "Loading %s" % __name__)
    Utils.Log(True, "Platform: %s" % (platform.platform()))
    Utils.Log(True, "Operating System: %s" % (os.name))
    Utils.Log(True, "Architecture: %sbit" % (struct.calcsize("P") * 8))
    try:
        return ApexParams()
    except Exception:
        traceback.print_exc()
