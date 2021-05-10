""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsGenerators.py"

#-------------------------------------------------------------------------
# Generator for generating pairs of related objects.
#-------------------------------------------------------------------------
class PairGenerator(object):
    
    #-------------------------------------------------------------------------    
    class Compare:
        EQUAL = 0
        PREDECESSOR = 1
        SUCCESSOR = 2
        
    #-------------------------------------------------------------------------
    @staticmethod
    def __Next(objs):        
        try:
            obj = next(objs)
        except StopIteration as _:
            obj = None
        return obj
        
    #-------------------------------------------------------------------------
    @staticmethod
    def Generate(objs1, objs2, functor):
        obj1 = PairGenerator.__Next(objs1)
        obj2 = PairGenerator.__Next(objs2)
        
        while obj1 or obj2:
            
            compare = functor(obj1, obj2) if obj1 and obj2 else None
            
            if compare == PairGenerator.Compare.EQUAL:
                yield obj1, obj2
                obj1 = PairGenerator.__Next(objs1)
                obj2 = PairGenerator.__Next(objs2)
            
            elif (obj1 and not obj2) or compare == PairGenerator.Compare.PREDECESSOR:
                yield obj1, None
                obj1 = PairGenerator.__Next(objs1)
                
            elif (obj2 and not obj1) or compare == PairGenerator.Compare.SUCCESSOR:
                yield None, obj2
                obj2 = PairGenerator.__Next(objs2)
                
            