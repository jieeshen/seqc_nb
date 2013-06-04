#
#   Module: dataRPGene.py
#   Author: JShen
#   Date: 9/11/12
#   Time: 11:27 AM
#   Version: 
#
#
#	Description: This module is used to calculate the Reads Per Gene (RPGene) results of a matrix from NGS data.
#
#
#	Dependence:
#	
#	Usage: rpmMatrix(inputfile, outputfile)
#
#!/bin/python
import getopt
import string
import sys

def usage(name):
    print "\n"
    print "\tUSAGE\n"
    print "\t\t", name, "-i INPUTFILE -o OUTPUTFILE "
    print """
		PARAMETERS

			-h, --help	: Help
			-i,		: input text file, contain a matrix
			-o,		: output file
		"""
    sys.exit()

def readfile(filename):
    matrix=[]
    readin=open(filename,"r")
    lines=readin.readlines()
    for line in lines:
        datasStr=line.strip("\n").strip("\r").strip("\t").split("\t")
        datas=[]
        for data in datasStr:
            try:
                datas.append(string.atof(data))
            except:
                datas.append(data)
        matrix.append(datas)

    return matrix

def dataMean(datas):
    s=0.0
    for data in datas:
        s=s+data
    return s/len(datas)


def rpgMatrix(inputM):


    titles=inputM[0]
    outputM=[inputM[0]]
    meanList=[]
    for i in range(1,len(titles)):
        datalist=[]
        for dataline in inputM[1:]:
            datalist.append(dataline[i])
        m=dataMean(datalist)
        meanList.append(m)



    for dataline in inputM[1:]: #dataline is geneline
        newline=[dataline[0]]
        for i in range(1,len(dataline)):
            rpg_data=float(dataline[i])/meanList[i-1]
            newline.append(rpg_data)
        outputM.append(newline)

    return outputM



if __name__ == '__main__':
    Path=r"C:\Documents and Settings\jshen\My Documents\Research\SEQC_NB\ngs_data_0911\\"
    infile=Path+"SEQC_NB_RefSeqCounts_HHong_498.txt"
    outfile=Path+"SEQC_NB_RefSeqCounts_HHong_498_rpg.txt"
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["help"])
    except getopt.GetoptError:
        usage(sys.argv[0])

    logfile="log.txt"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i"):
            infile=arg
        elif opt in ("-o"):
            outfile=arg

    source="".join(args)

    inputM=readfile(infile)
    outMatrix=rpgMatrix(inputM)
    rpgmin=1
    outp=open(outfile,"w")
    for dataline in outMatrix:
        for data in dataline:
            if data<rpgmin and data>0:
                rpgmin=data
            outp.write("%s\t" % data)
        outp.write("\n")
    print rpgmin

