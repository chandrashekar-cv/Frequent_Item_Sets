__author__ = 'Chandu'

import sys,itertools,copy

class pcy:
    allSizeFreqItems = {}
    support = None
    bucketSize = None
    transactions = []
    freqItems = []

    def __init__(self,fileName,support,bucketSize):
        self.support = support
        self.bucketSize = bucketSize
        self.readFile(fileName)

    def readFile(self, fileName):
        lines = None
        with open(fileName , "r") as reader:
            lines = reader.readlines()

        for line in lines:
            self.transactions.append(sorted(line.strip().split(",")))

    def pcyalgo(self):
        size = 1
        prevHash1={}
        prevHash2={}
        prevFreqSet=[]
        while True:
            htable1 = {}
            htable2 = {}
            countSet={}
            for items in self.transactions:

                candidateSet = itertools.combinations(items,size)

                for item in candidateSet:
                    if(size==1):
                        countSet.setdefault(item,0)
                        countSet[item]+=1
                    else:
                        h1 = self.hashFunc1(item)
                        h2 = self.hashFunc2(item)
                        flag = self.checkForPreviousSizeSubsets(item,size-1,prevFreqSet)

                        if(prevHash1[h1]>=support and prevHash2[h2]>=support):
                            countSet.setdefault(item,0)
                            countSet[item] += 1

                nextSet = itertools.combinations(items,size+1)
                for item in nextSet:
                    h1 =self.hashFunc1(item)
                    htable1.setdefault(h1,0)
                    htable1[h1]+=1

                    h2 = self.hashFunc2(item)
                    htable2.setdefault(h2,0)
                    htable2[h2]+=1

            self.freqitems = [list(k) for k in countSet.keys() if countSet[k] >= self.support]

            if(size==1):
                self.freqitems = sorted(list(itertools.chain(*self.freqitems)))
            else:
                self.sortFreqItems()

            if(len(self.freqitems)==0):
                break

            if(len(self.freqitems)>0 and len(prevHash1)>0 and len(prevHash2)>0):
                print(prevHash1)
                print(prevHash2)
            print(self.freqitems)

            prevFreqSet = self.freqitems

            size+=1
            prevHash1 = copy.deepcopy(htable1)
            prevHash2 = copy.deepcopy(htable2)

    def sortFreqItems(self):
        for i in range(0,len(self.freqitems),1):
            self.freqitems[i] = sorted(self.freqitems[i])
        self.freqitems = sorted(self.freqitems)

    def hashFunc1(self,items):
        items = list(items)
        h=0
        counter = 1
        for item in items:
            h += (ord(item) - 96)*counter
            counter+=1
        h = h%self.bucketSize
        return h

    def hashFunc2(self,items):
        items = list(items)
        h=0
        counter = len(items)+1
        for item in items:
            h += (ord(item) - 96)*counter
            counter-=1
        h = h%self.bucketSize
        return h


    def checkForPreviousSizeSubsets(self,items,prevSize,prevFreqSet):
        candidates = itertools.combinations(items,prevSize)
        for subset in candidates:
            flag = False
            subset = list(subset)
            if(prevSize==1):
                subset = subset[0]
            for prevFreq in prevFreqSet:
                 if tuple(sorted(subset)) == tuple(sorted(prevFreq)):
                    flag = True
                    break

            if flag==False:
                return False

        return True


if __name__=="__main__":
    fileName = sys.argv[1]
    support = int(sys.argv[2])
    bucketSize = int(sys.argv[3])

    pcyInstance = pcy(fileName,support,bucketSize)
    pcyInstance.pcyalgo()

