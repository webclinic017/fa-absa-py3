""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ConvertibleMarketMaking/etc/FCMMDataSourceListener.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCMMDataSourceListener

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""


class ValueInvoker(object):
    
    def __init__(self, quoteController, columns, callback):
        self._dataSourceDict = self.GetDataSources(quoteController, columns)
        self._unSavedDataSources = self.Sources()
        self.Callback = callback
        self._values = {}
        self.RunOrSetDependencies()
        
    def RunOrSetDependencies(self):
        for dataSource in reversed(self.Sources()):
            self.RemoveDependencies(dataSource)
            if self.Save(dataSource):
                self.Invoke()
            else:
                dataSource.AddDependent(self)
                
    def RemoveDependencies(self, dataSource):
        for dep in dataSource.Dependents(): 
            dataSource.RemoveDependent(dep)
            
    def PendingSources(self):
        
        def _SourceIfPending(ds):
            return ds if ds.IsValuePending() else None
        
        return list(map(_SourceIfPending, self.Sources()))
        
    def Ready(self):
        return (len(self._unSavedDataSources) == 0) and (len(filter(None, self.PendingSources())) == 0)
        
    @staticmethod
    def GetDataSources(qC, columns):
        return {qC.CreateDataSource(col_id):col_id for col_id in columns}
        
    def Invoke(self):
        if self.Ready():
            self.Execute()
            return True
        return False
    
    def Execute(self):
        self.Callback(self.Values())

    def ColumnFor(self, dataSource):
        return self._dataSourceDict.get(dataSource)

    def CreateValue(self, dataSource, value):
        return {self.ColumnFor(dataSource): value}
        
    def Save(self, dataSource):
        if not dataSource:
            return False
        value = dataSource.Get()
        if dataSource in self.PendingSources():
            return False
        else: 
            self.AppendValue(self.CreateValue(dataSource, value))
            self._unSavedDataSources.remove(dataSource)
            return True     

    def Sources(self):
        return self._dataSourceDict.keys()

    def Values(self):
        if self.Ready():
            return self._values
        return None

    def AppendValue(self, value):
        self._values.update(value)
    
    def ServerUpdate(self, sender, aspect, parameter):
        sender.RemoveDependent(self)
        if sender in self.Sources():
            if self.Save(sender):
                self.Invoke()