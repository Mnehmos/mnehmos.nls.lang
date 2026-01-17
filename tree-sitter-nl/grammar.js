/**
 * Tree-sitter grammar for NL (Natural Language Source)
 *
 * NL is a specification language that compiles to executable code.
 * This grammar enables IDE support, syntax highlighting, and error recovery.
 */

module.exports = grammar({
  name: "nl",

  // External scanner for literal blocks (complex brace matching)
  externals: ($) => [$._literal_content],

  // Extra tokens that can appear anywhere
  extras: ($) => [/\s/, $.comment],

  // Word token for keyword extraction
  word: ($) => $.identifier,

  // Conflict resolution
  conflicts: ($) => [[$.expression, $.type_spec]],

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
        $.literal_block
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

    anlu_block: ($) =>
      seq($.anlu_header, repeat($._anlu_section)),

    anlu_header: ($) =>
      seq("[", field("name", $.anlu_identifier), "]", $._newline),

    anlu_identifier: ($) => /[a-zA-Z][a-zA-Z0-9.-]*/,

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
        alias(/PURPOSE:/i, $.section_header),
        field("description", $.text_line),
        $._newline
      ),

    // INPUTS: bulleted list of parameters
    inputs_section: ($) =>
      seq(alias(/INPUTS:/i, $.section_header), $._newline, repeat1($.input_item)),

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
      repeat1(seq(",", choice("required", "optional", $.quoted_string, $.identifier))),

    // GUARDS: bulleted list of preconditions
    guards_section: ($) =>
      seq(alias(/GUARDS:/i, $.section_header), $._newline, repeat1($.guard_item)),

    guard_item: ($) =>
      seq(
        $.bullet,
        field("condition", $.guard_condition),
        optional(seq($.arrow, field("error", $.error_spec))),
        $._newline
      ),

    guard_condition: ($) => /[^\n→\->]+/,

    error_spec: ($) =>
      choice($.error_call, $.text_content),

    error_call: ($) =>
      seq(
        field("type", $.identifier),
        "(",
        optional($.error_args),
        ")"
      ),

    error_args: ($) =>
      seq($._error_arg, repeat(seq(",", $._error_arg))),

    _error_arg: ($) => choice($.identifier, $.quoted_string),

    // LOGIC: numbered list of steps
    logic_section: ($) =>
      seq(alias(/LOGIC:/i, $.section_header), $._newline, repeat1($.logic_item)),

    logic_item: ($) =>
      seq(
        field("number", $.step_number),
        ".",
        field("step", $.logic_step),
        $._newline
      ),

    step_number: ($) => /\d+/,

    logic_step: ($) =>
      seq(
        optional($.state_prefix),
        optional($.condition_prefix),
        field("description", $.step_description),
        optional($.output_binding)
      ),

    state_prefix: ($) => seq("[", field("state", $.identifier), "]"),

    condition_prefix: ($) =>
      seq(
        alias(/IF/i, $.keyword),
        field("condition", $.expression),
        alias(/THEN/i, $.keyword)
      ),

    step_description: ($) => /[^\n→\->[\]]+/,

    output_binding: ($) => seq($.arrow, field("variable", $.identifier)),

    // RETURNS: expression or type
    returns_section: ($) =>
      seq(
        alias(/RETURNS:/i, $.section_header),
        field("value", $.return_expression),
        $._newline
      ),

    return_expression: ($) => choice($.expression, $.type_spec),

    // DEPENDS: list of ANLU dependencies
    depends_section: ($) =>
      seq(
        alias(/DEPENDS:/i, $.section_header),
        field("dependencies", $.depends_list),
        $._newline
      ),

    depends_list: ($) => seq($.anlu_reference, repeat(seq(",", $.anlu_reference))),

    anlu_reference: ($) =>
      choice(
        seq("[", $.anlu_identifier, "]"),
        $.anlu_identifier
      ),

    // EDGE CASES: special handling
    edge_cases_section: ($) =>
      seq(alias(/EDGE\s+CASES:/i, $.section_header), $._newline, repeat1($.edge_case_item)),

    edge_case_item: ($) =>
      seq(
        $.bullet,
        field("condition", $.edge_condition),
        $.arrow,
        field("behavior", $.edge_behavior),
        $._newline
      ),

    edge_condition: ($) => /[^\n→\->]+/,
    edge_behavior: ($) => /[^\n]+/,

    // =========================================================================
    // TYPE BLOCK
    // =========================================================================

    type_block: ($) =>
      seq(
        $.type_header,
        repeat($.type_field),
        $.type_close
      ),

    type_header: ($) =>
      seq(
        "@type",
        field("name", $.type_name),
        optional($.extends_clause),
        "{",
        $._newline
      ),

    extends_clause: ($) =>
      seq("extends", field("base", $.type_name)),

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
      repeat1(seq(",", choice("required", "optional", $.quoted_string, $.identifier))),

    type_close: ($) => seq("}", $._newline),

    // =========================================================================
    // TEST BLOCK
    // =========================================================================

    test_block: ($) =>
      seq(
        $.test_header,
        repeat($.test_assertion),
        $.test_close
      ),

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
        field("expression", $.expression),
        "==",
        field("expected", $.expression),
        $._newline
      ),

    test_close: ($) => seq("}", $._newline),

    // =========================================================================
    // LITERAL BLOCK
    // =========================================================================

    literal_block: ($) =>
      seq(
        $.literal_header,
        field("content", $.literal_content),
        $.literal_close
      ),

    literal_header: ($) =>
      seq(
        "@literal",
        field("language", $.identifier),
        "{",
        $._newline
      ),

    // Literal content captures everything until closing brace
    // Uses external scanner for proper brace matching
    literal_content: ($) => repeat1(/[^\}]+|\}(?!\s*\n)/),

    literal_close: ($) => seq("}", $._newline),

    // =========================================================================
    // TYPE SYSTEM
    // =========================================================================

    type_spec: ($) =>
      choice(
        $.primitive_type,
        $.list_type,
        $.map_type,
        $.optional_type,
        $.custom_type
      ),

    primitive_type: ($) => choice("number", "string", "boolean", "void", "any"),

    list_type: ($) => seq("list", "of", field("element", $.type_spec)),

    map_type: ($) =>
      seq(
        "map",
        "of",
        field("key", $.type_spec),
        "to",
        field("value", $.type_spec)
      ),

    optional_type: ($) => seq($.type_spec, "?"),

    custom_type: ($) => $.type_name,

    // =========================================================================
    // EXPRESSIONS
    // =========================================================================

    expression: ($) =>
      choice(
        $.binary_expression,
        $.unary_expression,
        $.function_call,
        $.parenthesized_expression,
        $.member_expression,
        $._literal,
        $.identifier
      ),

    binary_expression: ($) =>
      prec.left(
        1,
        seq(field("left", $.expression), $.binary_op, field("right", $.expression))
      ),

    unary_expression: ($) =>
      prec(2, seq($.unary_op, field("operand", $.expression))),

    function_call: ($) =>
      prec(
        3,
        seq(
          field("function", $.identifier),
          "(",
          optional($.argument_list),
          ")"
        )
      ),

    argument_list: ($) => seq($.expression, repeat(seq(",", $.expression))),

    parenthesized_expression: ($) => seq("(", $.expression, ")"),

    member_expression: ($) =>
      prec.left(4, seq(field("object", $.expression), ".", field("property", $.identifier))),

    binary_op: ($) =>
      choice(
        // Arithmetic
        "+",
        "-",
        "*",
        "/",
        "×",
        "÷",
        // Comparison
        "==",
        "!=",
        "<",
        ">",
        "<=",
        ">=",
        // Logical
        "and",
        "or",
        "AND",
        "OR"
      ),

    unary_op: ($) => choice("-", "not", "NOT"),

    // =========================================================================
    // LITERALS
    // =========================================================================

    _literal: ($) => choice($.number, $.quoted_string, $.boolean),

    number: ($) => /-?\d+(\.\d+)?/,

    quoted_string: ($) =>
      choice(seq('"', /[^"]*/, '"'), seq("'", /[^']*/, "'")),

    boolean: ($) => choice("true", "false", "True", "False"),

    // =========================================================================
    // LEXICAL ELEMENTS
    // =========================================================================

    identifier: ($) => /[a-zA-Z_][a-zA-Z0-9_]*/,

    bullet: ($) => choice("•", "-", "*"),

    arrow: ($) => choice("→", "->"),

    text_line: ($) => /[^\n]+/,
    text_content: ($) => /[^\n→\->]+/,

    _newline: ($) => /\r?\n/,
  },
});
