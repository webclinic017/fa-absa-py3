from __future__ import print_function
import acm
import timeit
import os

from whoosh.index import create_in
from whoosh.fields import *
from whoosh import index
from whoosh import analysis
from whoosh.filedb.filestore import RamStorage
from whoosh.index import FileIndex

from IndexSearchUtils import unicode_decode
from IndexSearchUtils import safe_name
import IndexSearchUtils

import time
import threading

import collections

import uuid

def create_uuid() :
    return str(uuid.uuid4())    

class Configuration(object) :
    def __init__(self, identifier, indexClass, indexAttributes, preloadClasses, filterFunction) :
        self.m_indexAttributes = indexAttributes.split(';')
        self.m_class = acm.GetClass(indexClass)
        self.m_preloadClasses = preloadClasses.split(';') if preloadClasses else []
        self.m_typeName = identifier
        self.m_filterFunction = filterFunction

    def IndexAttributes(self) :
        return self.m_indexAttributes

    def IndexClass(self) :
        return self.m_class;

    def PreloadClasses(self) :
        return self.m_preloadClasses

    def Identifier(self) :
        return unicode_decode(self.m_typeName) if self.m_typeName else unicode_decode(self.IndexClass().Name())

    def FilterFunction(self):
        return self.m_filterFunction


def get_configurations() :
    context = acm.GetDefaultContext()
    
    indexSearchDefinitions = context.GetAllExtensions('FIndexSearchDefinition')
    
    configurations = []
    
    for indexSearchDefinitionExtension in indexSearchDefinitions :
        indexSearchDefinition = indexSearchDefinitionExtension.Value()
        identifier = str(indexSearchDefinition.Identifier())
        indexClass = str(indexSearchDefinition.IndexClass())
        indexAttributes = str(indexSearchDefinition.IndexAttributes())
        preloadClasses = str(indexSearchDefinition.PreloadClasses())
        filterFunction = str(indexSearchDefinition.FilterFunction())

        configurations.append(Configuration(identifier, indexClass, indexAttributes, preloadClasses, filterFunction))

    return configurations


def create_index(configuration, parentTaskId, progressCB) :
    ii = None
    if configuration :
        indexTable = IndexTable(configuration, parentTaskId, progressCB)
        indexTable.create()
    
    return indexTable


class IndexTable(object) :
    def __init__(self, configuration, parentTaskId, progressCB):
        self.m_configuration = configuration
        self.m_filterFunction = self.filter_function_from_configuration()
        self.m_nameKey = 'Name' #self.m_configuration.IndexAttributes()[0] #the first is the 'name' key
        self.m_schema = self.create_schema_from_configuration(self.m_configuration)
        self.m_progressCB = progressCB
        self.m_indexing = False
        self.m_objects = None
        self.m_parentTaskId = parentTaskId
        self.m_testCount = 0

        self.m_objectsToUpdate = []
        self.m_objectsToRemove = []
        self.m_objectsToInsert= []

        self.m_pendingUpdates = set()

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self.m_objects:
            self.m_objects.RemoveDependent(self)

        self.m_objects = None

    def name_field(self) :
        return self.m_nameKey

    def index_fields(self) :
        return self.m_configuration.IndexAttributes()

    def log(self, message):
        IndexSearchUtils.log(message)

    def preload(self):
        if self.m_configuration.IndexClass():
            if self.m_configuration.IndexClass().IncludesBehavior(acm.FBusinessObject) :
                self.m_objects = self.m_configuration.IndexClass().Select('')
                self.m_objects.AddDependent(self)
        
                if self.m_configuration.PreloadClasses() :
                    for preloadClass in self.m_configuration.PreloadClasses():
                        aClass = acm.GetClass(preloadClass)
                        if aClass :
                            aClass.Select('')
                        else:
                            self.log('Error in preload, no class named: ' + preloadClass)
            else:
                self.log('Error, index class needs to inherit from FBusinessObject: ' + self.m_configuration.Identifier())
        else:
            self.log('Error, no index class for configuration: ' + self.m_configuration.Identifier())
    
    def ServerUpdate(self, sender, aspectSymbol, parameter):

        if not parameter.Oid() in self.m_pendingUpdates :
            if aspectSymbol == acm.FSymbol('insert'):
                self.m_objectsToInsert.append(parameter)
            elif aspectSymbol == acm.FSymbol('update'):
                self.m_objectsToUpdate.append(parameter)
            elif aspectSymbol == acm.FSymbol('remove'):
                self.m_objectsToRemove.append(parameter)
            
            self.m_pendingUpdates.add(parameter.Oid())

    def HandlePendingUpdates(self) :
        if self.indexing_done ():
            for db_object in self.m_objectsToInsert :
                self.insert_object(db_object)
            for db_object in self.m_objectsToUpdate :
                self.update_object(db_object)
            for db_object in self.m_objectsToRemove :
                self.remove_object(db_object)

            self.m_objectsToUpdate = []
            self.m_objectsToRemove = []
            self.m_objectsToInsert= []

            self.m_pendingUpdates = set()



    def insert_object(self, db_object) :
        self.log('Insert: ' + self.string_from_method_chain(db_object, self.m_nameKey))

        kwargs = self.create_kwargs_from_configuration(db_object, self.m_configuration)
        with self.m_ix.writer() as writer:
            self.add_document(writer, kwargs)

    def update_object(self, db_object) :
        self.log('Update: ' + self.string_from_method_chain(db_object, self.m_nameKey))
        self.remove_object(db_object)
        self.insert_object(db_object)

    def remove_object(self, db_object) :
        self.log('Remove: ' + self.string_from_method_chain(db_object, self.m_nameKey))

        with self.m_ix.writer() as writer:
            writer.delete_by_term('oid', db_object.Oid())

    def string_from_method_chain(self, currentObject, methodName) :
        values = []
        self.values_from_method_chain(currentObject, methodName.split('.'), values)

        return ''.join(values) if values else ''

    def values_from_method_chain(self, currentObject, indexAttributes, values) :
        if indexAttributes :
            if hasattr(currentObject, 'Class') :
                aClass = currentObject.Class()
                methodName = indexAttributes[0]
                indexAttributes = indexAttributes[1:]
                method = aClass.GetMethod(methodName, 0)
                if method :
                    aClass = method.Domain()
                    args = [currentObject]
                    currentObject = method.Call(args)
                    if hasattr(aClass, 'IncludesBehavior') and aClass.IncludesBehavior(acm.FCollection):
                        for obj in currentObject :
                            self.values_from_method_chain(obj, indexAttributes, values)
                    elif indexAttributes and not isinstance(currentObject, type('')):
                        self.values_from_method_chain(currentObject, indexAttributes, values)

                else:
                    self.log('Incorrect method chain: ' + '.'.join(indexAttributes) + '. No method ' + methodName + ' on class ' + aClass.Name())
                    currentObject = None

        if isinstance(currentObject, type('')) :
            values.append(currentObject)

            
    def create_kwargs_from_configuration(self, dbObject, configuration) :
        indexAttributes = configuration.IndexAttributes()
        kwargs = {}
        contents = []
        for methodChain in indexAttributes :
            values = []
            self.values_from_method_chain(dbObject, methodChain.split('.'), values)
            valuesAsString = unicode_decode(' '.join(values))
            kwargs[methodChain] =  valuesAsString
            contents.append(valuesAsString)

        #defaults
        kwargs['oid'] = dbObject.Oid()
        ##kwargs['content'] = u' '.join(contents)
        kwargs['icon']  = unicode_decode(dbObject.Icon())
        kwargs['moniker'] = acm.Hgc().MakeMoniker(dbObject, 'any')

        return kwargs 


    def create_schema_from_configuration(self, configuration) :
        indexAttributes = configuration.IndexAttributes()

        kwargs = {}
        analyzer = analysis.StemmingAnalyzer(stoplist=[])
        ngram_analyzer = analysis.StandardAnalyzer(stoplist=[]) | analysis.NgramFilter(minsize=1, maxsize=4)

        for methodChain in indexAttributes :
            kwargs[methodChain] = TEXT(stored=True, analyzer=ngram_analyzer)

        #defaults
        kwargs['oid'] = NUMERIC(stored=True, unique=True)
        #kwargs['content'] = TEXT(stored=True, analyzer=ngram_analyzer)
        kwargs['icon']  =TEXT(stored=True)
        kwargs['moniker'] =STORED()

        return Schema(**kwargs)

    def filter_function_from_configuration(self) :
        function = None
        filterFunction = self.m_configuration.FilterFunction()
        if  filterFunction:
            try :
                moduleName, functionName = filterFunction.split('.', 1)
                module = __import__(moduleName)
                function = getattr(module, functionName)
                if function.func_code.co_argcount != 1 :
                    print ('The filter function ' + filterFunction + ' is incorrect, it should only have one argument')
                    function = None
            except Exception as e:
                self.log(filterFunction)
                self.log(e.message)

        return function

    def filter(self, db_object):
        ret = True

        if self.m_filterFunction:
            try :
                ret = self.m_filterFunction(db_object)
            except Exception as e:
                self.log (e.message)

        return ret
    
    def collect_objects(self, start_time):
        self.log('*** Preloading ***')
        self.preload()
        elapsed = timeit.default_timer() - start_time
        self.log('Elapsed: ' + str(elapsed))
        self.log('*** Start collecting objects ***')
        objects = []
        db_objects = self.m_configuration.IndexClass().Select('')#.FromTo(5000, 5200) # fixme
        n = len(db_objects)

        for index, db_object in enumerate(db_objects):
            if self.filter(db_object) :
                object_name = self.string_from_method_chain(db_object, self.m_nameKey)
                try :
                    kwargs = self.create_kwargs_from_configuration(db_object, self.m_configuration)
                    objects.append(kwargs)

                    if n > 200 and index % (n / 200) == 0:
                        elapsed = timeit.default_timer() - start_time
                        msg = str(index) + '/' + str(n) + ' (' + '{0:.1f}'.format(100.0 * index / n) + '%) ' + '{0:.2f}'.format(elapsed)
                        self.log(msg)
                        if self.m_progressCB :
                            self.m_progressCB(self.m_parentTaskId, index, 2 * n, msg)


                except Exception as ex :
                    self.log(' --- ' + object_name)

        self.log('*** Finished collecting objects ***')

        if self.m_progressCB :
            self.m_progressCB(self.m_parentTaskId, n, 2 * n, '*** Finished collecting objects ***')


        return objects

    def add_document(self, writer, kwargs, index = None, n = None, start_time = None):
        try :
            writer.add_document(**kwargs)

            if n and start_time :
                if n > 200 and index % (n / 200) == 0:
                    elapsed = timeit.default_timer() - start_time
                    msg = str(index) + '/' + str(n) + ' (' + '{0:.1f}'.format(100.0 * index / n) + '%) ' + '{0:.2f}'.format(elapsed)
                    self.log(msg)
                    if self.m_progressCB :
                        self.m_progressCB(self.m_parentTaskId, n + index, 2 * n, msg)

        except Exception as ex :
            self.log(' --- ' + kwargs[self.m_nameKey])
            self.log(str(ex))

    def create_index(self, objects, start_time) :
        n = len(objects)
        msg = '*** Start creating index  (#' + str(n) + ') ****'
        self.log(msg)
        if self.m_progressCB :
            self.m_progressCB(self.m_parentTaskId, n, 2 * n, msg)

        self.m_ix = FileIndex.create(RamStorage(), self.m_schema, create_uuid())

        with self.m_ix.writer(limitmb=512) as writer:
            for index, kwargs in enumerate(objects):
                self.add_document(writer, kwargs, index, n, start_time)

            self.log('*** Commiting index ****')
            if self.m_progressCB :
                self.m_progressCB(self.m_parentTaskId, 2 * n - 1, 2 * n, '*** Commiting index ****')

        self.log('*** Finished creating index ****')
        if self.m_progressCB :
            self.m_progressCB(self.m_parentTaskId, 2 * n, 2 * n, '*** Finished creating index ****')

        elapsed = timeit.default_timer() - start_time
        self.log('Elapsed: ' + str(elapsed))

        self.m_indexing = False

    def indexing_done(self) :
        return not self.m_indexing

   
    def create(self, ) :
        self.m_indexing = True
        start_time = timeit.default_timer()

        objects = self.collect_objects(start_time)

        t = threading.Thread(target=self.create_index, args=(objects, start_time,))        
        t.start()            
