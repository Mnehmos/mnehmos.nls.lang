#include "tree_sitter/parser.h"

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#ifdef _MSC_VER
#pragma optimize("", off)
#elif defined(__clang__)
#pragma clang optimize off
#elif defined(__GNUC__)
#pragma GCC optimize ("O0")
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 216
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 154
#define ALIAS_COUNT 0
#define TOKEN_COUNT 73
#define EXTERNAL_TOKEN_COUNT 1
#define FIELD_COUNT 24
#define MAX_ALIAS_SEQUENCE_LENGTH 6
#define PRODUCTION_ID_COUNT 29

enum ts_symbol_identifiers {
  sym_comment = 1,
  anon_sym_ATmodule = 2,
  anon_sym_ATversion = 3,
  anon_sym_ATtarget = 4,
  anon_sym_ATimports = 5,
  sym_version_string = 6,
  anon_sym_python = 7,
  anon_sym_typescript = 8,
  anon_sym_rust = 9,
  anon_sym_COMMA = 10,
  anon_sym_LBRACK = 11,
  anon_sym_RBRACK = 12,
  sym_anlu_identifier = 13,
  aux_sym_purpose_section_token1 = 14,
  aux_sym_description_text_token1 = 15,
  aux_sym_inputs_section_token1 = 16,
  anon_sym_COLON = 17,
  anon_sym_required = 18,
  anon_sym_optional = 19,
  aux_sym_guards_section_token1 = 20,
  aux_sym_guard_text_token1 = 21,
  anon_sym_LPAREN = 22,
  anon_sym_RPAREN = 23,
  aux_sym_logic_section_token1 = 24,
  anon_sym_DOT = 25,
  sym_step_number = 26,
  sym_state_name = 27,
  aux_sym_condition_prefix_token1 = 28,
  aux_sym_condition_prefix_token2 = 29,
  aux_sym_condition_token_token1 = 30,
  aux_sym_condition_token_token2 = 31,
  aux_sym_condition_token_token3 = 32,
  aux_sym_condition_token_token4 = 33,
  aux_sym_condition_token_token5 = 34,
  anon_sym_and = 35,
  anon_sym_or = 36,
  anon_sym_not = 37,
  aux_sym_returns_section_token1 = 38,
  aux_sym_depends_section_token1 = 39,
  aux_sym_edge_cases_section_token1 = 40,
  anon_sym_ATtype = 41,
  anon_sym_LBRACE = 42,
  anon_sym_extends = 43,
  sym_type_name = 44,
  anon_sym_RBRACE = 45,
  anon_sym_ATtest = 46,
  anon_sym_EQ_EQ = 47,
  anon_sym_ATliteral = 48,
  anon_sym_QMARK = 49,
  anon_sym_number = 50,
  anon_sym_string = 51,
  anon_sym_boolean = 52,
  anon_sym_void = 53,
  anon_sym_any = 54,
  anon_sym_list = 55,
  anon_sym_of = 56,
  anon_sym_map = 57,
  anon_sym_to = 58,
  sym_number = 59,
  aux_sym_quoted_string_token1 = 60,
  aux_sym_quoted_string_token2 = 61,
  anon_sym_true = 62,
  anon_sym_false = 63,
  anon_sym_True = 64,
  anon_sym_False = 65,
  anon_sym_u2022 = 66,
  anon_sym_DASH = 67,
  anon_sym_STAR = 68,
  anon_sym_u2192 = 69,
  anon_sym_DASH_GT = 70,
  sym__newline = 71,
  sym_literal_content = 72,
  sym_source_file = 73,
  sym_directive = 74,
  sym_module_directive = 75,
  sym_version_directive = 76,
  sym_target_directive = 77,
  sym_imports_directive = 78,
  sym_target_name = 79,
  sym_import_list = 80,
  sym_anlu_block = 81,
  sym_anlu_header = 82,
  sym_purpose_section = 83,
  sym_description_text = 84,
  sym_inputs_section = 85,
  sym_input_item = 86,
  sym_input_constraints = 87,
  sym_guards_section = 88,
  sym_guard_item = 89,
  sym_guard_text = 90,
  sym_error_spec = 91,
  sym_error_call = 92,
  sym_error_args = 93,
  sym_error_text = 94,
  sym_logic_section = 95,
  sym_logic_item = 96,
  sym_logic_step = 97,
  sym_state_prefix = 98,
  sym_condition_prefix = 99,
  sym_condition_text = 100,
  sym_condition_token = 101,
  sym_step_text = 102,
  sym_output_binding = 103,
  sym_returns_section = 104,
  sym_returns_text = 105,
  sym_depends_section = 106,
  sym_depends_list = 107,
  sym_anlu_reference = 108,
  sym_edge_cases_section = 109,
  sym_edge_case_item = 110,
  sym_edge_condition_text = 111,
  sym_edge_behavior_text = 112,
  sym_type_block = 113,
  sym_type_header = 114,
  sym_extends_clause = 115,
  sym_type_field = 116,
  sym_field_constraints = 117,
  sym_type_close = 118,
  sym_test_block = 119,
  sym_test_header = 120,
  sym_test_assertion = 121,
  sym_test_call = 122,
  sym_test_args = 123,
  sym_test_value = 124,
  sym_test_close = 125,
  sym_literal_block = 126,
  sym_literal_header = 127,
  sym_literal_close = 128,
  sym_type_spec = 129,
  sym__base_type = 130,
  sym_primitive_type = 131,
  sym_list_type = 132,
  sym_map_type = 133,
  sym_custom_type = 134,
  sym_quoted_string = 135,
  sym_boolean = 136,
  sym_identifier = 137,
  sym_bullet = 138,
  sym_arrow = 139,
  aux_sym_source_file_repeat1 = 140,
  aux_sym_import_list_repeat1 = 141,
  aux_sym_anlu_block_repeat1 = 142,
  aux_sym_inputs_section_repeat1 = 143,
  aux_sym_input_constraints_repeat1 = 144,
  aux_sym_guards_section_repeat1 = 145,
  aux_sym_error_args_repeat1 = 146,
  aux_sym_logic_section_repeat1 = 147,
  aux_sym_condition_text_repeat1 = 148,
  aux_sym_depends_list_repeat1 = 149,
  aux_sym_edge_cases_section_repeat1 = 150,
  aux_sym_type_block_repeat1 = 151,
  aux_sym_test_block_repeat1 = 152,
  aux_sym_test_args_repeat1 = 153,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [sym_comment] = "comment",
  [anon_sym_ATmodule] = "@module",
  [anon_sym_ATversion] = "@version",
  [anon_sym_ATtarget] = "@target",
  [anon_sym_ATimports] = "@imports",
  [sym_version_string] = "version_string",
  [anon_sym_python] = "python",
  [anon_sym_typescript] = "typescript",
  [anon_sym_rust] = "rust",
  [anon_sym_COMMA] = ",",
  [anon_sym_LBRACK] = "[",
  [anon_sym_RBRACK] = "]",
  [sym_anlu_identifier] = "anlu_identifier",
  [aux_sym_purpose_section_token1] = "section_keyword",
  [aux_sym_description_text_token1] = "description_text_token1",
  [aux_sym_inputs_section_token1] = "section_keyword",
  [anon_sym_COLON] = ":",
  [anon_sym_required] = "required",
  [anon_sym_optional] = "optional",
  [aux_sym_guards_section_token1] = "section_keyword",
  [aux_sym_guard_text_token1] = "guard_text_token1",
  [anon_sym_LPAREN] = "(",
  [anon_sym_RPAREN] = ")",
  [aux_sym_logic_section_token1] = "section_keyword",
  [anon_sym_DOT] = ".",
  [sym_step_number] = "step_number",
  [sym_state_name] = "state_name",
  [aux_sym_condition_prefix_token1] = "keyword",
  [aux_sym_condition_prefix_token2] = "keyword",
  [aux_sym_condition_token_token1] = "condition_token_token1",
  [aux_sym_condition_token_token2] = "condition_token_token2",
  [aux_sym_condition_token_token3] = "condition_token_token3",
  [aux_sym_condition_token_token4] = "condition_token_token4",
  [aux_sym_condition_token_token5] = "condition_token_token5",
  [anon_sym_and] = "and",
  [anon_sym_or] = "or",
  [anon_sym_not] = "not",
  [aux_sym_returns_section_token1] = "section_keyword",
  [aux_sym_depends_section_token1] = "section_keyword",
  [aux_sym_edge_cases_section_token1] = "section_keyword",
  [anon_sym_ATtype] = "@type",
  [anon_sym_LBRACE] = "{",
  [anon_sym_extends] = "extends",
  [sym_type_name] = "type_name",
  [anon_sym_RBRACE] = "}",
  [anon_sym_ATtest] = "@test",
  [anon_sym_EQ_EQ] = "==",
  [anon_sym_ATliteral] = "@literal",
  [anon_sym_QMARK] = "\?",
  [anon_sym_number] = "number",
  [anon_sym_string] = "string",
  [anon_sym_boolean] = "boolean",
  [anon_sym_void] = "void",
  [anon_sym_any] = "any",
  [anon_sym_list] = "list",
  [anon_sym_of] = "of",
  [anon_sym_map] = "map",
  [anon_sym_to] = "to",
  [sym_number] = "number",
  [aux_sym_quoted_string_token1] = "quoted_string_token1",
  [aux_sym_quoted_string_token2] = "quoted_string_token2",
  [anon_sym_true] = "true",
  [anon_sym_false] = "false",
  [anon_sym_True] = "True",
  [anon_sym_False] = "False",
  [anon_sym_u2022] = "\u2022",
  [anon_sym_DASH] = "-",
  [anon_sym_STAR] = "*",
  [anon_sym_u2192] = "\u2192",
  [anon_sym_DASH_GT] = "->",
  [sym__newline] = "_newline",
  [sym_literal_content] = "literal_content",
  [sym_source_file] = "source_file",
  [sym_directive] = "directive",
  [sym_module_directive] = "module_directive",
  [sym_version_directive] = "version_directive",
  [sym_target_directive] = "target_directive",
  [sym_imports_directive] = "imports_directive",
  [sym_target_name] = "target_name",
  [sym_import_list] = "import_list",
  [sym_anlu_block] = "anlu_block",
  [sym_anlu_header] = "anlu_header",
  [sym_purpose_section] = "purpose_section",
  [sym_description_text] = "description_text",
  [sym_inputs_section] = "inputs_section",
  [sym_input_item] = "input_item",
  [sym_input_constraints] = "input_constraints",
  [sym_guards_section] = "guards_section",
  [sym_guard_item] = "guard_item",
  [sym_guard_text] = "guard_text",
  [sym_error_spec] = "error_spec",
  [sym_error_call] = "error_call",
  [sym_error_args] = "error_args",
  [sym_error_text] = "error_text",
  [sym_logic_section] = "logic_section",
  [sym_logic_item] = "logic_item",
  [sym_logic_step] = "logic_step",
  [sym_state_prefix] = "state_prefix",
  [sym_condition_prefix] = "condition_prefix",
  [sym_condition_text] = "condition_text",
  [sym_condition_token] = "condition_token",
  [sym_step_text] = "step_text",
  [sym_output_binding] = "output_binding",
  [sym_returns_section] = "returns_section",
  [sym_returns_text] = "returns_text",
  [sym_depends_section] = "depends_section",
  [sym_depends_list] = "depends_list",
  [sym_anlu_reference] = "anlu_reference",
  [sym_edge_cases_section] = "edge_cases_section",
  [sym_edge_case_item] = "edge_case_item",
  [sym_edge_condition_text] = "edge_condition_text",
  [sym_edge_behavior_text] = "edge_behavior_text",
  [sym_type_block] = "type_block",
  [sym_type_header] = "type_header",
  [sym_extends_clause] = "extends_clause",
  [sym_type_field] = "type_field",
  [sym_field_constraints] = "field_constraints",
  [sym_type_close] = "type_close",
  [sym_test_block] = "test_block",
  [sym_test_header] = "test_header",
  [sym_test_assertion] = "test_assertion",
  [sym_test_call] = "test_call",
  [sym_test_args] = "test_args",
  [sym_test_value] = "test_value",
  [sym_test_close] = "test_close",
  [sym_literal_block] = "literal_block",
  [sym_literal_header] = "literal_header",
  [sym_literal_close] = "literal_close",
  [sym_type_spec] = "type_spec",
  [sym__base_type] = "_base_type",
  [sym_primitive_type] = "primitive_type",
  [sym_list_type] = "list_type",
  [sym_map_type] = "map_type",
  [sym_custom_type] = "custom_type",
  [sym_quoted_string] = "quoted_string",
  [sym_boolean] = "boolean",
  [sym_identifier] = "identifier",
  [sym_bullet] = "bullet",
  [sym_arrow] = "arrow",
  [aux_sym_source_file_repeat1] = "source_file_repeat1",
  [aux_sym_import_list_repeat1] = "import_list_repeat1",
  [aux_sym_anlu_block_repeat1] = "anlu_block_repeat1",
  [aux_sym_inputs_section_repeat1] = "inputs_section_repeat1",
  [aux_sym_input_constraints_repeat1] = "input_constraints_repeat1",
  [aux_sym_guards_section_repeat1] = "guards_section_repeat1",
  [aux_sym_error_args_repeat1] = "error_args_repeat1",
  [aux_sym_logic_section_repeat1] = "logic_section_repeat1",
  [aux_sym_condition_text_repeat1] = "condition_text_repeat1",
  [aux_sym_depends_list_repeat1] = "depends_list_repeat1",
  [aux_sym_edge_cases_section_repeat1] = "edge_cases_section_repeat1",
  [aux_sym_type_block_repeat1] = "type_block_repeat1",
  [aux_sym_test_block_repeat1] = "test_block_repeat1",
  [aux_sym_test_args_repeat1] = "test_args_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [sym_comment] = sym_comment,
  [anon_sym_ATmodule] = anon_sym_ATmodule,
  [anon_sym_ATversion] = anon_sym_ATversion,
  [anon_sym_ATtarget] = anon_sym_ATtarget,
  [anon_sym_ATimports] = anon_sym_ATimports,
  [sym_version_string] = sym_version_string,
  [anon_sym_python] = anon_sym_python,
  [anon_sym_typescript] = anon_sym_typescript,
  [anon_sym_rust] = anon_sym_rust,
  [anon_sym_COMMA] = anon_sym_COMMA,
  [anon_sym_LBRACK] = anon_sym_LBRACK,
  [anon_sym_RBRACK] = anon_sym_RBRACK,
  [sym_anlu_identifier] = sym_anlu_identifier,
  [aux_sym_purpose_section_token1] = aux_sym_purpose_section_token1,
  [aux_sym_description_text_token1] = aux_sym_description_text_token1,
  [aux_sym_inputs_section_token1] = aux_sym_purpose_section_token1,
  [anon_sym_COLON] = anon_sym_COLON,
  [anon_sym_required] = anon_sym_required,
  [anon_sym_optional] = anon_sym_optional,
  [aux_sym_guards_section_token1] = aux_sym_purpose_section_token1,
  [aux_sym_guard_text_token1] = aux_sym_guard_text_token1,
  [anon_sym_LPAREN] = anon_sym_LPAREN,
  [anon_sym_RPAREN] = anon_sym_RPAREN,
  [aux_sym_logic_section_token1] = aux_sym_purpose_section_token1,
  [anon_sym_DOT] = anon_sym_DOT,
  [sym_step_number] = sym_step_number,
  [sym_state_name] = sym_state_name,
  [aux_sym_condition_prefix_token1] = aux_sym_condition_prefix_token1,
  [aux_sym_condition_prefix_token2] = aux_sym_condition_prefix_token1,
  [aux_sym_condition_token_token1] = aux_sym_condition_token_token1,
  [aux_sym_condition_token_token2] = aux_sym_condition_token_token2,
  [aux_sym_condition_token_token3] = aux_sym_condition_token_token3,
  [aux_sym_condition_token_token4] = aux_sym_condition_token_token4,
  [aux_sym_condition_token_token5] = aux_sym_condition_token_token5,
  [anon_sym_and] = anon_sym_and,
  [anon_sym_or] = anon_sym_or,
  [anon_sym_not] = anon_sym_not,
  [aux_sym_returns_section_token1] = aux_sym_purpose_section_token1,
  [aux_sym_depends_section_token1] = aux_sym_purpose_section_token1,
  [aux_sym_edge_cases_section_token1] = aux_sym_purpose_section_token1,
  [anon_sym_ATtype] = anon_sym_ATtype,
  [anon_sym_LBRACE] = anon_sym_LBRACE,
  [anon_sym_extends] = anon_sym_extends,
  [sym_type_name] = sym_type_name,
  [anon_sym_RBRACE] = anon_sym_RBRACE,
  [anon_sym_ATtest] = anon_sym_ATtest,
  [anon_sym_EQ_EQ] = anon_sym_EQ_EQ,
  [anon_sym_ATliteral] = anon_sym_ATliteral,
  [anon_sym_QMARK] = anon_sym_QMARK,
  [anon_sym_number] = anon_sym_number,
  [anon_sym_string] = anon_sym_string,
  [anon_sym_boolean] = anon_sym_boolean,
  [anon_sym_void] = anon_sym_void,
  [anon_sym_any] = anon_sym_any,
  [anon_sym_list] = anon_sym_list,
  [anon_sym_of] = anon_sym_of,
  [anon_sym_map] = anon_sym_map,
  [anon_sym_to] = anon_sym_to,
  [sym_number] = sym_number,
  [aux_sym_quoted_string_token1] = aux_sym_quoted_string_token1,
  [aux_sym_quoted_string_token2] = aux_sym_quoted_string_token2,
  [anon_sym_true] = anon_sym_true,
  [anon_sym_false] = anon_sym_false,
  [anon_sym_True] = anon_sym_True,
  [anon_sym_False] = anon_sym_False,
  [anon_sym_u2022] = anon_sym_u2022,
  [anon_sym_DASH] = anon_sym_DASH,
  [anon_sym_STAR] = anon_sym_STAR,
  [anon_sym_u2192] = anon_sym_u2192,
  [anon_sym_DASH_GT] = anon_sym_DASH_GT,
  [sym__newline] = sym__newline,
  [sym_literal_content] = sym_literal_content,
  [sym_source_file] = sym_source_file,
  [sym_directive] = sym_directive,
  [sym_module_directive] = sym_module_directive,
  [sym_version_directive] = sym_version_directive,
  [sym_target_directive] = sym_target_directive,
  [sym_imports_directive] = sym_imports_directive,
  [sym_target_name] = sym_target_name,
  [sym_import_list] = sym_import_list,
  [sym_anlu_block] = sym_anlu_block,
  [sym_anlu_header] = sym_anlu_header,
  [sym_purpose_section] = sym_purpose_section,
  [sym_description_text] = sym_description_text,
  [sym_inputs_section] = sym_inputs_section,
  [sym_input_item] = sym_input_item,
  [sym_input_constraints] = sym_input_constraints,
  [sym_guards_section] = sym_guards_section,
  [sym_guard_item] = sym_guard_item,
  [sym_guard_text] = sym_guard_text,
  [sym_error_spec] = sym_error_spec,
  [sym_error_call] = sym_error_call,
  [sym_error_args] = sym_error_args,
  [sym_error_text] = sym_error_text,
  [sym_logic_section] = sym_logic_section,
  [sym_logic_item] = sym_logic_item,
  [sym_logic_step] = sym_logic_step,
  [sym_state_prefix] = sym_state_prefix,
  [sym_condition_prefix] = sym_condition_prefix,
  [sym_condition_text] = sym_condition_text,
  [sym_condition_token] = sym_condition_token,
  [sym_step_text] = sym_step_text,
  [sym_output_binding] = sym_output_binding,
  [sym_returns_section] = sym_returns_section,
  [sym_returns_text] = sym_returns_text,
  [sym_depends_section] = sym_depends_section,
  [sym_depends_list] = sym_depends_list,
  [sym_anlu_reference] = sym_anlu_reference,
  [sym_edge_cases_section] = sym_edge_cases_section,
  [sym_edge_case_item] = sym_edge_case_item,
  [sym_edge_condition_text] = sym_edge_condition_text,
  [sym_edge_behavior_text] = sym_edge_behavior_text,
  [sym_type_block] = sym_type_block,
  [sym_type_header] = sym_type_header,
  [sym_extends_clause] = sym_extends_clause,
  [sym_type_field] = sym_type_field,
  [sym_field_constraints] = sym_field_constraints,
  [sym_type_close] = sym_type_close,
  [sym_test_block] = sym_test_block,
  [sym_test_header] = sym_test_header,
  [sym_test_assertion] = sym_test_assertion,
  [sym_test_call] = sym_test_call,
  [sym_test_args] = sym_test_args,
  [sym_test_value] = sym_test_value,
  [sym_test_close] = sym_test_close,
  [sym_literal_block] = sym_literal_block,
  [sym_literal_header] = sym_literal_header,
  [sym_literal_close] = sym_literal_close,
  [sym_type_spec] = sym_type_spec,
  [sym__base_type] = sym__base_type,
  [sym_primitive_type] = sym_primitive_type,
  [sym_list_type] = sym_list_type,
  [sym_map_type] = sym_map_type,
  [sym_custom_type] = sym_custom_type,
  [sym_quoted_string] = sym_quoted_string,
  [sym_boolean] = sym_boolean,
  [sym_identifier] = sym_identifier,
  [sym_bullet] = sym_bullet,
  [sym_arrow] = sym_arrow,
  [aux_sym_source_file_repeat1] = aux_sym_source_file_repeat1,
  [aux_sym_import_list_repeat1] = aux_sym_import_list_repeat1,
  [aux_sym_anlu_block_repeat1] = aux_sym_anlu_block_repeat1,
  [aux_sym_inputs_section_repeat1] = aux_sym_inputs_section_repeat1,
  [aux_sym_input_constraints_repeat1] = aux_sym_input_constraints_repeat1,
  [aux_sym_guards_section_repeat1] = aux_sym_guards_section_repeat1,
  [aux_sym_error_args_repeat1] = aux_sym_error_args_repeat1,
  [aux_sym_logic_section_repeat1] = aux_sym_logic_section_repeat1,
  [aux_sym_condition_text_repeat1] = aux_sym_condition_text_repeat1,
  [aux_sym_depends_list_repeat1] = aux_sym_depends_list_repeat1,
  [aux_sym_edge_cases_section_repeat1] = aux_sym_edge_cases_section_repeat1,
  [aux_sym_type_block_repeat1] = aux_sym_type_block_repeat1,
  [aux_sym_test_block_repeat1] = aux_sym_test_block_repeat1,
  [aux_sym_test_args_repeat1] = aux_sym_test_args_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [sym_comment] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_ATmodule] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ATversion] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ATtarget] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ATimports] = {
    .visible = true,
    .named = false,
  },
  [sym_version_string] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_python] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_typescript] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_rust] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_COMMA] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LBRACK] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RBRACK] = {
    .visible = true,
    .named = false,
  },
  [sym_anlu_identifier] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_purpose_section_token1] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_description_text_token1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_inputs_section_token1] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_COLON] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_required] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_optional] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_guards_section_token1] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_guard_text_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_LPAREN] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_RPAREN] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_logic_section_token1] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_DOT] = {
    .visible = true,
    .named = false,
  },
  [sym_step_number] = {
    .visible = true,
    .named = true,
  },
  [sym_state_name] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_condition_prefix_token1] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_condition_prefix_token2] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_condition_token_token1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_condition_token_token2] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_condition_token_token3] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_condition_token_token4] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_condition_token_token5] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_and] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_or] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_not] = {
    .visible = true,
    .named = false,
  },
  [aux_sym_returns_section_token1] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_depends_section_token1] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_edge_cases_section_token1] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_ATtype] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_LBRACE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_extends] = {
    .visible = true,
    .named = false,
  },
  [sym_type_name] = {
    .visible = true,
    .named = true,
  },
  [anon_sym_RBRACE] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ATtest] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_EQ_EQ] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ATliteral] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_QMARK] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_number] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_string] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_boolean] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_void] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_any] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_list] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_of] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_map] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_to] = {
    .visible = true,
    .named = false,
  },
  [sym_number] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_quoted_string_token1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_quoted_string_token2] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_true] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_false] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_True] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_False] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u2022] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_STAR] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_u2192] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_DASH_GT] = {
    .visible = true,
    .named = false,
  },
  [sym__newline] = {
    .visible = false,
    .named = true,
  },
  [sym_literal_content] = {
    .visible = true,
    .named = true,
  },
  [sym_source_file] = {
    .visible = true,
    .named = true,
  },
  [sym_directive] = {
    .visible = true,
    .named = true,
  },
  [sym_module_directive] = {
    .visible = true,
    .named = true,
  },
  [sym_version_directive] = {
    .visible = true,
    .named = true,
  },
  [sym_target_directive] = {
    .visible = true,
    .named = true,
  },
  [sym_imports_directive] = {
    .visible = true,
    .named = true,
  },
  [sym_target_name] = {
    .visible = true,
    .named = true,
  },
  [sym_import_list] = {
    .visible = true,
    .named = true,
  },
  [sym_anlu_block] = {
    .visible = true,
    .named = true,
  },
  [sym_anlu_header] = {
    .visible = true,
    .named = true,
  },
  [sym_purpose_section] = {
    .visible = true,
    .named = true,
  },
  [sym_description_text] = {
    .visible = true,
    .named = true,
  },
  [sym_inputs_section] = {
    .visible = true,
    .named = true,
  },
  [sym_input_item] = {
    .visible = true,
    .named = true,
  },
  [sym_input_constraints] = {
    .visible = true,
    .named = true,
  },
  [sym_guards_section] = {
    .visible = true,
    .named = true,
  },
  [sym_guard_item] = {
    .visible = true,
    .named = true,
  },
  [sym_guard_text] = {
    .visible = true,
    .named = true,
  },
  [sym_error_spec] = {
    .visible = true,
    .named = true,
  },
  [sym_error_call] = {
    .visible = true,
    .named = true,
  },
  [sym_error_args] = {
    .visible = true,
    .named = true,
  },
  [sym_error_text] = {
    .visible = true,
    .named = true,
  },
  [sym_logic_section] = {
    .visible = true,
    .named = true,
  },
  [sym_logic_item] = {
    .visible = true,
    .named = true,
  },
  [sym_logic_step] = {
    .visible = true,
    .named = true,
  },
  [sym_state_prefix] = {
    .visible = true,
    .named = true,
  },
  [sym_condition_prefix] = {
    .visible = true,
    .named = true,
  },
  [sym_condition_text] = {
    .visible = true,
    .named = true,
  },
  [sym_condition_token] = {
    .visible = true,
    .named = true,
  },
  [sym_step_text] = {
    .visible = true,
    .named = true,
  },
  [sym_output_binding] = {
    .visible = true,
    .named = true,
  },
  [sym_returns_section] = {
    .visible = true,
    .named = true,
  },
  [sym_returns_text] = {
    .visible = true,
    .named = true,
  },
  [sym_depends_section] = {
    .visible = true,
    .named = true,
  },
  [sym_depends_list] = {
    .visible = true,
    .named = true,
  },
  [sym_anlu_reference] = {
    .visible = true,
    .named = true,
  },
  [sym_edge_cases_section] = {
    .visible = true,
    .named = true,
  },
  [sym_edge_case_item] = {
    .visible = true,
    .named = true,
  },
  [sym_edge_condition_text] = {
    .visible = true,
    .named = true,
  },
  [sym_edge_behavior_text] = {
    .visible = true,
    .named = true,
  },
  [sym_type_block] = {
    .visible = true,
    .named = true,
  },
  [sym_type_header] = {
    .visible = true,
    .named = true,
  },
  [sym_extends_clause] = {
    .visible = true,
    .named = true,
  },
  [sym_type_field] = {
    .visible = true,
    .named = true,
  },
  [sym_field_constraints] = {
    .visible = true,
    .named = true,
  },
  [sym_type_close] = {
    .visible = true,
    .named = true,
  },
  [sym_test_block] = {
    .visible = true,
    .named = true,
  },
  [sym_test_header] = {
    .visible = true,
    .named = true,
  },
  [sym_test_assertion] = {
    .visible = true,
    .named = true,
  },
  [sym_test_call] = {
    .visible = true,
    .named = true,
  },
  [sym_test_args] = {
    .visible = true,
    .named = true,
  },
  [sym_test_value] = {
    .visible = true,
    .named = true,
  },
  [sym_test_close] = {
    .visible = true,
    .named = true,
  },
  [sym_literal_block] = {
    .visible = true,
    .named = true,
  },
  [sym_literal_header] = {
    .visible = true,
    .named = true,
  },
  [sym_literal_close] = {
    .visible = true,
    .named = true,
  },
  [sym_type_spec] = {
    .visible = true,
    .named = true,
  },
  [sym__base_type] = {
    .visible = false,
    .named = true,
  },
  [sym_primitive_type] = {
    .visible = true,
    .named = true,
  },
  [sym_list_type] = {
    .visible = true,
    .named = true,
  },
  [sym_map_type] = {
    .visible = true,
    .named = true,
  },
  [sym_custom_type] = {
    .visible = true,
    .named = true,
  },
  [sym_quoted_string] = {
    .visible = true,
    .named = true,
  },
  [sym_boolean] = {
    .visible = true,
    .named = true,
  },
  [sym_identifier] = {
    .visible = true,
    .named = true,
  },
  [sym_bullet] = {
    .visible = true,
    .named = true,
  },
  [sym_arrow] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_source_file_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_import_list_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_anlu_block_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_inputs_section_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_input_constraints_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_guards_section_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_error_args_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_logic_section_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_condition_text_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_depends_list_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_edge_cases_section_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_type_block_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_test_block_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_test_args_repeat1] = {
    .visible = false,
    .named = false,
  },
};

enum ts_field_identifiers {
  field_anlu = 1,
  field_base = 2,
  field_behavior = 3,
  field_call = 4,
  field_condition = 5,
  field_content = 6,
  field_dependencies = 7,
  field_description = 8,
  field_element = 9,
  field_error = 10,
  field_expected = 11,
  field_function = 12,
  field_header = 13,
  field_imports = 14,
  field_key = 15,
  field_language = 16,
  field_name = 17,
  field_number = 18,
  field_state = 19,
  field_target = 20,
  field_type = 21,
  field_value = 22,
  field_variable = 23,
  field_version = 24,
};

static const char * const ts_field_names[] = {
  [0] = NULL,
  [field_anlu] = "anlu",
  [field_base] = "base",
  [field_behavior] = "behavior",
  [field_call] = "call",
  [field_condition] = "condition",
  [field_content] = "content",
  [field_dependencies] = "dependencies",
  [field_description] = "description",
  [field_element] = "element",
  [field_error] = "error",
  [field_expected] = "expected",
  [field_function] = "function",
  [field_header] = "header",
  [field_imports] = "imports",
  [field_key] = "key",
  [field_language] = "language",
  [field_name] = "name",
  [field_number] = "number",
  [field_state] = "state",
  [field_target] = "target",
  [field_type] = "type",
  [field_value] = "value",
  [field_variable] = "variable",
  [field_version] = "version",
};

static const TSFieldMapSlice ts_field_map_slices[PRODUCTION_ID_COUNT] = {
  [1] = {.index = 0, .length = 1},
  [2] = {.index = 1, .length = 1},
  [3] = {.index = 2, .length = 1},
  [4] = {.index = 3, .length = 1},
  [5] = {.index = 4, .length = 1},
  [6] = {.index = 5, .length = 1},
  [7] = {.index = 6, .length = 1},
  [8] = {.index = 7, .length = 2},
  [9] = {.index = 9, .length = 1},
  [10] = {.index = 10, .length = 2},
  [11] = {.index = 12, .length = 2},
  [12] = {.index = 14, .length = 1},
  [13] = {.index = 15, .length = 2},
  [14] = {.index = 17, .length = 2},
  [15] = {.index = 19, .length = 1},
  [16] = {.index = 20, .length = 1},
  [17] = {.index = 21, .length = 1},
  [18] = {.index = 22, .length = 1},
  [19] = {.index = 23, .length = 2},
  [20] = {.index = 25, .length = 1},
  [21] = {.index = 26, .length = 1},
  [22] = {.index = 27, .length = 2},
  [23] = {.index = 29, .length = 1},
  [24] = {.index = 30, .length = 1},
  [25] = {.index = 31, .length = 1},
  [26] = {.index = 32, .length = 2},
  [27] = {.index = 34, .length = 2},
  [28] = {.index = 36, .length = 1},
};

static const TSFieldMapEntry ts_field_map_entries[] = {
  [0] =
    {field_name, 1},
  [1] =
    {field_version, 1},
  [2] =
    {field_target, 1},
  [3] =
    {field_imports, 1},
  [4] =
    {field_content, 1},
  [5] =
    {field_base, 1},
  [6] =
    {field_language, 1},
  [7] =
    {field_description, 1},
    {field_header, 0},
  [9] =
    {field_header, 0},
  [10] =
    {field_header, 0},
    {field_value, 1},
  [12] =
    {field_dependencies, 1},
    {field_header, 0},
  [14] =
    {field_function, 0},
  [15] =
    {field_name, 0},
    {field_type, 2},
  [17] =
    {field_call, 0},
    {field_expected, 2},
  [19] =
    {field_anlu, 2},
  [20] =
    {field_condition, 1},
  [21] =
    {field_description, 0},
  [22] =
    {field_element, 2},
  [23] =
    {field_name, 1},
    {field_type, 3},
  [25] =
    {field_number, 0},
  [26] =
    {field_description, 1},
  [27] =
    {field_condition, 1},
    {field_error, 3},
  [29] =
    {field_state, 1},
  [30] =
    {field_description, 2},
  [31] =
    {field_variable, 1},
  [32] =
    {field_behavior, 3},
    {field_condition, 1},
  [34] =
    {field_key, 2},
    {field_value, 4},
  [36] =
    {field_type, 0},
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
  [12] = 12,
  [13] = 13,
  [14] = 14,
  [15] = 15,
  [16] = 16,
  [17] = 17,
  [18] = 18,
  [19] = 19,
  [20] = 20,
  [21] = 21,
  [22] = 22,
  [23] = 23,
  [24] = 24,
  [25] = 25,
  [26] = 26,
  [27] = 27,
  [28] = 28,
  [29] = 29,
  [30] = 30,
  [31] = 31,
  [32] = 32,
  [33] = 33,
  [34] = 34,
  [35] = 35,
  [36] = 36,
  [37] = 37,
  [38] = 38,
  [39] = 39,
  [40] = 40,
  [41] = 41,
  [42] = 42,
  [43] = 43,
  [44] = 44,
  [45] = 45,
  [46] = 46,
  [47] = 47,
  [48] = 48,
  [49] = 49,
  [50] = 50,
  [51] = 51,
  [52] = 52,
  [53] = 53,
  [54] = 54,
  [55] = 55,
  [56] = 56,
  [57] = 57,
  [58] = 58,
  [59] = 59,
  [60] = 60,
  [61] = 61,
  [62] = 62,
  [63] = 63,
  [64] = 64,
  [65] = 65,
  [66] = 66,
  [67] = 67,
  [68] = 68,
  [69] = 69,
  [70] = 70,
  [71] = 71,
  [72] = 72,
  [73] = 73,
  [74] = 74,
  [75] = 75,
  [76] = 76,
  [77] = 77,
  [78] = 78,
  [79] = 79,
  [80] = 80,
  [81] = 81,
  [82] = 82,
  [83] = 83,
  [84] = 84,
  [85] = 85,
  [86] = 86,
  [87] = 87,
  [88] = 88,
  [89] = 89,
  [90] = 90,
  [91] = 91,
  [92] = 92,
  [93] = 93,
  [94] = 94,
  [95] = 95,
  [96] = 96,
  [97] = 97,
  [98] = 98,
  [99] = 99,
  [100] = 100,
  [101] = 101,
  [102] = 102,
  [103] = 103,
  [104] = 104,
  [105] = 105,
  [106] = 106,
  [107] = 107,
  [108] = 108,
  [109] = 109,
  [110] = 110,
  [111] = 111,
  [112] = 112,
  [113] = 113,
  [114] = 114,
  [115] = 115,
  [116] = 116,
  [117] = 117,
  [118] = 118,
  [119] = 119,
  [120] = 120,
  [121] = 121,
  [122] = 122,
  [123] = 123,
  [124] = 124,
  [125] = 125,
  [126] = 126,
  [127] = 127,
  [128] = 128,
  [129] = 129,
  [130] = 130,
  [131] = 131,
  [132] = 132,
  [133] = 133,
  [134] = 134,
  [135] = 135,
  [136] = 136,
  [137] = 137,
  [138] = 138,
  [139] = 139,
  [140] = 140,
  [141] = 141,
  [142] = 142,
  [143] = 143,
  [144] = 144,
  [145] = 145,
  [146] = 146,
  [147] = 147,
  [148] = 148,
  [149] = 149,
  [150] = 150,
  [151] = 151,
  [152] = 152,
  [153] = 153,
  [154] = 154,
  [155] = 155,
  [156] = 156,
  [157] = 157,
  [158] = 158,
  [159] = 159,
  [160] = 160,
  [161] = 161,
  [162] = 162,
  [163] = 163,
  [164] = 164,
  [165] = 165,
  [166] = 166,
  [167] = 167,
  [168] = 168,
  [169] = 169,
  [170] = 170,
  [171] = 171,
  [172] = 172,
  [173] = 173,
  [174] = 174,
  [175] = 175,
  [176] = 176,
  [177] = 177,
  [178] = 178,
  [179] = 179,
  [180] = 180,
  [181] = 181,
  [182] = 182,
  [183] = 183,
  [184] = 184,
  [185] = 185,
  [186] = 186,
  [187] = 187,
  [188] = 188,
  [189] = 189,
  [190] = 190,
  [191] = 191,
  [192] = 192,
  [193] = 193,
  [194] = 194,
  [195] = 195,
  [196] = 196,
  [197] = 197,
  [198] = 198,
  [199] = 199,
  [200] = 200,
  [201] = 201,
  [202] = 202,
  [203] = 203,
  [204] = 204,
  [205] = 205,
  [206] = 206,
  [207] = 207,
  [208] = 208,
  [209] = 209,
  [210] = 210,
  [211] = 211,
  [212] = 212,
  [213] = 206,
  [214] = 112,
  [215] = 215,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(187);
      ADVANCE_MAP(
        '\n', 316,
        '\r', 1,
        '"', 5,
        '#', 189,
        '\'', 14,
        '(', 219,
        ')', 220,
        '*', 313,
        ',', 199,
        '-', 312,
        '.', 222,
        ':', 209,
        '=', 267,
        '?', 289,
        '@', 58,
        'E', 142,
        'F', 26,
        'L', 161,
        'P', 177,
        'R', 145,
        'T', 100,
        '[', 200,
        ']', 202,
        'a', 76,
        'b', 90,
        'e', 135,
        'f', 32,
        'l', 60,
        'm', 27,
        'n', 88,
        'o', 54,
        'p', 137,
        'r', 25,
        's', 118,
        't', 84,
        'v', 86,
        '{', 281,
        '}', 284,
        0x2022, 311,
        0x2192, 314,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(0);
      if (('+' <= lookahead && lookahead <= '/')) ADVANCE(270);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(146);
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(178);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(152);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(268);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(223);
      END_STATE();
    case 1:
      if (lookahead == '\n') ADVANCE(316);
      END_STATE();
    case 2:
      ADVANCE_MAP(
        '\n', 316,
        '\r', 1,
        '"', 5,
        '#', 189,
        '\'', 14,
        ')', 220,
        '-', 24,
        'F', 228,
        'T', 250,
        'f', 230,
        't', 253,
        0x2192, 314,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(299);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 3:
      ADVANCE_MAP(
        '"', 5,
        '#', 189,
        '\'', 14,
        ')', 220,
        '*', 313,
        '-', 312,
        '}', 284,
        0x2022, 311,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(3);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 4:
      if (lookahead == '"') ADVANCE(5);
      if (lookahead == '#') ADVANCE(189);
      if (lookahead == '\'') ADVANCE(14);
      if (lookahead == 'o') ADVANCE(248);
      if (lookahead == 'r') ADVANCE(237);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(4);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 5:
      if (lookahead == '"') ADVANCE(301);
      if (lookahead != 0) ADVANCE(5);
      END_STATE();
    case 6:
      if (lookahead == '#') ADVANCE(189);
      if (lookahead == '[') ADVANCE(200);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(6);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(203);
      END_STATE();
    case 7:
      if (lookahead == '#') ADVANCE(189);
      if (lookahead == 'a') ADVANCE(244);
      if (lookahead == 'n') ADVANCE(246);
      if (lookahead == 'o') ADVANCE(251);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(7);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(268);
      if (lookahead == '(' ||
          lookahead == ')' ||
          lookahead == '[' ||
          lookahead == ']') ADVANCE(269);
      if (lookahead == '*' ||
          lookahead == '+' ||
          lookahead == '-' ||
          lookahead == '/') ADVANCE(270);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(265);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 8:
      if (lookahead == '#') ADVANCE(189);
      if (lookahead == 'a') ADVANCE(244);
      if (lookahead == 'n') ADVANCE(246);
      if (lookahead == 'o') ADVANCE(251);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(8);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(262);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(268);
      if (lookahead == '(' ||
          lookahead == ')' ||
          lookahead == '[' ||
          lookahead == ']') ADVANCE(269);
      if (lookahead == '*' ||
          lookahead == '+' ||
          lookahead == '-' ||
          lookahead == '/') ADVANCE(270);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(265);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 9:
      ADVANCE_MAP(
        '#', 189,
        'a', 80,
        'b', 90,
        'l', 59,
        'm', 27,
        'n', 130,
        's', 118,
        'v', 86,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(9);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(15);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(283);
      END_STATE();
    case 10:
      if (lookahead == '#') ADVANCE(189);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(205);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(206);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(207);
      END_STATE();
    case 11:
      if (lookahead == '#') ADVANCE(189);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(11);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(224);
      END_STATE();
    case 12:
      if (lookahead == '#') ADVANCE(188);
      if (lookahead == '[') ADVANCE(201);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(215);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(217);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(218);
      END_STATE();
    case 13:
      if (lookahead == '#') ADVANCE(188);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(216);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(217);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(218);
      END_STATE();
    case 14:
      if (lookahead == '\'') ADVANCE(302);
      if (lookahead != 0) ADVANCE(14);
      END_STATE();
    case 15:
      if (lookahead == '.') ADVANCE(183);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(15);
      END_STATE();
    case 16:
      if (lookahead == ':') ADVANCE(221);
      END_STATE();
    case 17:
      if (lookahead == ':') ADVANCE(214);
      END_STATE();
    case 18:
      if (lookahead == ':') ADVANCE(208);
      END_STATE();
    case 19:
      if (lookahead == ':') ADVANCE(204);
      END_STATE();
    case 20:
      if (lookahead == ':') ADVANCE(277);
      END_STATE();
    case 21:
      if (lookahead == ':') ADVANCE(278);
      END_STATE();
    case 22:
      if (lookahead == ':') ADVANCE(279);
      END_STATE();
    case 23:
      if (lookahead == '=') ADVANCE(286);
      END_STATE();
    case 24:
      if (lookahead == '>') ADVANCE(315);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(299);
      END_STATE();
    case 25:
      if (lookahead == 'E') ADVANCE(176);
      if (lookahead == 'e') ADVANCE(99);
      if (lookahead == 'u') ADVANCE(114);
      END_STATE();
    case 26:
      if (lookahead == 'a') ADVANCE(70);
      END_STATE();
    case 27:
      if (lookahead == 'a') ADVANCE(94);
      END_STATE();
    case 28:
      if (lookahead == 'a') ADVANCE(101);
      if (lookahead == 'e') ADVANCE(115);
      if (lookahead == 'y') ADVANCE(97);
      END_STATE();
    case 29:
      if (lookahead == 'a') ADVANCE(68);
      END_STATE();
    case 30:
      if (lookahead == 'a') ADVANCE(69);
      END_STATE();
    case 31:
      if (lookahead == 'a') ADVANCE(78);
      END_STATE();
    case 32:
      if (lookahead == 'a') ADVANCE(73);
      END_STATE();
    case 33:
      if (lookahead == 'b') ADVANCE(52);
      END_STATE();
    case 34:
      if (lookahead == 'c') ADVANCE(105);
      END_STATE();
    case 35:
      if (lookahead == 'd') ADVANCE(271);
      if (lookahead == 'y') ADVANCE(294);
      END_STATE();
    case 36:
      if (lookahead == 'd') ADVANCE(293);
      END_STATE();
    case 37:
      if (lookahead == 'd') ADVANCE(210);
      END_STATE();
    case 38:
      if (lookahead == 'd') ADVANCE(134);
      END_STATE();
    case 39:
      if (lookahead == 'd') ADVANCE(110);
      END_STATE();
    case 40:
      if (lookahead == 'e') ADVANCE(307);
      END_STATE();
    case 41:
      if (lookahead == 'e') ADVANCE(303);
      END_STATE();
    case 42:
      if (lookahead == 'e') ADVANCE(280);
      END_STATE();
    case 43:
      if (lookahead == 'e') ADVANCE(309);
      END_STATE();
    case 44:
      if (lookahead == 'e') ADVANCE(305);
      END_STATE();
    case 45:
      if (lookahead == 'e') ADVANCE(190);
      END_STATE();
    case 46:
      if (lookahead == 'e') ADVANCE(82);
      END_STATE();
    case 47:
      if (lookahead == 'e') ADVANCE(31);
      END_STATE();
    case 48:
      if (lookahead == 'e') ADVANCE(103);
      END_STATE();
    case 49:
      if (lookahead == 'e') ADVANCE(109);
      END_STATE();
    case 50:
      if (lookahead == 'e') ADVANCE(37);
      END_STATE();
    case 51:
      if (lookahead == 'e') ADVANCE(108);
      END_STATE();
    case 52:
      if (lookahead == 'e') ADVANCE(102);
      END_STATE();
    case 53:
      if (lookahead == 'e') ADVANCE(124);
      END_STATE();
    case 54:
      if (lookahead == 'f') ADVANCE(296);
      if (lookahead == 'p') ADVANCE(126);
      if (lookahead == 'r') ADVANCE(273);
      END_STATE();
    case 55:
      if (lookahead == 'g') ADVANCE(291);
      END_STATE();
    case 56:
      if (lookahead == 'g') ADVANCE(53);
      END_STATE();
    case 57:
      if (lookahead == 'h') ADVANCE(92);
      END_STATE();
    case 58:
      if (lookahead == 'i') ADVANCE(75);
      if (lookahead == 'l') ADVANCE(65);
      if (lookahead == 'm') ADVANCE(85);
      if (lookahead == 't') ADVANCE(28);
      if (lookahead == 'v') ADVANCE(48);
      END_STATE();
    case 59:
      if (lookahead == 'i') ADVANCE(112);
      END_STATE();
    case 60:
      if (lookahead == 'i') ADVANCE(112);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(153);
      END_STATE();
    case 61:
      if (lookahead == 'i') ADVANCE(36);
      END_STATE();
    case 62:
      if (lookahead == 'i') ADVANCE(81);
      END_STATE();
    case 63:
      if (lookahead == 'i') ADVANCE(98);
      END_STATE();
    case 64:
      if (lookahead == 'i') ADVANCE(89);
      END_STATE();
    case 65:
      if (lookahead == 'i') ADVANCE(129);
      END_STATE();
    case 66:
      if (lookahead == 'i') ADVANCE(107);
      END_STATE();
    case 67:
      if (lookahead == 'i') ADVANCE(93);
      END_STATE();
    case 68:
      if (lookahead == 'l') ADVANCE(288);
      END_STATE();
    case 69:
      if (lookahead == 'l') ADVANCE(212);
      END_STATE();
    case 70:
      if (lookahead == 'l') ADVANCE(113);
      END_STATE();
    case 71:
      if (lookahead == 'l') ADVANCE(47);
      END_STATE();
    case 72:
      if (lookahead == 'l') ADVANCE(45);
      END_STATE();
    case 73:
      if (lookahead == 'l') ADVANCE(116);
      END_STATE();
    case 74:
      if (lookahead == 'm') ADVANCE(33);
      END_STATE();
    case 75:
      if (lookahead == 'm') ADVANCE(95);
      END_STATE();
    case 76:
      if (lookahead == 'n') ADVANCE(35);
      END_STATE();
    case 77:
      if (lookahead == 'n') ADVANCE(196);
      END_STATE();
    case 78:
      if (lookahead == 'n') ADVANCE(292);
      END_STATE();
    case 79:
      if (lookahead == 'n') ADVANCE(191);
      END_STATE();
    case 80:
      if (lookahead == 'n') ADVANCE(136);
      END_STATE();
    case 81:
      if (lookahead == 'n') ADVANCE(55);
      END_STATE();
    case 82:
      if (lookahead == 'n') ADVANCE(39);
      END_STATE();
    case 83:
      if (lookahead == 'n') ADVANCE(30);
      END_STATE();
    case 84:
      if (lookahead == 'o') ADVANCE(298);
      if (lookahead == 'r') ADVANCE(132);
      if (lookahead == 'y') ADVANCE(96);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(147);
      END_STATE();
    case 85:
      if (lookahead == 'o') ADVANCE(38);
      END_STATE();
    case 86:
      if (lookahead == 'o') ADVANCE(61);
      END_STATE();
    case 87:
      if (lookahead == 'o') ADVANCE(71);
      END_STATE();
    case 88:
      if (lookahead == 'o') ADVANCE(119);
      if (lookahead == 'u') ADVANCE(74);
      END_STATE();
    case 89:
      if (lookahead == 'o') ADVANCE(83);
      END_STATE();
    case 90:
      if (lookahead == 'o') ADVANCE(87);
      END_STATE();
    case 91:
      if (lookahead == 'o') ADVANCE(106);
      END_STATE();
    case 92:
      if (lookahead == 'o') ADVANCE(77);
      END_STATE();
    case 93:
      if (lookahead == 'o') ADVANCE(79);
      END_STATE();
    case 94:
      if (lookahead == 'p') ADVANCE(297);
      END_STATE();
    case 95:
      if (lookahead == 'p') ADVANCE(91);
      END_STATE();
    case 96:
      if (lookahead == 'p') ADVANCE(49);
      END_STATE();
    case 97:
      if (lookahead == 'p') ADVANCE(42);
      END_STATE();
    case 98:
      if (lookahead == 'p') ADVANCE(125);
      END_STATE();
    case 99:
      if (lookahead == 'q') ADVANCE(133);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(180);
      END_STATE();
    case 100:
      if (lookahead == 'r') ADVANCE(131);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(147);
      END_STATE();
    case 101:
      if (lookahead == 'r') ADVANCE(56);
      END_STATE();
    case 102:
      if (lookahead == 'r') ADVANCE(290);
      END_STATE();
    case 103:
      if (lookahead == 'r') ADVANCE(117);
      END_STATE();
    case 104:
      if (lookahead == 'r') ADVANCE(62);
      END_STATE();
    case 105:
      if (lookahead == 'r') ADVANCE(63);
      END_STATE();
    case 106:
      if (lookahead == 'r') ADVANCE(128);
      END_STATE();
    case 107:
      if (lookahead == 'r') ADVANCE(50);
      END_STATE();
    case 108:
      if (lookahead == 'r') ADVANCE(29);
      END_STATE();
    case 109:
      if (lookahead == 's') ADVANCE(34);
      END_STATE();
    case 110:
      if (lookahead == 's') ADVANCE(282);
      END_STATE();
    case 111:
      if (lookahead == 's') ADVANCE(193);
      END_STATE();
    case 112:
      if (lookahead == 's') ADVANCE(121);
      END_STATE();
    case 113:
      if (lookahead == 's') ADVANCE(43);
      END_STATE();
    case 114:
      if (lookahead == 's') ADVANCE(122);
      END_STATE();
    case 115:
      if (lookahead == 's') ADVANCE(123);
      END_STATE();
    case 116:
      if (lookahead == 's') ADVANCE(44);
      END_STATE();
    case 117:
      if (lookahead == 's') ADVANCE(67);
      END_STATE();
    case 118:
      if (lookahead == 't') ADVANCE(104);
      END_STATE();
    case 119:
      if (lookahead == 't') ADVANCE(275);
      END_STATE();
    case 120:
      if (lookahead == 't') ADVANCE(57);
      END_STATE();
    case 121:
      if (lookahead == 't') ADVANCE(295);
      END_STATE();
    case 122:
      if (lookahead == 't') ADVANCE(198);
      END_STATE();
    case 123:
      if (lookahead == 't') ADVANCE(285);
      END_STATE();
    case 124:
      if (lookahead == 't') ADVANCE(192);
      END_STATE();
    case 125:
      if (lookahead == 't') ADVANCE(197);
      END_STATE();
    case 126:
      if (lookahead == 't') ADVANCE(64);
      END_STATE();
    case 127:
      if (lookahead == 't') ADVANCE(46);
      END_STATE();
    case 128:
      if (lookahead == 't') ADVANCE(111);
      END_STATE();
    case 129:
      if (lookahead == 't') ADVANCE(51);
      END_STATE();
    case 130:
      if (lookahead == 'u') ADVANCE(74);
      END_STATE();
    case 131:
      if (lookahead == 'u') ADVANCE(40);
      END_STATE();
    case 132:
      if (lookahead == 'u') ADVANCE(41);
      END_STATE();
    case 133:
      if (lookahead == 'u') ADVANCE(66);
      END_STATE();
    case 134:
      if (lookahead == 'u') ADVANCE(72);
      END_STATE();
    case 135:
      if (lookahead == 'x') ADVANCE(127);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(154);
      END_STATE();
    case 136:
      if (lookahead == 'y') ADVANCE(294);
      END_STATE();
    case 137:
      if (lookahead == 'y') ADVANCE(120);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(166);
      END_STATE();
    case 138:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(165);
      END_STATE();
    case 139:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(173);
      END_STATE();
    case 140:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(16);
      END_STATE();
    case 141:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(139);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') ADVANCE(141);
      END_STATE();
    case 142:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(154);
      END_STATE();
    case 143:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(168);
      END_STATE();
    case 144:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(172);
      END_STATE();
    case 145:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(176);
      END_STATE();
    case 146:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(164);
      END_STATE();
    case 147:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(156);
      END_STATE();
    case 148:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(181);
      END_STATE();
    case 149:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(159);
      END_STATE();
    case 150:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(19);
      END_STATE();
    case 151:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(174);
      END_STATE();
    case 152:
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(225);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(163);
      END_STATE();
    case 153:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(155);
      END_STATE();
    case 154:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(148);
      END_STATE();
    case 155:
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(140);
      END_STATE();
    case 156:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(226);
      END_STATE();
    case 157:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(163);
      END_STATE();
    case 158:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(170);
      END_STATE();
    case 159:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(144);
      END_STATE();
    case 160:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(171);
      END_STATE();
    case 161:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(153);
      END_STATE();
    case 162:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(160);
      END_STATE();
    case 163:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(179);
      END_STATE();
    case 164:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(149);
      END_STATE();
    case 165:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(143);
      END_STATE();
    case 166:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(162);
      END_STATE();
    case 167:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(158);
      END_STATE();
    case 168:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(17);
      END_STATE();
    case 169:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(18);
      END_STATE();
    case 170:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(20);
      END_STATE();
    case 171:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(150);
      END_STATE();
    case 172:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(21);
      END_STATE();
    case 173:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(151);
      END_STATE();
    case 174:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(22);
      END_STATE();
    case 175:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(169);
      END_STATE();
    case 176:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(180);
      END_STATE();
    case 177:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(166);
      END_STATE();
    case 178:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(138);
      END_STATE();
    case 179:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(175);
      END_STATE();
    case 180:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(167);
      END_STATE();
    case 181:
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') ADVANCE(141);
      END_STATE();
    case 182:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(300);
      END_STATE();
    case 183:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(194);
      END_STATE();
    case 184:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(195);
      END_STATE();
    case 185:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(266);
      END_STATE();
    case 186:
      if (eof) ADVANCE(187);
      ADVANCE_MAP(
        '\n', 316,
        '\r', 1,
        '#', 189,
        '(', 219,
        ')', 220,
        '*', 313,
        ',', 199,
        '-', 312,
        ':', 209,
        '=', 23,
        '@', 58,
        '[', 200,
        ']', 202,
        '{', 281,
        0x2022, 311,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(186);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(146);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(142);
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(178);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(157);
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(161);
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(177);
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(145);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(223);
      END_STATE();
    case 187:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 188:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == '-' ||
          lookahead == 0x2192) ADVANCE(189);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(188);
      END_STATE();
    case 189:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(189);
      END_STATE();
    case 190:
      ACCEPT_TOKEN(anon_sym_ATmodule);
      END_STATE();
    case 191:
      ACCEPT_TOKEN(anon_sym_ATversion);
      END_STATE();
    case 192:
      ACCEPT_TOKEN(anon_sym_ATtarget);
      END_STATE();
    case 193:
      ACCEPT_TOKEN(anon_sym_ATimports);
      END_STATE();
    case 194:
      ACCEPT_TOKEN(sym_version_string);
      if (lookahead == '.') ADVANCE(184);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(194);
      END_STATE();
    case 195:
      ACCEPT_TOKEN(sym_version_string);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(195);
      END_STATE();
    case 196:
      ACCEPT_TOKEN(anon_sym_python);
      END_STATE();
    case 197:
      ACCEPT_TOKEN(anon_sym_typescript);
      END_STATE();
    case 198:
      ACCEPT_TOKEN(anon_sym_rust);
      END_STATE();
    case 199:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 200:
      ACCEPT_TOKEN(anon_sym_LBRACK);
      END_STATE();
    case 201:
      ACCEPT_TOKEN(anon_sym_LBRACK);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(218);
      END_STATE();
    case 202:
      ACCEPT_TOKEN(anon_sym_RBRACK);
      END_STATE();
    case 203:
      ACCEPT_TOKEN(sym_anlu_identifier);
      if (lookahead == '-' ||
          lookahead == '.' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(203);
      END_STATE();
    case 204:
      ACCEPT_TOKEN(aux_sym_purpose_section_token1);
      END_STATE();
    case 205:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (lookahead == '#') ADVANCE(189);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(205);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(206);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(207);
      END_STATE();
    case 206:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(206);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(207);
      END_STATE();
    case 207:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(207);
      END_STATE();
    case 208:
      ACCEPT_TOKEN(aux_sym_inputs_section_token1);
      END_STATE();
    case 209:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 210:
      ACCEPT_TOKEN(anon_sym_required);
      END_STATE();
    case 211:
      ACCEPT_TOKEN(anon_sym_required);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 212:
      ACCEPT_TOKEN(anon_sym_optional);
      END_STATE();
    case 213:
      ACCEPT_TOKEN(anon_sym_optional);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 214:
      ACCEPT_TOKEN(aux_sym_guards_section_token1);
      END_STATE();
    case 215:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead == '#') ADVANCE(188);
      if (lookahead == '[') ADVANCE(201);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(215);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(217);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(218);
      END_STATE();
    case 216:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead == '#') ADVANCE(188);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(216);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(217);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(218);
      END_STATE();
    case 217:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(218);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(218);
      END_STATE();
    case 218:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(218);
      END_STATE();
    case 219:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 220:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 221:
      ACCEPT_TOKEN(aux_sym_logic_section_token1);
      END_STATE();
    case 222:
      ACCEPT_TOKEN(anon_sym_DOT);
      END_STATE();
    case 223:
      ACCEPT_TOKEN(sym_step_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(223);
      END_STATE();
    case 224:
      ACCEPT_TOKEN(sym_state_name);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(224);
      END_STATE();
    case 225:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token1);
      END_STATE();
    case 226:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token2);
      END_STATE();
    case 227:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token2);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 228:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(241);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 229:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(242);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 230:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(243);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 231:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'd') ADVANCE(272);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 232:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'd') ADVANCE(211);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 233:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(308);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 234:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(304);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 235:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(310);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 236:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(306);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 237:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(249);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 238:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(232);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 239:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'i') ADVANCE(247);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 240:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'i') ADVANCE(252);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 241:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(254);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 242:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(213);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 243:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(255);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 244:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'n') ADVANCE(231);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 245:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'n') ADVANCE(229);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 246:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'o') ADVANCE(256);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 247:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'o') ADVANCE(245);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 248:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'p') ADVANCE(257);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 249:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'q') ADVANCE(260);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 250:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(258);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 251:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(274);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 252:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(238);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 253:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(259);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 254:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 's') ADVANCE(235);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 255:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 's') ADVANCE(236);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 256:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 't') ADVANCE(276);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 257:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 't') ADVANCE(239);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 258:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(233);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 259:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(234);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 260:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(240);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 261:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(263);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 262:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(261);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 263:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(227);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 264:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 265:
      ACCEPT_TOKEN(aux_sym_condition_token_token2);
      if (lookahead == '.') ADVANCE(185);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(265);
      END_STATE();
    case 266:
      ACCEPT_TOKEN(aux_sym_condition_token_token2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(266);
      END_STATE();
    case 267:
      ACCEPT_TOKEN(aux_sym_condition_token_token3);
      if (lookahead == '=') ADVANCE(287);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(268);
      END_STATE();
    case 268:
      ACCEPT_TOKEN(aux_sym_condition_token_token3);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(268);
      END_STATE();
    case 269:
      ACCEPT_TOKEN(aux_sym_condition_token_token4);
      END_STATE();
    case 270:
      ACCEPT_TOKEN(aux_sym_condition_token_token5);
      END_STATE();
    case 271:
      ACCEPT_TOKEN(anon_sym_and);
      END_STATE();
    case 272:
      ACCEPT_TOKEN(anon_sym_and);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 273:
      ACCEPT_TOKEN(anon_sym_or);
      END_STATE();
    case 274:
      ACCEPT_TOKEN(anon_sym_or);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 275:
      ACCEPT_TOKEN(anon_sym_not);
      END_STATE();
    case 276:
      ACCEPT_TOKEN(anon_sym_not);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 277:
      ACCEPT_TOKEN(aux_sym_returns_section_token1);
      END_STATE();
    case 278:
      ACCEPT_TOKEN(aux_sym_depends_section_token1);
      END_STATE();
    case 279:
      ACCEPT_TOKEN(aux_sym_edge_cases_section_token1);
      END_STATE();
    case 280:
      ACCEPT_TOKEN(anon_sym_ATtype);
      END_STATE();
    case 281:
      ACCEPT_TOKEN(anon_sym_LBRACE);
      END_STATE();
    case 282:
      ACCEPT_TOKEN(anon_sym_extends);
      END_STATE();
    case 283:
      ACCEPT_TOKEN(sym_type_name);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(283);
      END_STATE();
    case 284:
      ACCEPT_TOKEN(anon_sym_RBRACE);
      END_STATE();
    case 285:
      ACCEPT_TOKEN(anon_sym_ATtest);
      END_STATE();
    case 286:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      END_STATE();
    case 287:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(268);
      END_STATE();
    case 288:
      ACCEPT_TOKEN(anon_sym_ATliteral);
      END_STATE();
    case 289:
      ACCEPT_TOKEN(anon_sym_QMARK);
      END_STATE();
    case 290:
      ACCEPT_TOKEN(anon_sym_number);
      END_STATE();
    case 291:
      ACCEPT_TOKEN(anon_sym_string);
      END_STATE();
    case 292:
      ACCEPT_TOKEN(anon_sym_boolean);
      END_STATE();
    case 293:
      ACCEPT_TOKEN(anon_sym_void);
      END_STATE();
    case 294:
      ACCEPT_TOKEN(anon_sym_any);
      END_STATE();
    case 295:
      ACCEPT_TOKEN(anon_sym_list);
      END_STATE();
    case 296:
      ACCEPT_TOKEN(anon_sym_of);
      END_STATE();
    case 297:
      ACCEPT_TOKEN(anon_sym_map);
      END_STATE();
    case 298:
      ACCEPT_TOKEN(anon_sym_to);
      END_STATE();
    case 299:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(182);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(299);
      END_STATE();
    case 300:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(300);
      END_STATE();
    case 301:
      ACCEPT_TOKEN(aux_sym_quoted_string_token1);
      END_STATE();
    case 302:
      ACCEPT_TOKEN(aux_sym_quoted_string_token2);
      END_STATE();
    case 303:
      ACCEPT_TOKEN(anon_sym_true);
      END_STATE();
    case 304:
      ACCEPT_TOKEN(anon_sym_true);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 305:
      ACCEPT_TOKEN(anon_sym_false);
      END_STATE();
    case 306:
      ACCEPT_TOKEN(anon_sym_false);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 307:
      ACCEPT_TOKEN(anon_sym_True);
      END_STATE();
    case 308:
      ACCEPT_TOKEN(anon_sym_True);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 309:
      ACCEPT_TOKEN(anon_sym_False);
      END_STATE();
    case 310:
      ACCEPT_TOKEN(anon_sym_False);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(264);
      END_STATE();
    case 311:
      ACCEPT_TOKEN(anon_sym_u2022);
      END_STATE();
    case 312:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 313:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 314:
      ACCEPT_TOKEN(anon_sym_u2192);
      END_STATE();
    case 315:
      ACCEPT_TOKEN(anon_sym_DASH_GT);
      END_STATE();
    case 316:
      ACCEPT_TOKEN(sym__newline);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0, .external_lex_state = 1},
  [1] = {.lex_state = 186},
  [2] = {.lex_state = 186},
  [3] = {.lex_state = 186},
  [4] = {.lex_state = 186},
  [5] = {.lex_state = 186},
  [6] = {.lex_state = 186},
  [7] = {.lex_state = 186},
  [8] = {.lex_state = 186},
  [9] = {.lex_state = 186},
  [10] = {.lex_state = 186},
  [11] = {.lex_state = 186},
  [12] = {.lex_state = 186},
  [13] = {.lex_state = 186},
  [14] = {.lex_state = 186},
  [15] = {.lex_state = 186},
  [16] = {.lex_state = 186},
  [17] = {.lex_state = 186},
  [18] = {.lex_state = 186},
  [19] = {.lex_state = 186},
  [20] = {.lex_state = 186},
  [21] = {.lex_state = 186},
  [22] = {.lex_state = 186},
  [23] = {.lex_state = 186},
  [24] = {.lex_state = 186},
  [25] = {.lex_state = 2},
  [26] = {.lex_state = 9},
  [27] = {.lex_state = 9},
  [28] = {.lex_state = 9},
  [29] = {.lex_state = 9},
  [30] = {.lex_state = 9},
  [31] = {.lex_state = 9},
  [32] = {.lex_state = 2},
  [33] = {.lex_state = 2},
  [34] = {.lex_state = 7},
  [35] = {.lex_state = 8},
  [36] = {.lex_state = 8},
  [37] = {.lex_state = 186},
  [38] = {.lex_state = 186},
  [39] = {.lex_state = 186},
  [40] = {.lex_state = 186},
  [41] = {.lex_state = 186},
  [42] = {.lex_state = 3},
  [43] = {.lex_state = 186},
  [44] = {.lex_state = 186},
  [45] = {.lex_state = 186},
  [46] = {.lex_state = 186},
  [47] = {.lex_state = 186},
  [48] = {.lex_state = 186},
  [49] = {.lex_state = 3},
  [50] = {.lex_state = 186},
  [51] = {.lex_state = 186},
  [52] = {.lex_state = 8},
  [53] = {.lex_state = 3},
  [54] = {.lex_state = 4},
  [55] = {.lex_state = 3},
  [56] = {.lex_state = 3},
  [57] = {.lex_state = 12},
  [58] = {.lex_state = 3},
  [59] = {.lex_state = 3},
  [60] = {.lex_state = 186},
  [61] = {.lex_state = 186},
  [62] = {.lex_state = 10},
  [63] = {.lex_state = 186},
  [64] = {.lex_state = 186},
  [65] = {.lex_state = 3},
  [66] = {.lex_state = 3},
  [67] = {.lex_state = 3},
  [68] = {.lex_state = 3},
  [69] = {.lex_state = 2},
  [70] = {.lex_state = 2},
  [71] = {.lex_state = 3},
  [72] = {.lex_state = 3},
  [73] = {.lex_state = 3},
  [74] = {.lex_state = 2},
  [75] = {.lex_state = 0},
  [76] = {.lex_state = 0},
  [77] = {.lex_state = 6},
  [78] = {.lex_state = 0},
  [79] = {.lex_state = 0},
  [80] = {.lex_state = 2},
  [81] = {.lex_state = 0},
  [82] = {.lex_state = 0},
  [83] = {.lex_state = 0},
  [84] = {.lex_state = 13},
  [85] = {.lex_state = 0},
  [86] = {.lex_state = 186},
  [87] = {.lex_state = 186},
  [88] = {.lex_state = 186},
  [89] = {.lex_state = 186},
  [90] = {.lex_state = 186},
  [91] = {.lex_state = 0},
  [92] = {.lex_state = 2},
  [93] = {.lex_state = 0},
  [94] = {.lex_state = 2},
  [95] = {.lex_state = 0},
  [96] = {.lex_state = 3},
  [97] = {.lex_state = 0},
  [98] = {.lex_state = 0},
  [99] = {.lex_state = 186},
  [100] = {.lex_state = 2},
  [101] = {.lex_state = 0},
  [102] = {.lex_state = 6},
  [103] = {.lex_state = 0},
  [104] = {.lex_state = 0},
  [105] = {.lex_state = 186},
  [106] = {.lex_state = 0},
  [107] = {.lex_state = 0},
  [108] = {.lex_state = 0},
  [109] = {.lex_state = 186},
  [110] = {.lex_state = 0},
  [111] = {.lex_state = 186},
  [112] = {.lex_state = 10},
  [113] = {.lex_state = 0},
  [114] = {.lex_state = 0},
  [115] = {.lex_state = 13},
  [116] = {.lex_state = 13},
  [117] = {.lex_state = 3},
  [118] = {.lex_state = 10},
  [119] = {.lex_state = 0},
  [120] = {.lex_state = 0},
  [121] = {.lex_state = 10},
  [122] = {.lex_state = 2},
  [123] = {.lex_state = 13},
  [124] = {.lex_state = 186},
  [125] = {.lex_state = 0},
  [126] = {.lex_state = 3},
  [127] = {.lex_state = 13},
  [128] = {.lex_state = 10},
  [129] = {.lex_state = 3},
  [130] = {.lex_state = 0},
  [131] = {.lex_state = 3},
  [132] = {.lex_state = 13},
  [133] = {.lex_state = 3},
  [134] = {.lex_state = 3},
  [135] = {.lex_state = 3},
  [136] = {.lex_state = 0},
  [137] = {.lex_state = 3},
  [138] = {.lex_state = 186},
  [139] = {.lex_state = 0},
  [140] = {.lex_state = 0},
  [141] = {.lex_state = 0},
  [142] = {.lex_state = 0},
  [143] = {.lex_state = 0},
  [144] = {.lex_state = 0},
  [145] = {.lex_state = 0},
  [146] = {.lex_state = 186},
  [147] = {.lex_state = 0, .external_lex_state = 1},
  [148] = {.lex_state = 0},
  [149] = {.lex_state = 0},
  [150] = {.lex_state = 6},
  [151] = {.lex_state = 0},
  [152] = {.lex_state = 9},
  [153] = {.lex_state = 0},
  [154] = {.lex_state = 11},
  [155] = {.lex_state = 0},
  [156] = {.lex_state = 0},
  [157] = {.lex_state = 0},
  [158] = {.lex_state = 0},
  [159] = {.lex_state = 0},
  [160] = {.lex_state = 0},
  [161] = {.lex_state = 186},
  [162] = {.lex_state = 186},
  [163] = {.lex_state = 0},
  [164] = {.lex_state = 0},
  [165] = {.lex_state = 0},
  [166] = {.lex_state = 0, .external_lex_state = 1},
  [167] = {.lex_state = 0},
  [168] = {.lex_state = 0},
  [169] = {.lex_state = 0},
  [170] = {.lex_state = 0},
  [171] = {.lex_state = 186},
  [172] = {.lex_state = 0},
  [173] = {.lex_state = 0},
  [174] = {.lex_state = 0},
  [175] = {.lex_state = 0},
  [176] = {.lex_state = 186},
  [177] = {.lex_state = 186},
  [178] = {.lex_state = 0},
  [179] = {.lex_state = 0},
  [180] = {.lex_state = 0},
  [181] = {.lex_state = 9},
  [182] = {.lex_state = 6},
  [183] = {.lex_state = 186},
  [184] = {.lex_state = 0},
  [185] = {.lex_state = 0},
  [186] = {.lex_state = 0},
  [187] = {.lex_state = 0},
  [188] = {.lex_state = 0},
  [189] = {.lex_state = 186},
  [190] = {.lex_state = 186},
  [191] = {.lex_state = 0},
  [192] = {.lex_state = 6},
  [193] = {.lex_state = 0},
  [194] = {.lex_state = 0},
  [195] = {.lex_state = 186},
  [196] = {.lex_state = 13},
  [197] = {.lex_state = 0},
  [198] = {.lex_state = 0},
  [199] = {.lex_state = 0},
  [200] = {.lex_state = 0},
  [201] = {.lex_state = 0},
  [202] = {.lex_state = 0},
  [203] = {.lex_state = 0},
  [204] = {.lex_state = 0},
  [205] = {.lex_state = 186},
  [206] = {.lex_state = 3},
  [207] = {.lex_state = 0},
  [208] = {.lex_state = 0},
  [209] = {.lex_state = 9},
  [210] = {.lex_state = 186},
  [211] = {.lex_state = 0},
  [212] = {.lex_state = 0},
  [213] = {.lex_state = 13},
  [214] = {.lex_state = 3},
  [215] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [sym_comment] = ACTIONS(3),
    [anon_sym_ATmodule] = ACTIONS(1),
    [anon_sym_ATversion] = ACTIONS(1),
    [anon_sym_ATtarget] = ACTIONS(1),
    [anon_sym_ATimports] = ACTIONS(1),
    [anon_sym_python] = ACTIONS(1),
    [anon_sym_typescript] = ACTIONS(1),
    [anon_sym_rust] = ACTIONS(1),
    [anon_sym_COMMA] = ACTIONS(1),
    [anon_sym_LBRACK] = ACTIONS(1),
    [anon_sym_RBRACK] = ACTIONS(1),
    [aux_sym_purpose_section_token1] = ACTIONS(1),
    [aux_sym_inputs_section_token1] = ACTIONS(1),
    [anon_sym_COLON] = ACTIONS(1),
    [anon_sym_required] = ACTIONS(1),
    [anon_sym_optional] = ACTIONS(1),
    [aux_sym_guards_section_token1] = ACTIONS(1),
    [anon_sym_LPAREN] = ACTIONS(1),
    [anon_sym_RPAREN] = ACTIONS(1),
    [aux_sym_logic_section_token1] = ACTIONS(1),
    [anon_sym_DOT] = ACTIONS(1),
    [sym_step_number] = ACTIONS(1),
    [aux_sym_condition_prefix_token1] = ACTIONS(1),
    [aux_sym_condition_prefix_token2] = ACTIONS(1),
    [aux_sym_condition_token_token3] = ACTIONS(1),
    [aux_sym_condition_token_token4] = ACTIONS(1),
    [aux_sym_condition_token_token5] = ACTIONS(1),
    [anon_sym_and] = ACTIONS(1),
    [anon_sym_or] = ACTIONS(1),
    [anon_sym_not] = ACTIONS(1),
    [aux_sym_returns_section_token1] = ACTIONS(1),
    [aux_sym_depends_section_token1] = ACTIONS(1),
    [aux_sym_edge_cases_section_token1] = ACTIONS(1),
    [anon_sym_ATtype] = ACTIONS(1),
    [anon_sym_LBRACE] = ACTIONS(1),
    [anon_sym_extends] = ACTIONS(1),
    [anon_sym_RBRACE] = ACTIONS(1),
    [anon_sym_ATtest] = ACTIONS(1),
    [anon_sym_EQ_EQ] = ACTIONS(1),
    [anon_sym_ATliteral] = ACTIONS(1),
    [anon_sym_QMARK] = ACTIONS(1),
    [anon_sym_number] = ACTIONS(1),
    [anon_sym_string] = ACTIONS(1),
    [anon_sym_boolean] = ACTIONS(1),
    [anon_sym_void] = ACTIONS(1),
    [anon_sym_any] = ACTIONS(1),
    [anon_sym_list] = ACTIONS(1),
    [anon_sym_of] = ACTIONS(1),
    [anon_sym_map] = ACTIONS(1),
    [anon_sym_to] = ACTIONS(1),
    [aux_sym_quoted_string_token1] = ACTIONS(1),
    [aux_sym_quoted_string_token2] = ACTIONS(1),
    [anon_sym_true] = ACTIONS(1),
    [anon_sym_false] = ACTIONS(1),
    [anon_sym_True] = ACTIONS(1),
    [anon_sym_False] = ACTIONS(1),
    [anon_sym_u2022] = ACTIONS(1),
    [anon_sym_DASH] = ACTIONS(1),
    [anon_sym_STAR] = ACTIONS(1),
    [anon_sym_u2192] = ACTIONS(1),
    [sym__newline] = ACTIONS(1),
    [sym_literal_content] = ACTIONS(1),
  },
  [1] = {
    [sym_source_file] = STATE(165),
    [sym_directive] = STATE(6),
    [sym_module_directive] = STATE(37),
    [sym_version_directive] = STATE(37),
    [sym_target_directive] = STATE(37),
    [sym_imports_directive] = STATE(37),
    [sym_anlu_block] = STATE(6),
    [sym_anlu_header] = STATE(2),
    [sym_type_block] = STATE(6),
    [sym_type_header] = STATE(42),
    [sym_test_block] = STATE(6),
    [sym_test_header] = STATE(56),
    [sym_literal_block] = STATE(6),
    [sym_literal_header] = STATE(147),
    [aux_sym_source_file_repeat1] = STATE(6),
    [ts_builtin_sym_end] = ACTIONS(5),
    [sym_comment] = ACTIONS(3),
    [anon_sym_ATmodule] = ACTIONS(7),
    [anon_sym_ATversion] = ACTIONS(9),
    [anon_sym_ATtarget] = ACTIONS(11),
    [anon_sym_ATimports] = ACTIONS(13),
    [anon_sym_LBRACK] = ACTIONS(15),
    [anon_sym_ATtype] = ACTIONS(17),
    [anon_sym_ATtest] = ACTIONS(19),
    [anon_sym_ATliteral] = ACTIONS(21),
    [sym__newline] = ACTIONS(23),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 10,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(27), 1,
      aux_sym_purpose_section_token1,
    ACTIONS(29), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(31), 1,
      aux_sym_guards_section_token1,
    ACTIONS(33), 1,
      aux_sym_logic_section_token1,
    ACTIONS(35), 1,
      aux_sym_returns_section_token1,
    ACTIONS(37), 1,
      aux_sym_depends_section_token1,
    ACTIONS(39), 1,
      aux_sym_edge_cases_section_token1,
    STATE(4), 8,
      sym_purpose_section,
      sym_inputs_section,
      sym_guards_section,
      sym_logic_section,
      sym_returns_section,
      sym_depends_section,
      sym_edge_cases_section,
      aux_sym_anlu_block_repeat1,
    ACTIONS(25), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [47] = 10,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(43), 1,
      aux_sym_purpose_section_token1,
    ACTIONS(46), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(49), 1,
      aux_sym_guards_section_token1,
    ACTIONS(52), 1,
      aux_sym_logic_section_token1,
    ACTIONS(55), 1,
      aux_sym_returns_section_token1,
    ACTIONS(58), 1,
      aux_sym_depends_section_token1,
    ACTIONS(61), 1,
      aux_sym_edge_cases_section_token1,
    STATE(3), 8,
      sym_purpose_section,
      sym_inputs_section,
      sym_guards_section,
      sym_logic_section,
      sym_returns_section,
      sym_depends_section,
      sym_edge_cases_section,
      aux_sym_anlu_block_repeat1,
    ACTIONS(41), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [94] = 10,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(27), 1,
      aux_sym_purpose_section_token1,
    ACTIONS(29), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(31), 1,
      aux_sym_guards_section_token1,
    ACTIONS(33), 1,
      aux_sym_logic_section_token1,
    ACTIONS(35), 1,
      aux_sym_returns_section_token1,
    ACTIONS(37), 1,
      aux_sym_depends_section_token1,
    ACTIONS(39), 1,
      aux_sym_edge_cases_section_token1,
    STATE(3), 8,
      sym_purpose_section,
      sym_inputs_section,
      sym_guards_section,
      sym_logic_section,
      sym_returns_section,
      sym_depends_section,
      sym_edge_cases_section,
      aux_sym_anlu_block_repeat1,
    ACTIONS(64), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [141] = 17,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(66), 1,
      ts_builtin_sym_end,
    ACTIONS(68), 1,
      anon_sym_ATmodule,
    ACTIONS(71), 1,
      anon_sym_ATversion,
    ACTIONS(74), 1,
      anon_sym_ATtarget,
    ACTIONS(77), 1,
      anon_sym_ATimports,
    ACTIONS(80), 1,
      anon_sym_LBRACK,
    ACTIONS(83), 1,
      anon_sym_ATtype,
    ACTIONS(86), 1,
      anon_sym_ATtest,
    ACTIONS(89), 1,
      anon_sym_ATliteral,
    ACTIONS(92), 1,
      sym__newline,
    STATE(2), 1,
      sym_anlu_header,
    STATE(42), 1,
      sym_type_header,
    STATE(56), 1,
      sym_test_header,
    STATE(147), 1,
      sym_literal_header,
    STATE(37), 4,
      sym_module_directive,
      sym_version_directive,
      sym_target_directive,
      sym_imports_directive,
    STATE(5), 6,
      sym_directive,
      sym_anlu_block,
      sym_type_block,
      sym_test_block,
      sym_literal_block,
      aux_sym_source_file_repeat1,
  [201] = 17,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(7), 1,
      anon_sym_ATmodule,
    ACTIONS(9), 1,
      anon_sym_ATversion,
    ACTIONS(11), 1,
      anon_sym_ATtarget,
    ACTIONS(13), 1,
      anon_sym_ATimports,
    ACTIONS(15), 1,
      anon_sym_LBRACK,
    ACTIONS(17), 1,
      anon_sym_ATtype,
    ACTIONS(19), 1,
      anon_sym_ATtest,
    ACTIONS(21), 1,
      anon_sym_ATliteral,
    ACTIONS(95), 1,
      ts_builtin_sym_end,
    ACTIONS(97), 1,
      sym__newline,
    STATE(2), 1,
      sym_anlu_header,
    STATE(42), 1,
      sym_type_header,
    STATE(56), 1,
      sym_test_header,
    STATE(147), 1,
      sym_literal_header,
    STATE(37), 4,
      sym_module_directive,
      sym_version_directive,
      sym_target_directive,
      sym_imports_directive,
    STATE(5), 6,
      sym_directive,
      sym_anlu_block,
      sym_type_block,
      sym_test_block,
      sym_literal_block,
      aux_sym_source_file_repeat1,
  [261] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(126), 1,
      sym_bullet,
    STATE(11), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(101), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(99), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [296] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(115), 1,
      sym_bullet,
    STATE(10), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
    ACTIONS(105), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(103), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [331] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(123), 1,
      sym_bullet,
    STATE(12), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(105), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(107), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [366] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(115), 1,
      sym_bullet,
    STATE(10), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(109), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [401] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(126), 1,
      sym_bullet,
    STATE(11), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(116), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(114), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [436] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(123), 1,
      sym_bullet,
    STATE(12), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(121), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(119), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [471] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(126), 1,
      sym_step_number,
    STATE(15), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
    ACTIONS(124), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [501] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(128), 20,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [527] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(132), 1,
      sym_step_number,
    STATE(15), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
    ACTIONS(130), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [557] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(135), 20,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [583] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(137), 20,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [609] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(139), 20,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [635] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(141), 20,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [661] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(143), 18,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      sym_step_number,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [685] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(145), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [708] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(147), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [731] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(149), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [754] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(151), 17,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      aux_sym_purpose_section_token1,
      aux_sym_inputs_section_token1,
      aux_sym_guards_section_token1,
      aux_sym_logic_section_token1,
      aux_sym_returns_section_token1,
      aux_sym_depends_section_token1,
      aux_sym_edge_cases_section_token1,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [777] = 9,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(153), 1,
      anon_sym_RPAREN,
    ACTIONS(155), 1,
      aux_sym_condition_token_token1,
    ACTIONS(157), 1,
      sym_number,
    STATE(90), 1,
      sym_test_value,
    STATE(162), 1,
      sym_test_args,
    ACTIONS(159), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(87), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(161), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [811] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(163), 1,
      sym_type_name,
    ACTIONS(167), 1,
      anon_sym_list,
    ACTIONS(169), 1,
      anon_sym_map,
    STATE(79), 1,
      sym_type_spec,
    ACTIONS(165), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(108), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [841] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(163), 1,
      sym_type_name,
    ACTIONS(167), 1,
      anon_sym_list,
    ACTIONS(169), 1,
      anon_sym_map,
    STATE(83), 1,
      sym_type_spec,
    ACTIONS(165), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(108), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [871] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(163), 1,
      sym_type_name,
    ACTIONS(167), 1,
      anon_sym_list,
    ACTIONS(169), 1,
      anon_sym_map,
    STATE(82), 1,
      sym_type_spec,
    ACTIONS(165), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(108), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [901] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(163), 1,
      sym_type_name,
    ACTIONS(167), 1,
      anon_sym_list,
    ACTIONS(169), 1,
      anon_sym_map,
    ACTIONS(165), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(85), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [928] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(163), 1,
      sym_type_name,
    ACTIONS(167), 1,
      anon_sym_list,
    ACTIONS(169), 1,
      anon_sym_map,
    ACTIONS(165), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(163), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [955] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(163), 1,
      sym_type_name,
    ACTIONS(167), 1,
      anon_sym_list,
    ACTIONS(169), 1,
      anon_sym_map,
    ACTIONS(165), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(75), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [982] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(155), 1,
      aux_sym_condition_token_token1,
    ACTIONS(157), 1,
      sym_number,
    STATE(124), 1,
      sym_test_value,
    ACTIONS(159), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(87), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(161), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [1010] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(155), 1,
      aux_sym_condition_token_token1,
    ACTIONS(157), 1,
      sym_number,
    STATE(160), 1,
      sym_test_value,
    ACTIONS(159), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(87), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(161), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [1038] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(215), 1,
      sym_condition_text,
    STATE(35), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(171), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(173), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1061] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(175), 1,
      aux_sym_condition_prefix_token2,
    STATE(36), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(171), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(173), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1084] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(177), 1,
      aux_sym_condition_prefix_token2,
    STATE(36), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(179), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(182), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1107] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(185), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1123] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(187), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1139] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(189), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1155] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(191), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1171] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(193), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1187] = 8,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    ACTIONS(197), 1,
      anon_sym_RBRACE,
    STATE(48), 1,
      sym_type_close,
    STATE(134), 1,
      sym_bullet,
    STATE(143), 1,
      sym_identifier,
    STATE(49), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(101), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1215] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(199), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1231] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(201), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1247] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(203), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1263] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(205), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1279] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(207), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1295] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(209), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1311] = 8,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    ACTIONS(197), 1,
      anon_sym_RBRACE,
    STATE(43), 1,
      sym_type_close,
    STATE(134), 1,
      sym_bullet,
    STATE(143), 1,
      sym_identifier,
    STATE(53), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(101), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1339] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(211), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1355] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(213), 10,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATliteral,
      sym__newline,
  [1371] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(217), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
    ACTIONS(215), 5,
      aux_sym_condition_prefix_token2,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
  [1388] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(219), 1,
      aux_sym_condition_token_token1,
    ACTIONS(222), 1,
      anon_sym_RBRACE,
    STATE(134), 1,
      sym_bullet,
    STATE(143), 1,
      sym_identifier,
    STATE(53), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(224), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1413] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(155), 1,
      aux_sym_condition_token_token1,
    ACTIONS(159), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    ACTIONS(227), 2,
      anon_sym_required,
      anon_sym_optional,
    STATE(120), 2,
      sym_quoted_string,
      sym_identifier,
  [1432] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    ACTIONS(229), 1,
      anon_sym_RBRACE,
    STATE(47), 1,
      sym_test_close,
    STATE(183), 1,
      sym_test_call,
    STATE(189), 1,
      sym_identifier,
    STATE(59), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1455] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    ACTIONS(229), 1,
      anon_sym_RBRACE,
    STATE(38), 1,
      sym_test_close,
    STATE(183), 1,
      sym_test_call,
    STATE(189), 1,
      sym_identifier,
    STATE(55), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1478] = 8,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(233), 1,
      anon_sym_LBRACK,
    ACTIONS(235), 1,
      aux_sym_guard_text_token1,
    ACTIONS(237), 1,
      aux_sym_condition_prefix_token1,
    STATE(69), 1,
      sym_step_text,
    STATE(84), 1,
      sym_state_prefix,
    STATE(116), 1,
      sym_condition_prefix,
    STATE(157), 1,
      sym_logic_step,
  [1503] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    ACTIONS(239), 1,
      anon_sym_RPAREN,
    STATE(205), 1,
      sym_error_args,
    ACTIONS(159), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(109), 2,
      sym_quoted_string,
      sym_identifier,
  [1524] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(241), 1,
      aux_sym_condition_token_token1,
    ACTIONS(244), 1,
      anon_sym_RBRACE,
    STATE(183), 1,
      sym_test_call,
    STATE(189), 1,
      sym_identifier,
    STATE(59), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1544] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(115), 1,
      sym_bullet,
    STATE(8), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
    ACTIONS(105), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1560] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(126), 1,
      sym_bullet,
    STATE(7), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(101), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1576] = 7,
    ACTIONS(155), 1,
      aux_sym_condition_token_token1,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(246), 1,
      aux_sym_description_text_token1,
    STATE(173), 1,
      sym_error_spec,
    STATE(174), 1,
      sym_error_call,
    STATE(175), 1,
      sym_error_text,
    STATE(176), 1,
      sym_identifier,
  [1598] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(123), 1,
      sym_bullet,
    STATE(9), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(105), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1614] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(248), 6,
      anon_sym_COMMA,
      anon_sym_COLON,
      anon_sym_LPAREN,
      anon_sym_RPAREN,
      anon_sym_LBRACE,
      sym__newline,
  [1626] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    ACTIONS(159), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(138), 2,
      sym_quoted_string,
      sym_identifier,
  [1641] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(250), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1652] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(252), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1663] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(254), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1674] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(258), 1,
      sym__newline,
    STATE(129), 1,
      sym_arrow,
    STATE(184), 1,
      sym_output_binding,
    ACTIONS(256), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1691] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(260), 1,
      sym__newline,
    STATE(129), 1,
      sym_arrow,
    STATE(139), 1,
      sym_output_binding,
    ACTIONS(256), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1708] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(262), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1719] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(264), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1730] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(266), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1741] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(268), 1,
      sym__newline,
    STATE(129), 1,
      sym_arrow,
    STATE(207), 1,
      sym_output_binding,
    ACTIONS(256), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1758] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(270), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [1768] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(272), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [1778] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(274), 1,
      anon_sym_LBRACK,
    ACTIONS(276), 1,
      sym_anlu_identifier,
    STATE(95), 1,
      sym_anlu_reference,
    STATE(155), 1,
      sym_depends_list,
  [1794] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(278), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [1804] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(280), 1,
      anon_sym_COMMA,
    ACTIONS(282), 1,
      sym__newline,
    STATE(98), 1,
      aux_sym_input_constraints_repeat1,
    STATE(141), 1,
      sym_field_constraints,
  [1820] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(286), 1,
      sym__newline,
    STATE(62), 1,
      sym_arrow,
    ACTIONS(284), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1834] = 3,
    ACTIONS(3), 1,
      sym_comment,
    STATE(151), 1,
      sym_target_name,
    ACTIONS(288), 3,
      anon_sym_python,
      anon_sym_typescript,
      anon_sym_rust,
  [1846] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(280), 1,
      anon_sym_COMMA,
    ACTIONS(290), 1,
      sym__newline,
    STATE(98), 1,
      aux_sym_input_constraints_repeat1,
    STATE(168), 1,
      sym_field_constraints,
  [1862] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(280), 1,
      anon_sym_COMMA,
    ACTIONS(292), 1,
      sym__newline,
    STATE(107), 1,
      aux_sym_input_constraints_repeat1,
    STATE(191), 1,
      sym_input_constraints,
  [1878] = 5,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_guard_text_token1,
    ACTIONS(237), 1,
      aux_sym_condition_prefix_token1,
    STATE(70), 1,
      sym_step_text,
    STATE(127), 1,
      sym_condition_prefix,
  [1894] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(294), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [1904] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(296), 1,
      anon_sym_COMMA,
    ACTIONS(298), 1,
      anon_sym_RPAREN,
    STATE(105), 1,
      aux_sym_test_args_repeat1,
  [1917] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(300), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [1926] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(302), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [1935] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(304), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [1944] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(296), 1,
      anon_sym_COMMA,
    ACTIONS(306), 1,
      anon_sym_RPAREN,
    STATE(86), 1,
      aux_sym_test_args_repeat1,
  [1957] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(308), 1,
      anon_sym_COMMA,
    ACTIONS(311), 1,
      sym__newline,
    STATE(91), 1,
      aux_sym_import_list_repeat1,
  [1970] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(313), 3,
      anon_sym_u2192,
      anon_sym_DASH_GT,
      sym__newline,
  [1979] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(315), 1,
      anon_sym_COMMA,
    ACTIONS(318), 1,
      sym__newline,
    STATE(93), 1,
      aux_sym_depends_list_repeat1,
  [1992] = 3,
    ACTIONS(3), 1,
      sym_comment,
    STATE(118), 1,
      sym_arrow,
    ACTIONS(284), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2003] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(320), 1,
      anon_sym_COMMA,
    ACTIONS(322), 1,
      sym__newline,
    STATE(103), 1,
      aux_sym_depends_list_repeat1,
  [2016] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    STATE(97), 1,
      sym_identifier,
    STATE(153), 1,
      sym_import_list,
  [2029] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(324), 1,
      anon_sym_COMMA,
    ACTIONS(326), 1,
      sym__newline,
    STATE(101), 1,
      aux_sym_import_list_repeat1,
  [2042] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(280), 1,
      anon_sym_COMMA,
    ACTIONS(328), 1,
      sym__newline,
    STATE(104), 1,
      aux_sym_input_constraints_repeat1,
  [2055] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(330), 1,
      anon_sym_COMMA,
    ACTIONS(333), 1,
      anon_sym_RPAREN,
    STATE(99), 1,
      aux_sym_error_args_repeat1,
  [2068] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(335), 3,
      anon_sym_u2192,
      anon_sym_DASH_GT,
      sym__newline,
  [2077] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(324), 1,
      anon_sym_COMMA,
    ACTIONS(337), 1,
      sym__newline,
    STATE(91), 1,
      aux_sym_import_list_repeat1,
  [2090] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(274), 1,
      anon_sym_LBRACK,
    ACTIONS(276), 1,
      sym_anlu_identifier,
    STATE(119), 1,
      sym_anlu_reference,
  [2103] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(320), 1,
      anon_sym_COMMA,
    ACTIONS(339), 1,
      sym__newline,
    STATE(93), 1,
      aux_sym_depends_list_repeat1,
  [2116] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(341), 1,
      anon_sym_COMMA,
    ACTIONS(344), 1,
      sym__newline,
    STATE(104), 1,
      aux_sym_input_constraints_repeat1,
  [2129] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(346), 1,
      anon_sym_COMMA,
    ACTIONS(349), 1,
      anon_sym_RPAREN,
    STATE(105), 1,
      aux_sym_test_args_repeat1,
  [2142] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(351), 1,
      anon_sym_LBRACE,
    ACTIONS(353), 1,
      anon_sym_extends,
    STATE(188), 1,
      sym_extends_clause,
  [2155] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(280), 1,
      anon_sym_COMMA,
    ACTIONS(355), 1,
      sym__newline,
    STATE(104), 1,
      aux_sym_input_constraints_repeat1,
  [2168] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(359), 1,
      anon_sym_QMARK,
    ACTIONS(357), 2,
      anon_sym_COMMA,
      sym__newline,
  [2179] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(361), 1,
      anon_sym_COMMA,
    ACTIONS(363), 1,
      anon_sym_RPAREN,
    STATE(111), 1,
      aux_sym_error_args_repeat1,
  [2192] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(126), 1,
      sym_step_number,
    STATE(13), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
  [2203] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(361), 1,
      anon_sym_COMMA,
    ACTIONS(365), 1,
      anon_sym_RPAREN,
    STATE(99), 1,
      aux_sym_error_args_repeat1,
  [2216] = 2,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(367), 2,
      aux_sym_description_text_token1,
      aux_sym_condition_token_token1,
  [2224] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(369), 1,
      anon_sym_RBRACE,
    STATE(44), 1,
      sym_literal_close,
  [2234] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(371), 2,
      anon_sym_COMMA,
      sym__newline,
  [2242] = 3,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(373), 1,
      aux_sym_guard_text_token1,
    STATE(80), 1,
      sym_guard_text,
  [2252] = 3,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_guard_text_token1,
    STATE(70), 1,
      sym_step_text,
  [2262] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    STATE(211), 1,
      sym_identifier,
  [2272] = 3,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(375), 1,
      aux_sym_description_text_token1,
    STATE(187), 1,
      sym_edge_behavior_text,
  [2282] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(318), 2,
      anon_sym_COMMA,
      sym__newline,
  [2290] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(344), 2,
      anon_sym_COMMA,
      sym__newline,
  [2298] = 3,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(377), 1,
      aux_sym_description_text_token1,
    STATE(179), 1,
      sym_returns_text,
  [2308] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(379), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2316] = 3,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(381), 1,
      aux_sym_guard_text_token1,
    STATE(94), 1,
      sym_edge_condition_text,
  [2326] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(349), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [2334] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(383), 2,
      anon_sym_COMMA,
      sym__newline,
  [2342] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    STATE(169), 1,
      sym_identifier,
  [2352] = 3,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_guard_text_token1,
    STATE(74), 1,
      sym_step_text,
  [2362] = 3,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(385), 1,
      aux_sym_description_text_token1,
    STATE(197), 1,
      sym_description_text,
  [2372] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    STATE(200), 1,
      sym_identifier,
  [2382] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(311), 2,
      anon_sym_COMMA,
      sym__newline,
  [2390] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(387), 2,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
  [2398] = 2,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(389), 2,
      aux_sym_guard_text_token1,
      aux_sym_condition_prefix_token1,
  [2406] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    STATE(201), 1,
      sym_identifier,
  [2416] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    STATE(156), 1,
      sym_identifier,
  [2426] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(391), 2,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
  [2434] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(393), 2,
      anon_sym_COMMA,
      sym__newline,
  [2442] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 1,
      aux_sym_condition_token_token1,
    STATE(130), 1,
      sym_identifier,
  [2452] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(333), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [2460] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(395), 1,
      sym__newline,
  [2467] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(397), 1,
      sym__newline,
  [2474] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(399), 1,
      sym__newline,
  [2481] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(401), 1,
      sym__newline,
  [2488] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(403), 1,
      anon_sym_COLON,
  [2495] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(405), 1,
      sym__newline,
  [2502] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(407), 1,
      sym__newline,
  [2509] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(409), 1,
      anon_sym_EQ_EQ,
  [2516] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(411), 1,
      sym_literal_content,
  [2523] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(413), 1,
      anon_sym_of,
  [2530] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(415), 1,
      anon_sym_of,
  [2537] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(417), 1,
      sym_anlu_identifier,
  [2544] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(419), 1,
      sym__newline,
  [2551] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(421), 1,
      sym_type_name,
  [2558] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(423), 1,
      sym__newline,
  [2565] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(425), 1,
      sym_state_name,
  [2572] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(427), 1,
      sym__newline,
  [2579] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(429), 1,
      anon_sym_COLON,
  [2586] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(431), 1,
      sym__newline,
  [2593] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(433), 1,
      anon_sym_LBRACE,
  [2600] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(435), 1,
      sym__newline,
  [2607] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(437), 1,
      sym__newline,
  [2614] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(439), 1,
      anon_sym_EQ_EQ,
  [2621] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(441), 1,
      anon_sym_RPAREN,
  [2628] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(443), 1,
      anon_sym_to,
  [2635] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(445), 1,
      anon_sym_LBRACE,
  [2642] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(447), 1,
      ts_builtin_sym_end,
  [2649] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(449), 1,
      sym_literal_content,
  [2656] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(451), 1,
      sym__newline,
  [2663] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(453), 1,
      sym__newline,
  [2670] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(455), 1,
      anon_sym_COLON,
  [2677] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(457), 1,
      sym__newline,
  [2684] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(459), 1,
      anon_sym_RBRACK,
  [2691] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(461), 1,
      sym__newline,
  [2698] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(463), 1,
      sym__newline,
  [2705] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(465), 1,
      sym__newline,
  [2712] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(467), 1,
      sym__newline,
  [2719] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(469), 1,
      anon_sym_LPAREN,
  [2726] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(471), 1,
      anon_sym_RBRACK,
  [2733] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(473), 1,
      sym__newline,
  [2740] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(475), 1,
      sym__newline,
  [2747] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(477), 1,
      sym__newline,
  [2754] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(479), 1,
      sym_type_name,
  [2761] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(481), 1,
      sym_anlu_identifier,
  [2768] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(483), 1,
      anon_sym_EQ_EQ,
  [2775] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(485), 1,
      sym__newline,
  [2782] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(487), 1,
      sym__newline,
  [2789] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(489), 1,
      sym__newline,
  [2796] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(491), 1,
      sym__newline,
  [2803] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(493), 1,
      anon_sym_LBRACE,
  [2810] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(495), 1,
      anon_sym_LPAREN,
  [2817] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(497), 1,
      anon_sym_RBRACK,
  [2824] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(499), 1,
      sym__newline,
  [2831] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(501), 1,
      sym_anlu_identifier,
  [2838] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(503), 1,
      sym__newline,
  [2845] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(505), 1,
      sym__newline,
  [2852] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(507), 1,
      anon_sym_LBRACK,
  [2859] = 2,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(509), 1,
      aux_sym_guard_text_token1,
  [2866] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(511), 1,
      sym__newline,
  [2873] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(513), 1,
      anon_sym_DOT,
  [2880] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(515), 1,
      sym__newline,
  [2887] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(517), 1,
      sym__newline,
  [2894] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(519), 1,
      sym__newline,
  [2901] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(521), 1,
      sym__newline,
  [2908] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(523), 1,
      sym__newline,
  [2915] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(525), 1,
      sym__newline,
  [2922] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(527), 1,
      anon_sym_RPAREN,
  [2929] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(529), 1,
      aux_sym_condition_token_token1,
  [2936] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(531), 1,
      sym__newline,
  [2943] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(533), 1,
      sym__newline,
  [2950] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(535), 1,
      sym_version_string,
  [2957] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(537), 1,
      anon_sym_RBRACK,
  [2964] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(539), 1,
      anon_sym_LBRACE,
  [2971] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(541), 1,
      sym__newline,
  [2978] = 2,
    ACTIONS(231), 1,
      sym_comment,
    ACTIONS(543), 1,
      aux_sym_guard_text_token1,
  [2985] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(545), 1,
      aux_sym_condition_token_token1,
  [2992] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(547), 1,
      aux_sym_condition_prefix_token2,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 47,
  [SMALL_STATE(4)] = 94,
  [SMALL_STATE(5)] = 141,
  [SMALL_STATE(6)] = 201,
  [SMALL_STATE(7)] = 261,
  [SMALL_STATE(8)] = 296,
  [SMALL_STATE(9)] = 331,
  [SMALL_STATE(10)] = 366,
  [SMALL_STATE(11)] = 401,
  [SMALL_STATE(12)] = 436,
  [SMALL_STATE(13)] = 471,
  [SMALL_STATE(14)] = 501,
  [SMALL_STATE(15)] = 527,
  [SMALL_STATE(16)] = 557,
  [SMALL_STATE(17)] = 583,
  [SMALL_STATE(18)] = 609,
  [SMALL_STATE(19)] = 635,
  [SMALL_STATE(20)] = 661,
  [SMALL_STATE(21)] = 685,
  [SMALL_STATE(22)] = 708,
  [SMALL_STATE(23)] = 731,
  [SMALL_STATE(24)] = 754,
  [SMALL_STATE(25)] = 777,
  [SMALL_STATE(26)] = 811,
  [SMALL_STATE(27)] = 841,
  [SMALL_STATE(28)] = 871,
  [SMALL_STATE(29)] = 901,
  [SMALL_STATE(30)] = 928,
  [SMALL_STATE(31)] = 955,
  [SMALL_STATE(32)] = 982,
  [SMALL_STATE(33)] = 1010,
  [SMALL_STATE(34)] = 1038,
  [SMALL_STATE(35)] = 1061,
  [SMALL_STATE(36)] = 1084,
  [SMALL_STATE(37)] = 1107,
  [SMALL_STATE(38)] = 1123,
  [SMALL_STATE(39)] = 1139,
  [SMALL_STATE(40)] = 1155,
  [SMALL_STATE(41)] = 1171,
  [SMALL_STATE(42)] = 1187,
  [SMALL_STATE(43)] = 1215,
  [SMALL_STATE(44)] = 1231,
  [SMALL_STATE(45)] = 1247,
  [SMALL_STATE(46)] = 1263,
  [SMALL_STATE(47)] = 1279,
  [SMALL_STATE(48)] = 1295,
  [SMALL_STATE(49)] = 1311,
  [SMALL_STATE(50)] = 1339,
  [SMALL_STATE(51)] = 1355,
  [SMALL_STATE(52)] = 1371,
  [SMALL_STATE(53)] = 1388,
  [SMALL_STATE(54)] = 1413,
  [SMALL_STATE(55)] = 1432,
  [SMALL_STATE(56)] = 1455,
  [SMALL_STATE(57)] = 1478,
  [SMALL_STATE(58)] = 1503,
  [SMALL_STATE(59)] = 1524,
  [SMALL_STATE(60)] = 1544,
  [SMALL_STATE(61)] = 1560,
  [SMALL_STATE(62)] = 1576,
  [SMALL_STATE(63)] = 1598,
  [SMALL_STATE(64)] = 1614,
  [SMALL_STATE(65)] = 1626,
  [SMALL_STATE(66)] = 1641,
  [SMALL_STATE(67)] = 1652,
  [SMALL_STATE(68)] = 1663,
  [SMALL_STATE(69)] = 1674,
  [SMALL_STATE(70)] = 1691,
  [SMALL_STATE(71)] = 1708,
  [SMALL_STATE(72)] = 1719,
  [SMALL_STATE(73)] = 1730,
  [SMALL_STATE(74)] = 1741,
  [SMALL_STATE(75)] = 1758,
  [SMALL_STATE(76)] = 1768,
  [SMALL_STATE(77)] = 1778,
  [SMALL_STATE(78)] = 1794,
  [SMALL_STATE(79)] = 1804,
  [SMALL_STATE(80)] = 1820,
  [SMALL_STATE(81)] = 1834,
  [SMALL_STATE(82)] = 1846,
  [SMALL_STATE(83)] = 1862,
  [SMALL_STATE(84)] = 1878,
  [SMALL_STATE(85)] = 1894,
  [SMALL_STATE(86)] = 1904,
  [SMALL_STATE(87)] = 1917,
  [SMALL_STATE(88)] = 1926,
  [SMALL_STATE(89)] = 1935,
  [SMALL_STATE(90)] = 1944,
  [SMALL_STATE(91)] = 1957,
  [SMALL_STATE(92)] = 1970,
  [SMALL_STATE(93)] = 1979,
  [SMALL_STATE(94)] = 1992,
  [SMALL_STATE(95)] = 2003,
  [SMALL_STATE(96)] = 2016,
  [SMALL_STATE(97)] = 2029,
  [SMALL_STATE(98)] = 2042,
  [SMALL_STATE(99)] = 2055,
  [SMALL_STATE(100)] = 2068,
  [SMALL_STATE(101)] = 2077,
  [SMALL_STATE(102)] = 2090,
  [SMALL_STATE(103)] = 2103,
  [SMALL_STATE(104)] = 2116,
  [SMALL_STATE(105)] = 2129,
  [SMALL_STATE(106)] = 2142,
  [SMALL_STATE(107)] = 2155,
  [SMALL_STATE(108)] = 2168,
  [SMALL_STATE(109)] = 2179,
  [SMALL_STATE(110)] = 2192,
  [SMALL_STATE(111)] = 2203,
  [SMALL_STATE(112)] = 2216,
  [SMALL_STATE(113)] = 2224,
  [SMALL_STATE(114)] = 2234,
  [SMALL_STATE(115)] = 2242,
  [SMALL_STATE(116)] = 2252,
  [SMALL_STATE(117)] = 2262,
  [SMALL_STATE(118)] = 2272,
  [SMALL_STATE(119)] = 2282,
  [SMALL_STATE(120)] = 2290,
  [SMALL_STATE(121)] = 2298,
  [SMALL_STATE(122)] = 2308,
  [SMALL_STATE(123)] = 2316,
  [SMALL_STATE(124)] = 2326,
  [SMALL_STATE(125)] = 2334,
  [SMALL_STATE(126)] = 2342,
  [SMALL_STATE(127)] = 2352,
  [SMALL_STATE(128)] = 2362,
  [SMALL_STATE(129)] = 2372,
  [SMALL_STATE(130)] = 2382,
  [SMALL_STATE(131)] = 2390,
  [SMALL_STATE(132)] = 2398,
  [SMALL_STATE(133)] = 2406,
  [SMALL_STATE(134)] = 2416,
  [SMALL_STATE(135)] = 2426,
  [SMALL_STATE(136)] = 2434,
  [SMALL_STATE(137)] = 2442,
  [SMALL_STATE(138)] = 2452,
  [SMALL_STATE(139)] = 2460,
  [SMALL_STATE(140)] = 2467,
  [SMALL_STATE(141)] = 2474,
  [SMALL_STATE(142)] = 2481,
  [SMALL_STATE(143)] = 2488,
  [SMALL_STATE(144)] = 2495,
  [SMALL_STATE(145)] = 2502,
  [SMALL_STATE(146)] = 2509,
  [SMALL_STATE(147)] = 2516,
  [SMALL_STATE(148)] = 2523,
  [SMALL_STATE(149)] = 2530,
  [SMALL_STATE(150)] = 2537,
  [SMALL_STATE(151)] = 2544,
  [SMALL_STATE(152)] = 2551,
  [SMALL_STATE(153)] = 2558,
  [SMALL_STATE(154)] = 2565,
  [SMALL_STATE(155)] = 2572,
  [SMALL_STATE(156)] = 2579,
  [SMALL_STATE(157)] = 2586,
  [SMALL_STATE(158)] = 2593,
  [SMALL_STATE(159)] = 2600,
  [SMALL_STATE(160)] = 2607,
  [SMALL_STATE(161)] = 2614,
  [SMALL_STATE(162)] = 2621,
  [SMALL_STATE(163)] = 2628,
  [SMALL_STATE(164)] = 2635,
  [SMALL_STATE(165)] = 2642,
  [SMALL_STATE(166)] = 2649,
  [SMALL_STATE(167)] = 2656,
  [SMALL_STATE(168)] = 2663,
  [SMALL_STATE(169)] = 2670,
  [SMALL_STATE(170)] = 2677,
  [SMALL_STATE(171)] = 2684,
  [SMALL_STATE(172)] = 2691,
  [SMALL_STATE(173)] = 2698,
  [SMALL_STATE(174)] = 2705,
  [SMALL_STATE(175)] = 2712,
  [SMALL_STATE(176)] = 2719,
  [SMALL_STATE(177)] = 2726,
  [SMALL_STATE(178)] = 2733,
  [SMALL_STATE(179)] = 2740,
  [SMALL_STATE(180)] = 2747,
  [SMALL_STATE(181)] = 2754,
  [SMALL_STATE(182)] = 2761,
  [SMALL_STATE(183)] = 2768,
  [SMALL_STATE(184)] = 2775,
  [SMALL_STATE(185)] = 2782,
  [SMALL_STATE(186)] = 2789,
  [SMALL_STATE(187)] = 2796,
  [SMALL_STATE(188)] = 2803,
  [SMALL_STATE(189)] = 2810,
  [SMALL_STATE(190)] = 2817,
  [SMALL_STATE(191)] = 2824,
  [SMALL_STATE(192)] = 2831,
  [SMALL_STATE(193)] = 2838,
  [SMALL_STATE(194)] = 2845,
  [SMALL_STATE(195)] = 2852,
  [SMALL_STATE(196)] = 2859,
  [SMALL_STATE(197)] = 2866,
  [SMALL_STATE(198)] = 2873,
  [SMALL_STATE(199)] = 2880,
  [SMALL_STATE(200)] = 2887,
  [SMALL_STATE(201)] = 2894,
  [SMALL_STATE(202)] = 2901,
  [SMALL_STATE(203)] = 2908,
  [SMALL_STATE(204)] = 2915,
  [SMALL_STATE(205)] = 2922,
  [SMALL_STATE(206)] = 2929,
  [SMALL_STATE(207)] = 2936,
  [SMALL_STATE(208)] = 2943,
  [SMALL_STATE(209)] = 2950,
  [SMALL_STATE(210)] = 2957,
  [SMALL_STATE(211)] = 2964,
  [SMALL_STATE(212)] = 2971,
  [SMALL_STATE(213)] = 2978,
  [SMALL_STATE(214)] = 2985,
  [SMALL_STATE(215)] = 2992,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT_EXTRA(),
  [5] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0, 0, 0),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(133),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(209),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(81),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(96),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(150),
  [17] = {.entry = {.count = 1, .reusable = true}}, SHIFT(152),
  [19] = {.entry = {.count = 1, .reusable = true}}, SHIFT(195),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(117),
  [23] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [25] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_block, 1, 0, 0),
  [27] = {.entry = {.count = 1, .reusable = true}}, SHIFT(128),
  [29] = {.entry = {.count = 1, .reusable = true}}, SHIFT(140),
  [31] = {.entry = {.count = 1, .reusable = true}}, SHIFT(142),
  [33] = {.entry = {.count = 1, .reusable = true}}, SHIFT(145),
  [35] = {.entry = {.count = 1, .reusable = true}}, SHIFT(121),
  [37] = {.entry = {.count = 1, .reusable = true}}, SHIFT(77),
  [39] = {.entry = {.count = 1, .reusable = true}}, SHIFT(185),
  [41] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0),
  [43] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(128),
  [46] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(140),
  [49] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(142),
  [52] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(145),
  [55] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(121),
  [58] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(77),
  [61] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(185),
  [64] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_block, 2, 0, 0),
  [66] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0),
  [68] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(133),
  [71] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(209),
  [74] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(81),
  [77] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(96),
  [80] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(150),
  [83] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(152),
  [86] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(195),
  [89] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(117),
  [92] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(5),
  [95] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1, 0, 0),
  [97] = {.entry = {.count = 1, .reusable = true}}, SHIFT(5),
  [99] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_inputs_section, 3, 0, 9),
  [101] = {.entry = {.count = 1, .reusable = true}}, SHIFT(206),
  [103] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guards_section, 3, 0, 9),
  [105] = {.entry = {.count = 1, .reusable = true}}, SHIFT(213),
  [107] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_cases_section, 3, 0, 9),
  [109] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_guards_section_repeat1, 2, 0, 0),
  [111] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_guards_section_repeat1, 2, 0, 0), SHIFT_REPEAT(213),
  [114] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_inputs_section_repeat1, 2, 0, 0),
  [116] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_inputs_section_repeat1, 2, 0, 0), SHIFT_REPEAT(206),
  [119] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_edge_cases_section_repeat1, 2, 0, 0),
  [121] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_edge_cases_section_repeat1, 2, 0, 0), SHIFT_REPEAT(213),
  [124] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_section, 3, 0, 9),
  [126] = {.entry = {.count = 1, .reusable = true}}, SHIFT(198),
  [128] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_item, 3, 0, 16),
  [130] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_logic_section_repeat1, 2, 0, 0),
  [132] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_logic_section_repeat1, 2, 0, 0), SHIFT_REPEAT(198),
  [135] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_item, 5, 0, 19),
  [137] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_item, 5, 0, 22),
  [139] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_case_item, 5, 0, 26),
  [141] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_item, 6, 0, 19),
  [143] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_item, 4, 0, 20),
  [145] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_purpose_section, 3, 0, 8),
  [147] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_section, 3, 0, 11),
  [149] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_header, 4, 0, 1),
  [151] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_returns_section, 3, 0, 10),
  [153] = {.entry = {.count = 1, .reusable = true}}, SHIFT(161),
  [155] = {.entry = {.count = 1, .reusable = false}}, SHIFT(64),
  [157] = {.entry = {.count = 1, .reusable = true}}, SHIFT(87),
  [159] = {.entry = {.count = 1, .reusable = true}}, SHIFT(88),
  [161] = {.entry = {.count = 1, .reusable = false}}, SHIFT(89),
  [163] = {.entry = {.count = 1, .reusable = true}}, SHIFT(76),
  [165] = {.entry = {.count = 1, .reusable = true}}, SHIFT(78),
  [167] = {.entry = {.count = 1, .reusable = true}}, SHIFT(148),
  [169] = {.entry = {.count = 1, .reusable = true}}, SHIFT(149),
  [171] = {.entry = {.count = 1, .reusable = false}}, SHIFT(52),
  [173] = {.entry = {.count = 1, .reusable = true}}, SHIFT(52),
  [175] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_text, 1, 0, 0),
  [177] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0),
  [179] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0), SHIFT_REPEAT(52),
  [182] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0), SHIFT_REPEAT(52),
  [185] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_directive, 1, 0, 0),
  [187] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_block, 2, 0, 0),
  [189] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_module_directive, 3, 0, 1),
  [191] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_close, 2, 0, 0),
  [193] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_version_directive, 3, 0, 2),
  [195] = {.entry = {.count = 1, .reusable = true}}, SHIFT(64),
  [197] = {.entry = {.count = 1, .reusable = true}}, SHIFT(202),
  [199] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_block, 3, 0, 0),
  [201] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_block, 3, 0, 5),
  [203] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_close, 2, 0, 0),
  [205] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_target_directive, 3, 0, 3),
  [207] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_block, 3, 0, 0),
  [209] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_block, 2, 0, 0),
  [211] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_imports_directive, 3, 0, 4),
  [213] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_close, 2, 0, 0),
  [215] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_token, 1, 0, 0),
  [217] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition_token, 1, 0, 0),
  [219] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0), SHIFT_REPEAT(64),
  [222] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0),
  [224] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0), SHIFT_REPEAT(206),
  [227] = {.entry = {.count = 1, .reusable = false}}, SHIFT(120),
  [229] = {.entry = {.count = 1, .reusable = true}}, SHIFT(170),
  [231] = {.entry = {.count = 1, .reusable = false}}, SHIFT_EXTRA(),
  [233] = {.entry = {.count = 1, .reusable = false}}, SHIFT(154),
  [235] = {.entry = {.count = 1, .reusable = false}}, SHIFT(100),
  [237] = {.entry = {.count = 1, .reusable = false}}, SHIFT(34),
  [239] = {.entry = {.count = 1, .reusable = true}}, SHIFT(204),
  [241] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_test_block_repeat1, 2, 0, 0), SHIFT_REPEAT(64),
  [244] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_test_block_repeat1, 2, 0, 0),
  [246] = {.entry = {.count = 1, .reusable = false}}, SHIFT(172),
  [248] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 1, 0, 0),
  [250] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_header, 4, 0, 1),
  [252] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_header, 5, 0, 1),
  [254] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 4, 0, 13),
  [256] = {.entry = {.count = 1, .reusable = true}}, SHIFT(214),
  [258] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 1, 0, 17),
  [260] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 2, 0, 21),
  [262] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 5, 0, 13),
  [264] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 6, 0, 19),
  [266] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 5, 0, 19),
  [268] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 3, 0, 24),
  [270] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_map_type, 5, 0, 27),
  [272] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_custom_type, 1, 0, 0),
  [274] = {.entry = {.count = 1, .reusable = true}}, SHIFT(182),
  [276] = {.entry = {.count = 1, .reusable = true}}, SHIFT(136),
  [278] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_primitive_type, 1, 0, 0),
  [280] = {.entry = {.count = 1, .reusable = true}}, SHIFT(54),
  [282] = {.entry = {.count = 1, .reusable = true}}, SHIFT(68),
  [284] = {.entry = {.count = 1, .reusable = true}}, SHIFT(112),
  [286] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [288] = {.entry = {.count = 1, .reusable = true}}, SHIFT(212),
  [290] = {.entry = {.count = 1, .reusable = true}}, SHIFT(73),
  [292] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [294] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_list_type, 3, 0, 18),
  [296] = {.entry = {.count = 1, .reusable = true}}, SHIFT(32),
  [298] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_args, 2, 0, 0),
  [300] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_value, 1, 0, 0),
  [302] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_quoted_string, 1, 0, 0),
  [304] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_boolean, 1, 0, 0),
  [306] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_args, 1, 0, 0),
  [308] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_import_list_repeat1, 2, 0, 0), SHIFT_REPEAT(137),
  [311] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_import_list_repeat1, 2, 0, 0),
  [313] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_text, 1, 0, 0),
  [315] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_depends_list_repeat1, 2, 0, 0), SHIFT_REPEAT(102),
  [318] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_depends_list_repeat1, 2, 0, 0),
  [320] = {.entry = {.count = 1, .reusable = true}}, SHIFT(102),
  [322] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_list, 1, 0, 0),
  [324] = {.entry = {.count = 1, .reusable = true}}, SHIFT(137),
  [326] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_import_list, 1, 0, 0),
  [328] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_field_constraints, 1, 0, 0),
  [330] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_error_args_repeat1, 2, 0, 0), SHIFT_REPEAT(65),
  [333] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_error_args_repeat1, 2, 0, 0),
  [335] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_step_text, 1, 0, 0),
  [337] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_import_list, 2, 0, 0),
  [339] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_list, 2, 0, 0),
  [341] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_input_constraints_repeat1, 2, 0, 0), SHIFT_REPEAT(54),
  [344] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_input_constraints_repeat1, 2, 0, 0),
  [346] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_test_args_repeat1, 2, 0, 0), SHIFT_REPEAT(32),
  [349] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_test_args_repeat1, 2, 0, 0),
  [351] = {.entry = {.count = 1, .reusable = true}}, SHIFT(180),
  [353] = {.entry = {.count = 1, .reusable = true}}, SHIFT(181),
  [355] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_constraints, 1, 0, 0),
  [357] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_spec, 1, 0, 0),
  [359] = {.entry = {.count = 1, .reusable = true}}, SHIFT(125),
  [361] = {.entry = {.count = 1, .reusable = true}}, SHIFT(65),
  [363] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_args, 1, 0, 0),
  [365] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_args, 2, 0, 0),
  [367] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_arrow, 1, 0, 0),
  [369] = {.entry = {.count = 1, .reusable = true}}, SHIFT(144),
  [371] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_reference, 3, 0, 0),
  [373] = {.entry = {.count = 1, .reusable = false}}, SHIFT(92),
  [375] = {.entry = {.count = 1, .reusable = false}}, SHIFT(186),
  [377] = {.entry = {.count = 1, .reusable = false}}, SHIFT(199),
  [379] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_condition_text, 1, 0, 0),
  [381] = {.entry = {.count = 1, .reusable = false}}, SHIFT(122),
  [383] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_spec, 2, 0, 0),
  [385] = {.entry = {.count = 1, .reusable = false}}, SHIFT(194),
  [387] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_assertion, 4, 0, 14),
  [389] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_state_prefix, 3, 0, 23),
  [391] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_header, 6, 0, 15),
  [393] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_reference, 1, 0, 0),
  [395] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 3, 0, 21),
  [397] = {.entry = {.count = 1, .reusable = true}}, SHIFT(61),
  [399] = {.entry = {.count = 1, .reusable = true}}, SHIFT(71),
  [401] = {.entry = {.count = 1, .reusable = true}}, SHIFT(60),
  [403] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [405] = {.entry = {.count = 1, .reusable = true}}, SHIFT(40),
  [407] = {.entry = {.count = 1, .reusable = true}}, SHIFT(110),
  [409] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_call, 4, 0, 12),
  [411] = {.entry = {.count = 1, .reusable = true}}, SHIFT(113),
  [413] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [415] = {.entry = {.count = 1, .reusable = true}}, SHIFT(30),
  [417] = {.entry = {.count = 1, .reusable = true}}, SHIFT(171),
  [419] = {.entry = {.count = 1, .reusable = true}}, SHIFT(46),
  [421] = {.entry = {.count = 1, .reusable = true}}, SHIFT(106),
  [423] = {.entry = {.count = 1, .reusable = true}}, SHIFT(50),
  [425] = {.entry = {.count = 1, .reusable = true}}, SHIFT(177),
  [427] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [429] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [431] = {.entry = {.count = 1, .reusable = true}}, SHIFT(20),
  [433] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_extends_clause, 2, 0, 6),
  [435] = {.entry = {.count = 1, .reusable = true}}, SHIFT(67),
  [437] = {.entry = {.count = 1, .reusable = true}}, SHIFT(131),
  [439] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_call, 3, 0, 12),
  [441] = {.entry = {.count = 1, .reusable = true}}, SHIFT(146),
  [443] = {.entry = {.count = 1, .reusable = true}}, SHIFT(31),
  [445] = {.entry = {.count = 1, .reusable = true}}, SHIFT(167),
  [447] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [449] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_header, 4, 0, 7),
  [451] = {.entry = {.count = 1, .reusable = true}}, SHIFT(135),
  [453] = {.entry = {.count = 1, .reusable = true}}, SHIFT(72),
  [455] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [457] = {.entry = {.count = 1, .reusable = true}}, SHIFT(45),
  [459] = {.entry = {.count = 1, .reusable = true}}, SHIFT(178),
  [461] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_text, 1, 0, 0),
  [463] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [465] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_spec, 1, 2, 0),
  [467] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_spec, 1, 1, 0),
  [469] = {.entry = {.count = 1, .reusable = true}}, SHIFT(58),
  [471] = {.entry = {.count = 1, .reusable = true}}, SHIFT(132),
  [473] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [475] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [477] = {.entry = {.count = 1, .reusable = true}}, SHIFT(66),
  [479] = {.entry = {.count = 1, .reusable = true}}, SHIFT(158),
  [481] = {.entry = {.count = 1, .reusable = true}}, SHIFT(210),
  [483] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [485] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 2, 0, 17),
  [487] = {.entry = {.count = 1, .reusable = true}}, SHIFT(63),
  [489] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_behavior_text, 1, 0, 0),
  [491] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [493] = {.entry = {.count = 1, .reusable = true}}, SHIFT(159),
  [495] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [497] = {.entry = {.count = 1, .reusable = true}}, SHIFT(164),
  [499] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [501] = {.entry = {.count = 1, .reusable = true}}, SHIFT(190),
  [503] = {.entry = {.count = 1, .reusable = true}}, SHIFT(166),
  [505] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_description_text, 1, 0, 0),
  [507] = {.entry = {.count = 1, .reusable = true}}, SHIFT(192),
  [509] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_prefix, 3, 0, 0),
  [511] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [513] = {.entry = {.count = 1, .reusable = true}}, SHIFT(57),
  [515] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_returns_text, 1, 0, 0),
  [517] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_output_binding, 2, 0, 25),
  [519] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [521] = {.entry = {.count = 1, .reusable = true}}, SHIFT(51),
  [523] = {.entry = {.count = 1, .reusable = true}}, SHIFT(41),
  [525] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_call, 3, 0, 28),
  [527] = {.entry = {.count = 1, .reusable = true}}, SHIFT(208),
  [529] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_bullet, 1, 0, 0),
  [531] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 4, 0, 24),
  [533] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_call, 4, 0, 28),
  [535] = {.entry = {.count = 1, .reusable = true}}, SHIFT(203),
  [537] = {.entry = {.count = 1, .reusable = true}}, SHIFT(114),
  [539] = {.entry = {.count = 1, .reusable = true}}, SHIFT(193),
  [541] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_target_name, 1, 0, 0),
  [543] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_bullet, 1, 0, 0),
  [545] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arrow, 1, 0, 0),
  [547] = {.entry = {.count = 1, .reusable = true}}, SHIFT(196),
};

enum ts_external_scanner_symbol_identifiers {
  ts_external_token_literal_content = 0,
};

static const TSSymbol ts_external_scanner_symbol_map[EXTERNAL_TOKEN_COUNT] = {
  [ts_external_token_literal_content] = sym_literal_content,
};

static const bool ts_external_scanner_states[2][EXTERNAL_TOKEN_COUNT] = {
  [1] = {
    [ts_external_token_literal_content] = true,
  },
};

#ifdef __cplusplus
extern "C" {
#endif
void *tree_sitter_nl_external_scanner_create(void);
void tree_sitter_nl_external_scanner_destroy(void *);
bool tree_sitter_nl_external_scanner_scan(void *, TSLexer *, const bool *);
unsigned tree_sitter_nl_external_scanner_serialize(void *, char *);
void tree_sitter_nl_external_scanner_deserialize(void *, const char *, unsigned);

#ifdef TREE_SITTER_HIDE_SYMBOLS
#define TS_PUBLIC
#elif defined(_WIN32)
#define TS_PUBLIC __declspec(dllexport)
#else
#define TS_PUBLIC __attribute__((visibility("default")))
#endif

TS_PUBLIC const TSLanguage *tree_sitter_nl(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .field_names = ts_field_names,
    .field_map_slices = ts_field_map_slices,
    .field_map_entries = ts_field_map_entries,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .external_scanner = {
      &ts_external_scanner_states[0][0],
      ts_external_scanner_symbol_map,
      tree_sitter_nl_external_scanner_create,
      tree_sitter_nl_external_scanner_destroy,
      tree_sitter_nl_external_scanner_scan,
      tree_sitter_nl_external_scanner_serialize,
      tree_sitter_nl_external_scanner_deserialize,
    },
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
