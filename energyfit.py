import argparse
import os
import pdb
import sys
from tqdm import tqdm
import numpy as np
try:
	import ROOT as root
except ImportError:
	print("Could not import ROOT. Source thisroot.sh first.")
	exit(1)

np.set_printoptions(suppress=True)

class Energy_Fitter():

	def __init__(self, bonsai_fn=None, nwindow = None,
		medium=None, fitter=None, load_lib=True):
		self.bonsai_fn = bonsai_fn
		self.nwindow = nwindow
		self.medium = medium
		self.fitter = fitter
		self.load_lib = load_lib

	def parse_options(self, argv=None):
		parser = argparse.ArgumentParser()
		parser.add_argument("bonsai_fn", help="filepath to the bonsai file \
			containing reconstructed events", type=str)
		parser.add_argument("--nwindow", help="the time window for nhits \
			relative to current PMT hit time in ns, typically \
			a negative number or zero \
			(default: n100)", type=str, default='n100')
		parser.add_argument("--medium", help="specify the detection medium \
			(default: water)",
			type=str, choices=['water', 'wbls1pct',
					'wbls3pct', 'wbls5pct'],
                            default='water')
		parser.add_argument("--fitter", help="specify which fitter to analyse: \
					bonsai, qfit or MC \
					(default: bonsai)", type=str, default='bonsai')
		args = parser.parse_args(argv)
		if self.load_lib:
			root.gSystem.Load('libRATEvent.so')
			print("ROOT: Loaded libRATEvent.so")
		self.bonsai_fn = args.bonsai_fn
		self.bonsai_file = self.is_valid_file(parser, self.bonsai_fn, type="UPDATE")
		self.nwindow = args.nwindow
		self.medium = args.medium
		self.fitter = args.fitter
		self.get_file_data()

	def get_file_data(self):
		self.bonsai_t = self.bonsai_file.Get("data")
		self.bonsai_rt = self.bonsai_file.Get("runSummary")


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

	def fit_application(self):
		b_nentry = self.bonsai_t.GetEntries()
		conditions = "closestPMT > 0 && %s > 0" % self.nwindow
		fit,Emax,E = self.make_fit(self.nwindow,conditions)
		E_pos = E[1:]
		graph = ("(%s*%s*%f) + (%s*%f) + %f - mc_energy>>fitted_hist" % (self.nwindow,self.nwindow,fit[2],self.nwindow,fit[1],fit[0]))
		for i in range(len(E_pos)):
			#print("E_entry = ", E_entry, "E_event = ", E_event)
			discrete_conditions = "closestPMT > 0 && "+self.nwindow+" > 0 && mc_energy == "+str(E[i+1])
			self.bonsai_t.Draw(graph,discrete_conditions)
			fitted_hist = root.gDirectory.Get("fitted_hist")
			fitted_hist.Fit("gaus")
			fitted_hist.SaveAs("Fitted_hist_%i.C"%i)
			print(graph,discrete_conditions)
			with open("stats.txt",'a') as stats:
				stats.write("\nEnergy = %f\n" % E_pos[i])
				stats.write("sigma = %s\n" % str(fitted_hist.GetFunction("gaus").GetParameter(2)))
				stats.write("mean = %s\n" % str(fitted_hist.GetFunction("gaus").GetParameter(1)))


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

	def make_fit(self, estimator, conditions):
		self.bonsai_t.Draw(estimator+":mc_energy>>hist", conditions, "goff")
		hist = root.gDirectory.Get("hist")
		hist.Fit("pol2", "goff")
		hist.SaveAs("fit_hist.root")
		p0_root = hist.GetFunction("pol2").GetParameter(0)
		p1_root = hist.GetFunction("pol2").GetParameter(1)
		p2_root = hist.GetFunction("pol2").GetParameter(2)
		p0_root_err = hist.GetFunction("pol2").GetParError(0)
		p1_root_err = hist.GetFunction("pol2").GetParError(1)
		p2_root_err = hist.GetFunction("pol2").GetParError(2)

		mc_energy = self.read_from_tree("mc_energy")
		Emax = max(mc_energy)
		E = np.arange(0,Emax+0.5,0.5)
		n100_fit = p2_root*E**2 + p1_root*E + p0_root
		new_fit, new_residuals, _, _, _ = np.polyfit(n100_fit,E,2,full=True) #Find errors here
		p0 = new_fit[2]
		p1 = new_fit[1]
		p2 = new_fit[0]
		fit = (p0, p1, p2)
		return (fit, Emax, E)
	
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
	#energy_fitter.nX_extraction()
	energy_fitter.fit_application()

