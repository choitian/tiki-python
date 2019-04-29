'''
Created on 2019-4-28

@author: tyh
'''
import syntax.grammar.Grammar as Grammar
from pygments.lexers.sql import lookahead

class State(object): 
    def __init__(self):
        self.Id = 0      
        self.Items = set()
        self.GotoTable = {}
        self.LookaheadTable = {}
        self.ParsingActionTable = {}
                
    def HashString(self):
        hs = [item.HashString() for item in self.Items]
        ls = sorted(hs) 
        return "#".join(ls)
    def GetKernelItems(self):
        return [item for item in self.Items if item.IsKernel()]
    def AddLookahead(self,item,lookahead):
        hs = item.HashString()
        if hs not in self.LookaheadTable:
            self.LookaheadTable[hs] = set()
            self.LookaheadTable[hs].add(lookahead)
            return True
        else:
            if lookahead not in self.LookaheadTable[hs]:
                self.LookaheadTable[hs].add(lookahead)
                return True
            else:
                return False
   
class Item(object):
    def __init__(self, prod,dot):
        self.Production = prod
        self.Dot = dot  
        self.SpontaneousTable = {}
        self.PropagateTable = set()
        
    def HashString(self):
        return self.S_HashString(self.Production,self.Dot) 
    @staticmethod
    def S_HashString(prod,dot):
        hasv = prod.Head
        hasv += "/" + "+".join(prod.Nodes)
        hasv += "." + str(dot)
        return hasv      
    def DotRight(self):       
        if self.Production.IsNull():
            return ""
        if self.Dot < len(self.Production.Nodes):
            return self.Production.Nodes[self.Dot]
        return ""
    
    def DotRightTailingNodes(self):     
        nodes = []
        if self.Production.IsNull():
            return nodes
        
        fromIndex = self.Dot + 1
        if fromIndex< len(self.Production.Nodes):
            nodes = self.Production.Nodes[fromIndex:]
        return nodes
        
    def IsKernel(self):
        if self.Production.IsNull():
            return False
        if self.Production.Head == Grammar.SymbolStart:
            return True
        
        return self.Dot !=0
        
        
        
        
        
        
        
        
        
        
        