"""
Deployment date     : 2013-12-05
Purpose             : A feed processor which handles the bond price data
                      from JSE and uses them to update
                      the instruments' prices.
Department and Desk : Prime Services
Requester           : Ruth Forssman
Developer           : Peter Basista
CR Number           : CHNG0001547146

HISTORY:
========

Date        CR number       Developer       Description
-------------------------------------------------------
2014-12-02  CHNG0002472033  Peter Basista   Change the logic of the price
                                            updates to always update
                                            the prices of the original
                                            instrument, as well as
                                            the "/MTM" one.
                                            Also, use at_feed_processing.
"""

import string

import acm

import at_feed_processing


# Human readable quotation types
HR_QTYPES = {"Factor": "% of nominal",
             "Yield": "Yield"}


def modified_data(file_object):
    """
    A generator function which yields the next available row
    in the provided file object while skipping the first lines
    until the appropriate header is encountered.
    """
    header_found = False
    for line in file_object:
        if "Bond Code" in line:
            header_found = True
        if header_found:
            yield line


def set_instrument_price_wrapper(acm_instrument,
                                 date_string,
                                 fa_market_name,
                                 price):
    """
    Set the market price of the specified instrument
    on the provided market for the provided date to the provided value.
    """
    fa_instrument_name = acm_instrument.Name()
    fa_instrument_qtype = acm_instrument.Quotation().QuotationType()
    try:
        acm_market = acm.FParty[fa_market_name]
        # We should not have any assumptions
        # about the type of exceptions
        # that the following function call
        # might eventually raise.
        # Therefore, we have to catch
        # almost all the exception types.
        import at_price
        at_price.set_instrument_price(acm_instrument,
                                      acm_market,
                                      price,
                                      date_string=date_string)
    except Exception as exc:
        error_message = ("Failed to set the {market_name} "
                         "price of instrument {instrument_name} "
                         "[{quotation_type}] to {price_value}. "
                         "A call to the price update function "
                         "thew the following exception: "
                         "'{string_exception}'").format(
                             market_name=fa_market_name,
                             instrument_name=fa_instrument_name,
                             quotation_type=HR_QTYPES[fa_instrument_qtype],
                             price_value=price,
                             string_exception=str(exc))
        raise JSEMTMFeedProcessor.FeedProcessingException(error_message)
    print(("{instrument_name} [{quotation_type}]: "
           "{market_name} price "
           "updated to '{price_value}'.").format(
               instrument_name=fa_instrument_name,
               quotation_type=HR_QTYPES[fa_instrument_qtype],
               market_name=fa_market_name,
               price_value=price))


class JSEMTMFeedProcessor(at_feed_processing.SimpleCSVFeedProcessor):

    """
    A feed processor for the MTM feed from JSE.
    It parses the csv file containing the MTM feed from JSE
    and creates or updates the prices of the instruments
    which are also present in Front Arena.
    The instruments are uniquely identified by their ISIN
    (International Securities Identification Number).
    In case there is also a "/MTM" flavour of the identified instrument
    in Front Arena, its price is updated as well.
    The price to be updated is determined by the quotation type
    of the corresponding Front Arena instrument.
    For all the instruments, the default market to be used for price updates
    is "SPOT_BESA". If an instrument is listed in the query folder called
    "Instruments using SPOT prices", its price for the "SPOT" market
    is updated as well. In case of "/MTM" instruments, their
    "SPOT" market price is always updated, even if they are not listed
    in the query folder mentioned above.
    """

    column_bond_code = "Bond Code"
    column_isin = "ISIN Code"
    column_mtm_price = "MTM"
    column_all_in_price = "All in price"
    _required_columns = [column_bond_code,
                         column_isin,
                         column_mtm_price,
                         column_all_in_price]

    def __init__(self, file_path_template, date_string):
        """
        Initialize the feed processor using the proper name
        of the today's csv file which containins the MTM feed.
        """
        fpath_template = string.Template(file_path_template)
        file_path = fpath_template.substitute(DATE=date_string)
        self.date_string = date_string
        super(JSEMTMFeedProcessor, self).__init__(file_path)

        # Getting the list of instruments for which
        # we need to update the SPOT prices as well.
        query_folder = acm.FStoredASQLQuery["Instruments using SPOT prices"]
        self.spot_instruments = set(query_folder.Query().Select())

    def _load(self):
        """
        Prepare the feed processor for usage by opening a csv file
        which containins the MTM feed and advancing to its header row.
        """
        super(JSEMTMFeedProcessor, self)._load()
        self._data = modified_data(self._data)

    def _finish(self):
        """
        Clean up the objects which are no longer in use.
        Also, raise an exception if there were some instruments
        whose SPOT prices should have been updated, but they were not.
        """
        super(JSEMTMFeedProcessor, self)._finish()
        if self.spot_instruments:
            instrument_names = ""
            for acm_instrument in self.spot_instruments:
                instrument_names += acm_instrument.Name() + "\n"
            error_message = ("The prices of the following required "
                             "instruments were not updated:\n{0}").format(
                                 instrument_names)
            raise self.FeedProcessingException(error_message)

    def _process_record(self, record, dry_run):
        """
        Use the current MTM file record for setting
        the appropriate instruments' prices.
        """
        (_index, record_data) = record
        instrument_code = record_data[self.column_bond_code]
        isin = record_data[self.column_isin]
        mtm_price = record_data[self.column_mtm_price]
        all_in_price = record_data[self.column_all_in_price]
        candidate_instruments = acm.FInstrument.Select("isin = {0}".format(
            isin))
        if len(candidate_instruments) == 0:
            # No instrument in Front Arena has the same ISIN
            # as the currently processed instrument.
            return
        # At this point, len(candidate_instruments) > 0.
        # The ISIN field is unique among all instruments,
        # which means that there can never be
        # more than one instrument with the same ISIN.
        acm_instrument = candidate_instruments[0]
        if acm_instrument.InsType() == "Deposit":
            # The decision was not to update
            # the prices of Deposits using this feed.
            return
        fa_instrument_name = acm_instrument.Name()
        fa_instrument_qtype = acm_instrument.Quotation().QuotationType()

        if fa_instrument_qtype == "Yield":
            sprice = mtm_price
        elif fa_instrument_qtype == "Factor":
            sprice = all_in_price
        else:
            error_message = ("Instrument '{0}' (ISIN: {1}, "
                             "feed code: {2}) uses a quotation type '{3}' "
                             "but we do not know how to handle it.").format(
                                 fa_instrument_name,
                                 isin,
                                 instrument_code,
                                 fa_instrument_qtype)
            raise self.RecordProcessingException(error_message)
        # At this point, the sprice variable is guaranteed to be defined,
        # but since its value comes from a csv reader, it is of type string.
        # Therefore, we have to convert it to float in order to continue.
        if sprice:
            price = float(sprice)
        else:
            price = 0
        # FIXME: Is this check required?
        # Can the correct instrument's price be zero?
        if not price:
            error_message = ("Instrument '{0}' (ISIN: {1}, "
                             "quotation type: '{2}', feed code: {3}) "
                             "does not have the appropriate price set "
                             "in the JSE MTM feed.").format(
                                 fa_instrument_name,
                                 isin,
                                 HR_QTYPES[fa_instrument_qtype],
                                 instrument_code)
            raise self.RecordProcessingException(error_message)
        # The default market for setting the price.
        markets = ["SPOT_BESA"]
        if acm_instrument in self.spot_instruments:
            markets.append("SPOT")
            self.spot_instruments.remove(acm_instrument)
        if dry_run:
            print ("Dry run has been requested. "
                   "Skipping the 'non-/MTM' price updates.")
        else:
            # Update the prices of the "non-/MTM" instrument.
            for market in markets:
                set_instrument_price_wrapper(acm_instrument,
                                             self.date_string,
                                             market,
                                             price)

        # Now check whether the "/MTM" alternative
        # of the matched instrument exists.
        # If it does, update its prices as well.
        acm_mtm_alternatives = acm.FInstrument.Select("name = {0}/MTM".format(
            fa_instrument_name))
        if len(acm_mtm_alternatives) == 0:
            # If the "/MTM" alternative instrument exists,
            # its prices are updated as well.
            return
        # At this point, len(acm_mtm_alternatives) > 0.
        # The instrument's name is guaranteed to be unique
        # among all the instruments, which means
        # that we always get at most one MTM alternative.
        acm_mtm_alternative = acm_mtm_alternatives[0]
        mtm_alternative_name = acm_mtm_alternative.Name()
        mtm_alternative_qtype = acm_mtm_alternative.Quotation().QuotationType()
        if fa_instrument_qtype != mtm_alternative_qtype:
            error_message = ("The quotation type "
                             "of the original instrument "
                             "'{0}' is '{1}', "
                             "but this is different "
                             "from the quotation type "
                             "'{2}' of the \"/MTM\" "
                             "instrument '{3}'!").format(
                                 fa_instrument_name,
                                 fa_instrument_qtype,
                                 mtm_alternative_qtype,
                                 mtm_alternative_name)
            raise self.RecordProcessingException(error_message)
        # The default market for setting the price.
        markets = ["SPOT_BESA", "SPOT"]
        if dry_run:
            print ("Dry run has been requested. "
                   "Skipping the '/MTM' price updates.")
        else:
            for market in markets:
                set_instrument_price_wrapper(acm_mtm_alternative,
                                             self.date_string,
                                             market,
                                             price)


ael_variables = JSEMTMFeedProcessor.ael_variables()
variable_index = ael_variables._index_of_var("file_dir")
del ael_variables[variable_index]
variable_index = ael_variables._index_of_var("file_name")
del ael_variables[variable_index]
ael_variables.add("date_override",
                  label="Date override",
                  cls="date",
                  mandatory=False,
                  alt=("A date which shall be used throughout "
                       "this script's execution "
                       "instead of the today's date."))
ael_variables.add("file_path_template",
                  label="File path template",
                  alt=("A path template to the input file. "
                       "It can contain the variable DATE (\"$DATE\") "
                       "which will be replaced by the today's date"))
ael_variables.add("reporting_emails",
                  label="Reporting e-mails",
                  multiple=True,
                  alt=("E-mail addresses (delimited by a comma \",\") "
                       "to which the reporting e-mails will be sent."))


def ael_main(parameters):
    """
    The entry point for task execution.
    """
    dry_run = parameters["dry_run"]
    ael_date = parameters["date_override"]
    file_path_template = parameters["file_path_template"]
    reporting_emails = list(parameters["reporting_emails"])
    reporting_emails = ",".join(reporting_emails)
    email_error_notifier = at_feed_processing.EmailNotifier(reporting_emails)
    if ael_date:
        date_string = str(ael_date)
    else:
        date_string = acm.Time().DateToday()

    processor = JSEMTMFeedProcessor(file_path_template, date_string)
    processor.add_error_notifier(at_feed_processing.notify_log)
    processor.add_error_notifier(email_error_notifier)

    processor.process(dry_run)

    if not processor.errors:
        print("Completed successfully")
