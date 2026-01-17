; =============================================================================
; Tree-sitter Text Objects for NL (Natural Language Source)
;
; Enables structural selection and navigation.
; Used by editors like Neovim (via nvim-treesitter-textobjects).
; =============================================================================

; Functions (ANLUs)
(anlu_block) @function.outer
(anlu_block
  (anlu_header)
  (_)+ @function.inner)

; Classes (Type blocks)
(type_block) @class.outer
(type_block
  (type_header)
  (type_field)+ @class.inner)

; Parameters (Inputs)
(input_item) @parameter.outer
(input_item
  name: (identifier)
  type: (type_spec) @parameter.inner)

; Comments
(comment) @comment.outer

; Blocks (any braced block)
(type_block) @block.outer
(test_block) @block.outer
(literal_block) @block.outer

; Statements (logic steps, guards, edge cases)
(logic_item) @statement.outer
(guard_item) @statement.outer
(edge_case_item) @statement.outer

; Conditionals (IF...THEN in logic)
(condition_prefix) @conditional.outer
(condition_prefix
  condition: (expression) @conditional.inner)

; Assignments (output bindings)
(output_binding) @assignment.outer
(output_binding
  variable: (identifier) @assignment.inner)
