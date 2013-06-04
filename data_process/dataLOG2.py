#
#   Module: dataLOG2.py
#   Author: JShen
#   Date: 9/3/12
#   Time: 03:08 PM
#   Version: 
#
#
#	Description: This module is used to calculate the log2 RPM results of a matrix from NGS data.
#
#
#	Dependence:
#	
#	Usage: rpmMatrix(inputfile, outputfile)
#
#!/bin/python
import getopt
from math import log
import string
import sys

def usage(name):
    print "\n"
    print "\tUSAGE\n"
    print "\t\t", name, "-i INPUTFILE -z R_ZERO -o OUTPUTFILE "
    print """
		PARAMETERS

			-h, --help	: Help
			-i,		: input text file, contain a matrix
			-z,     : the value to replace the 0, usually using the results generated from dataRPM.py or dataRPGene.py
			-o,		: output file
		"""
    sys.exit()

def readfile(filename):
    matrix=[]
    readin=open(filename,"r")
    lines=readin.readlines()
    for line in lines:
        datasStr=line.strip("\n").strip("\r").strip("\t").split("\t")
        datas=[datasStr[0]]
        for data in datasStr[1:]:
            try:
                datas.append(string.atof(data))
            except:
                datas.append(data)
        matrix.append(datas)

    return matrix

def dataSum(datas):
    s=0.0
    for data in datas:
        s=s+data
    return s


def log2Matrix(inputM, zerovalue): #zerovalue is the number to replace the 0


    titles=inputM[0]
    outputM=[titles]

    zcounts=0
    for dataline in inputM[1:]: #dataline is geneline
        newline=[dataline[0]]
        for i in range(1,len(dataline)):
            try:
                log2_data=log(dataline[i],2)
            except:
                log2_data=log(zerovalue,2)
                zcounts+=1
            newline.append(log2_data)
        outputM.append(newline)
    print("%d 0s have been replaced by %f" % (zcounts,zerovalue))
    return outputM



if __name__ == '__main__':
    Path=r"C:\JShen\Research\SEQC_NB\SEQC_NB_Fudan\\"
    infile=Path+"SEQC_NB_Fudan_498_rpm.txt"
    outfile=Path+"SEQC_NB_Fudan_498_rpm_log2.txt"


    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:z:o:",["help"])
    except getopt.GetoptError:
        usage(sys.argv[0])

    logfile="log.txt"
    z=0.0126464824675
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i"):
            infile=arg
        elif opt in ("-z"):
            z=float(arg)
        elif opt in ("-o"):
            outfile=arg

    source="".join(args)

    inputM=readfile(infile)
    outMatrix=log2Matrix(inputM,z/1.2)

    outp=open(outfile,"w")
    for dataline in outMatrix:
        for data in dataline:
            outp.write("%s\t" % data)
        outp.write("\n")

    outp.close()
