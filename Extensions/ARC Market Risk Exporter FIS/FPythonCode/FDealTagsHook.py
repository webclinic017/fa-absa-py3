""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FDealTagsHook.py"
class DefaultTagCreator():
    @staticmethod
    def getTagTitles():
        return "Instrument Type,Currency,Counterparty,Book Node"

    def _getTagVals(self, bookNode, trade):
        instType = trade.Instrument().InsType()
        currency = trade.Currency().Name()
        counterpty = trade.Counterparty().Name()
        return "[{0},{1},{2},{3}]".format(instType, currency, counterpty, bookNode)


TAGCLASS = DefaultTagCreator
