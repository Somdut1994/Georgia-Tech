from util import entropy, information_gain, partition_classes
import numpy as np

class DecisionTree(object):
    def __init__(self):
        self.tree = {"L" : None,"R" : None,"Split" : -1,"IG" : 0,"TH" : 0,"lbl" : 0}

    def learn(self, X, y):
        # TODO: train decision tree and store it in self.tree
        self.store_tree(X, y, range(len(X[0])-1))

    def classify(self, record):
        # TODO: return predicted label for a single record using self.tree
        if self.tree["L"] == None and self.tree["R"] == None:
            return str(self.tree["lbl"])
        elif self.tree["Split"] > -1 and record[self.tree["Split"]] <= self.tree["TH"]:
            return str(self.tree["L"].classify(record))
        else:
            return str(self.tree["R"].classify(record))
        
    def store_tree(self, X, Y, Z):
        for i in range(0,2):
            if Y.count(i) == len(Y):
                self.tree["lbl"] = i
                return        
        if len(Z) == 0:
            self.tree["lbl"] = (Y.count(0) <= Y.count(1)) + 0
        for j in Z:
            ig = information_gain(Y, partition_classes([i[j] for i in X], Y, self.tree["TH"]))
            if self.tree["Split"] == -1 or ig > self.tree["IG"]:
                self.tree["Split"] = j
                self.tree["IG"] = ig
                self.tree["TH"] = np.mean(np.array(X), axis = 0)[j]
        if len(Z) > 0:
            Z.remove(self.tree["Split"])
            self.tree["L"] = DecisionTree()
            self.tree["R"] = DecisionTree()
            Data = [[],[],[],[]]
            for i in range(len(X)):
                if X[i][self.tree["Split"]] <= self.tree["TH"]:
                    Data[0].append(X[i])
                    Data[1].append(Y[i])
                else:
                    Data[2].append(X[i])
                    Data[3].append(Y[i])
            self.tree["L"].store_tree(Data[0], Data[1], Z)
            self.tree["R"].store_tree(Data[2], Data[3], Z)

