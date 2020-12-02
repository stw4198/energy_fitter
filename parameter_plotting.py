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

	P1 = stats_lines[3]
	p1_string = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in P1)
	p1_options = [float(i) for i in p1_string.split()]
	p1 = p1_options[1]

	P2 = stats_lines[5]
	p2_string = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in P2)
	p2_options = [float(i) for i in p2_string.split()]
	p2 = p2_options[1]

	return(p0,p1,p2)

p0_0,p1_0,p2_0 = value_extraction_nhits("wbls_1pc",0.25,'_centre')
p0_1000,p1_1000,p2_1000 = value_extraction_nhits("wbls_1pc",0.25,'_1000')
p0_2000,p1_2000,p2_2000 = value_extraction_nhits("wbls_1pc",0.25,'_2000')
p0_3000,p1_3000,p2_3000 = value_extraction_nhits("wbls_1pc",0.25,'_3000')
p0_4000,p1_4000,p2_4000 = value_extraction_nhits("wbls_1pc",0.25,'_4000')
p0_5000,p1_5000,p2_5000 = value_extraction_nhits("wbls_1pc",0.25,'_5000')
p0_6000,p1_6000,p2_6000 = value_extraction_nhits("wbls_1pc",0.25,'_6000')

r = [0,1000,2000,3000,4000,5000,6000]
p0 = [p0_0,p0_1000,p0_2000,p0_3000,p0_4000,p0_5000,p0_6000]
p1 = [p1_0,p1_1000,p1_2000,p1_3000,p1_4000,p1_5000,p1_6000]
p2 = [p2_0,p2_1000,p2_2000,p2_3000,p2_4000,p2_5000,p2_6000]

#plt.plot(r,p0,label="p0")
#plt.plot(r,p1,label="p1")
#plt.plot(r,p2,label="p2")
#plt.xlabel("r [mm]")
#plt.legend()
#plt.show()

fig,ax = plt.subplots()
ax.plot(r,p1,color='red',label="p1")
ax.set_ylabel("p1",color='red')
ax2=ax.twinx()
ax2.plot(r,p2,label="p2",color='blue')
ax2.set_ylabel("p2",color='blue')
ax2.ticklabel_format(axis='y',style='sci')
#plt.title("WbLS 3% Electrons Reconstructed in FRED (n100)")
ax.set_xlabel("r [mm]")
#plt.ylabel("Mean n100")
#plt.legend()
plt.show()
