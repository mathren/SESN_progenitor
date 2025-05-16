"""
modified from the `grid_setup.py` script provided with SNEC
"""


def make_grid_pattern(profile, output_file="input/GridPattern.dat"):
    """ profile: path to MESA profile output to convert
        output_file: optional, path to output
    """

    delta = []
    grid_pattern = []

    imax = 1000
    itran = 100

    ratio1 = 0.1
    ratio2 = 0.001

    f1 = ratio1**(1/(itran-2))
    f2 = ratio2**(1/(imax-itran-1))

    delta_tran = ( (1-f2)*(1-f1)
                   /((1-f2)*(1-f1**(itran-1))+(1-f1)*(1-f2**(imax-itran))) )

    for l in range(0,itran-1):
        delta.append(delta_tran*f1**(itran-2-l))

    for l in range(0,imax-itran):
        delta.append(delta_tran*f2**(l))

    grid_pattern.append(0.0)
    for l in range(0,imax-1):
        grid_pattern.append(grid_pattern[l]+delta[l])

    print "grid pattern consists of", len(grid_pattern), "points"
    with open(output_file,"w") as outfile:
        for l in range(0,imax):
            outfile.write(str(grid_pattern[l]) + '\n')
    print("done! New grid pattern file at", output_file)


if __name__ == "__main__":
    profile = sys.argv[1]
    try:
        output_file = sys.argv[2]
    except:
        output_file = ""
    make_grid_pattern(profile, output_file)
