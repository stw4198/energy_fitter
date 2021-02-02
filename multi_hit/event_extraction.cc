// Extracts the MC and pmt hit information from events.
// Also outputs MC and pmt hit data to csvfile
// Author: Stephen Wilson, February 2020
// Heavily adapted from get_features.cc by Elisabeth Kneale, November 2020
// what was adapted in part from bonsai.cc for rat-pac (M. Smy)
// To compile (requires Makefile):
// make get_features
// To run:
// ./get_features ratds.root outfile.csv

#include <iostream>
#include <fstream>
#include <iomanip>

using namespace std;

#include <RAT/DS/Run.hh>
#include <RAT/DS/PMTInfo.hh>
#include <RAT/DS/Root.hh>
#include <RAT/DS/MC.hh>
#include <RAT/DS/MCParticle.hh>
#include <RAT/DS/EV.hh>
#include <RAT/DS/PMT.hh>

#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>

//Need to separate the Inner-Detector tubes from the Outer-Detector tubes
static const int innerPMTcode = 1;
static const int vetoPMTcode  = 2;


int main(int argc, char** argv)
{

  // check if minimum arguments exist
  if (argc<4)
    {
      printf("Less than the required number of arguments\n");
      return -1;
    }
 
  int id;
    
  Int_t    subid=0, vetoHit=0;
  Int_t    innerHit=0,triggers=0;

  Double_t totPE=0., innerPE=0., vetoPE=0.;
  Double_t trueX=0., trueY=0., trueZ=0., trueT=0., trueU=0., trueV=0., trueW=0.;
  Double_t trueEnergy=0.;
  Double_t timestamp=0., dt_sub=0.;
  Int_t sub_event_tally[20] = {};
  Double_t pmtBoundR=0.,pmtBoundZ=0.;

  // root stuff
  TFile *f;
  TTree *rat_tree,*run_tree,*data;
  Int_t n_events;
  TTree *run_summary;

  // rat stuff
  RAT::DS::Root *ds=new RAT::DS::Root();
  RAT::DS::Run  *run=new RAT::DS::Run();
  RAT::DS::EV *ev;
  RAT::DS::PMTInfo *pmtinfo;
  RAT::DS::MC *mc;
  RAT::DS::MCParticle *prim;
  RAT::DS::PMT *pmt;


  // BONSAI stuff
  float       hitpmt[5000][5];
  int         event,sub_event,n,count;
  int         inpmt,vetopmt;
  int         pmtindex,hit,nhit;

  // open input file
  f= new TFile(argv[1]);

  rat_tree=(TTree*) f->Get("T");
  rat_tree->SetBranchAddress("ds", &ds);
  run_tree=(TTree*) f->Get("runT");
  if (rat_tree==0x0 || run_tree==0x0)
    {
      printf("can't find trees T and runT in this file\n");
      return -1;
    }
  run_tree->SetBranchAddress("run", &run);
  if (run_tree->GetEntries() != 1)
    {
      printf("More than one run! Ignoring all but the geometry for the first run\n");
      //return -1;
    }

  // open output files
  ofstream mc_csvfile;
  mc_csvfile.open (argv[2],ofstream::trunc);
  mc_csvfile << "# trueX,  trueY,  trueZ,  trueU,  trueV,  trueW,  trueT \n";
  ofstream hit_csvfile;
  hit_csvfile.open (argv[3],ofstream::trunc);
  hit_csvfile << "event, hit, x, y, z, q, id, t \n";

  run_tree->GetEntry(0);


  // loop over PMTs and find positions and location of PMT support
  pmtinfo=run->GetPMTInfo();
  n=pmtinfo->GetPMTCount();
  inpmt = 0; vetopmt =0;

  //Determines the number of inner and veto pmts
  for(pmtindex=0; pmtindex<n; pmtindex++)
    {
      if (pmtinfo->GetType(pmtindex)==innerPMTcode)     ++inpmt;
      else if (pmtinfo->GetType(pmtindex)==vetoPMTcode) ++vetopmt;
      else
	printf("PMT does not have valid identifier: %d \n",
	       pmtinfo->GetType(pmtindex));
    }
  if (n != (inpmt+vetopmt))
    printf("Mis-match in total PMT numbers: %d, %d \n",n, inpmt+vetopmt);
    

  // get pmt information
  {
    float xyz[3*inpmt+1];

    printf("In total there are  %d PMTs in WATCHMAN\n",n);
    
    for(pmtindex=count=0; pmtindex<n; pmtindex++)
      {
	if(pmtinfo->GetType(pmtindex)==innerPMTcode)
	  {
	    TVector3 pos=pmtinfo->GetPosition(pmtindex);
	    xyz[3*count]=pos[0]*0.1;
	    xyz[3*count+1]=pos[1]*0.1;
	    xyz[3*count+2]=pos[2]*0.1;
	    if (pos[0]>pmtBoundR) pmtBoundR = pos[0];
	    if (pos[2]>pmtBoundZ) pmtBoundZ = pos[2];
	    ++count;
	  }
      }
    
    printf("There are %d inner pmts and %d veto pmts \n ",inpmt,vetopmt);
    printf("Inner PMT boundary (r,z):(%4.1f mm %4.1f, mm)\n",pmtBoundR,pmtBoundZ);

    if (count!= inpmt)
      printf("There is a descrepancy in inner PMTS %d vs %d",count,inpmt);

  }

  n_events = rat_tree->GetEntries();
  // loop over all events
  for (event = 0; event < n_events; event++)
    {
      if (event%1000==0)
        printf("Evaluating event %d of %d (%d sub events)\n",event,n_events,
	      ds->GetEVCount());
      rat_tree->GetEntry(event);


      sub_event_tally[ds->GetEVCount()]++;
      // loop over all subevents
      for(sub_event=0;sub_event<ds->GetEVCount();sub_event++)
        {
        subid = sub_event;
     
        ev = ds->GetEV(sub_event);
        totPE = ev->GetTotalCharge();

        TVector3 temp;
      
        mc = ds->GetMC();
        prim = mc->GetMCParticle(sub_event); 
        trueEnergy = prim->GetKE();
        temp = prim->GetPosition();
        trueX = temp.X();
        trueY = temp.Y();
        trueZ = temp.Z();
        trueT    = prim->GetTime(); // local emission time
        if (subid>0)
          {
          temp = prim->GetEndPosition();
          trueX = temp.X(); 
          trueY = temp.Y(); 
          trueZ = temp.Z(); 
          trueT    = prim->GetEndTime(); // should be the time of the neutron capture, may cause an issue with re-triggers
          }
        // get true event timings
        // times are in ns unless specified
        //timestamp = 1e6*mc->GetUTC().GetSec() + 1e-3*mc->GetUTC().GetNanoSec() + 1e-3*ev->GetCalibratedTriggerTime() - 1e6*run->GetStartTime().GetSec()-1e-3*run->GetStartTime().GetNanoSec(); //global time of subevent trigger (us)
        dt_sub = ev->GetCalibratedTriggerTime(); //trigger time (first pmt hit time) from start of event mc

        nhit=ev->GetPMTCount();

        // loop over all PMT hits for each subevent
        innerPE=0;vetoPE=0;    
        for(hit=innerHit=vetoHit=0; hit<nhit; hit++)
          {
          pmt=ev->GetPMT(hit);
          id = pmt->GetID();
          //only use information from the inner pmts
          if(pmtinfo->GetType(id) == innerPMTcode)
            {
            TVector3 pos=pmtinfo->GetPosition(id);
            hitpmt[innerHit][0]=pos[0]*0.1;    //x
            hitpmt[innerHit][1]=pos[1]*0.1;       //y
            hitpmt[innerHit][2]=pos[2]*0.1;       //z
            hitpmt[innerHit][3]=pmt->GetTime();   //t
            hitpmt[innerHit][4]=pmt->GetCharge(); //q
            innerPE += pmt->GetCharge();
            ofstream save;
            hit_csvfile << event << "," << hit << "," << pos[0]*0.1 << "," << pos[1]*0.1 << "," << pos[2]*0.1 << "," << pmt->GetCharge() << "," << id << "," << pmt->GetTime() << "\n";
            innerHit++;
            }
          else if(pmtinfo->GetType(id)== vetoPMTcode)
            {
            vetoPE += pmt->GetCharge();    
            vetoHit++;
            }
          else
            printf("Unidentified PMT type: (%d,%d) \n",count,pmtinfo->GetType(id));
          } // end of loop over all PMT hits
        triggers++;

        // get momentum vector and normalize it (find direction)
        temp = prim->GetMomentum();
        temp = temp.Unit();
        trueU = temp.X();trueV = temp.Y();trueW = temp.Z();

	// write the mc data to the other csvfile
	mc_csvfile << trueX << "," << trueY << "," << trueZ << "," << trueU << "," << trueV << "," << trueW << "," << trueT << "\n";
      } 
    }
  cout << triggers << " triggered events" << endl;
  return 0;
}

