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
#define STATE_COUNT 248
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 169
#define ALIAS_COUNT 0
#define TOKEN_COUNT 78
#define EXTERNAL_TOKEN_COUNT 1
#define FIELD_COUNT 25
#define MAX_ALIAS_SEQUENCE_LENGTH 6
#define PRODUCTION_ID_COUNT 32

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
  anon_sym_none = 17,
  anon_sym_COLON = 18,
  anon_sym_required = 19,
  anon_sym_optional = 20,
  aux_sym_guards_section_token1 = 21,
  aux_sym_guard_text_token1 = 22,
  anon_sym_LPAREN = 23,
  anon_sym_RPAREN = 24,
  aux_sym_logic_section_token1 = 25,
  anon_sym_DOT = 26,
  sym_step_number = 27,
  sym_state_name = 28,
  aux_sym_condition_prefix_token1 = 29,
  aux_sym_condition_prefix_token2 = 30,
  aux_sym_condition_token_token1 = 31,
  aux_sym_condition_token_token2 = 32,
  aux_sym_condition_token_token3 = 33,
  aux_sym_condition_token_token4 = 34,
  aux_sym_condition_token_token5 = 35,
  anon_sym_and = 36,
  anon_sym_or = 37,
  anon_sym_not = 38,
  sym_step_text = 39,
  aux_sym_returns_section_token1 = 40,
  aux_sym_depends_section_token1 = 41,
  aux_sym_edge_cases_section_token1 = 42,
  anon_sym_ATtype = 43,
  anon_sym_LBRACE = 44,
  anon_sym_extends = 45,
  sym_type_name = 46,
  anon_sym_RBRACE = 47,
  anon_sym_ATtest = 48,
  anon_sym_EQ_EQ = 49,
  anon_sym_ATinvariant = 50,
  anon_sym_ATproperty = 51,
  sym_expression_text = 52,
  anon_sym_ATliteral = 53,
  anon_sym_QMARK = 54,
  anon_sym_number = 55,
  anon_sym_string = 56,
  anon_sym_boolean = 57,
  anon_sym_void = 58,
  anon_sym_any = 59,
  anon_sym_list = 60,
  anon_sym_of = 61,
  anon_sym_map = 62,
  anon_sym_to = 63,
  sym_number = 64,
  aux_sym_quoted_string_token1 = 65,
  aux_sym_quoted_string_token2 = 66,
  anon_sym_true = 67,
  anon_sym_false = 68,
  anon_sym_True = 69,
  anon_sym_False = 70,
  anon_sym_u2022 = 71,
  anon_sym_DASH = 72,
  anon_sym_STAR = 73,
  anon_sym_u2192 = 74,
  anon_sym_DASH_GT = 75,
  sym__newline = 76,
  sym_literal_content = 77,
  sym_source_file = 78,
  sym_directive = 79,
  sym_module_directive = 80,
  sym_version_directive = 81,
  sym_target_directive = 82,
  sym_imports_directive = 83,
  sym_target_name = 84,
  sym_import_list = 85,
  sym_anlu_block = 86,
  sym_anlu_header = 87,
  sym_purpose_section = 88,
  sym_description_text = 89,
  sym_inputs_section = 90,
  sym_input_item = 91,
  sym_input_constraints = 92,
  sym_guards_section = 93,
  sym_guard_item = 94,
  sym_guard_text = 95,
  sym_error_spec = 96,
  sym_error_call = 97,
  sym_error_args = 98,
  sym_error_text = 99,
  sym_logic_section = 100,
  sym_logic_item = 101,
  sym_logic_step = 102,
  sym_state_prefix = 103,
  sym_condition_prefix = 104,
  sym_condition_text = 105,
  sym_condition_token = 106,
  sym_output_binding = 107,
  sym_returns_section = 108,
  sym_returns_text = 109,
  sym_depends_section = 110,
  sym_depends_list = 111,
  sym_anlu_reference = 112,
  sym_edge_cases_section = 113,
  sym_edge_case_item = 114,
  sym_edge_condition_text = 115,
  sym_edge_behavior_text = 116,
  sym_type_block = 117,
  sym_type_header = 118,
  sym_extends_clause = 119,
  sym_type_field = 120,
  sym_field_constraints = 121,
  sym_constraint_pair = 122,
  sym_type_close = 123,
  sym_test_block = 124,
  sym_test_header = 125,
  sym_test_assertion = 126,
  sym_test_call = 127,
  sym_test_args = 128,
  sym_test_value = 129,
  sym_test_close = 130,
  sym_invariant_block = 131,
  sym_invariant_header = 132,
  sym_invariant_assertion = 133,
  sym_invariant_close = 134,
  sym_property_block = 135,
  sym_property_header = 136,
  sym_property_assertion = 137,
  sym_property_close = 138,
  sym_literal_block = 139,
  sym_literal_header = 140,
  sym_literal_close = 141,
  sym_type_spec = 142,
  sym__base_type = 143,
  sym_primitive_type = 144,
  sym_list_type = 145,
  sym_map_type = 146,
  sym_custom_type = 147,
  sym_quoted_string = 148,
  sym_boolean = 149,
  sym_identifier = 150,
  sym_bullet = 151,
  sym_arrow = 152,
  aux_sym_source_file_repeat1 = 153,
  aux_sym_import_list_repeat1 = 154,
  aux_sym_anlu_block_repeat1 = 155,
  aux_sym_inputs_section_repeat1 = 156,
  aux_sym_input_constraints_repeat1 = 157,
  aux_sym_guards_section_repeat1 = 158,
  aux_sym_error_args_repeat1 = 159,
  aux_sym_logic_section_repeat1 = 160,
  aux_sym_condition_text_repeat1 = 161,
  aux_sym_depends_list_repeat1 = 162,
  aux_sym_edge_cases_section_repeat1 = 163,
  aux_sym_type_block_repeat1 = 164,
  aux_sym_test_block_repeat1 = 165,
  aux_sym_test_args_repeat1 = 166,
  aux_sym_invariant_block_repeat1 = 167,
  aux_sym_property_block_repeat1 = 168,
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
  [anon_sym_none] = "none_marker",
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
  [sym_step_text] = "step_text",
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
  [anon_sym_ATinvariant] = "@invariant",
  [anon_sym_ATproperty] = "@property",
  [sym_expression_text] = "expression_text",
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
  [sym_constraint_pair] = "constraint_pair",
  [sym_type_close] = "type_close",
  [sym_test_block] = "test_block",
  [sym_test_header] = "test_header",
  [sym_test_assertion] = "test_assertion",
  [sym_test_call] = "test_call",
  [sym_test_args] = "test_args",
  [sym_test_value] = "test_value",
  [sym_test_close] = "test_close",
  [sym_invariant_block] = "invariant_block",
  [sym_invariant_header] = "invariant_header",
  [sym_invariant_assertion] = "invariant_assertion",
  [sym_invariant_close] = "invariant_close",
  [sym_property_block] = "property_block",
  [sym_property_header] = "property_header",
  [sym_property_assertion] = "property_assertion",
  [sym_property_close] = "property_close",
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
  [aux_sym_invariant_block_repeat1] = "invariant_block_repeat1",
  [aux_sym_property_block_repeat1] = "property_block_repeat1",
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
  [anon_sym_none] = anon_sym_none,
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
  [sym_step_text] = sym_step_text,
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
  [anon_sym_ATinvariant] = anon_sym_ATinvariant,
  [anon_sym_ATproperty] = anon_sym_ATproperty,
  [sym_expression_text] = sym_expression_text,
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
  [sym_constraint_pair] = sym_constraint_pair,
  [sym_type_close] = sym_type_close,
  [sym_test_block] = sym_test_block,
  [sym_test_header] = sym_test_header,
  [sym_test_assertion] = sym_test_assertion,
  [sym_test_call] = sym_test_call,
  [sym_test_args] = sym_test_args,
  [sym_test_value] = sym_test_value,
  [sym_test_close] = sym_test_close,
  [sym_invariant_block] = sym_invariant_block,
  [sym_invariant_header] = sym_invariant_header,
  [sym_invariant_assertion] = sym_invariant_assertion,
  [sym_invariant_close] = sym_invariant_close,
  [sym_property_block] = sym_property_block,
  [sym_property_header] = sym_property_header,
  [sym_property_assertion] = sym_property_assertion,
  [sym_property_close] = sym_property_close,
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
  [aux_sym_invariant_block_repeat1] = aux_sym_invariant_block_repeat1,
  [aux_sym_property_block_repeat1] = aux_sym_property_block_repeat1,
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
  [anon_sym_none] = {
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
  [sym_step_text] = {
    .visible = true,
    .named = true,
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
  [anon_sym_ATinvariant] = {
    .visible = true,
    .named = false,
  },
  [anon_sym_ATproperty] = {
    .visible = true,
    .named = false,
  },
  [sym_expression_text] = {
    .visible = true,
    .named = true,
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
  [sym_constraint_pair] = {
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
  [sym_invariant_block] = {
    .visible = true,
    .named = true,
  },
  [sym_invariant_header] = {
    .visible = true,
    .named = true,
  },
  [sym_invariant_assertion] = {
    .visible = true,
    .named = true,
  },
  [sym_invariant_close] = {
    .visible = true,
    .named = true,
  },
  [sym_property_block] = {
    .visible = true,
    .named = true,
  },
  [sym_property_header] = {
    .visible = true,
    .named = true,
  },
  [sym_property_assertion] = {
    .visible = true,
    .named = true,
  },
  [sym_property_close] = {
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
  [aux_sym_invariant_block_repeat1] = {
    .visible = false,
    .named = false,
  },
  [aux_sym_property_block_repeat1] = {
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
  field_expression = 12,
  field_function = 13,
  field_header = 14,
  field_imports = 15,
  field_key = 16,
  field_language = 17,
  field_name = 18,
  field_number = 19,
  field_state = 20,
  field_target = 21,
  field_type = 22,
  field_value = 23,
  field_variable = 24,
  field_version = 25,
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
  [field_expression] = "expression",
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
  [8] = {.index = 7, .length = 1},
  [9] = {.index = 8, .length = 1},
  [10] = {.index = 9, .length = 2},
  [11] = {.index = 11, .length = 1},
  [12] = {.index = 12, .length = 2},
  [13] = {.index = 14, .length = 2},
  [14] = {.index = 16, .length = 1},
  [15] = {.index = 17, .length = 2},
  [16] = {.index = 19, .length = 2},
  [17] = {.index = 21, .length = 1},
  [18] = {.index = 22, .length = 1},
  [19] = {.index = 23, .length = 1},
  [20] = {.index = 24, .length = 1},
  [21] = {.index = 25, .length = 2},
  [22] = {.index = 27, .length = 1},
  [23] = {.index = 28, .length = 1},
  [24] = {.index = 29, .length = 2},
  [25] = {.index = 31, .length = 1},
  [26] = {.index = 32, .length = 1},
  [27] = {.index = 33, .length = 1},
  [28] = {.index = 34, .length = 2},
  [29] = {.index = 36, .length = 2},
  [30] = {.index = 38, .length = 2},
  [31] = {.index = 40, .length = 1},
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
    {field_expression, 0},
  [5] =
    {field_content, 1},
  [6] =
    {field_base, 1},
  [7] =
    {field_type, 1},
  [8] =
    {field_language, 1},
  [9] =
    {field_description, 1},
    {field_header, 0},
  [11] =
    {field_header, 0},
  [12] =
    {field_header, 0},
    {field_value, 1},
  [14] =
    {field_dependencies, 1},
    {field_header, 0},
  [16] =
    {field_function, 0},
  [17] =
    {field_name, 0},
    {field_type, 2},
  [19] =
    {field_call, 0},
    {field_expected, 2},
  [21] =
    {field_anlu, 2},
  [22] =
    {field_condition, 1},
  [23] =
    {field_description, 0},
  [24] =
    {field_element, 2},
  [25] =
    {field_name, 1},
    {field_type, 3},
  [27] =
    {field_number, 0},
  [28] =
    {field_description, 1},
  [29] =
    {field_condition, 1},
    {field_error, 3},
  [31] =
    {field_state, 1},
  [32] =
    {field_variable, 1},
  [33] =
    {field_description, 2},
  [34] =
    {field_behavior, 3},
    {field_condition, 1},
  [36] =
    {field_key, 2},
    {field_value, 4},
  [38] =
    {field_key, 0},
    {field_value, 2},
  [40] =
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
  [213] = 213,
  [214] = 214,
  [215] = 215,
  [216] = 216,
  [217] = 217,
  [218] = 218,
  [219] = 219,
  [220] = 220,
  [221] = 221,
  [222] = 222,
  [223] = 223,
  [224] = 224,
  [225] = 225,
  [226] = 226,
  [227] = 227,
  [228] = 228,
  [229] = 229,
  [230] = 230,
  [231] = 231,
  [232] = 232,
  [233] = 233,
  [234] = 234,
  [235] = 235,
  [236] = 236,
  [237] = 237,
  [238] = 238,
  [239] = 239,
  [240] = 240,
  [241] = 241,
  [242] = 242,
  [243] = 243,
  [244] = 244,
  [245] = 196,
  [246] = 134,
  [247] = 247,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(207);
      ADVANCE_MAP(
        '\n', 366,
        '\r', 1,
        '"', 7,
        '#', 211,
        '\'', 19,
        '(', 240,
        ')', 241,
        '*', 363,
        ',', 221,
        '-', 362,
        '.', 243,
        ':', 232,
        '=', 311,
        '?', 339,
        '@', 65,
        'D', 162,
        'E', 159,
        'F', 30,
        'G', 195,
        'I', 169,
        'L', 178,
        'P', 196,
        'R', 163,
        'T', 111,
        '[', 222,
        ']', 224,
        'a', 250,
        'b', 254,
        'd', 259,
        'e', 256,
        'f', 247,
        'g', 264,
        'i', 261,
        'l', 249,
        'm', 246,
        'n', 251,
        'o', 248,
        'p', 257,
        'r', 245,
        's', 255,
        't', 252,
        'v', 253,
        '{', 327,
        '}', 330,
        0x2022, 361,
        0x2192, 364,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(0);
      if (('+' <= lookahead && lookahead <= '/')) ADVANCE(314);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(312);
      if (('c' <= lookahead && lookahead <= 'z')) ADVANCE(244);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(266);
      END_STATE();
    case 1:
      if (lookahead == '\n') ADVANCE(366);
      END_STATE();
    case 2:
      ADVANCE_MAP(
        '\n', 366,
        '\r', 1,
        '"', 7,
        '#', 211,
        '\'', 19,
        ')', 241,
        '-', 29,
        'F', 272,
        'T', 294,
        'f', 274,
        't', 297,
        0x2192, 364,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(349);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 3:
      ADVANCE_MAP(
        '\n', 366,
        '\r', 1,
        '#', 211,
        ',', 221,
        '?', 339,
        'a', 88,
        'b', 96,
        'e', 151,
        'l', 66,
        'm', 31,
        'n', 103,
        'o', 61,
        'p', 154,
        'r', 148,
        's', 140,
        't', 93,
        'v', 95,
        '{', 327,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(3);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(20);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(329);
      END_STATE();
    case 4:
      ADVANCE_MAP(
        '"', 7,
        '#', 211,
        '\'', 19,
        ')', 241,
        '*', 363,
        '-', 362,
        '}', 330,
        0x2022, 361,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(4);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 5:
      if (lookahead == '"') ADVANCE(7);
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '\'') ADVANCE(19);
      if (lookahead == '-') ADVANCE(201);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(5);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(349);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 6:
      if (lookahead == '"') ADVANCE(7);
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '\'') ADVANCE(19);
      if (lookahead == 'o') ADVANCE(292);
      if (lookahead == 'r') ADVANCE(281);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(6);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 7:
      if (lookahead == '"') ADVANCE(351);
      if (lookahead != 0) ADVANCE(7);
      END_STATE();
    case 8:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '[') ADVANCE(222);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(8);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(225);
      END_STATE();
    case 9:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == 'a') ADVANCE(288);
      if (lookahead == 'n') ADVANCE(290);
      if (lookahead == 'o') ADVANCE(295);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(9);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(306);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(312);
      if (lookahead == '(' ||
          lookahead == ')' ||
          lookahead == '[' ||
          lookahead == ']') ADVANCE(313);
      if (lookahead == '*' ||
          lookahead == '+' ||
          lookahead == '-' ||
          lookahead == '/') ADVANCE(314);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(309);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 10:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == 'a') ADVANCE(288);
      if (lookahead == 'n') ADVANCE(290);
      if (lookahead == 'o') ADVANCE(295);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(10);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(312);
      if (lookahead == '(' ||
          lookahead == ')' ||
          lookahead == '[' ||
          lookahead == ']') ADVANCE(313);
      if (lookahead == '*' ||
          lookahead == '+' ||
          lookahead == '-' ||
          lookahead == '/') ADVANCE(314);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(309);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 11:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(227);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(228);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(229);
      END_STATE();
    case 12:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(12);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(267);
      END_STATE();
    case 13:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(13);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(172);
      END_STATE();
    case 14:
      if (lookahead == '#') ADVANCE(209);
      if (lookahead == '-') ADVANCE(199);
      if (lookahead == '[') ADVANCE(223);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(14);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(321);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(322);
      END_STATE();
    case 15:
      if (lookahead == '#') ADVANCE(209);
      if (lookahead == '-') ADVANCE(199);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(15);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(321);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(322);
      END_STATE();
    case 16:
      if (lookahead == '#') ADVANCE(209);
      if (lookahead == '-') ADVANCE(199);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(16);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(322);
      END_STATE();
    case 17:
      if (lookahead == '#') ADVANCE(208);
      if (lookahead == '}') ADVANCE(330);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(336);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(337);
      END_STATE();
    case 18:
      if (lookahead == '#') ADVANCE(210);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(238);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(239);
      END_STATE();
    case 19:
      if (lookahead == '\'') ADVANCE(352);
      if (lookahead != 0) ADVANCE(19);
      END_STATE();
    case 20:
      if (lookahead == '.') ADVANCE(203);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(20);
      END_STATE();
    case 21:
      if (lookahead == ':') ADVANCE(242);
      END_STATE();
    case 22:
      if (lookahead == ':') ADVANCE(237);
      END_STATE();
    case 23:
      if (lookahead == ':') ADVANCE(230);
      END_STATE();
    case 24:
      if (lookahead == ':') ADVANCE(324);
      END_STATE();
    case 25:
      if (lookahead == ':') ADVANCE(226);
      END_STATE();
    case 26:
      if (lookahead == ':') ADVANCE(323);
      END_STATE();
    case 27:
      if (lookahead == ':') ADVANCE(325);
      END_STATE();
    case 28:
      if (lookahead == '=') ADVANCE(332);
      END_STATE();
    case 29:
      if (lookahead == '>') ADVANCE(365);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(349);
      END_STATE();
    case 30:
      if (lookahead == 'a') ADVANCE(77);
      END_STATE();
    case 31:
      if (lookahead == 'a') ADVANCE(104);
      END_STATE();
    case 32:
      if (lookahead == 'a') ADVANCE(112);
      if (lookahead == 'e') ADVANCE(128);
      if (lookahead == 'y') ADVANCE(107);
      END_STATE();
    case 33:
      if (lookahead == 'a') ADVANCE(75);
      END_STATE();
    case 34:
      if (lookahead == 'a') ADVANCE(76);
      END_STATE();
    case 35:
      if (lookahead == 'a') ADVANCE(84);
      END_STATE();
    case 36:
      if (lookahead == 'a') ADVANCE(91);
      END_STATE();
    case 37:
      if (lookahead == 'a') ADVANCE(117);
      END_STATE();
    case 38:
      if (lookahead == 'b') ADVANCE(58);
      END_STATE();
    case 39:
      if (lookahead == 'c') ADVANCE(118);
      END_STATE();
    case 40:
      if (lookahead == 'd') ADVANCE(315);
      if (lookahead == 'y') ADVANCE(344);
      END_STATE();
    case 41:
      if (lookahead == 'd') ADVANCE(343);
      END_STATE();
    case 42:
      if (lookahead == 'd') ADVANCE(233);
      END_STATE();
    case 43:
      if (lookahead == 'd') ADVANCE(149);
      END_STATE();
    case 44:
      if (lookahead == 'd') ADVANCE(124);
      END_STATE();
    case 45:
      if (lookahead == 'e') ADVANCE(357);
      END_STATE();
    case 46:
      if (lookahead == 'e') ADVANCE(87);
      END_STATE();
    case 47:
      if (lookahead == 'e') ADVANCE(231);
      END_STATE();
    case 48:
      if (lookahead == 'e') ADVANCE(353);
      END_STATE();
    case 49:
      if (lookahead == 'e') ADVANCE(326);
      END_STATE();
    case 50:
      if (lookahead == 'e') ADVANCE(359);
      END_STATE();
    case 51:
      if (lookahead == 'e') ADVANCE(355);
      END_STATE();
    case 52:
      if (lookahead == 'e') ADVANCE(212);
      END_STATE();
    case 53:
      if (lookahead == 'e') ADVANCE(35);
      END_STATE();
    case 54:
      if (lookahead == 'e') ADVANCE(115);
      END_STATE();
    case 55:
      if (lookahead == 'e') ADVANCE(123);
      END_STATE();
    case 56:
      if (lookahead == 'e') ADVANCE(42);
      END_STATE();
    case 57:
      if (lookahead == 'e') ADVANCE(122);
      END_STATE();
    case 58:
      if (lookahead == 'e') ADVANCE(113);
      END_STATE();
    case 59:
      if (lookahead == 'e') ADVANCE(136);
      END_STATE();
    case 60:
      if (lookahead == 'e') ADVANCE(120);
      END_STATE();
    case 61:
      if (lookahead == 'f') ADVANCE(346);
      END_STATE();
    case 62:
      if (lookahead == 'g') ADVANCE(341);
      END_STATE();
    case 63:
      if (lookahead == 'g') ADVANCE(59);
      END_STATE();
    case 64:
      if (lookahead == 'h') ADVANCE(100);
      END_STATE();
    case 65:
      if (lookahead == 'i') ADVANCE(82);
      if (lookahead == 'l') ADVANCE(69);
      if (lookahead == 'm') ADVANCE(94);
      if (lookahead == 'p') ADVANCE(114);
      if (lookahead == 't') ADVANCE(32);
      if (lookahead == 'v') ADVANCE(54);
      END_STATE();
    case 66:
      if (lookahead == 'i') ADVANCE(126);
      END_STATE();
    case 67:
      if (lookahead == 'i') ADVANCE(41);
      END_STATE();
    case 68:
      if (lookahead == 'i') ADVANCE(86);
      END_STATE();
    case 69:
      if (lookahead == 'i') ADVANCE(144);
      END_STATE();
    case 70:
      if (lookahead == 'i') ADVANCE(98);
      END_STATE();
    case 71:
      if (lookahead == 'i') ADVANCE(108);
      END_STATE();
    case 72:
      if (lookahead == 'i') ADVANCE(102);
      END_STATE();
    case 73:
      if (lookahead == 'i') ADVANCE(121);
      END_STATE();
    case 74:
      if (lookahead == 'i') ADVANCE(36);
      END_STATE();
    case 75:
      if (lookahead == 'l') ADVANCE(338);
      END_STATE();
    case 76:
      if (lookahead == 'l') ADVANCE(235);
      END_STATE();
    case 77:
      if (lookahead == 'l') ADVANCE(129);
      END_STATE();
    case 78:
      if (lookahead == 'l') ADVANCE(53);
      END_STATE();
    case 79:
      if (lookahead == 'l') ADVANCE(52);
      END_STATE();
    case 80:
      if (lookahead == 'l') ADVANCE(130);
      END_STATE();
    case 81:
      if (lookahead == 'm') ADVANCE(38);
      END_STATE();
    case 82:
      if (lookahead == 'm') ADVANCE(105);
      if (lookahead == 'n') ADVANCE(150);
      END_STATE();
    case 83:
      if (lookahead == 'n') ADVANCE(218);
      END_STATE();
    case 84:
      if (lookahead == 'n') ADVANCE(342);
      END_STATE();
    case 85:
      if (lookahead == 'n') ADVANCE(213);
      END_STATE();
    case 86:
      if (lookahead == 'n') ADVANCE(62);
      END_STATE();
    case 87:
      if (lookahead == 'n') ADVANCE(44);
      END_STATE();
    case 88:
      if (lookahead == 'n') ADVANCE(152);
      END_STATE();
    case 89:
      if (lookahead == 'n') ADVANCE(47);
      END_STATE();
    case 90:
      if (lookahead == 'n') ADVANCE(47);
      if (lookahead == 't') ADVANCE(319);
      END_STATE();
    case 91:
      if (lookahead == 'n') ADVANCE(138);
      END_STATE();
    case 92:
      if (lookahead == 'n') ADVANCE(34);
      END_STATE();
    case 93:
      if (lookahead == 'o') ADVANCE(348);
      if (lookahead == 'y') ADVANCE(106);
      END_STATE();
    case 94:
      if (lookahead == 'o') ADVANCE(43);
      END_STATE();
    case 95:
      if (lookahead == 'o') ADVANCE(67);
      END_STATE();
    case 96:
      if (lookahead == 'o') ADVANCE(97);
      END_STATE();
    case 97:
      if (lookahead == 'o') ADVANCE(78);
      END_STATE();
    case 98:
      if (lookahead == 'o') ADVANCE(92);
      END_STATE();
    case 99:
      if (lookahead == 'o') ADVANCE(109);
      END_STATE();
    case 100:
      if (lookahead == 'o') ADVANCE(83);
      END_STATE();
    case 101:
      if (lookahead == 'o') ADVANCE(119);
      END_STATE();
    case 102:
      if (lookahead == 'o') ADVANCE(85);
      END_STATE();
    case 103:
      if (lookahead == 'o') ADVANCE(89);
      if (lookahead == 'u') ADVANCE(81);
      END_STATE();
    case 104:
      if (lookahead == 'p') ADVANCE(347);
      END_STATE();
    case 105:
      if (lookahead == 'p') ADVANCE(101);
      END_STATE();
    case 106:
      if (lookahead == 'p') ADVANCE(55);
      END_STATE();
    case 107:
      if (lookahead == 'p') ADVANCE(49);
      END_STATE();
    case 108:
      if (lookahead == 'p') ADVANCE(139);
      END_STATE();
    case 109:
      if (lookahead == 'p') ADVANCE(60);
      END_STATE();
    case 110:
      if (lookahead == 'q') ADVANCE(146);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(198);
      END_STATE();
    case 111:
      if (lookahead == 'r') ADVANCE(145);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(164);
      END_STATE();
    case 112:
      if (lookahead == 'r') ADVANCE(63);
      END_STATE();
    case 113:
      if (lookahead == 'r') ADVANCE(340);
      END_STATE();
    case 114:
      if (lookahead == 'r') ADVANCE(99);
      END_STATE();
    case 115:
      if (lookahead == 'r') ADVANCE(131);
      END_STATE();
    case 116:
      if (lookahead == 'r') ADVANCE(68);
      END_STATE();
    case 117:
      if (lookahead == 'r') ADVANCE(74);
      END_STATE();
    case 118:
      if (lookahead == 'r') ADVANCE(71);
      END_STATE();
    case 119:
      if (lookahead == 'r') ADVANCE(143);
      END_STATE();
    case 120:
      if (lookahead == 'r') ADVANCE(137);
      END_STATE();
    case 121:
      if (lookahead == 'r') ADVANCE(56);
      END_STATE();
    case 122:
      if (lookahead == 'r') ADVANCE(33);
      END_STATE();
    case 123:
      if (lookahead == 's') ADVANCE(39);
      END_STATE();
    case 124:
      if (lookahead == 's') ADVANCE(328);
      END_STATE();
    case 125:
      if (lookahead == 's') ADVANCE(215);
      END_STATE();
    case 126:
      if (lookahead == 's') ADVANCE(133);
      END_STATE();
    case 127:
      if (lookahead == 's') ADVANCE(134);
      END_STATE();
    case 128:
      if (lookahead == 's') ADVANCE(135);
      END_STATE();
    case 129:
      if (lookahead == 's') ADVANCE(50);
      END_STATE();
    case 130:
      if (lookahead == 's') ADVANCE(51);
      END_STATE();
    case 131:
      if (lookahead == 's') ADVANCE(72);
      END_STATE();
    case 132:
      if (lookahead == 't') ADVANCE(64);
      END_STATE();
    case 133:
      if (lookahead == 't') ADVANCE(345);
      END_STATE();
    case 134:
      if (lookahead == 't') ADVANCE(220);
      END_STATE();
    case 135:
      if (lookahead == 't') ADVANCE(331);
      END_STATE();
    case 136:
      if (lookahead == 't') ADVANCE(214);
      END_STATE();
    case 137:
      if (lookahead == 't') ADVANCE(153);
      END_STATE();
    case 138:
      if (lookahead == 't') ADVANCE(334);
      END_STATE();
    case 139:
      if (lookahead == 't') ADVANCE(219);
      END_STATE();
    case 140:
      if (lookahead == 't') ADVANCE(116);
      END_STATE();
    case 141:
      if (lookahead == 't') ADVANCE(70);
      END_STATE();
    case 142:
      if (lookahead == 't') ADVANCE(46);
      END_STATE();
    case 143:
      if (lookahead == 't') ADVANCE(125);
      END_STATE();
    case 144:
      if (lookahead == 't') ADVANCE(57);
      END_STATE();
    case 145:
      if (lookahead == 'u') ADVANCE(45);
      END_STATE();
    case 146:
      if (lookahead == 'u') ADVANCE(73);
      END_STATE();
    case 147:
      if (lookahead == 'u') ADVANCE(48);
      END_STATE();
    case 148:
      if (lookahead == 'u') ADVANCE(127);
      END_STATE();
    case 149:
      if (lookahead == 'u') ADVANCE(79);
      END_STATE();
    case 150:
      if (lookahead == 'v') ADVANCE(37);
      END_STATE();
    case 151:
      if (lookahead == 'x') ADVANCE(142);
      END_STATE();
    case 152:
      if (lookahead == 'y') ADVANCE(344);
      END_STATE();
    case 153:
      if (lookahead == 'y') ADVANCE(335);
      END_STATE();
    case 154:
      if (lookahead == 'y') ADVANCE(132);
      END_STATE();
    case 155:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(183);
      END_STATE();
    case 156:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(191);
      END_STATE();
    case 157:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(21);
      END_STATE();
    case 158:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(156);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') ADVANCE(158);
      END_STATE();
    case 159:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(171);
      END_STATE();
    case 160:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(186);
      END_STATE();
    case 161:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(188);
      END_STATE();
    case 162:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(182);
      END_STATE();
    case 163:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(193);
      END_STATE();
    case 164:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(174);
      END_STATE();
    case 165:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(200);
      END_STATE();
    case 166:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(176);
      END_STATE();
    case 167:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(25);
      END_STATE();
    case 168:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(192);
      END_STATE();
    case 169:
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(268);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(181);
      END_STATE();
    case 170:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(173);
      END_STATE();
    case 171:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(165);
      END_STATE();
    case 172:
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(164);
      END_STATE();
    case 173:
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(157);
      END_STATE();
    case 174:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(270);
      END_STATE();
    case 175:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(181);
      END_STATE();
    case 176:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(161);
      END_STATE();
    case 177:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(190);
      END_STATE();
    case 178:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(170);
      END_STATE();
    case 179:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(189);
      END_STATE();
    case 180:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(179);
      END_STATE();
    case 181:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(197);
      END_STATE();
    case 182:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(166);
      END_STATE();
    case 183:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(160);
      END_STATE();
    case 184:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(180);
      END_STATE();
    case 185:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(177);
      END_STATE();
    case 186:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(22);
      END_STATE();
    case 187:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(23);
      END_STATE();
    case 188:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(24);
      END_STATE();
    case 189:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(167);
      END_STATE();
    case 190:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(26);
      END_STATE();
    case 191:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(168);
      END_STATE();
    case 192:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(27);
      END_STATE();
    case 193:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(198);
      END_STATE();
    case 194:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(187);
      END_STATE();
    case 195:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(155);
      END_STATE();
    case 196:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(184);
      END_STATE();
    case 197:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(194);
      END_STATE();
    case 198:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(185);
      END_STATE();
    case 199:
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(199);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(322);
      END_STATE();
    case 200:
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') ADVANCE(158);
      END_STATE();
    case 201:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(349);
      END_STATE();
    case 202:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(350);
      END_STATE();
    case 203:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(216);
      END_STATE();
    case 204:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(217);
      END_STATE();
    case 205:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(310);
      END_STATE();
    case 206:
      if (eof) ADVANCE(207);
      ADVANCE_MAP(
        '\n', 366,
        '\r', 1,
        '#', 211,
        '(', 240,
        ')', 241,
        '*', 363,
        ',', 221,
        '-', 362,
        ':', 232,
        '=', 28,
        '@', 65,
        'D', 162,
        'E', 159,
        'G', 195,
        'I', 175,
        'L', 178,
        'P', 196,
        'R', 163,
        '[', 222,
        ']', 224,
        'd', 259,
        'e', 258,
        'g', 264,
        'i', 262,
        'l', 263,
        'p', 265,
        'r', 260,
        '{', 327,
        0x2022, 361,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(206);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(266);
      if (('a' <= lookahead && lookahead <= 'z')) ADVANCE(244);
      END_STATE();
    case 207:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 208:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == '}') ADVANCE(211);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(208);
      END_STATE();
    case 209:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == 0x2192) ADVANCE(211);
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(209);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(209);
      END_STATE();
    case 210:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == '-' ||
          lookahead == 0x2192) ADVANCE(211);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(210);
      END_STATE();
    case 211:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(211);
      END_STATE();
    case 212:
      ACCEPT_TOKEN(anon_sym_ATmodule);
      END_STATE();
    case 213:
      ACCEPT_TOKEN(anon_sym_ATversion);
      END_STATE();
    case 214:
      ACCEPT_TOKEN(anon_sym_ATtarget);
      END_STATE();
    case 215:
      ACCEPT_TOKEN(anon_sym_ATimports);
      END_STATE();
    case 216:
      ACCEPT_TOKEN(sym_version_string);
      if (lookahead == '.') ADVANCE(204);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(216);
      END_STATE();
    case 217:
      ACCEPT_TOKEN(sym_version_string);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(217);
      END_STATE();
    case 218:
      ACCEPT_TOKEN(anon_sym_python);
      END_STATE();
    case 219:
      ACCEPT_TOKEN(anon_sym_typescript);
      END_STATE();
    case 220:
      ACCEPT_TOKEN(anon_sym_rust);
      END_STATE();
    case 221:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 222:
      ACCEPT_TOKEN(anon_sym_LBRACK);
      END_STATE();
    case 223:
      ACCEPT_TOKEN(anon_sym_LBRACK);
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(199);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(322);
      END_STATE();
    case 224:
      ACCEPT_TOKEN(anon_sym_RBRACK);
      END_STATE();
    case 225:
      ACCEPT_TOKEN(sym_anlu_identifier);
      if (lookahead == '-' ||
          lookahead == '.' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(225);
      END_STATE();
    case 226:
      ACCEPT_TOKEN(aux_sym_purpose_section_token1);
      END_STATE();
    case 227:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(227);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(228);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(229);
      END_STATE();
    case 228:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(228);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(229);
      END_STATE();
    case 229:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(229);
      END_STATE();
    case 230:
      ACCEPT_TOKEN(aux_sym_inputs_section_token1);
      END_STATE();
    case 231:
      ACCEPT_TOKEN(anon_sym_none);
      END_STATE();
    case 232:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 233:
      ACCEPT_TOKEN(anon_sym_required);
      END_STATE();
    case 234:
      ACCEPT_TOKEN(anon_sym_required);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 235:
      ACCEPT_TOKEN(anon_sym_optional);
      END_STATE();
    case 236:
      ACCEPT_TOKEN(anon_sym_optional);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 237:
      ACCEPT_TOKEN(aux_sym_guards_section_token1);
      END_STATE();
    case 238:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead == '#') ADVANCE(210);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(238);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(239);
      END_STATE();
    case 239:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(239);
      END_STATE();
    case 240:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 241:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 242:
      ACCEPT_TOKEN(aux_sym_logic_section_token1);
      END_STATE();
    case 243:
      ACCEPT_TOKEN(anon_sym_DOT);
      END_STATE();
    case 244:
      ACCEPT_TOKEN(sym_step_number);
      END_STATE();
    case 245:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'E') ADVANCE(193);
      if (lookahead == 'e') ADVANCE(110);
      if (lookahead == 'u') ADVANCE(127);
      END_STATE();
    case 246:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'a') ADVANCE(104);
      END_STATE();
    case 247:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'a') ADVANCE(80);
      END_STATE();
    case 248:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'f') ADVANCE(346);
      if (lookahead == 'p') ADVANCE(141);
      if (lookahead == 'r') ADVANCE(317);
      END_STATE();
    case 249:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'i') ADVANCE(126);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(170);
      END_STATE();
    case 250:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'n') ADVANCE(40);
      END_STATE();
    case 251:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'o') ADVANCE(90);
      if (lookahead == 'u') ADVANCE(81);
      END_STATE();
    case 252:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'o') ADVANCE(348);
      if (lookahead == 'r') ADVANCE(147);
      if (lookahead == 'y') ADVANCE(106);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(164);
      END_STATE();
    case 253:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'o') ADVANCE(67);
      END_STATE();
    case 254:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'o') ADVANCE(97);
      END_STATE();
    case 255:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 't') ADVANCE(116);
      END_STATE();
    case 256:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'x') ADVANCE(142);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(171);
      END_STATE();
    case 257:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'y') ADVANCE(132);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(184);
      END_STATE();
    case 258:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(171);
      END_STATE();
    case 259:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(182);
      END_STATE();
    case 260:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(193);
      END_STATE();
    case 261:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(268);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(181);
      END_STATE();
    case 262:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(181);
      END_STATE();
    case 263:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(170);
      END_STATE();
    case 264:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(155);
      END_STATE();
    case 265:
      ACCEPT_TOKEN(sym_step_number);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(184);
      END_STATE();
    case 266:
      ACCEPT_TOKEN(sym_step_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(266);
      END_STATE();
    case 267:
      ACCEPT_TOKEN(sym_state_name);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(267);
      END_STATE();
    case 268:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token1);
      END_STATE();
    case 269:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token1);
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(199);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(322);
      END_STATE();
    case 270:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token2);
      END_STATE();
    case 271:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token2);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 272:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(285);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 273:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(286);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 274:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(287);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 275:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'd') ADVANCE(316);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 276:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'd') ADVANCE(234);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 277:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(358);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 278:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(354);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 279:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(360);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 280:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(356);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 281:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(293);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 282:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(276);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 283:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'i') ADVANCE(291);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 284:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'i') ADVANCE(296);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 285:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(298);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 286:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(236);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 287:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(299);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 288:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'n') ADVANCE(275);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 289:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'n') ADVANCE(273);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 290:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'o') ADVANCE(300);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 291:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'o') ADVANCE(289);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 292:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'p') ADVANCE(301);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 293:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'q') ADVANCE(304);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 294:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(302);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 295:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(318);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 296:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(282);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 297:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(303);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 298:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 's') ADVANCE(279);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 299:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 's') ADVANCE(280);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 300:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 't') ADVANCE(320);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 301:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 't') ADVANCE(283);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 302:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(277);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 303:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(278);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 304:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(284);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 305:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(307);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 306:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(305);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 307:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(271);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 308:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 309:
      ACCEPT_TOKEN(aux_sym_condition_token_token2);
      if (lookahead == '.') ADVANCE(205);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(309);
      END_STATE();
    case 310:
      ACCEPT_TOKEN(aux_sym_condition_token_token2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(310);
      END_STATE();
    case 311:
      ACCEPT_TOKEN(aux_sym_condition_token_token3);
      if (lookahead == '=') ADVANCE(333);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(312);
      END_STATE();
    case 312:
      ACCEPT_TOKEN(aux_sym_condition_token_token3);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(312);
      END_STATE();
    case 313:
      ACCEPT_TOKEN(aux_sym_condition_token_token4);
      END_STATE();
    case 314:
      ACCEPT_TOKEN(aux_sym_condition_token_token5);
      END_STATE();
    case 315:
      ACCEPT_TOKEN(anon_sym_and);
      END_STATE();
    case 316:
      ACCEPT_TOKEN(anon_sym_and);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 317:
      ACCEPT_TOKEN(anon_sym_or);
      END_STATE();
    case 318:
      ACCEPT_TOKEN(anon_sym_or);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 319:
      ACCEPT_TOKEN(anon_sym_not);
      END_STATE();
    case 320:
      ACCEPT_TOKEN(anon_sym_not);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 321:
      ACCEPT_TOKEN(sym_step_text);
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(269);
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(199);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(322);
      END_STATE();
    case 322:
      ACCEPT_TOKEN(sym_step_text);
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(199);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(322);
      END_STATE();
    case 323:
      ACCEPT_TOKEN(aux_sym_returns_section_token1);
      END_STATE();
    case 324:
      ACCEPT_TOKEN(aux_sym_depends_section_token1);
      END_STATE();
    case 325:
      ACCEPT_TOKEN(aux_sym_edge_cases_section_token1);
      END_STATE();
    case 326:
      ACCEPT_TOKEN(anon_sym_ATtype);
      END_STATE();
    case 327:
      ACCEPT_TOKEN(anon_sym_LBRACE);
      END_STATE();
    case 328:
      ACCEPT_TOKEN(anon_sym_extends);
      END_STATE();
    case 329:
      ACCEPT_TOKEN(sym_type_name);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(329);
      END_STATE();
    case 330:
      ACCEPT_TOKEN(anon_sym_RBRACE);
      END_STATE();
    case 331:
      ACCEPT_TOKEN(anon_sym_ATtest);
      END_STATE();
    case 332:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      END_STATE();
    case 333:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(312);
      END_STATE();
    case 334:
      ACCEPT_TOKEN(anon_sym_ATinvariant);
      END_STATE();
    case 335:
      ACCEPT_TOKEN(anon_sym_ATproperty);
      END_STATE();
    case 336:
      ACCEPT_TOKEN(sym_expression_text);
      if (lookahead == '#') ADVANCE(208);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(336);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '}') ADVANCE(337);
      END_STATE();
    case 337:
      ACCEPT_TOKEN(sym_expression_text);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '}') ADVANCE(337);
      END_STATE();
    case 338:
      ACCEPT_TOKEN(anon_sym_ATliteral);
      END_STATE();
    case 339:
      ACCEPT_TOKEN(anon_sym_QMARK);
      END_STATE();
    case 340:
      ACCEPT_TOKEN(anon_sym_number);
      END_STATE();
    case 341:
      ACCEPT_TOKEN(anon_sym_string);
      END_STATE();
    case 342:
      ACCEPT_TOKEN(anon_sym_boolean);
      END_STATE();
    case 343:
      ACCEPT_TOKEN(anon_sym_void);
      END_STATE();
    case 344:
      ACCEPT_TOKEN(anon_sym_any);
      END_STATE();
    case 345:
      ACCEPT_TOKEN(anon_sym_list);
      END_STATE();
    case 346:
      ACCEPT_TOKEN(anon_sym_of);
      END_STATE();
    case 347:
      ACCEPT_TOKEN(anon_sym_map);
      END_STATE();
    case 348:
      ACCEPT_TOKEN(anon_sym_to);
      END_STATE();
    case 349:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(202);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(349);
      END_STATE();
    case 350:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(350);
      END_STATE();
    case 351:
      ACCEPT_TOKEN(aux_sym_quoted_string_token1);
      END_STATE();
    case 352:
      ACCEPT_TOKEN(aux_sym_quoted_string_token2);
      END_STATE();
    case 353:
      ACCEPT_TOKEN(anon_sym_true);
      END_STATE();
    case 354:
      ACCEPT_TOKEN(anon_sym_true);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 355:
      ACCEPT_TOKEN(anon_sym_false);
      END_STATE();
    case 356:
      ACCEPT_TOKEN(anon_sym_false);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 357:
      ACCEPT_TOKEN(anon_sym_True);
      END_STATE();
    case 358:
      ACCEPT_TOKEN(anon_sym_True);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 359:
      ACCEPT_TOKEN(anon_sym_False);
      END_STATE();
    case 360:
      ACCEPT_TOKEN(anon_sym_False);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(308);
      END_STATE();
    case 361:
      ACCEPT_TOKEN(anon_sym_u2022);
      END_STATE();
    case 362:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 363:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 364:
      ACCEPT_TOKEN(anon_sym_u2192);
      END_STATE();
    case 365:
      ACCEPT_TOKEN(anon_sym_DASH_GT);
      END_STATE();
    case 366:
      ACCEPT_TOKEN(sym__newline);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0, .external_lex_state = 1},
  [1] = {.lex_state = 206},
  [2] = {.lex_state = 206},
  [3] = {.lex_state = 206},
  [4] = {.lex_state = 206},
  [5] = {.lex_state = 206},
  [6] = {.lex_state = 206},
  [7] = {.lex_state = 206},
  [8] = {.lex_state = 206},
  [9] = {.lex_state = 206},
  [10] = {.lex_state = 206},
  [11] = {.lex_state = 206},
  [12] = {.lex_state = 206},
  [13] = {.lex_state = 206},
  [14] = {.lex_state = 206},
  [15] = {.lex_state = 206},
  [16] = {.lex_state = 206},
  [17] = {.lex_state = 206},
  [18] = {.lex_state = 206},
  [19] = {.lex_state = 206},
  [20] = {.lex_state = 206},
  [21] = {.lex_state = 206},
  [22] = {.lex_state = 206},
  [23] = {.lex_state = 206},
  [24] = {.lex_state = 206},
  [25] = {.lex_state = 206},
  [26] = {.lex_state = 2},
  [27] = {.lex_state = 3},
  [28] = {.lex_state = 3},
  [29] = {.lex_state = 3},
  [30] = {.lex_state = 3},
  [31] = {.lex_state = 3},
  [32] = {.lex_state = 3},
  [33] = {.lex_state = 206},
  [34] = {.lex_state = 206},
  [35] = {.lex_state = 206},
  [36] = {.lex_state = 2},
  [37] = {.lex_state = 206},
  [38] = {.lex_state = 206},
  [39] = {.lex_state = 206},
  [40] = {.lex_state = 206},
  [41] = {.lex_state = 206},
  [42] = {.lex_state = 206},
  [43] = {.lex_state = 206},
  [44] = {.lex_state = 206},
  [45] = {.lex_state = 206},
  [46] = {.lex_state = 206},
  [47] = {.lex_state = 2},
  [48] = {.lex_state = 206},
  [49] = {.lex_state = 206},
  [50] = {.lex_state = 206},
  [51] = {.lex_state = 206},
  [52] = {.lex_state = 206},
  [53] = {.lex_state = 206},
  [54] = {.lex_state = 9},
  [55] = {.lex_state = 10},
  [56] = {.lex_state = 9},
  [57] = {.lex_state = 4},
  [58] = {.lex_state = 4},
  [59] = {.lex_state = 4},
  [60] = {.lex_state = 9},
  [61] = {.lex_state = 6},
  [62] = {.lex_state = 4},
  [63] = {.lex_state = 4},
  [64] = {.lex_state = 4},
  [65] = {.lex_state = 206},
  [66] = {.lex_state = 206},
  [67] = {.lex_state = 11},
  [68] = {.lex_state = 14},
  [69] = {.lex_state = 4},
  [70] = {.lex_state = 5},
  [71] = {.lex_state = 206},
  [72] = {.lex_state = 206},
  [73] = {.lex_state = 17},
  [74] = {.lex_state = 4},
  [75] = {.lex_state = 17},
  [76] = {.lex_state = 17},
  [77] = {.lex_state = 2},
  [78] = {.lex_state = 4},
  [79] = {.lex_state = 4},
  [80] = {.lex_state = 4},
  [81] = {.lex_state = 17},
  [82] = {.lex_state = 4},
  [83] = {.lex_state = 2},
  [84] = {.lex_state = 2},
  [85] = {.lex_state = 4},
  [86] = {.lex_state = 4},
  [87] = {.lex_state = 3},
  [88] = {.lex_state = 3},
  [89] = {.lex_state = 17},
  [90] = {.lex_state = 8},
  [91] = {.lex_state = 17},
  [92] = {.lex_state = 3},
  [93] = {.lex_state = 0},
  [94] = {.lex_state = 3},
  [95] = {.lex_state = 2},
  [96] = {.lex_state = 0},
  [97] = {.lex_state = 3},
  [98] = {.lex_state = 0},
  [99] = {.lex_state = 0},
  [100] = {.lex_state = 206},
  [101] = {.lex_state = 8},
  [102] = {.lex_state = 0},
  [103] = {.lex_state = 0},
  [104] = {.lex_state = 206},
  [105] = {.lex_state = 206},
  [106] = {.lex_state = 206},
  [107] = {.lex_state = 206},
  [108] = {.lex_state = 3},
  [109] = {.lex_state = 4},
  [110] = {.lex_state = 2},
  [111] = {.lex_state = 0},
  [112] = {.lex_state = 2},
  [113] = {.lex_state = 206},
  [114] = {.lex_state = 206},
  [115] = {.lex_state = 0},
  [116] = {.lex_state = 15},
  [117] = {.lex_state = 0},
  [118] = {.lex_state = 0},
  [119] = {.lex_state = 206},
  [120] = {.lex_state = 0},
  [121] = {.lex_state = 206},
  [122] = {.lex_state = 0},
  [123] = {.lex_state = 0},
  [124] = {.lex_state = 206},
  [125] = {.lex_state = 0},
  [126] = {.lex_state = 15},
  [127] = {.lex_state = 17},
  [128] = {.lex_state = 0},
  [129] = {.lex_state = 17},
  [130] = {.lex_state = 4},
  [131] = {.lex_state = 4},
  [132] = {.lex_state = 4},
  [133] = {.lex_state = 17},
  [134] = {.lex_state = 11},
  [135] = {.lex_state = 4},
  [136] = {.lex_state = 4},
  [137] = {.lex_state = 18},
  [138] = {.lex_state = 11},
  [139] = {.lex_state = 3},
  [140] = {.lex_state = 0},
  [141] = {.lex_state = 17},
  [142] = {.lex_state = 11},
  [143] = {.lex_state = 206},
  [144] = {.lex_state = 11},
  [145] = {.lex_state = 0},
  [146] = {.lex_state = 4},
  [147] = {.lex_state = 0},
  [148] = {.lex_state = 0},
  [149] = {.lex_state = 4},
  [150] = {.lex_state = 2},
  [151] = {.lex_state = 0},
  [152] = {.lex_state = 0},
  [153] = {.lex_state = 18},
  [154] = {.lex_state = 0},
  [155] = {.lex_state = 4},
  [156] = {.lex_state = 206},
  [157] = {.lex_state = 0},
  [158] = {.lex_state = 0},
  [159] = {.lex_state = 8},
  [160] = {.lex_state = 0},
  [161] = {.lex_state = 8},
  [162] = {.lex_state = 0},
  [163] = {.lex_state = 206},
  [164] = {.lex_state = 0},
  [165] = {.lex_state = 3},
  [166] = {.lex_state = 0},
  [167] = {.lex_state = 0, .external_lex_state = 1},
  [168] = {.lex_state = 206},
  [169] = {.lex_state = 3},
  [170] = {.lex_state = 0},
  [171] = {.lex_state = 0},
  [172] = {.lex_state = 206},
  [173] = {.lex_state = 206},
  [174] = {.lex_state = 0},
  [175] = {.lex_state = 206},
  [176] = {.lex_state = 0},
  [177] = {.lex_state = 0},
  [178] = {.lex_state = 0},
  [179] = {.lex_state = 206},
  [180] = {.lex_state = 0},
  [181] = {.lex_state = 206},
  [182] = {.lex_state = 3},
  [183] = {.lex_state = 0},
  [184] = {.lex_state = 12},
  [185] = {.lex_state = 0},
  [186] = {.lex_state = 0},
  [187] = {.lex_state = 0},
  [188] = {.lex_state = 3},
  [189] = {.lex_state = 16},
  [190] = {.lex_state = 3},
  [191] = {.lex_state = 0},
  [192] = {.lex_state = 3},
  [193] = {.lex_state = 0},
  [194] = {.lex_state = 0},
  [195] = {.lex_state = 3},
  [196] = {.lex_state = 4},
  [197] = {.lex_state = 0},
  [198] = {.lex_state = 0},
  [199] = {.lex_state = 0},
  [200] = {.lex_state = 0},
  [201] = {.lex_state = 0},
  [202] = {.lex_state = 0},
  [203] = {.lex_state = 0},
  [204] = {.lex_state = 0},
  [205] = {.lex_state = 0},
  [206] = {.lex_state = 206},
  [207] = {.lex_state = 206},
  [208] = {.lex_state = 206},
  [209] = {.lex_state = 13},
  [210] = {.lex_state = 0},
  [211] = {.lex_state = 0},
  [212] = {.lex_state = 206},
  [213] = {.lex_state = 206},
  [214] = {.lex_state = 0},
  [215] = {.lex_state = 16},
  [216] = {.lex_state = 0},
  [217] = {.lex_state = 0},
  [218] = {.lex_state = 0},
  [219] = {.lex_state = 0},
  [220] = {.lex_state = 0},
  [221] = {.lex_state = 0},
  [222] = {.lex_state = 0},
  [223] = {.lex_state = 206},
  [224] = {.lex_state = 0},
  [225] = {.lex_state = 0},
  [226] = {.lex_state = 0},
  [227] = {.lex_state = 16},
  [228] = {.lex_state = 0},
  [229] = {.lex_state = 0},
  [230] = {.lex_state = 0},
  [231] = {.lex_state = 0},
  [232] = {.lex_state = 8},
  [233] = {.lex_state = 8},
  [234] = {.lex_state = 0},
  [235] = {.lex_state = 0},
  [236] = {.lex_state = 0},
  [237] = {.lex_state = 206},
  [238] = {.lex_state = 0},
  [239] = {.lex_state = 0},
  [240] = {.lex_state = 0},
  [241] = {.lex_state = 0},
  [242] = {.lex_state = 0, .external_lex_state = 1},
  [243] = {.lex_state = 0},
  [244] = {.lex_state = 0},
  [245] = {.lex_state = 18},
  [246] = {.lex_state = 4},
  [247] = {.lex_state = 0},
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
    [anon_sym_none] = ACTIONS(1),
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
    [anon_sym_ATinvariant] = ACTIONS(1),
    [anon_sym_ATproperty] = ACTIONS(1),
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
    [sym_source_file] = STATE(164),
    [sym_directive] = STATE(2),
    [sym_module_directive] = STATE(52),
    [sym_version_directive] = STATE(52),
    [sym_target_directive] = STATE(52),
    [sym_imports_directive] = STATE(52),
    [sym_anlu_block] = STATE(2),
    [sym_anlu_header] = STATE(5),
    [sym_type_block] = STATE(2),
    [sym_type_header] = STATE(57),
    [sym_test_block] = STATE(2),
    [sym_test_header] = STATE(62),
    [sym_invariant_block] = STATE(2),
    [sym_invariant_header] = STATE(81),
    [sym_property_block] = STATE(2),
    [sym_property_header] = STATE(75),
    [sym_literal_block] = STATE(2),
    [sym_literal_header] = STATE(167),
    [aux_sym_source_file_repeat1] = STATE(2),
    [ts_builtin_sym_end] = ACTIONS(5),
    [sym_comment] = ACTIONS(3),
    [anon_sym_ATmodule] = ACTIONS(7),
    [anon_sym_ATversion] = ACTIONS(9),
    [anon_sym_ATtarget] = ACTIONS(11),
    [anon_sym_ATimports] = ACTIONS(13),
    [anon_sym_LBRACK] = ACTIONS(15),
    [anon_sym_ATtype] = ACTIONS(17),
    [anon_sym_ATtest] = ACTIONS(19),
    [anon_sym_ATinvariant] = ACTIONS(21),
    [anon_sym_ATproperty] = ACTIONS(23),
    [anon_sym_ATliteral] = ACTIONS(25),
    [sym__newline] = ACTIONS(27),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 21,
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
      anon_sym_ATinvariant,
    ACTIONS(23), 1,
      anon_sym_ATproperty,
    ACTIONS(25), 1,
      anon_sym_ATliteral,
    ACTIONS(29), 1,
      ts_builtin_sym_end,
    ACTIONS(31), 1,
      sym__newline,
    STATE(5), 1,
      sym_anlu_header,
    STATE(57), 1,
      sym_type_header,
    STATE(62), 1,
      sym_test_header,
    STATE(75), 1,
      sym_property_header,
    STATE(81), 1,
      sym_invariant_header,
    STATE(167), 1,
      sym_literal_header,
    STATE(52), 4,
      sym_module_directive,
      sym_version_directive,
      sym_target_directive,
      sym_imports_directive,
    STATE(3), 8,
      sym_directive,
      sym_anlu_block,
      sym_type_block,
      sym_test_block,
      sym_invariant_block,
      sym_property_block,
      sym_literal_block,
      aux_sym_source_file_repeat1,
  [74] = 21,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(33), 1,
      ts_builtin_sym_end,
    ACTIONS(35), 1,
      anon_sym_ATmodule,
    ACTIONS(38), 1,
      anon_sym_ATversion,
    ACTIONS(41), 1,
      anon_sym_ATtarget,
    ACTIONS(44), 1,
      anon_sym_ATimports,
    ACTIONS(47), 1,
      anon_sym_LBRACK,
    ACTIONS(50), 1,
      anon_sym_ATtype,
    ACTIONS(53), 1,
      anon_sym_ATtest,
    ACTIONS(56), 1,
      anon_sym_ATinvariant,
    ACTIONS(59), 1,
      anon_sym_ATproperty,
    ACTIONS(62), 1,
      anon_sym_ATliteral,
    ACTIONS(65), 1,
      sym__newline,
    STATE(5), 1,
      sym_anlu_header,
    STATE(57), 1,
      sym_type_header,
    STATE(62), 1,
      sym_test_header,
    STATE(75), 1,
      sym_property_header,
    STATE(81), 1,
      sym_invariant_header,
    STATE(167), 1,
      sym_literal_header,
    STATE(52), 4,
      sym_module_directive,
      sym_version_directive,
      sym_target_directive,
      sym_imports_directive,
    STATE(3), 8,
      sym_directive,
      sym_anlu_block,
      sym_type_block,
      sym_test_block,
      sym_invariant_block,
      sym_property_block,
      sym_literal_block,
      aux_sym_source_file_repeat1,
  [148] = 10,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(70), 1,
      aux_sym_purpose_section_token1,
    ACTIONS(72), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(74), 1,
      aux_sym_guards_section_token1,
    ACTIONS(76), 1,
      aux_sym_logic_section_token1,
    ACTIONS(78), 1,
      aux_sym_returns_section_token1,
    ACTIONS(80), 1,
      aux_sym_depends_section_token1,
    ACTIONS(82), 1,
      aux_sym_edge_cases_section_token1,
    STATE(6), 8,
      sym_purpose_section,
      sym_inputs_section,
      sym_guards_section,
      sym_logic_section,
      sym_returns_section,
      sym_depends_section,
      sym_edge_cases_section,
      aux_sym_anlu_block_repeat1,
    ACTIONS(68), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [197] = 10,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(70), 1,
      aux_sym_purpose_section_token1,
    ACTIONS(72), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(74), 1,
      aux_sym_guards_section_token1,
    ACTIONS(76), 1,
      aux_sym_logic_section_token1,
    ACTIONS(78), 1,
      aux_sym_returns_section_token1,
    ACTIONS(80), 1,
      aux_sym_depends_section_token1,
    ACTIONS(82), 1,
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
    ACTIONS(84), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [246] = 10,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(88), 1,
      aux_sym_purpose_section_token1,
    ACTIONS(91), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(94), 1,
      aux_sym_guards_section_token1,
    ACTIONS(97), 1,
      aux_sym_logic_section_token1,
    ACTIONS(100), 1,
      aux_sym_returns_section_token1,
    ACTIONS(103), 1,
      aux_sym_depends_section_token1,
    ACTIONS(106), 1,
      aux_sym_edge_cases_section_token1,
    STATE(6), 8,
      sym_purpose_section,
      sym_inputs_section,
      sym_guards_section,
      sym_logic_section,
      sym_returns_section,
      sym_depends_section,
      sym_edge_cases_section,
      aux_sym_anlu_block_repeat1,
    ACTIONS(86), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [295] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(153), 1,
      sym_bullet,
    STATE(11), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(109), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [332] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(136), 1,
      sym_bullet,
    STATE(10), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(115), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(113), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [369] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(137), 1,
      sym_bullet,
    STATE(12), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(117), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [406] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(136), 1,
      sym_bullet,
    STATE(10), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(121), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(119), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [443] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(153), 1,
      sym_bullet,
    STATE(11), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
    ACTIONS(126), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(124), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [480] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(137), 1,
      sym_bullet,
    STATE(12), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(131), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(129), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [517] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(134), 22,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [545] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(138), 1,
      sym_step_number,
    STATE(15), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
    ACTIONS(136), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [577] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(142), 1,
      sym_step_number,
    STATE(15), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
    ACTIONS(140), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [609] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(145), 22,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [637] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(147), 22,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [665] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(149), 22,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [693] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(151), 22,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
      sym__newline,
  [721] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(155), 1,
      sym_step_number,
    ACTIONS(153), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [749] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(113), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [774] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(157), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [799] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(159), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [824] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(161), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [849] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(163), 19,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [874] = 9,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(165), 1,
      anon_sym_RPAREN,
    ACTIONS(167), 1,
      aux_sym_condition_token_token1,
    ACTIONS(169), 1,
      sym_number,
    STATE(107), 1,
      sym_test_value,
    STATE(223), 1,
      sym_test_args,
    ACTIONS(171), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(104), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(173), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [908] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(175), 1,
      sym_type_name,
    ACTIONS(179), 1,
      anon_sym_list,
    ACTIONS(181), 1,
      anon_sym_map,
    STATE(93), 1,
      sym_type_spec,
    ACTIONS(177), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(103), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [938] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(175), 1,
      sym_type_name,
    ACTIONS(179), 1,
      anon_sym_list,
    ACTIONS(181), 1,
      anon_sym_map,
    STATE(96), 1,
      sym_type_spec,
    ACTIONS(177), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(103), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [968] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(175), 1,
      sym_type_name,
    ACTIONS(179), 1,
      anon_sym_list,
    ACTIONS(181), 1,
      anon_sym_map,
    STATE(98), 1,
      sym_type_spec,
    ACTIONS(177), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(103), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [998] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(175), 1,
      sym_type_name,
    ACTIONS(179), 1,
      anon_sym_list,
    ACTIONS(181), 1,
      anon_sym_map,
    ACTIONS(177), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(192), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [1025] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(175), 1,
      sym_type_name,
    ACTIONS(179), 1,
      anon_sym_list,
    ACTIONS(181), 1,
      anon_sym_map,
    ACTIONS(177), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(88), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [1052] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(175), 1,
      sym_type_name,
    ACTIONS(179), 1,
      anon_sym_list,
    ACTIONS(181), 1,
      anon_sym_map,
    ACTIONS(177), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(97), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [1079] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(183), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1097] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(185), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1115] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(187), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1133] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(167), 1,
      aux_sym_condition_token_token1,
    ACTIONS(169), 1,
      sym_number,
    STATE(201), 1,
      sym_test_value,
    ACTIONS(171), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(104), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(173), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [1161] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(189), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1179] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(191), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1197] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(193), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1215] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(195), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1233] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(197), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1251] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(199), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1269] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(201), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1287] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(203), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1305] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(205), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1323] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(207), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1341] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(167), 1,
      aux_sym_condition_token_token1,
    ACTIONS(169), 1,
      sym_number,
    STATE(143), 1,
      sym_test_value,
    ACTIONS(171), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(104), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(173), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [1369] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(209), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1387] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(211), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1405] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(213), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1423] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(215), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1441] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(217), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1459] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(219), 12,
      ts_builtin_sym_end,
      anon_sym_ATmodule,
      anon_sym_ATversion,
      anon_sym_ATtarget,
      anon_sym_ATimports,
      anon_sym_LBRACK,
      anon_sym_ATtype,
      anon_sym_ATtest,
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [1477] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(221), 1,
      aux_sym_condition_prefix_token2,
    STATE(54), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(223), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(226), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1500] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(209), 1,
      sym_condition_text,
    STATE(56), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(229), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(231), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1523] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_prefix_token2,
    STATE(54), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(229), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(231), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1546] = 8,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    ACTIONS(237), 1,
      anon_sym_RBRACE,
    STATE(44), 1,
      sym_type_close,
    STATE(149), 1,
      sym_bullet,
    STATE(160), 1,
      sym_identifier,
    STATE(58), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(115), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1574] = 8,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    ACTIONS(237), 1,
      anon_sym_RBRACE,
    STATE(34), 1,
      sym_type_close,
    STATE(149), 1,
      sym_bullet,
    STATE(160), 1,
      sym_identifier,
    STATE(59), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(115), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1602] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(239), 1,
      aux_sym_condition_token_token1,
    ACTIONS(242), 1,
      anon_sym_RBRACE,
    STATE(149), 1,
      sym_bullet,
    STATE(160), 1,
      sym_identifier,
    STATE(59), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(244), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1627] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(249), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
    ACTIONS(247), 5,
      aux_sym_condition_prefix_token2,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
  [1644] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(167), 1,
      aux_sym_condition_token_token1,
    STATE(117), 1,
      sym_identifier,
    ACTIONS(171), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    ACTIONS(251), 2,
      anon_sym_required,
      anon_sym_optional,
    STATE(140), 2,
      sym_constraint_pair,
      sym_quoted_string,
  [1666] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    ACTIONS(253), 1,
      anon_sym_RBRACE,
    STATE(45), 1,
      sym_test_close,
    STATE(172), 1,
      sym_test_call,
    STATE(181), 1,
      sym_identifier,
    STATE(64), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1689] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    ACTIONS(255), 1,
      anon_sym_RPAREN,
    STATE(237), 1,
      sym_error_args,
    ACTIONS(171), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(124), 2,
      sym_quoted_string,
      sym_identifier,
  [1710] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    ACTIONS(253), 1,
      anon_sym_RBRACE,
    STATE(38), 1,
      sym_test_close,
    STATE(172), 1,
      sym_test_call,
    STATE(181), 1,
      sym_identifier,
    STATE(69), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1733] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(257), 6,
      anon_sym_COMMA,
      anon_sym_COLON,
      anon_sym_LPAREN,
      anon_sym_RPAREN,
      anon_sym_LBRACE,
      sym__newline,
  [1745] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(136), 1,
      sym_bullet,
    STATE(8), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(115), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1761] = 7,
    ACTIONS(167), 1,
      aux_sym_condition_token_token1,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(261), 1,
      aux_sym_description_text_token1,
    STATE(203), 1,
      sym_error_spec,
    STATE(204), 1,
      sym_error_call,
    STATE(206), 1,
      sym_identifier,
    STATE(247), 1,
      sym_error_text,
  [1783] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(263), 1,
      anon_sym_LBRACK,
    ACTIONS(265), 1,
      aux_sym_condition_prefix_token1,
    ACTIONS(267), 1,
      sym_step_text,
    STATE(116), 1,
      sym_state_prefix,
    STATE(187), 1,
      sym_logic_step,
    STATE(189), 1,
      sym_condition_prefix,
  [1805] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(269), 1,
      aux_sym_condition_token_token1,
    ACTIONS(272), 1,
      anon_sym_RBRACE,
    STATE(172), 1,
      sym_test_call,
    STATE(181), 1,
      sym_identifier,
    STATE(69), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1825] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    ACTIONS(274), 1,
      sym_number,
    ACTIONS(171), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(151), 2,
      sym_quoted_string,
      sym_identifier,
  [1843] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(137), 1,
      sym_bullet,
    STATE(9), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1859] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(153), 1,
      sym_bullet,
    STATE(7), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1875] = 5,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(276), 1,
      anon_sym_RBRACE,
    ACTIONS(278), 1,
      sym_expression_text,
    STATE(40), 1,
      sym_invariant_close,
    STATE(89), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [1892] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(280), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1903] = 5,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(282), 1,
      anon_sym_RBRACE,
    ACTIONS(284), 1,
      sym_expression_text,
    STATE(48), 1,
      sym_property_close,
    STATE(76), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [1920] = 5,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(282), 1,
      anon_sym_RBRACE,
    ACTIONS(284), 1,
      sym_expression_text,
    STATE(42), 1,
      sym_property_close,
    STATE(91), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [1937] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(288), 1,
      sym__newline,
    STATE(146), 1,
      sym_arrow,
    STATE(211), 1,
      sym_output_binding,
    ACTIONS(286), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1954] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(290), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1965] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(292), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1976] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(294), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1987] = 5,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(276), 1,
      anon_sym_RBRACE,
    ACTIONS(278), 1,
      sym_expression_text,
    STATE(49), 1,
      sym_invariant_close,
    STATE(73), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [2004] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(296), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [2015] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(298), 1,
      sym__newline,
    STATE(146), 1,
      sym_arrow,
    STATE(230), 1,
      sym_output_binding,
    ACTIONS(286), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2032] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(300), 1,
      sym__newline,
    STATE(146), 1,
      sym_arrow,
    STATE(239), 1,
      sym_output_binding,
    ACTIONS(286), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2049] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(302), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [2060] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    ACTIONS(171), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(156), 2,
      sym_quoted_string,
      sym_identifier,
  [2075] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(304), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2085] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(306), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2095] = 4,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(308), 1,
      anon_sym_RBRACE,
    ACTIONS(310), 1,
      sym_expression_text,
    STATE(89), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [2109] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(313), 1,
      anon_sym_LBRACK,
    ACTIONS(315), 1,
      sym_anlu_identifier,
    STATE(125), 1,
      sym_anlu_reference,
    STATE(157), 1,
      sym_depends_list,
  [2125] = 4,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(317), 1,
      anon_sym_RBRACE,
    ACTIONS(319), 1,
      sym_expression_text,
    STATE(91), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [2139] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(322), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2149] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(324), 1,
      anon_sym_COMMA,
    ACTIONS(326), 1,
      sym__newline,
    STATE(99), 1,
      aux_sym_input_constraints_repeat1,
    STATE(170), 1,
      sym_field_constraints,
  [2165] = 3,
    ACTIONS(3), 1,
      sym_comment,
    STATE(224), 1,
      sym_target_name,
    ACTIONS(328), 3,
      anon_sym_python,
      anon_sym_typescript,
      anon_sym_rust,
  [2177] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(332), 1,
      sym__newline,
    STATE(67), 1,
      sym_arrow,
    ACTIONS(330), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2191] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(324), 1,
      anon_sym_COMMA,
    ACTIONS(334), 1,
      sym__newline,
    STATE(99), 1,
      aux_sym_input_constraints_repeat1,
    STATE(198), 1,
      sym_field_constraints,
  [2207] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(336), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2217] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(324), 1,
      anon_sym_COMMA,
    ACTIONS(338), 1,
      sym__newline,
    STATE(120), 1,
      aux_sym_input_constraints_repeat1,
    STATE(222), 1,
      sym_input_constraints,
  [2233] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(324), 1,
      anon_sym_COMMA,
    ACTIONS(340), 1,
      sym__newline,
    STATE(118), 1,
      aux_sym_input_constraints_repeat1,
  [2246] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(342), 1,
      anon_sym_COMMA,
    ACTIONS(344), 1,
      anon_sym_RPAREN,
    STATE(113), 1,
      aux_sym_error_args_repeat1,
  [2259] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(313), 1,
      anon_sym_LBRACK,
    ACTIONS(315), 1,
      sym_anlu_identifier,
    STATE(148), 1,
      sym_anlu_reference,
  [2272] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(346), 1,
      anon_sym_COMMA,
    ACTIONS(348), 1,
      sym__newline,
    STATE(111), 1,
      aux_sym_depends_list_repeat1,
  [2285] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(352), 1,
      anon_sym_QMARK,
    ACTIONS(350), 2,
      anon_sym_COMMA,
      sym__newline,
  [2296] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(354), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2305] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(356), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2314] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(358), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2323] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(360), 1,
      anon_sym_COMMA,
    ACTIONS(362), 1,
      anon_sym_RPAREN,
    STATE(114), 1,
      aux_sym_test_args_repeat1,
  [2336] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(364), 1,
      anon_sym_LBRACE,
    ACTIONS(366), 1,
      anon_sym_extends,
    STATE(197), 1,
      sym_extends_clause,
  [2349] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    STATE(122), 1,
      sym_identifier,
    STATE(205), 1,
      sym_import_list,
  [2362] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(368), 3,
      anon_sym_u2192,
      anon_sym_DASH_GT,
      sym__newline,
  [2371] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(370), 1,
      anon_sym_COMMA,
    ACTIONS(373), 1,
      sym__newline,
    STATE(111), 1,
      aux_sym_depends_list_repeat1,
  [2384] = 3,
    ACTIONS(3), 1,
      sym_comment,
    STATE(138), 1,
      sym_arrow,
    ACTIONS(330), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2395] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(375), 1,
      anon_sym_COMMA,
    ACTIONS(378), 1,
      anon_sym_RPAREN,
    STATE(113), 1,
      aux_sym_error_args_repeat1,
  [2408] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(360), 1,
      anon_sym_COMMA,
    ACTIONS(380), 1,
      anon_sym_RPAREN,
    STATE(119), 1,
      aux_sym_test_args_repeat1,
  [2421] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(382), 1,
      anon_sym_COMMA,
    ACTIONS(384), 1,
      sym__newline,
    STATE(123), 1,
      aux_sym_import_list_repeat1,
  [2434] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(265), 1,
      aux_sym_condition_prefix_token1,
    ACTIONS(386), 1,
      sym_step_text,
    STATE(215), 1,
      sym_condition_prefix,
  [2447] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(390), 1,
      anon_sym_COLON,
    ACTIONS(388), 2,
      anon_sym_COMMA,
      sym__newline,
  [2458] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(388), 1,
      sym__newline,
    ACTIONS(392), 1,
      anon_sym_COMMA,
    STATE(118), 1,
      aux_sym_input_constraints_repeat1,
  [2471] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(395), 1,
      anon_sym_COMMA,
    ACTIONS(398), 1,
      anon_sym_RPAREN,
    STATE(119), 1,
      aux_sym_test_args_repeat1,
  [2484] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(324), 1,
      anon_sym_COMMA,
    ACTIONS(400), 1,
      sym__newline,
    STATE(118), 1,
      aux_sym_input_constraints_repeat1,
  [2497] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(402), 1,
      sym_step_number,
    STATE(14), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
  [2508] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(382), 1,
      anon_sym_COMMA,
    ACTIONS(404), 1,
      sym__newline,
    STATE(115), 1,
      aux_sym_import_list_repeat1,
  [2521] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(406), 1,
      anon_sym_COMMA,
    ACTIONS(409), 1,
      sym__newline,
    STATE(123), 1,
      aux_sym_import_list_repeat1,
  [2534] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(342), 1,
      anon_sym_COMMA,
    ACTIONS(411), 1,
      anon_sym_RPAREN,
    STATE(100), 1,
      aux_sym_error_args_repeat1,
  [2547] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(346), 1,
      anon_sym_COMMA,
    ACTIONS(413), 1,
      sym__newline,
    STATE(102), 1,
      aux_sym_depends_list_repeat1,
  [2560] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(415), 2,
      aux_sym_condition_prefix_token1,
      sym_step_text,
  [2568] = 2,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(417), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2576] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(419), 2,
      anon_sym_COMMA,
      sym__newline,
  [2584] = 2,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(421), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2592] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(423), 2,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
  [2600] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    STATE(162), 1,
      sym_identifier,
  [2610] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(425), 2,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
  [2618] = 2,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(427), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2626] = 2,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(429), 2,
      aux_sym_description_text_token1,
      aux_sym_condition_token_token1,
  [2634] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    STATE(145), 1,
      sym_identifier,
  [2644] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    STATE(238), 1,
      sym_identifier,
  [2654] = 3,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(431), 1,
      aux_sym_guard_text_token1,
    STATE(112), 1,
      sym_edge_condition_text,
  [2664] = 3,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(433), 1,
      aux_sym_description_text_token1,
    STATE(217), 1,
      sym_edge_behavior_text,
  [2674] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(435), 1,
      anon_sym_none,
    ACTIONS(437), 1,
      sym__newline,
  [2684] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(388), 2,
      anon_sym_COMMA,
      sym__newline,
  [2692] = 2,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(439), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2700] = 3,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(441), 1,
      aux_sym_description_text_token1,
    STATE(231), 1,
      sym_returns_text,
  [2710] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(398), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [2718] = 3,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(443), 1,
      aux_sym_description_text_token1,
    STATE(219), 1,
      sym_description_text,
  [2728] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(409), 2,
      anon_sym_COMMA,
      sym__newline,
  [2736] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    STATE(229), 1,
      sym_identifier,
  [2746] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(445), 2,
      anon_sym_COMMA,
      sym__newline,
  [2754] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(373), 2,
      anon_sym_COMMA,
      sym__newline,
  [2762] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    STATE(177), 1,
      sym_identifier,
  [2772] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(447), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2780] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(449), 2,
      anon_sym_COMMA,
      sym__newline,
  [2788] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(451), 2,
      anon_sym_COMMA,
      sym__newline,
  [2796] = 3,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(453), 1,
      aux_sym_guard_text_token1,
    STATE(95), 1,
      sym_guard_text,
  [2806] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(455), 1,
      anon_sym_RBRACE,
    STATE(43), 1,
      sym_literal_close,
  [2816] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(235), 1,
      aux_sym_condition_token_token1,
    STATE(176), 1,
      sym_identifier,
  [2826] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(378), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [2834] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(457), 1,
      sym__newline,
  [2841] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(459), 1,
      sym__newline,
  [2848] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(461), 1,
      sym_anlu_identifier,
  [2855] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(463), 1,
      anon_sym_COLON,
  [2862] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(465), 1,
      sym_anlu_identifier,
  [2869] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(467), 1,
      anon_sym_LBRACE,
  [2876] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(469), 1,
      anon_sym_RBRACK,
  [2883] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(471), 1,
      ts_builtin_sym_end,
  [2890] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(473), 1,
      sym_type_name,
  [2897] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(475), 1,
      anon_sym_DOT,
  [2904] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(477), 1,
      sym_literal_content,
  [2911] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(479), 1,
      anon_sym_LBRACK,
  [2918] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(481), 1,
      sym_type_name,
  [2925] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(483), 1,
      sym__newline,
  [2932] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(485), 1,
      sym__newline,
  [2939] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(487), 1,
      anon_sym_EQ_EQ,
  [2946] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(489), 1,
      anon_sym_RBRACK,
  [2953] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(491), 1,
      sym__newline,
  [2960] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(493), 1,
      anon_sym_EQ_EQ,
  [2967] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(495), 1,
      sym__newline,
  [2974] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(497), 1,
      anon_sym_COLON,
  [2981] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(499), 1,
      sym__newline,
  [2988] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(501), 1,
      anon_sym_LBRACK,
  [2995] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(503), 1,
      sym__newline,
  [3002] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(505), 1,
      anon_sym_LPAREN,
  [3009] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(507), 1,
      sym_version_string,
  [3016] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(509), 1,
      sym__newline,
  [3023] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(511), 1,
      sym_state_name,
  [3030] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(513), 1,
      sym__newline,
  [3037] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(515), 1,
      sym__newline,
  [3044] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(517), 1,
      sym__newline,
  [3051] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(519), 1,
      anon_sym_of,
  [3058] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(386), 1,
      sym_step_text,
  [3065] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(521), 1,
      anon_sym_of,
  [3072] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(523), 1,
      sym__newline,
  [3079] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(525), 1,
      anon_sym_to,
  [3086] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(527), 1,
      sym__newline,
  [3093] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(529), 1,
      sym__newline,
  [3100] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(531), 1,
      sym_type_name,
  [3107] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(533), 1,
      aux_sym_condition_token_token1,
  [3114] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(535), 1,
      anon_sym_LBRACE,
  [3121] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(537), 1,
      sym__newline,
  [3128] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(539), 1,
      anon_sym_LBRACE,
  [3135] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(541), 1,
      sym__newline,
  [3142] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(543), 1,
      sym__newline,
  [3149] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(545), 1,
      sym__newline,
  [3156] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(547), 1,
      sym__newline,
  [3163] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(549), 1,
      sym__newline,
  [3170] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(551), 1,
      sym__newline,
  [3177] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(553), 1,
      anon_sym_LPAREN,
  [3184] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(555), 1,
      anon_sym_RBRACK,
  [3191] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(557), 1,
      anon_sym_RBRACK,
  [3198] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(559), 1,
      aux_sym_condition_prefix_token2,
  [3205] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(561), 1,
      sym__newline,
  [3212] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(563), 1,
      sym__newline,
  [3219] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(565), 1,
      anon_sym_EQ_EQ,
  [3226] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(567), 1,
      anon_sym_RBRACK,
  [3233] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(569), 1,
      sym__newline,
  [3240] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(571), 1,
      sym_step_text,
  [3247] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(573), 1,
      sym__newline,
  [3254] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(575), 1,
      sym__newline,
  [3261] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(577), 1,
      sym__newline,
  [3268] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(579), 1,
      sym__newline,
  [3275] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(581), 1,
      sym__newline,
  [3282] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(583), 1,
      sym__newline,
  [3289] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(585), 1,
      sym__newline,
  [3296] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(587), 1,
      anon_sym_RPAREN,
  [3303] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(589), 1,
      sym__newline,
  [3310] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(591), 1,
      anon_sym_LBRACE,
  [3317] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(593), 1,
      sym__newline,
  [3324] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(595), 1,
      sym_step_text,
  [3331] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(597), 1,
      sym__newline,
  [3338] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(599), 1,
      sym__newline,
  [3345] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(601), 1,
      sym__newline,
  [3352] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(603), 1,
      sym__newline,
  [3359] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(605), 1,
      sym_anlu_identifier,
  [3366] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(607), 1,
      sym_anlu_identifier,
  [3373] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(609), 1,
      sym__newline,
  [3380] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(611), 1,
      sym__newline,
  [3387] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(613), 1,
      sym__newline,
  [3394] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(615), 1,
      anon_sym_RPAREN,
  [3401] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(617), 1,
      anon_sym_COLON,
  [3408] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(619), 1,
      sym__newline,
  [3415] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(621), 1,
      sym__newline,
  [3422] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(623), 1,
      anon_sym_LBRACE,
  [3429] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(625), 1,
      sym_literal_content,
  [3436] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(627), 1,
      anon_sym_LBRACE,
  [3443] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(629), 1,
      sym__newline,
  [3450] = 2,
    ACTIONS(259), 1,
      sym_comment,
    ACTIONS(631), 1,
      aux_sym_guard_text_token1,
  [3457] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(633), 1,
      aux_sym_condition_token_token1,
  [3464] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(635), 1,
      sym__newline,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(2)] = 0,
  [SMALL_STATE(3)] = 74,
  [SMALL_STATE(4)] = 148,
  [SMALL_STATE(5)] = 197,
  [SMALL_STATE(6)] = 246,
  [SMALL_STATE(7)] = 295,
  [SMALL_STATE(8)] = 332,
  [SMALL_STATE(9)] = 369,
  [SMALL_STATE(10)] = 406,
  [SMALL_STATE(11)] = 443,
  [SMALL_STATE(12)] = 480,
  [SMALL_STATE(13)] = 517,
  [SMALL_STATE(14)] = 545,
  [SMALL_STATE(15)] = 577,
  [SMALL_STATE(16)] = 609,
  [SMALL_STATE(17)] = 637,
  [SMALL_STATE(18)] = 665,
  [SMALL_STATE(19)] = 693,
  [SMALL_STATE(20)] = 721,
  [SMALL_STATE(21)] = 749,
  [SMALL_STATE(22)] = 774,
  [SMALL_STATE(23)] = 799,
  [SMALL_STATE(24)] = 824,
  [SMALL_STATE(25)] = 849,
  [SMALL_STATE(26)] = 874,
  [SMALL_STATE(27)] = 908,
  [SMALL_STATE(28)] = 938,
  [SMALL_STATE(29)] = 968,
  [SMALL_STATE(30)] = 998,
  [SMALL_STATE(31)] = 1025,
  [SMALL_STATE(32)] = 1052,
  [SMALL_STATE(33)] = 1079,
  [SMALL_STATE(34)] = 1097,
  [SMALL_STATE(35)] = 1115,
  [SMALL_STATE(36)] = 1133,
  [SMALL_STATE(37)] = 1161,
  [SMALL_STATE(38)] = 1179,
  [SMALL_STATE(39)] = 1197,
  [SMALL_STATE(40)] = 1215,
  [SMALL_STATE(41)] = 1233,
  [SMALL_STATE(42)] = 1251,
  [SMALL_STATE(43)] = 1269,
  [SMALL_STATE(44)] = 1287,
  [SMALL_STATE(45)] = 1305,
  [SMALL_STATE(46)] = 1323,
  [SMALL_STATE(47)] = 1341,
  [SMALL_STATE(48)] = 1369,
  [SMALL_STATE(49)] = 1387,
  [SMALL_STATE(50)] = 1405,
  [SMALL_STATE(51)] = 1423,
  [SMALL_STATE(52)] = 1441,
  [SMALL_STATE(53)] = 1459,
  [SMALL_STATE(54)] = 1477,
  [SMALL_STATE(55)] = 1500,
  [SMALL_STATE(56)] = 1523,
  [SMALL_STATE(57)] = 1546,
  [SMALL_STATE(58)] = 1574,
  [SMALL_STATE(59)] = 1602,
  [SMALL_STATE(60)] = 1627,
  [SMALL_STATE(61)] = 1644,
  [SMALL_STATE(62)] = 1666,
  [SMALL_STATE(63)] = 1689,
  [SMALL_STATE(64)] = 1710,
  [SMALL_STATE(65)] = 1733,
  [SMALL_STATE(66)] = 1745,
  [SMALL_STATE(67)] = 1761,
  [SMALL_STATE(68)] = 1783,
  [SMALL_STATE(69)] = 1805,
  [SMALL_STATE(70)] = 1825,
  [SMALL_STATE(71)] = 1843,
  [SMALL_STATE(72)] = 1859,
  [SMALL_STATE(73)] = 1875,
  [SMALL_STATE(74)] = 1892,
  [SMALL_STATE(75)] = 1903,
  [SMALL_STATE(76)] = 1920,
  [SMALL_STATE(77)] = 1937,
  [SMALL_STATE(78)] = 1954,
  [SMALL_STATE(79)] = 1965,
  [SMALL_STATE(80)] = 1976,
  [SMALL_STATE(81)] = 1987,
  [SMALL_STATE(82)] = 2004,
  [SMALL_STATE(83)] = 2015,
  [SMALL_STATE(84)] = 2032,
  [SMALL_STATE(85)] = 2049,
  [SMALL_STATE(86)] = 2060,
  [SMALL_STATE(87)] = 2075,
  [SMALL_STATE(88)] = 2085,
  [SMALL_STATE(89)] = 2095,
  [SMALL_STATE(90)] = 2109,
  [SMALL_STATE(91)] = 2125,
  [SMALL_STATE(92)] = 2139,
  [SMALL_STATE(93)] = 2149,
  [SMALL_STATE(94)] = 2165,
  [SMALL_STATE(95)] = 2177,
  [SMALL_STATE(96)] = 2191,
  [SMALL_STATE(97)] = 2207,
  [SMALL_STATE(98)] = 2217,
  [SMALL_STATE(99)] = 2233,
  [SMALL_STATE(100)] = 2246,
  [SMALL_STATE(101)] = 2259,
  [SMALL_STATE(102)] = 2272,
  [SMALL_STATE(103)] = 2285,
  [SMALL_STATE(104)] = 2296,
  [SMALL_STATE(105)] = 2305,
  [SMALL_STATE(106)] = 2314,
  [SMALL_STATE(107)] = 2323,
  [SMALL_STATE(108)] = 2336,
  [SMALL_STATE(109)] = 2349,
  [SMALL_STATE(110)] = 2362,
  [SMALL_STATE(111)] = 2371,
  [SMALL_STATE(112)] = 2384,
  [SMALL_STATE(113)] = 2395,
  [SMALL_STATE(114)] = 2408,
  [SMALL_STATE(115)] = 2421,
  [SMALL_STATE(116)] = 2434,
  [SMALL_STATE(117)] = 2447,
  [SMALL_STATE(118)] = 2458,
  [SMALL_STATE(119)] = 2471,
  [SMALL_STATE(120)] = 2484,
  [SMALL_STATE(121)] = 2497,
  [SMALL_STATE(122)] = 2508,
  [SMALL_STATE(123)] = 2521,
  [SMALL_STATE(124)] = 2534,
  [SMALL_STATE(125)] = 2547,
  [SMALL_STATE(126)] = 2560,
  [SMALL_STATE(127)] = 2568,
  [SMALL_STATE(128)] = 2576,
  [SMALL_STATE(129)] = 2584,
  [SMALL_STATE(130)] = 2592,
  [SMALL_STATE(131)] = 2600,
  [SMALL_STATE(132)] = 2610,
  [SMALL_STATE(133)] = 2618,
  [SMALL_STATE(134)] = 2626,
  [SMALL_STATE(135)] = 2634,
  [SMALL_STATE(136)] = 2644,
  [SMALL_STATE(137)] = 2654,
  [SMALL_STATE(138)] = 2664,
  [SMALL_STATE(139)] = 2674,
  [SMALL_STATE(140)] = 2684,
  [SMALL_STATE(141)] = 2692,
  [SMALL_STATE(142)] = 2700,
  [SMALL_STATE(143)] = 2710,
  [SMALL_STATE(144)] = 2718,
  [SMALL_STATE(145)] = 2728,
  [SMALL_STATE(146)] = 2736,
  [SMALL_STATE(147)] = 2746,
  [SMALL_STATE(148)] = 2754,
  [SMALL_STATE(149)] = 2762,
  [SMALL_STATE(150)] = 2772,
  [SMALL_STATE(151)] = 2780,
  [SMALL_STATE(152)] = 2788,
  [SMALL_STATE(153)] = 2796,
  [SMALL_STATE(154)] = 2806,
  [SMALL_STATE(155)] = 2816,
  [SMALL_STATE(156)] = 2826,
  [SMALL_STATE(157)] = 2834,
  [SMALL_STATE(158)] = 2841,
  [SMALL_STATE(159)] = 2848,
  [SMALL_STATE(160)] = 2855,
  [SMALL_STATE(161)] = 2862,
  [SMALL_STATE(162)] = 2869,
  [SMALL_STATE(163)] = 2876,
  [SMALL_STATE(164)] = 2883,
  [SMALL_STATE(165)] = 2890,
  [SMALL_STATE(166)] = 2897,
  [SMALL_STATE(167)] = 2904,
  [SMALL_STATE(168)] = 2911,
  [SMALL_STATE(169)] = 2918,
  [SMALL_STATE(170)] = 2925,
  [SMALL_STATE(171)] = 2932,
  [SMALL_STATE(172)] = 2939,
  [SMALL_STATE(173)] = 2946,
  [SMALL_STATE(174)] = 2953,
  [SMALL_STATE(175)] = 2960,
  [SMALL_STATE(176)] = 2967,
  [SMALL_STATE(177)] = 2974,
  [SMALL_STATE(178)] = 2981,
  [SMALL_STATE(179)] = 2988,
  [SMALL_STATE(180)] = 2995,
  [SMALL_STATE(181)] = 3002,
  [SMALL_STATE(182)] = 3009,
  [SMALL_STATE(183)] = 3016,
  [SMALL_STATE(184)] = 3023,
  [SMALL_STATE(185)] = 3030,
  [SMALL_STATE(186)] = 3037,
  [SMALL_STATE(187)] = 3044,
  [SMALL_STATE(188)] = 3051,
  [SMALL_STATE(189)] = 3058,
  [SMALL_STATE(190)] = 3065,
  [SMALL_STATE(191)] = 3072,
  [SMALL_STATE(192)] = 3079,
  [SMALL_STATE(193)] = 3086,
  [SMALL_STATE(194)] = 3093,
  [SMALL_STATE(195)] = 3100,
  [SMALL_STATE(196)] = 3107,
  [SMALL_STATE(197)] = 3114,
  [SMALL_STATE(198)] = 3121,
  [SMALL_STATE(199)] = 3128,
  [SMALL_STATE(200)] = 3135,
  [SMALL_STATE(201)] = 3142,
  [SMALL_STATE(202)] = 3149,
  [SMALL_STATE(203)] = 3156,
  [SMALL_STATE(204)] = 3163,
  [SMALL_STATE(205)] = 3170,
  [SMALL_STATE(206)] = 3177,
  [SMALL_STATE(207)] = 3184,
  [SMALL_STATE(208)] = 3191,
  [SMALL_STATE(209)] = 3198,
  [SMALL_STATE(210)] = 3205,
  [SMALL_STATE(211)] = 3212,
  [SMALL_STATE(212)] = 3219,
  [SMALL_STATE(213)] = 3226,
  [SMALL_STATE(214)] = 3233,
  [SMALL_STATE(215)] = 3240,
  [SMALL_STATE(216)] = 3247,
  [SMALL_STATE(217)] = 3254,
  [SMALL_STATE(218)] = 3261,
  [SMALL_STATE(219)] = 3268,
  [SMALL_STATE(220)] = 3275,
  [SMALL_STATE(221)] = 3282,
  [SMALL_STATE(222)] = 3289,
  [SMALL_STATE(223)] = 3296,
  [SMALL_STATE(224)] = 3303,
  [SMALL_STATE(225)] = 3310,
  [SMALL_STATE(226)] = 3317,
  [SMALL_STATE(227)] = 3324,
  [SMALL_STATE(228)] = 3331,
  [SMALL_STATE(229)] = 3338,
  [SMALL_STATE(230)] = 3345,
  [SMALL_STATE(231)] = 3352,
  [SMALL_STATE(232)] = 3359,
  [SMALL_STATE(233)] = 3366,
  [SMALL_STATE(234)] = 3373,
  [SMALL_STATE(235)] = 3380,
  [SMALL_STATE(236)] = 3387,
  [SMALL_STATE(237)] = 3394,
  [SMALL_STATE(238)] = 3401,
  [SMALL_STATE(239)] = 3408,
  [SMALL_STATE(240)] = 3415,
  [SMALL_STATE(241)] = 3422,
  [SMALL_STATE(242)] = 3429,
  [SMALL_STATE(243)] = 3436,
  [SMALL_STATE(244)] = 3443,
  [SMALL_STATE(245)] = 3450,
  [SMALL_STATE(246)] = 3457,
  [SMALL_STATE(247)] = 3464,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT_EXTRA(),
  [5] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0, 0, 0),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(155),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(182),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(94),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(109),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(159),
  [17] = {.entry = {.count = 1, .reusable = true}}, SHIFT(165),
  [19] = {.entry = {.count = 1, .reusable = true}}, SHIFT(168),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(169),
  [23] = {.entry = {.count = 1, .reusable = true}}, SHIFT(179),
  [25] = {.entry = {.count = 1, .reusable = true}}, SHIFT(131),
  [27] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [29] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1, 0, 0),
  [31] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [33] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0),
  [35] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(155),
  [38] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(182),
  [41] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(94),
  [44] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(109),
  [47] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(159),
  [50] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(165),
  [53] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(168),
  [56] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(169),
  [59] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(179),
  [62] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(131),
  [65] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(3),
  [68] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_block, 2, 0, 0),
  [70] = {.entry = {.count = 1, .reusable = true}}, SHIFT(144),
  [72] = {.entry = {.count = 1, .reusable = true}}, SHIFT(139),
  [74] = {.entry = {.count = 1, .reusable = true}}, SHIFT(183),
  [76] = {.entry = {.count = 1, .reusable = true}}, SHIFT(191),
  [78] = {.entry = {.count = 1, .reusable = true}}, SHIFT(142),
  [80] = {.entry = {.count = 1, .reusable = true}}, SHIFT(90),
  [82] = {.entry = {.count = 1, .reusable = true}}, SHIFT(174),
  [84] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_block, 1, 0, 0),
  [86] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0),
  [88] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(144),
  [91] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(139),
  [94] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(183),
  [97] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(191),
  [100] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(142),
  [103] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(90),
  [106] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(174),
  [109] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guards_section, 3, 0, 11),
  [111] = {.entry = {.count = 1, .reusable = true}}, SHIFT(245),
  [113] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_inputs_section, 3, 0, 11),
  [115] = {.entry = {.count = 1, .reusable = true}}, SHIFT(196),
  [117] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_cases_section, 3, 0, 11),
  [119] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_inputs_section_repeat1, 2, 0, 0),
  [121] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_inputs_section_repeat1, 2, 0, 0), SHIFT_REPEAT(196),
  [124] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_guards_section_repeat1, 2, 0, 0),
  [126] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_guards_section_repeat1, 2, 0, 0), SHIFT_REPEAT(245),
  [129] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_edge_cases_section_repeat1, 2, 0, 0),
  [131] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_edge_cases_section_repeat1, 2, 0, 0), SHIFT_REPEAT(245),
  [134] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_item, 6, 0, 21),
  [136] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_section, 3, 0, 11),
  [138] = {.entry = {.count = 1, .reusable = false}}, SHIFT(166),
  [140] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_logic_section_repeat1, 2, 0, 0),
  [142] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_logic_section_repeat1, 2, 0, 0), SHIFT_REPEAT(166),
  [145] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_item, 3, 0, 18),
  [147] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_item, 5, 0, 21),
  [149] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_item, 5, 0, 24),
  [151] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_case_item, 5, 0, 28),
  [153] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_item, 4, 0, 22),
  [155] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_logic_item, 4, 0, 22),
  [157] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_header, 4, 0, 1),
  [159] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_purpose_section, 3, 0, 10),
  [161] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_returns_section, 3, 0, 12),
  [163] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_section, 3, 0, 13),
  [165] = {.entry = {.count = 1, .reusable = true}}, SHIFT(212),
  [167] = {.entry = {.count = 1, .reusable = false}}, SHIFT(65),
  [169] = {.entry = {.count = 1, .reusable = true}}, SHIFT(104),
  [171] = {.entry = {.count = 1, .reusable = true}}, SHIFT(105),
  [173] = {.entry = {.count = 1, .reusable = false}}, SHIFT(106),
  [175] = {.entry = {.count = 1, .reusable = true}}, SHIFT(87),
  [177] = {.entry = {.count = 1, .reusable = true}}, SHIFT(92),
  [179] = {.entry = {.count = 1, .reusable = true}}, SHIFT(188),
  [181] = {.entry = {.count = 1, .reusable = true}}, SHIFT(190),
  [183] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_imports_directive, 3, 0, 4),
  [185] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_block, 3, 0, 0),
  [187] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_close, 2, 0, 0),
  [189] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_close, 2, 0, 0),
  [191] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_block, 3, 0, 0),
  [193] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_close, 2, 0, 0),
  [195] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_block, 3, 0, 0),
  [197] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_close, 2, 0, 0),
  [199] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_block, 3, 0, 0),
  [201] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_block, 3, 0, 6),
  [203] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_block, 2, 0, 0),
  [205] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_block, 2, 0, 0),
  [207] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_close, 2, 0, 0),
  [209] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_block, 2, 0, 0),
  [211] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_block, 2, 0, 0),
  [213] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_module_directive, 3, 0, 1),
  [215] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_version_directive, 3, 0, 2),
  [217] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_directive, 1, 0, 0),
  [219] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_target_directive, 3, 0, 3),
  [221] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0),
  [223] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0), SHIFT_REPEAT(60),
  [226] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0), SHIFT_REPEAT(60),
  [229] = {.entry = {.count = 1, .reusable = false}}, SHIFT(60),
  [231] = {.entry = {.count = 1, .reusable = true}}, SHIFT(60),
  [233] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_text, 1, 0, 0),
  [235] = {.entry = {.count = 1, .reusable = true}}, SHIFT(65),
  [237] = {.entry = {.count = 1, .reusable = true}}, SHIFT(193),
  [239] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0), SHIFT_REPEAT(65),
  [242] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0),
  [244] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0), SHIFT_REPEAT(196),
  [247] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_token, 1, 0, 0),
  [249] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition_token, 1, 0, 0),
  [251] = {.entry = {.count = 1, .reusable = false}}, SHIFT(140),
  [253] = {.entry = {.count = 1, .reusable = true}}, SHIFT(171),
  [255] = {.entry = {.count = 1, .reusable = true}}, SHIFT(236),
  [257] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 1, 0, 0),
  [259] = {.entry = {.count = 1, .reusable = false}}, SHIFT_EXTRA(),
  [261] = {.entry = {.count = 1, .reusable = false}}, SHIFT(202),
  [263] = {.entry = {.count = 1, .reusable = false}}, SHIFT(184),
  [265] = {.entry = {.count = 1, .reusable = false}}, SHIFT(55),
  [267] = {.entry = {.count = 1, .reusable = false}}, SHIFT(77),
  [269] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_test_block_repeat1, 2, 0, 0), SHIFT_REPEAT(65),
  [272] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_test_block_repeat1, 2, 0, 0),
  [274] = {.entry = {.count = 1, .reusable = true}}, SHIFT(151),
  [276] = {.entry = {.count = 1, .reusable = false}}, SHIFT(194),
  [278] = {.entry = {.count = 1, .reusable = false}}, SHIFT(226),
  [280] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 4, 0, 15),
  [282] = {.entry = {.count = 1, .reusable = false}}, SHIFT(244),
  [284] = {.entry = {.count = 1, .reusable = false}}, SHIFT(158),
  [286] = {.entry = {.count = 1, .reusable = true}}, SHIFT(246),
  [288] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 1, 0, 19),
  [290] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 5, 0, 15),
  [292] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 5, 0, 21),
  [294] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 6, 0, 21),
  [296] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_header, 4, 0, 1),
  [298] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 2, 0, 23),
  [300] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 3, 0, 27),
  [302] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_header, 5, 0, 1),
  [304] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_custom_type, 1, 0, 0),
  [306] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_map_type, 5, 0, 29),
  [308] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_invariant_block_repeat1, 2, 0, 0),
  [310] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_invariant_block_repeat1, 2, 0, 0), SHIFT_REPEAT(226),
  [313] = {.entry = {.count = 1, .reusable = true}}, SHIFT(232),
  [315] = {.entry = {.count = 1, .reusable = true}}, SHIFT(152),
  [317] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_property_block_repeat1, 2, 0, 0),
  [319] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_property_block_repeat1, 2, 0, 0), SHIFT_REPEAT(158),
  [322] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_primitive_type, 1, 0, 0),
  [324] = {.entry = {.count = 1, .reusable = true}}, SHIFT(61),
  [326] = {.entry = {.count = 1, .reusable = true}}, SHIFT(74),
  [328] = {.entry = {.count = 1, .reusable = true}}, SHIFT(221),
  [330] = {.entry = {.count = 1, .reusable = true}}, SHIFT(134),
  [332] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [334] = {.entry = {.count = 1, .reusable = true}}, SHIFT(79),
  [336] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_list_type, 3, 0, 20),
  [338] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [340] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_field_constraints, 1, 0, 0),
  [342] = {.entry = {.count = 1, .reusable = true}}, SHIFT(86),
  [344] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_args, 2, 0, 0),
  [346] = {.entry = {.count = 1, .reusable = true}}, SHIFT(101),
  [348] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_list, 2, 0, 0),
  [350] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_spec, 1, 0, 0),
  [352] = {.entry = {.count = 1, .reusable = true}}, SHIFT(128),
  [354] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_value, 1, 0, 0),
  [356] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_quoted_string, 1, 0, 0),
  [358] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_boolean, 1, 0, 0),
  [360] = {.entry = {.count = 1, .reusable = true}}, SHIFT(47),
  [362] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_args, 1, 0, 0),
  [364] = {.entry = {.count = 1, .reusable = true}}, SHIFT(186),
  [366] = {.entry = {.count = 1, .reusable = true}}, SHIFT(195),
  [368] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_text, 1, 0, 0),
  [370] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_depends_list_repeat1, 2, 0, 0), SHIFT_REPEAT(101),
  [373] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_depends_list_repeat1, 2, 0, 0),
  [375] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_error_args_repeat1, 2, 0, 0), SHIFT_REPEAT(86),
  [378] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_error_args_repeat1, 2, 0, 0),
  [380] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_args, 2, 0, 0),
  [382] = {.entry = {.count = 1, .reusable = true}}, SHIFT(135),
  [384] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_import_list, 2, 0, 0),
  [386] = {.entry = {.count = 1, .reusable = false}}, SHIFT(83),
  [388] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_input_constraints_repeat1, 2, 0, 0),
  [390] = {.entry = {.count = 1, .reusable = true}}, SHIFT(70),
  [392] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_input_constraints_repeat1, 2, 0, 0), SHIFT_REPEAT(61),
  [395] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_test_args_repeat1, 2, 0, 0), SHIFT_REPEAT(47),
  [398] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_test_args_repeat1, 2, 0, 0),
  [400] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_constraints, 1, 0, 0),
  [402] = {.entry = {.count = 1, .reusable = true}}, SHIFT(166),
  [404] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_import_list, 1, 0, 0),
  [406] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_import_list_repeat1, 2, 0, 0), SHIFT_REPEAT(135),
  [409] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_import_list_repeat1, 2, 0, 0),
  [411] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_args, 1, 0, 0),
  [413] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_list, 1, 0, 0),
  [415] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_state_prefix, 3, 0, 25),
  [417] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_invariant_header, 4, 0, 8),
  [419] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_spec, 2, 0, 0),
  [421] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_property_assertion, 2, 0, 5),
  [423] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_assertion, 4, 0, 16),
  [425] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_header, 6, 0, 17),
  [427] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_property_header, 6, 0, 17),
  [429] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_arrow, 1, 0, 0),
  [431] = {.entry = {.count = 1, .reusable = false}}, SHIFT(150),
  [433] = {.entry = {.count = 1, .reusable = false}}, SHIFT(216),
  [435] = {.entry = {.count = 1, .reusable = true}}, SHIFT(220),
  [437] = {.entry = {.count = 1, .reusable = true}}, SHIFT(66),
  [439] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_invariant_assertion, 2, 0, 5),
  [441] = {.entry = {.count = 1, .reusable = false}}, SHIFT(228),
  [443] = {.entry = {.count = 1, .reusable = false}}, SHIFT(218),
  [445] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_reference, 3, 0, 0),
  [447] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_condition_text, 1, 0, 0),
  [449] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_constraint_pair, 3, 0, 30),
  [451] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_reference, 1, 0, 0),
  [453] = {.entry = {.count = 1, .reusable = false}}, SHIFT(110),
  [455] = {.entry = {.count = 1, .reusable = true}}, SHIFT(178),
  [457] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [459] = {.entry = {.count = 1, .reusable = true}}, SHIFT(129),
  [461] = {.entry = {.count = 1, .reusable = true}}, SHIFT(163),
  [463] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [465] = {.entry = {.count = 1, .reusable = true}}, SHIFT(213),
  [467] = {.entry = {.count = 1, .reusable = true}}, SHIFT(214),
  [469] = {.entry = {.count = 1, .reusable = true}}, SHIFT(185),
  [471] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [473] = {.entry = {.count = 1, .reusable = true}}, SHIFT(108),
  [475] = {.entry = {.count = 1, .reusable = true}}, SHIFT(68),
  [477] = {.entry = {.count = 1, .reusable = true}}, SHIFT(154),
  [479] = {.entry = {.count = 1, .reusable = true}}, SHIFT(233),
  [481] = {.entry = {.count = 1, .reusable = true}}, SHIFT(243),
  [483] = {.entry = {.count = 1, .reusable = true}}, SHIFT(78),
  [485] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [487] = {.entry = {.count = 1, .reusable = true}}, SHIFT(36),
  [489] = {.entry = {.count = 1, .reusable = true}}, SHIFT(147),
  [491] = {.entry = {.count = 1, .reusable = true}}, SHIFT(71),
  [493] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_call, 4, 0, 14),
  [495] = {.entry = {.count = 1, .reusable = true}}, SHIFT(50),
  [497] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [499] = {.entry = {.count = 1, .reusable = true}}, SHIFT(46),
  [501] = {.entry = {.count = 1, .reusable = true}}, SHIFT(161),
  [503] = {.entry = {.count = 1, .reusable = true}}, SHIFT(51),
  [505] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [507] = {.entry = {.count = 1, .reusable = true}}, SHIFT(180),
  [509] = {.entry = {.count = 1, .reusable = true}}, SHIFT(72),
  [511] = {.entry = {.count = 1, .reusable = true}}, SHIFT(207),
  [513] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [515] = {.entry = {.count = 1, .reusable = true}}, SHIFT(82),
  [517] = {.entry = {.count = 1, .reusable = true}}, SHIFT(20),
  [519] = {.entry = {.count = 1, .reusable = true}}, SHIFT(32),
  [521] = {.entry = {.count = 1, .reusable = true}}, SHIFT(30),
  [523] = {.entry = {.count = 1, .reusable = true}}, SHIFT(121),
  [525] = {.entry = {.count = 1, .reusable = true}}, SHIFT(31),
  [527] = {.entry = {.count = 1, .reusable = true}}, SHIFT(37),
  [529] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [531] = {.entry = {.count = 1, .reusable = true}}, SHIFT(199),
  [533] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_bullet, 1, 0, 0),
  [535] = {.entry = {.count = 1, .reusable = true}}, SHIFT(200),
  [537] = {.entry = {.count = 1, .reusable = true}}, SHIFT(80),
  [539] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_extends_clause, 2, 0, 7),
  [541] = {.entry = {.count = 1, .reusable = true}}, SHIFT(85),
  [543] = {.entry = {.count = 1, .reusable = true}}, SHIFT(130),
  [545] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_text, 1, 0, 0),
  [547] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [549] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_spec, 1, 2, 0),
  [551] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [553] = {.entry = {.count = 1, .reusable = true}}, SHIFT(63),
  [555] = {.entry = {.count = 1, .reusable = true}}, SHIFT(126),
  [557] = {.entry = {.count = 1, .reusable = true}}, SHIFT(225),
  [559] = {.entry = {.count = 1, .reusable = true}}, SHIFT(227),
  [561] = {.entry = {.count = 1, .reusable = true}}, SHIFT(127),
  [563] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 2, 0, 19),
  [565] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_call, 3, 0, 14),
  [567] = {.entry = {.count = 1, .reusable = true}}, SHIFT(241),
  [569] = {.entry = {.count = 1, .reusable = true}}, SHIFT(242),
  [571] = {.entry = {.count = 1, .reusable = false}}, SHIFT(84),
  [573] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_behavior_text, 1, 0, 0),
  [575] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [577] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_description_text, 1, 0, 0),
  [579] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [581] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [583] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_target_name, 1, 0, 0),
  [585] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
  [587] = {.entry = {.count = 1, .reusable = true}}, SHIFT(175),
  [589] = {.entry = {.count = 1, .reusable = true}}, SHIFT(53),
  [591] = {.entry = {.count = 1, .reusable = true}}, SHIFT(234),
  [593] = {.entry = {.count = 1, .reusable = true}}, SHIFT(141),
  [595] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_prefix, 3, 0, 0),
  [597] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_returns_text, 1, 0, 0),
  [599] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_output_binding, 2, 0, 26),
  [601] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 3, 0, 23),
  [603] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [605] = {.entry = {.count = 1, .reusable = true}}, SHIFT(173),
  [607] = {.entry = {.count = 1, .reusable = true}}, SHIFT(208),
  [609] = {.entry = {.count = 1, .reusable = true}}, SHIFT(132),
  [611] = {.entry = {.count = 1, .reusable = true}}, SHIFT(133),
  [613] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_call, 3, 0, 31),
  [615] = {.entry = {.count = 1, .reusable = true}}, SHIFT(240),
  [617] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [619] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 4, 0, 27),
  [621] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_call, 4, 0, 31),
  [623] = {.entry = {.count = 1, .reusable = true}}, SHIFT(235),
  [625] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_header, 4, 0, 9),
  [627] = {.entry = {.count = 1, .reusable = true}}, SHIFT(210),
  [629] = {.entry = {.count = 1, .reusable = true}}, SHIFT(41),
  [631] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_bullet, 1, 0, 0),
  [633] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arrow, 1, 0, 0),
  [635] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_spec, 1, 1, 0),
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
