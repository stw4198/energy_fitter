import argparse
import os
import pdb
import sys
from tqdm import tqdm
import numpy as np
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

class Energy_Fitter():

	def __init__(self, bonsai_fn=None, nwindow = None, interval = None,
		medium=None, fitter=None, load_lib=True):
		self.bonsai_fn = bonsai_fn
		self.nwindow = nwindow
		self.interval = interval
		self.medium = medium
		self.fitter = fitter
		self.load_lib = load_lib

	def parse_options(self, argv=None):
		parser = argparse.ArgumentParser()
		parser.add_argument("bonsai_fn", help="filepath to the bonsai file \
			containing reconstructed events", type=str)
		parser.add_argument("--nwindow", help="the time window for nhits in ns\
			(default: n100)", type=str, default='n100')
		parser.add_argument("--interval", help="energy interval for \
			calculating resolution in MeV \
			(default: 0.5)", type=float, default=0.5)
		parser.add_argument("--medium", help="specify the detection medium \
			(default: none)",
			type=str, choices=['none','water', 'wbls1pct',
					'wbls3pct', 'wbls5pct'],
                            default='none')
		parser.add_argument("--fitter", help="specify which fitter to analyse (N/A): \
					bonsai, qfit or MC \
					(default: bonsai)", type=str, default='bonsai')
		args = parser.parse_args(argv)
		if self.load_lib:
			root.gSystem.Load('libRATEvent.so')
			print("ROOT: Loaded libRATEvent.so")
		self.bonsai_fn = args.bonsai_fn
		self.bonsai_file = self.is_valid_file(parser, self.bonsai_fn, type="UPDATE")
		self.nwindow = args.nwindow
		self.interval = args.interval
		self.medium = args.medium
		self.fitter = args.fitter
		self.get_file_data()

	def get_file_data(self):
		self.bonsai_t = self.bonsai_file.Get("data")
		self.bonsai_rt = self.bonsai_file.Get("runSummary")

	def medium_detect(self):

		if self.medium == 'none':
			if "wbls" in self.bonsai_fn and "1pc" in self.bonsai_fn and "baseline" in self.bonsai_fn:
				medium = 'WbLS 1% Baseline'
				medium_save = 'wbls_1pc_baseline'
			elif "wbls" in self.bonsai_fn and "1pc" in self.bonsai_fn and "cons" in self.bonsai_fn:
				medium = 'WbLS 1% Conservative'
				medium_save = 'wbls_1pc_cons'
			elif "wbls" in self.bonsai_fn and "3pc" in self.bonsai_fn and "baseline" in self.bonsai_fn:
				medium = 'WbLS 3% Baseline'
				medium_save = 'wbls_3pc_baseline'
			elif "wbls" in self.bonsai_fn and "3pc" in self.bonsai_fn and "cons" in self.bonsai_fn:
				medium = 'WbLS 3% Conservative'
				medium_save = 'wbls_3pc_cons'
			elif "wbls" in self.bonsai_fn and "5pc" in self.bonsai_fn and "baseline" in self.bonsai_fn:
				medium = 'WbLS 5% Baseline'
				medium_save = 'wbls_5pc_baseline'
			elif "wbls" in self.bonsai_fn and "5pc" in self.bonsai_fn and "cons" in self.bonsai_fn:
				medium = 'WbLS 5% Conservative'
				medium_save = 'wbls_5pc_cons'


		else:
			medium,medium_save = self.medium

		return (medium,medium_save)


#Calculations here inc. loop

	def nX_extraction(self):
		b_nentry = self.bonsai_t.GetEntries()
		nX_values = []
		print(f"There are {b_nentry} reconstructed events in {self.bonsai_fn}")

		nwin = self.nwindow
		print("nwin = ", nwin)

		for b_entry, b_event in enumerate(tqdm(self.bonsai_t, total=b_nentry)):
			nX_extract = b_event.n100 #Calling this nX sets it to literal nX branch
			nX_values.append(nX_extract)
		#print(nX_values[10],nX_values[-5],nX_values[-7])
		return(nX_values)

	def resolution_testing(self):
		medium,medium_save = self.medium_detect()
		conditions = "closestPMT > 0 && %s > 0" % self.nwindow
		fit = self.make_fit(self.nwindow,conditions)
		mc_energy,Emax,E,E_cut = self.energy_values(self.interval)
		save_dir = self.make_directory(medium_save)
		try:
			os.remove("%s/stats_%s.txt" % (save_dir,medium_save))
		except:
			print("%s/stats_%s.txt not found" % (save_dir,medium_save))

		#c_all = TCanvas( "c_all" , "Delta E "+medium, 200, 10, 700 ,500)
		graph = ("(%s*%s*%f) + (%s*%f) + %f - mc_energy>>deltaE" % (self.nwindow,self.nwindow,fit[2],self.nwindow,fit[1],fit[0]))
		gROOT.SetBatch(True)
		c_all = TCanvas( "c_all" , "Delta E "+medium, 200, 10, 700 ,500)
		self.bonsai_t.Draw(graph,conditions)
		deltaE = root.gDirectory.Get("deltaE")
		deltaE.Fit("gaus")
		gStyle.SetOptFit(11)
		deltaE.SetTitle("#DeltaE %s" % medium)
		deltaE.GetXaxis().SetTitle("#DeltaE [MeV]")
		deltaE.GetXaxis().SetRangeUser(-.4*E[-1],.4*Emax[-1])
		c_all.SaveAs("%s/Gaussian_fit_%s.png"%(save_dir,medium_save))

		del c_all
		del deltaE

		c1 = TCanvas( "c1" , "Delta E "+medium, 200, 10, 700 ,500)
		E = E[1:]

		with open("%s/stats_%s.txt" % (save_dir,medium_save),'a') as stats:
			stats.write("Medium = %s\n" % medium)
			stats.write("p0 = %.5e\n" % fit[0])
			stats.write("p1 = %.5e\n" % fit[1])
			stats.write("p2 = %.5e\n" % fit[2])
		for i in tqdm(range(len(E_cut)),desc="Applying fit to all energies"):
			c1 = TCanvas("c1" , "Delta E "+medium, 200, 10, 700 ,500)
			condition = "%s && %s" %(conditions,E_cut[i])
			print(condition)
			self.bonsai_t.Draw(graph,condition)
			deltaE = root.gDirectory.Get("deltaE")
			deltaE.Fit("gaus")
			gStyle.SetOptFit(11)
			deltaE.SetTitle("E_{centre} = %f MeV (%f MeV interval) %s" % (E[i],self.interval,medium))
			c1.SaveAs("%s/Gaussian_fit_%s_%s.png"% (save_dir,medium_save,E[i]))
			with open("%s/stats_%s.txt" % (save_dir,medium_save),'a') as stats:
				stats.write("\nEnergy [MeV] = %f\n" % E[i])
				stats.write("Energy range [MeV] = +/- %f\n" % float(0.5*self.interval))
				stats.write("sigma [MeV] = %s\n" % str(deltaE.GetFunction("gaus").GetParameter(2)))
				stats.write("mean [MeV] = %s\n" % str(deltaE.GetFunction("gaus").GetParameter(1)))
				stats.write("resolution [\u03C3/E] = %s\n" % str(deltaE.GetFunction("gaus").GetParameter(2)/E[i]))
			del c1


	@staticmethod
	def is_valid_file(parser, arg, type="READ"):
		if not os.path.exists(arg):
			parser.error(f"File {arg} does not exist.")
		else:
			return root.TFile(arg, type)

	def make_directory(self,medium_save):
		
		if os.path.isdir("../%s_%f" % (medium_save,self.interval)):
			print("../%s_%f exists" % (medium_save,self.interval))
		else:
			os.mkdir("../%s_%f" % (medium_save,self.interval))
		save_dir = "../%s_%f" % (medium_save,self.interval)
		return save_dir

	def read_from_tree(self, br_name):
		# Read values of branch br_name from bonsai tree into np array
		values = self.bonsai_t.AsMatrix(columns=[br_name])
		return values

	def make_fit(self, estimator, conditions):
		medium,medium_save = self.medium_detect()
		gROOT.SetBatch(True)
		c1 = TCanvas( "c1" , "Fit Production", 200, 10, 700 ,500)
		self.bonsai_t.Draw(estimator+":mc_energy>>hist", conditions, "goff")
		hist = root.gDirectory.Get("hist")
		hist.Fit("pol2", "goff")
		hist.GetXaxis().SetTitle("E_{True} [MeV]")
		hist.GetYaxis().SetTitle(self.nwindow)
		hist.SetTitle("Production of fit between E_{True} and %s"%self.nwindow)
		save_dir = self.make_directory(medium_save)
		c1.SaveAs("%s/fit_production.png"%save_dir)
		p0_root = hist.GetFunction("pol2").GetParameter(0)
		p1_root = hist.GetFunction("pol2").GetParameter(1)
		p2_root = hist.GetFunction("pol2").GetParameter(2)
		p0_root_err = hist.GetFunction("pol2").GetParError(0)
		p1_root_err = hist.GetFunction("pol2").GetParError(1)
		p2_root_err = hist.GetFunction("pol2").GetParError(2)

		mc_energy,Emax,E,E_cut = self.energy_values(self.interval)
		n100_fit = p2_root*E**2 + p1_root*E + p0_root
		new_fit, new_residuals, _, _, _ = np.polyfit(n100_fit,E,2,full=True) #Find errors here
		p0 = new_fit[2]
		p1 = new_fit[1]
		p2 = new_fit[0]
		fit = (p0, p1, p2)
		return (fit)

	def energy_values(self,interval):
		mc_energy = self.read_from_tree("mc_energy")
		Emax = max(mc_energy)
		E = np.arange(0,Emax+interval,interval)
		E_cut = []
		for i in range(len(E)):
			E_cut.append("mc_energy > %f && mc_energy < %f" % (E[i]-0.5*interval,E[i]+0.5*interval))
		return(mc_energy,Emax,E,E_cut[1:])

	def write_to_tree(self, values, br_name):
		# write values to bonsai tree under branch br_name
		vals_to_write = np.empty((1), dtype="double")
		branch = self.bonsai_t.Branch(br_name, vals_to_write, br_name+"/D")
		for value in values:
			vals_to_write[0] = value
			branch.Fill()
		self.bonsai_file.Write("", root.TFile.kOverwrite)
		
	
	@staticmethod
	def estimate_energy(estimator,fit):
		#estimator should be a value or array of values
		estimate = fit[0] + fit[1]*estimator + fit[2]*estimator
		if isinstance(estimate, np.ndarray):
			estimate[estimate<0] = -9999.9
		return estimate


def fastmag(vector):
	# Faster magnitude calculation than linalg.norm or elementwise operation
	return np.sqrt(vector.dot(vector))

if __name__ == "__main__":
	energy_fitter = Energy_Fitter()
	energy_fitter.parse_options()
	energy_fitter.resolution_testing()

