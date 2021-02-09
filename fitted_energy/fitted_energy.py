import argparse
import os
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
try:
	import ROOT as root
	from ROOT import gStyle
	from ROOT import TStyle
	from ROOT import TCanvas, TGraphErrors
	from ROOT import gROOT
	from ROOT import TPaveText
except ImportError:
	print("Could not import ROOT. Source thisroot.sh first.")
	exit(1)

np.set_printoptions(suppress=True)

Tol_bright = ['#4477AA','#66CCEE','#228833',
                     '#CCBB44','#EE6677','#AA3377','#BBBBBB','k']

class Fitted_Energy():

	def __init__(self, bonsai_fn=None, load_lib=True):
		self.bonsai_fn = bonsai_fn
		self.load_lib = load_lib

	def parse_options(self, argv=None):
		parser = argparse.ArgumentParser()
		parser.add_argument("bonsai_fn", help="filepath to the bonsai file \
			containing reconstructed events", type=str)
		args = parser.parse_args(argv)
		if self.load_lib:
			root.gSystem.Load('libRATEvent.so')
			print("ROOT: Loaded libRATEvent.so")
		self.bonsai_fn = args.bonsai_fn
		self.bonsai_file = self.is_valid_file(parser, self.bonsai_fn, type="UPDATE")
		self.get_file_data()

	def get_file_data(self):
		self.bonsai_t = self.bonsai_file.Get("data")
		self.bonsai_rt = self.bonsai_file.Get("runSummary")
		
	@staticmethod
	def is_valid_file(parser, arg, type="READ"):
		if not os.path.exists(arg):
			parser.error(f"File {arg} does not exist.")
		else:
			return root.TFile(arg, type)
			
	def read_from_tree(self, br_name):
		# Read values of branch br_name from bonsai tree into np array
		values = self.bonsai_t.AsMatrix(columns=[br_name])
		return values
			
	def energy_values(self,interval):
		mc_energy = self.read_from_tree("mc_energy")
		Emax = max(mc_energy)
		E = np.arange(0,Emax+interval,interval)
		E_cut = []
		for i in range(len(E)):
			E_cut.append("mc_energy > %f && mc_energy < %f" % (E[i]-0.5*interval,E[i]+0.5*interval))
		return(mc_energy,Emax,E,E_cut[1:])
		
	def pe_values(self,conditions):
		innerPE = self.read_from_tree("pe")
		return(innerPE)
		
	def make_fit(self, conditions):
		#medium,medium_save = self.medium_detect()
		gROOT.SetBatch(True)
		c1 = TCanvas( "c1" , "Fit Production", 200, 10, 700 ,500)
		self.bonsai_t.Draw("mc_energy:innerPE>>hist",conditions)
		hist = root.gDirectory.Get("hist")
		hist.Fit("pol1", "Q")
		hist.GetYaxis().SetTitle("E_{True} [MeV]")
		hist.GetXaxis().SetTitle("Photoelectrons")
		hist.SetTitle("Production of fit between E_{True} and photoelectrons")
		#save_dir = self.make_directory(medium_save)
		#c1.SaveAs("fit_production.png")
		
		p0 = hist.GetFunction("pol1").GetParameter(0)
		p1 = hist.GetFunction("pol1").GetParameter(1)
		p0_err = hist.GetFunction("pol1").GetParError(0)
		p1_err = hist.GetFunction("pol1").GetParError(1)
		fit = (p0, p1)
		fit_err = (p0_err, p1_err)
		print("\np0 = %.5e +/- %.5e\np1 = %.5e +/- %.5e\n" % (fit[0],abs(fit_err[0]),fit[1],abs(fit_err[1])))

		del c1

		return (fit,fit_err)
		
	def fit(self,e,a,b,c):
		return(a/np.sqrt(e) + b + c/e)
		
	def use_fit(self):
		conditions = "innerPE > 0.25 && closestPMT > 0 && n100 > 0"
		#fit,fit_err = self.make_fit(conditions)
		mc_energy,Emax,E,E_cut = self.energy_values(0.25)
		fit,fit_err,sigma,sigma_err,resolution,resolution_err = self.resolution_testing()
		E = E[1:]
		E_err = 0.25/np.sqrt(12)
		
		popt, pcov = curve_fit(self.fit, E, resolution)
		plt.errorbar(E[1:],resolution[1:],yerr=resolution_err[1:],linestyle='none',xerr=E_err)
		plt.xlabel("Kinetic Energy [MeV]")
		plt.ylabel("Resolution [\u03C3/E]")
		plt.show()
		
		#innerPE = self.pe_values(conditions)
		innerPE = np.arange(0,300,1)
		e = fit[1]*innerPE + fit[0]
		e_err = popt[0]*np.sqrt(e) + e*popt[1] + popt[2]
		
		plt.plot(innerPE,e,color=Tol_bright[7],label="E$_{reco}$")
		plt.fill_between(innerPE, e-e_err, e+e_err,color=Tol_bright[3],label="$\pm$\u03C3")
		plt.ylabel("E$_{reco}$ [MeV]")
		plt.xlabel("Photoelectrons")
		plt.grid()
		plt.legend()
		plt.show()
		
		#plt.errorbar(mc_energy,e,marker='x',linestyle='none')
		#plt.show()
		
	def call_fit(self):
		#if "wbls" in medium_save:
		conditions = "innerPE > 0.25 && closestPMT > 0 && n100 > 0"
		#elif "wbls" not in medium_save:
		#conditions = "innerPE > 0.25 && -3000 < x < 3000 && -3000 < z < 3000 && n100 > 0"
		fit,fit_err = self.make_fit(conditions)
		
		with open("stats_test.txt",'w') as stats:
			stats.write("Medium = WbLS\n")
			stats.write("p0 = %.5e\n" % fit[0])
			stats.write("p0 error = %.5e\n" % fit_err[0])
			stats.write("p1 = %.5e\n" % fit[1])
			stats.write("p1 error = %.5e\n" % fit_err[1])

	def resolution_testing(self):
		#if "wbls" in medium_save:
		conditions = "innerPE > 0.25 && closestPMT > 0 && n100 > 0"
		#elif "wbls" not in medium_save:
		#conditions = "innerPE > 0.25 && -3000 < x < 3000 && -3000 < z < 3000 && n100 > 0"
		fit,fit_err = self.make_fit(conditions)
		mc_energy,Emax,E,E_cut = self.energy_values(0.25)
		#try:
		#	os.remove("/stats_test.txt")
		#except:
		#	print("stats_test.txt not found")
		#if self.charge == 1:
		graph = ("(%f*innerPE) + %f - mc_energy>>deltaE" % (fit[1],fit[0]))
		gROOT.SetBatch(True)
		c_all = TCanvas( "c_all" , "Delta E", 200, 10, 700 ,500)
		self.bonsai_t.Draw(graph,conditions)
		deltaE = root.gDirectory.Get("deltaE")
		deltaE.Fit("gaus","Q")
		gStyle.SetOptFit(11)
		deltaE.SetTitle("#DeltaE")
		deltaE.GetXaxis().SetTitle("#DeltaE [MeV]")
		deltaE.GetXaxis().SetRangeUser(-.4*E[-1],.4*Emax[-1])
		#c_all.SaveAs("Gaussian_fit_all.png")
		#else:
		#	graph = ("(%s*%s*%f) + (%s*%f) + %f - mc_energy>>deltaE" % (self.nwindow,self.nwindow,fit[2],self.nwindow,fit[1],fit[0]))
		#	gROOT.SetBatch(True)
		#	c_all = TCanvas( "c_all" , "Delta E "+medium, 200, 10, 700 ,500)
		#	self.bonsai_t.Draw(graph,conditions)
		#	deltaE = root.gDirectory.Get("deltaE")
		#	deltaE.Fit("gaus","Q")
		#	gStyle.SetOptFit(11)
		#	deltaE.SetTitle("#DeltaE %s" % medium)
		#	deltaE.GetXaxis().SetTitle("#DeltaE [MeV]")
		#	deltaE.GetXaxis().SetRangeUser(-.4*E[-1],.4*Emax[-1])
		#	c_all.SaveAs("%s/Gaussian_fit_%s.png"%(save_dir,medium_save))

		del c_all
		del deltaE

		E = E[1:]

		sigma_arr = []
		sigma_err_arr = []
		res_arr = []
		res_err_arr = []

		#with open("stats_test.txt",'a') as stats:
		#	stats.write("Medium = WbLS\n")
		#	stats.write("p0 = %.5e\n" % fit[0])
		#	stats.write("p0 error = %.5e\n" % fit_err[0])
		#	stats.write("p1 = %.5e\n" % fit[1])
		#	stats.write("p1 error = %.5e\n" % fit_err[1])

		for i in tqdm(range(len(E_cut)),desc="Applying fit to all energies"):
			c1 = TCanvas("c1" , "Delta E", 200, 10, 700 ,500)
			condition = "%s && %s" %(conditions,E_cut[i])
			self.bonsai_t.Draw(graph,condition)
			deltaE = root.gDirectory.Get("deltaE")
			deltaE.Fit("gaus","Q")
			gStyle.SetOptFit(11)
			deltaE.SetTitle("E_{centre} = %f MeV (%f MeV range)" % (E[i],0.25))
			n = deltaE.GetEntries()
			#c1.SaveAs("%s/Gaussian_fit_%s_%s.png"% (save_dir,medium_save,E[i]))

			sigma = deltaE.GetFunction("gaus").GetParameter(2)
			sigma_err = deltaE.GetFunction("gaus").GetParError(2)
			mean = deltaE.GetFunction("gaus").GetParameter(1)
			mean_err = deltaE.GetFunction("gaus").GetParError(1)
			resolution = deltaE.GetFunction("gaus").GetParameter(2)/E[i]
			resolution_err = resolution * np.sqrt((1/np.sqrt(n))**2 + (sigma_err/sigma)**2)
			sigma_arr.append(sigma)
			sigma_err_arr.append(sigma_err)
			res_arr.append(resolution)
			res_err_arr.append(resolution_err)
			
			#with open("%s/stats_%s.txt" % (save_dir,medium_save),'a') as stats:
			#	stats.write("\nEnergy [MeV] = %f\n" % E[i])
			#	stats.write("Energy range [MeV] = +/- %f\n" % float(0.25/np.sqrt(12)))
			#	stats.write("sigma [MeV] = %f\n" % sigma)
			#	stats.write("sigma error [MeV] = +/- %f\n" % sigma_err)
			#	stats.write("mean [MeV] = %f\n" % mean)
			#	stats.write("mean error [MeV] = +/- %f\n" % mean_err)
			#	stats.write("resolution [\u03C3/E] = %f\n" % resolution)
			#	stats.write("resolution error = +/- %f\n" % resolution_err)
			del c1
		return (fit,fit_err,sigma_arr,sigma_err_arr,res_arr,res_err_arr)	
		
if __name__ == "__main__":
	fitted_energy = Fitted_Energy()
	fitted_energy.parse_options()
	fitted_energy.use_fit()
