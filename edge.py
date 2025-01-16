import random

class Edge:
    def __init__(self, source_node, dest_node, weight):
        self.source_node = source_node
        self.dest_node = dest_node
        self.weight = weight

    def clone(self, source_node, dest_node):
        clone = Edge(source_node, dest_node, self.weight)
        return clone