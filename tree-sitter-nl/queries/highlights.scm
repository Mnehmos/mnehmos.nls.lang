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

; Section headers
(section_header) @keyword

; PURPOSE section
(purpose_section description: (text_line) @string)

; -----------------------------------------------------------------------------
; INPUTS SECTION
; -----------------------------------------------------------------------------
(input_item
  (bullet) @punctuation.special
  name: (identifier) @variable.parameter
  ":" @punctuation.delimiter
  type: (type_spec) @type)

(input_constraints
  "," @punctuation.delimiter
  "required" @keyword.modifier
  "optional" @keyword.modifier)

; -----------------------------------------------------------------------------
; GUARDS SECTION
; -----------------------------------------------------------------------------
(guard_item
  (bullet) @punctuation.special
  condition: (guard_condition) @string)

(guard_item (arrow) @operator)

(error_call
  type: (identifier) @type.exception
  "(" @punctuation.bracket
  ")" @punctuation.bracket)

(error_call (error_args (identifier) @constant))
(error_call (error_args (quoted_string) @string))

; -----------------------------------------------------------------------------
; LOGIC SECTION
; -----------------------------------------------------------------------------
(logic_item number: (step_number) @number)
(logic_item "." @punctuation.delimiter)

(state_prefix "[" @punctuation.bracket)
(state_prefix "]" @punctuation.bracket)
(state_prefix state: (identifier) @label)

(condition_prefix (keyword) @keyword.conditional)
(condition_prefix condition: (expression) @string)

(step_description) @string

(output_binding (arrow) @operator)
(output_binding variable: (identifier) @variable)

; -----------------------------------------------------------------------------
; RETURNS SECTION
; -----------------------------------------------------------------------------
(returns_section value: (return_expression) @string)

; -----------------------------------------------------------------------------
; DEPENDS SECTION
; -----------------------------------------------------------------------------
(depends_list (anlu_reference (anlu_identifier) @function))

; -----------------------------------------------------------------------------
; EDGE CASES SECTION
; -----------------------------------------------------------------------------
(edge_case_item
  (bullet) @punctuation.special
  condition: (edge_condition) @string
  (arrow) @operator
  behavior: (edge_behavior) @string)

; -----------------------------------------------------------------------------
; TYPE BLOCK
; -----------------------------------------------------------------------------
("@type") @keyword.type

(type_header
  name: (type_name) @type.definition
  "{" @punctuation.bracket)

(extends_clause "extends" @keyword)
(extends_clause base: (type_name) @type)

(type_field
  name: (identifier) @property
  ":" @punctuation.delimiter
  type: (type_spec) @type)

(type_close "}" @punctuation.bracket)

; -----------------------------------------------------------------------------
; TEST BLOCK
; -----------------------------------------------------------------------------
("@test") @keyword.test

(test_header
  "[" @punctuation.bracket
  anlu: (anlu_identifier) @function
  "]" @punctuation.bracket
  "{" @punctuation.bracket)

(test_assertion
  expression: (expression) @function.call
  "==" @operator
  expected: (expression) @number)

(test_close "}" @punctuation.bracket)

; -----------------------------------------------------------------------------
; LITERAL BLOCK
; -----------------------------------------------------------------------------
("@literal") @keyword.directive

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
(optional_type "?" @operator)
(custom_type (type_name) @type)

; -----------------------------------------------------------------------------
; EXPRESSIONS
; -----------------------------------------------------------------------------
(binary_op) @operator
(unary_op) @operator

(function_call
  function: (identifier) @function.call
  "(" @punctuation.bracket
  ")" @punctuation.bracket)

(argument_list "," @punctuation.delimiter)

(member_expression
  "." @punctuation.delimiter
  property: (identifier) @property)

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
