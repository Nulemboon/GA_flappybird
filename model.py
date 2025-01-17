import neuron
import edge
import random

"""
Simple 2-layer perceptron model: 
    1 input layer and 1 output layer
"""
class Model:
    def __init__(self, inputs, clone=False):
        self.edges = []
        self.neurons = []
        self.inputs = inputs
        self.net = []
        self.layers = 2

        if not clone:
            #input layer
            for i in range(0, self.inputs):
                self.neurons.append(neuron.Neuron(i))
                self.neurons[i].layer = 0

            #output layer
            self.neurons.append(neuron.Neuron(self.inputs))
            self.neurons[self.inputs].layer = 1;

            #constructing edges with random weights
            for i in range(0, self.inputs):
                self.edges.append(edge.Edge(self.neurons[i], self.neurons[self.inputs], 
                                            random.uniform(-1, 1)))

    def connect(self):
        for i in range(0, len(self.neurons)):
            self.neurons[i].edges = []

        for i in range(0, len(self.edges)):
            self.edges[i].source_node.edges.append(self.edges[i])


    def generate(self):
        self.connect()
        self.net = []
        for i in range(0, self.layers):
            for j in range(0, len(self.neurons)):
                if self.neurons[j].layer == i:
                    self.net.append(self.neurons[j])

    def feed_forward(self, x):
        #input
        for i in range(0, self.inputs):
            self.neurons[i].output = x[i]

        #activate each neuron in the network
        for i in range(0, len(self.net)):
            self.net[i].activate()
        
        #Result value
        res = self.neurons[self.inputs].output
        
        #reset the neurons
        for i in range(0, len(self.neurons)):
            self.neurons[i].input = 0

        return res
    
    def getNeuron(self, id):
        for n in self.neurons:
            if n.id == id:
                return n

    def clone(self):
        clone = Model(self.inputs, True)
        #clone the neurons
        for neuron in self.neurons:
            clone.neurons.append(neuron.clone())
        #clone the edges
        for edge in self.edges:
            clone.edges.append(edge.clone(clone.getNeuron(edge.source_node.id),
                                           clone.getNeuron(edge.dest_node.id)))
        
        clone.layers = self.layers
        clone.connect()
        return clone

    def mutate(self):
        if random.uniform(0, 1) < 0.8:
            for i in range(0, len(self.edges)):
                self.mutate_gene(self.edges[i].weight)
            
            for n in self.neurons:
                self.mutate_gene(n.bias)

    @staticmethod
    def mutate_gene(gene):
        if random.uniform(0, 1) < 0.1:
            gene = random.uniform(-1, 1)
        else:
            gene += random.gauss(0, 1) / 10
            if gene > 1:
                gene = 1
            if gene < -1:
                gene = -1

class MultilayerPerceptronModel(Model):
    def __init__(self, inputs, layers=3, hidden_layer_size=[3], clone=False):
        
        self.layers = layers
        self.hidden_layer_size = hidden_layer_size

