#ifndef EFIT_H
#define EFIT_H

#include <iostream>
#include <fstream>
#include <iomanip>
#include <math.h>

#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TCanvas.h>
#include <TLegend.h>
#include "TGraphErrors.h"
#include "TF1.h"
#include "TH2.h"

std::vector<std::vector<double>> FitParams_Linear(const char* file, const char* x_var, const char* y_var, const char* tcut, const char* fit_file, int args);

std::vector<std::vector<double>> resolution(const char* file, const char* x_var, const char* y_var, const char* tcut, std::vector<std::vector<double>> params, std::vector<double> y_int, double interval, int args);

Double_t fit_func(Double_t *x, Double_t *par);

std::vector<std::vector<double>> plot_res(std::vector<std::vector<double>> res_plus_err,double interval, const char* fit_file, const char* plot_name, int args);

#endif
