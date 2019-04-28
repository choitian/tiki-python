'''
Created on 2019-4-28
@author: tyh
'''
import re

SymbolEnd  = "__END__"
SymbolNull  = "__NULL__"
SymbolStart  = "__START__"
class Grammar(object):
    '''
    classdocs
    '''
    Productions = []
    FST = {}
    IsTerminal = {}
    Nullable = set()

    def __init__(self,file):
        '''
        Constructor
        '''
        content =""
        with open(file, 'r') as file:
            content = file.read()
            
        rSymbol = r"(\s*(?P<head>\w+)\s*)\:(?P<prods>((\s*\w+\s*)+(\s*\{.*\}\s*)?\|?)+)(\s*;)"
        pattern = re.compile(rSymbol)
        for mo in re.finditer(pattern, content):
            head = mo.group("head").strip()
            prods = mo.group("prods")          
            
            rProd = r"(?P<prod>(\s*\w+\s*)+)(\s*(?P<script>\{.*\})\s*)?\|?"
            pattern = re.compile(rProd)
            for mo in re.finditer(pattern, prods):
                production = Production()
                production.Head = head
                
                prod = mo.group("prod").split()
                production.Nodes = [node.strip() for node in prod if len(node)!=0]
                script = mo.group("script")
                production.script = script.strip() if script else "{}"
                
                self.Productions.append(production)
                
        if len(self.Productions)!=0:
            production = Production()
            production.Head = SymbolStart
            production.Nodes = [self.Productions[0].Head]
            production.script = "{}"
            self.Productions.append(production)
        
        self.computeAttributes()
    def GetProductionsOfHead(self,head):
        return [prod for prod in self.Productions if prod.Head==head]
        
    def CalcFst(self,symbols):
        fst = set()
        nullable = False
        for index,symbol in enumerate(symbols):
            if symbol != SymbolNull:
                if symbol in self.FST:
                    fst = fst.union(self.FST[symbol])
            
            if symbol not in self.Nullable:
                break
            
            if index == len(symbols) -1:
                nullable = True
        return fst,nullable        

    def computeAttributes(self):
        #initialize special symbols
        self.Nullable.add(SymbolNull)
        self.IsTerminal[SymbolEnd] = True
        self.FST[SymbolEnd] = set([SymbolEnd])
        
        #initialize IsTerminal & Nullable
        prodId = 0
        for prod in self.Productions:
            self.IsTerminal[prod.Head] = False
            self.FST[prod.Head] = set() 
            prod.Id = prodId
            prodId +=1    
        
        #if not exist in IsTerminal as not being a head,then Is Terminal.
        for prod in self.Productions:
            for symbol in prod.Nodes:
                if symbol not in self.IsTerminal:
                    self.IsTerminal[symbol] = True
                    self.FST[symbol] = set([symbol])   
                                     
        #iterate util nothing changed
        nothingChanged = False
        while not nothingChanged:
            nothingChanged = True
            for prod in self.Productions:
                info = self.CalcFst(prod.Nodes)
                fst = info[0]
                nullable = info[1]
                if nullable and (prod.Head not in self.Nullable):
                    self.Nullable.add(prod.Head)
                    nothingChanged = False
                    
                oldSize = len(self.FST[prod.Head])
                self.FST[prod.Head] =self.FST[prod.Head].union(fst)
                if len(self.FST[prod.Head]) > oldSize:
                    nothingChanged = False
                
        
class Production(object):
    Id = 0
    Head = ""
    Nodes = []
    Script = ""
    
    def IsNull(self):
        return len(self.Nodes)==1 and self.Nodes[0] == SymbolNull
    
    def HashString(self):
        hasv = self.Head
        hasv += "/" + "+".join(self.Nodes)
        return hasv
    