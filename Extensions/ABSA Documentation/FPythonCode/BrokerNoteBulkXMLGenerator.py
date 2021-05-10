"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    BrokerNoteBulkXMLGenerator
    
DESCRIPTION
    This module contains an object used for generating the XML content for a
   broker note.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-04-20      FAOPS-702       Joash Moodley                                   Initial Implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
2020-12-09      FAOPS-907       Metse Moshobane         Nqubeko Zondi           Changing four Columns to 6 decimals.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import xml.etree.ElementTree as ElementTree

import acm

from BrokerNoteBulkGeneral import get_default_document_parameter, get_broker_note_trades
import DocumentGeneral


class GenerateBrokerNoteBulkXMLXRequest(object):
    """
    An object embodying the request to generate 
    the XML content for a broker note.
    """

    def __init__(
            self, managing_party, instrument_type,
            from_date, to_date, block_trade_id):
        """
        Constructor.
        """
        self.managing_party = managing_party
        self.instrument_type = instrument_type
        self.from_date = from_date
        self.to_date = to_date
        self.block_trade_id = block_trade_id
        

class BrokerNoteBulkXMLGenerator(object):
    """
    An object responsible for generating the XML content for a broker_note.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.trade_date = None
        self.trade_no = None
        self.settlement_date = None
        self.security_descr = None
        self.buyer = None
        self.seller = None
        self.isin = None
        self.issuer = None
        self.maturity_date = None
        self.currency = None
        self.nominal = None
        self.yield_to_maturity = None
        self.clean_price = None
        self.clean_consideration = None
        self.consideration_interest = None
        self.all_in_consideration = None
        self.companion = None
        self.companion_spread = None
        self.nutron_code = None
        self.unexcor_code = None
        self.all_in_price = None

    @staticmethod    
    def _get_interest(trade, calc_space):
        ins_type = trade.Instrument().InsType()
        if ins_type in ['IndexLinkedBond', 'Bond']:
            return round(
                calc_space.CreateCalculation(calc_space.InsertItem(trade),
                'Portfolio Traded Interest').Value(),
                2
            )

        elif ins_type == 'FRN':
            return round(
                calc_space.CreateCalculation(calc_space.InsertItem(trade),
                'Portfolio Traded Interest').Value(),
                2
            )

    @staticmethod
    def get_all_in_consideration(trade):
        return abs(trade.Premium())

    @staticmethod
    def _get_yield(trade):
        ins_type = trade.Instrument().InsType()
        
        if ins_type in ['IndexLinkedBond', 'Bond']:
            return abs(trade.Price())

        return ''

    @staticmethod
    def security_description(trade):
        instrument = trade.Instrument()
        if instrument.Underlying():
            instrument_name = instrument.Underlying().Name()
        else:
            instrument_name = instrument.Name()

        if instrument.InsType() == 'FRN':
            return instrument_name
        else:
            leg = instrument.Legs()[0]
        fixed_rate = leg.FixedRate()
        maturity_year = instrument.ExpiryDate().split()[0][:4]
        security_description = str(instrument_name) + ' ' + str(fixed_rate) + '% ' + str(maturity_year)
        if fixed_rate == 0:
            return instrument_name
        else:
            return security_description
        
    def generate_xml(self, generate_broker_note_xml_request):
        """
        Generate the XML for a pre-settlement broker_note
        """
        broker_note_element = self._generate_broker_note_element(generate_broker_note_xml_request)
        return ElementTree.tostring(broker_note_element)

    def _generate_broker_note_element(self, generate_broker_note_xml_request):
        """
        Generate the broker note XML element and sub-elements.
        """
        trade = acm.FTrade[generate_broker_note_xml_request.block_trade_id]
        instrument_type = generate_broker_note_xml_request.instrument_type
        to_date = generate_broker_note_xml_request.to_date
        from_date = generate_broker_note_xml_request.from_date
        element = self._generate_element('BROKER_NOTES')
        element.append(self._generate_element('BANK_ABBREVIATED_NAME', str(DocumentGeneral
            .get_default_bank_abbreviated_name())))
        element.append(self._generate_element('FROM_DATE', from_date))
        element.append(self._generate_element('TO_DATE', to_date))
        element.append(self._generate_element('INSTRUMENT_TYPE', instrument_type))
        trades = get_broker_note_trades(
            trade,
            generate_broker_note_xml_request.managing_party
        )

        for trade in trades:
            element.append(self._generate_broker_note_elements(trade))

        return element

    def _generate_broker_note_elements(self, trade):
        """
        Generates the broker note elements.
        """
        element = self._generate_element('BROKER_NOTE')
        calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')
        trade_date = trade.CreateDay()
        trade_no = trade.Oid()
        settlement_date = trade.ValueDay()
        security_descr = self.security_description(trade)
        currency = trade.Instrument().Currency().Name()
        companion = trade.Instrument().AddInfoValue('Companion')
        companion_spread = trade.AddInfoValue('Companion_Spread')
        if companion_spread != None:
            companion_spread = "{0:10.6f}".format(float(companion_spread))
        nutron_code = trade.Counterparty().HostId()
        unexcor_code = trade.Counterparty().AddInfoValue('UnexCor Code')
        nominal = abs(trade.Nominal())
        all_in_price = abs(trade.Price())
        if all_in_price != None:
            all_in_price = "{0:10.6f}".format(float(all_in_price))
        if trade.Instrument().Underlying():
            isin = trade.Instrument().Underlying().Isin()
        else:
            isin = trade.Instrument().Isin()

        if trade.Nominal() > 0:
            buyer = get_default_document_parameter('DefaultBankName')
            seller = DocumentGeneral.get_party_full_name(trade.Counterparty())
        else:
            seller = get_default_document_parameter('DefaultBankName')
            buyer = DocumentGeneral.get_party_full_name(trade.Counterparty())

        issuer = trade.Instrument().Issuer().Name() if trade.Instrument().Issuer() else ''
        maturity_date = trade.Instrument().ExpiryDateOnly()
        clean_price = calc_space.CreateCalculation(calc_space.InsertItem(trade), 'cleanPrice').Value()
        if clean_price != None:
            clean_price = "{0:10.6f}".format(float(clean_price))
        all_in_consideration = self.get_all_in_consideration(trade)
        yield_to_maturity = self._get_yield(trade)
        if yield_to_maturity != '':
            yield_to_maturity = "{:0.6f}".format(float(yield_to_maturity))
        consideration_interest = abs(self._get_interest(trade, calc_space))
        clean_consideration = all_in_consideration - consideration_interest

        element.append(self._generate_element('TRADE_DATE', str(trade_date)))
        element.append(self._generate_element('TRADE_NO', str(trade_no)))
        element.append(self._generate_element('SETTLEMENT_DATE', str(settlement_date)))
        element.append(self._generate_element('SECURITY_DESCR', str(security_descr)))
        element.append(self._generate_element('BUYER', str(buyer)))
        element.append(self._generate_element('SELLER', str(seller)))
        element.append(self._generate_element('ISIN', str(isin)))
        element.append(self._generate_element('ALL_IN_PRICE', str(all_in_price)))
        element.append(self._generate_element('ISSUER', str(issuer)))
        element.append(self._generate_element('MATURITY_DATE', str(maturity_date)))
        element.append(self._generate_element('CURRENCY', str(currency)))
        element.append(self._generate_element('NOMINAL', str(round(nominal, 2))))
        element.append(self._generate_element('YIELD_TO_MATURITY', str(yield_to_maturity)))
        element.append(self._generate_element('CLEAN_PRICE', str(clean_price)))
        element.append(self._generate_element('CLEAN_CONSIDERATION', str(round(clean_consideration, 2))))
        element.append(self._generate_element('CONSIDERATION_INTEREST', str(consideration_interest)))
        element.append(self._generate_element('ALL_IN_CONSIDERATION', str(round(all_in_consideration, 2))))
        element.append(self._generate_element('COMPANION', str(companion)))
        element.append(self._generate_element('COMPANION_SPREAD', str(companion_spread)))
        element.append(self._generate_element('NUTRON_CODE', str(nutron_code)))
        element.append(self._generate_element('UNEXCOR_CODE', str(unexcor_code)))
        return element
    
    @staticmethod
    def _generate_element(element_name, element_text=''):
        """
        Generate an XML element with the specified name and text.
        """
        element = ElementTree.Element(element_name)
        element.text = element_text
        return element
