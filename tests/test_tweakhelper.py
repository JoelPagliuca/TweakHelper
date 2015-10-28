'''
Created on 29/10/2015

@author: Joel Pagliuca
'''
import unittest, re

from ClassHook import parse_class_dump, Method, HookedClass, METHOD_REGEX

class Test(unittest.TestCase):

    def setUp(self):
        self.dump1 = open('test_dump1', 'r').readlines()
        self.dump2 = open('test_dump2', 'r').readlines()
    
    def test_methodregex(self):
        self.assertIsNotNone(re.match(METHOD_REGEX, "-(void)login;"))
        self.assertIsNotNone(re.match(METHOD_REGEX, "- (*int)add;"))
        self.assertIsNotNone(re.match(METHOD_REGEX, "- (*int)add:(int)number;"))
        self.assertIsNotNone(re.match(METHOD_REGEX, "+ (*int)add:(int)number1 (int)number2;"))

    def test_parse1(self):
        res = parse_class_dump(self.dump1)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], HookedClass)
        self.assertEqual(len(res[0].methods), 1)
        m = res[0].methods[0]
        self.assertIsInstance(m, Method)
        self.assertEqual(len(m.params), 0)
        self.assertEqual(m.class_name, res[0].name)
        self.assertEqual(m.signature, "- (id)init;")
        self.assertEqual(m.name, "init")
        self.assertEqual(m.type, "id")
    
    def test_parse2(self):
        res = parse_class_dump(self.dump2)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)
        c1 = res[0]
        c2 = res[1]
        self.assertEqual(len(c1.methods), 3)
        self.assertEqual(len(c2.methods), 2)
        [m1, m2, _] = c1.methods
        [_, m5] = c2.methods
        
        self.assertEqual(m1.signature, "- (id)init;")
        self.assertEqual(m1.name, "init")
        self.assertEqual(m1.type, "id")
        
        self.assertEqual(m2.name, "login")
        self.assertEqual(m2.type, "void")
        
        self.assertEqual(m5.name, "destroy")
        self.assertEqual(m5.type, "void")
    
    def test_parse3(self):
        pass

if __name__ == "__main__":
    unittest.main()