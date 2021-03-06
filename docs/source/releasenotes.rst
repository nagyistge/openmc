.. _releasenotes:

==============================
Release Notes for OpenMC 0.8.0
==============================

This release of OpenMC includes a few new major features including the
capability to perform neutron transport with multi-group cross section data as
well as experimental support for the windowed multipole method being developed
at MIT. Source sampling options have also been expanded significantly, with the
option to supply arbitrary tabular and discrete distributions for energy, angle,
and spatial coordinates.

The Python API has been significantly restructured in this release compared to
version 0.7.1. Any scripts written based on the version 0.7.1 API will likely
need to be rewritten. Some of the most visible changes include the following:

- ``SettingsFile`` is now ``Settings``, ``MaterialsFile`` is now ``Materials``,
  and ``TalliesFile`` is now ``Tallies``.
- The ``GeometryFile`` class no longer exists and is replaced by the
  ``Geometry`` class which now has an ``export_to_xml()`` method.
- Source distributions are defined using the ``Source`` class and assigned to
  the ``Settings.source`` property.
- The ``Executor`` class no longer exists and is replaced by ``openmc.run()``
  and ``openmc.plot_geometry()`` functions.

The Python API documentation has also been significantly expanded.

-------------------
System Requirements
-------------------

There are no special requirements for running the OpenMC code. As of this
release, OpenMC has been tested on a variety of Linux distributions and Mac
OS X. Numerous users have reported working builds on Microsoft Windows, but your
mileage may vary. Memory requirements will vary depending on the size of the
problem at hand (mostly on the number of nuclides and tallies in the problem).

------------
New Features
------------

- Multi-group mode
- Vast improvements to the Python API
- Experimental windowed multipole capability
- Periodic boundary conditions
- Expanded source sampling options
- Distributed materials
- Subcritical multiplication support
- Improved method for reproducible URR table sampling
- Refactor of continuous-energy reaction data
- Improved documentation and new Jupyter notebooks

---------
Bug Fixes
---------

- 70daa7_: Make sure MT=3 cross section is not used
- 40b05f_: Ensure source bank is resampled for fixed source runs
- 9586ed_: Fix two hexagonal lattice bugs
- a855e8_: Make sure graphite models don't error out on max events
- 7294a1_: Fix incorrect check on cmfd.xml
- 12f246_: Ensure number of realizations is written to statepoint
- 0227f4_: Fix bug when sampling multiple energy distributions
- 51deaa_: Prevent segfault when user specifies '18' on tally scores
- fed74b_: Prevent duplicate tally scores
- 8467ae_: Better threshold for allowable lost particles
- 493c6f_: Fix type of return argument for h5pget_driver_f

.. _70daa7: https://github.com/mit-crpg/openmc/commit/70daa7
.. _40b05f: https://github.com/mit-crpg/openmc/commit/40b05f
.. _9586ed: https://github.com/mit-crpg/openmc/commit/9586ed
.. _a855e8: https://github.com/mit-crpg/openmc/commit/a855e8
.. _7294a1: https://github.com/mit-crpg/openmc/commit/7294a1
.. _12f246: https://github.com/mit-crpg/openmc/commit/12f246
.. _0227f4: https://github.com/mit-crpg/openmc/commit/0227f4
.. _51deaa: https://github.com/mit-crpg/openmc/commit/51deaa
.. _fed74b: https://github.com/mit-crpg/openmc/commit/fed74b
.. _8467ae: https://github.com/mit-crpg/openmc/commit/8467ae
.. _493c6f: https://github.com/mit-crpg/openmc/commit/493c6f

------------
Contributors
------------

This release contains new contributions from the following people:

- `Will Boyd <wbinventor@gmail.com>`_
- `Derek Gaston <friedmud@gmail.com>`_
- `Sterling Harper <sterlingmharper@gmail.com>`_
- `Colin Josey <cjosey@mit.edu>`_
- `Jingang Liang <liangjg2008@gmail.com>`_
- `Adam Nelson <nelsonag@umich.edu>`_
- `Paul Romano <paul.k.romano@gmail.com>`_
- `Kelly Rowland <kellylynnerowland@gmail.com>`_
- `Sam Shaner <samuelshaner@gmail.com>`_
