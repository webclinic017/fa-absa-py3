

import unittest

import acm

class TestIndexedCollection(unittest.TestCase):
    def test_slice(self):
        """SPR 269754 - Slicing acm-arrays behaves differently from slicing python arrays"""
        def _test_slice(a,b):
            for i in range(-10,11):
                for j in range(-10,11):
                    self.assertEqual(list(a[i:j]), list(b[i:j]))                                           
        _test_slice(list(range(6)), list(range(6)))    
        _test_slice(list(range(6)), acm.FVariantArray().AddAll(list(range(6))) )
        _test_slice(list(range(0)), acm.FVariantArray().AddAll(list(range(0))) )
        _test_slice(list(range(0)), acm.FVariantArray().AddAll(list(range(0))) )





