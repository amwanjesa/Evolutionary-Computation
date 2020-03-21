from random import shuffle, randint, seed
from tqdm import tqdm
from block import Block

seed(42)


class Node:

    def __init__(self, id, degree):
        self.id = id
        self.degree = degree
        self.free = True


class Edge:
    def __init__(self, source, target):
        self.pair = set([source, target])


class Graph:
    def __init__(self, nodes=[], degrees=[], connections=[]):
        self.nodes = nodes
        self.degrees = degrees
        self.connections = connections
        self.freedoms = {}
        self.block_a = None
        self.block_b = None
        self.current_solution = []
        self.current_cutstate = None

    def add_node(self, new_node_id, degree):
        self.nodes.append(new_node_id)
        self.degrees.append(degree)
        self.freedoms[new_node_id] = True


    def remove_node(self, node):
        self.nodes.remove(node)

    def add_connection(self, connections):
        self.connections.append(connections)

    def init_partition(self):
        shuffle(self.nodes)
        halfway = len(self.nodes) // 2
        nodes_1 = self.nodes[:halfway]
        nodes_2 = self.nodes[halfway:]

        freedoms_1 = {k:v for k,v in self.freedoms.items() if k in nodes_1}
        freedoms_2 = {k:v for k,v in self.freedoms.items() if k in nodes_2}

        self.block_a = Block(
            nodes=nodes_1, freedoms=freedoms_1, max_degree=max(self.degrees))
        self.block_b = Block(
            nodes=nodes_2, freedoms=freedoms_2, max_degree=max(self.degrees))
    
    def setup_gains(self):
        for node in self.nodes:
            gain = self.calculate_gain(node)
            if self.block_a.contains_node(node):
                self.block_a.save_node_at_gain(node, gain)
            else:
                self.block_b.save_node_at_gain(node, gain)

    def calculate_gain(self, node):
        gain = 0
        node_block = self.block_a if self.block_a.contains_node(
            node) else self.block_b
        for net in self.critical_network(node):
            if all([node_block.contains_node(cell) for cell in net]):
                gain += 1
            else:
                gain -= 1
        return gain

    def create_network(self):
        nets = []
        counter = 0
        for i in self.connections:
            counter += 1
            for j in i:
                # intersection of i and connections[j]
                inters = list(set(i).intersection(
                    set(self.connections[int(j)-1])))
                if inters:
                    inters.extend([counter, j])
                    inters.sort()
                else:
                    inters.extend([counter, j])
                    inters.sort()
                if inters not in nets:
                    nets.append(inters)
        self.nets = nets

    def critical_network(self, base_cell):
        critical_network = []
        for network in self.nets:
            if str(base_cell) in network and len(network) < 4:
                critical_network.append(network)
        return critical_network

    def get_solution(self):
        solution = []
        for node in self.nodes:
            if self.block_a.contains_node(node):
                solution.append(1)
            else:
                solution.append(0)
        return solution

    def get_cutstate(self):
        cutstate = 0
        for node in self.block_a.nodes:
            for net in self.nets:
                if node in net:
                    if not all([self.block_a.contains_node(cell) for cell in net]):
                        cutstate += 1
        return cutstate

    def update_solution(self):
        new_cutstate = self.get_cutstate()
        if self.current_cutstate is not None:
            if new_cutstate < self.current_cutstate:
                self.current_solution = self.get_solution()
                self.current_cutstate = new_cutstate
        else:
            self.current_solution = self.get_solution()
            self.current_cutstate = new_cutstate

    def bipartitioning(self):
        largest_block = self.block_a if self.block_a.size > self.block_b.size else self.block_b
        possible_nodes = largest_block.get_free_node_with_highest_gain()
        node_index = randint(0, (len(possible_nodes)-1))
        node = list(possible_nodes)[node_index]
        # Remove node from current block and move it to the other one
        largest_block.remove_node(node)
        other_block = self.block_a if self.block_a.size > self.block_b.size else self.block_b

        # Mark moved node as not free
        other_block.add_node(node, False)
        # Updated gains using self.setup_gains
        self.setup_gains()

        # Select new node
        possible_nodes = other_block.get_free_node_with_highest_gain()
        node_index = randint(0, (len(possible_nodes)-1))
        node = list(possible_nodes)[node_index]
        # Remove node from current block
        other_block.remove_node(node)
        # Move it to the other block and Set node to false
        largest_block.add_node(node, False)
        largest_block.lock_node(node)
        # Gains update
        self.setup_gains()

        # Calculate new solution
        self.update_solution()

    def fiduccia_mattheyses(self):
        for _ in tqdm(range(4), desc='Fiduccia Mattheyses iterations'):
            if self.block_a.has_free_nodes() and self.block_b.has_free_nodes():
                self.bipartitioning()
            else:
                break
        return {'solution': self.current_solution, 'cutstate': self.current_cutstate}
