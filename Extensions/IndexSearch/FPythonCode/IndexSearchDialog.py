import acm
import FUxCore

from IndexSearchConsumer import ScopeTaskConsumer
from IndexSearchConsumer import QueryTaskConsumer

from IndexSearchUtils import unicode_decode

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


class IndexSearchDialog (FUxCore.LayoutDialog):
    def __init__(self, query = ''):
        self.m_openBtn = None
        self.m_searchInput = None
        self.m_suggestionLink = None
        self.m_suggestionInfo = None
        self.m_list = None
        self.m_resultInfo = None
        self.m_previousLink = None
        self.m_nextLink = None
        self.m_typed = False
        self.m_progressCtrl = None
        self.m_currentPage = 1
        self.m_query = query
        self.m_scopePaceConsumer = ScopeTaskConsumer.Create(self.IndexName(), self.OnScopeTaskConsumerResult, self.OnScopeTaskConsumerProgress, self.OnScopeState, self.OnScopeInitialPopulateDone)
        self.m_queryPaceConsumer = QueryTaskConsumer(self.OnQueryTaskConsumerResult)
        self.m_startTime = timeit.default_timer()

    def OnScopeState(self, status, statusText):
        pass

    def OnScopeInitialPopulateDone(self) :
        pass

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

    def HandleApply( self ):
        self.Open()
        return None

    def Caption(self) :
        return ''

    def HandleDestroy(self):
        self.m_queryPaceConsumer.Destroy()

    def HandleCreate( self, dlg, layout):
        self.m_fuxDlg = dlg
        self.m_fuxDlg.Caption(self.Caption())

        self.m_openBtn = layout.GetControl('ok')

        self.m_searchInput = layout.GetControl('searchInput')
        self.m_searchInput.AddCallback( 'Changed', self.OnSearchChanged, self )
      
        self.m_suggestionLink = layout.GetControl('suggestionLink')
        self.m_suggestionLink.AddCallback('Activate', self.OnSuggestionLinkClicked, None)
        self.m_suggestionLink.Visible(False)

        self.m_suggestionInfo = layout.GetControl('suggestionInfo')
        self.m_suggestionInfo.Visible(False)

        self.m_list = layout.GetControl('resultList')
        self.m_list.AddCallback('DefaultAction', self.OnListClicked, self)
        self.m_list.AddCallback('SelectionChanged', self.OnListSelChanged, self)
        self.m_list.AddCallback( 'ContextMenu', self.OnListContextMenu, self)

        self.m_list.ShowColumnHeaders(True)
        self.PopulateColumns()
        self.m_list.EnableHeaderSorting(True)

        #self.m_fuxDlg.RegisterTimer( self.OnTimer, 100) 

        self.m_progressCtrl = layout.GetControl('indexProgress')

        self.m_resultInfo = layout.GetControl('resultInfo')
        #self.m_resultInfo.Editable(False)

        self.m_previousLink = layout.GetControl('previousLink')
        self.m_nextLink = layout.GetControl('nextLink')

        self.m_previousLink.SetData('Previous')
        self.m_nextLink.SetData('Next')

        self.m_previousLink.Enabled(False)
        self.m_nextLink.Enabled(False)

        self.m_previousLink.AddCallback('Activate', self.OnPreviousClicked, None)
        self.m_nextLink.AddCallback('Activate', self.OnNextClicked, None)

        self.m_searchInput.SetData(self.m_query)

        self.UpdateControls()

        if self.m_query :
            self.m_typed = True


    def PopulateColumns(self):
        pass

    def UpdateControls(self) :
        self.m_openBtn.Enabled(self.m_list.GetSelectedItem() != None)

    def OnSuggestionLinkClicked(self, cd, ud) :
        query = self.m_suggestionLink.GetData()
        self.m_suggestionLink.SetData('')
        self.m_suggestionLink.Visible(False)
        self.m_suggestionInfo.Visible(False)

    def OnPreviousClicked(self, cd, ud) :
        self.DoSearch(self.m_currentPage - 1)

    def OnNextClicked(self, cd, ud) :
        self.DoSearch(self.m_currentPage + 1)

    def OnTimer(self, ud):
        if self.m_typed :
            elapsed = timeit.default_timer() - self.m_startTypedTime

            if elapsed > 0.25 :
                self.DoSearch(1)
                self.m_typed = False

    def IndexName(self) :
        return u''

    def DoSearch(self, page) :
        query = unicode_decode(self.m_searchInput.GetData())
        self.m_currentPage = page
        self.m_startTime = timeit.default_timer()

        self.m_queryPaceConsumer.DoSearch(query, page, 20, self.m_scopePaceConsumer.PaceConsumer(), self.m_scopePaceConsumer.Scope())
            
    def OnSearchChanged(self, ud, cd) :
        #if not self.m_typed :
        #    self.m_startTypedTime = timeit.default_timer()

        #self.m_typed = True
        self.DoSearch(1)

    def Open(self):
        pass    

    def OnListClicked(self, ud, cd):
        self.Open()        

    def OnListSelChanged(self, ud, cd):
        self.UpdateControls()

    def BuildContextMenu(self, menuBuilder):
        pass

    def OnListContextMenu(self, ud, cd):
        self.BuildContextMenu(cd.At('menuBuilder'))
    def AddListItem(self, root, info, select) :
        pass

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

    def UpdateSuggestionIfNeeded(self, resultInfo) :
        self.m_suggestionLink.SetData(str(resultInfo.m_suggestion))
        self.m_suggestionLink.Visible(True if resultInfo.m_suggestion else False)
        self.m_suggestionInfo.Visible(True if resultInfo.m_suggestion else False)

    def PopulateList(self, resultInfo, elapsed_time):
        self.m_list.RemoveAllItems()
        root = self.m_list.GetRootItem()
        self.UpdateSuggestionIfNeeded(resultInfo)
        self.UpdateResultInfo(resultInfo, elapsed_time)
        first = True
        for info in resultInfo.m_infos :
            if info :
                self.AddListItem(root, info, first)
                first = False

        self.UpdateControls()


    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox()
        b.  BeginHorzBox()
        b.      AddInput('searchInput', '')
        b.  EndBox()
        b.  BeginVertBox()
        b.      AddLabel('suggestionInfo', 'Did you mean:')
        b.      AddHyperLink('suggestionLink')
        b.      AddList('resultList', 20, -1, 177)
        b.  EndBox()
        b.  BeginHorzBox()
        b.      AddHyperLink('previousLink', 40, 40)
        b.      AddFill()
        b.      AddLabel('resultInfo', '                                                                                                       ')
        b.      AddFill()
        b.      AddHyperLink('nextLink', 25, 25)
        b.  EndBox()
        b.  AddProgress('indexProgress', 1, 10, -1, 10)
        b.  BeginHorzBox()
        b.      AddFill()
        b.      AddButton('ok', 'Open')
        b.      AddButton('cancel', 'Close')
        b.  EndBox()
        b.EndBox()
        return b
