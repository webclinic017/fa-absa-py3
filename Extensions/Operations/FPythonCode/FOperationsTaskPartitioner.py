""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTaskPartitioner.py"
import acm

from itertools import groupby

from FOperationsTaskManager import TaskManager
from FOperationsMethodChainParser import ParseMethodChain, CallMethodChain
from FOperationsExceptions import IncorrectMethodException

#-------------------------------------------------------------------------
class MethodChainPartitioner(TaskManager.Partitioner):

    #-------------------------------------------------------------------------
    def __init__(self, methodChainExtensionValue, idFunction):
        super(MethodChainPartitioner, self).__init__()
        self._methodChains = self._GetMethodChains(methodChainExtensionValue)
        self._idFunction = idFunction

    #-------------------------------------------------------------------------
    def PA_CreatePartitions(self, objects, nbrPartitions):
        partitions = [[] for _ in range(nbrPartitions)]

        counter = 0
        step = 1
        for position in sorted(self._CreatePositions(objects), key=len, reverse=True):
            partitions[counter].extend(position)
                
            counter += step

            if counter == nbrPartitions or counter == -1:
                step = 1 if counter == -1 else -1
                counter += step

        return partitions

    #-------------------------------------------------------------------------
    def _CreatePositions(self, objects):
        positions = []

        for _, items in groupby(sorted(objects, key=self._ComputeKey), key=self._ComputeKey):
            positions.append([self._idFunction(obj) for obj in items])

        return positions

    #-------------------------------------------------------------------------
    def _ComputeKey(self, obj):
        keyvalues = [''.join([chain, '=', str(CallMethodChain(chain, obj))]) for chain in self._methodChains]
        return "-".join(keyvalues)

    #-------------------------------------------------------------------------
    def _GetMethodChains(self, methodChainExtensionValue):
        methodChains = []
        domain = methodChainExtensionValue.ExtendedClass()

        try:
            for chain in methodChainExtensionValue.Value().split(';'):
                chain = chain.split('.')
                lastMethod = ParseMethodChain(domain, chain)

                if lastMethod.Domain().IsClass():
                    idAttribute = lastMethod.Domain().IdentityAttribute()
                    method = idAttribute.GetMethod()
                    chain.append(str(method.Name()))

                methodChains.append('.'.join(chain))
        except IncorrectMethodException as e:
            raise IncorrectMethodException('Error detected when processing method chains in {}: {}'.format(
                                            methodChainExtensionValue.Name(), str(e)))

        return methodChains
