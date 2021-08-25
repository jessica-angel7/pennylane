# Copyright 2018-2021 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for generating basis set default parameters.
"""
# pylint: disable=no-self-use
import pytest
from pennylane import numpy as np
from basis_set import BasisFunction, atom_basis_data, mol_basis_data

basis_data_H = [
    (
        "sto-3g",
        "H",
        1,
        [(0, 0, 0)],
        [0.3425250914e01, 0.6239137298e00, 0.1688554040e00],
        [0.1543289673e00, 0.5353281423e00, 0.4446345422e00],
        [0.0000000000e00, 0.0000000000e00, -0.694349000e00],
    )
]


class TestBasis:
    """Tests for generating basis set default parameters"""

    @pytest.mark.parametrize("basis_data", basis_data_H)
    def test_basisfunction(self, basis_data):
        """Test that BasisFunction class creates basis function objects correctly."""
        _, _, _, l, alpha, coeff, rgaus = basis_data

        basis_function = BasisFunction(l, alpha, coeff, rgaus)

        assert np.allclose(np.array(basis_function.alpha), np.array(alpha))
        assert np.allclose(np.array(basis_function.coeff), np.array(coeff))
        assert np.allclose(np.array(basis_function.rgaus), np.array(rgaus))

        assert np.allclose(basis_function.params[0], alpha)
        assert np.allclose(basis_function.params[1], coeff)
        assert np.allclose(basis_function.params[2], rgaus)

    @pytest.mark.parametrize("basis_data", basis_data_H)
    def test_atom_basis_data(self, basis_data):
        """Test that correct basis set parameters are generated for a given atom."""
        basis, symbol, _, l, alpha, coeff, _ = basis_data
        params = atom_basis_data(basis, symbol)[0]

        assert np.allclose(params[0], l)
        assert np.allclose(params[1], alpha)
        assert np.allclose(params[2], coeff)

    basis_data_HF = [
        (
            "sto-3g",
            ["H", "F"],
            [1, 5],
            (
                (
                    (0, 0, 0),
                    [0.3425250914E+01, 0.6239137298E+00, 0.1688554040E+00],
                    [0.1543289673E+00, 0.5353281423E+00, 0.4446345422E+00],
                ),
                (
                    (0, 0, 0),
                    [0.1666791340E+03, 0.3036081233E+02, 0.8216820672E+01],
                    [0.1543289673E+00, 0.5353281423E+00, 0.4446345422E+00],
                ),
                (
                    (0, 0, 0),
                    [0.6464803249E+01, 0.1502281245E+01, 0.4885884864E+00],
                    [-0.9996722919E-01, 0.3995128261E+00, 0.7001154689E+00],
                ),
                (
                    (1, 0, 0),
                    [0.6464803249E+01, 0.1502281245E+01, 0.4885884864E+00],
                    [0.1559162750E+00, 0.6076837186E+00, 0.3919573931E+00],
                ),
                (
                    (0, 1, 0),
                    [0.6464803249E+01, 0.1502281245E+01, 0.4885884864E+00],
                    [0.1559162750E+00, 0.6076837186E+00, 0.3919573931E+00],
                ),
                (
                    (0, 0, 1),
                    [0.6464803249E+01, 0.1502281245E+01, 0.4885884864E+00],
                    [0.1559162750E+00, 0.6076837186E+00, 0.3919573931E+00],
                ),
            ),
        )
    ]

    @pytest.mark.parametrize("basis_data", basis_data_HF)
    def test_mol_basis_data(self, basis_data):
        """Test that correct basis set parameters are generated for a given molecule represented as
        a list of atom."""
        basis, symbols, n_ref, params_ref = basis_data
        n_basis, params = mol_basis_data(basis, symbols)

        assert n_basis == n_ref

        assert np.allclose(params, params_ref)
