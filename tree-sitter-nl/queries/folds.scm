; =============================================================================
; Tree-sitter Code Folding for NL (Natural Language Source)
;
; Defines foldable regions for .nl files.
; =============================================================================

; ANLU blocks are foldable (from header to end of sections)
(anlu_block) @fold

; Type blocks with braces
(type_block) @fold

; Test blocks with braces
(test_block) @fold

; Literal blocks with braces
(literal_block) @fold

; Sections within ANLUs are individually foldable
(inputs_section) @fold
(guards_section) @fold
(logic_section) @fold
(edge_cases_section) @fold
