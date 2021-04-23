import acm

INDEX_ROW_VALUE = 4
INDEX_ROW_RELATION = 3

CORRECT_TIME = '12:00:00 AM'

def get_index_from(conditions):
    """ Find the index of the 'date from' part row in the filter conditions. """
    return get_index_relation(conditions, 'greater equal')

def get_index_to(conditions):
    """ Find the index of the 'date to' part row in the filter conditions. """
    return get_index_relation(conditions, 'less than')

def get_index_relation(conditions, relation):
    """ Find the index of the row in the conditions having the relation. """
    for i, condition in enumerate(conditions):
        if str(condition[INDEX_ROW_RELATION]) == relation:
            return i

def adjust_datetime(datetime):
    if not datetime:
        return datetime

    date, time, suffix = datetime.split(' ')
    time = time + ' ' + suffix

    if time != CORRECT_TIME:
        time = CORRECT_TIME
        date = acm.Time.DateAddDelta(date, 0, 0, 1)

    return date + ' ' + time

for trade_filter in acm.FTradeSelection.Select(''):
    if not trade_filter.Name().startswith('NOP_'):
        continue

    split_name = trade_filter.Name().split('_')
    if len(split_name) != 3:
        # The filter is not numbered.
        continue

    _, instype, number = split_name
    number = int(number)

    conditions = trade_filter.FilterCondition()
    index_from = get_index_from(conditions)
    index_to = get_index_to(conditions)
    if not index_from:
        continue

    date_from = str(conditions[index_from][INDEX_ROW_VALUE])
    date_to = None
    if index_to:
        date_to = str(conditions[index_to][INDEX_ROW_VALUE])

    field_name = str(conditions[index_from][2])

    if field_name == 'Time' and (not date_from.endswith(CORRECT_TIME) or (date_to and not date_to.endswith(CORRECT_TIME))):
        try:
            date_from = adjust_datetime(date_from)
            date_to = adjust_datetime(date_to)
        except Exception, ex:
            print(trade_filter.Name())
            print(trade_filter.FilterCondition())
            raise

        trade_filter_clone = trade_filter.Clone()

        date_from_condition = conditions[index_from]
        date_from_condition[INDEX_ROW_VALUE] = acm.FSymbol(date_from)
        conditions[index_from] = date_from_condition
        if index_to:
            date_to_condition = conditions[index_to]
            date_to_condition[INDEX_ROW_VALUE] = acm.FSymbol(date_to)
            conditions[index_to] = date_to_condition

        print(conditions)
        trade_filter_clone.FilterCondition(conditions)
        trade_filter.Apply(trade_filter_clone)
        trade_filter.Commit()

print("Completed successfully")

