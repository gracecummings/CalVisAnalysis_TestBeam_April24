#define Analysis_cxx
#include "Analysis.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <iostream>

void Analysis::Loop(std::string outputFileName)
{
//   In a ROOT session, you can do:
//      root> .L Analysis.C
//      root> Analysis t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;

      //debug
      std::cout<<"Checking event: "<<jentry<<std::endl;
      if (jentry > 10) break;

      //Print some stuff
      //std::cout<<"        Samples: "<<samples<<std::endl;
      //std::cout<<"    Trig offset: "<<trigger_offset<<std::endl;
      //std::cout<<"      Trig time: "<<trigger_time<<std::endl;
      //std::cout<<"    hori offset: "<<horizontal_offset<<std::endl;
      //std::cout<<"  hori interval: "<<horizontal_interval<<std::endl;

      //Pulse analysis
      TGraph * grSnglPul[8];

      for (int ich=0;ich<8; ich++){
	grSnglPul[ich] = new TGraph();
	for (int isamp=0;isamp<samples;isamp++){
	  grSnglPul[ich]->SetPoint(isamp,(time[isamp]-trigger_time) * 1e+9,channels[ich][isamp]);
	}
      }
      
   }
}
