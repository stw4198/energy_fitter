import matplotlib.pyplot as plt
import numpy as np
import re

def value_extraction_nhits(media):

	stats = open("../%s_0.500000/stats_%s.txt" % (media,media), 'r')
	stats_lines = stats.readlines()

	RES = stats_lines[14::9]
	resolution = []
	for i in range(len(RES)):
		temp = re.findall(r"[-+]?\d*\.\d+|\d+", RES[i])
		resolution.append(float(temp[0]))

	RES_err = stats_lines[15::9]
	resolution_err = []
	for i in range(len(RES_err)):
		temp = re.findall(r"[-+]?\d*\.\d+|\d+", RES_err[i])
		resolution_err.append(float(temp[0]))#+.15*resolution[i])


	en = stats_lines[8::9]
	energy = []
	for i in range(len(en)):
		temp = re.findall(r"[-+]?\d*\.\d+|\d+", en[i]) 
		energy.append(float(temp[0]))


	en_err = stats_lines[9::9]
	energy_err = []
	for i in range(len(en_err)):
		temp = re.findall(r"[-+]?\d*\.\d+|\d+", en_err[i]) 
		energy_err.append(float(temp[0]))


	MEAN = stats_lines[12::9]
	mean = []
	for i in range(len(MEAN)):
		temp = re.findall(r"[-+]?\d*\.\d+|\d+", MEAN[i]) 
		mean.append(float(temp[0]))


	MEAN_err = stats_lines[13::9]
	mean_err = []
	for i in range(len(MEAN_err)):
		temp = re.findall(r"[-+]?\d*\.\d+|\d+", MEAN_err[i]) 
		mean_err.append(float(temp[0]))


	SIGMA = stats_lines[10::9]
	sigma = []
	for i in range(len(SIGMA)):
		temp = re.findall(r"[-+]?\d*\.\d+|\d+", SIGMA[i]) 
		sigma.append(float(temp[0]))

	SIGMA_err = stats_lines[11::9]
	sigma_err = []
	for i in range(len(SIGMA_err)):
		temp = re.findall(r"[-+]?\d*\.\d+|\d+", SIGMA_err[i]) 
		sigma_err.append(float(temp[0]))



	return(resolution,resolution_err,en,en_err)

resolution_1,resolution_err_1,energy_1,energy_err_1 = value_extraction_nhits("wbls_1pc_baseline")
resolution_3,resolution_err_3,energy_3,energy_err_3 = value_extraction_nhits("wbls_3pc_baseline")
resolution_5,resolution_err_5,energy_5,energy_err_5 = value_extraction_nhits("wbls_5pc_baseline")
energy = np.arange(0.5,10.5,0.5)
energy_err = 0.25

plt.errorbar(energy,resolution_1,yerr=resolution_err_1,xerr=energy_err,linestyle='none',label="WbLS 1% Baseline")
plt.errorbar(energy,resolution_3,yerr=resolution_err_3,xerr=energy_err,linestyle='none',label="WbLS 3% Baseline")
plt.errorbar(energy,resolution_5,yerr=resolution_err_5,xerr=energy_err,linestyle='none',label="WbLS 5% Baseline")
plt.xlim(energy[1]-0.25,energy[-1]+0.25)
plt.xlabel("Energy [MeV]")
plt.ylabel("Resolution [\u03C3/E]")
plt.title("Electrons in Baseline WATCHMAN Detector")
plt.legend()
plt.savefig("../electron_resolution_baseline.pdf")
plt.show()

