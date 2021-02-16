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
#include <TApplication.h>

#include "pe_E.h"

//Need to separate the Inner-Detector tubes from the Outer-Detector tubes
static const int innerPMTcode = 1;
static const int vetoPMTcode  = 2;


int main(int argc, char** argv)
{

  // check if minimum arguments exist
  if (argc<5)
    {
      printf("Less than the required number of arguments\n");
      return -1;
    }
 
  //MC extraction
  int detector_threshold = 9;
  double charge_threshold = 0.25;
  int id;
    
  Int_t    gtid=0, mcid=0, subid=0, tot_nhit=0, vetoHit=0;
  Int_t    innerHit=0,innerHitPrev=0,vetoHitPrev=0,triggers=0;

  Double_t totPE=0., innerPE=0., vetoPE=0.;
  Double_t mcx=0., mcy=0., mcz=0., mct=0., mcu=0., mcv=0., mcw=0.;
  Double_t mcxprev=0., mcyprev=0., mczprev=0., mctprev=0., mcuprev=0., mcvprev=0., mcwprev=0.;
  Double_t mc_energy=0., mc_energyPrev=0.;
  Double_t timestamp=0., timestampPrev=0., dt_sub=0., dtPrev_us=0.;
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
  TFile *out=new TFile(argv[2],"RECREATE");
  data=new TTree("data","low-energy detector-triggered events");
  ofstream mc_csvfile;
  mc_csvfile.open (argv[3],ofstream::trunc);
  mc_csvfile << "# event, mcx,  mcy,  mcz,  mcu,  mcv,  mcw,  mct \n";
  ofstream hit_csvfile;
  hit_csvfile.open (argv[4],ofstream::trunc);
  hit_csvfile << "# event, hit, x, y, z, q, id, t \n";
  

  //Define the Integer Tree Leaves
  data->Branch("gtid",&gtid,"gtid/I");
  data->Branch("mcid",&mcid,"mcid/I");
  data->Branch("subid",&subid,"subid/I");
  data->Branch("innerHit",&innerHit,"innerHit/I");//inner detector    
  data->Branch("innerHitPrev",&innerHitPrev,"innerHitPrev/I");//inner detector
  data->Branch("vetoHit",&vetoHit,"vetoHit/I");//veto detector
  data->Branch("vetoHitPrev",&vetoHitPrev,"vetoHitPrev/I");//veto detector
  //Define the double Tree Leaves
  data->Branch("pe",&totPE,"pe/D");
  data->Branch("innerPE",&innerPE,"innerPE/D");
  data->Branch("vetoPE",&vetoPE,"vetoPE/D");
  data->Branch("mc_energy",&mc_energy,"mc_energy/D");
  data->Branch("mc_energyPrev",&mc_energyPrev,"mc_energyPrev/D");
  data->Branch("mcx",&mcx,"mcx/D"); data->Branch("mcy",&mcy,"mcy/D");
  data->Branch("mcz",&mcz,"mcz/D"); data->Branch("mct",&mct,"mct/D");
  data->Branch("mcxprev",&mcxprev,"mcxprev/D"); data->Branch("mcyprev",&mcyprev,"mcyprev/D");
  data->Branch("mczprev",&mczprev,"mczprev/D"); data->Branch("mctprev",&mctprev,"mctprev/D");
  data->Branch("mcu",&mcu,"mcu/D"); data->Branch("mcv",&mcv,"mcv/D");
  data->Branch("mcw",&mcw,"mcw/D"); 
  data->Branch("mcuprev",&mcuprev,"mcuprev/D"); data->Branch("mcvprev",&mcvprev,"mcvprev/D");
  data->Branch("mcwprev",&mcwprev,"mcwprev/D"); 
  
  data->Branch("dt_sub", &dt_sub, "dt_sub/D"); //time of the sub-event trigger from start of the event mc
  data->Branch("dtPrev_us",&dtPrev_us,"dtPrev_us/D"); //global time between consecutive events in us
  data->Branch("timestamp",&timestamp,"timestamp/D"); //trigger time of sub event from start of run
  data->Branch("timestampPrev",&timestampPrev,"timestampPrev/D"); //trigger time of sub event from start of run


  run_summary=new TTree("runSummary","mc run summary");
  run_summary->Branch("nEvents",&n_events,"nEvents/I");
  run_summary->Branch("subEventTally",sub_event_tally,"subEventTally[20]/I");

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
        gtid += 1;
        mcid = event;
        subid = sub_event;
     
        ev = ds->GetEV(sub_event);
        totPE = ev->GetTotalCharge();

        mc_energyPrev = mc_energy;
        mcxprev = mcx;mcyprev=mcy;mczprev=mcz;

        TVector3 temp;
      
        mc = ds->GetMC();
        prim = mc->GetMCParticle(sub_event); 
        mc_energy = prim->GetKE();
        temp = prim->GetPosition();
        mcx = temp.X();
        mcy = temp.Y();
        mcz = temp.Z();
        mct    = prim->GetTime(); // local emission time
        if (subid>0)
          {
          temp = prim->GetEndPosition();
          mcx = temp.X(); 
          mcy = temp.Y(); 
          mcz = temp.Z(); 
          mct    = prim->GetEndTime(); // should be the time of the neutron capture, may cause an issue with re-triggers
          }
        // get true event timings
        // times are in ns unless specified
        timestamp = 1e6*mc->GetUTC().GetSec() + 1e-3*mc->GetUTC().GetNanoSec() + 1e-3*ev->GetCalibratedTriggerTime() - 1e6*run->GetStartTime().GetSec()-1e-3*run->GetStartTime().GetNanoSec(); //global time of subevent trigger (us)
        dtPrev_us = timestamp-timestampPrev; //time since the previous trigger (us)
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
        if (innerHit<detector_threshold)
          {
          continue;
          }
        triggers++;

        // get momentum vector and normalize it (find direction)
        temp = prim->GetMomentum();
        temp = temp.Unit();
        mcu = temp.X();mcv = temp.Y();mcw = temp.Z();
        data->Fill();

	// write the mc data to the other csvfile
	mc_csvfile << event << "," << mcx << "," << mcy << "," << mcz << "," << mcu << "," << mcv << "," << mcw << "," << mct << "\n";
        //save reference values for the next subevent
        mc_energyPrev = mc_energy;
        mcxprev = mcx;mcyprev=mcy;mczprev=mcz;
        timestampPrev = timestamp;
        innerHitPrev = innerHit;
        vetoHitPrev = vetoHit;
      } 
    }
  cout << triggers << " triggered events" << endl;
  out->cd();
  data->Write();
  run_summary->Fill();
  run_summary->Write();
  out->Close();
  //End of MC extraction
  
  /*const char* file = argv[1];
  const char* x_var = "innerPE";
  const char* y_var = "trueEnergy";
  const char* tcut = Form("innerPE>%f",charge_threshold);
  double interval = 0.25;
  
  std::vector<std::vector<double>> params = FitParams_Linear(file, x_var, y_var, tcut);
  std::vector<double> param = params[0];
  std::vector<double> param_err = params[1];
  double p0 = param[0];
  double p1 = param[1];
  double p0_err = param_err[0];
  double p1_err = param_err[1];
  printf("\np0 = %f +/- %f\np1 = %f +/- %f\n", p0, p0_err, p1, p1_err);
  
  std::vector<std::vector<double>> res = resolution(file, x_var, y_var, tcut,params,interval);
  std::vector<double> resolutions = res[0];
  std::vector<double> resolutions_err = res[1];
  std::vector<double> en = res[2];
  
  printf("\nE = %f, res = %f +/- %f\n",en[0],resolutions[0],resolutions_err[0]);
  printf("\nE = %f, res = %f +/- %f\n",en[1],resolutions[1],resolutions_err[1]);
  printf("\nE = %f, res = %f +/- %f\n",en[2],resolutions[2],resolutions_err[2]);
  printf("\nE = %f, res = %f +/- %f\n",en[3],resolutions[3],resolutions_err[3]);
  printf("\nE = %f, res = %f +/- %f\n",en[4],resolutions[4],resolutions_err[4]);
  printf("\nE = %f, res = %f +/- %f\n",en[5],resolutions[5],resolutions_err[5]);
  printf("\nE = %f, res = %f +/- %f\n",en[6],resolutions[6],resolutions_err[6]);
  printf("\nE = %f, res = %f +/- %f\n",en[7],resolutions[7],resolutions_err[7]);
  printf("\nE = %f, res = %f +/- %f\n",en[8],resolutions[8],resolutions_err[8]);
  printf("\nE = %f, res = %f +/- %f\n",en[9],resolutions[9],resolutions_err[9]);
  
  std::vector<double> res_params = plot_res(res,interval);
  double a = res_params[0];
  double b = res_params[1];
  double c = res_params[2];
  
  printf("\nresolution = %f/root(E) + %f + %f/E\n",a,b,c);*/
  
  return 0;
}
