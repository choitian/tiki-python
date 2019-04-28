'''
Created on 2019-4-28

@author: tyh
'''

class State(object): 
    def __init__(self):
        self.Items = set()
        self.GotoTable = {}
        self.Id = 0      
    def HashString(self):
        hs = [item.HashString() for item in self.Items]
        ls = sorted(hs) 
        return "#".join(ls)
class Item(object):
    def __init__(self, prod,dot):
        self.Production = prod
        self.Dot = dot  
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
        
        
        
        
        
        
        
        
        
        
        
        