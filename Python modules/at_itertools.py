"""
Iteration tools. This is an extension of the tools provided by the standard
itertools module.

"""

import itertools

def groupby_multi(iterator, key, *keys):
    """Lazy grouping by multiple keys.

    Similar to itertools.groupby, the iterator must contain data sorted by
    all the provided keys in the same order.

    The difference between this and using itertools.groupby with a tuple
    key is that the grouping happens on separate levels for each key.

    Usage:
    Item = namedtuple('Item', 'a', 'b', 'payload')
    data = [Item(a=1, b=1, payload='foo'),
            Item(a=1, b=1, payload='bar'),
            Item(a=1, b=2, payload='baz'),
            Item(a=2, b=1, payload='foobar'),
            Item(a=2, b=2, payload='groupby_multi ftw')]

    for a_group, b_groups in groupby_multi(data, lambda i: i.a, lambda i: i.b):
        print 'a:', a_group
        for b_group, items in b_groups:
            print '\tb:', b_group
            for item in items:
                print '\t\t', item

    """

    for k, vals in itertools.groupby(iterator, key=key):
        if keys:
            vals = groupby_multi(vals, *keys)

        yield k, vals

