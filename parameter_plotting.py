import numpy as np
import matplotlib.pyplot as plt
import re

def value_extraction_nhits(media,interval,tags):

	stats = open("../%s_%f%s/stats_%s.txt" % (media,interval,tags,media), 'r')
	stats_lines = stats.readlines()

	P0 = stats_lines[1]
	p0_string = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in P0)
	p0_options = [float(i) for i in p0_string.split()]
	p0 = p0_options[1]

	P0_err = stats_lines[2]
	match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
	final_list = [float(x) for x in re.findall(match_number, P0_err)]
	p0_err = final_list[1]

	P1 = stats_lines[3]
	p1_string = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in P1)
	p1_options = [float(i) for i in p1_string.split()]
	p1 = p1_options[1]

	P1_err = stats_lines[4]
	match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
	final_list = [float(x) for x in re.findall(match_number, P1_err)]
	p1_err = final_list[1]

	P2 = stats_lines[5]
	p2_string = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in P2)
	p2_options = [float(i) for i in p2_string.split()]
	p2 = p2_options[1]

	P2_err = stats_lines[6]
	match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
	final_list = [float(x) for x in re.findall(match_number, P2_err)]
	p2_err = final_list[1]

	return(p0,p0_err,p1,p1_err,p2,p2_err)

p0_0,p0_0_err,p1_0,p1_0_err,p2_0,p2_0_err = value_extraction_nhits("wbls_1pc",0.25,'_centre')
p0_1000,p0_1000_err,p1_1000,p1_1000_err,p2_1000,p2_1000_err = value_extraction_nhits("wbls_1pc",0.25,'_1000')
p0_2000,p0_2000_err,p1_2000,p1_2000_err,p2_2000,p2_2000_err = value_extraction_nhits("wbls_1pc",0.25,'_2000')
p0_3000,p0_3000_err,p1_3000,p1_3000_err,p2_3000,p2_3000_err = value_extraction_nhits("wbls_1pc",0.25,'_3000')
p0_4000,p0_4000_err,p1_4000,p1_4000_err,p2_4000,p2_4000_err = value_extraction_nhits("wbls_1pc",0.25,'_4000')
p0_5000,p0_5000_err,p1_5000,p1_5000_err,p2_5000,p2_5000_err = value_extraction_nhits("wbls_1pc",0.25,'_5000')
p0_6000,p0_6000_err,p1_6000,p1_6000_err,p2_6000,p2_6000_err = value_extraction_nhits("wbls_1pc",0.25,'_6000')

r = [0,1000,2000,3000,4000,5000,6000]
p0_1 = [p0_0,p0_1000,p0_2000,p0_3000,p0_4000,p0_5000,p0_6000]
p1_1 = [p1_0,p1_1000,p1_2000,p1_3000,p1_4000,p1_5000,p1_6000]
p2_1 = [p2_0,p2_1000,p2_2000,p2_3000,p2_4000,p2_5000,p2_6000]
p0_err_1 = [p0_0_err,p0_1000_err,p0_2000_err,p0_3000_err,p0_4000_err,p0_5000_err,p0_6000_err]
p1_err_1 = [p1_0_err,p1_1000_err,p1_2000_err,p1_3000_err,p1_4000_err,p1_5000_err,p1_6000_err]
p2_err_1 = [p2_0_err,p2_1000_err,p2_2000_err,p2_3000_err,p2_4000_err,p2_5000_err,p2_6000_err]

print("\np0_1 = \n",p0_1)
print("\np1_1 = \n",p1_1)
print("\np2_1 = \n",p2_1)

p0_0,p0_0_err,p1_0,p1_0_err,p2_0,p2_0_err = value_extraction_nhits("wbls_3pc",0.25,'_centre')
p0_1000,p0_1000_err,p1_1000,p1_1000_err,p2_1000,p2_1000_err = value_extraction_nhits("wbls_3pc",0.25,'_1000')
p0_2000,p0_2000_err,p1_2000,p1_2000_err,p2_2000,p2_2000_err = value_extraction_nhits("wbls_3pc",0.25,'_2000')
p0_3000,p0_3000_err,p1_3000,p1_3000_err,p2_3000,p2_3000_err = value_extraction_nhits("wbls_3pc",0.25,'_3000')
p0_4000,p0_4000_err,p1_4000,p1_4000_err,p2_4000,p2_4000_err = value_extraction_nhits("wbls_3pc",0.25,'_4000')
p0_5000,p0_5000_err,p1_5000,p1_5000_err,p2_5000,p2_5000_err = value_extraction_nhits("wbls_3pc",0.25,'_5000')
p0_6000,p0_6000_err,p1_6000,p1_6000_err,p2_6000,p2_6000_err = value_extraction_nhits("wbls_3pc",0.25,'_6000')

p0_3 = [p0_0,p0_1000,p0_2000,p0_3000,p0_4000,p0_5000,p0_6000]
p1_3 = [p1_0,p1_1000,p1_2000,p1_3000,p1_4000,p1_5000,p1_6000]
p2_3 = [p2_0,p2_1000,p2_2000,p2_3000,p2_4000,p2_5000,p2_6000]
p0_err_3 = [p0_0_err,p0_1000_err,p0_2000_err,p0_3000_err,p0_4000_err,p0_5000_err,p0_6000_err]
p1_err_3 = [p1_0_err,p1_1000_err,p1_2000_err,p1_3000_err,p1_4000_err,p1_5000_err,p1_6000_err]
p2_err_3 = [p2_0_err,p2_1000_err,p2_2000_err,p2_3000_err,p2_4000_err,p2_5000_err,p2_6000_err]

print("\np0_3 = \n",p0_3)
print("\np1_3 = \n",p1_3)
print("\np2_3 = \n",p2_3)

p0_0,p0_0_err,p1_0,p1_0_err,p2_0,p2_0_err = value_extraction_nhits("wbls_5pc",0.25,'_centre')
p0_1000,p0_1000_err,p1_1000,p1_1000_err,p2_1000,p2_1000_err = value_extraction_nhits("wbls_5pc",0.25,'_1000')
p0_2000,p0_2000_err,p1_2000,p1_2000_err,p2_2000,p2_2000_err = value_extraction_nhits("wbls_5pc",0.25,'_2000')
p0_3000,p0_3000_err,p1_3000,p1_3000_err,p2_3000,p2_3000_err = value_extraction_nhits("wbls_5pc",0.25,'_3000')
p0_4000,p0_4000_err,p1_4000,p1_4000_err,p2_4000,p2_4000_err = value_extraction_nhits("wbls_5pc",0.25,'_4000')
p0_5000,p0_5000_err,p1_5000,p1_5000_err,p2_5000,p2_5000_err = value_extraction_nhits("wbls_5pc",0.25,'_5000')
p0_6000,p0_6000_err,p1_6000,p1_6000_err,p2_6000,p2_6000_err = value_extraction_nhits("wbls_5pc",0.25,'_6000')

p0_5 = [p0_0,p0_1000,p0_2000,p0_3000,p0_4000,p0_5000,p0_6000]
p1_5 = [p1_0,p1_1000,p1_2000,p1_3000,p1_4000,p1_5000,p1_6000]
p2_5 = [p2_0,p2_1000,p2_2000,p2_3000,p2_4000,p2_5000,p2_6000]
p0_err_5 = [p0_0_err,p0_1000_err,p0_2000_err,p0_3000_err,p0_4000_err,p0_5000_err,p0_6000_err]
p1_err_5 = [p1_0_err,p1_1000_err,p1_2000_err,p1_3000_err,p1_4000_err,p1_5000_err,p1_6000_err]
p2_err_5 = [p2_0_err,p2_1000_err,p2_2000_err,p2_3000_err,p2_4000_err,p2_5000_err,p2_6000_err]

print("\np0_5 = \n",p0_5)
print("\np1_5 = \n",p1_5)
print("\np2_5 = \n",p2_5)

#plt.plot(r,p0,label="p0")
#plt.plot(r,p1,label="p1")
#plt.plot(r,p2,label="p2")
#plt.xlabel("r [mm]")
#plt.legend()
#plt.show()

fig,ax = plt.subplots()
ax.errorbar(r,p1_1,yerr=p1_err_1,color='red',linestyle='dashed',label="p1")
ax.set_ylabel("p1",color='red')
ax2=ax.twinx()
ax2.errorbar(r,p2_1,yerr=p2_err_1,linestyle='dashed',label="p2",color='blue')
ax2.set_ylabel("p2",color='blue')
ax2.ticklabel_format(axis='y',style='sci')
#plt.title("WbLS 3% Electrons Reconstructed in FRED (n100)")
ax.set_xlabel("r [mm]")
#plt.ylabel("Mean n100")
#plt.legend()
plt.title("WbLS 1% - Fit Parameters")
plt.savefig("../p1_p2_wbls_1pc_distance.pdf")
plt.show()

fig,ax = plt.subplots()
ax.errorbar(r,p1_3,yerr=p1_err_3,color='red',linestyle='dashed',label="p1")
ax.set_ylabel("p1",color='red')
ax2=ax.twinx()
ax2.errorbar(r,p2_3,yerr=p2_err_3,linestyle='dashed',label="p2",color='blue')
ax2.set_ylabel("p2",color='blue')
ax2.ticklabel_format(axis='y',style='sci')
#plt.title("WbLS 3% Electrons Reconstructed in FRED (n100)")
ax.set_xlabel("r [mm]")
#plt.ylabel("Mean n100")
#plt.legend()
plt.title("WbLS 3% - Fit Parameters")
plt.savefig("../p1_p2_wbls_3pc_distance.pdf")
plt.show()

fig,ax = plt.subplots()
ax.errorbar(r,p1_5,yerr=p1_err_5,color='red',linestyle='dashed',label="p1")
ax.set_ylabel("p1",color='red')
ax2=ax.twinx()
ax2.errorbar(r,p2_5,yerr=p2_err_5,linestyle='dashed',label="p2",color='blue')
ax2.set_ylabel("p2",color='blue')
ax2.ticklabel_format(axis='y',style='sci')
#plt.title("WbLS 3% Electrons Reconstructed in FRED (n100)")
ax.set_xlabel("r [mm]")
#plt.ylabel("Mean n100")
#plt.legend()
plt.title("WbLS 5% - Fit Parameters")
plt.savefig("../p1_p2_wbls_5pc_distance.pdf")
plt.show()
