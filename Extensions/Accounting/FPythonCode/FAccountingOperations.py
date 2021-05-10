""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingOperations.py"

#-------------------------------------------------------------------------
class Operation:
    CREATE = 'Create'
    UPDATE = 'Update'

#-------------------------------------------------------------------------
def CommitNew(obj):
    obj.Commit()

#-------------------------------------------------------------------------
def CommitUpdate(obj):
    if obj.IsClone():
        original = obj.Original()
        original.Apply(obj)
        original.Commit()
    else:
        obj.Commit()

#-------------------------------------------------------------------------
def GetOperations():
    return {Operation.CREATE : CommitNew, Operation.UPDATE : CommitUpdate}

#-------------------------------------------------------------------------
def GetOpForObject(obj):
    return Operation.UPDATE if obj.IsClone() else Operation.CREATE