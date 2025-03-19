#!/usr/bin/env python

import os
import sys
import subprocess

profile = sys.argv[1]

os.system('python ./mesa_to_GR1D.py '+profile)
#rename the short file
rename_command='mv *.short '+profile+'.short'
os.system(rename_command)
#produce the isotope file
os.system('python ./MESA_isotopes.py '+profile+' '+profile+'iso.dat')
