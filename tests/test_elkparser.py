#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest

from nomad.datamodel import EntryArchive
from elkparser import ElkParser


def approx(value, abs=0, rel=1e-6):
    return pytest.approx(value, abs=abs, rel=rel)


@pytest.fixture(scope='module')
def parser():
    return ElkParser()


def test_basic(parser):
    archive = EntryArchive()

    parser.parse('tests/data/Al/INFO.OUT', archive, None)

    sec_run = archive.section_run[0]
    assert sec_run.program_version == '4.0.15'

    sec_system = archive.section_run[0].section_system[0]
    assert sec_system.lattice_vectors[1][0].magnitude == approx(2.02500243e-10)
    assert sec_system.atom_labels == ['Al']
    assert sec_system.atom_positions[0][1].magnitude == 0.

    sec_sccs = sec_run.section_single_configuration_calculation
    assert len(sec_sccs) == 19
    assert sec_sccs[2].energy_total.magnitude == approx(-1.05555622e-15)
    assert sec_sccs[7].energy_reference_fermi[0].magnitude == approx(1.13675091e-18)
    assert sec_sccs[12].energy_X.magnitude == approx(-7.28319203e-17)


def test_2(parser):
    archive = EntryArchive()

    parser.parse('tests/data/GaAs/INFO.OUT', archive, None)

    sec_system = archive.section_run[0].section_system[0]
    assert sec_system.atom_labels == ['Ga', 'As']
    assert sec_system.atom_positions[1][2].magnitude == approx(1.41382921e-10)
