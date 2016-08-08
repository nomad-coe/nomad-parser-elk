package eu.nomad_lab.parsers

import org.specs2.mutable.Specification

object ElkTests extends Specification {
  "ElkParserTest" >> {
    "test with json-events" >> {
      ParserRun.parse(ElkParser, "parsers/elk/test/examples/ok/ok.scf", "json-events") must_== ParseResult.ParseSuccess
    }
    "test with json" >> {
      ParserRun.parse(ElkParser, "parsers/elk/test/examples/ok/ok.scf", "json") must_== ParseResult.ParseSuccess
    }
  }
}
