import random


class NeuralNode:
    
    def __init__(self, inVector):
        
        self.weights = []
        for i in range(len(inVector)-1):
            self.weights.append(inVector[i])
        
        self.threshold = inVector[-1]
    
    def Output(self, inVector):
        return 0;
        
    def WeightString(self, mutateThis, maxDifference, mutateChance):
        
        string = "" 
        for i in range(len(self.weights)):
            newWeight = self.weights[i]
            if mutateThis:
               tryMutate = random.random()
               if tryMutate <= mutateChance:
                   #get a value between -maxDifference and + maxDifference
                   #([0,1] -> [0,2] -> [-1, 1])*maxDifference
                   difference = (random.random()*2-1)*maxDifference
                   newWeight += difference
            
            string += str(newWeight) + " " 
        return string

class SumNode(NeuralNode):
    
    def Output(self, inVector):
        
        calc = 0
        for i in range(len(inVector)):
            calc += inVector[i]*self.weights[i]
            
        return max(0 , calc-self.threshold)
        
        

class NeuralNetwork:
    
    def __init__(self, CanMutate, fileName):
        self.canMutate = CanMutate
        
        #read size and weights from file:
        file = open(fileName, 'r')
        
        SizeLine = self.file.readline().split()
        self.depth = len(SizeLine)-1
        self.NeuralLine = []
        for i in range(self.depth):
            depthLine = file.readline().split()
            self.NeuralLine.append([])
            j = 0
            weightSize = len(depthLine)/SizeLine[i+1]
            for j in range(len(depthLine)):
                inVector = []
                for x in range(weightSize):
                    inVector.append(depthLine[j*weightSize+x])
                self.NeuralLine.append(SumNode(inVector))
                j += x
                
        
    def Calculate(self, inVector):
        
        #calculate each step 
        nextIn = inVector
        for i in range(self.depth):
            out = []
            for j in range(len(nextIn)):
                out.append(self.NeuralLine[i][j].Output(nextIn))
            nextIn = out
                
        return nextIn
        
    def WriteToFile(self, fileName, mutateThis, maxDifference, mutateChance):
        
        
        if not self.canMutate:
            return
            
        file = open(fileName, 'r+')
        
        depthLine = ""
        weightLines = []
        for i in range(self.depth):
            neuralWidth = len(self.NeuralLine[i])
            depthLine += str(neuralWidth) + " "
            
            for j in range(neuralWidth):
                weightLines.append(self.NeuralLine[i][j].WeightString(mutateThis, maxDifference, mutateChance))
        
        file.writeline(depthLine)
        for line in weightLines:
            file.writeline(line)