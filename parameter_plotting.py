import numpy as np
import matplotlib.pyplot as plt
import re

Tol_bright = ['#4477AA','#66CCEE','#228833',
                     '#CCBB44','#EE6677','#AA3377','#BBBBBB','k']

def value_extraction(medium,interval,tags):

	stats = open("../%s_%f_%s/stats_%s.txt" % (medium,interval,tags,medium), 'r')
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

#medium = 'wbls_1pc_baseline'

r = [-1,6500,6000,5500,5000,4500,4000,3500,3000,2500,2000,1500,1000,500,0]
r_len = len(r)
	
p0_1 = []
p0_err_1 = []
p1_1 = []
p1_err_1 = []
p2_1 = []
p2_err_1 = []

for i in range(r_len-1):
	p0_file,p0_err_file,p1_file,p1_err_file,p2_file,p2_err_file = value_extraction('wbls_1pc_baseline',0.25,r[i+1])
	p0_1.append(p0_file)
	p0_err_1.append(p0_err_file)
	p1_1.append(p1_file)
	p1_err_1.append(p1_err_file)
	p2_1.append(p2_file)
	p2_err_1.append(p2_err_file)
	
p0_3 = []
p0_err_3 = []
p1_3 = []
p1_err_3 = []
p2_3 = []
p2_err_3 = []

for i in range(r_len-1):
	p0_file,p0_err_file,p1_file,p1_err_file,p2_file,p2_err_file = value_extraction('wbls_3pc_baseline',0.25,r[i+1])
	p0_3.append(p0_file)
	p0_err_3.append(p0_err_file)
	p1_3.append(p1_file)
	p1_err_3.append(p1_err_file)
	p2_3.append(p2_file)
	p2_err_3.append(p2_err_file)
	
p0_5 = []
p0_err_5 = []
p1_5 = []
p1_err_5 = []
p2_5 = []
p2_err_5 = []

for i in range(r_len-1):
	p0_file,p0_err_file,p1_file,p1_err_file,p2_file,p2_err_file = value_extraction('wbls_5pc_baseline',0.25,r[i+1])
	p0_5.append(p0_file)
	p0_err_5.append(p0_err_file)
	p1_5.append(p1_file)
	p1_err_5.append(p1_err_file)
	p2_5.append(p2_file)
	p2_err_5.append(p2_err_file)
	
p2_1_rel = []
p2_3_rel = []
p2_5_rel = []

p2_len = len(p2_5)

for i in range(p2_len):
	p2_1_rel.append(p2_1[i]/p2_1[0])
	p2_3_rel.append(p2_3[i]/p2_3[0])
	p2_5_rel.append(p2_5[i]/p2_5[0])
	
p2_err_1_rel = []
p2_err_3_rel = []
p2_err_5_rel = []

p2_err_len = len(p2_err_5)

for i in range(p2_err_len):
	p2_err_1_rel.append((p2_1[i]/p2_1[0])*np.sqrt((p2_err_1[i]/p2_1[i])**2 + (p2_err_1[0]/p2_1[0])**2))
	p2_err_3_rel.append((p2_3[i]/p2_3[0])*np.sqrt((p2_err_3[i]/p2_3[i])**2 + (p2_err_3[0]/p2_3[0])**2))
	p2_err_5_rel.append((p2_5[i]/p2_5[0])*np.sqrt((p2_err_5[i]/p2_5[i])**2 + (p2_err_5[0]/p2_5[0])**2))
	
#plt.plot(r[1:],p0)
#plt.xlabel('r [mm]')
#plt.ylabel('p0')
#plt.show()

#plt.plot(r[1:],p1)
#plt.xlabel('r [mm]')
#plt.ylabel('p1')
#plt.show()

plt.errorbar(r[1:],p2_1,yerr=p2_err_1,color=Tol_bright[0],linestyle='solid',label="WbLS 1%")
plt.errorbar(r[1:],p2_3,yerr=p2_err_3,color=Tol_bright[3],linestyle='dashed',label="WbLS 3%")
plt.errorbar(r[1:],p2_5,yerr=p2_err_5,color=Tol_bright[7],linestyle='dotted',label="WbLS 5%")
plt.xlabel('r [mm]')
plt.ylabel('p2')
plt.title("Electrons, 6.7 m PSUP, 20% PC")
plt.grid()
plt.legend(loc='upper left')
plt.savefig("../p2_saturation.png")
plt.show()

plt.errorbar(r[1:],p2_1_rel,yerr=p2_err_1_rel,color=Tol_bright[0],linestyle='solid',label="WbLS 1%")
plt.errorbar(r[1:],p2_3_rel,yerr=p2_err_3_rel,color=Tol_bright[3],linestyle='dashed',label="WbLS 3%")
plt.errorbar(r[1:],p2_5_rel,yerr=p2_err_5_rel,color=Tol_bright[7],linestyle='dotted',label="WbLS 5%")
plt.xlabel('r [mm]')
plt.ylabel('p2/p2$_0$')
plt.title("Electrons, 6.7 m PSUP, 20% PC")
plt.grid()
plt.legend(loc='upper left')
plt.savefig("../p2_saturation_rel.png")
plt.show()
			
