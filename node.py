class Node:
    def __init__(self,data):
        self.data = data
        self.featureIndex = None
        self.dataPointIndex = None
        self.lChild = None
        self.rChild = None
        self.parent = None
        self.thresh = None
        self.splitError = None
        self.isaLeaf = False
        self.prediction = None
        self.splits = []