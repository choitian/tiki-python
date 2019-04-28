import unittest
import os
import syntax.grammar.Grammar as Grammar
import syntax.parsing.LookaheadLR as LookaheadLR

class TestSyntax(unittest.TestCase):
    def setUp(self):
        self.gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/dnf0.txt") 
        
    def test_Grammar(self):
        self.assertEqual(len(self.gram.Nullable),4, 'Nullable.Size is wrong')
        self.assertTrue("ini_exp" in self.gram.Nullable, 'ini_exp is not nullable')
        self.assertTrue("test_exp" in self.gram.Nullable, 'test_exp is not nullable')
        self.assertTrue("reini_exp" in self.gram.Nullable, 'reini_exp is not nullable')
        
        for symbol,fst in self.gram.FST.items():
            if symbol =="exp":
                expectFst = "DEC FALSE FLOATING ID INC INTEGER LPAREN NEW NOT NULL STRING SUB TRUE"
                self.assertEqual((" ".join(sorted(fst))),expectFst, "Fst of '%s' is wrong" % symbol)

            if symbol =="ini_exp":
                expectFst = "BOOLEAN CHAR COMMA DEC FALSE FLOAT FLOATING ID INC INT INTEGER LPAREN NEW NOT NULL STATIC STRING SUB TRUE VOID"
                self.assertEqual((" ".join(sorted(fst))),expectFst, "Fst of '%s' is wrong" % symbol)
                 
            if symbol =="postfix_exp":
                expectFst = "FALSE FLOATING ID INTEGER LPAREN NULL STRING TRUE"
                self.assertEqual((" ".join(sorted(fst))),expectFst, "Fst of '%s' is wrong" % symbol)
                
            if symbol =="method_definition":
                expectFst = "BOOLEAN CHAR FLOAT ID INT STATIC VOID"
                self.assertEqual((" ".join(sorted(fst))),expectFst, "Fst of '%s' is wrong" % symbol)
                             
    def test_LookaheadLR(self):
        lalr = LookaheadLR.LookaheadLR(self.gram)
        lalr.BuildCanonicalCollection()
        
        self.assertEqual(len(lalr.States.items()), 249, "%s size is wrong(expect %s,but is %s)" %("state",249,len(lalr.States)))
        
        
if __name__ == '__main__':
    unittest.main()