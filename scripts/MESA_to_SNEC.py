#!/usr/bin/env python

""" wrapper script to produce all SNEC input from MESA output """
import sys
import os

from make_grid_pattern import make_grid_pattern
from MESA_profile_to_short import convert_mesa_profile_to_short_file
from MESA_profile_to_iso import make_iso_file


if __name__ == "__main__":
    profile = sys.argv[1]
    try:
        output_folder = sys.argv[2]
    except:
        output_folder = "./test"
    os.system("mkdir -p "+output_folder)
    make_grid_pattern(profile, output_file=
                      output_folder+"/test_grid_pattern.dat")
    convert_mesa_profile_to_short_file(profile, output_file=
                                       output_folder+"test_short.short")
    make_iso_file(profile, output=output_folder+"test_iso.data")
    print("converted MESA output", profile, "to SNEC input!")
