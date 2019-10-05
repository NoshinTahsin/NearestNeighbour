import math
import xlrd
import random

numClass=input("Enter number of classes:")

numberOfTestData=100

loc = ("C:/Users/noshi/PycharmProjects/nearestNeighbour/venv/NearestNeighbour/a.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
numberOfRowsInxls = sheet.nrows
numberOfcolsInxls = sheet.ncols

arrayOfData = [0] * numberOfRowsInxls
print("Number of rows:"+str(numberOfRowsInxls))
print("Number of columns:" +str(numberOfcolsInxls))
print(" ")


def readcsv( ):

   for i in range(numberOfRowsInxls):
      arrayOfData[i] = [0] * numberOfcolsInxls

   #print("Line 33")
   for i in range(0,numberOfRowsInxls):
     for j in range(0,numberOfcolsInxls):
            arrayOfData[i][j]=sheet.cell_value(i, j)
            #print(a[i][j])

   return


#checks if the row was in test set before
#checkList[i]=0 means row i was not in the test set before
checkList=[0]* numberOfRowsInxls

def split():

    numberOfSections=int((sheet.nrows)/numberOfTestData)

    for i in range(0,numberOfSections):

        #ekbar er jonno accuracy ber kora
        testDataArray = [0] * numberOfTestData
        for i in range(0,numberOfTestData):
            testDataArray[i] = [0] * numberOfcolsInxls

        for i in range(0,numberOfTestData):
            for j in range(0,numberOfcolsInxls):
                testDataArray[i][j]=0

        testVar=0;
        #to keep track if 100 random numbers are generated
        count=0
        q=0


        randomNumList=[0]*numberOfTestData

        #loop 100 times
        for j in range(0,numberOfRowsInxls+1):
            for x in range(1):
                singleRand=random.randint(0,numberOfRowsInxls-1)
                #print("This is the single random number : "+str(singleRand)+"  no " + str(count))

                #if row no singleRand was not in test data before set testVar to 1
                if checkList[singleRand]==0:
                    testVar=1

                if testVar==1:
                    checkList[singleRand]=1
                    count=count+1
                    #keeps the row numbers of test set
                    randomNumList[q]=singleRand;

                    q=q+1
                    #p=0
                    #print(sheet.row_values(singleRand))
                    #100 size er array te test data row rakha hocche
                    for k in range(0,numberOfcolsInxls):
                        testDataArray[count-1][k]=arrayOfData[singleRand][k]
                        #p=p+1
                    #ek row rakha shesh
            testVar=0
            if count==numberOfTestData:
                break

        trainingSet = [0] * numberOfRowsInxls
        for i in range(0,numberOfRowsInxls):
            trainingSet[i] = [0] * numberOfcolsInxls

        for i in range(0,numberOfRowsInxls):
            for j in range(0,numberOfcolsInxls):
                trainingSet[i][j]=0

        #protita row er jonno  check kora hoitese training set e rakha jay kina
        ccc=0;
        for i in range (0,numberOfRowsInxls):
            canKeep=0
            cnt=0
            for traverseRandLoop in range(0,numberOfTestData):
                cnt=cnt+1

                #if row is in testSet, can't keep in training set
                if(randomNumList[traverseRandLoop]==i):
                    break;

            if(cnt==numberOfTestData):
                canKeep=1
                #keeping track of total rows
                ccc=ccc+1

            if(canKeep==1):
                for ck in range(0,numberOfcolsInxls):
                    #print("i: ck: i: "+ str(i)+" "+ str(ck)+" " + str(i))
                    trainingSet[i][ck]=arrayOfData[i][ck]

        distanceList=[]
        #print(n-perSet)
        #print(len(distanceList))
        classOfTrainingSet=[0] * (numberOfRowsInxls-numberOfTestData)
        classOfTestSet=[0] * numberOfTestData

        arrayToTestAccuracy=[0] * numberOfTestData
        originalClass=[0] * numberOfTestData

        for i in range (0,numberOfTestData):
            originalClass[i]=testDataArray[i][numberOfcolsInxls-1]

        for i in range (0,numberOfTestData):


            #print("Line 129")
            #print("i : "+str(i)+"  ")
            for k in range (0, (numberOfRowsInxls-numberOfTestData)):
                ans=0
                for j in range (0,numberOfcolsInxls-1):
                    ans=ans+pow((trainingSet[k][j]-testDataArray[i][j]),2)
                #print(" k : "+ str(k) +" ")
                distanceList.append(math.sqrt(ans))
                classOfTrainingSet[k]=trainingSet[k][numberOfcolsInxls-1]


            #data_list = [-5, -23, 5, 0, 23, -6, 23, 67]
            new_list = []
            new_classList = []


            while distanceList:
              it=-1
              minimum = distanceList[0]  # arbitrary number in list
              for x in distanceList:
                 it=it+1
                 if x < minimum:
                    minimum = x
              new_list.append(minimum)
              new_classList.append(classOfTrainingSet[it])
              distanceList.remove(minimum)

            #print(new_list)
            #print(new_classList)

            #distanceList.sort()
            sortedTopList=[0] * 3
            for st in range (0,3):
                #print(new_list[st])
                #print("  ")
                sortedTopList[st]=new_list[st]
                #print(new_classList[st])
                #print("  ")

            cnt1=0
            maxAppearanceType=-1
            for tr in range(0,3):
                var=new_classList[tr]
                for st in range (0,3):
                    if var==new_classList[st] :
                        cnt1=cnt1+1
                if(cnt1>maxAppearanceType):
                    maxAppearanceType=var
                    #strVar1=new_classList[st]

            arrayToTestAccuracy[i]=maxAppearanceType
            #cmp=3-cnt1

            #if cnt1>cmp:
            #    arrayToTestAccuracy[i]=strVar1
            #else:
            #   arrayToTestAccuracy[i]=var

        comparedAccuracyList = [0] * numberOfTestData

        fMeasure=[0] * numberOfTestData
        #print("Line 184")
        for i in range (0,numberOfTestData):
            if arrayToTestAccuracy[i]==originalClass[i] :
                comparedAccuracyList[i]=1

            #1 for true positive
            #2 for false positive
            #3 for true negative
            #4 for false negative

            if(numClass==2):
                if arrayToTestAccuracy[i]==2 and originalClass[i]==2 :
                    fMeasure[i]=1
                elif arrayToTestAccuracy[i]==2 and originalClass[i]==1 :
                    fMeasure[i]=2
                elif arrayToTestAccuracy[i]==1 and originalClass[i]==2 :
                    fMeasure[i]=3
                else:
                    fMeasure[i]=4

        if numClass==2:
            fmc1=0
            fmc2=0
            fmc3=0
            fmc4=0
            for i in range (0,numberOfTestData):
                if fMeasure[i]==1:
                    fmc1=fmc1+1
                elif fMeasure[i]==2:
                    fmc2=fmc2+1
                elif fMeasure[i]==3:
                    fmc3=fmc3+1
                else:
                    fmc4=fmc4+1

            print("fMeasureCount1: " + str(fmc1)+" fMeasureCount2: "+str(fmc2)+" fMeasureCount3: "+str(fmc3)+"  fMeasureCount4: "+str(fmc4)+" ")
            precision=fmc1/(fmc1+fmc2)
            recall=fmc1/(fmc1+fmc4)


        accuracy=0

        #print("Line 191")
        for i in range (0,numberOfTestData):
            if comparedAccuracyList[i]==1 :
                accuracy=accuracy+1

        accuracyPercentage=accuracy/100

        #print("Line 198 ")
        if numClass==2:
            print( "   precision " + str(precision))
            print( "   recall " + str(recall))
        print( "   accuracy  " + str(accuracyPercentage))
        print(' ')

    return
