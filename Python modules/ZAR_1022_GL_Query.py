"""
---------------------------------------------------------------------------------------------------
MODULE
    ZAR_1022_GL_Query

DESCRIPTION
    Date                    :  17-07-2020
    Purpose                 :  Extends the logic of the SQL query that retrieves ZAR 1022 GL trades
    Department and Desk     :  Product Control Team
    Requester               :  Daveshin Chetty
    Developer               :  Qaqamba Ntshobane
    Jira Number             :  PCGDEV-449

===================================================================================================
---------------------------------------------------------------------------------------------------
"""

import acm
import re


def find_desk_books(desk_acronym):

    query_name = desk_acronym + '_1022_GL'
    return acm.FStoredASQLQuery[query_name]


def extend_query(desk_name):

    temp_table_list = []
    new_sql_text = ''
    table_unions = ''

    rollback_query_extension()

    sql = acm.FSQL['1022_GL_Trades']
    sql_text = sql.Text()

    list_of_compounds = find_desk_books(desk_name)

    if not list_of_compounds:
        raise ValueError('The desk name (acronym) given was not found')

    list_of_compounds = list_of_compounds.Query().Select()

    for compound in list_of_compounds:
        compound = compound.Name()
        temp_table_name = re.sub('[^0-9a-zA-Z]', '', compound)

        if temp_table_name[0].isdigit():
            temp_table_name = 'temp_' + temp_table_name

        temp_table_list.append(temp_table_name)
        temp_sql_text = sql_text

        temp_sql_text = temp_sql_text.replace('from', 'into\n    %s\nfrom' %temp_table_name)
        temp_sql_text = temp_sql_text+("\nand match_portfolio(t, '%s')\n" %compound)

        if compound == list_of_compounds[0].Name():
            new_sql_text = temp_sql_text
            continue
        new_sql_text += temp_sql_text.replace('/* update_method=0 */', '')

    for temp_table in temp_table_list:
        temp_table_unions = '\nselect\n    trdnbr\nfrom\n    '+temp_table

        if temp_table != temp_table_list[-1]:
            temp_table_unions += '\n\nunion\n'
        table_unions += temp_table_unions

    sql_text = new_sql_text + table_unions
    sql.Text(sql_text)
    sql.Commit()


def rollback_query_extension():

    sql = acm.FSQL['1022_GL_Trades']
    sql_text = sql.Text()
    sql_temp_text = acm.FSQL['1022_GL_Trades_temp'].Text()

    if sql_text != sql_temp_text:
        sql.Text(sql_temp_text)
        sql.Commit()
