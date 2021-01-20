#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
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
import numpy as np            # pylint: disable=unused-import
import typing                 # pylint: disable=unused-import
from nomad.metainfo import (  # pylint: disable=unused-import
    MSection, MCategory, Category, Package, Quantity, Section, SubSection, SectionProxy,
    Reference
)
from nomad.metainfo.legacy import LegacyDefinition

from nomad.datamodel.metainfo import public

m_package = Package(
    name='elk_nomadmetainfo_json',
    description='None',
    a_legacy=LegacyDefinition(name='elk.nomadmetainfo.json'))


class x_elk_section_lattice_vectors(MSection):
    '''
    lattice vectors
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_elk_section_lattice_vectors'))

    x_elk_geometry_lattice_vector_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        x component of lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_lattice_vector_x'))

    x_elk_geometry_lattice_vector_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        y component of lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_lattice_vector_y'))

    x_elk_geometry_lattice_vector_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        z component of lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_lattice_vector_z'))


class x_elk_section_reciprocal_lattice_vectors(MSection):
    '''
    reciprocal lattice vectors
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_elk_section_reciprocal_lattice_vectors'))

    x_elk_geometry_reciprocal_lattice_vector_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='1 / meter',
        description='''
        x component of reciprocal lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_reciprocal_lattice_vector_x'))

    x_elk_geometry_reciprocal_lattice_vector_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='1 / meter',
        description='''
        y component of reciprocal lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_reciprocal_lattice_vector_y'))

    x_elk_geometry_reciprocal_lattice_vector_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='1 / meter',
        description='''
        z component of reciprocal lattice vector
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_reciprocal_lattice_vector_z'))


class x_elk_section_atoms_group(MSection):
    '''
    a group of atoms of the same type
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_elk_section_atoms_group'))

    x_elk_geometry_atom_labels = Quantity(
        type=str,
        shape=[],
        description='''
        labels of atom
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_atom_labels'))

    x_elk_geometry_atom_number = Quantity(
        type=str,
        shape=[],
        description='''
        number to identify the atoms of a species
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_atom_number'))

    x_elk_geometry_atom_positions_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        x component of atomic position
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_atom_positions_x'))

    x_elk_geometry_atom_positions_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        y component of atomic position
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_atom_positions_y'))

    x_elk_geometry_atom_positions_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        z component of atomic position
        ''',
        a_legacy=LegacyDefinition(name='x_elk_geometry_atom_positions_z'))


class x_elk_section_spin(MSection):
    '''
    section for exciting spin treatment
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_elk_section_spin'))

    x_elk_spin_treatment = Quantity(
        type=str,
        shape=[],
        description='''
        Spin treatment
        ''',
        a_legacy=LegacyDefinition(name='x_elk_spin_treatment'))


class x_elk_section_xc(MSection):
    '''
    index for elk functional
    '''

    m_def = Section(validate=False, a_legacy=LegacyDefinition(name='x_elk_section_xc'))

    x_elk_xc_functional = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        index for elk functional
        ''',
        a_legacy=LegacyDefinition(name='x_elk_xc_functional'))


class section_system(public.section_system):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_system'))

    x_elk_brillouin_zone_volume = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='1 / meter ** 3',
        description='''
        Brillouin zone volume
        ''',
        a_legacy=LegacyDefinition(name='x_elk_brillouin_zone_volume'))

    x_elk_simulation_reciprocal_cell = Quantity(
        type=np.dtype(np.float64),
        shape=[3, 3],
        unit='meter',
        description='''
        Reciprocal lattice vectors of the simulation cell.
        ''',
        categories=[public.configuration_core],
        a_legacy=LegacyDefinition(name='x_elk_simulation_reciprocal_cell'))

    x_elk_unit_cell_volume = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter ** 3',
        description='''
        unit cell volume
        ''',
        a_legacy=LegacyDefinition(name='x_elk_unit_cell_volume'))

    x_elk_muffin_tin_radius = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        muffin-tin radius
        ''',
        a_legacy=LegacyDefinition(name='x_elk_muffin_tin_radius'))

    x_elk_muffin_tin_points = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        muffin-tin points
        ''',
        a_legacy=LegacyDefinition(name='x_elk_muffin_tin_points'))

    x_elk_number_kpoint_x = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        number k-points x
        ''',
        a_legacy=LegacyDefinition(name='x_elk_number_kpoint_x'))

    x_elk_number_kpoint_y = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        number k-points y
        ''',
        a_legacy=LegacyDefinition(name='x_elk_number_kpoint_y'))

    x_elk_number_kpoint_z = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        number k-points z
        ''',
        a_legacy=LegacyDefinition(name='x_elk_number_kpoint_z'))

    x_elk_number_kpoints = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        number k-points
        ''',
        a_legacy=LegacyDefinition(name='x_elk_number_kpoints'))

    x_elk_kpoint_offset_x = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        K-points offset x component
        ''',
        a_legacy=LegacyDefinition(name='x_elk_kpoint_offset_x'))

    x_elk_kpoint_offset_y = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        K-points offset y component
        ''',
        a_legacy=LegacyDefinition(name='x_elk_kpoint_offset_y'))

    x_elk_kpoint_offset_z = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        K-points offset z component
        ''',
        a_legacy=LegacyDefinition(name='x_elk_kpoint_offset_z'))

    x_elk_rgkmax = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        Radius MT * Gmax
        ''',
        a_legacy=LegacyDefinition(name='x_elk_rgkmax'))

    x_elk_gvector_size_x = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        G-vector grid size x
        ''',
        a_legacy=LegacyDefinition(name='x_elk_gvector_size_x'))

    x_elk_gvector_size_y = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        G-vector grid size y
        ''',
        a_legacy=LegacyDefinition(name='x_elk_gvector_size_y'))

    x_elk_gvector_size_z = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        G-vector grid size z
        ''',
        a_legacy=LegacyDefinition(name='x_elk_gvector_size_z'))

    x_elk_gvector_total = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        G-vector total
        ''',
        a_legacy=LegacyDefinition(name='x_elk_gvector_total'))

    x_elk_lmaxapw = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Angular momentum cut-off for the APW functions
        ''',
        a_legacy=LegacyDefinition(name='x_elk_lmaxapw'))

    x_elk_gkmax = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='1 / meter',
        description='''
        Maximum length of |G+k| for APW functions
        ''',
        a_legacy=LegacyDefinition(name='x_elk_gkmax'))

    x_elk_smearing_width = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Smearing width for KS occupancies
        ''',
        a_legacy=LegacyDefinition(name='x_elk_smearing_width'))

    x_elk_lo = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Total number of local-orbitals
        ''',
        a_legacy=LegacyDefinition(name='x_elk_lo'))

    x_elk_gmaxvr = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='1 / meter',
        description='''
        Maximum length of |G|
        ''',
        a_legacy=LegacyDefinition(name='x_elk_gmaxvr'))

    x_elk_valence_states = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Total number of valence states
        ''',
        a_legacy=LegacyDefinition(name='x_elk_valence_states'))

    x_elk_core_states = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Total number of core states
        ''',
        a_legacy=LegacyDefinition(name='x_elk_core_states'))

    x_elk_empty_states = Quantity(
        type=np.dtype(np.int32),
        shape=[],
        description='''
        Number of empty states
        ''',
        a_legacy=LegacyDefinition(name='x_elk_empty_states'))

    x_elk_wigner_radius = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='meter',
        description='''
        Effective Wigner radius
        ''',
        a_legacy=LegacyDefinition(name='x_elk_wigner_radius'))

    x_elk_electronic_charge = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Electronic charge
        ''',
        a_legacy=LegacyDefinition(name='x_elk_electronic_charge'))

    x_elk_valence_charge = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Valence charge
        ''',
        a_legacy=LegacyDefinition(name='x_elk_valence_charge'))

    x_elk_nuclear_charge = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Nuclear charge
        ''',
        a_legacy=LegacyDefinition(name='x_elk_nuclear_charge'))

    x_elk_core_charge = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Core charge
        ''',
        a_legacy=LegacyDefinition(name='x_elk_core_charge'))

    x_elk_section_lattice_vectors = SubSection(
        sub_section=SectionProxy('x_elk_section_lattice_vectors'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_elk_section_lattice_vectors'))

    x_elk_section_reciprocal_lattice_vectors = SubSection(
        sub_section=SectionProxy('x_elk_section_reciprocal_lattice_vectors'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_elk_section_reciprocal_lattice_vectors'))

    x_elk_section_atoms_group = SubSection(
        sub_section=SectionProxy('x_elk_section_atoms_group'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_elk_section_atoms_group'))

    x_elk_section_spin = SubSection(
        sub_section=SectionProxy('x_elk_section_spin'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_elk_section_spin'))

    x_elk_section_xc = SubSection(
        sub_section=SectionProxy('x_elk_section_xc'),
        repeats=True,
        a_legacy=LegacyDefinition(name='x_elk_section_xc'))


class section_scf_iteration(public.section_scf_iteration):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_scf_iteration'))

    x_elk_core_charge_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Core charge scf iteration
        ''',
        a_legacy=LegacyDefinition(name='x_elk_core_charge_scf_iteration'))

    x_elk_valence_charge_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Valence charge scf iteration
        ''',
        a_legacy=LegacyDefinition(name='x_elk_valence_charge_scf_iteration'))

    x_elk_interstitial_charge_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Interstitial charge scf iteration
        ''',
        a_legacy=LegacyDefinition(name='x_elk_interstitial_charge_scf_iteration'))

    x_elk_fermi_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Fermi energy
        ''',
        a_legacy=LegacyDefinition(name='x_elk_fermi_energy_scf_iteration'))

    x_elk_core_electron_kinetic_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Core-electron kinetic energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_core_electron_kinetic_energy_scf_iteration'))

    x_elk_coulomb_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Coulomb energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_coulomb_energy_scf_iteration'))

    x_elk_coulomb_potential_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Coulomb potential energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_coulomb_potential_energy_scf_iteration'))

    x_elk_nuclear_nuclear_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Nuclear-nuclear energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_nuclear_nuclear_energy_scf_iteration'))

    x_elk_electron_nuclear_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Electron-nuclear energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_electron_nuclear_energy_scf_iteration'))

    x_elk_hartree_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Hartree energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_hartree_energy_scf_iteration'))

    x_elk_madelung_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Madelung energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_madelung_energy_scf_iteration'))

    x_elk_exchange_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Exchange energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_exchange_energy_scf_iteration'))

    x_elk_correlation_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Correlation energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_correlation_energy_scf_iteration'))

    x_elk_electron_entropic_energy_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Electron entropic energy
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_electron_entropic_energy_scf_iteration'))

    x_elk_dos_fermi_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='1 / joule',
        description='''
        DOS at Fermi energy
        ''',
        a_legacy=LegacyDefinition(name='x_elk_dos_fermi_scf_iteration'))

    x_elk_direct_gap_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Estimated fundamental direct gap
        ''',
        a_legacy=LegacyDefinition(name='x_elk_direct_gap_scf_iteration'))

    x_elk_indirect_gap_scf_iteration = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Estimated fundamental indirect gap
        ''',
        a_legacy=LegacyDefinition(name='x_elk_indirect_gap_scf_iteration'))


class section_single_configuration_calculation(public.section_single_configuration_calculation):

    m_def = Section(validate=False, extends_base_section=True, a_legacy=LegacyDefinition(name='section_single_configuration_calculation'))

    x_elk_core_charge_final = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Core charge final
        ''',
        a_legacy=LegacyDefinition(name='x_elk_core_charge_final'))

    x_elk_valence_charge_final = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Valence charge final
        ''',
        a_legacy=LegacyDefinition(name='x_elk_valence_charge_final'))

    x_elk_interstitial_charge_final = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        description='''
        Interstitial charge final
        ''',
        a_legacy=LegacyDefinition(name='x_elk_interstitial_charge_final'))

    x_elk_fermi_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Fermi energy final
        ''',
        a_legacy=LegacyDefinition(name='x_elk_fermi_energy'))

    x_elk_core_electron_kinetic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Core-electron kinetic energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_core_electron_kinetic_energy'))

    x_elk_coulomb_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Coulomb energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_coulomb_energy'))

    x_elk_coulomb_potential_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Coulomb potential energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_coulomb_potential_energy'))

    x_elk_nuclear_nuclear_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Nuclear-nuclear energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_nuclear_nuclear_energy'))

    x_elk_electron_nuclear_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Electron-nuclear energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_electron_nuclear_energy'))

    x_elk_hartree_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Hartree energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_hartree_energy'))

    x_elk_madelung_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Madelung energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_madelung_energy'))

    x_elk_exchange_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Exchange energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_exchange_energy'))

    x_elk_correlation_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Correlation energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_correlation_energy'))

    x_elk_electron_entropic_energy = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Electron entropic energy final
        ''',
        categories=[public.energy_value, public.energy_component],
        a_legacy=LegacyDefinition(name='x_elk_electron_entropic_energy'))

    x_elk_dos_fermi = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='1 / joule',
        description='''
        DOS at Fermi energy
        ''',
        a_legacy=LegacyDefinition(name='x_elk_dos_fermi'))

    x_elk_direct_gap = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Estimated fundamental direct gap final
        ''',
        a_legacy=LegacyDefinition(name='x_elk_direct_gap'))

    x_elk_indirect_gap = Quantity(
        type=np.dtype(np.float64),
        shape=[],
        unit='joule',
        description='''
        Estimated fundamental indirect gap final
        ''',
        a_legacy=LegacyDefinition(name='x_elk_indirect_gap'))


m_package.__init_metainfo__()
