import numpy as np
import matplotlib.pyplot as plt
import sys


def get_lightcurve(lc_file):
    src = np.genfromtxt(lc_file)
    t = src[:, 0]/(24*60*60)  # days
    L = src[:, 1]  # erg/s
    return t, L


def get_ni_lum(ni_file):
    src = np.genfromtxt(ni_file)
    t = src[:, 0]/(24*60*60)  # days
    L_ni = src[:, 1]  # erg/s
    return t, L_ni


if __name__ == "__main__":
    root = sys.argv[1]  # path to output read from cmd line
    lc_file = root+"/lum_observed.dat"
    fig, ax = plt.subplots()
    t, L = get_lightcurve(lc_file)
    ax.plot(t, np.log10(L), label=r"MESA+STIR+MESA+SNEC", zorder=1)
    try:
        ni_file = root+"/Ni_total_luminosity.dat"
        t, L_ni = get_ni_lum(ni_file)
        ax.plot(t, np.log10(L_ni), ls='--', lw=4, c="#808080", label=r"$^{56}\mathrm{Ni}$ decay", zorder=0)
    except FileNotFoundError:
        pass
    ax.legend(fontsize=20)
    ax.set_xlim(-1, 80)
    ax.set_ylim
    ax.set_xlabel(r"$t \mathrm{[days]}$")
    ax.set_ylabel(r"$\log_{10}(L / \mathrm{[erg \ s^{-1}]})$")
    plt.show()
