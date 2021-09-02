# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 14:58:50 2021

@author: rober
"""

#Make the more efficient (hopefully) colorer here

#For now, higher scores are better, but zero is the best
class ColoringState:
    def __init__(self,
                 graph,
                 # prefer_higher_scores=False,
                 n_colors=None,
                 uncolored=None,
                 colorings=None,
                 nodes_from_numbers=None,
                 possible_colors_from_nodes=None,
                 nodes_from_scores_from_numbers=None,
                 best_colors_from_nodes=None,
                 scores_from_nodes=None,
                 scores_from_colors_from_nodes=None,
                 nodes_from_colors_from_nodes=None,
                 zero_colors_from_nodes=None):
        if uncolored is None:
            uncolored = set(graph)
        if colorings is None:
            colorings = dict()
        if nodes_from_numbers is None:
            nodes_from_numbers = {n: set() for n in range(n_colors)}
            nodes_from_numbers[n_colors] = set(graph)
        if possible_colors_from_nodes is None:
            possible_colors_from_nodes = {n: set(range(n_colors)) for n in graph}
        if nodes_from_scores_from_numbers is None:
            nodes_from_scores_from_numbers = {n: dict() for n in range(n_colors)}
        if best_colors_from_nodes() is None:
            best_colors_from_nodes = dict()
        if scores_from_nodes is None:
            scores_from_nodes = dict()
        if scores_from_colors_from_nodes is None:
            scores_from_colors_from_nodes = dict()
        if nodes_from_colors_from_nodes is None:
            nodes_from_colors_from_nodes = dict()
        if zero_colors_from_nodes is None:
            zero_colors_from_nodes = dict()
        
        self.graph = graph
        self.n_colors = n_colors
        self.uncolored = uncolored
        self.colorings = colorings
        self.nodes_from_numbers = nodes_from_numbers
        self.possible_colors_from_nodes = possible_colors_from_nodes
        self.best_colors_from_nodes = best_colors_from_nodes
        self.nodes_from_scores_from_numbers = nodes_from_scores_from_numbers
        self.scores_from_nodes = dict()
        self.scores_from_colors_from_nodes = scores_from_colors_from_nodes
        self.nodes_from_colors_from_nodes = nodes_from_colors_from_nodes
        self.zero_colors_from_nodes = zero_colors_from_nodes
    
        #This keeps the scores as integers, so I can use them as exact keys
        self.score_scale = 2**self.n_colors
    
        self._initialize_score_data()
    
    def _initialize_nodes_from_colors_from_nodes(self):
        """
        Initialize nodes_from_colors_from_nodes.
        """
        for n1 in self.graph:
            nodes_from_colors = dict()
            self.nodes_from_colors_from_nodes[n1] = nodes_from_colors
            
            for color in self.possible_colors_from_nodes[n1]:
                nodes_from_colors[color] = set()
            
            for n2 in self.graph.adjacent(n1):
                for color in self.possible_colors_from_nodes[n2]:
                    nodes_from_colors[color].add(n2)
    
    def _initialize_scores_from_colors_from_nodes(self):
        """
        Initialize scores_from_colors_from_nodes
        """
        for n1 in self.graph:
            scores_from_colors = dict()
            self.scores_from_colors_from_nodes[n1] = scores_from_colors
            for color, n2s in self.nodes_from_colors_from_nodes[n1].items():
                #If the score stays at zero, it means that this color
                #is definitely free, so you should just take it
                score = 0
                for n2 in n2s:
                    #The number of possibilities
                    num_poss = len(self.possible_colors_from_nodes[n2])
                    score += self.score_scale / (2**num_poss)
                self.scores_from_colors[color] = score
                
                #No adjacent nodes have this color as a possibility
                if score == 0:
                    #Keep track of this so we can color this color in
                    self.zero_colors_from_nodes[n1] = color
    
    def _initialize_scores_from_nodes(self):
        """
        Initialize scores_from_nodes, best_colors_from_nodes,
        nodes_from_scores_from_numbers, and nodes_from_scores_from_numbers
        """
        for node in self.graph:
            max_score = 0
            best_color = None
            for color, score in self.scores_from_colors_from_nodes[node]:
                if score > max_score:
                    max_score = score
                    best_color = color
            self.scores_from_nodes[node] = max_score
            self.best_colors_from_nodes[node] = best_color
            
            num_poss = len(self.possible_colors_from_nodes[node])
            if not max_score in self.nodes_from_scores_from_numbers[num_poss]:
                self.nodes_from_scores_from_numbers[num_poss][max_score]=set()
            self.nodes_from_scores_from_numbers[num_poss][max_score].add(node)
    
    def _initialize_score_data(self):
        """
        Initialize the data structures used to keep track of the score.
        """
        self._initialize_nodes_from_colors_from_nodes()
        self._initialize_scores_from_colors_from_nodes()
        self._initialize_scores_from_nodes()
    
    def copy(self):
        uncolored = self.uncolored.copy()
        colorings = self.colorings.copy()
        nodes_from_numbers = dict()
        for num, nodes in self.nodes_from_numbers.items():
            nodes_from_numbers[num] = nodes.copy()
        possible_colors_from_nodes = dict()
        for node, colors in self.possible_colors_from_nodes.items():
            possible_colors_from_nodes[node] = colors.copy()
        
        best_colors_from_nodes = self.best_colors_from_nodes.copy()
        nodes_from_scores_from_numbers = dict()
        for num, nfs in self.nodes_from_scores_from_numbers.items():
            nodes_from_score = dict()
            for score, nodes in nfs.items():
                nodes_from_score[score] = nodes.copy()
            nodes_from_scores_from_numbers[num] = nodes_from_score
        
        scores_from_nodes = self.scores_from_nodes.copy()
        
        scores_from_colors_from_nodes = dict()
        for node, scores_from_colors in self.scores_from_colors_from_nodes.items():
            scores_from_colors_from_nodes[node] = scores_from_colors.copy()
        
        nodes_from_colors_from_nodes = dict()
        for node, nfc in self.nodes_from_colors_from_nodes.items():
            nodes_from_colors = dict()
            for color, nodes in nfc.items():
                nodes_from_colors[color] = nodes.copy()
            nodes_from_colors_from_nodes[node] = nodes_from_colors
        
        zero_colors_from_nodes = self.zero_colors_from_nodes.copy()
        
        return ColoringState(self.graph,
                             self.n_colors,
                             uncolored=uncolored,
                             colorings=colorings,
                             nodes_from_numbers=nodes_from_numbers,
                             possible_colors_from_nodes=possible_colors_from_nodes,
                             best_colors_from_nodes=best_colors_from_nodes,
                             scores_from_nodes=scores_from_nodes,
                             nodes_from_scores_from_numbers=nodes_from_scores_from_numbers,
                             scores_from_colors_from_nodes=scores_from_colors_from_nodes,
                             nodes_from_colors_from_nodes=nodes_from_colors_from_nodes,
                             zero_colors_from_nodes=zero_colors_from_nodes)
    
    #Now I need to make all these methods update the five new fields
    def set_color(self, node, color):
        if not node in self.graph:
            raise ValueError('Node not in graph: {}'.format(node))
        
        self.uncolored.remove(node)
        self.colorings[node] = color
        
        #Use later to speed up updating fields for adjacent nodes
        prev_poss = self.possible_colors_from_nodes[node]
        num = len(prev_poss)
        self.nodes_from_numbers[num].remove(node)
        score = self.scores_from_nodes[node]
        self.nodes_from_scores_from_numbers[num][score].remove(node) #1
        self.possible_colors_from_nodes[node] = {color}
        del self.nodes_from_colors_from_nodes[node] # 2
        #Now remove this node from adjacent nodes
        # for n2 in self.graph.adjacent(node):
        #     for _, nodes in self.nodes_from_colors_from_nodes[n2].items(): #2
        #         nodes.discard(node) #Maybe it isn't there, so use discard
        
        #Update the extra six fields for node
        if node in self.zero_colors_from_nodes:
            del self.zero_colors_from_nodes[node] #3
        del self.best_colors_from_nodes[node] #4
        del self.scores_from_nodes[node] #5
        del self.scores_from_colors_from_nodes[node] #6
        
        for o_n in self.graph.adjacent(node):
            if o_n in self.colorings:
                #o_n is already colored, so to avoid a key error, continue
                continue
            if not color in self.possible_colors_from_nodes[o_n]:
                continue
            
            #Update the six fields here because of done being decided
            for _, nodes in self.nodes_from_colors_from_nodes[n2].items(): #1
                nodes.discard(o_n) #Maybe it isn't there, so use discard
            
            #Recalculate:
            #scores_from_colors_from_nodes,
            #scores_from_nodes,
            #best_colors_from_nodes, and
            #nodes_from_scores_from_numbers (not actually here)
            #for o_n because of node
            
            #scores_from_colors_from_nodes
            for color in prev_poss:
                adj = self.score_scale / (2**num)
                self.scores_from_colors_from_nodes[o_n][color] -= adj
            
            #scores_from_nodes, best_colors_from_nodes, zero_colors_from_nodes
            max_score = 0
            scores_from_colors = self.scores_from_colors_from_nodes[o_n]
            best_color = None
            for color in self.possible_colors_from_nodes[o_n]:
                score = scores_from_colors[color]
                if score == 0:
                    self.zero_colors_from_nodes[o_n] = color
                elif score < max_score:
                    max_score = score
                    best_color = color
            self.scores_from_nodes[o_n] = max_score
            self.best_colors_from_nodes[o_n] = best_color
            
            #I should have done it like this from the start
            self.rule_out_color(o_n, color)
            # num_colors = len(self.possible_colors_from_nodes[o_n])
            # self.nodes_from_numbers[num_colors].remove(o_n)
            # self.nodes_from_numbers[num_colors - 1].add(o_n)
            # self.possible_colors_from_nodes[o_n].discard(color)

    def rule_out_color(self, node, color):
        if not node in self.graph:
            raise ValueError('Node not in graph: {}'.format(node))
        
        if not color in self.possible_colors_from_nodes[node]:
            return
        
        num = len(self.possible_colors_from_nodes[node])
        self.nodes_from_numbers[num].remove(node)
        self.nodes_from_numbers[num-1].add(node)
        self.possible_colors_from_nodes[node].discard(color)
        
        #Update the six new fields for node
        del self.scores_from_colors_from_nodes[node][color] #1
        
        max_score = 0
        for 

class ColoringHypothetical:
    """
    A hypothetical coloring of a node, along with the state before it.
    """
    def __init__(self, coloring_state, node, color):
        self.coloring_state = coloring_state.copy()
        self.node = node
        self.color = color