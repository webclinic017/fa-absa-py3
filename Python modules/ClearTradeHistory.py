"""
This task removes trades from the recently used list of all
users, except those listed in the exclude field.
"""
import acm

KEY_RECENT = "recent"

PARM_SIMULATE = "simulate"
PARM_ARCHIVED = "archived"
PARM_EXCLUDE_USER = "exclude"


def _get_all_users():
    return [u for u in acm.FUser.Select("")]


ael_variables = [
    # [field_id,
    #  name, type,
    #  choices, default_value, mandatory, multi_choice,
    #  description, input_hook, enabled]
    [PARM_EXCLUDE_USER,
     "Exclude users", "FUser",
     _get_all_users(), None, 0, 1,
     "Users that should not have their histories cleared.", None, True],
    [PARM_ARCHIVED,
     "Archived", "bool",
     [True, False], False, 1, 0,
     "Only remove references to archived trades.", None, True],
    [PARM_SIMULATE,
     "Simulate", "bool",
     [True, False], False, 1, 0,
     "Log changes that would be applied, but don't apply changes.", None, True]
]


def _get_trade_from_preferences(recent_items, key):
    trades = recent_items.At(key)
    if trades:
        trade = trades[0]
        if trade and "ArchiveStatus" in dir(trade):
            return trade

    return None


def remove_recent_trades(user_name, archived, simulate):
    trade_count = 0
    all_preferences = acm.FPreferences.Select("name='%s' and user='%s'" % (user_name, user_name))
    if not all_preferences:
        pass  # print "No preferences for user: %s" % user_name
    elif len(all_preferences) > 1:
        print("*** More than one preference list for user: %s" % user_name)
    else:
        preferences = all_preferences[0]
        recent_items = preferences.FromArchive(KEY_RECENT)
        if recent_items:
            recent_items = recent_items.Clone()
            keys = [k for k in recent_items.Keys() if k.AsString().startswith("CInsDef")]
            for k in keys:
                should_remove = True
                if archived:
                    trade = _get_trade_from_preferences(recent_items, k)
                    if trade and not trade.ArchiveStatus():
                        should_remove = False

                if should_remove:
                    trade_count += 1
                    recent_items.RemoveKey(k)

        if trade_count:
            if simulate:
                print("  User %s has %i trade references that can be removed." % (user_name, trade_count))
            else:
                preferences.ToArchive(KEY_RECENT, recent_items)
                print("  Removing %i trade references from trade history for user: %s" % (trade_count, user_name))
                preferences.Commit()

    return trade_count


def ael_main(parameters):
    exclude_users = parameters[PARM_EXCLUDE_USER]
    simulate = parameters[PARM_SIMULATE]
    archived = parameters[PARM_ARCHIVED]

    if not exclude_users:
        exclude_users = []

    exclude_names = [u.Name() for u in exclude_users]
    user_names = [u.Name() for u in _get_all_users() if u.Name() not in exclude_names]

    user_count = 0
    total_trade_count = 0
    print("Checking %i users for trade history:" % len(user_names))
    for user_name in sorted(user_names):
        trade_count = remove_recent_trades(user_name, archived, simulate)
        total_trade_count += trade_count
        if trade_count:
            user_count += 1

    if simulate:
        print("%i users would have been updated." % user_count)
        print("%i trade references would have been removed." % total_trade_count)
    else:
        print("%i users updated." % user_count)
        print("%i trade references removed." % total_trade_count)
