import numpy as np
import os
import re
import csv

docstring= """
    Usage: run_files.py [options]

    Arguments:

    Options:

    ## System options

    --medium=<_m>             medium to test energy resolution of
"""

try:
    import docopt
    arguments = docopt.docopt(docstring)
    print('\nUsing docopt as the user control interface\n')
except ImportError:
    print('docopt is not a recognized module, it is required to run this module')

print(docstring)

if not (arguments['--medium']):
        print("--medium argument not provided\n")
else:
     	medium = arguments['--medium']
cwd = os.getcwd()

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

config = '6.7PSUP_20_pct_PC'

p0 = []
p0_err = []
p1 = []
p1_err = []
p2 = []
p2_err = []

r = [-1,6500,6000,5500,5000,4500,4000,3500,3000,2500,2000,1500,1000,500,0]
r_len = len(r)

for i in range(r_len-1):
	p0_file,p0_err_file,p1_file,p1_err_file,p2_file,p2_err_file = value_extraction(medium,0.25,r[i+1])
	p0.append(p0_file)
	p0_err.append(p0_err_file)
	p1.append(p1_file)
	p1_err.append(p1_err_file)
	p2.append(p2_file)
	p2_err.append(p2_err_file)
			
with open('../%s_%s.csv'%(medium,config),'w',newline='') as csvfile:
	write_csv = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	write_csv.writerow(['r','p0','p0_err','p1','p1_err','p2','p2_err'])
	write_csv.writerow([-1,0,0,0,0,0,0])
	for i in range(r_len-1):
		write_csv.writerow([r[i+1],p0[i],p0_err[i],p1[i],p1_err[i],p2[i],p2_err[i]])
