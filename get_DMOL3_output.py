# -*- coding: utf-8 -*-

'''
From the folder get all the newest output files of 
DMOL3, then extract the SCF energy from the files
'''

import os, sys
from collections import defaultdict
#import getopt # later will involve this

def get_newest_files():

	folder = sys.argv[1]
	postfix = '.outmol'

	# get the right postfix files
	outmol_files = []
	for root, dirs, files in os.walk(folder):
		for filename in files:
			if filename.endswith(postfix):
				outmol_files.append(os.path.join(root, filename))

	# collapse the files to the same name dict
	samefile_dict = defaultdict(list)
	for fn in outmol_files:
		filename = fn.split('/')[-1]
		samefile_dict[filename].append(fn)

	# get the newest files
	newest_files = {}
	get_oldest = lambda x: sorted(x, key=lambda t: os.path.getmtime(t))[0]
	get_newest = lambda x: sorted(x, key=lambda t: os.path.getmtime(t))[-1]
	for filename, filepath in samefile_dict.items():
		newest_files[filename] = get_newest(filepath)

	return newest_files

def extract_DMOL_SCF(dmol_output):
	with open(dmol_output) as f:
		for line in f:
			if line.startswith('opt=='):
				energy = line.split()[2]
	return energy

def parser():
	newest_files = get_newest_files()
	for fname, fpath in newest_files.items():
		print fname, extract_DMOL_SCF(fpath)

parser()
