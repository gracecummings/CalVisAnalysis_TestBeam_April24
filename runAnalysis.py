import ROOT
import os
import datetime
import argparse

def makeOutFile(descrip,ftype):
    strpath = "testbeam_plots/"+str(datetime.date.today())+"/"
    now = datetime.datetime.now()
    strdatetime = now.strftime("%y-%m-%d_%H-%M")
    if not os.path.exists(strpath):
        os.makedirs(strpath)
        
    outFile = "testbeam_plots_run"+descrip+"_"+strdatetime+ftype
    return outFile

parser = argparse.ArgumentParser()

if __name__ =="__main__":
    parser.add_argument("-r","--runnum",type=int)
    parser.add_argument("-f","--infile",type=str)
    args = parser.parse_args()

    runnum = args.runnum

    outFile = makeOutFile(str(runnum),".root")

    inChain = ROOT.TChain("tree")
    inChain.Add(args.infile)

    ROOT.gSystem.CompileMacro("Analysis.C","kfc")
    ROOT.gSystem.Load('Analysis_C')
    plotter = ROOT.Analysis(inChain)
    plotter.Loop(outFile)
