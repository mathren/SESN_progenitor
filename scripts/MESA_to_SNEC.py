#!/usr/bin/env python

""" wrapper script to produce all SNEC input from MESA output """
import sys

from make_grid_pattern import make_grid_pattern
from MESA_profile_to_short import convert_mesa_profile_to_short_file
from MESA_profile_to_iso import make_iso_file


if __name__ == "__main__":
    profile = sys.argv[1]
    make_grid_pattern(profile, output_file=
                      "./test/test_grid_pattern.dat")
    convert_mesa_profile_to_short_file(profile, output_file=
                                       "./test/test_short.short")
    make_iso_file(profile, output="./test/test_iso.data")
    print("converted MESA output", profile, "to SNEC input!")
