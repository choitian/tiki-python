'''
Created on 2019-4-28

@author: tyh
'''
import syntax.grammar.Grammar as Grammar
import syntax.parsing.State as State
import logging
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class LookaheadLR(object):
	def __init__(self,gram):
		self._gram = gram
		self.InitialItem = None
		self.InitialState =None
		self.States = {}
		self.ItemPool = {}
		
	def MakeItem(self,prod,dot):
		hasv = State.Item.S_HashString(prod, dot)
		if hasv not in self.ItemPool:
			self.ItemPool[hasv] = State.Item(prod,dot)
		return self.ItemPool[hasv]
	
	def AddState(self,state):
		hs = state.HashString()
		if hs not in self.States:
			state.Id = len(self.States)
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
		self.InitialItem = self.MakeItem(self._gram.Productions[0],0)
		self.InitialState = State.State()
		self.InitialState.Items.add(self.InitialItem)	
		self.AddState(self.InitialState)
		uncheckedState = []
		uncheckedState.append(self.InitialState)
		
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

	def visitItemWithLookahead(self,item,unchecked,visited,lookaheadSet):
		dotR = item.DotRight()
		if dotR and (not self._gram.IsTerminal[dotR]):
			for lookahead in lookaheadSet:
				tailingNodes = list(item.DotRightTailingNodes())
				tailingNodes.append(lookahead)
				info = self._gram.CalcFst(tailingNodes)
				fstSet = info[0]
				for fst in fstSet:
					key = dotR + "." + fst
					if key not in visited:
						visited.add(key)
						unchecked.append((dotR,fst))
			
	def ClosureWithLookahead(self,state):
		unchecked = []
		visited = set()
		for itemHash,lookaheadSet in state.LookaheadTable.items():
			item = self.ItemPool[itemHash]
			self.visitItemWithLookahead(item,unchecked,visited,lookaheadSet)
			
		while unchecked:		
			info = unchecked.pop()
			nonTerminal = info[0]
			lookahead = info[1]
			
			prods = self._gram.GetProductionsOfHead(nonTerminal)
			for prod in prods:
				item = self.MakeItem(prod,0)
				if state.AddLookahead(item,lookahead):
					self.visitItemWithLookahead(item,unchecked,visited,[lookahead])	
							
	def BuildPropagateAndSpontaneousTable(self):
		#kernels = [kernel for kernel in self.ItemPool if]
		for kernel in self.ItemPool.values():
			if kernel.IsKernel():
				dummyState = State.State()
				dummyState.Items.add(kernel)
				dummyState.AddLookahead(kernel, Grammar.SymbolEnd)
				self.ClosureWithLookahead(dummyState)
				
				for itemHash,lookaheadSet in dummyState.LookaheadTable.items():
					item = self.ItemPool[itemHash]
					if item.DotRight():
						for lookahead in lookaheadSet:
							hs = item.HashString()
							if lookahead!=Grammar.SymbolEnd:
								if hs not in kernel.SpontaneousTable:
									kernel.SpontaneousTable[hs] = set()
									
								kernel.SpontaneousTable[hs].add(lookahead)	
							else:
								kernel.PropagateTable.add(hs)
	def tryAddLookahead(self,unpropagated,state,item,lookaheadSet):
		dotRight = item.DotRight()
		peer = self.MakeItem(item.Production, item.Dot + 1)
		targetState = state.GotoTable[dotRight]
		for lookahead in lookaheadSet:
			if targetState.AddLookahead(peer,lookahead):
				info = (targetState, peer, lookahead)
				unpropagated.append(info)				
		
	def DoPropagation(self):
		unpropagated = []
		self.InitialState.AddLookahead(self.InitialItem, Grammar.SymbolEnd)
		info = (self.InitialState, self.InitialItem, Grammar.SymbolEnd)
		unpropagated.append(info)
		for state in self.States.values():
			for kernel in state.GetKernelItems():
				for itemHash,lookaheadSet in kernel.SpontaneousTable.items():
					item = self.ItemPool[itemHash]
					self.tryAddLookahead(unpropagated,state,item,lookaheadSet)
							
		while unpropagated:
			info = unpropagated.pop()
			fromState = info[0]
			fromItem = info[1]
			byLookahead = info[2]
			
			for itemHash in fromItem.PropagateTable:
				byItem = self.ItemPool[itemHash] 		
				self.tryAddLookahead(unpropagated,fromState,byItem,[byLookahead])
								
	def BuildParsingActionTable(self):
		for state in self.States.values():
			self.ClosureWithLookahead(state)
			
			for itemHash, lookaheadSet in state.LookaheadTable.items():
				item = self.ItemPool[itemHash]
				dotRight = item.DotRight()
				for lookahead in lookaheadSet:
					if dotRight:
						if self._gram.IsTerminal[dotRight]:
							action = ("shift",None)
							if dotRight in state.ParsingActionTable:
								actName = state.ParsingActionTable[dotRight][0]
								if actName=="reduce":
									actProd = state.ParsingActionTable[dotRight][1]
									logging.warning("Warning Conflicting(S/R),perfer shift: shift %s / reduce %s" %(dotRight,actProd.HashString()))
									state.ParsingActionTable[dotRight] = action
							else:
								state.ParsingActionTable[dotRight] = action	
					else:
						if item.Production.Head == Grammar.SymbolStart and lookahead ==Grammar.SymbolEnd:
							state.ParsingActionTable[lookahead] = ("accept",None)
						else:
							if lookahead in state.ParsingActionTable:
								actName = state.ParsingActionTable[lookahead][0]
								if actName=="reduce":
									actProd = state.ParsingActionTable[lookahead][1]
									logging.error("Error Conflicting(R/R): reduce %s / reduce %s" %(item.Production.HashString(),actProd.HashString()))
								elif actName=="shift":
									logging.warning("Warning Conflicting(S/R),perfer shift: shift %s / reduce %s" %(lookahead,item.Production.HashString()))
									
							else:
								state.ParsingActionTable[lookahead] = ("reduce", item.Production)	
	def toXML(self,xmlFile):
		root = ET.Element("root")
		for prod in self._gram.Productions:
			prodXML = ET.Element("production")
			prodXML.set("head", prod.Head)
			prodXML.set("nodes", "|".join(prod.Nodes))
			prodXML.set("script", prod.Script)
			prodXML.set("len", str(len(prod.Nodes)))
			prodXML.set("id", str(prod.Id))
			root.append(prodXML)
		for state in self.States.values():
			stateXml = ET.Element("state")
			stateXml.set("id", str(state.Id))	
			
			#append gotos
			for on,target in state.GotoTable.items():
				gotoXml = ET.Element("goto")
				gotoXml.set("on", on)
				gotoXml.set("state", str(target.Id))
				stateXml.append(gotoXml)
				
			#append actions	
			for on,actInfo in state.ParsingActionTable.items():
				actText = actInfo[0]
				if actText == "reduce":
					actProd = actInfo[1]
					actText = actText + str(actProd.Id)
				actionXml = ET.Element("action")
				actionXml.set("on", on)
				actionXml.set("do", actText)
				stateXml.append(actionXml)	
			root.append(stateXml)	
			
		xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
		with open(xmlFile, "w") as fxml:
			fxml.write(xmlstr)
			
			
			
			
			