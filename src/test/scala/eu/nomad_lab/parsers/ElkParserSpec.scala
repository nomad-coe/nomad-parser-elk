package eu.nomad_lab.parsers

import org.specs2.mutable.Specification

object ElkTests extends Specification {
  "ElkParserTest" >> {
    "test with json-events GaAs" >> {
      ParserRun.parse(ElkParser, "parsers/elk/test/examples/GaAs/INFO.OUT", "json-events") must_== ParseResult.ParseSuccess
    }
    "test with json GaAs" >> {
      ParserRun.parse(ElkParser, "parsers/elk/test/examples/GaAs/INFO.OUT", "json") must_== ParseResult.ParseSuccess
    }
    "test with json-events Al" >> {
      ParserRun.parse(ElkParser, "parsers/elk/test/examples/Al/INFO.OUT", "json-events") must_== ParseResult.ParseSuccess
    }
    "test with json Al" >> {
      ParserRun.parse(ElkParser, "parsers/elk/test/examples/Al/INFO.OUT", "json") must_== ParseResult.ParseSuccess
    }
  }
}
