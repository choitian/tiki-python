import re

class Grammar:
    SymbolEnd  = "__END__"
    SymbolNull  = "__NULL__"
    SymbolStart  = "__START__"
    Productions = []
    FST = {}
    IsTerminal = {}
    Nullable = set()

    def __init__(self,file):
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
            production.Head = self.SymbolStart
            production.Nodes = [self.Productions[0].Head]
            production.script = "{}"
            self.Productions.append(production)
        
        self.computeAttributes()
    
    def CalcFst(self,symbols):
        fst = set()
        nullable = False
        for index,symbol in enumerate(symbols):
            if symbol != self.SymbolNull:
                if symbol in self.FST:
                    fst = fst.union(self.FST[symbol])
            
            if symbol not in self.Nullable:
                break
            
            if index == len(symbols) -1:
                nullable = True
        return fst,nullable        

    def computeAttributes(self):
        #initialize special symbols
        self.Nullable.add(self.SymbolNull)
        self.IsTerminal[self.SymbolEnd] = True
        self.FST[self.SymbolEnd] = set([self.SymbolEnd])
        
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
                
        
class Production:
    Id = 0
    Head = ""
    Nodes = []
    Script = ""