#
#   Module: CV_result_collect.py
#   Author: JShen
#   Date: 09/05/12
#   Time: 3:12 PM
#   Version: 0.01
#
#
#	Description: This module is used to evaluate the CV results generated from CV
#
#
#
#	Dependence: fileRead.py
#	
#	Usage: CV_result_collect.py -i labelfile -j predictresultfile -o outfile
#
#!/bin/python
import getopt
import sys
from fileRead import *
import numpy as np
import math

def usage(name):
    print "\n"
    print "\tUSAGE\n"
    print "\t\t", name, "-i INPUTLABELFILE -j PREDRESULTFILE -o OUTPUTFILE "
    print """
		PARAMETERS

			-h, --help	: Help
			-i,		: labelfile with known labels
			-j,     : predict result file
			-o,		: output file
		"""
    sys.exit()


def prediction(predlist,reallist,cutvalue=0.5):
    tp=0
    fp=0
    tn=0
    fn=0
    for i in range(0,len(predlist)):
        if reallist[i]==1:
            if predlist[i]>cutvalue:
                tp=tp+1
            else:
                fn=fn+1
        else:
            if predlist[i]>cutvalue:
                fp=fp+1
            else:
                tn=tn+1
    sp=tn*1.0/(tn+fp)
    se=tp*1.0/(tp+fn)
    acc=(tp+tn)*1.0/(tn+fp+tp+fn)
    try:
        mcc=(tp*tn-fp*fn)/math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    except ZeroDivisionError:
        mcc=0
        print "error"
    finally:
        pass
    return tp,fp,tn,fn,sp,se,acc,mcc

def roc(predlist,reallist):
    resultmatrix=[]     #[predict probility, real value]
    for i in range(0,len(predlist)):
        resultmatrix.append([predlist[i],reallist[i]])
    resultmatrix.sort(reverse=True)
    plist=[]
    rlist=[]
    rocmatrix=[]
    for values in resultmatrix:
        plist.append(values[0])
        rlist.append(values[1])
    for i in range(0,len(plist)):
        tp,fp,tn,fn,sp,se,acc,mcc=prediction(plist,rlist,cutvalue=plist[i])
        rocmatrix.append([fp*1.0/(tn+fp),tp*1.0/(tp+fn)])

    auc = 0.
    prev_x = 0
    for x,y in rocmatrix:
        if x != prev_x:
            auc += (x - prev_x) * y
            prev_x = x

    return auc,rocmatrix







if __name__ == '__main__':
    is_win32 = (sys.platform == 'win32')
    if is_win32:
        outpath="C:\\Documents and Settings\\jshen\\My Documents\\Research\\SEQC_TGx\\AffyTGx\\Results\\"
    else:
        outpath="/home/hhong/seqc_tgx/AffyTGx/data/"


    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:j:o:",["help"])
    except getopt.GetoptError:
        usage(sys.argv[0])

    logfile=outpath+"log.txt"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i"):
            labelfile=arg
        elif opt in ("-j"):
            predfile=arg
        elif opt in ("-o"):
            outfile=arg

    source="".join(args)

    labelMatrix=readfile_int(labelfile)
    dataMatrix=readfile_float(predfile)

    ncv=len(dataMatrix[0])

    reallisttitles=[]
    for dataline in labelMatrix:
        reallisttitles.append(dataline[0])

    predlisttitles=[]
    sortedreallist=[]
    for dataline in dataMatrix[1:]:
        predlisttitles.append(dataline[0])
        id=reallisttitles.index(dataline[0])
        sortedreallist.append(labelMatrix[id][1])

    tplist=[]
    fplist=[]
    tnlist=[]
    fnlist=[]
    splist=[]
    selist=[]
    acclist=[]
    mcclist=[]
    auclist=[]
    for i in range(1,ncv):
        predlist=[]
        for j in range(0,len(predlisttitles)):
            predlist.append(dataMatrix[j+1][i])
        tp,fp,tn,fn,sp,se,acc,mcc=prediction(predlist,sortedreallist)
        auc,rocm=roc(predlist,sortedreallist)
        tplist.append(tp)
        fplist.append(fp)
        tnlist.append(tn)
        fnlist.append(fn)
        splist.append(sp)
        selist.append(se)
        acclist.append(acc)
        mcclist.append(mcc)
        auclist.append(auc)
    name=["TP","FP","TN","FN","SP","SE","ACCURACY","MCC","AUC"]
    j=0
    # output results
    outp=open(outfile,"w")
    for list in [tplist,fplist,tnlist,fnlist]:
        outp.write("%s" % name[j]),
        j+=1
        for i in range(1,ncv):
            outp.write("\t%d" % list[i-1]),
        outp.write("\n"),
    for list in [splist,selist,acclist,mcclist,auclist]:
        outp.write("%s" % name[j])
        j+=1
        for i in range(1,ncv):
            outp.write("\t%.3f" % list[i-1])
        outp.write("\n")

    outp.write("%.3f\t%.3f\t%.3f\t%.3f\t%.3f\n" %(np.average(splist), np.average(selist),
                                                  np.average(acclist),np.average(mcclist),np.average(auclist)))
    outp.close()





