@module lockfile
@target python

[hash-content]
PURPOSE: Generate SHA256 hash of content
INPUTS:
  - content: string
RETURNS: string

[hash-anlu]
PURPOSE: Generate deterministic hash of an ANLU
INPUTS:
  - anlu: ANLU
LOGIC:
  1. canonical = f'{anlu.identifier}|{anlu.purpose}|{anlu.returns}'
RETURNS: hash_content(canonical)

[generate-lockfile]
PURPOSE: Generate a lockfile for a compilation.
INPUTS:
  - nl_file: NLFile
  - generated_code: string
  - output_path: string
  - llm_backend: string
LOGIC:
  1. lockfile = Lockfile(llm_backend=llm_backend)
  2. output_lines = generated_code.count('\n') + 1
RETURNS: lockfile

[write-lockfile]
PURPOSE: Write lockfile to disk as YAML-like format
INPUTS:
  - lockfile: Lockfile
  - path: Path
RETURNS: void

[read-lockfile]
PURPOSE: Read an existing lockfile (simple YAML-like parser)
INPUTS:
  - path: Path
LOGIC:
  1. content = path.read_text(encoding='utf-8')
  2. lockfile = Lockfile()
  3. current_module = None
  4. current_anlu = None
RETURNS: lockfile

[verify-lockfile]
PURPOSE: Verify that a lockfile matches current sources.
INPUTS:
  - lockfile: Lockfile
  - nl_file: NLFile
LOGIC:
  1. errors = []
  2. mod_lock = lockfile.modules.get(nl_file.module.name)
RETURNS: errors
