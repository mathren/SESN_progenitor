#!/usr/bin/env python

import os
import sys

# Edit line below to point to the location
where_the_scripts_are = "/home/mrenzo/Runs/TARDIS_connector_workshop/SESN_progenitor/scripts/"
profile = sys.argv[1]

os.system('python '+where_the_scripts_are+'mesa_to_GR1D.py '+profile+' '+profile+'.short')
os.system('python '+where_the_scripts_are+'MESA_isotopes.py '+profile+' '+profile+'.iso.dat')
