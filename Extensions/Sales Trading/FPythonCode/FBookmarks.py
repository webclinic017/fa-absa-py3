""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FBookmarks.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FBookmarks

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""

import acm

class FBookmarks(object):
    def __init__(self, subType):
        self._userPrefs = acm.GetUserPreferences()
        self._subType = subType
        self._bms = self._userPrefs.Bookmarks()
    
    def Get(self, bms = None):
        if not bms:
            bms = self._Bookmarks()
        if bms.Includes(self._SubTypeSymbol()):
            return bms.At(self._SubTypeSymbol())
        else:
            return acm.FArray()
                    
    def GetBookmarksAsList(self,bms=None):
        bmsList = acm.FArray()
        for b in self.Get():
            if b.IsKindOf(acm.FPageGroup):
                bmsList.AddAll(b.InstrumentsRecursively())
            else:
                bmsList.Add(b)
        return bmsList

    def SubType(self):
        return self._subType
    
    def Toggle(self, obj):
        bms = self._Bookmarks()
        array = self.Get(bms)
        if self.IsIncluded(obj, bms):
            array.Remove(obj)
        else:
            array.Add(obj)
        bms.AtPut(self._SubTypeSymbol(), array)
        self._Set(bms)

    def IsIncluded(self, obj, bms = None):
        return not self.Get(bms).IndexOf(obj) is -1

    def _SubTypeSymbol(self):
        return acm.FSymbol(self._subType)
    
    def _Set(self, bms):
        self._userPrefs.Bookmarks(bms)
        self._userPrefs.Commit()

    def _Bookmarks(self):
        return self._userPrefs.Bookmarks()
        
    def IsDeleted(self):
        return False