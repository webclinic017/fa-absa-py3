"""
Reverse script for Commitment Fee Calculation
which resets the amount of payments based on report file
from previous run of CommFeeCalculation.py

12/05/2016 Evgeniya Baskaeva
ABITFA-4268 Adjustments to Comm Fee script /
ABITFA-4322 Comm Fee Reverse script
"""

from time import localtime, strftime
import ael, acm, csv
from at_ael_variables import AelVariableHandler


ael_variables = AelVariableHandler()
# Path to report file. Output from CommFeeCalculation.py
ael_variables.add_input_file(
    'file',
    label='File',
    cls='file',
    file_filter='*.xls'
)

# Columns of the file that are necessary for resetting the payments
COL_TRADE_NUMBER = 'Cash Payment Trade Number'
COL_NEXT_PAYDATE = 'Next Paydate'
COL_NEW_CUM_AMOUNT = 'New Cumulative Amount'


class CMFTrades(object):
    def __init__(self, trade_number, next_paydate, new_cum_amount):
        self.trade_number = trade_number
        self.trade = acm.FTrade[trade_number]
        if not self.trade:
            msg = "{0}: Trade couldn't be found".format(trade_number)
            raise ValueError(msg)
        try:
            self.next_paydate = ael.date(next_paydate)
        except Exception as e:
            msg = "{0}: Next Paydate value is not a date".format(self.trade_number)
            raise ValueError(msg)
        try:
            self.new_cum_amount = float(new_cum_amount)
        except Exception as e:
            msg = "{0}: New Cumulative value is not a float".format(self.trade_number)
            raise ValueError(msg)

    def update_payment(self):
        for payment in self.trade.Payments():
            is_comm_fee = payment.Type() == 'Commitment Fee'
            is_next_paydate = ael.date(payment.PayDay()) == self.next_paydate
            if is_comm_fee and is_next_paydate:
                msg = "{0}: Current amount for {1}: {2}".format(self.trade_number,
                                                                self.next_paydate,
                                                                payment.Amount())
                log_message(msg)
                payment.Amount(self.new_cum_amount)
                try:
                    payment.Commit()
                except Exception as e:
                    msg = "{0}: Couldn't commit to db: {1}".format(self.trade_number,
                                                                   e)
                    log_message(msg)
                else:
                    msg = "{0}: Payment committed to db: {1}".format(self.trade_number,
                                                                     self.new_cum_amount)
                    log_message(msg)
                return


def log_message(msg):
    time = strftime("%d.%m.%Y %H:%M:%S", localtime())
    print("{0}\t{1}".format(time, msg))


def ael_main(args):
    log_message("Script started")
    log_message("Input params: {0}".format(args))

    input_filename = str(args['file'])
    try:
        input_file = open(input_filename, 'rU')
        reader = csv.reader(input_file,
                            delimiter='\t',
                            dialect='excel')
    except IOError as e:
        msg = "The path to file is incorrect".format(input_filename, e)
        log_message(msg)
        return

    hrow = reader.next()
    # find indeces of columns
    i_trade_number = hrow.index(COL_TRADE_NUMBER)
    i_next_paydate = hrow.index(COL_NEXT_PAYDATE)
    i_new_cum_amount = hrow.index(COL_NEW_CUM_AMOUNT)

    for row in reader:
        try:
            try:
                trade_number = row[i_trade_number]
            except IndexError as e:
                break
            if not trade_number:
                break

            log_message("{0}: Running...".format(trade_number))
            trade_row = CMFTrades(trade_number,
                                  row[i_next_paydate],
                                  row[i_new_cum_amount])
            trade_row.update_payment()

        except Exception as e:
            log_message(e)

    input_file.close()
    log_message("Script finished\n\n")
