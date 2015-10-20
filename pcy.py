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
        prevHash={}
        prevFreqSet=[]
        while True:
            htable = {}
            countSet={}

            for items in self.transactions:

                candidateSet = itertools.combinations(items,size)

                for item in candidateSet:
                    if(size==1):
                        countSet.setdefault(item,0)
                        countSet[item]+=1
                    else:
                        h = self.hashFunc(item)
                        prevFreqSubsetFlag = self.checkForPreviousSizeSubsets(item,size-1,prevFreqSet)
                        if(prevFreqSubsetFlag and prevHash[h]>=support):
                            countSet.setdefault(item,0)
                            countSet[item] += 1

                nextSet = itertools.combinations(items,size+1)
                for item in nextSet:
                    h =self.hashFunc(item)
                    htable.setdefault(h,0)
                    htable[h]+=1

            self.freqitems = [list(k) for k in countSet.keys() if countSet[k] >= self.support]

            if(size==1):
                self.freqitems = sorted(list(itertools.chain(*self.freqitems)))
            else:
                self.sortFreqItems()

            if(len(self.freqitems)==0):
                break

            if(len(self.freqitems)>0 and len(prevHash)>0):
                print(prevHash)

            prevFreqSet = self.freqitems

            print(self.freqitems)




            size+=1
            prevHash = copy.deepcopy(htable)

    def sortFreqItems(self):
        for i in range(0,len(self.freqitems),1):
            self.freqitems[i] = sorted(self.freqitems[i])
        self.freqitems = sorted(self.freqitems)

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

    def hashFunc(self,items):
        items = list(items)
        h=0
        counter = 1
        for item in items:
            h += (ord(item) - 96)*counter
            counter+=1
        h = h%self.bucketSize
        return h

if __name__=="__main__":
    fileName = sys.argv[1]
    support = int(sys.argv[2])
    bucketSize = int(sys.argv[3])

    pcyInstance = pcy(fileName,support,bucketSize)
    pcyInstance.pcyalgo()

