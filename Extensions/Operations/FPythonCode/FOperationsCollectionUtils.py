""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsCollectionUtils.py"

#-------------------------------------------------------------------------
def PopObject(iterable, key):
    obj = None
    if iterable:
        try:
            obj = iterable.pop(key)
        except KeyError:
            pass
    return obj