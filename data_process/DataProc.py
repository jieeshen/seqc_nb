#
#   Module: DataProc.py
#   Author: JShen
#   Date: 09/04/12
#   Time: 11:51 AM
#   Version: 
#
#
#	Description:  This module process the Affy MicroArray Data. According to specified input, e.g. the repeat sample
#               list, the control sample list, the outlier list ..., it will generate a training/testing data matrix.
#               for the data, it will calculate the control mean and do the ratio.
#
#               Since the data has been transformed using log2, the control mean is calculated using
#               log2[(2^d1+2^d2+2^d3)/3] and the ratio is calculated using d1-(control mean)
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
    print "\t\t", name, "-i INPUTFILE -c CONTROLLIST -t OUTLIERLIST -r REPEATLIST -o OUTPUTFILE "
    print """
		PARAMETERS

			-h, --help	: Help
			-i,		: input text file, contain a matrix
			-c,     : match list file
			-t,     : outlier list, delimited using ","
			-r,     : repeat list, delimited using ","
			-o,		: output file
		"""
    sys.exit()


if __name__ == '__main__':
    is_win32 = (sys.platform == 'win32')
    if is_win32:
        outpath="C:\\Documents and Settings\\jshen\\My Documents\\Research\\SEQC_NB\\120903\\"
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
    infile=outpath+"SEQC_NB_RefSeqCounts_HHong.txt"
    outfile=outpath+"SEQC_NB_RefSeqCounts_HHong_498.txt"

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:t:r:o:",["help"])
    except getopt.GetoptError:
        usage(sys.argv[0])

    logfile=outpath+"log.txt"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i"):
            infile=arg
        elif opt in ("-t"):
            outlierlist=arg.split(",")
        elif opt in ("-r"):
            repeatlist=arg.split(",")
        elif opt in ("-o"):
            outfile=arg

    source="".join(args)

    inp=open(infile,"r")
    matrix=inp.readlines()
    inp.close()


    sampletitles=matrix[0].strip("\r").strip("\n").strip("\t").split("\t")
    outp=open(outfile,"w")
    datasampletitles=list(set(sampletitles)-set(repeatlist))
    datasampletitles.sort()
    outp.write("%s" % datasampletitles[0])
    for title in datasampletitles[1:]:
        outp.write("\t%s" % title)
    outp.write("\n")

    for line in matrix[1:]:
        dataline=line.strip("\r").strip("\n").strip("\t").split("\t")
        outp.write("%s" % dataline[0])

        for datatitle in datasampletitles[1:]:
            newdata=float(dataline[sampletitles.index(datatitle)])
            outp.write("\t%s" % newdata)
        outp.write("\n")
    outp.close()