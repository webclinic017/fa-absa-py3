import ael

ael_variables = []

EXCL_TABLES = ('trade_filter', 'credit_limit_par', 'parameter')

Q_TABLES = """
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
"""

Q_TABLE_COLUMNS = """
select column_name
from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME='%s'
"""

Q_LAST_UPDATE = """
    SELECT TOP 1 *
    FROM %s
    ORDER BY updat_time DESC
    """


def get_columns(table):
    query = Q_TABLE_COLUMNS % table
    res = ael.dbsql(query)[0]
    l = []
    for r in res:
        l.append(r[0])
    return l


def ael_main(ael_dict):
    tables = ael.dbsql(Q_TABLES)[0]
    print "TABLES: %d" %len(tables)
    for i,tbl in enumerate(sorted(tables), 1):
        table = tbl[0]
        print "%d) table '%s'" %(i, table)
        columns = get_columns(table)
        if table in EXCL_TABLES or 'updat_time' not in columns:
            continue
        
        Q = Q_LAST_UPDATE % table
        q = ael.dbsql(Q)[0]
        if q:
            vals = q[0]
            print list(zip(columns, vals))

    print "Completed successfully."
