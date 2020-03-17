from random import shuffle


class Node:

    def __init__(self, id, degree):
        self.id = id
        self.degree = degree


class Edge:
    def __init__(self, source, target):
        self.pair = set([source, target])


class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        self.edges = edges
        self.block_a = None
        self.block_b = None

    def add_node(self, id, degree):
        new_node = Node(id, degree)
        self.nodes.append(new_node)

    def add_edge(self, source, target):
        new_edge = Edge(source, target)
        if not new_edge in self.edges:
            self.edges.append(new_edge)

    def init_partition(self):
        shuffle(self.nodes)

        self.block_a = Block(self.nodes[:len(self.nodes) // 2], self.edges)
        self.block_b = Block(self.nodes[:len(self.nodes) // 2], self.edges)

    def contains_node(self, node):
        return node in self.nodes

    def contains_node_id(self, node_id):
        return node_id in [node.id for node in self.nodes]

    def contains_edge(self, edge):
        return edge in self.edges

    def calculate_gain(self, node):
        gain = 0
        set_for_calc = set([node.id])
        for edge in self.associated_edges(node):
            counterpart = (edge.pair - set_for_calc).pop()

            if not self.block_a.contains_node_id(counterpart):
                gain += 1
            else:
                gain -= 1
        return gain

    def associated_edges(self, node):
        for edge in self.edges:
            if node.id in edge.pair:
                yield edge


class Block(Graph):
    def __init__(self, nodes=[], edges=[]):
        super().__init__(nodes=nodes, edges=edges)