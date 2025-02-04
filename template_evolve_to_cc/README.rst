.. _template_evolve_to_cc:

***************************
template_evolve_to_cc
***************************

For bit for bit convergence, we recomended to run by using the ./run_all script instead of restarting from models,
see https://github.com/MESAHub/mesa/issues/610.

Note that for higher masses at solar metallicity, some combination of Pextra_factor, mass-loss, and/or superadiabatic convection reduction (e.g. mlt++)
might be necessary to stabilize the surface and avoid numerical issues. See the 80Msun_zams_to_cc test_suite as an example.

For production science we recommend adopting tighter mesh and timestep controls.

Physical checks
===============

None

Inlists
=======

This test case has seven parts.

* Part 1 (``inlist_to_cc``) reads a model and evolves it until core collapse.


Last-Updated: 4Feb2025 by EbF
