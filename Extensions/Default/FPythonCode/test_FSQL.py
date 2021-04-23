

import acm
import unittest



class TestFSQL(unittest.TestCase):
    """This class initialy introduces by SPR 271255"""
    def test_existance(self):
        self.assertTrue( hasattr(acm, "FSQL") )        
    def test_creation(self):
        newsql = acm.FSQL()
    def test_settingtext(self):
        newsql = acm.FSQL()        
        text = "a"*1000
        newsql.Text(text)
        self.assertEqual(text, newsql.Text())
        self.assertEqual(len(text), newsql.TextSize())
        newsql.Commit()
        newsql.Delete()
    def test_access(self):
        somesql = acm.FSQL.Select('').At(0)






