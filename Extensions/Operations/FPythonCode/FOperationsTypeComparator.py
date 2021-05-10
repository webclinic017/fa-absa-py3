""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTypeComparator.py"

#-------------------------------------------------------------------------
# Type comparator interface 
#-------------------------------------------------------------------------
class TypeComparator(object):
    
    def IsCorrectType(self, value):
        return False

    def GetExpectedType(self):
        return ''