import os.path
import acm
import PS_Functions
from at_report import CSVReportCreator


class SweepingDataException(Exception):
    """General exception to detect incomplete sweeping data."""

    pass


class SweepingReport(CSVReportCreator):
    """Generic report to expose how sweeping amounts are calculated."""

    def __init__(self, full_file_path):
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)

        super(SweepingReport, self).__init__(file_name_only, file_suffix, file_path)


class CallAccountSweepingReport(SweepingReport):
    """Report to expose how sweeping amounts are calculated."""

    def __init__(self, full_file_path, data):
        try:
            (
                self.current_tpl,
                self.hist_tpl,
                self.call_account_tpl,
                self.current_tpl_breakdown,
                self.hist_tpl_breakdown,
            ) = data
        except Exception as ex:
            message = "Input data mismatch: {0}".format(ex)
            raise SweepingDataException(message)

        super(CallAccountSweepingReport, self).__init__(full_file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for pswap_name in sorted(self.current_tpl):
            pswap = acm.FInstrument[pswap_name]
            fully_funded = PS_Functions.get_pb_pswap_ff_flag(pswap)
            for date in sorted(self.current_tpl[pswap_name]):
                for ins_type in sorted(self.current_tpl[pswap_name][date]):
                    self._add_ins_type_line(pswap_name, date, ins_type, fully_funded)
                    ins_list = []
                    ins_list.extend(
                        self.current_tpl_breakdown[pswap_name][date][ins_type]
                    )
                    ins_list.extend(self.hist_tpl_breakdown[pswap_name][date][ins_type])

                    for instrument in sorted(set(ins_list)):
                        self._add_instrument_line(
                            pswap_name, date, ins_type, instrument, fully_funded
                        )

    def _add_ins_type_line(self, pswap_name, date, ins_type, fully_funded):
        """Add one line per instrument type."""
        line = []
        line.append(date)
        line.append(pswap_name)
        line.append(ins_type)
        line.append("-")

        total_tpl = 0.0
        if fully_funded:
            cash_end = self.current_tpl[pswap_name][date][ins_type][0]
            total_tpl = cash_end
            line.append("-")
            line.append("-")
            line.append("-")
            line.append("-")
            line.append(cash_end)
            line.append(total_tpl)
        else:
            for value in self.current_tpl[pswap_name][date][ins_type]:
                line.append(value)
                total_tpl += value
            line.append("-")
            line.append(total_tpl)

        line.append(self.hist_tpl[pswap_name][date][ins_type])
        line.append(self.call_account_tpl[pswap_name][date][ins_type][0])
        line.append(self.call_account_tpl[pswap_name][date][ins_type][1])
        line.append(self.call_account_tpl[pswap_name][date][ins_type][2])
        # Append the line to the output file
        self.content.append(line)

    def _add_instrument_line(
        self, pswap_name, date, ins_type, instrument, fully_funded
    ):
        """Add one line per instrument."""
        line = []
        line.append(date)
        line.append(pswap_name)
        line.append(ins_type)
        line.append(instrument)

        total_tpl = 0.0
        if fully_funded:
            if self.current_tpl_breakdown[pswap_name][date][ins_type][instrument]:
                cash_end = self.current_tpl_breakdown[pswap_name][date][ins_type][
                    instrument
                ][0]
                total_tpl = cash_end
            else:
                cash_end = total_tpl = 0
            line.append("-")
            line.append("-")
            line.append("-")
            line.append("-")
            line.append(cash_end)
            line.append(total_tpl)
        else:
            if self.current_tpl_breakdown[pswap_name][date][ins_type][instrument]:
                for value in self.current_tpl_breakdown[pswap_name][date][ins_type][
                    instrument
                ]:
                    if value == None:
                        value = 0
                    line.append(value)
                    total_tpl += value
            else:
                for _ in range(0, 4):
                    line.append(0)

            line.append("-")
            line.append(total_tpl)

        hist = self.hist_tpl_breakdown[pswap_name][date][ins_type][instrument]
        line.append(hist)
        line.append(total_tpl - hist)
        line.append("-")
        line.append("-")
        # Append the line to the output file
        self.content.append(line)

    def _header(self):
        """Return columns of the header."""
        header = [
            "Date",
            "Portfolio Swap",
            "Instrument Type",
            "Instrument Name",
            "Client TPL",
            "Daily Funding",
            "Daily Warehousing",
            "Daily Provision",
            "Portfolio Cash End",
            "Total TPL",
            "Previous Business Day TPL",
            "Diff",
            "Current Call Account Posting",
            "Adjustment Posting",
        ]

        return header


class LoanAccountSweepingReport(SweepingReport):
    """Report to expose how sweeping amounts are calculated."""

    def __init__(self, full_file_path, trade_data):
        self.trade_data = trade_data
        super(LoanAccountSweepingReport, self).__init__(full_file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for line in self.trade_data:
            self.content.append(line)

    def _header(self):
        """Return columns of the header."""
        header = [
            "Trade Number",
            "Instrument Type",
            "Instrument Name",
            "Portfolio Name",
            "Portfolio Value End",
        ]

        return header


class SaxoSweepingReport(SweepingReport):
    def __init__(self, full_file_path, trade_data):
        self.trade_data = trade_data
        super(SaxoSweepingReport, self).__init__(full_file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for line in self.trade_data:
            self.content.append(line)

    def _header(self):
        """Return columns of the header."""
        header = [
            "Trade Number",
            "Instrument Type",
            "Instrument Name",
            "Portfolio Name",
            "Portfolio Value End",
        ]

        return header


class PSwapSweepingReport(SweepingReport):
    def __init__(self, full_file_path, data):
        self.data = data
        super(PSwapSweepingReport, self).__init__(full_file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for pswap_name, pswap_data in sorted(self.data.items()):
            pswap = acm.FInstrument[pswap_name]
            fully_funded = (
                "Fully Funded"
                if PS_Functions.get_pb_pswap_ff_flag(pswap)
                else "Financed"
            )

            for date, (funding, provision, tpl) in sorted(pswap_data.items()):
                for ins_type in sorted(
                    set(tpl.keys() + provision.keys() + funding.keys())
                ):

                    ins_tpl = tpl[ins_type]
                    ins_provision = provision[ins_type]
                    ins_funding = funding[ins_type]

                    ins_type_tpl = sum(ins_tpl.values())
                    ins_type_provision = sum(ins_provision.values())
                    ins_type_funding = sum(ins_funding.values())

                    self.content.append(
                        [
                            date,
                            pswap_name,
                            fully_funded,
                            ins_type,
                            "-",
                            ins_type_funding,
                            ins_type_provision,
                            ins_type_tpl,
                        ]
                    )

                    for ins_name in sorted(
                        set(ins_tpl.keys() + ins_provision.keys() + ins_funding.keys())
                    ):
                        self.content.append(
                            [
                                date,
                                pswap_name,
                                fully_funded,
                                ins_type,
                                ins_name,
                                funding[ins_type].get(ins_name, 0.0),
                                provision[ins_type].get(ins_name, 0.0),
                                tpl[ins_type].get(ins_name, 0.0),
                            ]
                        )

    def _header(self):
        """Return column names."""
        return [
            "Date",
            "Portfolio Swap",
            "Position",
            "Instrument Type",
            "Instrument Name",
            "Funding",
            "Provision",
            "TPL",
        ]


class OffshoreFundingSweepingReport(SweepingReport):
    def __init__(self, full_file_path, data):
        self.data = data
        super(OffshoreFundingSweepingReport, self).__init__(full_file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for line in self.data:
            self.content.append(line)

    def _header(self):
        """Return column names."""
        header = [
            "Report Date",
            "Pay Date",
            "Client",
            "Security Code",
            "Security Ticker",
            "Security Name",
            "Currency",
            "MtM",
            "Number of Days",
            "Base Rate",
            "Broker Spread",
            "Broker Rate",
            "Absa Spread",
            "Absa Rate",
            "Day Count Method",
            "Broker Funding in Currency",
            "Absa Funding in Currency",
            "FX Rate",
            "Absa Funding in USD",
        ]
        return header


class OffshorePnLSweepingReport(SweepingReport):
    def __init__(self, full_file_path, data):
        self.data = data
        super(OffshorePnLSweepingReport, self).__init__(full_file_path)

    def _collect_data(self):
        """Collect data relevant for the report."""
        for line in self.data:
            self.content.append(line)

    def _header(self):
        """Return column names."""
        header = [
            "Report Date",
            "Client",
            "Security Code",
            "Security Ticker",
            "Security Name",
            "Underlying Currency",
            "Funding Currency",
            "Quantity",
            "Weighted Average Price",
            "Traded Amount",
            "Closing Price",
            "MtM",
            "Unrealised MtM",
            "Execution Rate",
            "Execution Fees",
            "Funding",
            "TPL in Currency",
            "FX Rate",
            "TPL in USD",
        ]
        return header
