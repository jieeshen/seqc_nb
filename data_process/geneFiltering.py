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
    print "\t\t", name, "-i INPUTFILE -l GENELIST -o OUTPUTFILE "
    print """
		PARAMETERS

			-h, --help	: Help
			-i,		: input text file, contain a matrix
			-l,     : gene list file
			-o,		: output file
		"""
    sys.exit()

def retain(datas):
    l=len(datas)
    n=0
    for data in datas:
        try:
            datavalue=float(data)
        except:
            datavalue=E_MIN
        if datavalue<E_CUT:
            n=n+1
    if n>l*0.6:
        return False
    else:
        return True

def strave(strlist):
    sum=0
    for data in strlist:
         sum+=float(data)
    return sum/len(strlist)



def geneFilter(infile,outfile,listfile):
    inp=open(infile,"r")
    listp=open(listfile,"r")
    outp=open(outfile,"w")
    count=0

    matrix=inp.readlines()
    listmatrix=listp.readlines()
    glist=[]
    for line in listmatrix[1:]:
        glist.append(line.strip("\n").strip("\r"))

    titles=matrix[0].split("\t")
    outp.write("%s" % titles[0])
    for title in titles[1:]:
        outp.write("\t%s" % title)

    for line in matrix[1:]:
        dataline=line.strip("\n").strip("\r").strip("\t").split("\t")

        if dataline[0] in glist:
            count += 1
            outp.write("%s" % dataline[0])
            for data in dataline[1:]:
                outp.write("\t%s" % data)
            outp.write("\n")

    print("Original matrix contains %d rows, now contains %d rows" % (len(matrix)-1,count))
    print len(glist)
    inp.close()
    outp.close()

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:l:u:o:",["help"])
    except getopt.GetoptError:
        usage(sys.agv[0])

    logfile="log.txt"

    infile=r"C:\Documents and Settings\jshen\My Documents\Research\SEQC_NB\ngs_data_0911\SEQC_NB_RefSeqCounts_HHong_498_rpg_log2.txt"
    listfile=r"C:\Documents and Settings\jshen\My Documents\Research\SEQC_NB\ngs_data_0911\genelist.txt"
    outfile=r"C:\Documents and Settings\jshen\My Documents\Research\SEQC_NB\ngs_data_0911\SEQC_NB_RefSeqCounts_HHong_498_rpg_log2_filtered.txt"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i"):
            infile=arg
        elif opt in ("-o"):
            outfile=arg
        elif opt in ("-l"):
            listfile=arg

    source="".join(args)

    geneFilter(infile,outfile,listfile)



