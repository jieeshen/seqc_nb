#
#	Module: geneFiltering.py
#	Author: Jie Shen
#	Date: 2012.09.07
#	Version 0.01
#
#		
#
#	Description: 
#		This Module reads a matrix and filter out the genes with average value out of the range. the lower and upper
#       number is specified. It also filters out the gene with any of 4 control sample with the value of 0.
#
#	Dependence:
#	
#	Usage: geneFilter -i inputfile -l lowbound -u upperbound -o outputfile
#
#!/bin/python
import getopt
import sys



def usage(name):
    print "\n"
    print "\tUSAGE\n"
    print "\t\t", name, "-i INPUTFILE -l LOWBOUND -u UPBOUND -o OUTPUTFILE "
    print """
		PARAMETERS

			-h, --help	: Help
			-i,		: input text file, contain a matrix
			-l,     : low bound
			-u,     : up bound
			-o,		: output file
		"""
    sys.exit()



def strave(strlist):
    sum=0
    for data in strlist:
         sum+=float(data)
    return sum/len(strlist)



def geneFilter(infile,outfile,low,high):
    inp=open(infile,"r")
    outp=open(outfile,"w")
    count=0

    matrix=inp.readlines()
    titles=matrix[0].strip("\n").strip("\r").strip("\t").split("\t")
    outp.write("%s\n" % titles[0])
    #for title in titles[1:]:
    #    outp.write("\t%s" % title)

    for line in matrix[1:]:
        dataline=line.strip("\n").strip("\r").strip("\t").split("\t")
        datas=dataline[1:]
#        controls=map(float,dataline[-4:])
#        print datas
        ave=strave(datas)

        if low < ave < high:
            count += 1
            outp.write("%s" % dataline[0])
#            for data in datas:
#                outp.write("\t%s" % data)
            outp.write("\n")

    print("Original matrix contains %d rows, now contains %d rows" % (len(matrix)-1,count))
    inp.close()
    outp.close()

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:l:u:o:",["help"])
    except getopt.GetoptError:
        usage(sys.argv[0])

    logfile="log.txt"
    low=-5
    high=10000000000

    infile=r"C:\Documents and Settings\jshen\My Documents\Research\SEQC_NB\ngs_data_0911\SEQC_NB_RefSeqCounts_HHong_498_rpg_log2.txt"
    outfile=r"C:\Documents and Settings\jshen\My Documents\Research\SEQC_NB\ngs_data_0911\genelist.txt"
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i"):
            infile=arg
        elif opt in ("-o"):
            outfile=arg
        elif opt in ("-l"):
            low=float(arg)
        elif opt in ("-u"):
            high=float(arg)

    source="".join(args)

    geneFilter(infile,outfile,low,high)



