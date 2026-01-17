; =============================================================================
; Tree-sitter Syntax Highlighting for NL (Natural Language Source)
;
; This file defines semantic highlighting for .nl files.
; Compatible with editors: VS Code, Neovim, Helix, Zed, etc.
; =============================================================================

; -----------------------------------------------------------------------------
; COMMENTS
; -----------------------------------------------------------------------------
(comment) @comment.line

; -----------------------------------------------------------------------------
; DIRECTIVES
; -----------------------------------------------------------------------------
(module_directive "@module" @keyword.directive)
(version_directive "@version" @keyword.directive)
(target_directive "@target" @keyword.directive)
(imports_directive "@imports" @keyword.directive)

; Directive values
(module_directive name: (identifier) @namespace)
(version_directive version: (version_string) @string.special)
(target_directive target: (target_name) @constant.builtin)
(imports_directive imports: (import_list (identifier) @namespace))

; -----------------------------------------------------------------------------
; ANLU BLOCK
; -----------------------------------------------------------------------------
(anlu_header "[" @punctuation.bracket)
(anlu_header "]" @punctuation.bracket)
(anlu_header name: (anlu_identifier) @function.definition)

; Section keywords (PURPOSE:, INPUTS:, GUARDS:, etc.)
(section_keyword) @keyword

; PURPOSE section
(purpose_section description: (description_text) @string)

; -----------------------------------------------------------------------------
; INPUTS SECTION
; -----------------------------------------------------------------------------
(input_item
  (bullet) @punctuation.special
  name: (identifier) @variable.parameter
  ":" @punctuation.delimiter
  type: (type_spec) @type)

(input_constraints
  "," @punctuation.delimiter)

; Constraint keywords
"required" @keyword.modifier
"optional" @keyword.modifier

; -----------------------------------------------------------------------------
; GUARDS SECTION
; -----------------------------------------------------------------------------
(guard_item
  (bullet) @punctuation.special
  condition: (guard_text) @string)

(guard_item (arrow) @operator)

(error_call
  type: (identifier) @type.exception
  "(" @punctuation.bracket
  ")" @punctuation.bracket)

(error_call (error_args (identifier) @constant))
(error_call (error_args (quoted_string) @string))

(error_text) @string

; -----------------------------------------------------------------------------
; LOGIC SECTION
; -----------------------------------------------------------------------------
(logic_item number: (step_number) @number)
(logic_item "." @punctuation.delimiter)

(state_prefix "[" @punctuation.bracket)
(state_prefix "]" @punctuation.bracket)
(state_prefix state: (state_name) @label)

(condition_prefix (keyword) @keyword.conditional)
(condition_token) @variable

(step_text) @string

(output_binding (arrow) @operator)
(output_binding variable: (identifier) @variable)

; -----------------------------------------------------------------------------
; RETURNS SECTION
; -----------------------------------------------------------------------------
(returns_section value: (returns_text) @string)

; -----------------------------------------------------------------------------
; DEPENDS SECTION
; -----------------------------------------------------------------------------
(depends_list (anlu_reference (anlu_identifier) @function))

; -----------------------------------------------------------------------------
; EDGE CASES SECTION
; -----------------------------------------------------------------------------
(edge_case_item
  (bullet) @punctuation.special
  condition: (edge_condition_text) @string
  (arrow) @operator
  behavior: (edge_behavior_text) @string)

; -----------------------------------------------------------------------------
; TYPE BLOCK
; -----------------------------------------------------------------------------
"@type" @keyword.type

(type_header
  name: (type_name) @type.definition
  "{" @punctuation.bracket)

(extends_clause "extends" @keyword)
(extends_clause base: (type_name) @type)

(type_field
  name: (identifier) @property
  ":" @punctuation.delimiter
  type: (type_spec) @type)

(field_constraints "," @punctuation.delimiter)

(type_close "}" @punctuation.bracket)

; -----------------------------------------------------------------------------
; TEST BLOCK
; -----------------------------------------------------------------------------
"@test" @keyword.test

(test_header
  "[" @punctuation.bracket
  anlu: (anlu_identifier) @function
  "]" @punctuation.bracket
  "{" @punctuation.bracket)

(test_assertion
  call: (test_call) @function.call
  "==" @operator
  expected: (test_value) @constant)

(test_call
  function: (identifier) @function
  "(" @punctuation.bracket
  ")" @punctuation.bracket)

(test_args "," @punctuation.delimiter)

(test_close "}" @punctuation.bracket)

; -----------------------------------------------------------------------------
; LITERAL BLOCK
; -----------------------------------------------------------------------------
"@literal" @keyword.directive

(literal_header
  language: (identifier) @tag
  "{" @punctuation.bracket)

(literal_content) @string.special

(literal_close "}" @punctuation.bracket)

; -----------------------------------------------------------------------------
; TYPE SYSTEM
; -----------------------------------------------------------------------------
(primitive_type) @type.builtin
(list_type "list" @type.builtin "of" @keyword)
(map_type "map" @type.builtin "of" @keyword "to" @keyword)
"?" @operator
(custom_type (type_name) @type)

; -----------------------------------------------------------------------------
; LITERALS
; -----------------------------------------------------------------------------
(number) @number
(quoted_string) @string
(boolean) @constant.builtin.boolean

; -----------------------------------------------------------------------------
; PUNCTUATION
; -----------------------------------------------------------------------------
(bullet) @punctuation.special
(arrow) @operator

; -----------------------------------------------------------------------------
; IDENTIFIERS (fallback)
; -----------------------------------------------------------------------------
(identifier) @variable
