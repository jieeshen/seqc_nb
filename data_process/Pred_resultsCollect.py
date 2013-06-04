#
#   Module: resultsCollect
#   Author: JShen
#   Date: 8/21/12
#   Time: 9:43 PM
#   Version: 0.01
#
#
#	Description: This module is used to collect the predict results of several models and generate a combined table
#
#
#	Dependence:
#	
#	Usage: resultsCollect.py -i file1 file2 file3 ... -o outfile
#
#!/bin/python
import getopt
import sys

def usage(name):
    print "\n"
    print "\tUSAGE\n"
    print "\t\t", name, "-i INPUTFILE -c CONTROLLIST -t OUTLIERLIST -r REPEATLIST -o OUTPUTFILE "
    print """
		PARAMETERS

			-h, --help	: Help
			-i,		: input text files, using ""
			-o,		: output file
		"""
    sys.exit()

if __name__ == '__main__':
    is_win32 = (sys.platform == 'win32')
    if is_win32:
        outpath="C:\\Documents and Settings\\jshen\\My Documents\\Research\\SEQC_TGx\\AffyTGx\\Results\\"
    else:
        outpath="/home/hhong/seqc_tgx/AffyTGx/data/"


    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["help"])
    except getopt.GetoptError:
        usage(sys.argv[0])

    logfile=outpath+"log.txt"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(sys.argv[0])
        elif opt in ("-i"):
            infiles=arg.split(" ")
        elif opt in ("-o"):
            outfile=arg

    source="".join(args)

    inputdatalist=[]
    outp=open(outfile,"w")
    outp.write("sample")

    for infile in infiles:
        outp.write("\t%s" % infile[1:-12])
        inp=open(infile,"r")
        lines=inp.readlines()
        datamatrix=[]
        sampletitles=[]
        for line in lines[1:]:
            newline=[]
            datastrs=line.strip("\n").strip("\r").strip("\t").split("\t")
            sampletitles.append(datastrs[0])
            if int(datastrs[1])==-1:
                newline.append(0)
            else:
                newline.append(int(datastrs[1]))
            if newline[0]*(float(datastrs[2])-0.5)<0:
                newline.append(1-float(datastrs[2]))
            else:
                newline.append(float(datastrs[2]))
            datamatrix.append(newline)
        inputdatalist.append(datamatrix)
        inp.close()
#######statistics########

    z=0 #all is zero
    p=0 #all is 1
    ufav=0
    dead=0
    fav=0
    efs=0
    os=0


######################

    resultmatrix=[]
    for i in range(0,len(sampletitles)):
        dataline=[]
        for j in range(0,len(infiles)):
#            dataline.append(inputdatalist[j][i][1])
            dataline.append(inputdatalist[j][i][0])
#        sortedline=dataline[:]         #!!!!!!!!! if there is no ":", only the address were copied

        if sum(dataline)==0:
            z=z+1
        if sum(dataline)==3:
            p=p+1
        if dataline[0]==0 and dataline[1]+dataline[2]>=1:
            ufav=ufav+1
        if dataline[2]==1 and dataline[0]+dataline[1]<2:
            dead=dead+1
        if dataline[0]==1:
            fav=fav+1
        if dataline[1]==1:
            efs=efs+1
        if dataline[2]==1:
            os=os+1




            #        sortedline.sort(reverse=True)

#        dataline.append(sortedline[0])  #Max
#        dataline.append(sortedline[-1])  #Min
#        datarange=sortedline[0]-sortedline[-1]
#        dataline.append(datarange)  #Range
#        datadiff=sortedline[0]-sortedline[1]
#        dataline.append(datadiff)  #diff
#        dataconf=datadiff/datarange
#        dataline.append(dataconf) #conf
#        if sortedline[0]>0.5:
#            m1predict=infiles[dataline.index(sortedline[0])][1:-12]
#            dataline.append(m1predict)
#        else:
#            dataline.append("")

#        if dataconf>=0.5 and sortedline[0]>0.25:
#            m2predict=infiles[dataline.index(sortedline[0])][1:-12]
#            dataline.append(m2predict)
#        else:
#            dataline.append("")
        resultmatrix.append(dataline)

    outp.write("\n")
    for i in range(0,len(sampletitles)):
        outp.write(sampletitles[i])
        for j in range(0,len(infiles)):
            outp.write("\t%s" % resultmatrix[i][j])
        outp.write("\n")
    outp.close()
    print("all 0 are %d; all 1 are %d; when fav=0 error=%d; when os=1 error=%d\n" % (z,p,ufav,dead))
    print("%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (z,p,ufav,dead,fav,efs,os))





