# Copyright 2018-2020 Xanadu Quantum Technologies Inc.

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
Unit tests for the :mod:`pauli_group`  functions in ``grouping/pauli_group.py``.
"""
import pytest
from pennylane import Identity, PauliX, PauliY, PauliZ

import numpy as np

from pennylane.grouping.pauli_group import (
    pauli_group,
    pauli_group_generator,
    pauli_mult,
    pauli_mult_with_phase,
)


class TestPauliGroup:
    """Testing for Pauli group construction and manipulation functions."""

    @pytest.mark.parametrize(
        "pauli_word_1,pauli_word_2,wire_map,expected_product",
        [
            (PauliX(0), Identity(0), {0: 0}, PauliX(0)),
            (PauliZ(0), PauliY(0), {0: 0}, PauliX(0)),
            (PauliZ(0) @ PauliY(1), PauliX(0) @ PauliZ(1), {0: 0, 1: 1}, PauliY(0) @ PauliX(1)),
            # (PauliZ(1) @ PauliY(0), PauliX(0) @ PauliZ(1), {0: 0, 1: 1}, PauliX(1) @ PauliY(0)),
            (PauliZ("a"), PauliX("b"), {"a": 0, "b": 1}, PauliZ("a") @ PauliX("b")),
            (
                PauliZ("a"),
                PauliX("e"),
                {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4},
                PauliZ("a") @ PauliX("e"),
            ),
        ],
    )
    def test_pauli_mult(self, pauli_word_1, pauli_word_2, wire_map, expected_product):
        """Test that Pauli words are multiplied together correctly."""
        obtained_product = pauli_mult(pauli_word_1, pauli_word_2, wire_map=wire_map)
        assert obtained_product.compare(expected_product)

    @pytest.mark.parametrize(
        "pauli_word_1,pauli_word_2,wire_map,expected_phase",
        [
            (PauliX(0), Identity(0), {0: 0}, 1),
            (PauliZ(0), PauliY(0), {0: 0}, -1j),
            (PauliZ("a") @ PauliY("b"), PauliX("a") @ PauliZ("b"), {"a": 0, "b": 1}, -1),
            (PauliX(0) @ PauliY(1) @ PauliZ(2), PauliY(0) @ PauliY(1), {0: 0, 1: 1, 2: 2}, 1j),
        ],
    )
    def test_pauli_mult_with_phase(self, pauli_word_1, pauli_word_2, wire_map, expected_phase):
        """Test that multiplication including phases works as expected."""
        _, obtained_phase = pauli_mult_with_phase(pauli_word_1, pauli_word_2, wire_map=wire_map)
        assert obtained_phase == expected_phase
