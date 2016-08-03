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

# description of the input
mainFileDescription = \
    SM(name = "root matcher",
       startReStr = "",
       weak = True,
       subMatchers = [
         SM(name = "header",
         startReStr = r"\s*\|\s*Elk version\s*(?P<program_version>[-a-zA-Z0-9]+)\s*started\s*=",
         fixedStartValues={'program_name': 'elk', 'program_basis_set_type': '(L)APW+lo' },
            sections = ["section_run", "section_method"],
         subMatchers = [
           SM(name = 'input',
              startReStr = r"\|\sGroundi\-state run starting from atomic densities\s\|\s",
              endReStr = r"\|\sDensity and potential initialised from atomic data\s",
              sections = ['section_system'],
              subMatchers = [
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

if __name__ == "__main__":
    superContext = ElkContext()
    mainFunction(mainFileDescription, metaInfoEnv, parserInfo, superContext = superContext)
