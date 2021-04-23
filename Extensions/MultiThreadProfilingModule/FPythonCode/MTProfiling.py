
import acm

blockCalls = acm.FDictionary()
wutCount = acm.WorkUnitThreads().PoolSize()
startShiftSize = 2
endShiftSize = 256
factorShift = 2
maxBlockCalls = 100

def startMTProfiling(eii):
    blockCalls.Clear()
    hook = acm.GetFunction("callVAHook", 3)
    acm.FACMServer().RegisterCallVAHook(hook)
    print ("MT Call profiling enabled")

def stopMTProfiling(eii):
    acm.FACMServer().RegisterCallVAHook(None)
    print ("MT Call profiling disabled")
    
def callVAHook(time, block, args):
    if block.IsMTSafe():        
        calls = blockCalls.At(block)
        if calls:
            calls.Add(args.Clone())
        else:
            calls = acm.FArray()
            calls.Add(args.Clone())
            blockCalls.AtPut(block, calls)
            
def runProfiling(eii):
    tester = MultiThreadTester(blockCalls)
    tester.ProcessProfiledCalls()
    tester.OutputProfilingData()
            
class ProfilingData:
    def __init__(self, args, numberOfThreads, cost):
        self.m_args = args
        self.m_numberOfThreads = numberOfThreads
        self.m_cost = cost
        
    def Args(self):
        return self.m_args
        
    def NumberOfThreads(self):
        return self.m_numberOfThreads
        
    def Cost(self):
        return self.m_cost
        
class ProfilingDataHelper:
    def __init__(self, singleData, multiData):
        self.m_singleData = singleData
        self.m_multiData = multiData
        
    def SingleData(self):
        return self.m_singleData
        
    def MultiData(self):
        return self.m_multiData
        
class MultiThreadTester:
    def __init__(self, blockCalls):
        self.m_timeProfiler = acm.FTimeProfiler()
        self.m_profilingDataDictionary = acm.FDictionary()
        self.m_blockCalls = blockCalls
        self.m_minimumShiftsDictionary = acm.FDictionary()
        
    def ProcessProfiledCalls(self):
        defaultContext = acm.GetDefaultContext()
        module = self.GetModuleForStorage(defaultContext)
        if module:
            if self.BlockCalls():
                for block in self.BlockCalls().Keys():
                    i = 0
                    self.WriteToModule(defaultContext, module, block.DocKey(), 1, "True")
                    calls = self.BlockCalls().At(block)
                    argumentsArray = acm.FArray()
                    for args in calls:
                        if i < maxBlockCalls:
                            argumentsArray.Add(args)
                        else:
                            break
                        i = i + 1
                    self.RunTest(block, argumentsArray, startShiftSize, factorShift, endShiftSize)
                self.StoreFBlockInfoData(defaultContext, module)
        else:
            print ("No module selected")
        
    def RunTest(self, block, argumentsArray, start = 1, factor = 1, max = 1):
        self.StartProfiling(block)
        count = start
        self.MinimumShiftsDictionary().AtPut(block, 0)
        while count <=  max:
            for args in argumentsArray:
                newArgs = self.ModifyArguments(block, args, count)
                profilingDataSingle = self.CallBlockWithThreads(block, newArgs, count, 1)
                profilingDataMulti = self.CallBlockWithThreads(block, newArgs, count, wutCount)
                profilingDataHelper = ProfilingDataHelper(profilingDataSingle, profilingDataMulti)
                self.AddProfilingData(block, count, profilingDataHelper)
            numberOfThreads = self.GetMinimumThreads(block)            
            if numberOfThreads > 0:
                self.MinimumShiftsDictionary().AtPut(block, numberOfThreads)
                break
            count = count * factor
        self.EndProfiling(block)
        
    def CallBlockWithThreads(self, block, args, shifts, numberOfThreads):
        acm.WorkUnitThreads().PoolSize(numberOfThreads)
        minProfilingData = None
        i = 0
        while i < 10:
            try:
                results =  block.CallVA(args)
            except:
                print ("Could not call block ", block, " with args ", args)
            acm.WorkUnitThreads().PoolSize(wutCount)
            profilingData = self.GetProfilingResults(block, args, shifts, numberOfThreads)
            self.ClearProfilingData(block)
            if 0 == i or profilingData.Cost() < minProfilingData.Cost():
                minProfilingData = profilingData
            i = i + 1
        return minProfilingData
        
    def ModifyArguments(self, block, args, totalCount):
        modifiedArgument = None
        i = 0
        newArgs = []
        blockIsMethod = block.IsKindOf("FMethod")
        for arg in args:
            if (blockIsMethod and 0 == i) or modifiedArgument:
                newArgs.append(arg)
            else:
                modifiedArgument = self.GenerateVectorFromArgument(totalCount, arg)
                newArgs.append(modifiedArgument)
            i = i + 1
        if not modifiedArgument:
            print ("No argument to modify in argument list", args)
        return newArgs
    
    def StartProfiling(self, function):
        self.TimeProfiler().Profile(function)
        
    def EndProfiling(self, function):
        self.TimeProfiler().DropProfile(function)
        
    def GetProfilingResults(self, block, args, shifts, numberOfThreads):
        profile = self.TimeProfiler().GetProfile(block)
        profilingData = ProfilingData(args, numberOfThreads, profile.Cost())
        return profilingData
        
    def AddProfilingData(self, block, shifts, profilingData):
        shiftsDictionary = self.ProfilingDataDictionary().At(block)
        if shiftsDictionary:
            profilingDataArray = shiftsDictionary.At(shifts)
            if profilingDataArray:
                profilingDataArray.Add(profilingData)
            else:
                profilingDataArray = acm.FArray()
                profilingDataArray.Add(profilingData)
                shiftsDictionary.AtPut(shifts, profilingDataArray)
        else:
            profilingDataArray = acm.FArray()
            profilingDataArray.Add(profilingData)
            shiftsDictionary = acm.FDictionary()
            shiftsDictionary.AtPut(shifts, profilingDataArray)
            self.ProfilingDataDictionary().AtPut(block, shiftsDictionary)
        
    def ClearProfilingData(self, function):
        profile = self.TimeProfiler().GetProfile(function)
        profile.Clear()
        
    def OutputProfilingData(self):
        for block in self.ProfilingDataDictionary().Keys():
            shiftsDictionary = self.ProfilingDataDictionary().At(block)
            sortedKeys = shiftsDictionary.Keys().Sort()
            for shift in sortedKeys:
                profilingDataArray = shiftsDictionary.At(shift)
                print ("-----------------------------------")
                print ("block   ", block)
                print ("shifts  ", shift)
                for profilingDataHelper in profilingDataArray:
                    print ("    -----------------------------------")
                    print ("    ---------Single--------------------")
                    print ("    threads ", profilingDataHelper.SingleData().NumberOfThreads())
                    print ("    cost    ", profilingDataHelper.SingleData().Cost())
                    print ("    args    ", profilingDataHelper.SingleData().Args())
                    print ("    ---------Multi--------------------")
                    print ("    threads ", profilingDataHelper.MultiData().NumberOfThreads())
                    print ("    cost    ", profilingDataHelper.MultiData().Cost())
                    print ("    args    ", profilingDataHelper.MultiData().Args())
    
    def WriteToModule(self, context, module, functionString, minimumThreads, useMultiThreading):
        blockInfo = context.GetExtension(acm.FBlockInfo, acm.FBlock, acm.FSymbol(functionString))
        blockInfoTemplate = 'FBlock:' + str(functionString) + ' = \n\
            MT=' + useMultiThreading + ' \n\
            MWMT=' + str(minimumThreads) +' \n'
        context.EditImport('FBlockInfo', blockInfoTemplate, False, module)
        module.Commit()

    def StoreFBlockInfoData(self, defaultContext, module):
        for block in self.MinimumShiftsDictionary().Keys():
            numberOfThreads = self.MinimumShiftsDictionary().At(block)
            if numberOfThreads > 0:
                self.WriteToModule(defaultContext, module, block.DocKey(), numberOfThreads, "True")
            else:
                self.WriteToModule(defaultContext, module, block.DocKey(), 0, "False")
            
    def GetModuleForStorage(self, context):
        modules = self.FilterBuiltInModules(context.Modules())
        if modules.Size() > 0:
            module = acm.UX().Dialogs().SelectObject(acm.UX().SessionManager().Shell(), 'Select module for storing block information', 'FExtensionModule', modules, modules.At(0))
        else:
            print ("No modules found in default context")
        return module
    
    def FilterBuiltInModules(self, modules):
        notBuiltInModules = acm.FArray()
        if not modules == None:
            for module in modules:
                if not module.IsBuiltIn():
                    notBuiltInModules.Add(module)
        return notBuiltInModules
        
    def GetMinimumThreads(self, block):
        shiftsDictionary = self.ProfilingDataDictionary().At(block)
        sortedKeys = shiftsDictionary.Keys().Sort()
        optimalWut = 0
        for shift in sortedKeys:
            profilingDataArray = shiftsDictionary.At(shift)
            multiIsBetter = self.AnalyzeProfilingDataForShift(profilingDataArray)
            if multiIsBetter and 0 == optimalWut:
                optimalWut = shift
        return optimalWut
            
    def AnalyzeProfilingDataForShift(self, array):
        totalSingleDataCost = 0.0
        totalMultiDataCost = 0.0
        for proflingDataHelper in array:
            totalSingleDataCost = totalSingleDataCost + proflingDataHelper.SingleData().Cost()
            totalMultiDataCost = totalMultiDataCost + proflingDataHelper.MultiData().Cost()
        return totalSingleDataCost > totalMultiDataCost
    
    def GenerateVectorFromArgument(self, numberOfCalls, start):
        vector = acm.FArray()
        vector.Add(start)
        i = 1
        while i < numberOfCalls:
            newValue = start
            vector.Add(newValue)
            i = i + 1
        lot = acm.GetFunction('lot', 2)(vector, 1)
        return lot
        
    def TimeProfiler(self):
        return self.m_timeProfiler
        
    def ProfilingDataDictionary(self):
        return self.m_profilingDataDictionary
    
    def BlockCalls(self):
        return self.m_blockCalls
        
    def MinimumShiftsDictionary(self):
        return self.m_minimumShiftsDictionary

