@module resolver
@target python

[resolve-dependencies]
PURPOSE: Resolve ANLU dependencies and return compilation order.
INPUTS:
  - nl_file: NLFile
LOGIC:
  1. result = ResolverResult()
  2. anlu_map = {anlu.identifier: anlu for anlu in nl_file.anlus}
  3. in_degree = {anlu.identifier: 0 for anlu in nl_file.anlus}
  4. unresolved = {anlu.identifier: len(anlu.depends) for anlu in nl_file.anlus}
  5. ready = [anlu for anlu in nl_file.anlus if not anlu.depends]
  6. resolved = set()
  7. unresolved_anlus = [a for a in nl_file.anlus if a.identifier not in resolved]
RETURNS: result

[success]
PURPOSE: Success operation
RETURNS: len(self.errors) == 0
