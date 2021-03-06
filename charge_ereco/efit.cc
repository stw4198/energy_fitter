#include "efit.h"

std::vector<std::vector<double>> FitParams_Linear(const char* file, const char* x_var, const char* y_var, const char* tcut, const char* fit_file, int args){

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

std::vector<std::vector<double>> resolution(const char* file, const char* x_var, const char* y_var, const char* tcut, std::vector<std::vector<double>> params, std::vector<double> y_int, double interval, const char* res_file, int args){

  std::vector<double> fit = params[0];
  std::vector<double> fit_err = params[1];

  std::vector<double> resolution;
  std::vector<double> resolution_err;
  
  TFile* f = new TFile(file);
  TTree *t = (TTree*)f->Get("data");
  
  const char* tgraph = Form("(%f*%s) + (%f) - %s>>hist",fit[1],x_var,fit[0],y_var);
  
  int y_n = y_int.size();
  
  if(args>3){
  std::remove(Form("%s.csv",res_file));
  }
  
  for(int i = 0; i<y_n; i++) {
  
    double y1 = y_int[i] - interval;
    double y2 = y_int[i] + interval;
    
    TCanvas *fit_canvas = new TCanvas("Fitted Data", "Fit");
    
    const char* tcut_range = Form("%s && %s > %f && %s < %f",tcut,y_var,y1,y_var,y2);
    
    t->Draw(tgraph,tcut_range);
    TH2 *hist = (TH2*)gDirectory->Get("hist");
    hist->GetXaxis()->SetTitle(Form("E$_{reco}$ - E$_{true}$ [MeV]"));
    hist->Fit("gaus","Q");
    hist->SetTitle(Form("#DeltaE, E$_{true}$ = %f",y_int[i]));
    
    int n = hist->GetEntries();
    
    double sigma = hist->GetFunction("gaus")->GetParameter(2);
    double sigma_err = hist->GetFunction("gaus")->GetParError(2);
    double mean = hist->GetFunction("gaus")->GetParameter(1);
    double mean_err = hist->GetFunction("gaus")->GetParError(1);
    double res = hist->GetFunction("gaus")->GetParameter(2)/y_int[i];
    double res_err = res * sqrt(1/n + (sigma_err/sigma)*(sigma_err/sigma));
    
    if(args>3){
      std::ofstream res_csv;
      res_csv.open (Form("%s.csv",res_file),std::ofstream::app);
      res_csv << "# E [MeV], E_err [MeV], sigma [MeV], sigma_err [MeV], mean [MeV], mean_err [MeV], resolution, resolution_err\n";
      res_csv << y_int[i] << ',' << interval/sqrt(12) << ',' << sigma << ',' << sigma_err << ',' << mean << ',' << mean_err << ',' << res << ',' << res_err << '\n';
      res_csv.close();
    }
  
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

std::vector<std::vector<double>> plot_res(std::vector<std::vector<double>> res_plus_err,double interval, const char* fit_file, const char* plot_name, int args){

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
  graph->SetMarkerColor(1);
  graph->SetLineColor(1);
  TCanvas *canvas = new TCanvas("Resolution", "Resolution");
  graph->GetXaxis()->SetTitle("E_{MC} [MeV]");
  graph->GetYaxis()->SetTitle("#sigma_{E}/E_{MC}");
  graph->GetYaxis()->SetTitleOffset(1.1);
  graph->SetTitle("Resolution using Photoelectrons");
  graph->Draw("AP");
  
  TF1 *fitfn = new TF1("fitfn",fit_func,en_arr[0],en_arr[n-1],3);
  fitfn->SetParameter(0,0);
  fitfn->SetParameter(1,0);
  fitfn->SetParameter(2,0);
  
  graph->Fit("fitfn","Q0");
  fitfn->SetLineColor(6);
  fitfn->SetLineStyle(2);
  fitfn->Draw("Same");
  
  TF1 *fitresult = graph->GetFunction("fitfn");

  double a = fitresult->GetParameter(0);
  double a_err = fitresult->GetParError(0);
  double b = fitresult->GetParameter(1);
  double b_err = fitresult->GetParError(1);
  double c = fitresult->GetParameter(2);
  double c_err = fitresult->GetParError(2);
  
  TLegend *leg = new TLegend(.55,.7,.9,.9);
  leg->SetFillColor(0);
  graph->SetFillColor(0);
  leg->AddEntry(graph,"resolution (pe)","lE");
  leg->AddEntry(fitfn,Form("%.3f/#sqrt{E} + %.3f + %.3f/E",a,b,c));
  leg->SetTextSize(0.03);
  leg->DrawClone("Same");
  
  if(args>4){
    canvas->SaveAs(Form("%s.pdf",plot_name),"Q");
  }
  canvas->Draw();
  
  std::vector<double> params;
  std::vector<double> params_err;
  std::vector<std::vector<double>> parameters;
  
  params.push_back(a);
  params.push_back(b);
  params.push_back(c);
  
  params_err.push_back(a_err);
  params_err.push_back(b_err);
  params_err.push_back(c_err);
  
  parameters.push_back(params);
  parameters.push_back(params_err);  
  
  delete graph;
  delete fitfn;
  delete canvas;
  
  return parameters;

}

int main(int argc, char** argv) {

  if (argc<2)
    {
      printf("Less than the required number of arguments\n");
      return -1;
    }
  
  gROOT->SetBatch(kTRUE);
  
  const char* file = argv[1]; //input file
  int args = argc; //number of arguments
  const char* fit_file;
  const char* res_file;
  const char* plot_name;
  
  switch(argc) {
    case 2:
      printf("\nOnly input file provided, all other values set to default.\n");
      break;
    case 3:
      fit_file = argv[2]; //output file for fit parameters + resolution fit
      printf("\n\nSaving fit parameters to %s.csv.\n\n",fit_file);
      break;
    case 4:
      fit_file = argv[2]; //output file for fit parameters + resolution fit
      res_file = argv[3]; //output file for resolution
      printf("\n\nSaving fit parameters to %s.csv, resolution to %s.csv.\n\n",fit_file,res_file);
      break;
   case 5:
      fit_file = argv[2]; //output file for fit parameters + resolution fit
      res_file = argv[3]; //output file for resolution
      plot_name = argv[4];
      printf("\n\nSaving fit parameters to %s.csv, resolution to %s.csv. Plotting resolution as %s.pdf.\n\n",fit_file,res_file,plot_name);
      break;
  }
  
  const char* x_var = "innerPE";
  const char* y_var = "mc_energy";
  const char* tcut = "innerPE>0.25";

  double interval = 0.25;

  std::vector<std::vector<double>> fit_parameters = FitParams_Linear(file, x_var, y_var, tcut, fit_file, args);
  std::vector<double> fit_params = fit_parameters[0];
  std::vector<double> fit_err_params = fit_parameters[1];
  double p0 = fit_params[0];
  double p1 = fit_params[1];
  double p0_err = fit_err_params[0];
  double p1_err = fit_err_params[1];
  
  std::vector<double> energy = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  
  std::vector<std::vector<double>> res = resolution(file, x_var, y_var, tcut,fit_parameters,energy,interval,res_file,args);
  
  std::vector<std::vector<double>> res_parameters = plot_res(res,interval,fit_file,plot_name,args);
  std::vector<double> res_params = res_parameters[0];
  std::vector<double> res_err_params = res_parameters[1];
  double a = res_params[0];
  double b = res_params[1];
  double c = res_params[2];
  double a_err = res_err_params[0];
  double b_err = res_err_params[1];
  double c_err = res_err_params[2];
  
  if(args>2){
    std::ofstream params_csv;
    params_csv.open (Form("%s.csv",argv[2]),std::ofstream::trunc);
    params_csv << "# p0, p0_err, p1, p1_err, a, a_err, b, b_err, c, c_err, E = p1*innerPE +p0, res/E = a/sqrt(E) + b + c/E\n";
    params_csv << p0 << ',' << p0_err << ',' << p1 << ',' << p1_err << ',' << a << ',' << a_err << ',' << b << ',' << b_err << ',' << c << ',' << c_err;
    params_csv.close();
  }
  
  return 0;
  
}
