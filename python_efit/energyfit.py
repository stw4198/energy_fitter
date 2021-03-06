import argparse
import os
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

###############################################################################################################################################################################################################

class Energy_Fitter():

	def __init__(self, bonsai_fn=None, nwindow = None, interval = None,
		medium=None, fitter=None, savedir=None, load_lib=True, resolution=None, charge=None):
		self.bonsai_fn = bonsai_fn
		self.nwindow = nwindow
		self.interval = interval
		self.medium = medium
		self.fitter = fitter
		self.savedir = savedir
		self.load_lib = load_lib
		self.resolution = resolution
		self.charge = charge

	def parse_options(self, argv=None):
		parser = argparse.ArgumentParser()
		parser.add_argument("bonsai_fn", help="filepath to the bonsai file \
			containing reconstructed events", type=str)
		parser.add_argument("--nwindow", help="the time window for nhits in ns\
			(default: n100)", type=str, default='n100')
		parser.add_argument("--interval", help="energy interval for \
			calculating resolution in MeV \
			(default: 0.25)", type=float, default=0.25)
		parser.add_argument("--medium", help="specify the detection medium \
			(default: none)",
			type=str, choices=['none','water', 'wbls1pct',
					'wbls3pct', 'wbls5pct'],
                            default='none')
		parser.add_argument("--fitter", help="specify which fitter to analyse (N/A): \
					bonsai, qfit or MC \
					(default: bonsai)", type=str, default='bonsai')
		parser.add_argument("--savedir", help="any additional tag to the name of the\
			directory is saved in (default: [blank])", type=str, default='')
		parser.add_argument("--resolution", help="specify resolution testing\
			1 = on, 0 = off (default: 0)", type=int, default=0)
		parser.add_argument("--charge", help="use PMT charge, not nhits, for energy.\
			 1 = on, 0 = off (default: 0)", type=int, default=0)
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
		self.savedir = args.savedir
		self.resolution = args.resolution
		self.charge = args.charge
		self.get_file_data()
		return self.resolution

	def get_file_data(self):
		self.bonsai_t = self.bonsai_file.Get("data")
		self.bonsai_rt = self.bonsai_file.Get("runSummary")
		
	@staticmethod
	def is_valid_file(parser, arg, type="READ"):
		if not os.path.exists(arg):
			parser.error(f"File {arg} does not exist.")
		else:
			return root.TFile(arg, type)

	def medium_detect(self):

		if self.medium == 'none':
			if "wbls" in self.bonsai_fn and "1pc" in self.bonsai_fn and "baseline" in self.bonsai_fn:
				medium = 'WbLS 1% Baseline'
				medium_save = 'wbls_1pc_baseline'
			elif "wbls" in self.bonsai_fn and "1pc" in self.bonsai_fn and "cons" in self.bonsai_fn:
				medium = 'WbLS 1% Conservative'
				medium_save = 'wbls_1pc_cons'
			elif "wbls" in self.bonsai_fn and "1pc" in self.bonsai_fn and not "baseline" in self.bonsai_fn and not "cons" in self.bonsai_fn:
				medium = 'WbLS 1%'
				medium_save = 'wbls_1pc'
			elif "wbls" in self.bonsai_fn and "3pc" in self.bonsai_fn and "baseline" in self.bonsai_fn:
				medium = 'WbLS 3% Baseline'
				medium_save = 'wbls_3pc_baseline'
			elif "wbls" in self.bonsai_fn and "3pc" in self.bonsai_fn and "cons" in self.bonsai_fn:
				medium = 'WbLS 3% Conservative'
				medium_save = 'wbls_3pc_cons'
			elif "wbls" in self.bonsai_fn and "3pc" in self.bonsai_fn and not "baseline" in self.bonsai_fn and not "cons" in self.bonsai_fn:
				medium = 'WbLS 3%'
				medium_save = 'wbls_3pc'
			elif "wbls" in self.bonsai_fn and "5pc" in self.bonsai_fn and "baseline" in self.bonsai_fn:
				medium = 'WbLS 5% Baseline'
				medium_save = 'wbls_5pc_baseline'
			elif "wbls" in self.bonsai_fn and "5pc" in self.bonsai_fn and "cons" in self.bonsai_fn:
				medium = 'WbLS 5% Conservative'
				medium_save = 'wbls_5pc_cons'
			elif "wbls" in self.bonsai_fn and "5pc" in self.bonsai_fn and not "baseline" in self.bonsai_fn and not "cons" in self.bonsai_fn:
				medium = 'WbLS 5%'
				medium_save = 'wbls_5pc'
			elif "8_50_8_10pct" in self.bonsai_fn:
				medium = '8 m x 50 m x 8 m letterbox (10% PC)'
				medium_save = '8_50_8_10pct'
			elif "8_50_8_15pct" in self.bonsai_fn:
				medium = '8 m x 50 m x 8 m letterbox (15% PC)'
				medium_save = '8_50_8_15pct'
			elif "8_50_8_20pct" in self.bonsai_fn:
				medium = '8 m x 50 m x 8 m letterbox (20% PC)'
				medium_save = '8_50_8_20pct'
			elif "8_80_8_10pct" in self.bonsai_fn:
				medium = '8 m x 80 m x 8 m letterbox (10% PC)'
				medium_save = '8_80_8_10pct'
			elif "8_80_8_15pct" in self.bonsai_fn:
				medium = '8 m x 80 m x 8 m letterbox (15% PC)'
				medium_save = '8_80_8_15pct'
			elif "8_80_8_20pct" in self.bonsai_fn:
				medium = '8 m x 80 m x 8 m letterbox (20% PC)'
				medium_save = '8_80_8_20pct'
			elif "10_10_10pct" in self.bonsai_fn:
				medium = '10 m x 10 m cylinder (10% PC)'
				medium_save = '10_10_10pct'
			elif "10_10_15pct" in self.bonsai_fn:
				medium = '10 m x 10 m cylinder (15% PC)'
				medium_save = '10_10_15pct'
			elif "10_10_20pct" in self.bonsai_fn:
				medium = '10 m x 10 m cylinder (20% PC)'
				medium_save = '10_10_20pct'
			elif "12_12_10pct" in self.bonsai_fn:
				medium = '12 m x  12 m cylinder (10% PC)'
				medium_save = '12_12_10pct'
			elif "12_12_15pct" in self.bonsai_fn:
				medium = '12 m x  12 m cylinder (15% PC)'
				medium_save = '12_12_15pct'
			elif "12_12_20pct" in self.bonsai_fn:
				medium = '12 m x  12 m cylinder (20% PC)'
				medium_save = '12_12_20pct'

		else:
			medium,medium_save = self.medium

		return (medium,medium_save)
		
	
	def make_directory(self,medium_save):
				
		if self.savedir == '':
		
			if self.charge == 1:
				if os.path.isdir("../%s_charge" % medium_save):
					print("../%s_charge exists" % medium_save)
				else:
					os.mkdir("../%s_charge" % medium_save)
				save_dir = ("../%s_charge" % medium_save)
			else:
				if os.path.isdir("../%s" % medium_save):
					print("../%s exists" % medium_save)
				else:
					os.mkdir("../%s" % medium_save)
				save_dir = ("../%s" % medium_save)
		else:
			
			if self.charge == 1:
				if os.path.isdir("../%s_charge_%s" % (medium_save,self.savedir)):
					print("../%s_charge_%s exists" % (medium_save,self.savedir))
				else:
					os.mkdir("../%s_charge_%s" % (medium_save,self.savedir))
				save_dir = ("../%s_charge_%s" % (medium_save,self.savedir))
			else:
				if os.path.isdir("../%s_%s" % (medium_save,self.savedir)):
					print("../%s_%s exists" % (medium_save,self.savedir))
				else:
					os.mkdir("../%s_%s" % (medium_save,self.savedir))
				save_dir = ("../%s_%s" % (medium_save,self.savedir))


		return save_dir

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
		
	def make_fit(self, conditions):
		medium,medium_save = self.medium_detect()
		gROOT.SetBatch(True)
		c1 = TCanvas( "c1" , "Fit Production", 200, 10, 700 ,500)
		if self.charge == 1:
			self.bonsai_t.Draw("mc_energy:innerPE>>hist",conditions)
			hist = root.gDirectory.Get("hist")
			hist.Fit("pol1", "Q")
			hist.GetYaxis().SetTitle("E_{True} [MeV]")
			hist.GetXaxis().SetTitle("Photoelectrons")
			hist.SetTitle("Production of fit between E_{True} and photoelectrons")
			save_dir = self.make_directory(medium_save)
			c1.SaveAs("%s/fit_production.png"%save_dir)
			
			p0 = hist.GetFunction("pol1").GetParameter(0)
			p1 = hist.GetFunction("pol1").GetParameter(1)
			p0_err = hist.GetFunction("pol1").GetParError(0)
			p1_err = hist.GetFunction("pol1").GetParError(1)
			fit = (p0, p1)
			fit_err = (p0_err, p1_err)
			print("\np0 = %.5e +/- %.5e\np1 = %.5e +/- %.5e\n" % (fit[0],abs(fit_err[0]),fit[1],abs(fit_err[1])))
			
		else:
			self.bonsai_t.Draw(self.nwindow+":mc_energy>>hist", conditions)
			hist = root.gDirectory.Get("hist")
			hist.Fit("pol2", "Q")
			hist.GetXaxis().SetTitle("E_{True} [MeV]")
			hist.GetYaxis().SetTitle(self.nwindow)
			hist.SetTitle("Production of fit between E_{True} and %s"%self.nwindow)
			save_dir = self.make_directory(medium_save)
			c1.SaveAs("%s/fit_production.png"%save_dir)
			
			#ROOT fit from E to nwindow
			p0_root = hist.GetFunction("pol2").GetParameter(0)
			p1_root = hist.GetFunction("pol2").GetParameter(1)
			p2_root = hist.GetFunction("pol2").GetParameter(2)
			p0_root_err = hist.GetFunction("pol2").GetParError(0)
			p1_root_err = hist.GetFunction("pol2").GetParError(1)
			p2_root_err = hist.GetFunction("pol2").GetParError(2)

			mc_energy,Emax,E,E_cut = self.energy_values(self.interval)

			#optimal fit from nwindow to E
			n100_fit = p2_root*E**2 + p1_root*E + p0_root
			new_fit, new_error_matrix = np.polyfit(n100_fit,E,2,cov=True) #Find errors here
			p0 = new_fit[2]
			p1 = new_fit[1]
			p2 = new_fit[0]
			fit = (p0, p1, p2)
			new_error = np.sqrt(np.diag(new_error_matrix))
			p0_err = new_error[2]
			p1_err = new_error[1]
			p2_err = new_error[0]

			#upperbound fit from nwindow to E
			n100_2 = (p2_root - p2_root_err)*E**2 + (p1_root-p1_root_err)*E + (p0_root-p0_root_err)
			new_fit_2,new_error_matrix_2 = np.polyfit(n100_2,E,2,cov=True)
			p0_2 = new_fit_2[2]
			p1_2 = new_fit_2[1]
			p2_2 = new_fit_2[0]
			new_error_2 = np.sqrt(np.diag(new_error_matrix_2))
			p0_err_2 = new_error_2[2]
			p1_err_2 = new_error_2[1]
			p2_err_2 = new_error_2[0]

			#lowerbound fit from nwindow to E
			n100_3 = (p2_root + p2_root_err)*E**2 + (p1_root+p1_root_err)*E + (p0_root+p0_root_err)
			new_fit_3,new_error_matrix_3 = np.polyfit(n100_3,E,2,cov=True)
			p0_3 = new_fit_3[2]
			p1_3 = new_fit_3[1]
			p2_3 = new_fit_3[0]
			new_error_3 = np.sqrt(np.diag(new_error_matrix_3))
			p0_err_3 = new_error_3[2]
			p1_err_3 = new_error_3[1]
			p2_err_3 = new_error_3[0]
			
			fit_err = (abs(p0*p0_root_err/p0_root),abs(p1*p1_root_err/p1_root),abs(p2*p2_root_err/p2_root))

			print("\np0 = %.5e +/- %.5e\np1 = %.5e +/- %.5e\np2 = %.5e +/- %.5e\n" % (fit[0],abs(fit_err[0]),fit[1],abs(fit_err[1]),fit[2],abs(fit_err[2])))

		del c1

		return (fit,fit_err)
		
	def call_fit(self):
		medium,medium_save = self.medium_detect()
		if "wbls" in medium_save:
			conditions = "innerPE > 0.25 && closestPMT > 0 && %s > 0" % self.nwindow
		elif "wbls" not in medium_save:
			conditions = "innerPE > 0.25 && -3000 < x < 3000 && -3000 < z < 3000 && %s > 0" % self.nwindow
		save_dir = self.make_directory(medium_save)
		conditions = "innerPE > 0.25 && closestPMT > 0 && %s > 0" % self.nwindow
		fit,fit_err = self.make_fit(conditions)
		
		with open("%s/stats_%s.txt" % (save_dir,medium_save),'w') as stats:
			stats.write("Medium = %s\n" % medium)
			stats.write("p0 = %.5e\n" % fit[0])
			stats.write("p0 error = %.5e\n" % fit_err[0])
			stats.write("p1 = %.5e\n" % fit[1])
			stats.write("p1 error = %.5e\n" % fit_err[1])
			if self.charge == 0:
				stats.write("p2 = %.5e\n" % fit[2])
				stats.write("p2 error = %.5e\n" % fit_err[2])
			elif self.charge == 1:
				stats.write("p2 = 0\n")
				stats.write("p2 error = 0\n")

	def resolution_testing(self):
		medium,medium_save = self.medium_detect()
		if "wbls" in medium_save:
			conditions = "closestPMT > 0 && innerPE > 0.25 && %s > 0" % self.nwindow
		elif "wbls" not in medium_save:
			conditions = "innerPE > 0.25 && -3000 < x < 3000 && -3000 < z < 3000 && %s > 0" % self.nwindow
		fit,fit_err = self.make_fit(conditions)
		mc_energy,Emax,E,E_cut = self.energy_values(self.interval)
		save_dir = self.make_directory(medium_save)
		try:
			os.remove("%s/stats_%s.txt" % (save_dir,medium_save))
		except:
			print("%s/stats_%s.txt not found" % (save_dir,medium_save))
		if self.charge == 1:
			graph = ("(%f*innerPE) + %f - mc_energy>>deltaE" % (fit[1],fit[0]))
			gROOT.SetBatch(True)
			c_all = TCanvas( "c_all" , "Delta E "+medium, 200, 10, 700 ,500)
			self.bonsai_t.Draw(graph,conditions)
			deltaE = root.gDirectory.Get("deltaE")
			deltaE.Fit("gaus","Q")
			gStyle.SetOptFit(11)
			deltaE.SetTitle("#DeltaE %s" % medium)
			deltaE.GetXaxis().SetTitle("#DeltaE [MeV]")
			deltaE.GetXaxis().SetRangeUser(-.4*E[-1],.4*Emax[-1])
			c_all.SaveAs("%s/Gaussian_fit_%s.png"%(save_dir,medium_save))
		else:
			graph = ("(%s*%s*%f) + (%s*%f) + %f - mc_energy>>deltaE" % (self.nwindow,self.nwindow,fit[2],self.nwindow,fit[1],fit[0]))
			gROOT.SetBatch(True)
			c_all = TCanvas( "c_all" , "Delta E "+medium, 200, 10, 700 ,500)
			self.bonsai_t.Draw(graph,conditions)
			deltaE = root.gDirectory.Get("deltaE")
			deltaE.Fit("gaus","Q")
			gStyle.SetOptFit(11)
			deltaE.SetTitle("#DeltaE %s" % medium)
			deltaE.GetXaxis().SetTitle("#DeltaE [MeV]")
			deltaE.GetXaxis().SetRangeUser(-.4*E[-1],.4*Emax[-1])
			c_all.SaveAs("%s/Gaussian_fit_%s.png"%(save_dir,medium_save))

		del c_all
		del deltaE

		E = E[1:]

		with open("%s/stats_%s.txt" % (save_dir,medium_save),'a') as stats:
			stats.write("Medium = %s\n" % medium)
			stats.write("p0 = %.5e\n" % fit[0])
			stats.write("p0 error = %.5e\n" % fit_err[0])
			stats.write("p1 = %.5e\n" % fit[1])
			stats.write("p1 error = %.5e\n" % fit_err[1])
			if self.charge == 0:
				stats.write("p2 = %.5e\n" % fit[2])
				stats.write("p2 error = %.5e\n" % fit_err[2])
			elif self.charge == 1:
				stats.write("p2 = 0\n")
				stats.write("p2 error = 0\n")

		for i in tqdm(range(len(E_cut)),desc="Applying fit to all energies"):
			c1 = TCanvas("c1" , "Delta E "+medium, 200, 10, 700 ,500)
			condition = "%s && %s" %(conditions,E_cut[i])
			self.bonsai_t.Draw(graph,condition)
			deltaE = root.gDirectory.Get("deltaE")
			deltaE.Fit("gaus","Q")
			gStyle.SetOptFit(11)
			deltaE.SetTitle("E_{centre} = %f MeV (%f MeV range) %s" % (E[i],self.interval,medium))
			n = deltaE.GetEntries()
			c1.SaveAs("%s/Gaussian_fit_%s_%s.png"% (save_dir,medium_save,E[i]))

			sigma = deltaE.GetFunction("gaus").GetParameter(2)
			sigma_err = deltaE.GetFunction("gaus").GetParError(2)
			mean = deltaE.GetFunction("gaus").GetParameter(1)
			mean_err = deltaE.GetFunction("gaus").GetParError(1)
			resolution = deltaE.GetFunction("gaus").GetParameter(2)/E[i]
			resolution_err = resolution * np.sqrt((1/np.sqrt(n))**2 + (sigma_err/sigma)**2)
			
			with open("%s/stats_%s.txt" % (save_dir,medium_save),'a') as stats:
				stats.write("\nEnergy [MeV] = %f\n" % E[i])
				stats.write("Energy range [MeV] = +/- %f\n" % float(self.interval/np.sqrt(12)))
				stats.write("sigma [MeV] = %f\n" % sigma)
				stats.write("sigma error [MeV] = +/- %f\n" % sigma_err)
				stats.write("mean [MeV] = %f\n" % mean)
				stats.write("mean error [MeV] = +/- %f\n" % mean_err)
				stats.write("resolution [\u03C3/E] = %f\n" % resolution)
				stats.write("resolution error = +/- %f\n" % resolution_err)
			del c1

	def write_to_tree(self, values, br_name):
		# write values to bonsai tree under branch br_name
		vals_to_write = np.empty((1), dtype="double")
		branch = self.bonsai_t.Branch(br_name, vals_to_write, br_name+"/D")
		for value in values:
			vals_to_write[0] = value
			branch.Fill()
		self.bonsai_file.Write("", root.TFile.kOverwrite)
		
###############################################################################################################################################################################################################

if __name__ == "__main__":
	energy_fitter = Energy_Fitter()
	resolution = energy_fitter.parse_options()
	if resolution == 1:
		energy_fitter.resolution_testing()
	else:
		energy_fitter.call_fit()
	
