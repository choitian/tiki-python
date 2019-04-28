'''
Created on 2019-4-28

@author: tyh
'''
import syntax.parsing.State as State

class LookaheadLR(object):
	_initialItem = None
	_initialState =None
	States = {}
	ItemPool = {}
	
	def __init__(self,gram):
		self._gram = gram
		
	def MakeItem(self,prod,dot):
		hasv = State.Item.S_HashString(prod, dot)
		if hasv not in self.ItemPool:
			self.ItemPool[hasv] = State.Item(prod,dot)
		return self.ItemPool[hasv]
	
	def AddState(self,state):
		hs = state.HashString()
		if hs not in self.States:
			self.States[hs] = state
			return self.States[hs],True
		else:
			return self.States[hs],False
	
	def visitItem(self,item,uncheckedNonTerminal,visited):
		dotR = item.DotRight()
		if dotR and (not self._gram.IsTerminal[dotR]) and dotR not in visited:
			uncheckedNonTerminal.append(dotR)
			visited.add(dotR)		
			
	def Closure(self,state):
		uncheckedNonTerminal = []
		visited = set()
		for item in state.Items:				
			self.visitItem(item,uncheckedNonTerminal,visited)
		while uncheckedNonTerminal:		
			nonTerminal = uncheckedNonTerminal.pop()
			prods = self._gram.GetProductionsOfHead(nonTerminal)
			for prod in prods:
				item = self.MakeItem(prod,0)
				if item not in state.Items:
					state.Items.add(item)
					self.visitItem(item,uncheckedNonTerminal,visited)
						
			
	def BuildCanonicalCollection(self):
		self._initialItem = self.MakeItem(self._gram.Productions[-1],0)
		self._initialState = State.State()
		self._initialState.Items.add(self._initialItem)	
		self.AddState(self._initialState)
		uncheckedState = []
		uncheckedState.append(self._initialState)
		
		while uncheckedState:		
			state = uncheckedState.pop()
			self.Closure(state)	
			gotoTable ={}
			for item in state.Items:
				dotR = item.DotRight()
				if dotR !="":
					if dotR not in gotoTable:
						gotoTable[dotR] = State.State()
					peer = self.MakeItem(item.Production,item.Dot + 1)
					gotoTable[dotR].Items.add(peer)
								
			for onSymbol,targetState in gotoTable.items():				
				info = self.AddState(targetState)	
				result, added = info[0],info[1]
				if added:
					uncheckedState.append(result)
				state.GotoTable[onSymbol] = result
				