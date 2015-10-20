__author__ = 'Chandu'

import sys,itertools,random

class toivonen:
    support = None
    newSupport = None
    bucketSize = None
    transactions = []


    def __init__(self,fileName,support,bucketSize):
        self.support = support
        self.bucketSize = bucketSize
        self.readFile(fileName)
        self.newSupport = int(0.4*0.8*support)

    def readFile(self, fileName):
        lines = None
        with open(fileName , "r") as reader:
            lines = reader.readlines()

        for line in lines:
            self.transactions.append(sorted(line.strip().split(",")))

    def toivonenalgo(self):

        output = ""
        output += "0.4"
        itr = 0
        while True:
            sample = random.sample(self.transactions , int(0.4*len(self.transactions)))
            negativeBorder = []
            freqItems = []
            prevFreq = []
            itr+=1
            size = 1
            while True:
                countSet={}
                for items in sample:
                    candidateSet = itertools.combinations(items,size)
                    for item in candidateSet:
                        if(size==1):
                            countSet.setdefault(item,0)
                            countSet[item]+=1
                        else:
                            prevSet = sorted(itertools.combinations(item,size-1))
                            #if all the subsets are frequent items, count it
                            item = tuple(sorted(list(item)))
                            if( all (item in prevFreq for item in prevSet)):
                                countSet.setdefault(tuple(sorted(item)),0)
                                countSet[tuple(sorted(item))]+=1


                prevFreq = [key for key,value in countSet.items() if value >= self.newSupport]

                freqItems.extend(prevFreq)
                #a set will be present in count only if its subsets are frequent. So if its count < new support, it is a negative border case

                #if all the subsets are frequent in the sample and the parent set is not frequent, add it to negative border
                negativeBorder.extend([key for key,value in countSet.items() if value < self.newSupport])

                if(len(prevFreq)==0):
                    break

                size+=1

            #I have the frequent items and negative border items from the sample. Now read the entire data set.

            freqItemsCount = {}
            negativeBorderItemCount = {}

            for transaction in self.transactions:

                allSubsets = []
                tempSize = size
                if(size > len(transaction)):
                    tempSize = len(transaction)-1

                for i in range(1,tempSize+1,1):
                    allSubsets.extend(list(itertools.combinations(sorted(transaction), i)))

                freqSet = [item for item in allSubsets if item in freqItems]
                negSet = [item for item in allSubsets if item in negativeBorder]

                for item in freqSet:
                    freqItemsCount.setdefault(item,0)
                    freqItemsCount[item]+=1
                for item in negSet:
                    negativeBorderItemCount.setdefault(item,0)
                    negativeBorderItemCount[item]+=1

            #frequent are filtered based on items count >= support from the entire dataset.
            freqSet = [key for key,value in freqItemsCount.items() if value >=self.support]

            #if any item in negative border set has a count in the entire dataset greater than support, then need to resample and restart algo
            negSet  = [key  for key,value in negativeBorderItemCount.items() if value >= support]

            if(len(negSet)==0):
                break

        print(str(itr))
        print("0.4")
        freqSet = sorted(freqSet, lambda x,y: len(x)-len(y))
        for length, group  in itertools.groupby(freqSet, lambda x: len(x)):
            print map(list,(sorted(group)))


if __name__=="__main__":
    fileName = sys.argv[1]
    support = int(sys.argv[2])

    toivonenInstance = toivonen(fileName,support,20)
    toivonenInstance.toivonenalgo()

