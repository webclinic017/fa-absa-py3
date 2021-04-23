from __future__ import print_function
import acm
import FUxCore

from IndexSearchConsumer import ScopeTaskConsumer
from IndexSearchConsumer import QueryTaskConsumer

from IndexSearchUtils import unicode_decode
from IndexSearchUtils import unicode_encode

import timeit

class ResultInfo :
    def __init__(self):
        self.m_infos = []
        self.m_page = 0
        self.m_pageCount = 0
        self.m_offset = 0
        self.m_foundCount = 0
        self.m_pageLength = 0
        self.m_total = 0
        self.m_suggestion = 0


class IndexSearcMultiPart(object):
    def __init__(self, configuration, ctrlKey, pageCount = 10):
        self.m_columnKeys = configuration.IndexAttributes()
        self.m_indexName = configuration.Identifier()
        self.m_ctrlKey = ctrlKey
        self.m_list = None
        self.m_resultInfo = None
        self.m_previousLink = None
        self.m_nextLink = None
        self.m_typed = False
        self.m_progressCtrl = None
        self.m_currentQuery = ''
        self.m_currentPage = 1
        self.m_pageCount = pageCount
        self.m_scopePaceConsumer = ScopeTaskConsumer.Create(self.IndexName(), self.OnScopeTaskConsumerResult, self.OnScopeTaskConsumerProgress, self.OnScopeState, self.OnScopeInitialPopulateDone)
        self.m_queryPaceConsumer = QueryTaskConsumer(self.OnQueryTaskConsumerResult)
        self.m_startTime = timeit.default_timer()

    def OnScopeState(self, status, statusText):
        pass

    def OnScopeInitialPopulateDone(self) :
        self.m_progressCtrl.Visible(False)

    def OnScopeTaskConsumerResult(self, result):
        pass

    def OnQueryTaskConsumerResult(self, consumerResults):
        resultInfo = ResultInfo()
        resultInfo.m_foundCount = consumerResults.foundCount
        resultInfo.m_page = consumerResults.page
        resultInfo.m_pageCount = consumerResults.pageCount
        resultInfo.m_offset = consumerResults.offset
        resultInfo.m_pageLength = consumerResults.pageLength
        resultInfo.m_total = consumerResults.total
        resultInfo.m_suggestion = consumerResults.suggestion

        for searchResult in consumerResults.searchResults :
            di = searchResult.displayInformation
            info = {
                'name': di.label.formatString,
                'icon': di.icon
            }
            for keyValue in searchResult.keyValues :
                info[keyValue.key] = keyValue.value

            if info :
                info['moniker'] = searchResult.moniker
                resultInfo.m_infos.append(info)

        self.PopulateList(resultInfo, timeit.default_timer() - self.m_startTime )

    def OnScopeTaskConsumerProgress(self, percent, progressText):
        if self.m_progressCtrl:
            self.m_progressCtrl.SetData(percent)

    def HandleDestroy(self):
        self.m_queryPaceConsumer.Destroy()

    def GetControl(self, layout, ctrlName) :
        return layout.GetControl(self.C(ctrlName))

    def HandleCreate( self, layout):
        self.m_list = self.GetControl(layout, 'resultList')
        self.m_list.AddCallback('DefaultAction', self.OnListClicked, self)
        self.m_list.AddCallback('SelectionChanged', self.OnListSelChanged, self)
        self.m_list.AddCallback( 'ContextMenu', self.OnListContextMenu, self)

        self.m_list.ShowColumnHeaders(True)
        self.PopulateColumns()
        self.m_list.EnableHeaderSorting(True)

        self.m_progressCtrl = self.GetControl(layout, 'indexProgress')

        self.m_resultInfo = self.GetControl(layout, 'resultInfo')

        self.m_previousLink = self.GetControl(layout, 'previousLink')
        self.m_nextLink = self.GetControl(layout, 'nextLink')

        self.m_previousLink.SetData('Previous')
        self.m_nextLink.SetData('Next')

        self.m_previousLink.Enabled(False)
        self.m_nextLink.Enabled(False)

        self.m_previousLink.AddCallback('Activate', self.OnPreviousClicked, None)
        self.m_nextLink.AddCallback('Activate', self.OnNextClicked, None)

        self.UpdateControls()

    def PopulateColumns(self):
        if self.m_columnKeys:
            self.m_list.AddColumn(unicode_encode(self.IndexName()), 200)
            self.m_list.AddColumn('Terms matched', 200)

    def UpdateControls(self) :
        #self.m_openBtn.Enabled(self.m_list.GetSelectedItem() != None)
        pass

    def OnPreviousClicked(self, cd, ud) :
        self.DoSearch(self.m_currentQuery, self.m_currentPage - 1)

    def OnNextClicked(self, cd, ud) :
        self.DoSearch(self.m_currentQuery, self.m_currentPage + 1)

    def IndexName(self) :
        return self.m_indexName

    def DoSearch(self, query, page) :
        self.m_currentQuery = query
        self.m_currentPage = page
        self.m_startTime = timeit.default_timer()

        self.m_queryPaceConsumer.DoSearch(query, page, self.m_pageCount, self.m_scopePaceConsumer.PaceConsumer(), self.m_scopePaceConsumer.Scope())
            

    def ObjectFromInfo(self, info) :
        obj = None
        try:
            m  = info['moniker']
            obj = acm.Hgc().ResolveMoniker(m.SerializeToString(), 'any')
        except Exception as e :
            print (e)

        return obj

    def Open(self):
        item = self.m_list.GetSelectedItem()
        if item :
            info = item.GetData()
            if info :
                obj = self.ObjectFromInfo(info)
                if obj :
                    applicationName = acm.UX().SessionManager().GetDefaultApplicationForDocument(obj.Class())
                    acm.UX().SessionManager().StartApplication(applicationName, obj)

    def OnListClicked(self, ud, cd):
        self.Open()        

    def OnListSelChanged(self, ud, cd):
        self.UpdateControls()

    def BuildContextMenu(self, menuBuilder):
        item = self.m_list.GetSelectedItem()
        if item :
            info = item.GetData()
            obj = self.ObjectFromInfo(info)
            if obj :
                acm.UX().Menu().BuildStandardObjectContextMenu(menuBuilder, [obj], False, None, None)

    def OnListContextMenu(self, ud, cd):
        self.BuildContextMenu(cd.At('menuBuilder'))

    def GetSafeIcon(self, info) :
        icon = None
        try :
            icon = info['icon']
        except:
            pass

        if not icon :
            icon = 'OpenFolder'

        return str(icon)

    def GetNameColumnKey(self) :
        return unicode_encode(self.m_columnKeys[0])

    def AddListItem(self, root, info, select) :
        if self.m_columnKeys :
            child = root.AddChild()
            child.Label(unicode_encode(info[self.GetNameColumnKey()]), 0)
            if 'terms' in info :
                child.Label(unicode_encode(info['terms']), 1)

            child.Icon(self.GetSafeIcon(info))
            child.SetData(info)
            child.Select(select)

    def UpdateResultInfo(self, resultInfo, elapsed_time) :
        found = resultInfo.m_foundCount
        page = resultInfo.m_page
        start = resultInfo.m_offset
        end = start + resultInfo.m_pageLength
        pageCount = resultInfo.m_pageCount
        total = resultInfo.m_total

        if total == 0:
            start = 0
            end = 0
        elif start != 0 :
            end -= 1
        else:
            start += 1
            
        
        s = 'Page %d of %d (%d-%d of %d) in %0.5f seconds' % (page, pageCount, start, end, total, elapsed_time)
        self.m_resultInfo.SetData(s)
        
        self.m_nextLink.Enabled(resultInfo.m_page < resultInfo.m_pageCount)
        self.m_previousLink.Enabled(resultInfo.m_page > 1)

    def PopulateList(self, resultInfo, elapsed_time):
        self.m_list.RemoveAllItems()
        root = self.m_list.GetRootItem()
        self.UpdateResultInfo(resultInfo, elapsed_time)
        first = True
        for info in resultInfo.m_infos :
            if info :
                self.AddListItem(root, info, first)
                first = False

        self.UpdateControls()

    def C(self, ctrlName) :
        return self.m_ctrlKey + ctrlName


    def BuildLayoutPart(self, builder):
        builder.BeginVertBox()
        builder.  BeginVertBox()
        builder.      AddList(self.C('resultList'), self.m_pageCount, self.m_pageCount, 50)
        builder.  EndBox()
        builder.  BeginHorzBox()
        builder.      AddHyperLink(self.C('previousLink'), 40, 40)
        builder.      AddFill()
        builder.      AddLabel(self.C('resultInfo'), '                                                                                                       ')
        builder.      AddFill()
        builder.      AddHyperLink(self.C('nextLink'), 25, 25)
        builder.  EndBox()
        builder.  AddProgress(self.C('indexProgress'), 1, 10, -1, 10)
        builder.EndBox()
