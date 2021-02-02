#include <TCanvas.h>
#include <TFile.h>
#include <TString.h>

//Need to seperate the Inner-Detector tubes from the Outer-Detector tubes
static const int innerPMTcode = 1;
static const int vetoPMTcode  = 2;

void event_extraction() {

	std::remove("charge.txt");

	int tot_inner,tot_veto,id;

	Int_t nhits=0;
	Int_t inner_hit=0;

	Int_t sub_event_tally[20] = {};

	Double_t totPE=0., innerPE=0., vetoPE=0.;

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
	
	float charges[5000];
	int event,sub_event,n,count;
	int inpmt;
	int hit,nhit,veto_count;

	f = new TFile("wbls_3pc_discrete.root");
	rat_tree = (TTree*)f->Get("T");
	rat_tree->SetBranchAddress("ds",&ds);
	run_tree = (TTree*)f->Get("runT");
	run_tree->SetBranchAddress("run", &run);
	
	run_tree->GetEntry(0);
	
	// loop over PMTs and find positions and location of PMT support
	pmtinfo=run->GetPMTInfo();
	n=pmtinfo->GetPMTCount();
	tot_inner = 0; tot_veto =0;
 
 	printf("\nn = %i\n",n);
 
	//Determines the number of inner and veto pmts
	for(hit=0; hit<n; hit++)
		{
			if (pmtinfo->GetType(hit)==innerPMTcode)     ++tot_inner;
			else if (pmtinfo->GetType(hit)==vetoPMTcode) ++tot_veto;
			else
				printf("PMT does not have valid identifier: %d \n",
					pmtinfo->GetType(hit));
		}
	if (n != (tot_inner+tot_veto))
		printf("Mis-match in total PMT numbers: %d, %d \n",n, tot_inner+tot_veto);
    
	inpmt= tot_inner;
	printf("\n%i PMTs\n",inpmt);
	
	n_events = rat_tree->GetEntries();
	printf("\n%d events\n",n_events);
	
	//loop over all events (up to nevents)
	for (event = 0; event < n_events; event++)
		{
			rat_tree->GetEntry(event);
			sub_event_tally[ds->GetEVCount()]++;
			//printf("\nsub events = %i\n",ds->GetEVCount());
			//loop over subevents
			for (sub_event=0;sub_event<ds->GetEVCount();sub_event++)
				{
					//printf("\nsub_event = %i\n",ds->GetEVCount());
					ev = ds->GetEV(sub_event);
					totPE = ev->GetTotalCharge();
					//printf("\ntotPE = %i\n",totPE);
					nhit=ev->GetPMTCount();
					printf("\nnhit = %i\n",nhit);
					innerPE=0;vetoPE=0;	
					//loop over hits for each subevents (up to nhits)
					for(hit=count=veto_count=0;hit<nhit;hit++)
						{
							pmt=ev->GetPMT(hit);
							id = pmt->GetID();
							if(pmtinfo->GetType(id) == innerPMTcode)
								{
									charges[count]=pmt->GetCharge();
									//printf("\nevent = %i, charge = %f, id = %i\n",event,charges[count],id);
									innerPE += pmt->GetCharge();
									//printf("\ninnerPE = %f\n",innerPE);
									printf("\nevent = %i, hit = %i, charge = %f\n",event,hit,pmt->GetCharge());
									ofstream save;
									save.open ("charge.txt", std::ios_base::app);
									save << "event = " << event << ", charge = " << charges[count] << " , pmt = " << id << "\n";
									save.close();
									count++;
								}
							inner_hit = count;
							nhit = count;
							//printf("\ninner hit = %i\n",inner_hit);
						}
					//printf("\ninnerPE = %i\n",innerPE);
				}
			//printf("\nevent = %i\n",event);
			//printf("\ninnerPE = %i\n",innerPE);
		}

}
