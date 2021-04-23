class Publisher(object):
    def __init__(self, contentProvider, writers, logger = None, testMode = False):
        self.contentProvider = contentProvider
        self.testMode = testMode
        self.logger = logger
        enabled = True
        self.writersToEnabledStatus = dict(((w, enabled) for w in writers))

    def _publishStructure(self):
        cp = self.contentProvider
        for (columnInfo, infoID) in cp.Columns():
            self._addToWriters("addColumn", columnInfo, infoID)

        for (rootPositionInfo, infoID) in cp.RootPositions():
            self._addToWriters("addRootPosition", rootPositionInfo, infoID)

        for (positionInfo, infoID) in cp.Positions():
            self._addToWriters("addPosition", positionInfo, infoID)

    def _publishContent(self):
        if self.testMode:
            """
            Test code to assert that "local" and mocked "distributed" results in the same values
            Only valid when running in local mode.
            """
            distValueGenerator = self.contentProvider.ValuesDistributed()
            for (posInfoID, columnInfoID, result) in self.contentProvider.ValuesLocal():
                (dist_posInfoID, dist_columnInfoID, dist_result) = next(distValueGenerator)
                assert dist_posInfoID == posInfoID
                assert dist_columnInfoID == columnInfoID
                #print columnInfoID
                #print dist_result
                #print result
                assert dist_result == result
                
        for (posInfoID, columnInfoID, result) in self.contentProvider.Values():
            self._addToWriters("addResult", posInfoID, columnInfoID, result)

    def publish(self):
        self._publishStructure()
        self._publishContent()

    def _addToWriters(self, writerAddMethodStr, *args, **kwargs):
        enabledWriters = (w for (w, enabled) in 
                          self.writersToEnabledStatus.iteritems() if enabled)
        for enabledWriter in enabledWriters:
            try:
                writerAddMethod = getattr(enabledWriter, writerAddMethodStr)
                writerAddMethod(*args, **kwargs)
            except Exception as e:
                # disable the writer
                if self.logger:
                    self.logger.ELOG( "Disabling writer. %s" % str(e) )
                self.writersToEnabledStatus[enabledWriter] = False
