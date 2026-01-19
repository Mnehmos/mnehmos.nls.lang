/**
 * Tree-sitter grammar for NL (Natural Language Source)
 *
 * NL is a specification language that compiles to executable code.
 * This grammar enables IDE support, syntax highlighting, and error recovery.
 */

module.exports = grammar({
  name: "nl",

  // External scanner for literal block content (proper brace matching)
  externals: ($) => [$.literal_content],

  // Extra tokens that can appear anywhere
  extras: ($) => [/[ \t]/, $.comment],

  // Inline rules (don't create nodes)
  inline: ($) => [$._item, $._anlu_section, $._literal, $._error_arg],

  rules: {
    // =========================================================================
    // TOP-LEVEL STRUCTURE
    // =========================================================================

    source_file: ($) => repeat($._item),

    _item: ($) =>
      choice(
        $.directive,
        $.anlu_block,
        $.type_block,
        $.test_block,
        $.invariant_block,
        $.property_block,
        $.literal_block,
        $._newline
      ),

    comment: ($) => token(seq("#", /.*/)),

    // =========================================================================
    // DIRECTIVES
    // =========================================================================

    directive: ($) =>
      choice(
        $.module_directive,
        $.version_directive,
        $.target_directive,
        $.imports_directive
      ),

    module_directive: ($) =>
      seq("@module", field("name", $.identifier), $._newline),

    version_directive: ($) =>
      seq("@version", field("version", $.version_string), $._newline),

    target_directive: ($) =>
      seq("@target", field("target", $.target_name), $._newline),

    imports_directive: ($) =>
      seq("@imports", field("imports", $.import_list), $._newline),

    version_string: ($) => /\d+\.\d+(\.\d+)?/,

    target_name: ($) => choice("python", "typescript", "rust"),

    import_list: ($) => seq($.identifier, repeat(seq(",", $.identifier))),

    // =========================================================================
    // ANLU BLOCK (Atomic Natural Language Unit)
    // =========================================================================

    anlu_block: ($) => seq($.anlu_header, repeat($._anlu_section)),

    anlu_header: ($) =>
      seq("[", field("name", $.anlu_identifier), "]", $._newline),

    anlu_identifier: ($) => /[a-zA-Z][a-zA-Z0-9._-]*/,

    _anlu_section: ($) =>
      choice(
        $.purpose_section,
        $.inputs_section,
        $.guards_section,
        $.logic_section,
        $.returns_section,
        $.depends_section,
        $.edge_cases_section
      ),

    // PURPOSE: single line description
    purpose_section: ($) =>
      seq(
        field("header", alias(/PURPOSE:/i, $.section_keyword)),
        field("description", $.description_text),
        $._newline
      ),

    description_text: ($) => /[^\n]+/,

    // INPUTS: bulleted list of parameters, or "INPUTS: none" for no parameters
    inputs_section: ($) =>
      choice(
        // INPUTS: none (no parameters)
        seq(
          field("header", alias(/INPUTS:/i, $.section_keyword)),
          alias("none", $.none_marker),
          $._newline
        ),
        // INPUTS: followed by bulleted items
        seq(
          field("header", alias(/INPUTS:/i, $.section_keyword)),
          $._newline,
          repeat1($.input_item)
        )
      ),

    input_item: ($) =>
      seq(
        $.bullet,
        field("name", $.identifier),
        ":",
        field("type", $.type_spec),
        optional($.input_constraints),
        $._newline
      ),

    input_constraints: ($) =>
      repeat1(
        seq(
          ",",
          choice(
            "required",
            "optional",
            $.constraint_pair,
            $.quoted_string,
            $.identifier
          )
        )
      ),

    // GUARDS: bulleted list of preconditions
    guards_section: ($) =>
      seq(
        field("header", alias(/GUARDS:/i, $.section_keyword)),
        $._newline,
        repeat1($.guard_item)
      ),

    guard_item: ($) =>
      seq(
        $.bullet,
        field("condition", $.guard_text),
        optional(seq($.arrow, field("error", $.error_spec))),
        $._newline
      ),

    guard_text: ($) => /[^\n→-]+/,

    error_spec: ($) => choice(
      prec.dynamic(2, $.error_call),
      prec.dynamic(1, $.error_text)
    ),

    error_call: ($) =>
      seq(field("type", $.identifier), "(", optional($.error_args), ")"),

    error_args: ($) => seq($._error_arg, repeat(seq(",", $._error_arg))),

    _error_arg: ($) => choice($.identifier, $.quoted_string),

    error_text: ($) => /[^\n]+/,

    // LOGIC: numbered list of steps
    logic_section: ($) =>
      seq(
        field("header", alias(/LOGIC:/i, $.section_keyword)),
        $._newline,
        repeat1($.logic_item)
      ),

    logic_item: ($) =>
      seq(field("number", $.step_number), ".", $.logic_step, $._newline),

    // Support both numbered steps (1., 2.) and lettered sub-steps (a., b.)
    step_number: ($) => /\d+|[a-z]/,

    logic_step: ($) =>
      seq(
        optional($.state_prefix),
        optional($.condition_prefix),
        field("description", $.step_text),
        optional($.output_binding)
      ),

    state_prefix: ($) => seq("[", field("state", $.state_name), "]"),

    state_name: ($) => /[a-zA-Z_][a-zA-Z0-9_-]*/,

    condition_prefix: ($) =>
      seq(alias(/IF/i, $.keyword), $.condition_text, alias(/THEN/i, $.keyword)),

    // Condition text: sequence of tokens that aren't THEN
    condition_text: ($) => prec.right(repeat1($.condition_token)),

    condition_token: ($) =>
      choice(
        /[a-zA-Z_][a-zA-Z0-9_]*/,
        /[0-9]+(\.[0-9]+)?/,
        /[<>=!]+/,
        /[()\[\]]/,
        /[+\-*/]/,
        "and",
        "or",
        "not"
      ),

    // Match step text, stopping at arrow sequences
    // Uses negative character class - allows hyphen but stops at → or ->
    step_text: ($) => /[^\n→]*[^\n→ \t-]/,

    output_binding: ($) => seq($.arrow, field("variable", $.identifier)),

    // RETURNS: expression or type
    returns_section: ($) =>
      seq(
        field("header", alias(/RETURNS:/i, $.section_keyword)),
        field("value", $.returns_text),
        $._newline
      ),

    returns_text: ($) => /[^\n]+/,

    // DEPENDS: list of ANLU dependencies
    depends_section: ($) =>
      seq(
        field("header", alias(/DEPENDS:/i, $.section_keyword)),
        field("dependencies", $.depends_list),
        $._newline
      ),

    depends_list: ($) =>
      seq($.anlu_reference, repeat(seq(",", $.anlu_reference))),

    anlu_reference: ($) =>
      choice(seq("[", $.anlu_identifier, "]"), $.anlu_identifier),

    // EDGE CASES: special handling
    edge_cases_section: ($) =>
      seq(
        field("header", alias(/EDGE\s+CASES:/i, $.section_keyword)),
        $._newline,
        repeat1($.edge_case_item)
      ),

    edge_case_item: ($) =>
      seq(
        $.bullet,
        field("condition", $.edge_condition_text),
        $.arrow,
        field("behavior", $.edge_behavior_text),
        $._newline
      ),

    edge_condition_text: ($) => /[^\n→-]+/,
    edge_behavior_text: ($) => /[^\n]+/,

    // =========================================================================
    // TYPE BLOCK
    // =========================================================================

    type_block: ($) =>
      seq($.type_header, repeat($.type_field), $.type_close),

    type_header: ($) =>
      seq(
        "@type",
        field("name", $.type_name),
        optional($.extends_clause),
        "{",
        $._newline
      ),

    extends_clause: ($) => seq("extends", field("base", $.type_name)),

    type_name: ($) => /[A-Z][a-zA-Z0-9]*/,

    type_field: ($) =>
      seq(
        optional($.bullet),
        field("name", $.identifier),
        ":",
        field("type", $.type_spec),
        optional($.field_constraints),
        $._newline
      ),

    field_constraints: ($) =>
      repeat1(
        seq(
          ",",
          choice(
            "required",
            "optional",
            $.constraint_pair,
            $.quoted_string,
            $.identifier
          )
        )
      ),

    // Support for key: value constraints like "min: 1", "max: 100"
    constraint_pair: ($) =>
      seq(
        field("key", $.identifier),
        ":",
        field("value", choice($.number, $.identifier, $.quoted_string))
      ),

    type_close: ($) => seq("}", $._newline),

    // =========================================================================
    // TEST BLOCK
    // =========================================================================

    test_block: ($) =>
      seq($.test_header, repeat($.test_assertion), $.test_close),

    test_header: ($) =>
      seq(
        "@test",
        "[",
        field("anlu", $.anlu_identifier),
        "]",
        "{",
        $._newline
      ),

    test_assertion: ($) =>
      seq(
        field("call", $.test_call),
        "==",
        field("expected", $.test_value),
        $._newline
      ),

    test_call: ($) =>
      seq(field("function", $.identifier), "(", optional($.test_args), ")"),

    test_args: ($) => seq($.test_value, repeat(seq(",", $.test_value))),

    test_value: ($) => choice($.number, $.quoted_string, $.boolean, $.identifier),

    test_close: ($) => seq("}", $._newline),

    // =========================================================================
    // INVARIANT BLOCK
    // =========================================================================

    invariant_block: ($) =>
      seq($.invariant_header, repeat($.invariant_assertion), $.invariant_close),

    invariant_header: ($) =>
      seq("@invariant", field("type", $.type_name), "{", $._newline),

    invariant_assertion: ($) =>
      seq(field("expression", $.expression_text), $._newline),

    invariant_close: ($) => seq("}", $._newline),

    // =========================================================================
    // PROPERTY BLOCK
    // =========================================================================

    property_block: ($) =>
      seq($.property_header, repeat($.property_assertion), $.property_close),

    property_header: ($) =>
      seq("@property", "[", field("anlu", $.anlu_identifier), "]", "{", $._newline),

    property_assertion: ($) =>
      seq(field("expression", $.expression_text), $._newline),

    property_close: ($) => seq("}", $._newline),

    // Expression text - captures everything until end of line
    expression_text: ($) => /[^\n}]+/,

    // =========================================================================
    // LITERAL BLOCK
    // =========================================================================

    literal_block: ($) =>
      seq($.literal_header, field("content", $.literal_content), $.literal_close),

    literal_header: ($) =>
      seq("@literal", field("language", $.identifier), "{", $._newline),

    literal_close: ($) => seq("}", $._newline),

    // =========================================================================
    // TYPE SYSTEM
    // =========================================================================

    type_spec: ($) =>
      seq($._base_type, optional("?")),

    _base_type: ($) =>
      choice($.primitive_type, $.list_type, $.map_type, $.custom_type),

    primitive_type: ($) => choice("number", "string", "boolean", "void", "any"),

    list_type: ($) => seq("list", "of", field("element", $._base_type)),

    map_type: ($) =>
      seq("map", "of", field("key", $._base_type), "to", field("value", $._base_type)),

    custom_type: ($) => $.type_name,

    // =========================================================================
    // LITERALS
    // =========================================================================

    _literal: ($) => choice($.number, $.quoted_string, $.boolean),

    number: ($) => /-?\d+(\.\d+)?/,

    quoted_string: ($) => choice(/"[^"]*"/, /'[^']*'/),

    boolean: ($) => choice("true", "false", "True", "False"),

    // =========================================================================
    // LEXICAL ELEMENTS
    // =========================================================================

    identifier: ($) => /[a-zA-Z_][a-zA-Z0-9_]*/,

    bullet: ($) => choice("•", "-", "*"),

    arrow: ($) => choice("→", "->"),

    _newline: ($) => /\r?\n/,
  },
});
