'''
Uses trade filter for trade selection and then loops through the money flows
to identify ones paying on a non business day. Uses the calender of the money flow currency.

Purpose: [Initial deployment]
Department: [OPS]
Requester: [Christa Hefer]
Developer: [Willie van der Bank]
CR Number: [CHNG0001877689 2014-04-10]
'''

import acm, ael
from at_ael_variables import AelVariableHandler
import at_report
import os


ael_gui_parameters = {
    'windowCaption': 'Generate the report',
    'runButtonLabel': '&&Generate',
    'closeWhenFinished': True
}

ael_variables = AelVariableHandler()

ael_variables.add(
    'date_from',
    label = 'Date from',
    default = acm.Time.DateToday(),
    mandatory = False,
    alt = 'Start date of requied time interval'
)

ael_variables.add(
    'date_to',
    label = 'Date to',
    default = acm.Time.DateAddDelta(acm.Time.DateToday(), 0, 1, 0),
    mandatory = False,
    alt = 'End date of requied time interval'
)

ael_variables.add(
    'target_folder',
    label = 'Target folder path',
    default = os.path.join("F:\\", "OPS_NONBUSDAY"),
    mandatory = True,
    alt = 'Path to folder where the file will be stored'
)

def ael_main(params):
    """Main run creates the report."""

    if params['date_from'] == '':
        runDate = ael.date_today()
    else:
        runDate = ael.date(params['date_from'])
    if params['date_to'] == '':
        toDate = runDate.add_days(30)
    else:
        toDate = ael.date(params['date_to'])
    
    fileName = 'OPS_NONBUSDAY'
    report = ReportCreator(file_name=fileName, file_suffix="csv", 
        path=params['target_folder'], date_from=runDate, 
        date_to=toDate)
    report.create_report()

    location = params['target_folder'] + "/" + fileName + ".csv"
    ael.log('Wrote secondary output to:::' + location)

class ReportCreator(at_report.CSVReportCreator):
    """Creates the report."""

    def __init__(self, file_name, file_suffix, path, date_from, date_to):

        super(ReportCreator, self).__init__(file_name=file_name,
            file_suffix=file_suffix, path=path)

        self.date_from = date_from
        self.date_to = date_to

        self.CalculationSpace = (
            acm.Calculations().CreateStandardCalculationsSpaceCollection())


    def _collect_data(self):

        tf = acm.FTradeSelection['OPS_NONBUSDAY']
        self._walk_trades(tf.Trades())


    def _walk_trades(self, trades):
        """To do."""

        for trade in trades:
            for money_flow in trade.MoneyFlows(self.date_from, self.date_to):
                if money_flow.Currency().Calendar().IsNonBankingDay(None, None, money_flow.PayDate()):
                    self._process_money_flow(money_flow)


    def _header(self):
        """Return data coluns header."""

        header = ([
            "Trade Number",
            "Acquirer",
            "Counterparty",
            "Trade Status",
            "Nominal",
            "Portfolio",
            "Trade Time",
            "Instrument",
            "Instrument Type",
            "Open Ended",
            "Instrument Currency",
            "Instrument Issuer",
            "Isin",
            "Cash Flow Type",
            "Pay Date",
            "Projected Value"
        ])

        return header


    def _process_money_flow(self, money_flow):
        """Process single money flow."""

        trade = money_flow.Trade()
        issuer = at_report.return_value_if_exists(trade.Instrument().Issuer(), "Name")
        portfolio = at_report.return_value_if_exists(trade.Portfolio(), "Name")
        projected = str(round(money_flow.Calculation().Projected(self.CalculationSpace).Number(), 2))

        single_line = (
            trade.Oid(),
            trade.AcquirerId(),
            trade.CounterpartyId(),
            trade.Status(),
            round(trade.Nominal(), 2),
            portfolio,
            trade.TradeTime(),
            trade.Instrument().Name(),
            trade.Instrument().InsType(),
            trade.Instrument().OpenEnd(),
            trade.Instrument().Currency().Name(),
            issuer,
            trade.Instrument().Isin(),
            money_flow.Type(),
            money_flow.PayDate(),
            projected
        )
        self.content.append(single_line)
