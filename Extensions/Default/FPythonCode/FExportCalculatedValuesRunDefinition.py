class RunDefinition:
    def __init__(self, portfolioNames, tradeFilterNames, storedASQLQueryNames, chainedGrouperDefinition, columnConfigurations, distributedMode, calculationEnvironment, logger):
        (self.portfolioNames, self.tradeFilterNames, self.storedASQLQueryNames, self.chainedGrouperDefinition, self.columnConfigurations, self.distributedMode, self.calculationEnvironment, self.logger) = \
           (portfolioNames, tradeFilterNames, storedASQLQueryNames, chainedGrouperDefinition, columnConfigurations, distributedMode, calculationEnvironment, logger)

    def __str__(self):
        return "\n".join(["portfolioNames = %s" % str(self.portfolioNames),
                         "tradeFilterNames = %s" % str(self.tradeFilterNames),
                         "storedASQLQueryNames = %s" % str(self.storedASQLQueryNames),
                         "chainedGrouperDefinition = %s" % str(self.chainedGrouperDefinition),
                         "columnConfigurations = %s" % str(self.columnConfigurations),
                         "distributedMode = %s" % str(self.distributedMode),
                         "calculationEnvironment = %s" % str(self.calculationEnvironment)])
    

def createRunDefinition(portfolioNames,
                        tradeFilterNames,
                        storedASQLQueryNames,
                        chainedGrouperDefinition,
                        columnConfigurations,
                        distributedMode,
                        calculationEnvironment,
                        logger):
    return RunDefinition(portfolioNames = portfolioNames,
                         tradeFilterNames = tradeFilterNames,
                         storedASQLQueryNames = storedASQLQueryNames,
                         chainedGrouperDefinition = chainedGrouperDefinition,
                         columnConfigurations = columnConfigurations,
                         distributedMode = distributedMode,
                         calculationEnvironment = calculationEnvironment,
                         logger = logger) 
