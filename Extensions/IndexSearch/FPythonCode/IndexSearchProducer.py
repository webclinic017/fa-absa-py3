from __future__ import print_function
import FPaceProducer
import acm
import IndexSearchCreator
import tempfile
import IndexSearchQueryTraits

from whoosh.index import create_in
from whoosh.fields import *
from whoosh import index
from whoosh import analysis
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import index
from whoosh import highlight

from IndexSearchConstants import TaskKeys
from IndexSearchUtils import unicode_decode
from IndexSearchUtils import unicode_encode


from Contracts_Tk_Messages_TkMessages import DisplayInformation

from shutil import rmtree

import time

class CleanHighlightFormatter(highlight.Formatter):
    def format_token(self, text, token, replace=False):
        # Use the get_text function to get the text corresponding to the
        # token
        tokentext = highlight.get_text(text, token, replace)

        # Return the text as you want it to appear in the highlighted
        # string
        return tokentext

def CreateProducer() :
    return ScopeProducer()

""" Class for query (child) task """
class QueryTask(FPaceProducer.Task): 
    def __init__(self):
        super(QueryTask, self).__init__()
            
    def ParentTraits(self):
        return self._producer.Traits()
            
    def SendResult(self, taskId, result):
        resultKey = IndexSearchQueryTraits.ResultKey()
        resultKey.id = 0
        self.SendInsertOrUpdate(taskId, resultKey, result)                         

    def GetSafeIcon(self, info) :
        icon = None
        try :
            icon = info['icon']
        except:
            pass

        if not icon :
            icon = 'Empty'

        return str(icon)

    def KeyValue(self, keyValue, key, value) :
        keyValue.key = key
        if not isinstance(value, basestring):
            value = unicode_encode(value)

        keyValue.value = value

    def CreateMatchedTerms(self, info) :
        matchedFields = set()

        for term in info.matched_terms() :
            matchedFields.add(term[0])

        terms = []
        for field in matchedFields :
            s = field + ': ' + info.highlights(field)
            terms.append(s)

        return ' '.join(terms)
        

    def CreateResultDescription(self, index, resultDescription, info, hasTerms) :
        for key, value in info.iteritems() :
            if key != 'moniker' :
                self.KeyValue(resultDescription.keyValues.add(), key, value)

        if hasTerms :
            self.KeyValue(resultDescription.keyValues.add(), 'terms', self.CreateMatchedTerms(info))

        di = resultDescription.displayInformation
        di.icon = self.GetSafeIcon(info)
        di.label.formatString = info[index.name_field()]

        # Facet?
        #di.groupLabel.formatString = self.Type()
        # Matched terms + highlights. Requires terms=True in search_page().
        #di.description.formatString = unicode_encode(info.highlights('content'))
        resultDescription.moniker.ParseFromString(str(info['moniker']))


    def ExtractResults(self, index, results):
        result = IndexSearchQueryTraits.Result()
        hasTerms = results.results.has_matched_terms()
        results.results.fragmenter = highlight.SentenceFragmenter(sentencechars='\n\t\r', maxchars=50)
        results.results.formatter = CleanHighlightFormatter()
        for info in results:
            self.CreateResultDescription(index, result.searchResults.add(), info, hasTerms)

        return result


    def DoSearch(self, index, taskId, query, page, pageSize) :
        if index :
            ix = index.m_ix
            #ix = index.open_dir(indexPath)

            with ix.searcher() as searcher:
                parser = MultifieldParser(index.index_fields(), schema=ix.schema)

                if parser:
                    query = parser.parse(query)

                    results = searcher.search_page(query, page, pageSize, terms=True)
                    found = results.scored_length()
                    result = self.ExtractResults(index, results)

                    result.page = results.pagenum
                    result.pageCount = results.pagecount
                    result.offset = results.offset + 1 if results.offset > 0 else 0 
                    result.pageLength = results.pagelen
                    result.total = len(results)
                    '''
                    #To slow...
                    try :
                        suggestion = searcher.correct_query(query, query)
                        if suggestion.query != query:
                            result.suggestion =  suggestion.string
                    except Exception as e:
                        print (e)
                    '''
                    try: 
                        self.SendResult(taskId, result)
                        self.SendInitialPopulateDone(taskId)

                    except:
                        pass

                    return results

    """Inherited from PaceProducer.Task"""
    def OnCreateTask(self, taskId, definition, parentTaskId, parentResultKey):
        query = definition.query
        page = definition.page
        pageSize = definition.pageSize
        
        index = self._producer.Index(parentTaskId)

        if index :
            self.DoSearch(index, taskId, query, page, pageSize)

    """Inherited from PaceProducer.Task"""
    def OnDestroyTask(self, taskId):
        pass 
    
class Progress(object) :
    def __init__(self, msg, i, n) :
        self.m_pos = 100 * i / n if n > 0 else 0   
        self.m_msg = msg

class ScopeProducer(FPaceProducer.Producer):
    def __init__(self):         
        super(ScopeProducer, self).__init__()
        self._taskName = TaskKeys.Scope
        self._lastPeriodicUpdateTime = 0
        self._periodicUpdatePeriodSeconds = 1
        self._indexCreators = {}
        self._progress = {}
        self._shouldSendInitialDone = []

    def Index(self, taskId) :
        return self._indexCreators.get(taskId, None)

    def OnProgress(self, taskId, i, n, msg) :
        self._progress[taskId] = Progress(msg, i, n)

    def PeriodicUpdateTimeOut(self):
        return (time.time() - self._lastPeriodicUpdateTime) > self._periodicUpdatePeriodSeconds

    """Inherited from FPaceProducer.Producer"""
    def OnDoPeriodicWork(self):
        if self.PeriodicUpdateTimeOut():
            for taskId, progress in self._progress.iteritems():
                self.SendProgress(taskId, progress.m_msg, progress.m_pos)

            self._progress = {}

            for index in self._indexCreators.keys() :
                self.OnIndexDone(index)
                self._indexCreators[index].HandlePendingUpdates()

            self._lastPeriodicUpdateTime = time.time()      
  
    """Inherited from FPaceProducer.Producer"""
    def OnCreateTask(self, taskId, definition):
        indexName = definition.indexName

        #self._indexPath = tempfile.mkdtemp()
        configurations = IndexSearchCreator.get_configurations()

        for configuration in configurations :
            if indexName == configuration.Identifier() :
                self._indexCreators[taskId] = IndexSearchCreator.create_index(configuration, taskId, self.OnProgress)
                self._shouldSendInitialDone.append(taskId)
                break
        
    def ShouldSendInitialDone(self, taskId) :
        return taskId in self._shouldSendInitialDone

    def OnIndexDone(self, index) :
        for taskId in self._indexCreators.keys():
            if self.IsIndexDone(taskId) and self.ShouldSendInitialDone(taskId):
                self.SendInitialPopulateDone(taskId)
                self._shouldSendInitialDone.remove(taskId)
        
                    
    """Inherited from FPaceProducer.Producer"""
    def OnDestroyTask(self, taskId):
        index = self.Index(taskId)

        if index:
            index.destroy()
            del self._indexCreators[taskId]

    """ Override method to register task creator by task name.
        Necessary to override if you are using child tasks. """
    def OnRegisterChildTaskCreators(self, taskCreatorByTaskName):
        taskCreatorByTaskName[TaskKeys.Query] = QueryTask

    def ValidQuery(self, taskId):
        return taskId in self._indexCreators

    def IsIndexDone(self, taskId):
        ret = False
        if self.ValidQuery(taskId) :
            ret = self._indexCreators[taskId].indexing_done()

        return ret
    
