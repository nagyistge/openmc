#!/usr/bin/env python

import glob
import os
import sys

import pandas as pd

sys.path.insert(0, os.pardir)
from testing_harness import PyAPITestHarness
import openmc

class DiffTallyTestHarness(PyAPITestHarness):
    def _build_inputs(self):
        # Build default materials/geometry
        self._input_set.build_default_materials_and_geometry()

        # Set settings explicitly
        self._input_set.settings.batches = 3
        self._input_set.settings.inactive = 0
        self._input_set.settings.particles = 100
        self._input_set.settings.source = openmc.Source(space=openmc.stats.Box(
            [-160, -160, -183], [160, 160, 183]))
        self._input_set.settings.temperature['multipole'] = True

        self._input_set.tallies = openmc.Tallies()

        filt_mats = openmc.MaterialFilter((1, 3))
        filt_eout = openmc.EnergyoutFilter((0.0, 0.625, 20.0e6))

        # We want density derivatives for both water and fuel to get coverage
        # for both fissile and non-fissile materials.
        d1 = openmc.TallyDerivative(derivative_id=1)
        d1.variable = 'density'
        d1.material = 3
        d2 = openmc.TallyDerivative(derivative_id=2)
        d2.variable = 'density'
        d2.material = 1

        # O-16 is a good nuclide to test against because it is present in both
        # water and fuel.  Some routines need to recognize that they have the
        # perturbed nuclide but not the perturbed material.
        d3 = openmc.TallyDerivative(derivative_id=3)
        d3.variable = 'nuclide_density'
        d3.material = 1
        d3.nuclide = 'O16'

        # A fissile nuclide, just for good measure.
        d4 = openmc.TallyDerivative(derivative_id=4)
        d4.variable = 'nuclide_density'
        d4.material = 1
        d4.nuclide = 'U235'

        # Temperature derivatives.
        d5 = openmc.TallyDerivative(derivative_id=5)
        d5.variable = 'temperature'
        d5.material = 1

        derivs = [d1, d2, d3, d4, d5]

        # Cover the flux score.
        for i in range(5):
            t = openmc.Tally()
            t.add_score('flux')
            t.add_filter(filt_mats)
            t.derivative = derivs[i]
            self._input_set.tallies.append(t)

        # Cover supported scores with a collision estimator.
        for i in range(5):
            t = openmc.Tally()
            t.add_score('total')
            t.add_score('absorption')
            t.add_score('scatter')
            t.add_score('fission')
            t.add_score('nu-fission')
            t.add_filter(filt_mats)
            t.add_nuclide('total')
            t.add_nuclide('U235')
            t.derivative = derivs[i]
            self._input_set.tallies.append(t)

        # Cover an analog estimator.
        for i in range(5):
            t = openmc.Tally()
            t.add_score('absorption')
            t.add_filter(filt_mats)
            t.estimator = 'analog'
            t.derivative = derivs[i]
            self._input_set.tallies.append(t)

        # Energyout filter and total nuclide for the density derivatives.
        for i in range(2):
            t = openmc.Tally()
            t.add_score('nu-fission')
            t.add_score('scatter')
            t.add_filter(filt_mats)
            t.add_filter(filt_eout)
            t.add_nuclide('total')
            t.add_nuclide('U235')
            t.derivative = derivs[i]
            self._input_set.tallies.append(t)

        # Energyout filter without total nuclide for other derivatives.
        for i in range(2, 5):
            t = openmc.Tally()
            t.add_score('nu-fission')
            t.add_score('scatter')
            t.add_filter(filt_mats)
            t.add_filter(filt_eout)
            t.add_nuclide('U235')
            t.derivative = derivs[i]
            self._input_set.tallies.append(t)

        self._input_set.export()

    def _get_results(self):
        # Read the statepoint and summary files.
        statepoint = glob.glob(os.path.join(os.getcwd(), self._sp_name))[0]
        sp = openmc.StatePoint(statepoint)

        # Extract the tally data as a Pandas DataFrame.
        df = pd.DataFrame()
        for t in sp.tallies.values():
            df = df.append(t.get_pandas_dataframe(), ignore_index=True)

        # Extract the relevant data as a CSV string.
        cols = ('d_material', 'd_nuclide', 'd_variable', 'score', 'mean',
                'std. dev.')
        return df.to_csv(None, columns=cols, index=False, float_format='%.7e')


if __name__ == '__main__':
    harness = DiffTallyTestHarness('statepoint.3.h5', True)
    harness.main()
