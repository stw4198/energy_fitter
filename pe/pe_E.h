#ifndef PE_E_H
#define PE_E_H

#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TCanvas.h>

std::vector<std::vector<double>> FitParams_Linear(const char* file, const char* x_var, const char* y_var, const char* tcut);
std::vector<std::vector<double>> resolution(const char* file, const char* x_var, const char* y_var, const char* tcut, std::vector<std::vector<double>> params, double interval);
Double_t fit_func(Double_t *x, Double_t *par);
std::vector<std::vector<double>> plot_res(std::vector<std::vector<double>> res_plus_err,double interval);

#endif
