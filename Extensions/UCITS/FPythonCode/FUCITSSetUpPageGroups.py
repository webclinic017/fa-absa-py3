""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/UCITS/etc/FUCITSSetUpPageGroups.py"

"""-------------------------------------------------------------------------------------------------------
MODULE
    FUCITSSetUpPageGroups

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from FAssetManagementUtils import logger

class SetUpPageGroups(object):

    UCITSBlacklists = ('Precious metals', 'Disallowed derivatives', 'Disallowed MM instruments', 'Disallowed securities')

    @staticmethod
    def IsSetUp():
        return PagesSetup.GetBlacklistsRoot() and PagesSetup.GetUCITSGroup() and \
               all([PagesSetup.GetUCITSBlacklist(bl) for bl in SetUpPageGroups.UCITSBlacklists])

    @staticmethod
    def SetUp():
        PS = PagesSetup()
        PS.CreateBlacklistsRoot()
        PS.CreateUCITSGroup()
        for bl in SetUpPageGroups.UCITSBlacklists:
            PS.CreateUCITSBlacklist(bl)
        return False

class PagesSetup(object):

    def CreateBlacklistsRoot(self):
        self._CreatePageGroup('ExclusionList', None)

    @staticmethod
    def GetBlacklistsRoot():
        return PagesSetup._GetPageGroup('ExclusionList', None)

    def CreateUCITSGroup(self):
        self._CreatePageGroup('UCITS', self.GetBlacklistsRoot())

    @staticmethod
    def GetUCITSGroup():
        return PagesSetup._GetPageGroup('UCITS', PagesSetup.GetBlacklistsRoot())

    def CreateUCITSBlacklist(self, name):
        self._CreatePage(name, self.GetUCITSGroup())

    @staticmethod
    def GetUCITSBlacklist(name):
        return PagesSetup._GetPage(name, PagesSetup.GetUCITSGroup())

    @staticmethod
    def _GetPageGroup(groupName, superGroup):
        pageGroup = acm.FPageGroup[groupName]
        return pageGroup if pageGroup and pageGroup.SuperGroup() == superGroup else None

    def _CreatePageGroup(self, groupName, superGroup):
        assert superGroup is None or superGroup.IsKindOf(acm.FPageGroup), \
            superGroup + ' should be a PageGroup or None'
        pageGroup = acm.FPageGroup[groupName]
        if pageGroup:
            if pageGroup.SuperGroup() is not superGroup:
                raise RuntimeError(groupName + ' PageGroup has superGroup ' +
                                   pageGroup.SuperGroup().Name() + ' expected ' + superGroup.Name())
        else:
            pageGroup = acm.FPageGroup()
            pageGroup.Name = groupName
            pageGroup.SuperGroup = superGroup
            try:
                pageGroup.Commit()
                logger.DLOG('Committed PageGroup ' + groupName)
            except Exception as e:
                print(e)
                logger.DLOG('Could not commit PageGroup ' + groupName)

    @staticmethod
    def _GetPage(pageName, superGroup):
        page = acm.FPhysInstrGroup[pageName]
        return page if page and page.SuperGroup() == superGroup else None

    def _CreatePage(self, pageName, superGroup):
        assert superGroup is None or superGroup.IsKindOf(acm.FPageGroup), \
            superGroup + ' should be a PageGroup or None'
        page = acm.FPhysInstrGroup[pageName]
        if page:
            if page.SuperGroup() is not superGroup:
                raise RuntimeError(pageName + ' page has super group ' +
                                   page.SuperGroup().Name() + ' expected ' + superGroup.Name())
        else:
            page = acm.FPhysInstrGroup()
            page.Name = pageName
            page.SuperGroup = superGroup
            page.Terminal = True
            try:
                page.Commit()
                logger.DLOG('Committed page ' + pageName)
            except Exception as e:
                print(e)
                logger.DLOG('Could not commit page ' + pageName)