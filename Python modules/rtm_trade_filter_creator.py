"""
Description: 
    Create trade filters required for the trade migration script for RTM.
    Trade filters for trades settling on T+3, T+2, T+1 and the rest are
    created to allow for trade split during the trade migration.

Project:     Risk Transfer Mechanism
Developer:   Jakub Tomaga
Date:        06/12/2017
"""

import os
import acm
import csv
from at_ael_variables import AelVariableHandler


tf_filename_mask = "{0}_T+{1}"
tf_filename_mask_settled = "{0}_S"
offsets = [1, 2, 3]

# Trade filter template for trade settling on T+x
template = [
    ('', '', 'Portfolio', 'equal to', '%(portfolio)s', ''),
    ('And', '', 'Acquire Day', 'equal to', '%(offset)s', '')]

# Trade filter template for all the rest of the trades
template_all = [('', '', 'Portfolio', 'equal to', '%(portfolio)s', '')]
    

def get_trade_filter_matrix(template, params):
    """Return an FMatrix instance for trade filter."""
    matrix = acm.FMatrix()
    for template_row in template:
        row = [
            (item % params) if isinstance(item, basestring) else item
            for item in template_row
        ]
        matrix.AddRow(row)
        print(row)
    return matrix



ael_variables = AelVariableHandler()
ael_variables.add("input_file",
                  label="Input file")


def ael_main(config):
    input_file = config["input_file"]
    with open(input_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            skip = row[2]
            if skip == "FALSE":
                original_portfolio = row[0]
                target_portfolio = row[1]
                print(original_portfolio, len(original_portfolio))
                
                for offset in offsets:
                    params = {
                        'portfolio': original_portfolio,
                        'offset': '{0}db'.format(offset),
                    }

                    filtering_matrix = get_trade_filter_matrix(template, params)
                    name = tf_filename_mask.format(target_portfolio.split('_')[0].split(' Structures')[0], offset)
                    # Create a trade filter
                    print("Creating: ", name)
                    if acm.FTradeSelection[name]:
                        print("Skipping: {0}".format(name))
                        continue
            
                    try:
                        # Not possible to instantiate FTradeSelection (hence the clone)
                        tf = acm.FTradeSelection.Select('')[-1].Clone()
                        tf.Name(name)
                        tf.FilterCondition(filtering_matrix)
                        tf.Query(None)
                        tf.Owner("ATS")
                        print("Creating trade filter: {0}".format(name))
                        tf.Commit()
                    except Exception as ex:
                        print(ex)

                    
                params = {
                    'portfolio': original_portfolio,
                }
                filtering_matrix = get_trade_filter_matrix(template_all, params)
                name = tf_filename_mask_settled.format(target_portfolio.split('_')[0].split(' Structures')[0])
                # Create a trade filter
                print("Creating: ", name)
                tf = acm.FTradeSelection[name]
                if tf:
                    print("Skipping: {0}".format(tf.Name()))
                    continue
                try:
                    tf = acm.FTradeSelection.Select('')[-1].Clone()
                    tf.Name(name)
                    tf.FilterCondition(filtering_matrix)
                    tf.Query(None)
                    tf.Owner("ATS")
                    print("Creating trade filter: {0}".format(name))
                    tf.Commit()
                except Exception as ex:
                    print(ex)
                
    print("Completed successfully")
