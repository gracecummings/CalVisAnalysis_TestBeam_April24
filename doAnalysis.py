#import ROOT
import os
import datetime
import argparse
import uproot
import matplotlib.pyplot as plt
import awkward as ak


def makeOutFile(descrip,ftype):
    strpath = "testbeam_plots/"+str(datetime.date.today())+"/"
    now = datetime.datetime.now()
    strdatetime = now.strftime("%y-%m-%d_%H-%M")
    if not os.path.exists(strpath):
        os.makedirs(strpath)
        
    outFile = strpath+"testbeam_plots_run"+descrip+"_"+strdatetime+ftype
    return outFile

parser = argparse.ArgumentParser()

if __name__ =="__main__":
    parser.add_argument("-r","--runnum",type=int)
    parser.add_argument("-f","--infile",type=str)
    args = parser.parse_args()

    runnum = args.runnum

    #outFile = makeOutFile(str(runnum),".root")

    with uproot.open(args.infile) as f:
        print(f['tree;3']['trigger_time'].array())
        print(f['tree;3']['time'].array())
        print(f['tree;3']['channels'].array())
        #print(ak.to_dataframe(f['tree;3']['channels'].array()))
        ak_arrays = f['tree;3']['channels'].arrays(library="pd")
        print(ak_arrays)

        #fig,ax=plt.subplots()
        #ax.plot(f['tree;3']['time']
