"""
Department and Desk    : FX
Developer              : Bhavik Mistry

Description of script:
Script used to update a set of trade filters used for EOD reporting.
In order to restrict trades from being included in reports that have an
execution time of after 19h00

------------------------------------------------------------------------------
HISTORY

===============================================================================
Date        Change no       Developer           Description
-------------------------------------------------------------------------------
2015-01-18  CHNG            Bhavik Mistry       Initial version

"""

import acm
import ael
from at_ael_variables import AelVariableHandler

DATE_TODAY = acm.DateToday()

TF_FIELD_INDEX = 2
TF_VALUE_INDEX = 4

calendar = acm.FCalendar['ZAR Johannesburg']
TODAY = acm.Time().DateToday()
PREVBUSDAY = calendar.AdjustBankingDays(TODAY, -1)
NEXTBUSDAY = calendar.AdjustBankingDays(TODAY, 1)

# ===========================Helper functions==================================


def get_time_index(conditions):
    """
    Helper function to retrieve row index in which "Execution Time appears in
    trade filter
    :param conditions:  Trade filter conditions of type FMatrix
    :return: index of row / None
    """
    for i, condition in enumerate(conditions):
        if str(condition[TF_FIELD_INDEX]) == 'Execution time':
            return i


# ============================== Main ========================================
# AEL Variables
ael_variables = AelVariableHandler()
ael_variables.add('TradeFilters',
                  label='Trade Filters: ',
                  cls='FTradeSelection',
                  collection=acm.FTradeSelection.Instances(),
                  mandatory=True,
                  multiple=True)

ael_variables.add('Date',
                  label='Date: ',
                  cls='string',
                  collection=['TODAY', 'PREVBUSDAY', 'NEXTBUSDAY'],
                  default='TODAY',
                  mandatory=True,
                  multiple=False)


def ael_main(data):

    tf_list = data['TradeFilters']

    try:
        if data['Date'].upper() == 'TODAY':
            run_date = TODAY
        elif data['Date'].upper() == 'PREVBUSDAY':
            run_date = PREVBUSDAY
        elif data['Date'].upper() == 'NEXTBUSDAY':
            run_date = NEXTBUSDAY
        else:
            run_date = ael.date(data['Date'])
            run_date = data['Date']
    except Exception, e:
        acm.Log('Error parsing date input: ' + str(e))
        raise Exception('Error parsing date input: ' + str(e))

    CUT_OFF_TIME = acm.FSymbol(run_date + ' ' + '07:00:00 PM')

    for tf in tf_list:

        conditions = tf.FilterCondition()
        time_index = get_time_index(conditions)

        if time_index is None:
            exec_time_row = ['And',
                             '',
                             'Execution time',
                             'less equal',
                             CUT_OFF_TIME,
                             '']
            conditions.AddRow(exec_time_row)

            try:
                tf_clone = tf.Clone()
                tf_clone.FilterCondition(conditions)
                tf.Apply(tf_clone)
                tf.Commit()
                print(tf.Name(), ' - Date added')
            except Exception, e:
                acm.Log('Error commiting filter: ' + str(tf.Name()) + ' ' + str(e))

        else:
            exec_time_row = conditions[time_index]
            exec_time_row[TF_VALUE_INDEX] = CUT_OFF_TIME
            conditions[time_index] = exec_time_row

            try:
                tf_clone = tf.Clone()
                tf_clone.FilterCondition(conditions)
                tf.Apply(tf_clone)
                tf.Commit()
                print(tf.Name(), ' - Date amended')
            except Exception, e:
                acm.Log('Error commiting filter: ' + str(tf.Name()) + ' ' + str(e))
