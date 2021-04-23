from at_time import *
import acm
from at_ael_variables import AelVariableHandler
import datetime
import sys


ael_variables = AelVariableHandler()

ael_variables.add('instrument_names',
                  label='Instrument Names',
                  default='USD/BRENT/BBM/36406916,'
                          'USD/BRENT/BBM/OCT 15/SYN CALL,'
                          'USD/JET_CCN/BARC/,'
                          'USD/JET_CCN/40561023,'
                          'USD/JET_KEROCFS/BBM/',
                  alt='The names of the AbCap instruments')

ael_variables.add('africa_instrument_names',
                  label='Africa Instrument Names',
                  default='USD/BRENT/BR/150630-150930,'
                          'USD/BRENT/BR/150930-151030,'
                          'USD/JET_CCN/141001-141231/934.00,'
                          'USD/JET_CCN/150630-151231,'
                          'USD/JET_KEROCFS/141001-141231/115.8',
                  alt='The names of the instruments in the Africa environment')

ael_variables.add('business_date',
                  label='Business Date',
                  default='T',
                  alt='T is current business date, T-1 is the previous date')

ael_variables.add('price_sets',
                  label='Price Sets',
                  default='SPOT_MID,'
                          'SPOT_GMT+0,'
                          'SPOT_GMT+2,'
                          'SPOT_GMT+3,'
                          'SPOT_GMT+4',
                  alt='The price sets in the Africa instance,'
                      ' where the price will be saved.')

ael_variables.add('file_path',
                  label='File Path',
                  default='/apps/services/front/QUERIES/IMPORT/temp/CommodityPriceFile.amba.tbl',
                  alt='The fullpath of the AMBA message that will be saved')


# returns AMBA price block containing the settle price of the AbCap instrument
# saved against the Africa Instrument
def __get_current_price_block(instrument_name,
                            africa_instrument_name, business_date):
    ins = acm.FInstrument[instrument_name]

    query = acm.CreateFASQLQuery('FPrice', 'AND')
    query.AddAttrNode('Instrument.Oid', 'EQUAL', ins.Oid())
    query.AddAttrNode('Day', 'EQUAL', str(business_date))

    for price_entry in query.Select():
        return ['\n  [PRICE]\n    BITS=256\n    CURR.INSID=%s\n'
                '    DAY=%s\n    INSADDR.INSID=%s\n    PTYNBR.PTYID='
                % (ins.Currency().Name(),
                   business_date.strftime('%Y-%m-%d'),
                   africa_instrument_name),
                '\n    SETTLE=%s\n  [/PRICE]' % price_entry.Settle()]
    return []


def ael_main(parameters):
    instrument_names = parameters['instrument_names'].split(',')
    africa_instrument_names = parameters['africa_instrument_names'].split(',')
    business_date_str = parameters['business_date']
    file_path = parameters['file_path']
    price_set_list = parameters['price_sets'].split(',')

    if len(instrument_names) != len(africa_instrument_names):
        print 'Error : The number of items in the AbCap Instrument List'
        ' does not match that of the Africa Instrument List.'
        return
    
    # Get the businessdate for which this script is running
    if business_date_str == 'T':        
        business_date = date_today()
    elif business_date_str[:2] == 'T-':
        business_date = add_days(date_today(), -1*int(business_date_str[2:]))
    else:
        business_date = add_days(date_today(), int(business_date_str[2:]))
    try:
        with open(file_path, 'w') as ambafile:
            for index in range(len(instrument_names)):
	        instrument_name = instrument_names[index]
                africa_instrument_name = africa_instrument_names[index]
                price_block = []
                price_block = __get_current_price_block(instrument_name,
                                                        africa_instrument_name,
                                                        business_date)

                if len(price_block) > 0:
                    # build AMBA message block for instrument and price set
                    ambafile.write('[MESSAGE]\n  TYPE=INSERT_PRICE\n'
                                   '  VERSION=1.0\n  TIME=%s\n  SOURCE=PackageTagger'
                                   % business_date.strftime('%Y-%m-%d %H:%M:00'))
                    for price_set in price_set_list:
                        ambafile.write(price_block[0] + price_set + price_block[1])
                    ambafile.write('\n[/MESSAGE]\n')

        print 'Wrote secondary output to ' + file_path
    except IOError as e:
        print 'ERROR : Secondary output not created: I/O error({0}): {1}'.format(e.errno, e.strerror)
    except:
        print 'ERROR : Secondary output not created: Unexpected error:', sys.exc_info()[0]
