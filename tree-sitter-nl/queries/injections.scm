; =============================================================================
; Tree-sitter Language Injection for NL (Natural Language Source)
;
; Enables syntax highlighting within @literal blocks based on language tag.
; =============================================================================

; Inject language into @literal blocks based on the language identifier
; Example: @literal python { ... } injects Python highlighting

((literal_block
  (literal_header
    language: (identifier) @injection.language)
  (literal_content) @injection.content))

; Specific language injections for common targets

; Python injection
((literal_block
  (literal_header
    language: (identifier) @_lang)
  (literal_content) @injection.content)
  (#eq? @_lang "python")
  (#set! injection.language "python"))

; TypeScript injection
((literal_block
  (literal_header
    language: (identifier) @_lang)
  (literal_content) @injection.content)
  (#eq? @_lang "typescript")
  (#set! injection.language "typescript"))

; JavaScript injection
((literal_block
  (literal_header
    language: (identifier) @_lang)
  (literal_content) @injection.content)
  (#eq? @_lang "javascript")
  (#set! injection.language "javascript"))

; Rust injection
((literal_block
  (literal_header
    language: (identifier) @_lang)
  (literal_content) @injection.content)
  (#eq? @_lang "rust")
  (#set! injection.language "rust"))

; SQL injection
((literal_block
  (literal_header
    language: (identifier) @_lang)
  (literal_content) @injection.content)
  (#eq? @_lang "sql")
  (#set! injection.language "sql"))
