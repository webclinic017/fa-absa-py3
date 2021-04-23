#  Developer                    : Heinrich Cronje, Willie van der Bank
#  Purpose                      : SND implementation, 2013 Upgrade - AddInfo function changed
#  Department and Desk          : Operations
#  Requester                    : Miguel
#  CR Number/Date               : 662927, 2013-10
import acm, exceptions

class SettlementCommitter(object):

    def __init__(self):
        self.__childrenToCommit = list()
        self.__parentToCommit = list()
        self.__SplitNetFlag = ''
        self.__AddInfoValue = ''
        
    def AddChild(self, newObject):
        self.__childrenToCommit.append(newObject)
    
    def AddParent(self, newObject):
        self.__parentToCommit.append(newObject)

    def SetSplitNetFlag(self, flag):
        self.__SplitNetFlag = flag
    
    def GetSplitNetFlag():
        return self.__SplitNetFlag
        
    def SetAddInfoValue(self, value):
        self.__AddInfoValue = value
    
    def GetAddInfoValue():
        return self.__AddInfoValue

    def __set_AdditionalInfoValue_ACM(self, entity, addInfoName, value):
        if entity.IsClone():
            entity.RegisterInStorage()

        if entity.AdditionalInfo().GetProperty(addInfoName) in (None, ''):
            addInfo = acm.FAdditionalInfo()
            addInfo.Recaddr(entity.Oid())
            addInfo.AddInf(acm.FAdditionalInfoSpec[addInfoName])
            addInfo.FieldValue(value)
        else:
            addInfo = acm.FAdditionalInfo.Select('recaddr = %i' %entity.Oid())
            for i in addInfo:
                if i.AddInf().Name() == addInfoName:
                    i.FieldValue(value)
        return addInfo
    
    def Commit(self):
        try:
            acm.BeginTransaction()
            parent = self.__parentToCommit[0]
            if parent.IsValidForSTP():
                parent.STP()
            parent.Commit()
            
            if self.__SplitNetFlag == 'Net':
                addInfo = self.__set_AdditionalInfoValue_ACM(parent, 'Call_Settle_Method', self.__AddInfoValue)
                try:
                    addInfo.Commit()
                except Exception, commitError:
                    self.__RaiseCommitException(commitError)

            for i in self.__childrenToCommit:
                if i.IsValidForSTP():
                    i.STP()
                i_clone = i.Clone()
                if self.__SplitNetFlag == 'Net':
                    i_clone.Parent(parent)
                elif self.__SplitNetFlag == 'Split':
                    i_clone.SplitParent(parent)
                i.Apply(i_clone)
                i.Commit()
                if self.__SplitNetFlag == 'Split':
                    addInfo = self.__set_AdditionalInfoValue_ACM(i, 'Call_Settle_Method', self.__AddInfoValue)
                    try:
                        addInfo.Commit()
                    except Exception, commitError:
                        self.__RaiseCommitException(commitError)
            acm.CommitTransaction()
        except Exception, commitError:
            self.__RaiseCommitException(commitError)

    def __RaiseCommitException(self, errorString):
        if (str(errorString).find("Update collision") != -1):
            msg = 'Error while committing netting for settlements! An update collision occurred.'
            acm.Log(msg)
            #raise UpdateCollisionException, errorString
        else:
            msg = 'Error while committing netting for settlements! Cause: %s.' %  errorString
            acm.Log(msg)
            #raise Exception, errorString


class UpdateCollisionException(exceptions.Exception):
    def init(self, args = None):
        self.args = args
