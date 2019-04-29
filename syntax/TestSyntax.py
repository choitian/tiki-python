import unittest
import os 
import syntax.grammar.Grammar as Grammar
import syntax.parsing.LookaheadLR as LookaheadLR
import syntax.parsing.State as State

class TestSyntax(unittest.TestCase):
    def setUp(self):
        self.info = "....."
        
    def test_Grammar(self):
        #on re_grammar.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/re_grammar.txt") 
        self.assertEqual(len(gram.Nullable),1, 'Nullable.Size is wrong')
        
        for symbol,fst in gram.FST.items():
            if symbol =="exp":
                expectFst = "ARRAY CHAR DOT LITERAL LPAREN"
                self.assertEqual((" ".join(sorted(fst))),expectFst, "Fst of '%s' is wrong" % symbol)
        
        #on dnf.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/dnf.txt") 
        self.assertEqual(len(gram.Nullable),4, 'Nullable.Size is wrong')
        self.assertTrue("ini_exp" in gram.Nullable, 'ini_exp is not nullable')
        
        for symbol,fst in gram.FST.items():
            if symbol =="exp":
                expectFst = "DEC FALSE FLOATING ID INC INTEGER LPAREN NEW NOT NULL SCOPE_ID STRING SUB TRUE"
                self.assertEqual((" ".join(sorted(fst))),expectFst, "Fst of '%s' is wrong" % symbol)

            if symbol =="ini_exp":
                expectFst = "BOOLEAN CHAR COMMA DEC FALSE FLOAT FLOATING ID INC INT INTEGER LPAREN NEW NOT NULL SCOPE_ID STATIC STRING SUB TRUE VOID"
                self.assertEqual((" ".join(sorted(fst))),expectFst, "Fst of '%s' is wrong" % symbol)
                
            if symbol =="method_definition":
                expectFst = "BOOLEAN CHAR FLOAT ID INT SCOPE_ID STATIC VOID"
                self.assertEqual((" ".join(sorted(fst))),expectFst, "Fst of '%s' is wrong" % symbol)                
                
                             
    def test_BuildCanonicalCollection(self):
        #on re_grammar.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/re_grammar.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        
        self.assertEqual(len(lalr.States.items()), 19, "%s size is wrong(expect %s,but is %s)" %("state",249,len(lalr.States)))
        
        kernelSum = 0
        gotoSum = 0
        for _,state in lalr.States.items():
            kernelSum += len(state.GetKernelItems())
            gotoSum += len(state.GotoTable.items())
        
        self.assertEqual(kernelSum, 24, "%s size is wrong(expect %s,but is %s)" %("kernelSum",24,kernelSum))
        self.assertEqual(gotoSum, 42, "%s size is wrong(expect %s,but is %s)" %("gotoSum",42,gotoSum))   
        
        #on dnf.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/dnf.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        
        self.assertEqual(len(lalr.States.items()), 245, "%s size is wrong(expect %s,but is %s)" %("state",249,len(lalr.States)))
        
        kernelSum = 0
        gotoSum = 0
        for _,state in lalr.States.items():
            kernelSum += len(state.GetKernelItems())
            gotoSum += len(state.GotoTable.items())
        
        self.assertEqual(kernelSum, 374, "%s size is wrong(expect %s,but is %s)" %("kernelSum",374,kernelSum))
        self.assertEqual(gotoSum, 1511, "%s size is wrong(expect %s,but is %s)" %("gotoSum",1511,gotoSum))  
        
    def test_ClosureWithLookahead(self):
        #on re_grammar.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/re_grammar.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        
        kernel = lalr.InitialItem
        dummyState = State.State()
        dummyState.Items.add(kernel)
        dummyState.AddLookahead(kernel, Grammar.SymbolEnd)
        lalr.ClosureWithLookahead(dummyState)
        
        DummyStateLookaheadSum = 0
        for _,lookaheadSet in dummyState.LookaheadTable.items():
            DummyStateLookaheadSum += len(lookaheadSet)
            
        self.assertEqual(DummyStateLookaheadSum, 86, "%s size is wrong(expect %s,but is %s)" %("DummyStateLookaheadSum",86,DummyStateLookaheadSum))
                
        #on dnf.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/dnf.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        
        kernel = lalr.InitialItem
        dummyState = State.State()
        dummyState.Items.add(kernel)
        dummyState.AddLookahead(kernel, Grammar.SymbolEnd)
        lalr.ClosureWithLookahead(dummyState)
        
        DummyStateLookaheadSum = 0
        for _,lookaheadSet in dummyState.LookaheadTable.items():
            DummyStateLookaheadSum += len(lookaheadSet)
            
        self.assertEqual(DummyStateLookaheadSum, 32, "%s size is wrong(expect %s,but is %s)" %("DummyStateLookaheadSum",32,DummyStateLookaheadSum))
    def test_BuildPropagateAndSpontaneousTable(self):
        #on re_grammar.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/re_grammar.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        lalr.BuildPropagateAndSpontaneousTable()
 
        spontaneousSum,propagateSum = 0,0
        for kernel in lalr.ItemPool.values():
            if kernel.IsKernel():
                spontaneousSum +=len(kernel.SpontaneousTable)
                propagateSum +=len(kernel.PropagateTable)
                
        self.assertEqual(spontaneousSum, 45, "%s size is wrong(expect %s,but is %s)" %("spontaneousSum",45,spontaneousSum))
        self.assertEqual(propagateSum, 47, "%s size is wrong(expect %s,but is %s)" %("propagateSum",47,propagateSum))       
            
        #on dnf.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/dnf.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        lalr.BuildPropagateAndSpontaneousTable()
 
        spontaneousSum,propagateSum = 0,0
        for kernel in lalr.ItemPool.values():
            if kernel.IsKernel():
                spontaneousSum +=len(kernel.SpontaneousTable)
                propagateSum +=len(kernel.PropagateTable)
                
        self.assertEqual(spontaneousSum, 2289, "%s size is wrong(expect %s,but is %s)" %("spontaneousSum",2289,spontaneousSum))
        self.assertEqual(propagateSum, 1240, "%s size is wrong(expect %s,but is %s)" %("propagateSum",1240,propagateSum))  
     
    def test_DoPropagation(self):
        #on re_grammar.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/re_grammar.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        lalr.BuildPropagateAndSpontaneousTable()
        lalr.DoPropagation()
        
        TestLookaheadSum = 0
        for state in lalr.States.values():
            for lookaheadSet in state.LookaheadTable.values():
                TestLookaheadSum += len(lookaheadSet)
        self.assertEqual(TestLookaheadSum, 154, "%s size is wrong(expect %s,but is %s)" %("TestLookaheadSum",154,TestLookaheadSum))  
 
        #on dnf.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/dnf.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        lalr.BuildPropagateAndSpontaneousTable()
        lalr.DoPropagation()
        
        TestLookaheadSum = 0
        for state in lalr.States.values():
            for lookaheadSet in state.LookaheadTable.values():
                TestLookaheadSum += len(lookaheadSet)
        self.assertEqual(TestLookaheadSum, 4791, "%s size is wrong(expect %s,but is %s)" %("TestLookaheadSum",4791,TestLookaheadSum))   

    def test_BuildParsingActionTable(self):
        #on re_grammar.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/re_grammar.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        lalr.BuildPropagateAndSpontaneousTable()
        lalr.DoPropagation()
        lalr.BuildParsingActionTable()     
        
        TestParsingActionSum = 0
        for state in lalr.States.values():
            TestParsingActionSum += len(state.ParsingActionTable)
            
        self.assertEqual(TestParsingActionSum, 125, "%s size is wrong(expect %s,but is %s)" %("TestParsingActionSum",125,TestParsingActionSum))
        
        lalr.toXML("re_grammar.xml") 
        
        #on dnf.txt
        gram = Grammar.Grammar(os.path.dirname(__file__) + "/test_env/dnf.txt") 
        lalr = LookaheadLR.LookaheadLR(gram)
        lalr.BuildCanonicalCollection()
        lalr.BuildPropagateAndSpontaneousTable()
        lalr.DoPropagation()
        lalr.BuildParsingActionTable()     
        
        TestParsingActionSum = 0
        for state in lalr.States.values():
            TestParsingActionSum += len(state.ParsingActionTable)
            
        self.assertEqual(TestParsingActionSum, 2780, "%s size is wrong(expect %s,but is %s)" %("TestParsingActionSum",2780,TestParsingActionSum))
        
        lalr.toXML("dnf.xml")       
        
if __name__ == '__main__':
    unittest.main()