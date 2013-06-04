#
#   Module: prediction.py
#	Author: Jie Shen  @ NCTR/FDA
#	Date: Sep. 8, 2012.
#
#	Description:
#		The module reads a svm model file and a data set, it will generate the prediction results
#       for the input data set.
#
#	Dependence: svmutil.py
#
import sys
from fileRead import *
from svmutil import *


def process_options(argv=sys.argv):
    """

    """

    global inputdatafile, outputfile, featurefile, modelfile
    global labelMatrix, dataMatrix, sampletitles, features, fnos, featuretitles, testdatafile, testdataMatrix
    global param_n, param_c, param_g, param_fset

    usage = """\
Usage: prediction.py -m SVM_MODEL -f FEATURE_FILE -i inputdatafile -o outputfile
        Feature file is the file generated during the training process..
"""


    is_win32 = (sys.platform == 'win32')
    if is_win32:
        Path="C:\\Documents and Settings\\jshen\\My Documents\\Research\\SEQC_TGx\\PredTGx\\"
        outpath="C:\\Documents and Settings\\jshen\\My Documents\\Research\\SEQC_TGx\\PredTGx\\"
    else:
        Path="/home/hhong/seqc_tgx/data/"
        outpath="/home/hhong/seqc_tgx/model/linear/y1/"

    datafile=Path+"train44_cleaned_ratio_log2.txt"


    if len(argv) < 0:
        print(usage)
        sys.exit(1)

    pass_through_options=[]

    i = 1
    while i < len(argv) - 1:
        if argv[i] == "-h":
            i += 1
            print usage
            exit(0)
        elif argv[i] == "-m":
            i += 1
            modelfile = argv[i]
        elif argv[i] == "-f":
            i += 1
            featurefile = argv[i]
        elif argv[i] == '-i':
            i += 1
            inputdatafile = argv[i]
        elif argv[i] == '-o':
            i += 1
            outputfile = argv[i]
        else:
            pass_through_options.append(argv[i])
        i += 1

    dataMatrix=readfile_float(inputdatafile)     #get data matrix with title line
    sampletitles=dataMatrix[0]
    featurep=open(featurefile,"r")
    datalines=featurep.readlines()
    datas=datalines[0].split("\t")
    features=datas[1].strip(" ").split(" ")
    featuretitles=[]
    for line in dataMatrix[1:]:
        featuretitles.append(str(line[0]))
    fnos=[]
    for f in features:
        id=featuretitles.index(f)
        fnos.append(id)


def getTestSVMinput(testXfile): #this is specifically for test set data
    #it reads the file and return a Y and X list.
    testp=open(testXfile,"r")
    testX=testp.readlines()
    testsampletitles=testX[0].strip("\r").strip("\n").strip("\t").split("\t")
    Y=[]
    X=[]
    for i in range(1,len(testsampletitles)):
        Y.append(0)
        vectorX=[]
        for line in testX[1:]:
            datas=line.strip("\r").strip("\n").split("\t")
            vectorX.append(float(datas[i]))
        X.append(vectorX)
    return Y,X

def getTestTitles(testXfile):
    testp=open(testXfile,"r")
    testX=testp.readlines()
    testsampletitles=testX[0].strip("\r").strip("\n").strip("\t").split("\t")
    return testsampletitles




def genX(X,selectedfno):
    # this methods generate the X matrix  according to the feature selection result
    selectedX=[]
    for x in X:
        line=[]
        for i in selectedfno:
            line.append(x[i])
        selectedX.append(line)
    return selectedX


def main(argv):

# Give the default parameters
    """

    """
    print "initializing...."
    process_options()



    print "Preparing data set..."

    testingY,testingX=getTestSVMinput(inputdatafile)
    selectedtestingX=genX(testingX,fnos)
    testsampletitles=getTestTitles(inputdatafile)

    print "Reading model..."
    m=svm_load_model(modelfile)

    print "Predicting..."
    p_label, p_acc, p_val=svm_predict(testingY,selectedtestingX,m,'-b 1')

    print "Writing Results..."
    outp=open(outputfile,"w")
    outp.write("sample\tpredict_class\tprobability\n")
    for i in range(0,len(testingY)):
        outp.write("%s\t%d\t%f\n" % (testsampletitles[i+1],p_label[i],p_val[i][0]))
    outp.close()

if __name__ == "__main__":
    main(sys.argv[1:])
