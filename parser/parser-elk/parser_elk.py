from builtins import object
import setup_paths
import numpy as np
from nomadcore.simple_parser import mainFunction, AncillaryParser, CachingLevel
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from nomadcore.unit_conversion import unit_conversion
import os, sys, json, logging

class ElkContext(object):
    """context for elk parser"""

    def __init__(self):
        self.parser = None

    def initialize_values(self):
      """allows to reset values if the same superContext is used to parse different files"""
      self.metaInfoEnv = self.parser.parserBuilder.metaInfoEnv

    def startedParsing(self, path, parser):
      """called when parsing starts"""
      self.parser = parser
      # allows to reset values if the same superContext is used to parse different files
      self.initialize_values()

      self.enTot = []
      self.atom_pos = []
      self.atom_labels = []
      self.spinTreat = None

    def onClose_x_elk_section_lattice_vectors(self, backend, gIndex, section):
      latticeX = section["x_elk_geometry_lattice_vector_x"]
      latticeY = section["x_elk_geometry_lattice_vector_y"]
      latticeZ = section["x_elk_geometry_lattice_vector_z"]
      cell = np.array([[latticeX[0],latticeY[0],latticeZ[0]],
              [latticeX[1],latticeY[1],latticeZ[1]],
              [latticeX[2],latticeY[2],latticeZ[2]]])
#      print ("celll= ", latticeZ)
      backend.addArrayValues("simulation_cell", cell)

    def onClose_x_elk_section_reciprocal_lattice_vectors(self, backend, gIndex, section):
      recLatticeX = section["x_elk_geometry_reciprocal_lattice_vector_x"]
      recLatticeY = section["x_elk_geometry_reciprocal_lattice_vector_y"]
      recLatticeZ = section["x_elk_geometry_reciprocal_lattice_vector_z"]
      recCell = np.array([[recLatticeX[0],recLatticeY[0],recLatticeZ[0]],
              [recLatticeX[1],recLatticeY[1],recLatticeZ[1]],
              [recLatticeX[2],recLatticeY[2],recLatticeZ[2]]])
      backend.addArrayValues("x_elk_simulation_reciprocal_cell", recCell)

    def onClose_x_elk_section_xc(self, backend, gIndex, section):
      xcNr = section["x_elk_xc_functional"][0]
      xc_internal_map = {
        2: ['LDA_C_PZ', 'LDA_X_PZ'],
        3: ['LDA_C_PW', 'LDA_X_PZ'],
        4: ['LDA_C_XALPHA'],
        5: ['LDA_C_VBH'],
        20: ['GGA_C_PBE', 'GGA_X_PBE'],
        21: ['GGA_C_PBE', 'GGA_X_PBE_R'],
        22: ['GGA_C_PBE_SOL', 'GGA_X_PBE_SOL'],
        26: ['GGA_C_PBE', 'GGA_X_WC'],
        30: ['GGA_C_AM05', 'GGA_X_AM05']
        }
      for xcName in xc_internal_map[xcNr]:
        gi = backend.openSection("section_XC_functionals")
        backend.addValue("XC_functional_name", xcName)
        backend.closeSection("section_XC_functionals", gi)

    def onClose_section_single_configuration_calculation(self, backend, gIndex, section):
      dirPath = os.path.dirname(self.parser.fIn.name)
      dosFile = os.path.join(dirPath, "TDOS.OUT")
      eigvalFile = os.path.join(dirPath, "EIGVAL.OUT")
      if os.path.exists(dosFile):
        dosGIndex=backend.openSection("section_dos")
        with open(dosFile) as f:
            dosE=[]
            dosV=[]
            fromH = unit_conversion.convert_unit_function("hartree", "J")
            while True:
                line = f.readline()
                if not line: break
                nrs = list(map(float,line.split()))
                if len(nrs) == 2:
                    dosV.append(nrs[1])
                    dosE.append(fromH(nrs[0]))
                elif len(nrs) != 0:
                    raise Exception("Found more than two values in dos file %s" % dosFile)
            backend.addArrayValues("dos_values", np.asarray(dosV))
            backend.addArrayValues("dos_energies", np.asarray(dosE))
        backend.closeSection("section_dos", dosGIndex)
      if os.path.exists(eigvalFile):
        eigvalGIndex = backend.openSection("section_eigenvalues")
        with open(eigvalFile) as g:
            eigvalKpoint=[]
            eigvalVal=[]
            eigvalOcc=[]
            fromH = unit_conversion.convert_unit_function("hartree", "J")
            while 1:
              s = g.readline()
              if not s: break
              s = s.strip()
              if len(s) < 20:
                continue
              elif len(s) > 50:
                eigvalVal.append([])
                eigvalOcc.append([])
                eigvalKpoint.append(list(map(float, s.split()[1:4])))
              else:
                try: int(s[0])
                except ValueError:
                  continue
                else:
                  n, e, occ = s.split()
                  eigvalVal[-1].append(fromH(float(e)))
                  eigvalOcc[-1].append(float(occ))
            backend.addArrayValues("eigenvalues_kpoints", np.asarray(eigvalKpoint))
            backend.addArrayValues("eigenvalues_values", np.asarray([eigvalVal]))
            backend.addArrayValues("eigenvalues_occupation", np.asarray([eigvalOcc]))
            backend.closeSection("section_eigenvalues",eigvalGIndex)

      backend.addValue("energy_total", self.enTot[-1])

    def onClose_x_elk_section_spin(self, backend, gIndex, section):
#    pass
      spin = section["x_elk_spin_treatment"][0]
#    print("prima",len(spin))
      spin = spin.strip()
#    print("dopo",len(spin))
#      print("spin=",spin,"spin", type(spin))
      if spin == "spin-polarised":
#        print("Vero")
        self.spinTreat = True
      else:
#        print("Falso")
        self.spinTreat = False

    def onClose_section_system(self, backend, gIndex, section):
      backend.addArrayValues('configuration_periodic_dimensions', np.asarray([True, True, True]))
      self.secSystemDescriptionIndex = gIndex

#      atom_pos = []
#      for i in ['x', 'y', 'z']:
#         api = section['x_elk_geometry_atom_positions_' + i]
#         if api is not None:
#            atom_pos.append(api)
#      if atom_pos:
#         backend.addArrayValues('atom_positions', np.transpose(np.asarray(atom_pos)))
#      atom_labels = section['x_elk_geometry_atom_labels']
#      if atom_labels is not None:
#         backend.addArrayValues('atom_labels', np.asarray(atom_labels))

      if self.atom_pos:
         backend.addArrayValues('atom_positions', np.asarray(self.atom_pos))
      self.atom_pos = []
      if self.atom_labels is not None:
         backend.addArrayValues('atom_labels', np.asarray(self.atom_labels))
      self.atom_labels = []
#      print("self.atom_labels=",self.atom_labels)
    def onClose_x_elk_section_atoms_group(self, backend, gIndex, section):
      pos = [section['x_elk_geometry_atom_positions_' + i] for i in ['x', 'y', 'z']]
      pl = [len(comp) for comp in pos]
      natom = pl[0]
      if pl[1] != natom or pl[2] != natom:
        raise Exception("invalid number of atoms in various components %s" % pl)
      for i in range(natom):
        self.atom_pos.append([pos[0][i], pos[1][i], pos[2][i]])
      self.atom_labels = self.atom_labels + (section['x_elk_geometry_atom_labels'] * natom)

    def onClose_section_scf_iteration(self, backend, gIndex, section):
      Etot = section["energy_total_scf_iteration"]
      self.enTot.append(Etot[0])

# description of the input
mainFileDescription = \
    SM(name = "root matcher",
       startReStr = "",
       weak = True,
       subMatchers = [
         SM(name = "header",
         startReStr = r"\s*\|\s*Elk version\s*(?P<program_version>[-a-zA-Z0-9\.]+)\s*started\s*",
         fixedStartValues={'program_name': 'elk', 'program_basis_set_type': '(L)APW+lo' },
            sections = ["section_run", "section_method"],
         subMatchers = [
           SM(name = 'input',
              startReStr = r"\|\sGround-state run starting from atomic densities\s\|\s",
              endReStr = r"\|\sDensity and potential initialised from atomic data\s",
              sections = ['section_system'],
              subMatchers = [
                SM(startReStr = r"\s*Lattice vectors :",
                sections = ["x_elk_section_lattice_vectors"],
                subMatchers = [

    SM(startReStr = r"\s*(?P<x_elk_geometry_lattice_vector_x__bohr>[-+0-9.]+)\s+(?P<x_elk_geometry_lattice_vector_y__bohr>[-+0-9.]+)\s+(?P<x_elk_geometry_lattice_vector_z__bohr>[-+0-9.]+)", repeats = True)
                ]),
                SM(startReStr = r"Reciprocal lattice vectors :",
                sections = ["x_elk_section_reciprocal_lattice_vectors"],
                subMatchers = [

    SM(startReStr = r"\s*(?P<x_elk_geometry_reciprocal_lattice_vector_x__bohr_1>[-+0-9.]+)\s+(?P<x_elk_geometry_reciprocal_lattice_vector_y__bohr_1>[-+0-9.]+)\s+(?P<x_elk_geometry_reciprocal_lattice_vector_z__bohr_1>[-+0-9.]+)", repeats = True)
                ]),
    SM(r"\s*Unit cell volume\s*:\s*(?P<x_elk_unit_cell_volume__bohr3>[-0-9.]+)"),
    SM(r"\s*Brillouin zone volume\s*:\s*(?P<x_elk_brillouin_zone_volume__bohr_3>[-0-9.]+)"),
    SM(r"\s*Species\s*:\s*[0-9]\s*\((?P<x_elk_geometry_atom_labels>[-a-zA-Z0-9]+)\)", repeats = True,
      sections = ["x_elk_section_atoms_group"],
       subMatchers = [
#    SM(r"\s*muffin-tin radius\s*:\s*(?P<x_elk_muffin_tin_radius__bohr>[-0-9.]+)"),
#    SM(r"\s*number of radial points in muffin-tin\s*:\s*(?P<x_elk_muffin_tin_points>[-0-9.]+)"),
    SM(startReStr = r"\s*atomic positions\s*\(lattice\)\, magnetic fields \(Cartesian\)\s*:\s*",
      subMatchers = [
        SM(r"\s*(?P<x_elk_geometry_atom_number>[+0-9]+)\s*:\s*(?P<x_elk_geometry_atom_positions_x__bohr>[-+0-9.]+)\s*(?P<x_elk_geometry_atom_positions_y__bohr>[-+0-9.]+)\s*(?P<x_elk_geometry_atom_positions_z__bohr>[-+0-9.]+)", repeats = True)
      ])
    ]),
    SM(startReStr = r"\s*Spin treatment\s*:\s*",
      sections = ["x_elk_section_spin"],
        subMatchers = [
        SM(r"\s*(?P<x_elk_spin_treatment>[-a-zA-Z\s*]+)")
     ]),
    SM(r"\s*k-point grid\s*:\s*(?P<x_elk_number_kpoint_x>[-0-9.]+)\s+(?P<x_elk_number_kpoint_y>[-0-9.]+)\s+(?P<x_elk_number_kpoint_z>[-0-9.]+)"),
    SM(r"\s*k-point offset\s*:\s*(?P<x_elk_kpoint_offset_x>[-0-9.]+)\s+(?P<x_elk_kpoint_offset_y>[-0-9.]+)\s+(?P<x_elk_kpoint_offset_z>[-0-9.]+)"),
    SM(r"\s*Total number of k-points\s*:\s*(?P<x_elk_number_kpoints>[-0-9.]+)"),
    SM(r"\s*Muffin-tin radius times maximum \|G\+k\|\s*:\s*(?P<x_elk_rgkmax__bohr>[-0-9.]+)"),
    SM(r"\s*Maximum \|G\+k\| for APW functions\s*:\s*(?P<x_elk_gkmax__bohr_1>[-0-9.]+)"),
    SM(r"\s*Maximum \|G\| for potential and density\s*:\s*(?P<x_elk_gmaxvr__bohr_1>[-0-9.]+)"),
    SM(r"\s*G-vector grid sizes\s*:\s*(?P<x_elk_gvector_size_x>[-0-9.]+)\s+(?P<x_elk_gvector_size_y>[-0-9.]+)\s+(?P<x_elk_gvector_size_z>[-0-9.]+)"),
    SM(r"\s*Number of G-vectors\s*:\s*(?P<x_elk_gvector_total>[-0-9.]+)"),
    SM(startReStr = r"\s*Maximum angular momentum used for\s*",
        subMatchers = [
          SM(r"\s*APW functions\s*:\s*(?P<x_elk_lmaxapw>[-0-9.]+)")
        ]),
    SM(r"\s*Total nuclear charge\s*:\s*(?P<x_elk_nuclear_charge>[-0-9.]+)"),
    SM(r"\s*Total core charge\s*:\s*(?P<x_elk_core_charge>[-0-9.]+)"),
    SM(r"\s*Total valence charge\s*:\s*(?P<x_elk_valence_charge>[-0-9.]+)"),
    SM(r"\s*Total electronic charge\s*:\s*(?P<x_elk_electronic_charge>[-0-9.]+)"),
    SM(r"\s*Effective Wigner radius, r_s\s*:\s*(?P<x_elk_wigner_radius>[-0-9.]+)"),
    SM(r"\s*Number of empty states\s*:\s*(?P<x_elk_empty_states>[-0-9.]+)"),
    SM(r"\s*Total number of valence states\s*:\s*(?P<x_elk_valence_states>[-0-9.]+)"),
    SM(r"\s*Total number of core states\s*:\s*(?P<x_elk_core_states>[-0-9.]+)"),
    SM(r"\s*Total number of local-orbitals\s*:\s*(?P<x_elk_lo>[-0-9.]+)"),
    SM(r"\s*Smearing width\s*:\s*(?P<x_elk_smearing_width__hartree>[-0-9.]+)"),
    SM(startReStr = r"\s*Exchange-correlation functional\s*:\s*(?P<x_elk_xc_functional>[-0-9.]+)",
       sections = ['x_elk_section_xc'])
           ]),
            SM(name = "single configuration iteration",
              startReStr = r"\|\s*Self-consistent loop started\s*\|",
              sections = ["section_single_configuration_calculation"],
              repeats = True,
              subMatchers = [
                SM(name = "scfi totE",
                 startReStr =r"\|\s*Loop number\s*:",
                  sections = ["section_scf_iteration"],
                  repeats = True,
                  subMatchers = [
                   SM(r"\s*Fermi\s*:\s*(?P<x_elk_fermi_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*sum of eigenvalues\s*:\s*(?P<energy_sum_eigenvalues_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*electron kinetic\s*:\s*(?P<electronic_kinetic_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*core electron kinetic\s*:\s*(?P<x_elk_core_electron_kinetic_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*Coulomb\s*:\s*(?P<x_elk_coulomb_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*Coulomb potential\s*:\s*(?P<x_elk_coulomb_potential_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*nuclear-nuclear\s*:\s*(?P<x_elk_nuclear_nuclear_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*electron-nuclear\s*:\s*(?P<x_elk_electron_nuclear_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*Hartree\s*:\s*(?P<x_elk_hartree_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*Madelung\s*:\s*(?P<x_elk_madelung_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*xc potential\s*:\s*(?P<energy_XC_potential_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*exchange\s*:\s*(?P<x_elk_exchange_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*correlation\s*:\s*(?P<x_elk_correlation_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*electron entropic\s*:\s*(?P<x_elk_electron_entropic_energy_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*total energy\s*:\s*(?P<energy_total_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*Density of states at Fermi energy\s*:\s*(?P<x_elk_dos_fermi_scf_iteration__hartree_1>[-0-9.]+)"),
                   SM(r"\s*Estimated indirect band gap\s*:\s*(?P<x_elk_indirect_gap_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*Estimated direct band gap\s*:\s*(?P<x_elk_direct_gap_scf_iteration__hartree>[-0-9.]+)"),
                   SM(r"\s*core\s*:\s*(?P<x_elk_core_charge_scf_iteration>[-0-9.]+)"),
                   SM(r"\s*valence\s*:\s*(?P<x_elk_valence_charge_scf_iteration>[-0-9.]+)"),
                   SM(r"\s*interstitial\s*:\s*(?P<x_elk_interstitial_charge_scf_iteration>[-0-9.]+)"),
                  ]) #,
#                SM(name="final_quantities",
#                  startReStr = r"\sConvergence targets achieved\s*\+",
#                  endReStr = r"\| Self-consistent loop stopped\s*\|\+",
#                   subMatchers = [
#                   SM(r"\s*Fermi\s*:\s*(?P<x_elk_fermi_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*sum of eigenvalues\s*:\s*(?P<energy_sum_eigenvalues__hartree>[-0-9.]+)"),
#                   SM(r"\s*electron kinetic\s*:\s*(?P<electronic_kinetic_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*core electron kinetic\s*:\s*(?P<x_elk_core_electron_kinetic_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*Coulomb\s*:\s*(?P<x_elk_coulomb_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*Coulomb potential\s*:\s*(?P<x_elk_coulomb_potential_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*nuclear-nuclear\s*:\s*(?P<x_elk_nuclear_nuclear_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*electron-nuclear\s*:\s*(?P<x_elk_electron_nuclear_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*Hartree\s*:\s*(?P<x_elk_hartree_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*Madelung\s*:\s*(?P<x_elk_madelung_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*xc potential\s*:\s*(?P<energy_XC_potential__hartree>[-0-9.]+)"),
#                   SM(r"\s*exchange\s*:\s*(?P<x_elk_exchange_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*correlation\s*:\s*(?P<x_elk_correlation_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*electron entropic\s*:\s*(?P<x_elk_electron_entropic_energy__hartree>[-0-9.]+)"),
#                   SM(r"\s*total energy\s*:\s*(?P<energy_total__hartree>[-0-9.]+)"),
#                   SM(r"\s*Density of states at Fermi energy\s*:\s*(?P<x_elk_dos_fermi__hartree_1>[-0-9.]+)"),
#                   SM(r"\s*Estimated indirect band gap\s*:\s*(?P<x_elk_indirect_gap__hartree>[-0-9.]+)"),
#                   SM(r"\s*Estimated direct band gap\s*:\s*(?P<x_elk_direct_gap__hartree>[-0-9.]+)"),
#                   SM(r"\s*core\s*:\s*(?P<x_elk_core_charge_final>[-0-9.]+)"),
#                   SM(r"\s*valence\s*:\s*(?P<x_elk_valence_charge_final>[-0-9.]+)"),
#                   SM(r"\s*interstitial\s*:\s*(?P<x_elk_interstitial_charge_final>[-0-9.]+)")
#                   ])
               ]
            )
          ])
    ])

parserInfo = {
  "name": "Elk"
}

metaInfoPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../../nomad-meta-info/meta_info/nomad_meta_info/elk.nomadmetainfo.json"))
metaInfoEnv, warnings = loadJsonFile(filePath = metaInfoPath, dependencyLoader = None, extraArgsHandling = InfoKindEl.ADD_EXTRA_ARGS, uri = None)

cachingLevelForMetaName = {
                            "x_elk_geometry_lattice_vector_x":CachingLevel.Cache,
                            "x_elk_geometry_lattice_vector_y":CachingLevel.Cache,
                            "x_elk_geometry_lattice_vector_z":CachingLevel.Cache,
                            "x_elk_section_lattice_vectors": CachingLevel.Ignore,
                            "x_elk_geometry_reciprocal_lattice_vector_x":CachingLevel.Cache,
                            "x_elk_geometry_reciprocal_lattice_vector_y":CachingLevel.Cache,
                            "x_elk_geometry_reciprocal_lattice_vector_z":CachingLevel.Cache,
                            "x_elk_section_reciprocal_lattice_vectors": CachingLevel.Ignore
                          }

if __name__ == "__main__":
    superContext = ElkContext()
    mainFunction(mainFileDescription, metaInfoEnv, parserInfo, superContext = superContext)
