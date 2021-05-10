""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsCompare.py"

#-------------------------------------------------------------------------
def IsEqualAddInfos(obj1, obj2):
    keyFunc = lambda addInfo: addInfo.AddInf().Oid() if addInfo.AddInf() else 0
    obj1AddInfos = sorted(obj1.AddInfos(), key=keyFunc)
    obj2AddInfos = sorted(obj2.AddInfos(), key=keyFunc)

    equalAddinfos = len(obj1AddInfos) == len(obj2AddInfos)

    if equalAddinfos:
        for i in range(0, len(obj1AddInfos)):
            if obj1AddInfos[i].AddInf() != obj2AddInfos[i].AddInf() or\
               obj1AddInfos[i].FieldValue() != obj2AddInfos[i].FieldValue():
                equalAddinfos = False
                break

    return equalAddinfos