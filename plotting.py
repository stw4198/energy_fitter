import matplotlib.pyplot as plt
import numpy as np
import re
from numpy.polynomial.polynomial import polyfit

Tol_bright = ['#4477AA','#66CCEE','#228833',
                     '#CCBB44','#EE6677','#AA3377','#BBBBBB','k']
                     
CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a', 
                  '#f781bf', '#a65628', '#984ea3', 
                  '#999999', '#e41a1c', '#dede00']

def value_extraction(media,interval,tags):

	stats = open("../%s_%f%s/stats_%s.txt" % (media,interval,tags,media), 'r')
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

interval = 0.25
medium_type = ''
pos = 'letterbox'

if pos == 'off':

	resolution_1,resolution_err_1,energy_1,energy_err_1 = value_extraction("wbls_1pc_baseline",interval,'')
	resolution_3,resolution_err_3,energy_3,energy_err_3 = value_extraction("wbls_3pc_baseline",interval,'')
	resolution_5,resolution_err_5,energy_5,energy_err_5 = value_extraction("wbls_5pc_baseline",interval,'')

elif pos == 'on':

	resolution_1_0,resolution_err_1_0,energy_1_0,energy_err_1_0 = value_extraction("wbls_1pc",interval,'_centre')
	resolution_1_1000,resolution_err_1_1000,energy_1_1000,energy_err_1_1000 = value_extraction("wbls_1pc",interval,'_1000')
	resolution_1_2000,resolution_err_1_2000,energy_1_2000,energy_err_1_2000 = value_extraction("wbls_1pc",interval,'_2000')
	resolution_1_3000,resolution_err_1_3000,energy_1_3000,energy_err_1_3000 = value_extraction("wbls_1pc",interval,'_3000')
	resolution_1_4000,resolution_err_1_4000,energy_1_4000,energy_err_1_4000 = value_extraction("wbls_1pc",interval,'_4000')
	resolution_1_5000,resolution_err_1_5000,energy_1_5000,energy_err_1_5000 = value_extraction("wbls_1pc",interval,'_5000')
	resolution_1_6000,resolution_err_1_6000,energy_1_6000,energy_err_1_6000 = value_extraction("wbls_1pc",interval,'_6000')

	resolution_3_0,resolution_err_3_0,energy_3_0,energy_err_3_0 = value_extraction("wbls_3pc",interval,'_centre')
	resolution_3_1000,resolution_err_3_1000,energy_3_1000,energy_err_3_1000 = value_extraction("wbls_3pc",interval,'_1000')
	resolution_3_2000,resolution_err_3_2000,energy_3_2000,energy_err_3_2000 = value_extraction("wbls_3pc",interval,'_2000')
	resolution_3_3000,resolution_err_3_3000,energy_3_3000,energy_err_3_3000 = value_extraction("wbls_3pc",interval,'_3000')
	resolution_3_4000,resolution_err_3_4000,energy_3_4000,energy_err_3_4000 = value_extraction("wbls_3pc",interval,'_4000')
	resolution_3_5000,resolution_err_3_5000,energy_3_5000,energy_err_3_5000 = value_extraction("wbls_3pc",interval,'_5000')
	resolution_3_6000,resolution_err_3_6000,energy_3_6000,energy_err_3_6000 = value_extraction("wbls_3pc",interval,'_6000')

	resolution_5_0,resolution_err_5_0,energy_5_0,energy_err_5_0 = value_extraction("wbls_5pc",interval,'_centre')
	resolution_5_1000,resolution_err_5_1000,energy_5_1000,energy_err_5_1000 = value_extraction("wbls_5pc",interval,'_1000')
	resolution_5_2000,resolution_err_5_2000,energy_5_2000,energy_err_5_2000 = value_extraction("wbls_5pc",interval,'_2000')
	resolution_5_3000,resolution_err_5_3000,energy_5_3000,energy_err_5_3000 = value_extraction("wbls_5pc",interval,'_3000')
	resolution_5_4000,resolution_err_5_4000,energy_5_4000,energy_err_5_4000 = value_extraction("wbls_5pc",interval,'_4000')
	resolution_5_5000,resolution_err_5_5000,energy_5_5000,energy_err_5_5000 = value_extraction("wbls_5pc",interval,'_5000')
	resolution_5_6000,resolution_err_5_6000,energy_5_6000,energy_err_5_6000 = value_extraction("wbls_5pc",interval,'_6000')
	
elif pos == 'centre':

	resolution_1_0,resolution_err_1_0,energy_1_0,energy_err_1_0 = value_extraction("wbls_1pc",interval,'_centre')
	resolution_3_0,resolution_err_3_0,energy_3_0,energy_err_3_0 = value_extraction("wbls_3pc",interval,'_centre')
	resolution_5_0,resolution_err_5_0,energy_5_0,energy_err_5_0 = value_extraction("wbls_5pc",interval,'_centre')
	
else:

	print('\nNo position-based energy reconstruction\n')	

energy = np.arange(interval,10.+interval,interval)
energy_err = interval/np.sqrt(12)

if pos == 'off':

	plt.errorbar(energy,resolution_1,yerr=resolution_err_1,xerr=energy_err,linestyle='none',color=Tol_bright[0],label="WbLS 1% Baseline")
	plt.errorbar(energy,resolution_3,yerr=resolution_err_3,xerr=energy_err,linestyle='none',color=Tol_bright[3],label="WbLS 3% Baseline")
	plt.errorbar(energy,resolution_5,yerr=resolution_err_5,xerr=energy_err,linestyle='none',color=Tol_bright[7],label="WbLS 5% Baseline")
	plt.xlabel("Kinetic Energy [MeV]")
	plt.ylabel("Resolution [\u03C3/E]")
	plt.title("Electrons in Baseline WATCHMAN Detector")
	plt.legend()
	plt.grid()
	plt.savefig("../electron_resolution_baseline_%f.pdf"%interval)
	plt.show()

	plt.errorbar(energy,resolution_1,yerr=resolution_err_1,xerr=energy_err,linestyle='none',color=Tol_bright[0],label="WbLS 1% Baseline")
	plt.errorbar(energy,resolution_3,yerr=resolution_err_3,xerr=energy_err,linestyle='none',color=Tol_bright[3],label="WbLS 3% Baseline")
	plt.errorbar(energy,resolution_5,yerr=resolution_err_5,xerr=energy_err,linestyle='none',color=Tol_bright[7],label="WbLS 5% Baseline")
	plt.xlim(energy[2]-0.125,energy[-1]+0.125)
	plt.ylim(0,resolution_1[2]+resolution_err_1[2]+0.05)
	plt.xlabel("Kinetic Energy [MeV]")
	plt.ylabel("Resolution [\u03C3/E]")
	plt.title("Electrons in Baseline WATCHMAN Detector")
	plt.legend()
	plt.grid()
	plt.savefig("../electron_resolution_baseline_zoomed_%f.pdf"%interval)
	plt.show()

	plt.errorbar(energy,resolution_1,yerr=resolution_err_1,xerr=energy_err,linestyle='none',color=Tol_bright[0],label="WbLS 1% Baseline")
	plt.errorbar(energy,resolution_3,yerr=resolution_err_3,xerr=energy_err,linestyle='none',color=Tol_bright[3],label="WbLS 3% Baseline")
	plt.errorbar(energy,resolution_5,yerr=resolution_err_5,xerr=energy_err,linestyle='none',color=Tol_bright[7],label="WbLS 5% Baseline")
	plt.xlim(0.5,4.5)
	plt.ylim(0.0,0.35)
	plt.xlabel("Kinetic Energy [MeV]")
	plt.ylabel("Resolution [\u03C3/E]")
	plt.title("Electrons in Baseline WATCHMAN Detector")
	plt.legend()
	plt.grid()
	plt.savefig("../electron_resolution_baseline_lowE_%f.pdf"%interval)
	plt.show()

elif pos == 'on':

	plt.errorbar(energy,resolution_1_0,yerr=resolution_err_1_0,xerr=energy_err,linestyle='none',label="0 mm")
	#plt.errorbar(energy,resolution_1_1000,yerr=resolution_err_1_1000,xerr=energy_err,linestyle='none',label="1000 mm")
	plt.errorbar(energy,resolution_1_2000,yerr=resolution_err_1_2000,xerr=energy_err,linestyle='none',label="2000 mm")
	#plt.errorbar(energy,resolution_1_3000,yerr=resolution_err_1_3000,xerr=energy_err,linestyle='none',label="3000 mm")
	plt.errorbar(energy,resolution_1_4000,yerr=resolution_err_1_4000,xerr=energy_err,linestyle='none',label="4000 mm")
	#plt.errorbar(energy,resolution_1_5000,yerr=resolution_err_1_5000,xerr=energy_err,linestyle='none',label="5000 mm")
	plt.errorbar(energy,resolution_1_6000,yerr=resolution_err_1_6000,xerr=energy_err,linestyle='none',label="6000 mm")
	plt.xlim(energy[2]-0.25,energy[-1]+0.25)
	plt.ylim(0,resolution_1_1000[2]+resolution_err_1_1000[2]+0.05)
	plt.xlabel("Kinetic Energy [MeV]")
	plt.ylabel("Resolution [\u03C3/E]")
	plt.title("Electrons in Baseline WATCHMAN Detector WbLS 1%")
	plt.legend()
	plt.grid()
	plt.savefig("../electrons_resolution_wbls_1pc_position_%f.pdf" % interval)
	plt.show()

	plt.errorbar(energy,resolution_3_0,yerr=resolution_err_3_0,xerr=energy_err,linestyle='none',label="0 mm")
	#plt.errorbar(energy,resolution_3_1000,yerr=resolution_err_3_1000,xerr=energy_err,linestyle='none',label="1000 mm")
	plt.errorbar(energy,resolution_3_2000,yerr=resolution_err_3_2000,xerr=energy_err,linestyle='none',label="2000 mm")
	#plt.errorbar(energy,resolution_3_3000,yerr=resolution_err_3_3000,xerr=energy_err,linestyle='none',label="3000 mm")
	plt.errorbar(energy,resolution_3_4000,yerr=resolution_err_3_4000,xerr=energy_err,linestyle='none',label="4000 mm")
	#plt.errorbar(energy,resolution_3_5000,yerr=resolution_err_3_5000,xerr=energy_err,linestyle='none',label="5000 mm")
	plt.errorbar(energy,resolution_3_6000,yerr=resolution_err_3_6000,xerr=energy_err,linestyle='none',label="6000 mm")
	plt.xlim(energy[2]-0.25,energy[-1]+0.25)
	plt.ylim(0,resolution_3_1000[2]+resolution_err_3_1000[2]+0.05)
	plt.xlabel("Kinetic Energy [MeV]")
	plt.ylabel("Resolution [\u03C3/E]")
	plt.title("Electrons in Baseline WATCHMAN Detector WbLS 3%")
	plt.legend()
	plt.grid()
	plt.savefig("../electrons_resolution_wbls_3pc_position_%f.pdf" % interval)
	plt.show()

	plt.errorbar(energy,resolution_5_0,yerr=resolution_err_5_0,xerr=energy_err,linestyle='none',label="0 mm")
	#plt.errorbar(energy,resolution_5_1000,yerr=resolution_err_5_1000,xerr=energy_err,linestyle='none',label="1000 mm")
	plt.errorbar(energy,resolution_5_2000,yerr=resolution_err_5_2000,xerr=energy_err,linestyle='none',label="2000 mm")
	#plt.errorbar(energy,resolution_5_3000,yerr=resolution_err_5_3000,xerr=energy_err,linestyle='none',label="3000 mm")
	plt.errorbar(energy,resolution_5_4000,yerr=resolution_err_5_4000,xerr=energy_err,linestyle='none',label="4000 mm")
	#plt.errorbar(energy,resolution_5_5000,yerr=resolution_err_5_5000,xerr=energy_err,linestyle='none',label="5000 mm")
	plt.errorbar(energy,resolution_5_6000,yerr=resolution_err_5_6000,xerr=energy_err,linestyle='none',label="6000 mm")
	plt.xlim(energy[2]-0.25,energy[-1]+0.25)
	plt.ylim(0,resolution_5_1000[2]+resolution_err_5_1000[2]+0.05)
	plt.xlabel("Kinetic Energy [MeV]")
	plt.ylabel("Resolution [\u03C3/E]")
	plt.title("Electrons in Baseline WATCHMAN Detector WbLS 5%")
	plt.legend()
	plt.grid()
	plt.savefig("../electrons_resolution_wbls_5pc_position_%f.pdf" % interval)
	plt.show()
	
	fit_1, fit_err_1 = np.polyfit(energy[2:-2],resolution_1_0[2:-2],2,cov=True)
	fit_3, fit_err_3 = np.polyfit(energy[2:-2],resolution_3_0[2:-2],2,cov=True)
	fit_5, fit_err_5 = np.polyfit(energy[2:-2],resolution_5_0[2:-2],2,cov=True)

	plt.plot(energy[2:-2], fit_1[2] + fit_1[1]*energy[2:-2] + fit_1[0]*energy[2:-2]*energy[2:-2])
	plt.errorbar(energy[2:-2],resolution_1_0[2:-2],yerr=resolution_err_1_0[2:-2],xerr=energy_err,linestyle='none',color=Tol_bright[0],label="WbLS 1%")
	plt.plot(energy[2:-2], fit_3[2] + fit_3[1]*energy[2:-2] + fit_3[0]*energy[2:-2]*energy[2:-2],color=Tol_bright[3])
	plt.errorbar(energy[2:-2],resolution_3_0[2:-2],yerr=resolution_err_3_0[2:-2],xerr=energy_err,linestyle='none',color=Tol_bright[3],label="WbLS 3%")
	plt.plot(energy[2:-2], fit_5[2] + fit_5[1]*energy[2:-2] + fit_5[0]*energy[2:-2]*energy[2:-2],color=Tol_bright[7])
	plt.errorbar(energy[2:-2],resolution_5_0[2:-2],yerr=resolution_err_5_0[2:-2],xerr=energy_err,linestyle='none',color=Tol_bright[7],label="WbLS 5%")
	plt.ylim(0,resolution_5_1000[2]+resolution_err_5_1000[2]+0.05)
	plt.xlabel("Kinetic Energy [MeV]")
	plt.ylabel("Resolution [\u03C3/E]")
	plt.title("Electrons in NEO (20% PMT Coverage, 6.7 m inner radius)")
	plt.legend()
	plt.grid()
	plt.savefig("../electrons_resolution_centre_best_fit_%f.pdf" % interval)
	plt.show()

elif pos == 'centre':

	fit_1, fit_err_1 = np.polyfit(energy[2:-2],resolution_1_0[2:-2],2,cov=True)
	fit_3, fit_err_3 = np.polyfit(energy[2:-2],resolution_3_0[2:-2],2,cov=True)
	fit_5, fit_err_5 = np.polyfit(energy[2:-2],resolution_5_0[2:-2],2,cov=True)

	plt.plot(energy[2:-2], fit_1[2] + fit_1[1]*energy[2:-2] + fit_1[0]*energy[2:-2]*energy[2:-2])
	plt.errorbar(energy[2:-2],resolution_1_0[2:-2],yerr=resolution_err_1_0[2:-2],xerr=energy_err,linestyle='none',color=Tol_bright[0],label="WbLS 1%")
	plt.plot(energy[2:-2], fit_3[2] + fit_3[1]*energy[2:-2] + fit_3[0]*energy[2:-2]*energy[2:-2],color=Tol_bright[3])
	plt.errorbar(energy[2:-2],resolution_3_0[2:-2],yerr=resolution_err_3_0[2:-2],xerr=energy_err,linestyle='none',color=Tol_bright[3],label="WbLS 3%")
	plt.plot(energy[2:-2], fit_5[2] + fit_5[1]*energy[2:-2] + fit_5[0]*energy[2:-2]*energy[2:-2],color=Tol_bright[7])
	plt.errorbar(energy[2:-2],resolution_5_0[2:-2],yerr=resolution_err_5_0[2:-2],xerr=energy_err,linestyle='none',color=Tol_bright[7],label="WbLS 5%")
	plt.ylim(0,resolution_1_0[2]+resolution_err_1_0[2]+0.05)
	plt.xlabel("Kinetic Energy [MeV]")
	plt.ylabel("Resolution [\u03C3/E]")
	plt.title("Electrons in NEO (20% PMT Coverage, 6.7 m inner radius)")
	plt.legend()
	plt.grid()
	plt.savefig("../electrons_resolution_centre_best_fit_%f.pdf" % interval)
	plt.show()
	
elif pos == 'letterbox':

	interval = 0.5

	res_8_50_8_10pct,res_err_8_50_8_10pct,en_8_50_8_10pct,en_err_8_50_8_10pct = value_extraction("8_50_8_10pct",interval,'')
	res_8_50_8_15pct,res_err_8_50_8_15pct,en_8_50_8_15pct,en_err_8_50_8_15pct = value_extraction("8_50_8_15pct",interval,'')
	res_8_50_8_20pct,res_err_8_50_8_20pct,en_8_50_8_20pct,en_err_8_50_8_20pct = value_extraction("8_50_8_20pct",interval,'')
	res_8_80_8_10pct,res_err_8_80_8_10pct,en_8_80_8_10pct,en_err_8_80_8_10pct = value_extraction("8_80_8_10pct",interval,'')
	res_8_80_8_15pct,res_err_8_80_8_15pct,en_8_80_8_15pct,en_err_8_80_8_15pct = value_extraction("8_80_8_15pct",interval,'')
	res_8_80_8_20pct,res_err_8_80_8_20pct,en_8_80_8_20pct,en_err_8_80_8_20pct = value_extraction("8_80_8_20pct",interval,'')
	
	energy = np.arange(interval,10.+interval,interval)
	energy_err = interval/np.sqrt(12)
	
	plt.errorbar(energy[1:-1],res_8_50_8_10pct[1:-1],yerr=res_err_8_50_8_10pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='10% PC')
	plt.errorbar(energy[1:-1],res_8_50_8_15pct[1:-1],yerr=res_err_8_50_8_15pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='15% PC')
	plt.errorbar(energy[1:-1],res_8_50_8_20pct[1:-1],yerr=res_err_8_50_8_20pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[7],label='20% PC')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("8 m x 50 m x 8 m Letterbox")
	plt.grid()
	plt.savefig("../8_50_8_letterbox.png")
	plt.show()
	
	plt.errorbar(energy[1:-1],res_8_80_8_10pct[1:-1],yerr=res_err_8_80_8_10pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='10% PC')
	plt.errorbar(energy[1:-1],res_8_80_8_15pct[1:-1],yerr=res_err_8_80_8_15pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='15% PC')
	plt.errorbar(energy[1:-1],res_8_80_8_20pct[1:-1],yerr=res_err_8_80_8_20pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[7],label='20% PC')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("8 m x 80 m x 8 m Letterbox")
	plt.grid()
	plt.savefig("../8_80_8_letterbox.png")
	plt.show()
	
	plt.errorbar(energy[1:-1],res_8_50_8_10pct[1:-1],yerr=res_err_8_50_8_10pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='8 x 50 x 8 m')
	plt.errorbar(energy[1:-1],res_8_80_8_10pct[1:-1],yerr=res_err_8_80_8_10pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='8 x 80 x 8 m')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("10% PC Letterbox")
	plt.grid()
	plt.savefig("../10pct_letterbox.png")
	plt.show()
	
	plt.errorbar(energy[1:-1],res_8_50_8_15pct[1:-1],yerr=res_err_8_50_8_15pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='8 x 50 x 8 m')
	plt.errorbar(energy[1:-1],res_8_80_8_15pct[1:-1],yerr=res_err_8_80_8_15pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='8 x 80 x 8 m')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("15% PC Letterbox")
	plt.grid()
	plt.savefig("../15pct_letterbox.png")
	plt.show()
	
	plt.errorbar(energy[1:-1],res_8_50_8_20pct[1:-1],yerr=res_err_8_50_8_20pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='8 x 50 x 8 m')
	plt.errorbar(energy[1:-1],res_8_80_8_20pct[1:-1],yerr=res_err_8_80_8_20pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='8 x 80 x 8 m')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("20% PC Letterbox")
	plt.grid()
	plt.savefig("../20pct_letterbox.png")
	plt.show()

elif pos == 'cylinder':

	interval = 0.25

	energy = np.arange(interval,10.+interval,interval)
	energy_err = interval/np.sqrt(12)

	res_10_10_10pct, res_err_10_10_10pct, en_10_10_10pct, en_err_10_10_10pct = value_extraction("10_10_10pct",interval,'')
	res_10_10_15pct, res_err_10_10_15pct, en_10_10_15pct, en_err_10_10_15pct = value_extraction("10_10_15pct",interval,'')
	res_10_10_20pct, res_err_10_10_20pct, en_10_10_20pct, en_err_10_10_20pct = value_extraction("10_10_20pct",interval,'')
	res_12_12_10pct, res_err_12_12_10pct, en_12_12_10pct, en_err_20_20_10pct = value_extraction("12_12_10pct",interval,'')
	res_12_12_15pct, res_err_12_12_15pct, en_12_12_15pct, en_err_20_20_15pct = value_extraction("12_12_15pct",interval,'')
	res_12_12_20pct, res_err_12_12_20pct, en_12_12_20pct, en_err_20_20_20pct = value_extraction("12_12_20pct",interval,'')
	
	plt.errorbar(energy[1:-1],res_10_10_10pct[1:-1],yerr=res_err_10_10_10pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='10% PC')
	plt.errorbar(energy[1:-1],res_10_10_15pct[1:-1],yerr=res_err_10_10_15pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='15% PC')
	plt.errorbar(energy[1:-1],res_10_10_20pct[1:-1],yerr=res_err_10_10_20pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[7],label='20% PC')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("10 m x 10 m Cylinder")
	plt.grid()
	#plt.ylim(0,2*res_10_10_10pct[1])
	plt.savefig("../10_10_cylinder.png")
	plt.show()
	
	plt.errorbar(energy[1:-1],res_12_12_10pct[1:-1],yerr=res_err_12_12_10pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='10% PC')
	plt.errorbar(energy[1:-1],res_12_12_15pct[1:-1],yerr=res_err_12_12_15pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='15% PC')
	plt.errorbar(energy[1:-1],res_12_12_20pct[1:-1],yerr=res_err_12_12_20pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[7],label='20% PC')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("12 m x 12 m Cylinder")
	plt.grid()
	#plt.ylim(0,2*res_12_12_10pct[1])
	plt.savefig("../12_12_cylinder.png")
	plt.show()
	
	plt.errorbar(energy[1:-1],res_10_10_10pct[1:-1],yerr=res_err_10_10_10pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='10 x 10 m')
	plt.errorbar(energy[1:-1],res_12_12_10pct[1:-1],yerr=res_err_12_12_10pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='12 x 12 m')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("10% PC Cylinder")
	plt.grid()
	#plt.ylim(0,2*res_10_10_10pct[1])
	plt.savefig("../10pct_cylinder.png")
	plt.show()
	
	plt.errorbar(energy[1:-1],res_10_10_15pct[1:-1],yerr=res_err_10_10_15pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='10 x 10 m')
	plt.errorbar(energy[1:-1],res_12_12_15pct[1:-1],yerr=res_err_12_12_15pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='12 x 12 m')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("15% PC Cylinder")
	plt.grid()
	#plt.ylim(0,2*res_10_10_15pct[1])
	plt.savefig("../15pct_cylinder.png")
	plt.show()
	
	plt.errorbar(energy[1:-1],res_10_10_20pct[1:-1],yerr=res_err_10_10_20pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[0],label='10 x 10 m')
	plt.errorbar(energy[1:-1],res_12_12_20pct[1:-1],yerr=res_err_12_12_20pct[1:-1],xerr=energy_err,linestyle='none',color=Tol_bright[3],label='12 x 12 m')
	plt.xlabel('Kinetic energy [MeV]')
	plt.ylabel("Resolution [\u03C3/E]")
	plt.legend()
	plt.title("20% PC Cylinder")
	plt.grid()
	#plt.ylim(0,2*res_10_10_20pct[1])
	plt.savefig("../20pct_cylinder.png")
	plt.show()
