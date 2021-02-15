#include "pe_E.h"
#include <iostream>
#include <fstream>
#include <iomanip>
#include <math.h>

//using namespace std;

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
#include <TCanvas.h>
#include <TString.h>
#include "TGraphErrors.h"
#include "TF1.h"
#include "TH2.h"
//#include "TStyle.h"

// Produce fit between two variables in ROOT

int main(){

  void pe_E();

  return 1;

}

void pe_E(){

  gROOT->SetBatch(kTRUE);

  const char* file = "../../merged_flat_MC_wbls_3pc_baseline.root";
  const char* x_var = "innerPE";
  const char* y_var = "trueEnergy";
  const char* tcut = "innerPE>0.25";

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
  
  double e = plot_res(res,interval);
  
}

std::vector<std::vector<double>> FitParams_Linear(const char* file, const char* x_var, const char* y_var, const char* tcut){

  const char* tgraph = Form("%s:%s>>hist",y_var,x_var);

  TCanvas *fit_prod = new TCanvas("Fit Production", "Fit Production");
  TFile* f = new TFile(file);
  TTree *t = (TTree*)f->Get("data");
  
  t->Draw(tgraph,tcut);
  TH2 *hist = (TH2*)gDirectory->Get("hist");
  hist->Fit("pol1","Q");
  
  TF1 *fitresult = hist->GetFunction("pol1");

  double p0 = fitresult->GetParameter(0);
  double p1 = fitresult->GetParameter(1);
  
  double p0_err = fitresult->GetParError(0);
  double p1_err = fitresult->GetParError(1);
  
  std::vector<double> params;
  std::vector<double> param_errs;
  
  params.push_back(p0);
  params.push_back(p1);
  param_errs.push_back(p0_err);
  param_errs.push_back(p1_err);
  
  std::vector<std::vector<double>> parameters;
  parameters.push_back(params);
  parameters.push_back(param_errs);
  
  delete hist;
  delete f;
  delete fit_prod;
  
  return parameters;
}

std::vector<std::vector<double>> resolution(const char* file, const char* x_var, const char* y_var, const char* tcut, std::vector<std::vector<double>> params, double interval){

//need energy as input
//extract number of unique energy values?
//extract min and max energy
//set interval
//loop over all energy cuts

  std::vector<double> fit = params[0];
  std::vector<double> fit_err = params[1];
  /*double p0 = param[0];
  double p1 = param[1];
  double p0_err = param_err[0];
  double p1_err = param_err[1];*/

  std::vector<double> resolution;
  std::vector<double> resolution_err;
  
  //gROOT->SetBatch(True);
  
  TFile* f = new TFile(file);
  TTree *t = (TTree*)f->Get("data");
  
  const char* tgraph = Form("(%f*%s) + (%f) - %s>>hist",fit[1],x_var,fit[0],y_var);
  
  std::vector<double> y_int = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}; //set dynamically
  
  //loop over list of energy values, not true energy
  for(int i = 0; i<y_int.size(); i++) {
  
    double y1 = y_int[i] - interval;
    double y2 = y_int[i] + interval;
    
    TCanvas *fit_canvas = new TCanvas("Fitted Data", "Fit");
    
    const char* tcut_range = Form("%s && %s > %f && %s < %f",tcut,y_var,y1,y_var,y2);
    
    t->Draw(tgraph,tcut_range);
    TH2 *hist = (TH2*)gDirectory->Get("hist");
    hist->GetXaxis()->SetTitle(Form("E$_{reco}$ - E$_{true}$ [MeV]"));
    hist->Fit("gaus","Q");
    //gStyle->SetOptFit(11);
    hist->SetTitle(Form("#DeltaE, E$_{true}$ = %f",y_int[i]));
    
    int n = hist->GetEntries();
    
    double sigma = hist->GetFunction("gaus")->GetParameter(2);
    double sigma_err = hist->GetFunction("gaus")->GetParError(2);
    double mean = hist->GetFunction("gaus")->GetParameter(1);
    double mean_err = hist->GetFunction("gaus")->GetParError(1);
    double res = hist->GetFunction("gaus")->GetParameter(2)/y_int[i];
    double res_err = res * sqrt(1/n + (sigma_err/sigma)*(sigma_err/sigma));
  
    resolution.push_back(res);
    resolution_err.push_back(res_err);
    
    delete hist;
    delete fit_canvas;
  
  }
  
  std::vector<std::vector<double>> res_plus_err;
  res_plus_err.push_back(resolution);
  res_plus_err.push_back(resolution_err);
  res_plus_err.push_back(y_int);

  delete f;

  return res_plus_err;

}

Double_t fit_func(Double_t *x, Double_t *par){

  Double_t fitval = par[0]/sqrt(x[0]) + par[1] + par[2]/x[0];

  return fitval;

}

/*double fit_resolution(const char* file, std::vector<std::vector<double>> res_plus_err) {

  //std::vector<double> resolution = res_plus_err[0];
  //std::vector<double> resolution_err = res_plus_err[1];
  //std::vector<double> energy = res_plus_err[2];
  
  //double a;
  //double b;
  //double c;
  
  //const char* tgraph = Form("%s:%s>>hist",y_var,x_var);

  TCanvas *fit_res = new TCanvas("Fit", "Fit");
  TFile* f = new TFile(file);
  TTree *t = (TTree*)f->Get("data");
  
  t->Draw("trueEnergy:innerPE>>hist","innerPE>0.25");
  TH2 *hist = (TH2*)gDirectory->Get("hist");
  //hist->Fit("pol1","Q");
  
  TF1 *fit_func = new TF1("fit_func",fit_func,0,10,3);
  fit_func->SetParameters(0,0,0);
  fit_func->SetParNames("p0","p1","p2");
  hist->Fit(fit_func,"r");
  
  fit_res->Draw();
  
  //res_fit = 
  delete hist;
  delete fit_res;
  delete f;
  
  double e = 1;
  return e;
  //return fit_params;
}*/

double plot_res(std::vector<std::vector<double>> res_plus_err,double interval){

  std::vector<double> resolution = res_plus_err[0];
  std::vector<double> resolution_err = res_plus_err[1];
  std::vector<double> energy = res_plus_err[2];
  const int n = energy.size();
  
  double res_arr[n];
  std::copy(resolution.begin(),resolution.end(),res_arr);
  double res_err_arr[n];
  std::copy(resolution_err.begin(),resolution_err.end(),res_err_arr);
  double en_arr[n];
  std::copy(energy.begin(),energy.end(),en_arr);
  
  double en_err[n];
  std::fill_n(en_err, n, interval/sqrt(12));
  
  TGraphErrors *graph = new TGraphErrors(n,en_arr,res_arr,en_err,res_err_arr);
  graph->SetMarkerStyle(2);
  graph->SetMarkerColor(6);
  graph->SetLineColor(6);
  TCanvas *Canvas_3_2_1 = new TCanvas("Resolution", "Resolution");
  graph->GetXaxis()->SetTitle("E_{true} [MeV]");
  graph->GetYaxis()->SetTitle("#sigma/E");
  graph->GetYaxis()->SetTitleOffset(1.1);
  graph->DrawClone("APE");
  
  TLegend *leg = new TLegend(.7,.7,.9,.9,"Resolution");
  leg->SetFillColor(0);
  graph->SetFillColor(0);
  leg->AddEntry(graph,"pe fit","lE");
  //leg.AddEntry(&function_3_2_1,"Th. Law");
  leg->DrawClone("Same");
  
  Canvas_3_2_1->SaveAs("test.pdf");
  Canvas_3_2_1->Draw();
  
  //TF1 *fit_func = new TF1("fit_func",fit_func,0,10,3);
  TCanvas *canvas = new TCanvas("canvas", "fit");
  TH2D *hist = new TH2D("hist", "Resolution Fit",100,en_arr[0],en_arr[n],100,res_arr[n],res_arr[0]);
  for(int i=0;i<n;i++){
    hist->Fill(en_arr[i],res_arr[i]);
  }
  hist->SetMarkerStyle(2);
  hist->Draw();
  canvas->SaveAs("hist.pdf");
  
  /*fit_func->SetParameter(0,0);
  fit_func->SetParameter(1,0);
  fit_func->SetParameter(2,0);
  
  TF1 *fitresult = hist->GetFunction(&fit_func);

  double a = fitresult->GetParameter(0);
  double b = fitresult->GetParameter(1);
  double c = fitresult->GetParameter(2);*/
  
  double e = 1;
  return e;

}
