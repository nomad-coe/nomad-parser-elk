from builtins import object
import setup_paths
import numpy as np
from nomadcore.simple_parser import mainFunction, AncillaryParser, CachingLevel
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
import os, sys, json

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

    def onClose_x_elk_section_lattice_vectors(self, backend, gIndex, section):
      latticeX = section["x_elk_geometry_lattice_vector_x"]
      latticeY = section["x_elk_geometry_lattice_vector_y"]
      latticeZ = section["x_elk_geometry_lattice_vector_z"]
      cell = [[latticeX[0],latticeY[0],latticeZ[0]],
              [latticeX[1],latticeY[1],latticeZ[1]],
              [latticeX[2],latticeY[2],latticeZ[2]]]
      backend.addValue("simulation_cell", cell)

    def onClose_x_elk_section_reciprocal_lattice_vectors(self, backend, gIndex, section):
      recLatticeX = section["x_elk_geometry_reciprocal_lattice_vector_x"]
      recLatticeY = section["x_elk_geometry_reciprocal_lattice_vector_y"]
      recLatticeZ = section["x_elk_geometry_reciprocal_lattice_vector_z"]
      recCell = [[recLatticeX[0],recLatticeY[0],recLatticeZ[0]],
              [recLatticeX[1],recLatticeY[1],recLatticeZ[1]],
              [recLatticeX[2],recLatticeY[2],recLatticeZ[2]]]
      backend.addValue("x_elk_simulation_reciprocal_cell", recCell)

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
    SM(r"\s*Brillouin zone volume\s*:\s*(?P<x_elk_brillouin_zone_volume__bohr_3>[-0-9.]+)")
           ] )
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
