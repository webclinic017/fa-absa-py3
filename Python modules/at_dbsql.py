import acm

def dbsql_set_str(items):
    return "({0})".format(", ".join(map(str, items)))

class DBEnumHelper:
    """A helper class for dealing with enum values in DBSQL."""
    UNKNOWN_ENUM_TYPE = 'Unknown enum type:'

    # this dict can be used to translate shortcuts to full enum names
    SHORTCUTS = {'tstatus': 'tradestatus'}

    def __init__(self, as_tuple=False):
        """Initialization.

        as_tuple    - if true, return a tuple with int values rather than str

        """
        self.as_tuple = as_tuple

    def __getattr__(self, name):
        """Return the enum value-reading method.

        This allows for dynamic calls like enum.tradestatus('void', 'terminated').

        """

        # translate shortcuts
        if name in self.SHORTCUTS:
            name = self.SHORTCUTS[name]

        try:
            acm.EnumFromString(name, '')
        except RuntimeError, e:
            if self.UNKNOWN_ENUM_TYPE in str(e):
                raise

        # returns a tuple with int values
        def cond_func_list(*tags):
            return [acm.EnumFromString(name, tag) for tag in tags]

        # returns a list of values suitable for dbsql queries
        def cond_func(*tags):
            return dbsql_set_str(cond_func_list(*tags))

        if self.as_tuple:
            return cond_func_list
        else:
            return cond_func

def party_ids(names):
    """Return a string value of the list of party ids."""
    return dbsql_set_str(party_ids_list(names))

def party_ids_list(names):
    """Return a list of party ids."""
    stack = [acm.FParty[name] for name in names]
    result = []
    while stack: # recursion isn't cool anymore
        party = stack.pop()
        result.append(party)
        for child_party in party.Children():
            if child_party not in result and child_party not in stack:
                stack.append(child_party)

    return [party.Oid() for party in result]

def portfolio_ids_list(names):
    """Return a list of pf ids."""
    physical_pfs = []
    for name in names:
        pf = acm.FPhysicalPortfolio[name]
        if pf:
            if pf.Compound():
                physical_pfs.extend(pf.AllPhysicalPortfolios())
            else:
                physical_pfs.append(pf)

    return [p.Oid() for p in physical_pfs]

def portfolio_ids(names):
    """Return a string value of the list of pf ids."""
    return dbsql_set_str(portfolio_ids_list(names))

# publish the implicit string returning instance
enum = DBEnumHelper()

# publish the implicit tuple returning instance
enum_t = DBEnumHelper(as_tuple=True)

