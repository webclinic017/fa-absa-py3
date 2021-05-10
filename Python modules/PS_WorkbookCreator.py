"""
Facilitates the creation of workbooks for the PB new client setup.

The module is meant to be temporary, until FWorksheetReport works correctly
(currently, adding content to a CashAnalysis sheet doesn't work).

"""

import base64
import zlib

import acm

from at_logging import getLogger
from Transporters import FWorkbookTransporter


__all__ = ['setup_workbooks']
LOGGER = getLogger()


def workbook_exists(wbk_name):
    if acm.FWorkbook.Select01('name="%s" user="ATS"' % wbk_name, None) is not None:
        return True
    return False


def create_cash_analysis_wbk(config):
    """
    Creates the cash analysis workbook.

    Currently, this is rather a hack - to be removed once the
    FWorksheetReport is repaired.

    """
    wbk_name = tradefilter_name = 'PB_CashAnalysis_%s' % config['shortName']

    if workbook_exists(wbk_name):
        LOGGER.info("Workbook {} already exists".format(wbk_name))
        return

    tradingsheet_params = {
        'tradefilter_name': tradefilter_name,
    }
    tradingsheet_str = CASH_ANALYSIS_TRADINGSHEET_DATA % tradingsheet_params
    tradingsheet_data = base64.encodestring(zlib.compress(tradingsheet_str))
    wbk_params = {
        'wbk_name': wbk_name,
        'tradingsheet_data': tradingsheet_data,
    }
    workbook_str = CASH_ANALYSIS_WORKBOOK % wbk_params
    transporter = FWorkbookTransporter(owner=acm.FUser['ATS'])
    transporter.ImportSingle({}, wbk_name, workbook_str)


def create_onboarding_trades_wbk(config):
    """
    Creates the onboarding trades workbook.
    """
    wbk_name = tradefilter_name = 'PB_Onb_tr_%s' % config['shortName']

    if workbook_exists(wbk_name):
        LOGGER.info("Workbook {} already exists".format(wbk_name))
        return

    tradingsheet_params = {
        'tradefilter_name': tradefilter_name,
    }
    tradingsheet_str = ONBOARDING_TRADES_TRADINGSHEET_DATA % tradingsheet_params
    tradingsheet_data = base64.encodestring(zlib.compress(tradingsheet_str))
    wbk_params = {
        'wbk_name': wbk_name,
        'tradingsheet_data': tradingsheet_data,
    }
    workbook_str = ONBOARDING_TRADES_WORKBOOK % wbk_params
    transporter = FWorkbookTransporter(owner=acm.FUser['ATS'])
    transporter.ImportSingle({}, wbk_name, workbook_str)


## Main body.

def setup_workbooks(config):
    """
    Create workbooks for the new PB client.

    <config> is the ael_variables instance from PS_MO_Onboarding.

    """
    workbooks = (
        ('CashAnalysis', create_cash_analysis_wbk),
    )
    for description, setup_func in workbooks:
        LOGGER.info('Creating the %s workbook ...', description)
        if config['dryRun']:
            LOGGER.warning('Skipping the actual creation according to the Dry Run setting.')
            continue
        try:
            setup_func(config)
        except Exception as e:
            LOGGER.exception("Could not commit workbook {}".format(description))
            raise e
        LOGGER.info('Done')


CASH_ANALYSIS_WORKBOOK = """<?xml version='1.0' encoding='ISO-8859-1'?>
  <FWorkbook>
    <acm_version>2013.3, Jun 13 2013</acm_version>
    <version>0 $Id$</version>
    <update_time>2013-06-28 12:11:29</update_time>
    <object_name>%(wbk_name)s</object_name>
    <owner>ATS</owner>
    <protection>3072</protection>
    <type>FWorkbook</type>
    <FTradingSheet>
        <type>FMoneyFlowSheet</type>
        <data>%(tradingsheet_data)s</data>
    </FTradingSheet>
</FWorkbook>
"""


CASH_ANALYSIS_TRADINGSHEET_DATA = """<?xml version='1.0' encoding='ISO-8859-1'?>
<FrontArenaPrimeSheetExport>
<!--PRIME Version: 2014.4.8-->
<FPersistentArchive type ="AcmDomain">
  <ArchiveContents type ="Property">
    <FDictionary type ="AcmDomain">
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">columncreators</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FColumnCreators type ="AcmDomain">
            <creators type ="Property">
              <FArray type ="AcmDomain">
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">d65d36ec-3a06-4c22-9caf-c1aefc60d7d5</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Instrument</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">54cb59c5-82c2-4bf8-9594-8edbdfe54941</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Type</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">41bdb577-0d7b-48bb-bb7b-945b47900f39</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Currency</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">a9f05a98-d2b2-4732-9a38-80151ec44b63</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Start Date</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">86d1e842-76ce-47a1-add5-1b7660264493</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis End Date</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">4f109f9b-091a-462b-8665-b274b2deaa23</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Period Days</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">e3c8e14a-2f14-4710-9f63-551a0599bc53</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Pay Day</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">a9507de6-3e01-4d84-bf67-b0c41abf42b3</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Forward Rate</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">fbc506ba-922e-45ad-8aea-428c16402067</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Projected</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">754d1fc1-e5c9-402d-90af-fb60032e4c67</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Portfolio Theoretical Value</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">a537edbc-360a-4001-bece-d8691546a99e</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis PS Deposit Type</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FMethodColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">69eb0bc8-f664-4eed-8e59-e6b1794e5091</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FMethodColumnCreatorTemplate type ="AcmDomain">
                      <category type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">MoneyFlow</string>
                          </Text>
                        </FSymbol>
                      </category>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                      <method type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">CashFlow.AdditionalInfo.PS_Descriptor</string>
                          </Text>
                        </FSymbol>
                      </method>
                      <subjectClass type ="Property">
                        <FDomain type ="AcmDomain">
                          <DomainName type ="Property">
                            <string type ="AcmDomain">FMoneyFlow</string>
                          </DomainName>
                        </FDomain>
                      </subjectClass>
                    </FMethodColumnCreatorTemplate>
                  </creatorTemplate>
                </FMethodColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">15f10251-3d61-46e4-ab6e-0832c823421e</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis PS Cash Type</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">eaf29bbe-acbe-412c-823b-79a202c4178f</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis PS Cash Type Portfolio</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">eb98c669-1324-456d-82e3-ae58c7e56b60</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis PS Instrument Type</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">1a7347f8-3ff7-4f22-b857-fc678595fdf8</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Prevent Settlement</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">d7b4aac8-629a-49f4-8a03-0b6c52a21d5a</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Cash Flow Number</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">c7272301-36ef-4b42-b7de-85797cb8512e</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Counterparty</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">4906f2de-4c8c-4d5d-a6e3-37073fffcc0f</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Cash Analysis Trade Number</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
              </FArray>
            </creators>
            <headerColWidth type ="Property">
              <int type ="AcmDomain">291</int>
            </headerColWidth>
          </FColumnCreators>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">columnsettings</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FDictionary type ="AcmDomain">
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Cash Flow Number-d7b4aac8-629a-49f4-8a03-0b6c52a21d5a</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">1</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">103</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Counterparty-c7272301-36ef-4b42-b7de-85797cb8512e</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">141</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Currency-41bdb577-0d7b-48bb-bb7b-945b47900f39</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">1</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">55</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis End Date-86d1e842-76ce-47a1-add5-1b7660264493</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">1</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">62</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Forward Rate-a9507de6-3e01-4d84-bf67-b0c41abf42b3</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">1</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">80</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Instrument-d65d36ec-3a06-4c22-9caf-c1aefc60d7d5</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">1</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">107</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Pay Day-e3c8e14a-2f14-4710-9f63-551a0599bc53</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">customLabel</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">Pay Date</string>
                        </Text>
                      </FSymbol>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">62</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Period Days-4f109f9b-091a-462b-8665-b274b2deaa23</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">1</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">69</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Prevent Settlement-1a7347f8-3ff7-4f22-b857-fc678595fdf8</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">113</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Projected-fbc506ba-922e-45ad-8aea-428c16402067</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">customLabel</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">Projected Cash</string>
                        </Text>
                      </FSymbol>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">90</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis PS Cash Type Portfolio-eaf29bbe-acbe-412c-823b-79a202c4178f</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">customLabel</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">PSwap Cash Type Portfolio</string>
                        </Text>
                      </FSymbol>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">185</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis PS Cash Type-15f10251-3d61-46e4-ab6e-0832c823421e</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">customLabel</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">PSwap Cash Type</string>
                        </Text>
                      </FSymbol>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">147</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis PS Deposit Type-a537edbc-360a-4001-bece-d8691546a99e</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">78</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis PS Instrument Type-eb98c669-1324-456d-82e3-ae58c7e56b60</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">customLabel</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">PSwap Instrument Type</string>
                        </Text>
                      </FSymbol>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">173</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Start Date-a9f05a98-d2b2-4732-9a38-80151ec44b63</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">1</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">62</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Trade Number-4906f2de-4c8c-4d5d-a6e3-37073fffcc0f</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">1</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">130</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Cash Analysis Type-54cb59c5-82c2-4bf8-9594-8edbdfe54941</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">customLabel</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">Action Type</string>
                        </Text>
                      </FSymbol>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">131</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">CashFlow.AdditionalInfo.PS_Descriptor-69eb0bc8-f664-4eed-8e59-e6b1794e5091</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">75</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Portfolio Theoretical Value-754d1fc1-e5c9-402d-90af-fb60032e4c67</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">label</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">2</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">78</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
          </FDictionary>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">frzcol</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">gridBuilderContents</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FDictionary type ="AcmDomain">
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">scenarioManager</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
          </FDictionary>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">grplbl</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FTrue type ="AcmDomain">
          </FTrue>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">gryinv</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">inihdc</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">inslab</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">Name</string>
            </Text>
          </FSymbol>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">isCalculateCellsOutOfViewEnabled</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FFalse type ="AcmDomain">
          </FFalse>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">isCellContentSuppressed</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FFalse type ="AcmDomain">
          </FFalse>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">isDistributedProcessingEnabled</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FFalse type ="AcmDomain">
          </FFalse>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">leftcol</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">Cash Analysis Instrument-d65d36ec-3a06-4c22-9caf-c1aefc60d7d5</string>
            </Text>
          </FSymbol>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">manrfr</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">moneyFlowFromToDatePair</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FPair type ="AcmDomain">
            <first type ="Property">
              <FString type ="AcmDomain">
                <Text type ="Property">
                  <string type ="AcmDomain">-35d</string>
                </Text>
              </FString>
            </first>
            <second type ="Property">
              <FString type ="AcmDomain">
                <Text type ="Property">
                  <string type ="AcmDomain"></string>
                </Text>
              </FString>
            </second>
          </FPair>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">moneyFlowSettlementTypes</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FArray type ="AcmDomain">
          </FArray>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">pgsetup</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FString type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">94 71 94 71 100 p</string>
            </Text>
          </FString>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">rfrper</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">rows</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FGuiTree type ="AcmDomain">
            <item type ="Property">
              <FSymbol type ="AcmDomain">
                <Text type ="Property">
                  <string type ="AcmDomain">DummyRoot</string>
                </Text>
              </FSymbol>
            </item>
            <Element>
            <FGuiTree type ="AcmDomain">
              <item type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Root</string>
                  </Text>
                </FSymbol>
              </item>
              <treeId type ="Property">
                <int type ="AcmDomain">10</int>
              </treeId>
              <Element>
              <FLocalBuiltTree type ="AcmDomain">
                <treeId type ="Property">
                  <int type ="AcmDomain">9</int>
                </treeId>
                <builder type ="Property">
                  <FMoneyFlowAndTradesBuilder type ="AcmDomain">
                    <treeConfiguration type ="Property">
                      <FTreeConfiguration type ="AcmDomain">
                        <treeSpecification type ="Property">
                          <FTreeSpecification type ="AcmDomain">
                            <groupingSubjectClass type ="Property">
                              <FDomain type ="AcmDomain">
                                <DomainName type ="Property">
                                  <string type ="AcmDomain">FMoneyFlowGrouperSubject</string>
                                </DomainName>
                              </FDomain>
                            </groupingSubjectClass>
                            <originObject type ="Property">
                              <FPersistent type ="AcmDomain">
                                <Class type ="Property">
                                  <FDomain type ="AcmDomain">
                                    <DomainName type ="Property">
                                      <string type ="AcmDomain">FTradeSelection</string>
                                    </DomainName>
                                  </FDomain>
                                </Class>
                                <ExternalReference type ="Property">
                                  <FVariantDictionary type ="AcmDomain">
                                    <Element>
                                    <FAssociation type ="AcmDomain">
                                      <associationKey type ="Property">
                                        <FSymbol type ="AcmDomain">
                                          <Text type ="Property">
                                            <string type ="AcmDomain">Name</string>
                                          </Text>
                                        </FSymbol>
                                      </associationKey>
                                      <associationValue type ="Property">
                                        <FString type ="AcmDomain">
                                          <Text type ="Property">
                                            <string type ="AcmDomain">%(tradefilter_name)s</string>
                                          </Text>
                                        </FString>
                                      </associationValue>
                                    </FAssociation>
                                    </Element>
                                  </FVariantDictionary>
                                </ExternalReference>
                              </FPersistent>
                            </originObject>
                            <grouper type ="Property">
                              <FDefaultGrouper type ="AcmDomain">
                                <split type ="Property">
                                  <bool type ="AcmDomain">false</bool>
                                </split>
                              </FDefaultGrouper>
                            </grouper>
                          </FTreeSpecification>
                        </treeSpecification>
                        <visibilityOptions type ="Property">
                          <FTreeVisibilityOptions type ="AcmDomain">
                            <includeSingleInstruments type ="Property">
                              <bool type ="AcmDomain">true</bool>
                            </includeSingleInstruments>
                          </FTreeVisibilityOptions>
                        </visibilityOptions>
                        <extendedGroupingTreeTemplates type ="Property">
                          <FDictionary type ="AcmDomain">
                          </FDictionary>
                        </extendedGroupingTreeTemplates>
                        <rowModifier type ="Property">
                          <FRowModifier type ="AcmDomain">
                            <propKeys type ="Property">
                              <FArray type ="AcmDomain">
                              </FArray>
                            </propKeys>
                            <propVals type ="Property">
                              <FArray type ="AcmDomain">
                              </FArray>
                            </propVals>
                          </FRowModifier>
                        </rowModifier>
                        <buildChildren type ="Property">
                          <bool type ="AcmDomain">true</bool>
                        </buildChildren>
                        <includeSourceLevel type ="Property">
                          <bool type ="AcmDomain">false</bool>
                        </includeSourceLevel>
                      </FTreeConfiguration>
                    </treeConfiguration>
                    <treeNodeInclExcl type ="Property">
                      <FGroupNodeInclusionExclusionController type ="AcmDomain">
                        <excludedNodes type ="Property">
                          <FIdentitySet type ="AcmDomain">
                          </FIdentitySet>
                        </excludedNodes>
                        <includedNodes type ="Property">
                          <FIdentitySet type ="AcmDomain">
                          </FIdentitySet>
                        </includedNodes>
                      </FGroupNodeInclusionExclusionController>
                    </treeNodeInclExcl>
                  </FMoneyFlowAndTradesBuilder>
                </builder>
                <expandedLabelNodes type ="Property">
                  <FIdentitySet type ="AcmDomain">
                  </FIdentitySet>
                </expandedLabelNodes>
                <isExpanded type ="Property">
                  <bool type ="AcmDomain">true</bool>
                </isExpanded>
              </FLocalBuiltTree>
              </Element>
            </FGuiTree>
            </Element>
          </FGuiTree>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">sname</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FString type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">Cash Analysis1</string>
            </Text>
          </FString>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">toprow</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">9</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">txstyl</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">usovr</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FDictionary type ="AcmDomain">
          </FDictionary>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">version</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FDictionary type ="AcmDomain">
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FDomain type ="AcmDomain">
                  <DomainName type ="Property">
                    <string type ="AcmDomain">FTradingSheet</string>
                  </DomainName>
                </FDomain>
              </associationKey>
              <associationValue type ="Property">
                <FInteger type ="AcmDomain">
                  <Number type ="Property">
                    <int type ="AcmDomain">1</int>
                  </Number>
                </FInteger>
              </associationValue>
            </FAssociation>
            </Element>
          </FDictionary>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">zoom</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">100</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
    </FDictionary>
  </ArchiveContents>
  <Class type ="Property">
    <FDomain type ="AcmDomain">
      <DomainName type ="Property">
        <string type ="AcmDomain">FMoneyFlowSheet</string>
      </DomainName>
    </FDomain>
  </Class>
</FPersistentArchive>
</FrontArenaPrimeSheetExport>
"""

ONBOARDING_TRADES_WORKBOOK = """<?xml version='1.0' encoding='ISO-8859-1'?>
<FWorkbook>
    <acm_version>2014.4.8, Feb 19 2015</acm_version>
    <version>0 $Id$</version>
    <update_time>2016-06-16 14:51:45</update_time>
    <object_name>%(wbk_name)s</object_name>
    <owner>ATS</owner>
    <protection>3072</protection>
    <type>FWorkbook</type>
    <FTradingSheet>
        <type>FTradeSheet</type>
        <data>%(tradingsheet_data)s</data>
    </FTradingSheet>
</FWorkbook>
"""


ONBOARDING_TRADES_TRADINGSHEET_DATA = """<?xml version='1.0' encoding='ISO-8859-1'?>
<FrontArenaPrimeSheetExport>
<!--PRIME Version: 2014.4.8-->
<FPersistentArchive type ="AcmDomain">
  <ArchiveContents type ="Property">
    <FDictionary type ="AcmDomain">
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">columncreators</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FColumnCreators type ="AcmDomain">
            <creators type ="Property">
              <FArray type ="AcmDomain">
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">0a660176-1e67-4da4-85a9-00dfc4183e2b</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Instrument</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">15dfb8c0-0058-4125-b0a1-7bc27f9a2357</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Price</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">d57d16b9-206e-47f0-ada4-d6ab751520fd</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Quantity</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">7b1b90dc-6832-46b4-bb90-29855254012a</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Acquire Day</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">ef14556a-24bc-4a69-bab7-f115a84e2768</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Portfolio</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">13b68c9b-c9c2-4158-a6d1-0ec7dae4a102</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Currency</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">ba8de859-c2ba-4f92-a964-889d42e8dbad</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Status</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">ae8e021c-204f-416d-8ada-2b6368af783f</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Counterparty</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
                <Element>
                <FStandardColumnCreator type ="AcmDomain">
                  <guid type ="Property">
                    <string type ="AcmDomain">85d5b39b-6cc8-48ae-99dd-e35d24bd6595</string>
                  </guid>
                  <creatorTemplate type ="Property">
                    <FStandardColumnCreatorTemplate type ="AcmDomain">
                      <columnId type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Trade Trader</string>
                          </Text>
                        </FSymbol>
                      </columnId>
                      <contextSym type ="Property">
                        <FSymbol type ="AcmDomain">
                          <Text type ="Property">
                            <string type ="AcmDomain">Standard</string>
                          </Text>
                        </FSymbol>
                      </contextSym>
                    </FStandardColumnCreatorTemplate>
                  </creatorTemplate>
                </FStandardColumnCreator>
                </Element>
              </FArray>
            </creators>
            <headerColWidth type ="Property">
              <int type ="AcmDomain">208</int>
            </headerColWidth>
          </FColumnCreators>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">columnsettings</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FDictionary type ="AcmDomain">
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Acquire Day-7b1b90dc-6832-46b4-bb90-29855254012a</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">71</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Counterparty-ae8e021c-204f-416d-8ada-2b6368af783f</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">235</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Currency-13b68c9b-c9c2-4158-a6d1-0ec7dae4a102</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">64</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Instrument-0a660176-1e67-4da4-85a9-00dfc4183e2b</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">111</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Portfolio-ef14556a-24bc-4a69-bab7-f115a84e2768</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">134</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Price-15dfb8c0-0058-4125-b0a1-7bc27f9a2357</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">64</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Quantity-d57d16b9-206e-47f0-ada4-d6ab751520fd</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">64</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Status-ba8de859-c2ba-4f92-a964-889d42e8dbad</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">71</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Trade Trader-85d5b39b-6cc8-48ae-99dd-e35d24bd6595</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                  <Element>
                  <FAssociation type ="AcmDomain">
                    <associationKey type ="Property">
                      <FSymbol type ="AcmDomain">
                        <Text type ="Property">
                          <string type ="AcmDomain">width</string>
                        </Text>
                      </FSymbol>
                    </associationKey>
                    <associationValue type ="Property">
                      <FInteger type ="AcmDomain">
                        <Number type ="Property">
                          <int type ="AcmDomain">64</int>
                        </Number>
                      </FInteger>
                    </associationValue>
                  </FAssociation>
                  </Element>
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
          </FDictionary>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">frzcol</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">gridBuilderContents</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FDictionary type ="AcmDomain">
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">scenarioManager</string>
                  </Text>
                </FSymbol>
              </associationKey>
              <associationValue type ="Property">
                <FDictionary type ="AcmDomain">
                </FDictionary>
              </associationValue>
            </FAssociation>
            </Element>
          </FDictionary>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">grplbl</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FTrue type ="AcmDomain">
          </FTrue>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">gryinv</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">inihdc</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">inslab</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">Name</string>
            </Text>
          </FSymbol>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">isCalculateCellsOutOfViewEnabled</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FFalse type ="AcmDomain">
          </FFalse>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">isCellContentSuppressed</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FFalse type ="AcmDomain">
          </FFalse>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">isDistributedProcessingEnabled</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FFalse type ="AcmDomain">
          </FFalse>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">leftcol</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">Trade Instrument-0a660176-1e67-4da4-85a9-00dfc4183e2b</string>
            </Text>
          </FSymbol>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">manrfr</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">pgsetup</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FString type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">94 71 94 71 100 p</string>
            </Text>
          </FString>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">rfrper</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">rows</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FGuiTree type ="AcmDomain">
            <item type ="Property">
              <FSymbol type ="AcmDomain">
                <Text type ="Property">
                  <string type ="AcmDomain">DummyRoot</string>
                </Text>
              </FSymbol>
            </item>
            <Element>
            <FGuiTree type ="AcmDomain">
              <item type ="Property">
                <FSymbol type ="AcmDomain">
                  <Text type ="Property">
                    <string type ="AcmDomain">Root</string>
                  </Text>
                </FSymbol>
              </item>
              <treeId type ="Property">
                <int type ="AcmDomain">3</int>
              </treeId>
              <Element>
              <FPortfolioTree type ="AcmDomain">
                <treeId type ="Property">
                  <int type ="AcmDomain">2</int>
                </treeId>
                <builder type ="Property">
                  <FPortfolioTreeBuilder type ="AcmDomain">
                    <treeConfiguration type ="Property">
                      <FTreeConfiguration type ="AcmDomain">
                        <treeSpecification type ="Property">
                          <FTreeSpecification type ="AcmDomain">
                            <groupingSubjectClass type ="Property">
                              <FDomain type ="AcmDomain">
                                <DomainName type ="Property">
                                  <string type ="AcmDomain">FInstrumentAndTradesGrouperSubject</string>
                                </DomainName>
                              </FDomain>
                            </groupingSubjectClass>
                            <originObject type ="Property">
                              <FPersistent type ="AcmDomain">
                                <Class type ="Property">
                                  <FDomain type ="AcmDomain">
                                    <DomainName type ="Property">
                                      <string type ="AcmDomain">FTradeSelection</string>
                                    </DomainName>
                                  </FDomain>
                                </Class>
                                <ExternalReference type ="Property">
                                  <FVariantDictionary type ="AcmDomain">
                                    <Element>
                                    <FAssociation type ="AcmDomain">
                                      <associationKey type ="Property">
                                        <FSymbol type ="AcmDomain">
                                          <Text type ="Property">
                                            <string type ="AcmDomain">Name</string>
                                          </Text>
                                        </FSymbol>
                                      </associationKey>
                                      <associationValue type ="Property">
                                        <FString type ="AcmDomain">
                                          <Text type ="Property">
                                            <string type ="AcmDomain">%(tradefilter_name)s</string>
                                          </Text>
                                        </FString>
                                      </associationValue>
                                    </FAssociation>
                                    </Element>
                                  </FVariantDictionary>
                                </ExternalReference>
                              </FPersistent>
                            </originObject>
                            <grouper type ="Property">
                              <FDefaultGrouper type ="AcmDomain">
                                <split type ="Property">
                                  <bool type ="AcmDomain">false</bool>
                                </split>
                              </FDefaultGrouper>
                            </grouper>
                          </FTreeSpecification>
                        </treeSpecification>
                        <visibilityOptions type ="Property">
                          <FPortfolioTreeVisibilityOptions type ="AcmDomain">
                            <includeSingleInstruments type ="Property">
                              <bool type ="AcmDomain">false</bool>
                            </includeSingleInstruments>
                            <includeInactive type ="Property">
                              <bool type ="AcmDomain">true</bool>
                            </includeInactive>
                            <activateAtInstrumentLevel type ="Property">
                              <bool type ="AcmDomain">true</bool>
                            </activateAtInstrumentLevel>
                            <includeResidual type ="Property">
                              <bool type ="AcmDomain">true</bool>
                            </includeResidual>
                            <includeExpired type ="Property">
                              <bool type ="AcmDomain">true</bool>
                            </includeExpired>
                          </FPortfolioTreeVisibilityOptions>
                        </visibilityOptions>
                        <extendedGroupingTreeTemplates type ="Property">
                          <FDictionary type ="AcmDomain">
                          </FDictionary>
                        </extendedGroupingTreeTemplates>
                        <rowModifier type ="Property">
                          <FRowModifier type ="AcmDomain">
                            <propKeys type ="Property">
                              <FArray type ="AcmDomain">
                              </FArray>
                            </propKeys>
                            <propVals type ="Property">
                              <FArray type ="AcmDomain">
                              </FArray>
                            </propVals>
                          </FRowModifier>
                        </rowModifier>
                        <buildChildren type ="Property">
                          <bool type ="AcmDomain">true</bool>
                        </buildChildren>
                        <includeSourceLevel type ="Property">
                          <bool type ="AcmDomain">true</bool>
                        </includeSourceLevel>
                      </FTreeConfiguration>
                    </treeConfiguration>
                    <treeNodeInclExcl type ="Property">
                      <FGroupNodeInclusionExclusionController type ="AcmDomain">
                        <excludedNodes type ="Property">
                          <FIdentitySet type ="AcmDomain">
                          </FIdentitySet>
                        </excludedNodes>
                        <includedNodes type ="Property">
                          <FIdentitySet type ="AcmDomain">
                          </FIdentitySet>
                        </includedNodes>
                      </FGroupNodeInclusionExclusionController>
                    </treeNodeInclExcl>
                  </FPortfolioTreeBuilder>
                </builder>
                <expandedLabelNodes type ="Property">
                  <FIdentitySet type ="AcmDomain">
                  </FIdentitySet>
                </expandedLabelNodes>
                <isExpanded type ="Property">
                  <bool type ="AcmDomain">true</bool>
                </isExpanded>
              </FPortfolioTree>
              </Element>
            </FGuiTree>
            </Element>
          </FGuiTree>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">sname</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FString type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">Trades1</string>
            </Text>
          </FString>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">toprow</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">2</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">txstyl</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">0</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">usovr</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FDictionary type ="AcmDomain">
          </FDictionary>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">version</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FDictionary type ="AcmDomain">
            <Element>
            <FAssociation type ="AcmDomain">
              <associationKey type ="Property">
                <FDomain type ="AcmDomain">
                  <DomainName type ="Property">
                    <string type ="AcmDomain">FTradingSheet</string>
                  </DomainName>
                </FDomain>
              </associationKey>
              <associationValue type ="Property">
                <FInteger type ="AcmDomain">
                  <Number type ="Property">
                    <int type ="AcmDomain">1</int>
                  </Number>
                </FInteger>
              </associationValue>
            </FAssociation>
            </Element>
          </FDictionary>
        </associationValue>
      </FAssociation>
      </Element>
      <Element>
      <FAssociation type ="AcmDomain">
        <associationKey type ="Property">
          <FSymbol type ="AcmDomain">
            <Text type ="Property">
              <string type ="AcmDomain">zoom</string>
            </Text>
          </FSymbol>
        </associationKey>
        <associationValue type ="Property">
          <FInteger type ="AcmDomain">
            <Number type ="Property">
              <int type ="AcmDomain">100</int>
            </Number>
          </FInteger>
        </associationValue>
      </FAssociation>
      </Element>
    </FDictionary>
  </ArchiveContents>
  <Class type ="Property">
    <FDomain type ="AcmDomain">
      <DomainName type ="Property">
        <string type ="AcmDomain">FTradeSheet</string>
      </DomainName>
    </FDomain>
  </Class>
</FPersistentArchive>
</FrontArenaPrimeSheetExport>
"""
