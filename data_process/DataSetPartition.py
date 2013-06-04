#
#   Module: DataSetPartition.py
#   Author: JShen
#   Date: 09/04/12
#   Time: 03:25 PM
#   Version: 
#       !!!!!!!!!!!! This version is incomplete. It does not read testing list. It generates testing set with
#       all the data other than training set.!!!!!!!!!!!!!!!!!!
#
#	Description:
#       This module read a data set from NGS/MA and separate it into training set and testing set according to the
#       training and testing list.
#
#
#	Dependence:
#	
#	Usage: 
#
#!/bin/python
import getopt
import string
import sys
import math

def usage(name):
    print "\n"
    print "\tUSAGE\n"
    print "\t\t", name, "-i INPUTFILE -l TRAININGLISTFILE -m TESTINGLISTFILE -r Training OUTPUTFILE " \
                        "-e Testing OUTPUTFILE "
    print """
		PARAMETERS

			-h, --help	: Help
			-i,		: input text file, contain a matrix
			-l,     : Training list file
			-m,     : Testing list file
			-r, 	: output training file
			-e,     : output testing file
		"""
    sys.exit()


if __name__ == '__main__':
    is_win32 = (sys.platform == 'win32')
    if is_win32:
        outpath=r"C:\JShen\Research\SEQC_NB\SEQC_NB_Fudan\\"
    else:
        outpath="/home/hhong/seqc_tgx/AffyTGx/data/"

    #Define Control lists
#    NNIPlist=["95865.CEL", "95836.CEL", "96606.CEL", "96211.CEL", "96483.CEL", "96496.CEL"]
#    NNOGlist=["95716.CEL", "95841.CEL", "95893.CEL", "95793.CEL", "96006.CEL", "95375.CEL"]
#    NUOGlist=["95686.CEL", "95746.CEL", "95915.CEL", "95797.CEL", "96706.CEL", "96729.CEL"]

    outlierlist=[]

    repeatlist=["SEQC_NB248_BD0JPPACXX_L3_TTAGGC",
                "SEQC_NB251_BD0JPPACXX_L3_GATCAG",
                "SEQC_NB252_BD0JPPACXX_L3_GGCTAC",
                "SEQC_NB253_BD0JPPACXX_L3_CGATGT",
                "SEQC_NB254_BD0JPPACXX_L3_TGACCA",
                "SEQC_NB255_BD0JPPACXX_L3_GCCAAT",
                "SEQC_NB256_BD0JPPACXX_L3_ACTTGA",
                "SEQC_NB257_BD0JPPACXX_L3_TAGCTT",
                "SEQC_NB258_BD0JPPACXX_L3_CTTGTA"]

    #Define files
    infile=outpath+"SEQC_NB_Fudan_498_rpm_log2.txt"
    traininglist=outpath+"list_training249.txt"
    trainingoutfile=outpath+"Training_249.txt"
    testingoutfile= outpath+"Testing_249.txt"
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:l:m:r:e:",["help"])
    except getopt.GetoptError:
        usage(sys.argv[0])

    logfile=outpath+"log.txt"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i"):
            infile=arg
        elif opt in ("-l"):
            traininglist=arg
        elif opt in ("-m"):
            testinglist=arg
        elif opt in ("-r"):
            trainingoutfile=arg
        elif opt in ("-e"):
            testingoutfile=arg
    source="".join(args)

    inp=open(infile,"r")
    matrix=inp.readlines()
    inp.close()

    inp=open(traininglist,"r")
    trmatrix=inp.readlines()
    inp.close()

    trlist=[]
    for line in trmatrix:
        trlist.append(line.strip("\r").strip("\n").strip("\t"))

    sampletitles=matrix[0].strip("\r").strip("\n").strip("\t").split("\t")
    trp=open(trainingoutfile,"w")
    tep=open(testingoutfile,"w")

    trainingsampletitles=["GeneID"]
    testingsampletitles=["GeneID"]
    trp.write("%s" % "GeneID")
    tep.write("%s" % "GeneID")
    for title in sampletitles[1:]:
        if title in trlist:
            trainingsampletitles.append(title)
            trp.write("\t%s" % title)
        else:
            testingsampletitles.append(title)
            tep.write("\t%s" % title)
    trp.write("\n")
    tep.write("\n")


    for line in matrix[1:]:
        dataline=line.strip("\r").strip("\n").strip("\t").split("\t")
        trp.write("%s" % dataline[0])
        tep.write("%s" % dataline[0])

        for datatitle in trainingsampletitles[1:]:
            newdata=float(dataline[sampletitles.index(datatitle)])
            trp.write("\t%s" % newdata)
        trp.write("\n")

        for datatitle in testingsampletitles[1:]:
            newdata=float(dataline[sampletitles.index(datatitle)])
            tep.write("\t%s" % newdata)
        tep.write("\n")

    trp.close()
    tep.close()
