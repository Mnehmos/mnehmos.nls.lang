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
#define STATE_COUNT 247
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 168
#define ALIAS_COUNT 0
#define TOKEN_COUNT 76
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
  anon_sym_ATinvariant = 48,
  anon_sym_ATproperty = 49,
  sym_expression_text = 50,
  anon_sym_ATliteral = 51,
  anon_sym_QMARK = 52,
  anon_sym_number = 53,
  anon_sym_string = 54,
  anon_sym_boolean = 55,
  anon_sym_void = 56,
  anon_sym_any = 57,
  anon_sym_list = 58,
  anon_sym_of = 59,
  anon_sym_map = 60,
  anon_sym_to = 61,
  sym_number = 62,
  aux_sym_quoted_string_token1 = 63,
  aux_sym_quoted_string_token2 = 64,
  anon_sym_true = 65,
  anon_sym_false = 66,
  anon_sym_True = 67,
  anon_sym_False = 68,
  anon_sym_u2022 = 69,
  anon_sym_DASH = 70,
  anon_sym_STAR = 71,
  anon_sym_u2192 = 72,
  anon_sym_DASH_GT = 73,
  sym__newline = 74,
  sym_literal_content = 75,
  sym_source_file = 76,
  sym_directive = 77,
  sym_module_directive = 78,
  sym_version_directive = 79,
  sym_target_directive = 80,
  sym_imports_directive = 81,
  sym_target_name = 82,
  sym_import_list = 83,
  sym_anlu_block = 84,
  sym_anlu_header = 85,
  sym_purpose_section = 86,
  sym_description_text = 87,
  sym_inputs_section = 88,
  sym_input_item = 89,
  sym_input_constraints = 90,
  sym_guards_section = 91,
  sym_guard_item = 92,
  sym_guard_text = 93,
  sym_error_spec = 94,
  sym_error_call = 95,
  sym_error_args = 96,
  sym_error_text = 97,
  sym_logic_section = 98,
  sym_logic_item = 99,
  sym_logic_step = 100,
  sym_state_prefix = 101,
  sym_condition_prefix = 102,
  sym_condition_text = 103,
  sym_condition_token = 104,
  sym_step_text = 105,
  sym_output_binding = 106,
  sym_returns_section = 107,
  sym_returns_text = 108,
  sym_depends_section = 109,
  sym_depends_list = 110,
  sym_anlu_reference = 111,
  sym_edge_cases_section = 112,
  sym_edge_case_item = 113,
  sym_edge_condition_text = 114,
  sym_edge_behavior_text = 115,
  sym_type_block = 116,
  sym_type_header = 117,
  sym_extends_clause = 118,
  sym_type_field = 119,
  sym_field_constraints = 120,
  sym_constraint_pair = 121,
  sym_type_close = 122,
  sym_test_block = 123,
  sym_test_header = 124,
  sym_test_assertion = 125,
  sym_test_call = 126,
  sym_test_args = 127,
  sym_test_value = 128,
  sym_test_close = 129,
  sym_invariant_block = 130,
  sym_invariant_header = 131,
  sym_invariant_assertion = 132,
  sym_invariant_close = 133,
  sym_property_block = 134,
  sym_property_header = 135,
  sym_property_assertion = 136,
  sym_property_close = 137,
  sym_literal_block = 138,
  sym_literal_header = 139,
  sym_literal_close = 140,
  sym_type_spec = 141,
  sym__base_type = 142,
  sym_primitive_type = 143,
  sym_list_type = 144,
  sym_map_type = 145,
  sym_custom_type = 146,
  sym_quoted_string = 147,
  sym_boolean = 148,
  sym_identifier = 149,
  sym_bullet = 150,
  sym_arrow = 151,
  aux_sym_source_file_repeat1 = 152,
  aux_sym_import_list_repeat1 = 153,
  aux_sym_anlu_block_repeat1 = 154,
  aux_sym_inputs_section_repeat1 = 155,
  aux_sym_input_constraints_repeat1 = 156,
  aux_sym_guards_section_repeat1 = 157,
  aux_sym_error_args_repeat1 = 158,
  aux_sym_logic_section_repeat1 = 159,
  aux_sym_condition_text_repeat1 = 160,
  aux_sym_depends_list_repeat1 = 161,
  aux_sym_edge_cases_section_repeat1 = 162,
  aux_sym_type_block_repeat1 = 163,
  aux_sym_test_block_repeat1 = 164,
  aux_sym_test_args_repeat1 = 165,
  aux_sym_invariant_block_repeat1 = 166,
  aux_sym_property_block_repeat1 = 167,
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
    {field_description, 2},
  [33] =
    {field_variable, 1},
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
  [244] = 177,
  [245] = 132,
  [246] = 246,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(204);
      ADVANCE_MAP(
        '\n', 338,
        '\r', 1,
        '"', 6,
        '#', 207,
        '\'', 16,
        '(', 237,
        ')', 238,
        '*', 335,
        ',', 217,
        '-', 334,
        '.', 240,
        ':', 227,
        '=', 285,
        '?', 311,
        '@', 63,
        'E', 158,
        'F', 28,
        'L', 177,
        'P', 193,
        'R', 161,
        'T', 109,
        '[', 218,
        ']', 220,
        'a', 82,
        'b', 97,
        'e', 150,
        'f', 36,
        'l', 65,
        'm', 29,
        'n', 95,
        'o', 59,
        'p', 153,
        'r', 27,
        's', 139,
        't', 91,
        'v', 93,
        '{', 299,
        '}', 302,
        0x2022, 333,
        0x2192, 336,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(0);
      if (('+' <= lookahead && lookahead <= '/')) ADVANCE(288);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(162);
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(194);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(168);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(286);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(241);
      END_STATE();
    case 1:
      if (lookahead == '\n') ADVANCE(338);
      END_STATE();
    case 2:
      ADVANCE_MAP(
        '\n', 338,
        '\r', 1,
        '"', 6,
        '#', 207,
        '\'', 16,
        ')', 238,
        '-', 26,
        'F', 246,
        'T', 268,
        'f', 248,
        't', 271,
        0x2192, 336,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(321);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 3:
      ADVANCE_MAP(
        '"', 6,
        '#', 207,
        '\'', 16,
        ')', 238,
        '*', 335,
        '-', 334,
        '}', 302,
        0x2022, 333,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(3);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 4:
      if (lookahead == '"') ADVANCE(6);
      if (lookahead == '#') ADVANCE(207);
      if (lookahead == '\'') ADVANCE(16);
      if (lookahead == '-') ADVANCE(198);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(4);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(321);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 5:
      if (lookahead == '"') ADVANCE(6);
      if (lookahead == '#') ADVANCE(207);
      if (lookahead == '\'') ADVANCE(16);
      if (lookahead == 'o') ADVANCE(266);
      if (lookahead == 'r') ADVANCE(255);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(5);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 6:
      if (lookahead == '"') ADVANCE(323);
      if (lookahead != 0) ADVANCE(6);
      END_STATE();
    case 7:
      if (lookahead == '#') ADVANCE(207);
      if (lookahead == '[') ADVANCE(218);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(7);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(221);
      END_STATE();
    case 8:
      if (lookahead == '#') ADVANCE(207);
      if (lookahead == 'a') ADVANCE(262);
      if (lookahead == 'n') ADVANCE(264);
      if (lookahead == 'o') ADVANCE(269);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(8);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(280);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(286);
      if (lookahead == '(' ||
          lookahead == ')' ||
          lookahead == '[' ||
          lookahead == ']') ADVANCE(287);
      if (lookahead == '*' ||
          lookahead == '+' ||
          lookahead == '-' ||
          lookahead == '/') ADVANCE(288);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(283);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 9:
      if (lookahead == '#') ADVANCE(207);
      if (lookahead == 'a') ADVANCE(262);
      if (lookahead == 'n') ADVANCE(264);
      if (lookahead == 'o') ADVANCE(269);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(9);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(286);
      if (lookahead == '(' ||
          lookahead == ')' ||
          lookahead == '[' ||
          lookahead == ']') ADVANCE(287);
      if (lookahead == '*' ||
          lookahead == '+' ||
          lookahead == '-' ||
          lookahead == '/') ADVANCE(288);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(283);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 10:
      ADVANCE_MAP(
        '#', 207,
        'a', 87,
        'b', 97,
        'l', 64,
        'm', 29,
        'n', 144,
        's', 139,
        'v', 93,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(10);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(17);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(301);
      END_STATE();
    case 11:
      if (lookahead == '#') ADVANCE(207);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(223);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(224);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(225);
      END_STATE();
    case 12:
      if (lookahead == '#') ADVANCE(207);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(12);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(242);
      END_STATE();
    case 13:
      if (lookahead == '#') ADVANCE(206);
      if (lookahead == '[') ADVANCE(219);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(233);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(235);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(236);
      END_STATE();
    case 14:
      if (lookahead == '#') ADVANCE(206);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(234);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(235);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(236);
      END_STATE();
    case 15:
      if (lookahead == '#') ADVANCE(205);
      if (lookahead == '}') ADVANCE(302);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(308);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(309);
      END_STATE();
    case 16:
      if (lookahead == '\'') ADVANCE(324);
      if (lookahead != 0) ADVANCE(16);
      END_STATE();
    case 17:
      if (lookahead == '.') ADVANCE(200);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(17);
      END_STATE();
    case 18:
      if (lookahead == ':') ADVANCE(239);
      END_STATE();
    case 19:
      if (lookahead == ':') ADVANCE(232);
      END_STATE();
    case 20:
      if (lookahead == ':') ADVANCE(226);
      END_STATE();
    case 21:
      if (lookahead == ':') ADVANCE(222);
      END_STATE();
    case 22:
      if (lookahead == ':') ADVANCE(295);
      END_STATE();
    case 23:
      if (lookahead == ':') ADVANCE(296);
      END_STATE();
    case 24:
      if (lookahead == ':') ADVANCE(297);
      END_STATE();
    case 25:
      if (lookahead == '=') ADVANCE(304);
      END_STATE();
    case 26:
      if (lookahead == '>') ADVANCE(337);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(321);
      END_STATE();
    case 27:
      if (lookahead == 'E') ADVANCE(192);
      if (lookahead == 'e') ADVANCE(108);
      if (lookahead == 'u') ADVANCE(126);
      END_STATE();
    case 28:
      if (lookahead == 'a') ADVANCE(76);
      END_STATE();
    case 29:
      if (lookahead == 'a') ADVANCE(102);
      END_STATE();
    case 30:
      if (lookahead == 'a') ADVANCE(110);
      if (lookahead == 'e') ADVANCE(127);
      if (lookahead == 'y') ADVANCE(105);
      END_STATE();
    case 31:
      if (lookahead == 'a') ADVANCE(74);
      END_STATE();
    case 32:
      if (lookahead == 'a') ADVANCE(75);
      END_STATE();
    case 33:
      if (lookahead == 'a') ADVANCE(84);
      END_STATE();
    case 34:
      if (lookahead == 'a') ADVANCE(89);
      END_STATE();
    case 35:
      if (lookahead == 'a') ADVANCE(115);
      END_STATE();
    case 36:
      if (lookahead == 'a') ADVANCE(79);
      END_STATE();
    case 37:
      if (lookahead == 'b') ADVANCE(56);
      END_STATE();
    case 38:
      if (lookahead == 'c') ADVANCE(116);
      END_STATE();
    case 39:
      if (lookahead == 'd') ADVANCE(289);
      if (lookahead == 'y') ADVANCE(316);
      END_STATE();
    case 40:
      if (lookahead == 'd') ADVANCE(315);
      END_STATE();
    case 41:
      if (lookahead == 'd') ADVANCE(228);
      END_STATE();
    case 42:
      if (lookahead == 'd') ADVANCE(148);
      END_STATE();
    case 43:
      if (lookahead == 'd') ADVANCE(122);
      END_STATE();
    case 44:
      if (lookahead == 'e') ADVANCE(329);
      END_STATE();
    case 45:
      if (lookahead == 'e') ADVANCE(325);
      END_STATE();
    case 46:
      if (lookahead == 'e') ADVANCE(298);
      END_STATE();
    case 47:
      if (lookahead == 'e') ADVANCE(331);
      END_STATE();
    case 48:
      if (lookahead == 'e') ADVANCE(327);
      END_STATE();
    case 49:
      if (lookahead == 'e') ADVANCE(208);
      END_STATE();
    case 50:
      if (lookahead == 'e') ADVANCE(88);
      END_STATE();
    case 51:
      if (lookahead == 'e') ADVANCE(33);
      END_STATE();
    case 52:
      if (lookahead == 'e') ADVANCE(112);
      END_STATE();
    case 53:
      if (lookahead == 'e') ADVANCE(121);
      END_STATE();
    case 54:
      if (lookahead == 'e') ADVANCE(41);
      END_STATE();
    case 55:
      if (lookahead == 'e') ADVANCE(120);
      END_STATE();
    case 56:
      if (lookahead == 'e') ADVANCE(111);
      END_STATE();
    case 57:
      if (lookahead == 'e') ADVANCE(135);
      END_STATE();
    case 58:
      if (lookahead == 'e') ADVANCE(118);
      END_STATE();
    case 59:
      if (lookahead == 'f') ADVANCE(318);
      if (lookahead == 'p') ADVANCE(140);
      if (lookahead == 'r') ADVANCE(291);
      END_STATE();
    case 60:
      if (lookahead == 'g') ADVANCE(313);
      END_STATE();
    case 61:
      if (lookahead == 'g') ADVANCE(57);
      END_STATE();
    case 62:
      if (lookahead == 'h') ADVANCE(99);
      END_STATE();
    case 63:
      if (lookahead == 'i') ADVANCE(81);
      if (lookahead == 'l') ADVANCE(69);
      if (lookahead == 'm') ADVANCE(92);
      if (lookahead == 'p') ADVANCE(114);
      if (lookahead == 't') ADVANCE(30);
      if (lookahead == 'v') ADVANCE(52);
      END_STATE();
    case 64:
      if (lookahead == 'i') ADVANCE(124);
      END_STATE();
    case 65:
      if (lookahead == 'i') ADVANCE(124);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(169);
      END_STATE();
    case 66:
      if (lookahead == 'i') ADVANCE(40);
      END_STATE();
    case 67:
      if (lookahead == 'i') ADVANCE(86);
      END_STATE();
    case 68:
      if (lookahead == 'i') ADVANCE(106);
      END_STATE();
    case 69:
      if (lookahead == 'i') ADVANCE(143);
      END_STATE();
    case 70:
      if (lookahead == 'i') ADVANCE(96);
      END_STATE();
    case 71:
      if (lookahead == 'i') ADVANCE(119);
      END_STATE();
    case 72:
      if (lookahead == 'i') ADVANCE(101);
      END_STATE();
    case 73:
      if (lookahead == 'i') ADVANCE(34);
      END_STATE();
    case 74:
      if (lookahead == 'l') ADVANCE(310);
      END_STATE();
    case 75:
      if (lookahead == 'l') ADVANCE(230);
      END_STATE();
    case 76:
      if (lookahead == 'l') ADVANCE(125);
      END_STATE();
    case 77:
      if (lookahead == 'l') ADVANCE(51);
      END_STATE();
    case 78:
      if (lookahead == 'l') ADVANCE(49);
      END_STATE();
    case 79:
      if (lookahead == 'l') ADVANCE(128);
      END_STATE();
    case 80:
      if (lookahead == 'm') ADVANCE(37);
      END_STATE();
    case 81:
      if (lookahead == 'm') ADVANCE(104);
      if (lookahead == 'n') ADVANCE(149);
      END_STATE();
    case 82:
      if (lookahead == 'n') ADVANCE(39);
      END_STATE();
    case 83:
      if (lookahead == 'n') ADVANCE(214);
      END_STATE();
    case 84:
      if (lookahead == 'n') ADVANCE(314);
      END_STATE();
    case 85:
      if (lookahead == 'n') ADVANCE(209);
      END_STATE();
    case 86:
      if (lookahead == 'n') ADVANCE(60);
      END_STATE();
    case 87:
      if (lookahead == 'n') ADVANCE(151);
      END_STATE();
    case 88:
      if (lookahead == 'n') ADVANCE(43);
      END_STATE();
    case 89:
      if (lookahead == 'n') ADVANCE(137);
      END_STATE();
    case 90:
      if (lookahead == 'n') ADVANCE(32);
      END_STATE();
    case 91:
      if (lookahead == 'o') ADVANCE(320);
      if (lookahead == 'r') ADVANCE(146);
      if (lookahead == 'y') ADVANCE(103);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(163);
      END_STATE();
    case 92:
      if (lookahead == 'o') ADVANCE(42);
      END_STATE();
    case 93:
      if (lookahead == 'o') ADVANCE(66);
      END_STATE();
    case 94:
      if (lookahead == 'o') ADVANCE(77);
      END_STATE();
    case 95:
      if (lookahead == 'o') ADVANCE(130);
      if (lookahead == 'u') ADVANCE(80);
      END_STATE();
    case 96:
      if (lookahead == 'o') ADVANCE(90);
      END_STATE();
    case 97:
      if (lookahead == 'o') ADVANCE(94);
      END_STATE();
    case 98:
      if (lookahead == 'o') ADVANCE(107);
      END_STATE();
    case 99:
      if (lookahead == 'o') ADVANCE(83);
      END_STATE();
    case 100:
      if (lookahead == 'o') ADVANCE(117);
      END_STATE();
    case 101:
      if (lookahead == 'o') ADVANCE(85);
      END_STATE();
    case 102:
      if (lookahead == 'p') ADVANCE(319);
      END_STATE();
    case 103:
      if (lookahead == 'p') ADVANCE(53);
      END_STATE();
    case 104:
      if (lookahead == 'p') ADVANCE(100);
      END_STATE();
    case 105:
      if (lookahead == 'p') ADVANCE(46);
      END_STATE();
    case 106:
      if (lookahead == 'p') ADVANCE(138);
      END_STATE();
    case 107:
      if (lookahead == 'p') ADVANCE(58);
      END_STATE();
    case 108:
      if (lookahead == 'q') ADVANCE(147);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(196);
      END_STATE();
    case 109:
      if (lookahead == 'r') ADVANCE(145);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(163);
      END_STATE();
    case 110:
      if (lookahead == 'r') ADVANCE(61);
      END_STATE();
    case 111:
      if (lookahead == 'r') ADVANCE(312);
      END_STATE();
    case 112:
      if (lookahead == 'r') ADVANCE(129);
      END_STATE();
    case 113:
      if (lookahead == 'r') ADVANCE(67);
      END_STATE();
    case 114:
      if (lookahead == 'r') ADVANCE(98);
      END_STATE();
    case 115:
      if (lookahead == 'r') ADVANCE(73);
      END_STATE();
    case 116:
      if (lookahead == 'r') ADVANCE(68);
      END_STATE();
    case 117:
      if (lookahead == 'r') ADVANCE(142);
      END_STATE();
    case 118:
      if (lookahead == 'r') ADVANCE(136);
      END_STATE();
    case 119:
      if (lookahead == 'r') ADVANCE(54);
      END_STATE();
    case 120:
      if (lookahead == 'r') ADVANCE(31);
      END_STATE();
    case 121:
      if (lookahead == 's') ADVANCE(38);
      END_STATE();
    case 122:
      if (lookahead == 's') ADVANCE(300);
      END_STATE();
    case 123:
      if (lookahead == 's') ADVANCE(211);
      END_STATE();
    case 124:
      if (lookahead == 's') ADVANCE(132);
      END_STATE();
    case 125:
      if (lookahead == 's') ADVANCE(47);
      END_STATE();
    case 126:
      if (lookahead == 's') ADVANCE(133);
      END_STATE();
    case 127:
      if (lookahead == 's') ADVANCE(134);
      END_STATE();
    case 128:
      if (lookahead == 's') ADVANCE(48);
      END_STATE();
    case 129:
      if (lookahead == 's') ADVANCE(72);
      END_STATE();
    case 130:
      if (lookahead == 't') ADVANCE(293);
      END_STATE();
    case 131:
      if (lookahead == 't') ADVANCE(62);
      END_STATE();
    case 132:
      if (lookahead == 't') ADVANCE(317);
      END_STATE();
    case 133:
      if (lookahead == 't') ADVANCE(216);
      END_STATE();
    case 134:
      if (lookahead == 't') ADVANCE(303);
      END_STATE();
    case 135:
      if (lookahead == 't') ADVANCE(210);
      END_STATE();
    case 136:
      if (lookahead == 't') ADVANCE(152);
      END_STATE();
    case 137:
      if (lookahead == 't') ADVANCE(306);
      END_STATE();
    case 138:
      if (lookahead == 't') ADVANCE(215);
      END_STATE();
    case 139:
      if (lookahead == 't') ADVANCE(113);
      END_STATE();
    case 140:
      if (lookahead == 't') ADVANCE(70);
      END_STATE();
    case 141:
      if (lookahead == 't') ADVANCE(50);
      END_STATE();
    case 142:
      if (lookahead == 't') ADVANCE(123);
      END_STATE();
    case 143:
      if (lookahead == 't') ADVANCE(55);
      END_STATE();
    case 144:
      if (lookahead == 'u') ADVANCE(80);
      END_STATE();
    case 145:
      if (lookahead == 'u') ADVANCE(44);
      END_STATE();
    case 146:
      if (lookahead == 'u') ADVANCE(45);
      END_STATE();
    case 147:
      if (lookahead == 'u') ADVANCE(71);
      END_STATE();
    case 148:
      if (lookahead == 'u') ADVANCE(78);
      END_STATE();
    case 149:
      if (lookahead == 'v') ADVANCE(35);
      END_STATE();
    case 150:
      if (lookahead == 'x') ADVANCE(141);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(170);
      END_STATE();
    case 151:
      if (lookahead == 'y') ADVANCE(316);
      END_STATE();
    case 152:
      if (lookahead == 'y') ADVANCE(307);
      END_STATE();
    case 153:
      if (lookahead == 'y') ADVANCE(131);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(182);
      END_STATE();
    case 154:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(181);
      END_STATE();
    case 155:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(189);
      END_STATE();
    case 156:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(18);
      END_STATE();
    case 157:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(155);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') ADVANCE(157);
      END_STATE();
    case 158:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(170);
      END_STATE();
    case 159:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(184);
      END_STATE();
    case 160:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(188);
      END_STATE();
    case 161:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(192);
      END_STATE();
    case 162:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(180);
      END_STATE();
    case 163:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(172);
      END_STATE();
    case 164:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(197);
      END_STATE();
    case 165:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(175);
      END_STATE();
    case 166:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(21);
      END_STATE();
    case 167:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(190);
      END_STATE();
    case 168:
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(243);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(179);
      END_STATE();
    case 169:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(171);
      END_STATE();
    case 170:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(164);
      END_STATE();
    case 171:
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(156);
      END_STATE();
    case 172:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(244);
      END_STATE();
    case 173:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(179);
      END_STATE();
    case 174:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(186);
      END_STATE();
    case 175:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(160);
      END_STATE();
    case 176:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(187);
      END_STATE();
    case 177:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(169);
      END_STATE();
    case 178:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(176);
      END_STATE();
    case 179:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(195);
      END_STATE();
    case 180:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(165);
      END_STATE();
    case 181:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(159);
      END_STATE();
    case 182:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(178);
      END_STATE();
    case 183:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(174);
      END_STATE();
    case 184:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(19);
      END_STATE();
    case 185:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(20);
      END_STATE();
    case 186:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(22);
      END_STATE();
    case 187:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(166);
      END_STATE();
    case 188:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(23);
      END_STATE();
    case 189:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(167);
      END_STATE();
    case 190:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(24);
      END_STATE();
    case 191:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(185);
      END_STATE();
    case 192:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(196);
      END_STATE();
    case 193:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(182);
      END_STATE();
    case 194:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(154);
      END_STATE();
    case 195:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(191);
      END_STATE();
    case 196:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(183);
      END_STATE();
    case 197:
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') ADVANCE(157);
      END_STATE();
    case 198:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(321);
      END_STATE();
    case 199:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(322);
      END_STATE();
    case 200:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(212);
      END_STATE();
    case 201:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(213);
      END_STATE();
    case 202:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(284);
      END_STATE();
    case 203:
      if (eof) ADVANCE(204);
      ADVANCE_MAP(
        '\n', 338,
        '\r', 1,
        '#', 207,
        '(', 237,
        ')', 238,
        '*', 335,
        ',', 217,
        '-', 334,
        ':', 227,
        '=', 25,
        '@', 63,
        '[', 218,
        ']', 220,
        '{', 299,
        0x2022, 333,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(203);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(162);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(158);
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(194);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(173);
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(177);
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(193);
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(161);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(241);
      END_STATE();
    case 204:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 205:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == '}') ADVANCE(207);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(205);
      END_STATE();
    case 206:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead == '-' ||
          lookahead == 0x2192) ADVANCE(207);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(206);
      END_STATE();
    case 207:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(207);
      END_STATE();
    case 208:
      ACCEPT_TOKEN(anon_sym_ATmodule);
      END_STATE();
    case 209:
      ACCEPT_TOKEN(anon_sym_ATversion);
      END_STATE();
    case 210:
      ACCEPT_TOKEN(anon_sym_ATtarget);
      END_STATE();
    case 211:
      ACCEPT_TOKEN(anon_sym_ATimports);
      END_STATE();
    case 212:
      ACCEPT_TOKEN(sym_version_string);
      if (lookahead == '.') ADVANCE(201);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(212);
      END_STATE();
    case 213:
      ACCEPT_TOKEN(sym_version_string);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(213);
      END_STATE();
    case 214:
      ACCEPT_TOKEN(anon_sym_python);
      END_STATE();
    case 215:
      ACCEPT_TOKEN(anon_sym_typescript);
      END_STATE();
    case 216:
      ACCEPT_TOKEN(anon_sym_rust);
      END_STATE();
    case 217:
      ACCEPT_TOKEN(anon_sym_COMMA);
      END_STATE();
    case 218:
      ACCEPT_TOKEN(anon_sym_LBRACK);
      END_STATE();
    case 219:
      ACCEPT_TOKEN(anon_sym_LBRACK);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(236);
      END_STATE();
    case 220:
      ACCEPT_TOKEN(anon_sym_RBRACK);
      END_STATE();
    case 221:
      ACCEPT_TOKEN(sym_anlu_identifier);
      if (lookahead == '-' ||
          lookahead == '.' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(221);
      END_STATE();
    case 222:
      ACCEPT_TOKEN(aux_sym_purpose_section_token1);
      END_STATE();
    case 223:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (lookahead == '#') ADVANCE(207);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(223);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(224);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(225);
      END_STATE();
    case 224:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(224);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(225);
      END_STATE();
    case 225:
      ACCEPT_TOKEN(aux_sym_description_text_token1);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(225);
      END_STATE();
    case 226:
      ACCEPT_TOKEN(aux_sym_inputs_section_token1);
      END_STATE();
    case 227:
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 228:
      ACCEPT_TOKEN(anon_sym_required);
      END_STATE();
    case 229:
      ACCEPT_TOKEN(anon_sym_required);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 230:
      ACCEPT_TOKEN(anon_sym_optional);
      END_STATE();
    case 231:
      ACCEPT_TOKEN(anon_sym_optional);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 232:
      ACCEPT_TOKEN(aux_sym_guards_section_token1);
      END_STATE();
    case 233:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead == '#') ADVANCE(206);
      if (lookahead == '[') ADVANCE(219);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(233);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(235);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(236);
      END_STATE();
    case 234:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead == '#') ADVANCE(206);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(234);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(235);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(236);
      END_STATE();
    case 235:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(236);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(236);
      END_STATE();
    case 236:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(236);
      END_STATE();
    case 237:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 238:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 239:
      ACCEPT_TOKEN(aux_sym_logic_section_token1);
      END_STATE();
    case 240:
      ACCEPT_TOKEN(anon_sym_DOT);
      END_STATE();
    case 241:
      ACCEPT_TOKEN(sym_step_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(241);
      END_STATE();
    case 242:
      ACCEPT_TOKEN(sym_state_name);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(242);
      END_STATE();
    case 243:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token1);
      END_STATE();
    case 244:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token2);
      END_STATE();
    case 245:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token2);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 246:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(259);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 247:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(260);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 248:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(261);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 249:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'd') ADVANCE(290);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 250:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'd') ADVANCE(229);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 251:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(330);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 252:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(326);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 253:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(332);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 254:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(328);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 255:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(267);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 256:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(250);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 257:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'i') ADVANCE(265);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 258:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'i') ADVANCE(270);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 259:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(272);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 260:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(231);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 261:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(273);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 262:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'n') ADVANCE(249);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 263:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'n') ADVANCE(247);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 264:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'o') ADVANCE(274);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 265:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'o') ADVANCE(263);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 266:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'p') ADVANCE(275);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 267:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'q') ADVANCE(278);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 268:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(276);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 269:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(292);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 270:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(256);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 271:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(277);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 272:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 's') ADVANCE(253);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 273:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 's') ADVANCE(254);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 274:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 't') ADVANCE(294);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 275:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 't') ADVANCE(257);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 276:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(251);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 277:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(252);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 278:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(258);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 279:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(281);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 280:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(279);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 281:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(245);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 282:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 283:
      ACCEPT_TOKEN(aux_sym_condition_token_token2);
      if (lookahead == '.') ADVANCE(202);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(283);
      END_STATE();
    case 284:
      ACCEPT_TOKEN(aux_sym_condition_token_token2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(284);
      END_STATE();
    case 285:
      ACCEPT_TOKEN(aux_sym_condition_token_token3);
      if (lookahead == '=') ADVANCE(305);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(286);
      END_STATE();
    case 286:
      ACCEPT_TOKEN(aux_sym_condition_token_token3);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(286);
      END_STATE();
    case 287:
      ACCEPT_TOKEN(aux_sym_condition_token_token4);
      END_STATE();
    case 288:
      ACCEPT_TOKEN(aux_sym_condition_token_token5);
      END_STATE();
    case 289:
      ACCEPT_TOKEN(anon_sym_and);
      END_STATE();
    case 290:
      ACCEPT_TOKEN(anon_sym_and);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 291:
      ACCEPT_TOKEN(anon_sym_or);
      END_STATE();
    case 292:
      ACCEPT_TOKEN(anon_sym_or);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 293:
      ACCEPT_TOKEN(anon_sym_not);
      END_STATE();
    case 294:
      ACCEPT_TOKEN(anon_sym_not);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 295:
      ACCEPT_TOKEN(aux_sym_returns_section_token1);
      END_STATE();
    case 296:
      ACCEPT_TOKEN(aux_sym_depends_section_token1);
      END_STATE();
    case 297:
      ACCEPT_TOKEN(aux_sym_edge_cases_section_token1);
      END_STATE();
    case 298:
      ACCEPT_TOKEN(anon_sym_ATtype);
      END_STATE();
    case 299:
      ACCEPT_TOKEN(anon_sym_LBRACE);
      END_STATE();
    case 300:
      ACCEPT_TOKEN(anon_sym_extends);
      END_STATE();
    case 301:
      ACCEPT_TOKEN(sym_type_name);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(301);
      END_STATE();
    case 302:
      ACCEPT_TOKEN(anon_sym_RBRACE);
      END_STATE();
    case 303:
      ACCEPT_TOKEN(anon_sym_ATtest);
      END_STATE();
    case 304:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      END_STATE();
    case 305:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(286);
      END_STATE();
    case 306:
      ACCEPT_TOKEN(anon_sym_ATinvariant);
      END_STATE();
    case 307:
      ACCEPT_TOKEN(anon_sym_ATproperty);
      END_STATE();
    case 308:
      ACCEPT_TOKEN(sym_expression_text);
      if (lookahead == '#') ADVANCE(205);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(308);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '}') ADVANCE(309);
      END_STATE();
    case 309:
      ACCEPT_TOKEN(sym_expression_text);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '}') ADVANCE(309);
      END_STATE();
    case 310:
      ACCEPT_TOKEN(anon_sym_ATliteral);
      END_STATE();
    case 311:
      ACCEPT_TOKEN(anon_sym_QMARK);
      END_STATE();
    case 312:
      ACCEPT_TOKEN(anon_sym_number);
      END_STATE();
    case 313:
      ACCEPT_TOKEN(anon_sym_string);
      END_STATE();
    case 314:
      ACCEPT_TOKEN(anon_sym_boolean);
      END_STATE();
    case 315:
      ACCEPT_TOKEN(anon_sym_void);
      END_STATE();
    case 316:
      ACCEPT_TOKEN(anon_sym_any);
      END_STATE();
    case 317:
      ACCEPT_TOKEN(anon_sym_list);
      END_STATE();
    case 318:
      ACCEPT_TOKEN(anon_sym_of);
      END_STATE();
    case 319:
      ACCEPT_TOKEN(anon_sym_map);
      END_STATE();
    case 320:
      ACCEPT_TOKEN(anon_sym_to);
      END_STATE();
    case 321:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(199);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(321);
      END_STATE();
    case 322:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(322);
      END_STATE();
    case 323:
      ACCEPT_TOKEN(aux_sym_quoted_string_token1);
      END_STATE();
    case 324:
      ACCEPT_TOKEN(aux_sym_quoted_string_token2);
      END_STATE();
    case 325:
      ACCEPT_TOKEN(anon_sym_true);
      END_STATE();
    case 326:
      ACCEPT_TOKEN(anon_sym_true);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 327:
      ACCEPT_TOKEN(anon_sym_false);
      END_STATE();
    case 328:
      ACCEPT_TOKEN(anon_sym_false);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 329:
      ACCEPT_TOKEN(anon_sym_True);
      END_STATE();
    case 330:
      ACCEPT_TOKEN(anon_sym_True);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 331:
      ACCEPT_TOKEN(anon_sym_False);
      END_STATE();
    case 332:
      ACCEPT_TOKEN(anon_sym_False);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(282);
      END_STATE();
    case 333:
      ACCEPT_TOKEN(anon_sym_u2022);
      END_STATE();
    case 334:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 335:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 336:
      ACCEPT_TOKEN(anon_sym_u2192);
      END_STATE();
    case 337:
      ACCEPT_TOKEN(anon_sym_DASH_GT);
      END_STATE();
    case 338:
      ACCEPT_TOKEN(sym__newline);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0, .external_lex_state = 1},
  [1] = {.lex_state = 203},
  [2] = {.lex_state = 203},
  [3] = {.lex_state = 203},
  [4] = {.lex_state = 203},
  [5] = {.lex_state = 203},
  [6] = {.lex_state = 203},
  [7] = {.lex_state = 203},
  [8] = {.lex_state = 203},
  [9] = {.lex_state = 203},
  [10] = {.lex_state = 203},
  [11] = {.lex_state = 203},
  [12] = {.lex_state = 203},
  [13] = {.lex_state = 203},
  [14] = {.lex_state = 203},
  [15] = {.lex_state = 203},
  [16] = {.lex_state = 203},
  [17] = {.lex_state = 203},
  [18] = {.lex_state = 203},
  [19] = {.lex_state = 203},
  [20] = {.lex_state = 203},
  [21] = {.lex_state = 203},
  [22] = {.lex_state = 203},
  [23] = {.lex_state = 203},
  [24] = {.lex_state = 203},
  [25] = {.lex_state = 2},
  [26] = {.lex_state = 10},
  [27] = {.lex_state = 10},
  [28] = {.lex_state = 10},
  [29] = {.lex_state = 10},
  [30] = {.lex_state = 10},
  [31] = {.lex_state = 10},
  [32] = {.lex_state = 203},
  [33] = {.lex_state = 203},
  [34] = {.lex_state = 203},
  [35] = {.lex_state = 203},
  [36] = {.lex_state = 203},
  [37] = {.lex_state = 203},
  [38] = {.lex_state = 203},
  [39] = {.lex_state = 203},
  [40] = {.lex_state = 2},
  [41] = {.lex_state = 203},
  [42] = {.lex_state = 203},
  [43] = {.lex_state = 203},
  [44] = {.lex_state = 2},
  [45] = {.lex_state = 203},
  [46] = {.lex_state = 203},
  [47] = {.lex_state = 203},
  [48] = {.lex_state = 203},
  [49] = {.lex_state = 203},
  [50] = {.lex_state = 203},
  [51] = {.lex_state = 203},
  [52] = {.lex_state = 203},
  [53] = {.lex_state = 8},
  [54] = {.lex_state = 9},
  [55] = {.lex_state = 8},
  [56] = {.lex_state = 3},
  [57] = {.lex_state = 3},
  [58] = {.lex_state = 3},
  [59] = {.lex_state = 8},
  [60] = {.lex_state = 5},
  [61] = {.lex_state = 3},
  [62] = {.lex_state = 13},
  [63] = {.lex_state = 3},
  [64] = {.lex_state = 3},
  [65] = {.lex_state = 203},
  [66] = {.lex_state = 203},
  [67] = {.lex_state = 3},
  [68] = {.lex_state = 203},
  [69] = {.lex_state = 4},
  [70] = {.lex_state = 11},
  [71] = {.lex_state = 203},
  [72] = {.lex_state = 3},
  [73] = {.lex_state = 15},
  [74] = {.lex_state = 3},
  [75] = {.lex_state = 15},
  [76] = {.lex_state = 3},
  [77] = {.lex_state = 15},
  [78] = {.lex_state = 2},
  [79] = {.lex_state = 3},
  [80] = {.lex_state = 2},
  [81] = {.lex_state = 2},
  [82] = {.lex_state = 3},
  [83] = {.lex_state = 3},
  [84] = {.lex_state = 15},
  [85] = {.lex_state = 3},
  [86] = {.lex_state = 0},
  [87] = {.lex_state = 0},
  [88] = {.lex_state = 0},
  [89] = {.lex_state = 15},
  [90] = {.lex_state = 14},
  [91] = {.lex_state = 0},
  [92] = {.lex_state = 2},
  [93] = {.lex_state = 7},
  [94] = {.lex_state = 0},
  [95] = {.lex_state = 15},
  [96] = {.lex_state = 0},
  [97] = {.lex_state = 0},
  [98] = {.lex_state = 0},
  [99] = {.lex_state = 203},
  [100] = {.lex_state = 203},
  [101] = {.lex_state = 0},
  [102] = {.lex_state = 3},
  [103] = {.lex_state = 7},
  [104] = {.lex_state = 0},
  [105] = {.lex_state = 0},
  [106] = {.lex_state = 203},
  [107] = {.lex_state = 203},
  [108] = {.lex_state = 203},
  [109] = {.lex_state = 2},
  [110] = {.lex_state = 0},
  [111] = {.lex_state = 2},
  [112] = {.lex_state = 0},
  [113] = {.lex_state = 0},
  [114] = {.lex_state = 203},
  [115] = {.lex_state = 2},
  [116] = {.lex_state = 0},
  [117] = {.lex_state = 0},
  [118] = {.lex_state = 0},
  [119] = {.lex_state = 0},
  [120] = {.lex_state = 203},
  [121] = {.lex_state = 0},
  [122] = {.lex_state = 0},
  [123] = {.lex_state = 0},
  [124] = {.lex_state = 203},
  [125] = {.lex_state = 203},
  [126] = {.lex_state = 3},
  [127] = {.lex_state = 15},
  [128] = {.lex_state = 15},
  [129] = {.lex_state = 14},
  [130] = {.lex_state = 3},
  [131] = {.lex_state = 15},
  [132] = {.lex_state = 11},
  [133] = {.lex_state = 0},
  [134] = {.lex_state = 3},
  [135] = {.lex_state = 14},
  [136] = {.lex_state = 11},
  [137] = {.lex_state = 0},
  [138] = {.lex_state = 0},
  [139] = {.lex_state = 3},
  [140] = {.lex_state = 0},
  [141] = {.lex_state = 0},
  [142] = {.lex_state = 203},
  [143] = {.lex_state = 3},
  [144] = {.lex_state = 0},
  [145] = {.lex_state = 14},
  [146] = {.lex_state = 2},
  [147] = {.lex_state = 3},
  [148] = {.lex_state = 14},
  [149] = {.lex_state = 3},
  [150] = {.lex_state = 14},
  [151] = {.lex_state = 11},
  [152] = {.lex_state = 0},
  [153] = {.lex_state = 15},
  [154] = {.lex_state = 11},
  [155] = {.lex_state = 3},
  [156] = {.lex_state = 203},
  [157] = {.lex_state = 0},
  [158] = {.lex_state = 0},
  [159] = {.lex_state = 0},
  [160] = {.lex_state = 203},
  [161] = {.lex_state = 0},
  [162] = {.lex_state = 0},
  [163] = {.lex_state = 0},
  [164] = {.lex_state = 203},
  [165] = {.lex_state = 0},
  [166] = {.lex_state = 0},
  [167] = {.lex_state = 10},
  [168] = {.lex_state = 0},
  [169] = {.lex_state = 7},
  [170] = {.lex_state = 203},
  [171] = {.lex_state = 0},
  [172] = {.lex_state = 0},
  [173] = {.lex_state = 203},
  [174] = {.lex_state = 203},
  [175] = {.lex_state = 0},
  [176] = {.lex_state = 0},
  [177] = {.lex_state = 3},
  [178] = {.lex_state = 0},
  [179] = {.lex_state = 0},
  [180] = {.lex_state = 203},
  [181] = {.lex_state = 0},
  [182] = {.lex_state = 12},
  [183] = {.lex_state = 10},
  [184] = {.lex_state = 0},
  [185] = {.lex_state = 203},
  [186] = {.lex_state = 0},
  [187] = {.lex_state = 0},
  [188] = {.lex_state = 0},
  [189] = {.lex_state = 0},
  [190] = {.lex_state = 0},
  [191] = {.lex_state = 0},
  [192] = {.lex_state = 0},
  [193] = {.lex_state = 0},
  [194] = {.lex_state = 0, .external_lex_state = 1},
  [195] = {.lex_state = 0},
  [196] = {.lex_state = 0},
  [197] = {.lex_state = 0},
  [198] = {.lex_state = 0},
  [199] = {.lex_state = 0},
  [200] = {.lex_state = 0},
  [201] = {.lex_state = 0},
  [202] = {.lex_state = 0},
  [203] = {.lex_state = 0},
  [204] = {.lex_state = 0},
  [205] = {.lex_state = 203},
  [206] = {.lex_state = 0},
  [207] = {.lex_state = 7},
  [208] = {.lex_state = 0},
  [209] = {.lex_state = 203},
  [210] = {.lex_state = 0},
  [211] = {.lex_state = 203},
  [212] = {.lex_state = 10},
  [213] = {.lex_state = 0},
  [214] = {.lex_state = 10},
  [215] = {.lex_state = 0},
  [216] = {.lex_state = 0},
  [217] = {.lex_state = 203},
  [218] = {.lex_state = 0},
  [219] = {.lex_state = 7},
  [220] = {.lex_state = 0},
  [221] = {.lex_state = 0},
  [222] = {.lex_state = 0},
  [223] = {.lex_state = 0},
  [224] = {.lex_state = 7},
  [225] = {.lex_state = 0},
  [226] = {.lex_state = 14},
  [227] = {.lex_state = 0},
  [228] = {.lex_state = 0},
  [229] = {.lex_state = 0},
  [230] = {.lex_state = 0},
  [231] = {.lex_state = 0},
  [232] = {.lex_state = 0},
  [233] = {.lex_state = 203},
  [234] = {.lex_state = 0},
  [235] = {.lex_state = 0},
  [236] = {.lex_state = 203},
  [237] = {.lex_state = 0, .external_lex_state = 1},
  [238] = {.lex_state = 0},
  [239] = {.lex_state = 0},
  [240] = {.lex_state = 0},
  [241] = {.lex_state = 0},
  [242] = {.lex_state = 0},
  [243] = {.lex_state = 0},
  [244] = {.lex_state = 14},
  [245] = {.lex_state = 3},
  [246] = {.lex_state = 203},
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
    [sym_source_file] = STATE(162),
    [sym_directive] = STATE(3),
    [sym_module_directive] = STATE(32),
    [sym_version_directive] = STATE(32),
    [sym_target_directive] = STATE(32),
    [sym_imports_directive] = STATE(32),
    [sym_anlu_block] = STATE(3),
    [sym_anlu_header] = STATE(4),
    [sym_type_block] = STATE(3),
    [sym_type_header] = STATE(57),
    [sym_test_block] = STATE(3),
    [sym_test_header] = STATE(61),
    [sym_invariant_block] = STATE(3),
    [sym_invariant_header] = STATE(75),
    [sym_property_block] = STATE(3),
    [sym_property_header] = STATE(73),
    [sym_literal_block] = STATE(3),
    [sym_literal_header] = STATE(194),
    [aux_sym_source_file_repeat1] = STATE(3),
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
    ACTIONS(29), 1,
      ts_builtin_sym_end,
    ACTIONS(31), 1,
      anon_sym_ATmodule,
    ACTIONS(34), 1,
      anon_sym_ATversion,
    ACTIONS(37), 1,
      anon_sym_ATtarget,
    ACTIONS(40), 1,
      anon_sym_ATimports,
    ACTIONS(43), 1,
      anon_sym_LBRACK,
    ACTIONS(46), 1,
      anon_sym_ATtype,
    ACTIONS(49), 1,
      anon_sym_ATtest,
    ACTIONS(52), 1,
      anon_sym_ATinvariant,
    ACTIONS(55), 1,
      anon_sym_ATproperty,
    ACTIONS(58), 1,
      anon_sym_ATliteral,
    ACTIONS(61), 1,
      sym__newline,
    STATE(4), 1,
      sym_anlu_header,
    STATE(57), 1,
      sym_type_header,
    STATE(61), 1,
      sym_test_header,
    STATE(73), 1,
      sym_property_header,
    STATE(75), 1,
      sym_invariant_header,
    STATE(194), 1,
      sym_literal_header,
    STATE(32), 4,
      sym_module_directive,
      sym_version_directive,
      sym_target_directive,
      sym_imports_directive,
    STATE(2), 8,
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
    ACTIONS(64), 1,
      ts_builtin_sym_end,
    ACTIONS(66), 1,
      sym__newline,
    STATE(4), 1,
      sym_anlu_header,
    STATE(57), 1,
      sym_type_header,
    STATE(61), 1,
      sym_test_header,
    STATE(73), 1,
      sym_property_header,
    STATE(75), 1,
      sym_invariant_header,
    STATE(194), 1,
      sym_literal_header,
    STATE(32), 4,
      sym_module_directive,
      sym_version_directive,
      sym_target_directive,
      sym_imports_directive,
    STATE(2), 8,
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
    STATE(5), 8,
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
    STATE(6), 8,
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
    STATE(155), 1,
      sym_bullet,
    STATE(12), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
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
    STATE(129), 1,
      sym_bullet,
    STATE(10), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
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
    STATE(148), 1,
      sym_bullet,
    STATE(11), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(115), 3,
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
    STATE(129), 1,
      sym_bullet,
    STATE(10), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
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
    STATE(148), 1,
      sym_bullet,
    STATE(11), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
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
    STATE(155), 1,
      sym_bullet,
    STATE(12), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
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
  [517] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(136), 1,
      sym_step_number,
    STATE(16), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
    ACTIONS(134), 19,
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
  [549] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(138), 22,
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
  [577] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(140), 22,
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
  [605] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(144), 1,
      sym_step_number,
    STATE(16), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
    ACTIONS(142), 19,
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
  [721] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(153), 20,
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
      anon_sym_ATinvariant,
      anon_sym_ATproperty,
      anon_sym_ATliteral,
      sym__newline,
  [747] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(155), 19,
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
  [772] = 2,
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
  [797] = 2,
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
  [822] = 2,
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
  [847] = 9,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(163), 1,
      anon_sym_RPAREN,
    ACTIONS(165), 1,
      aux_sym_condition_token_token1,
    ACTIONS(167), 1,
      sym_number,
    STATE(108), 1,
      sym_test_value,
    STATE(211), 1,
      sym_test_args,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(99), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(171), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [881] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(173), 1,
      sym_type_name,
    ACTIONS(177), 1,
      anon_sym_list,
    ACTIONS(179), 1,
      anon_sym_map,
    STATE(86), 1,
      sym_type_spec,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(105), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [911] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(173), 1,
      sym_type_name,
    ACTIONS(177), 1,
      anon_sym_list,
    ACTIONS(179), 1,
      anon_sym_map,
    STATE(97), 1,
      sym_type_spec,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(105), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [941] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(173), 1,
      sym_type_name,
    ACTIONS(177), 1,
      anon_sym_list,
    ACTIONS(179), 1,
      anon_sym_map,
    STATE(88), 1,
      sym_type_spec,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(105), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [971] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(173), 1,
      sym_type_name,
    ACTIONS(177), 1,
      anon_sym_list,
    ACTIONS(179), 1,
      anon_sym_map,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(87), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [998] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(173), 1,
      sym_type_name,
    ACTIONS(177), 1,
      anon_sym_list,
    ACTIONS(179), 1,
      anon_sym_map,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(191), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [1025] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(173), 1,
      sym_type_name,
    ACTIONS(177), 1,
      anon_sym_list,
    ACTIONS(179), 1,
      anon_sym_map,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(96), 5,
      sym__base_type,
      sym_primitive_type,
      sym_list_type,
      sym_map_type,
      sym_custom_type,
  [1052] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(181), 12,
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
  [1070] = 2,
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
  [1088] = 2,
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
  [1106] = 2,
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
  [1124] = 2,
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
  [1142] = 2,
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
  [1160] = 2,
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
  [1178] = 2,
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
  [1196] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(165), 1,
      aux_sym_condition_token_token1,
    ACTIONS(167), 1,
      sym_number,
    STATE(199), 1,
      sym_test_value,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(99), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(171), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [1224] = 2,
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
  [1242] = 2,
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
  [1260] = 2,
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
  [1278] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(165), 1,
      aux_sym_condition_token_token1,
    ACTIONS(167), 1,
      sym_number,
    STATE(142), 1,
      sym_test_value,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(99), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(171), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [1306] = 2,
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
  [1324] = 2,
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
  [1342] = 2,
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
  [1360] = 2,
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
  [1378] = 2,
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
  [1396] = 2,
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
  [1414] = 2,
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
  [1432] = 2,
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
  [1450] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(219), 1,
      aux_sym_condition_prefix_token2,
    STATE(55), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(221), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(223), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1473] = 5,
    ACTIONS(3), 1,
      sym_comment,
    STATE(208), 1,
      sym_condition_text,
    STATE(53), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(221), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(223), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1496] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(225), 1,
      aux_sym_condition_prefix_token2,
    STATE(55), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(227), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(230), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1519] = 8,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(235), 1,
      anon_sym_RBRACE,
    STATE(37), 1,
      sym_type_close,
    STATE(139), 1,
      sym_bullet,
    STATE(161), 1,
      sym_identifier,
    STATE(58), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1547] = 8,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(235), 1,
      anon_sym_RBRACE,
    STATE(48), 1,
      sym_type_close,
    STATE(139), 1,
      sym_bullet,
    STATE(161), 1,
      sym_identifier,
    STATE(56), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1575] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(237), 1,
      aux_sym_condition_token_token1,
    ACTIONS(240), 1,
      anon_sym_RBRACE,
    STATE(139), 1,
      sym_bullet,
    STATE(161), 1,
      sym_identifier,
    STATE(58), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(242), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1600] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(247), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
    ACTIONS(245), 5,
      aux_sym_condition_prefix_token2,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
  [1617] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(165), 1,
      aux_sym_condition_token_token1,
    STATE(117), 1,
      sym_identifier,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    ACTIONS(249), 2,
      anon_sym_required,
      anon_sym_optional,
    STATE(138), 2,
      sym_constraint_pair,
      sym_quoted_string,
  [1639] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(251), 1,
      anon_sym_RBRACE,
    STATE(34), 1,
      sym_test_close,
    STATE(160), 1,
      sym_test_call,
    STATE(164), 1,
      sym_identifier,
    STATE(63), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1662] = 8,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(255), 1,
      anon_sym_LBRACK,
    ACTIONS(257), 1,
      aux_sym_guard_text_token1,
    ACTIONS(259), 1,
      aux_sym_condition_prefix_token1,
    STATE(78), 1,
      sym_step_text,
    STATE(90), 1,
      sym_state_prefix,
    STATE(135), 1,
      sym_condition_prefix,
    STATE(158), 1,
      sym_logic_step,
  [1687] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(251), 1,
      anon_sym_RBRACE,
    STATE(42), 1,
      sym_test_close,
    STATE(160), 1,
      sym_test_call,
    STATE(164), 1,
      sym_identifier,
    STATE(67), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1710] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(261), 1,
      anon_sym_RPAREN,
    STATE(236), 1,
      sym_error_args,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(124), 2,
      sym_quoted_string,
      sym_identifier,
  [1731] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(129), 1,
      sym_bullet,
    STATE(8), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
    ACTIONS(115), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1747] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(148), 1,
      sym_bullet,
    STATE(9), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(115), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1763] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(263), 1,
      aux_sym_condition_token_token1,
    ACTIONS(266), 1,
      anon_sym_RBRACE,
    STATE(160), 1,
      sym_test_call,
    STATE(164), 1,
      sym_identifier,
    STATE(67), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1783] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(155), 1,
      sym_bullet,
    STATE(7), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1799] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(268), 1,
      sym_number,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(152), 2,
      sym_quoted_string,
      sym_identifier,
  [1817] = 7,
    ACTIONS(165), 1,
      aux_sym_condition_token_token1,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(270), 1,
      aux_sym_description_text_token1,
    STATE(202), 1,
      sym_error_spec,
    STATE(203), 1,
      sym_error_call,
    STATE(204), 1,
      sym_error_text,
    STATE(205), 1,
      sym_identifier,
  [1839] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(272), 6,
      anon_sym_COMMA,
      anon_sym_COLON,
      anon_sym_LPAREN,
      anon_sym_RPAREN,
      anon_sym_LBRACE,
      sym__newline,
  [1851] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(274), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1862] = 5,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(276), 1,
      anon_sym_RBRACE,
    ACTIONS(278), 1,
      sym_expression_text,
    STATE(41), 1,
      sym_property_close,
    STATE(84), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [1879] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(280), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1890] = 5,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(282), 1,
      anon_sym_RBRACE,
    ACTIONS(284), 1,
      sym_expression_text,
    STATE(36), 1,
      sym_invariant_close,
    STATE(77), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [1907] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(286), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1918] = 5,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(282), 1,
      anon_sym_RBRACE,
    ACTIONS(284), 1,
      sym_expression_text,
    STATE(45), 1,
      sym_invariant_close,
    STATE(95), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [1935] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(290), 1,
      sym__newline,
    STATE(147), 1,
      sym_arrow,
    STATE(213), 1,
      sym_output_binding,
    ACTIONS(288), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1952] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(292), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1963] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(294), 1,
      sym__newline,
    STATE(147), 1,
      sym_arrow,
    STATE(229), 1,
      sym_output_binding,
    ACTIONS(288), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1980] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(296), 1,
      sym__newline,
    STATE(147), 1,
      sym_arrow,
    STATE(238), 1,
      sym_output_binding,
    ACTIONS(288), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1997] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(298), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [2008] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(156), 2,
      sym_quoted_string,
      sym_identifier,
  [2023] = 5,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(276), 1,
      anon_sym_RBRACE,
    ACTIONS(278), 1,
      sym_expression_text,
    STATE(46), 1,
      sym_property_close,
    STATE(89), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [2040] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(300), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [2051] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(302), 1,
      anon_sym_COMMA,
    ACTIONS(304), 1,
      sym__newline,
    STATE(113), 1,
      aux_sym_input_constraints_repeat1,
    STATE(168), 1,
      sym_field_constraints,
  [2067] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(306), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2077] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(302), 1,
      anon_sym_COMMA,
    ACTIONS(308), 1,
      sym__newline,
    STATE(123), 1,
      aux_sym_input_constraints_repeat1,
    STATE(221), 1,
      sym_input_constraints,
  [2093] = 4,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(310), 1,
      anon_sym_RBRACE,
    ACTIONS(312), 1,
      sym_expression_text,
    STATE(89), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [2107] = 5,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(257), 1,
      aux_sym_guard_text_token1,
    ACTIONS(259), 1,
      aux_sym_condition_prefix_token1,
    STATE(80), 1,
      sym_step_text,
    STATE(145), 1,
      sym_condition_prefix,
  [2123] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(315), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2133] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(319), 1,
      sym__newline,
    STATE(70), 1,
      sym_arrow,
    ACTIONS(317), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2147] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(321), 1,
      anon_sym_LBRACK,
    ACTIONS(323), 1,
      sym_anlu_identifier,
    STATE(121), 1,
      sym_anlu_reference,
    STATE(210), 1,
      sym_depends_list,
  [2163] = 3,
    ACTIONS(3), 1,
      sym_comment,
    STATE(243), 1,
      sym_target_name,
    ACTIONS(325), 3,
      anon_sym_python,
      anon_sym_typescript,
      anon_sym_rust,
  [2175] = 4,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(327), 1,
      anon_sym_RBRACE,
    ACTIONS(329), 1,
      sym_expression_text,
    STATE(95), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [2189] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(332), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2199] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(302), 1,
      anon_sym_COMMA,
    ACTIONS(334), 1,
      sym__newline,
    STATE(113), 1,
      aux_sym_input_constraints_repeat1,
    STATE(197), 1,
      sym_field_constraints,
  [2215] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(336), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2225] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(338), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2234] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(340), 1,
      anon_sym_COMMA,
    ACTIONS(343), 1,
      anon_sym_RPAREN,
    STATE(100), 1,
      aux_sym_error_args_repeat1,
  [2247] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(345), 1,
      anon_sym_COMMA,
    ACTIONS(348), 1,
      sym__newline,
    STATE(101), 1,
      aux_sym_import_list_repeat1,
  [2260] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(116), 1,
      sym_identifier,
    STATE(188), 1,
      sym_import_list,
  [2273] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(321), 1,
      anon_sym_LBRACK,
    ACTIONS(323), 1,
      sym_anlu_identifier,
    STATE(141), 1,
      sym_anlu_reference,
  [2286] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(350), 1,
      anon_sym_COMMA,
    ACTIONS(352), 1,
      sym__newline,
    STATE(110), 1,
      aux_sym_depends_list_repeat1,
  [2299] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(356), 1,
      anon_sym_QMARK,
    ACTIONS(354), 2,
      anon_sym_COMMA,
      sym__newline,
  [2310] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(358), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2319] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(360), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2328] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(362), 1,
      anon_sym_COMMA,
    ACTIONS(364), 1,
      anon_sym_RPAREN,
    STATE(114), 1,
      aux_sym_test_args_repeat1,
  [2341] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(366), 3,
      anon_sym_u2192,
      anon_sym_DASH_GT,
      sym__newline,
  [2350] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(368), 1,
      anon_sym_COMMA,
    ACTIONS(371), 1,
      sym__newline,
    STATE(110), 1,
      aux_sym_depends_list_repeat1,
  [2363] = 3,
    ACTIONS(3), 1,
      sym_comment,
    STATE(136), 1,
      sym_arrow,
    ACTIONS(317), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2374] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(373), 1,
      anon_sym_COMMA,
    ACTIONS(375), 1,
      sym__newline,
    STATE(101), 1,
      aux_sym_import_list_repeat1,
  [2387] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(302), 1,
      anon_sym_COMMA,
    ACTIONS(377), 1,
      sym__newline,
    STATE(119), 1,
      aux_sym_input_constraints_repeat1,
  [2400] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(362), 1,
      anon_sym_COMMA,
    ACTIONS(379), 1,
      anon_sym_RPAREN,
    STATE(120), 1,
      aux_sym_test_args_repeat1,
  [2413] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(381), 3,
      anon_sym_u2192,
      anon_sym_DASH_GT,
      sym__newline,
  [2422] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(373), 1,
      anon_sym_COMMA,
    ACTIONS(383), 1,
      sym__newline,
    STATE(112), 1,
      aux_sym_import_list_repeat1,
  [2435] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(387), 1,
      anon_sym_COLON,
    ACTIONS(385), 2,
      anon_sym_COMMA,
      sym__newline,
  [2446] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(136), 1,
      sym_step_number,
    STATE(13), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
  [2457] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(385), 1,
      sym__newline,
    ACTIONS(389), 1,
      anon_sym_COMMA,
    STATE(119), 1,
      aux_sym_input_constraints_repeat1,
  [2470] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(392), 1,
      anon_sym_COMMA,
    ACTIONS(395), 1,
      anon_sym_RPAREN,
    STATE(120), 1,
      aux_sym_test_args_repeat1,
  [2483] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(350), 1,
      anon_sym_COMMA,
    ACTIONS(397), 1,
      sym__newline,
    STATE(104), 1,
      aux_sym_depends_list_repeat1,
  [2496] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(399), 1,
      anon_sym_LBRACE,
    ACTIONS(401), 1,
      anon_sym_extends,
    STATE(171), 1,
      sym_extends_clause,
  [2509] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(302), 1,
      anon_sym_COMMA,
    ACTIONS(403), 1,
      sym__newline,
    STATE(119), 1,
      aux_sym_input_constraints_repeat1,
  [2522] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(405), 1,
      anon_sym_COMMA,
    ACTIONS(407), 1,
      anon_sym_RPAREN,
    STATE(125), 1,
      aux_sym_error_args_repeat1,
  [2535] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(405), 1,
      anon_sym_COMMA,
    ACTIONS(409), 1,
      anon_sym_RPAREN,
    STATE(100), 1,
      aux_sym_error_args_repeat1,
  [2548] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(411), 2,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
  [2556] = 2,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(413), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2564] = 2,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(415), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2572] = 3,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(417), 1,
      aux_sym_guard_text_token1,
    STATE(92), 1,
      sym_guard_text,
  [2582] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(419), 2,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
  [2590] = 2,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(421), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2598] = 2,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(423), 2,
      aux_sym_description_text_token1,
      aux_sym_condition_token_token1,
  [2606] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(348), 2,
      anon_sym_COMMA,
      sym__newline,
  [2614] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(227), 1,
      sym_identifier,
  [2624] = 3,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(257), 1,
      aux_sym_guard_text_token1,
    STATE(80), 1,
      sym_step_text,
  [2634] = 3,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(425), 1,
      aux_sym_description_text_token1,
    STATE(216), 1,
      sym_edge_behavior_text,
  [2644] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(427), 1,
      anon_sym_RBRACE,
    STATE(47), 1,
      sym_literal_close,
  [2654] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(385), 2,
      anon_sym_COMMA,
      sym__newline,
  [2662] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(223), 1,
      sym_identifier,
  [2672] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(429), 2,
      anon_sym_COMMA,
      sym__newline,
  [2680] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(371), 2,
      anon_sym_COMMA,
      sym__newline,
  [2688] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(395), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [2696] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(240), 1,
      sym_identifier,
  [2706] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(431), 2,
      anon_sym_COMMA,
      sym__newline,
  [2714] = 3,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(257), 1,
      aux_sym_guard_text_token1,
    STATE(81), 1,
      sym_step_text,
  [2724] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(433), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2732] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(230), 1,
      sym_identifier,
  [2742] = 3,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(435), 1,
      aux_sym_guard_text_token1,
    STATE(111), 1,
      sym_edge_condition_text,
  [2752] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(133), 1,
      sym_identifier,
  [2762] = 2,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(437), 2,
      aux_sym_guard_text_token1,
      aux_sym_condition_prefix_token1,
  [2770] = 3,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(439), 1,
      aux_sym_description_text_token1,
    STATE(186), 1,
      sym_description_text,
  [2780] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(441), 2,
      anon_sym_COMMA,
      sym__newline,
  [2788] = 2,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(443), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2796] = 3,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(445), 1,
      aux_sym_description_text_token1,
    STATE(200), 1,
      sym_returns_text,
  [2806] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(228), 1,
      sym_identifier,
  [2816] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(343), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [2824] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(447), 2,
      anon_sym_COMMA,
      sym__newline,
  [2832] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(449), 1,
      sym__newline,
  [2839] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(451), 1,
      sym__newline,
  [2846] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(453), 1,
      anon_sym_EQ_EQ,
  [2853] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(455), 1,
      anon_sym_COLON,
  [2860] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(457), 1,
      ts_builtin_sym_end,
  [2867] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(459), 1,
      anon_sym_DOT,
  [2874] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(461), 1,
      anon_sym_LPAREN,
  [2881] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(463), 1,
      sym__newline,
  [2888] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(465), 1,
      sym__newline,
  [2895] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(467), 1,
      sym_type_name,
  [2902] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(469), 1,
      sym__newline,
  [2909] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(471), 1,
      sym_anlu_identifier,
  [2916] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(473), 1,
      anon_sym_RBRACK,
  [2923] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(475), 1,
      anon_sym_LBRACE,
  [2930] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(477), 1,
      sym__newline,
  [2937] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(479), 1,
      anon_sym_EQ_EQ,
  [2944] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(481), 1,
      anon_sym_RBRACK,
  [2951] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(483), 1,
      sym__newline,
  [2958] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(485), 1,
      sym__newline,
  [2965] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(487), 1,
      aux_sym_condition_token_token1,
  [2972] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(489), 1,
      sym__newline,
  [2979] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(491), 1,
      sym__newline,
  [2986] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(493), 1,
      anon_sym_RBRACK,
  [2993] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(495), 1,
      sym__newline,
  [3000] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(497), 1,
      sym_state_name,
  [3007] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(499), 1,
      sym_type_name,
  [3014] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(501), 1,
      sym__newline,
  [3021] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(503), 1,
      anon_sym_LBRACK,
  [3028] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(505), 1,
      sym__newline,
  [3035] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(507), 1,
      anon_sym_of,
  [3042] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(509), 1,
      sym__newline,
  [3049] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(511), 1,
      anon_sym_of,
  [3056] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(513), 1,
      sym__newline,
  [3063] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(515), 1,
      anon_sym_to,
  [3070] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(517), 1,
      anon_sym_LBRACE,
  [3077] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(519), 1,
      sym__newline,
  [3084] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(521), 1,
      sym_literal_content,
  [3091] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(523), 1,
      sym__newline,
  [3098] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(525), 1,
      sym__newline,
  [3105] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(527), 1,
      sym__newline,
  [3112] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(529), 1,
      anon_sym_LBRACE,
  [3119] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(531), 1,
      sym__newline,
  [3126] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(533), 1,
      sym__newline,
  [3133] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(535), 1,
      sym__newline,
  [3140] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(537), 1,
      sym__newline,
  [3147] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(539), 1,
      sym__newline,
  [3154] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(541), 1,
      sym__newline,
  [3161] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(543), 1,
      anon_sym_LPAREN,
  [3168] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(545), 1,
      sym__newline,
  [3175] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(547), 1,
      sym_anlu_identifier,
  [3182] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(549), 1,
      aux_sym_condition_prefix_token2,
  [3189] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(551), 1,
      anon_sym_EQ_EQ,
  [3196] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(553), 1,
      sym__newline,
  [3203] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(555), 1,
      anon_sym_RPAREN,
  [3210] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(557), 1,
      sym_version_string,
  [3217] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(559), 1,
      sym__newline,
  [3224] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(561), 1,
      sym_type_name,
  [3231] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(563), 1,
      sym__newline,
  [3238] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(565), 1,
      sym__newline,
  [3245] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(567), 1,
      anon_sym_RBRACK,
  [3252] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(569), 1,
      anon_sym_LBRACE,
  [3259] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(571), 1,
      sym_anlu_identifier,
  [3266] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(573), 1,
      anon_sym_LBRACE,
  [3273] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(575), 1,
      sym__newline,
  [3280] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(577), 1,
      sym__newline,
  [3287] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(579), 1,
      anon_sym_COLON,
  [3294] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(581), 1,
      sym_anlu_identifier,
  [3301] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(583), 1,
      sym__newline,
  [3308] = 2,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(585), 1,
      aux_sym_guard_text_token1,
  [3315] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(587), 1,
      anon_sym_LBRACE,
  [3322] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(589), 1,
      anon_sym_COLON,
  [3329] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(591), 1,
      sym__newline,
  [3336] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(593), 1,
      sym__newline,
  [3343] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(595), 1,
      sym__newline,
  [3350] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(597), 1,
      sym__newline,
  [3357] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(599), 1,
      anon_sym_LBRACK,
  [3364] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(601), 1,
      sym__newline,
  [3371] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(603), 1,
      sym__newline,
  [3378] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(605), 1,
      anon_sym_RPAREN,
  [3385] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(607), 1,
      sym_literal_content,
  [3392] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(609), 1,
      sym__newline,
  [3399] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(611), 1,
      sym__newline,
  [3406] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(613), 1,
      sym__newline,
  [3413] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(615), 1,
      sym__newline,
  [3420] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(617), 1,
      sym__newline,
  [3427] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(619), 1,
      sym__newline,
  [3434] = 2,
    ACTIONS(253), 1,
      sym_comment,
    ACTIONS(621), 1,
      aux_sym_guard_text_token1,
  [3441] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(623), 1,
      aux_sym_condition_token_token1,
  [3448] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(625), 1,
      anon_sym_RBRACK,
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
  [SMALL_STATE(14)] = 549,
  [SMALL_STATE(15)] = 577,
  [SMALL_STATE(16)] = 605,
  [SMALL_STATE(17)] = 637,
  [SMALL_STATE(18)] = 665,
  [SMALL_STATE(19)] = 693,
  [SMALL_STATE(20)] = 721,
  [SMALL_STATE(21)] = 747,
  [SMALL_STATE(22)] = 772,
  [SMALL_STATE(23)] = 797,
  [SMALL_STATE(24)] = 822,
  [SMALL_STATE(25)] = 847,
  [SMALL_STATE(26)] = 881,
  [SMALL_STATE(27)] = 911,
  [SMALL_STATE(28)] = 941,
  [SMALL_STATE(29)] = 971,
  [SMALL_STATE(30)] = 998,
  [SMALL_STATE(31)] = 1025,
  [SMALL_STATE(32)] = 1052,
  [SMALL_STATE(33)] = 1070,
  [SMALL_STATE(34)] = 1088,
  [SMALL_STATE(35)] = 1106,
  [SMALL_STATE(36)] = 1124,
  [SMALL_STATE(37)] = 1142,
  [SMALL_STATE(38)] = 1160,
  [SMALL_STATE(39)] = 1178,
  [SMALL_STATE(40)] = 1196,
  [SMALL_STATE(41)] = 1224,
  [SMALL_STATE(42)] = 1242,
  [SMALL_STATE(43)] = 1260,
  [SMALL_STATE(44)] = 1278,
  [SMALL_STATE(45)] = 1306,
  [SMALL_STATE(46)] = 1324,
  [SMALL_STATE(47)] = 1342,
  [SMALL_STATE(48)] = 1360,
  [SMALL_STATE(49)] = 1378,
  [SMALL_STATE(50)] = 1396,
  [SMALL_STATE(51)] = 1414,
  [SMALL_STATE(52)] = 1432,
  [SMALL_STATE(53)] = 1450,
  [SMALL_STATE(54)] = 1473,
  [SMALL_STATE(55)] = 1496,
  [SMALL_STATE(56)] = 1519,
  [SMALL_STATE(57)] = 1547,
  [SMALL_STATE(58)] = 1575,
  [SMALL_STATE(59)] = 1600,
  [SMALL_STATE(60)] = 1617,
  [SMALL_STATE(61)] = 1639,
  [SMALL_STATE(62)] = 1662,
  [SMALL_STATE(63)] = 1687,
  [SMALL_STATE(64)] = 1710,
  [SMALL_STATE(65)] = 1731,
  [SMALL_STATE(66)] = 1747,
  [SMALL_STATE(67)] = 1763,
  [SMALL_STATE(68)] = 1783,
  [SMALL_STATE(69)] = 1799,
  [SMALL_STATE(70)] = 1817,
  [SMALL_STATE(71)] = 1839,
  [SMALL_STATE(72)] = 1851,
  [SMALL_STATE(73)] = 1862,
  [SMALL_STATE(74)] = 1879,
  [SMALL_STATE(75)] = 1890,
  [SMALL_STATE(76)] = 1907,
  [SMALL_STATE(77)] = 1918,
  [SMALL_STATE(78)] = 1935,
  [SMALL_STATE(79)] = 1952,
  [SMALL_STATE(80)] = 1963,
  [SMALL_STATE(81)] = 1980,
  [SMALL_STATE(82)] = 1997,
  [SMALL_STATE(83)] = 2008,
  [SMALL_STATE(84)] = 2023,
  [SMALL_STATE(85)] = 2040,
  [SMALL_STATE(86)] = 2051,
  [SMALL_STATE(87)] = 2067,
  [SMALL_STATE(88)] = 2077,
  [SMALL_STATE(89)] = 2093,
  [SMALL_STATE(90)] = 2107,
  [SMALL_STATE(91)] = 2123,
  [SMALL_STATE(92)] = 2133,
  [SMALL_STATE(93)] = 2147,
  [SMALL_STATE(94)] = 2163,
  [SMALL_STATE(95)] = 2175,
  [SMALL_STATE(96)] = 2189,
  [SMALL_STATE(97)] = 2199,
  [SMALL_STATE(98)] = 2215,
  [SMALL_STATE(99)] = 2225,
  [SMALL_STATE(100)] = 2234,
  [SMALL_STATE(101)] = 2247,
  [SMALL_STATE(102)] = 2260,
  [SMALL_STATE(103)] = 2273,
  [SMALL_STATE(104)] = 2286,
  [SMALL_STATE(105)] = 2299,
  [SMALL_STATE(106)] = 2310,
  [SMALL_STATE(107)] = 2319,
  [SMALL_STATE(108)] = 2328,
  [SMALL_STATE(109)] = 2341,
  [SMALL_STATE(110)] = 2350,
  [SMALL_STATE(111)] = 2363,
  [SMALL_STATE(112)] = 2374,
  [SMALL_STATE(113)] = 2387,
  [SMALL_STATE(114)] = 2400,
  [SMALL_STATE(115)] = 2413,
  [SMALL_STATE(116)] = 2422,
  [SMALL_STATE(117)] = 2435,
  [SMALL_STATE(118)] = 2446,
  [SMALL_STATE(119)] = 2457,
  [SMALL_STATE(120)] = 2470,
  [SMALL_STATE(121)] = 2483,
  [SMALL_STATE(122)] = 2496,
  [SMALL_STATE(123)] = 2509,
  [SMALL_STATE(124)] = 2522,
  [SMALL_STATE(125)] = 2535,
  [SMALL_STATE(126)] = 2548,
  [SMALL_STATE(127)] = 2556,
  [SMALL_STATE(128)] = 2564,
  [SMALL_STATE(129)] = 2572,
  [SMALL_STATE(130)] = 2582,
  [SMALL_STATE(131)] = 2590,
  [SMALL_STATE(132)] = 2598,
  [SMALL_STATE(133)] = 2606,
  [SMALL_STATE(134)] = 2614,
  [SMALL_STATE(135)] = 2624,
  [SMALL_STATE(136)] = 2634,
  [SMALL_STATE(137)] = 2644,
  [SMALL_STATE(138)] = 2654,
  [SMALL_STATE(139)] = 2662,
  [SMALL_STATE(140)] = 2672,
  [SMALL_STATE(141)] = 2680,
  [SMALL_STATE(142)] = 2688,
  [SMALL_STATE(143)] = 2696,
  [SMALL_STATE(144)] = 2706,
  [SMALL_STATE(145)] = 2714,
  [SMALL_STATE(146)] = 2724,
  [SMALL_STATE(147)] = 2732,
  [SMALL_STATE(148)] = 2742,
  [SMALL_STATE(149)] = 2752,
  [SMALL_STATE(150)] = 2762,
  [SMALL_STATE(151)] = 2770,
  [SMALL_STATE(152)] = 2780,
  [SMALL_STATE(153)] = 2788,
  [SMALL_STATE(154)] = 2796,
  [SMALL_STATE(155)] = 2806,
  [SMALL_STATE(156)] = 2816,
  [SMALL_STATE(157)] = 2824,
  [SMALL_STATE(158)] = 2832,
  [SMALL_STATE(159)] = 2839,
  [SMALL_STATE(160)] = 2846,
  [SMALL_STATE(161)] = 2853,
  [SMALL_STATE(162)] = 2860,
  [SMALL_STATE(163)] = 2867,
  [SMALL_STATE(164)] = 2874,
  [SMALL_STATE(165)] = 2881,
  [SMALL_STATE(166)] = 2888,
  [SMALL_STATE(167)] = 2895,
  [SMALL_STATE(168)] = 2902,
  [SMALL_STATE(169)] = 2909,
  [SMALL_STATE(170)] = 2916,
  [SMALL_STATE(171)] = 2923,
  [SMALL_STATE(172)] = 2930,
  [SMALL_STATE(173)] = 2937,
  [SMALL_STATE(174)] = 2944,
  [SMALL_STATE(175)] = 2951,
  [SMALL_STATE(176)] = 2958,
  [SMALL_STATE(177)] = 2965,
  [SMALL_STATE(178)] = 2972,
  [SMALL_STATE(179)] = 2979,
  [SMALL_STATE(180)] = 2986,
  [SMALL_STATE(181)] = 2993,
  [SMALL_STATE(182)] = 3000,
  [SMALL_STATE(183)] = 3007,
  [SMALL_STATE(184)] = 3014,
  [SMALL_STATE(185)] = 3021,
  [SMALL_STATE(186)] = 3028,
  [SMALL_STATE(187)] = 3035,
  [SMALL_STATE(188)] = 3042,
  [SMALL_STATE(189)] = 3049,
  [SMALL_STATE(190)] = 3056,
  [SMALL_STATE(191)] = 3063,
  [SMALL_STATE(192)] = 3070,
  [SMALL_STATE(193)] = 3077,
  [SMALL_STATE(194)] = 3084,
  [SMALL_STATE(195)] = 3091,
  [SMALL_STATE(196)] = 3098,
  [SMALL_STATE(197)] = 3105,
  [SMALL_STATE(198)] = 3112,
  [SMALL_STATE(199)] = 3119,
  [SMALL_STATE(200)] = 3126,
  [SMALL_STATE(201)] = 3133,
  [SMALL_STATE(202)] = 3140,
  [SMALL_STATE(203)] = 3147,
  [SMALL_STATE(204)] = 3154,
  [SMALL_STATE(205)] = 3161,
  [SMALL_STATE(206)] = 3168,
  [SMALL_STATE(207)] = 3175,
  [SMALL_STATE(208)] = 3182,
  [SMALL_STATE(209)] = 3189,
  [SMALL_STATE(210)] = 3196,
  [SMALL_STATE(211)] = 3203,
  [SMALL_STATE(212)] = 3210,
  [SMALL_STATE(213)] = 3217,
  [SMALL_STATE(214)] = 3224,
  [SMALL_STATE(215)] = 3231,
  [SMALL_STATE(216)] = 3238,
  [SMALL_STATE(217)] = 3245,
  [SMALL_STATE(218)] = 3252,
  [SMALL_STATE(219)] = 3259,
  [SMALL_STATE(220)] = 3266,
  [SMALL_STATE(221)] = 3273,
  [SMALL_STATE(222)] = 3280,
  [SMALL_STATE(223)] = 3287,
  [SMALL_STATE(224)] = 3294,
  [SMALL_STATE(225)] = 3301,
  [SMALL_STATE(226)] = 3308,
  [SMALL_STATE(227)] = 3315,
  [SMALL_STATE(228)] = 3322,
  [SMALL_STATE(229)] = 3329,
  [SMALL_STATE(230)] = 3336,
  [SMALL_STATE(231)] = 3343,
  [SMALL_STATE(232)] = 3350,
  [SMALL_STATE(233)] = 3357,
  [SMALL_STATE(234)] = 3364,
  [SMALL_STATE(235)] = 3371,
  [SMALL_STATE(236)] = 3378,
  [SMALL_STATE(237)] = 3385,
  [SMALL_STATE(238)] = 3392,
  [SMALL_STATE(239)] = 3399,
  [SMALL_STATE(240)] = 3406,
  [SMALL_STATE(241)] = 3413,
  [SMALL_STATE(242)] = 3420,
  [SMALL_STATE(243)] = 3427,
  [SMALL_STATE(244)] = 3434,
  [SMALL_STATE(245)] = 3441,
  [SMALL_STATE(246)] = 3448,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT_EXTRA(),
  [5] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0, 0, 0),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(143),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(212),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(94),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(102),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(169),
  [17] = {.entry = {.count = 1, .reusable = true}}, SHIFT(183),
  [19] = {.entry = {.count = 1, .reusable = true}}, SHIFT(185),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(214),
  [23] = {.entry = {.count = 1, .reusable = true}}, SHIFT(233),
  [25] = {.entry = {.count = 1, .reusable = true}}, SHIFT(134),
  [27] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [29] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0),
  [31] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(143),
  [34] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(212),
  [37] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(94),
  [40] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(102),
  [43] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(169),
  [46] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(183),
  [49] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(185),
  [52] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(214),
  [55] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(233),
  [58] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(134),
  [61] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(2),
  [64] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1, 0, 0),
  [66] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [68] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_block, 1, 0, 0),
  [70] = {.entry = {.count = 1, .reusable = true}}, SHIFT(151),
  [72] = {.entry = {.count = 1, .reusable = true}}, SHIFT(231),
  [74] = {.entry = {.count = 1, .reusable = true}}, SHIFT(232),
  [76] = {.entry = {.count = 1, .reusable = true}}, SHIFT(234),
  [78] = {.entry = {.count = 1, .reusable = true}}, SHIFT(154),
  [80] = {.entry = {.count = 1, .reusable = true}}, SHIFT(93),
  [82] = {.entry = {.count = 1, .reusable = true}}, SHIFT(176),
  [84] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_block, 2, 0, 0),
  [86] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0),
  [88] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(151),
  [91] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(231),
  [94] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(232),
  [97] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(234),
  [100] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(154),
  [103] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(93),
  [106] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(176),
  [109] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_inputs_section, 3, 0, 11),
  [111] = {.entry = {.count = 1, .reusable = true}}, SHIFT(177),
  [113] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guards_section, 3, 0, 11),
  [115] = {.entry = {.count = 1, .reusable = true}}, SHIFT(244),
  [117] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_cases_section, 3, 0, 11),
  [119] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_guards_section_repeat1, 2, 0, 0),
  [121] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_guards_section_repeat1, 2, 0, 0), SHIFT_REPEAT(244),
  [124] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_edge_cases_section_repeat1, 2, 0, 0),
  [126] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_edge_cases_section_repeat1, 2, 0, 0), SHIFT_REPEAT(244),
  [129] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_inputs_section_repeat1, 2, 0, 0),
  [131] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_inputs_section_repeat1, 2, 0, 0), SHIFT_REPEAT(177),
  [134] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_section, 3, 0, 11),
  [136] = {.entry = {.count = 1, .reusable = true}}, SHIFT(163),
  [138] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_case_item, 5, 0, 28),
  [140] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_item, 6, 0, 21),
  [142] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_logic_section_repeat1, 2, 0, 0),
  [144] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_logic_section_repeat1, 2, 0, 0), SHIFT_REPEAT(163),
  [147] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_item, 3, 0, 18),
  [149] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_item, 5, 0, 21),
  [151] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_item, 5, 0, 24),
  [153] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_item, 4, 0, 22),
  [155] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_header, 4, 0, 1),
  [157] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_purpose_section, 3, 0, 10),
  [159] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_returns_section, 3, 0, 12),
  [161] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_section, 3, 0, 13),
  [163] = {.entry = {.count = 1, .reusable = true}}, SHIFT(209),
  [165] = {.entry = {.count = 1, .reusable = false}}, SHIFT(71),
  [167] = {.entry = {.count = 1, .reusable = true}}, SHIFT(99),
  [169] = {.entry = {.count = 1, .reusable = true}}, SHIFT(106),
  [171] = {.entry = {.count = 1, .reusable = false}}, SHIFT(107),
  [173] = {.entry = {.count = 1, .reusable = true}}, SHIFT(98),
  [175] = {.entry = {.count = 1, .reusable = true}}, SHIFT(91),
  [177] = {.entry = {.count = 1, .reusable = true}}, SHIFT(187),
  [179] = {.entry = {.count = 1, .reusable = true}}, SHIFT(189),
  [181] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_directive, 1, 0, 0),
  [183] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_imports_directive, 3, 0, 4),
  [185] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_block, 2, 0, 0),
  [187] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_close, 2, 0, 0),
  [189] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_block, 2, 0, 0),
  [191] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_block, 3, 0, 0),
  [193] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_close, 2, 0, 0),
  [195] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_close, 2, 0, 0),
  [197] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_block, 2, 0, 0),
  [199] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_block, 3, 0, 0),
  [201] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_close, 2, 0, 0),
  [203] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_block, 3, 0, 0),
  [205] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_block, 3, 0, 0),
  [207] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_block, 3, 0, 6),
  [209] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_block, 2, 0, 0),
  [211] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_close, 2, 0, 0),
  [213] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_module_directive, 3, 0, 1),
  [215] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_version_directive, 3, 0, 2),
  [217] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_target_directive, 3, 0, 3),
  [219] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_text, 1, 0, 0),
  [221] = {.entry = {.count = 1, .reusable = false}}, SHIFT(59),
  [223] = {.entry = {.count = 1, .reusable = true}}, SHIFT(59),
  [225] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0),
  [227] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0), SHIFT_REPEAT(59),
  [230] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0), SHIFT_REPEAT(59),
  [233] = {.entry = {.count = 1, .reusable = true}}, SHIFT(71),
  [235] = {.entry = {.count = 1, .reusable = true}}, SHIFT(175),
  [237] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0), SHIFT_REPEAT(71),
  [240] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0),
  [242] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0), SHIFT_REPEAT(177),
  [245] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_token, 1, 0, 0),
  [247] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition_token, 1, 0, 0),
  [249] = {.entry = {.count = 1, .reusable = false}}, SHIFT(138),
  [251] = {.entry = {.count = 1, .reusable = true}}, SHIFT(206),
  [253] = {.entry = {.count = 1, .reusable = false}}, SHIFT_EXTRA(),
  [255] = {.entry = {.count = 1, .reusable = false}}, SHIFT(182),
  [257] = {.entry = {.count = 1, .reusable = false}}, SHIFT(115),
  [259] = {.entry = {.count = 1, .reusable = false}}, SHIFT(54),
  [261] = {.entry = {.count = 1, .reusable = true}}, SHIFT(235),
  [263] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_test_block_repeat1, 2, 0, 0), SHIFT_REPEAT(71),
  [266] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_test_block_repeat1, 2, 0, 0),
  [268] = {.entry = {.count = 1, .reusable = true}}, SHIFT(152),
  [270] = {.entry = {.count = 1, .reusable = false}}, SHIFT(201),
  [272] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 1, 0, 0),
  [274] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 6, 0, 21),
  [276] = {.entry = {.count = 1, .reusable = false}}, SHIFT(190),
  [278] = {.entry = {.count = 1, .reusable = false}}, SHIFT(193),
  [280] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 5, 0, 21),
  [282] = {.entry = {.count = 1, .reusable = false}}, SHIFT(172),
  [284] = {.entry = {.count = 1, .reusable = false}}, SHIFT(179),
  [286] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_header, 5, 0, 1),
  [288] = {.entry = {.count = 1, .reusable = true}}, SHIFT(245),
  [290] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 1, 0, 19),
  [292] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 5, 0, 15),
  [294] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 2, 0, 23),
  [296] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 3, 0, 26),
  [298] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 4, 0, 15),
  [300] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_header, 4, 0, 1),
  [302] = {.entry = {.count = 1, .reusable = true}}, SHIFT(60),
  [304] = {.entry = {.count = 1, .reusable = true}}, SHIFT(82),
  [306] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_list_type, 3, 0, 20),
  [308] = {.entry = {.count = 1, .reusable = true}}, SHIFT(18),
  [310] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_property_block_repeat1, 2, 0, 0),
  [312] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_property_block_repeat1, 2, 0, 0), SHIFT_REPEAT(193),
  [315] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_primitive_type, 1, 0, 0),
  [317] = {.entry = {.count = 1, .reusable = true}}, SHIFT(132),
  [319] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [321] = {.entry = {.count = 1, .reusable = true}}, SHIFT(207),
  [323] = {.entry = {.count = 1, .reusable = true}}, SHIFT(144),
  [325] = {.entry = {.count = 1, .reusable = true}}, SHIFT(242),
  [327] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_invariant_block_repeat1, 2, 0, 0),
  [329] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_invariant_block_repeat1, 2, 0, 0), SHIFT_REPEAT(179),
  [332] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_map_type, 5, 0, 29),
  [334] = {.entry = {.count = 1, .reusable = true}}, SHIFT(74),
  [336] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_custom_type, 1, 0, 0),
  [338] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_value, 1, 0, 0),
  [340] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_error_args_repeat1, 2, 0, 0), SHIFT_REPEAT(83),
  [343] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_error_args_repeat1, 2, 0, 0),
  [345] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_import_list_repeat1, 2, 0, 0), SHIFT_REPEAT(149),
  [348] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_import_list_repeat1, 2, 0, 0),
  [350] = {.entry = {.count = 1, .reusable = true}}, SHIFT(103),
  [352] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_list, 2, 0, 0),
  [354] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_spec, 1, 0, 0),
  [356] = {.entry = {.count = 1, .reusable = true}}, SHIFT(157),
  [358] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_quoted_string, 1, 0, 0),
  [360] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_boolean, 1, 0, 0),
  [362] = {.entry = {.count = 1, .reusable = true}}, SHIFT(44),
  [364] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_args, 1, 0, 0),
  [366] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_text, 1, 0, 0),
  [368] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_depends_list_repeat1, 2, 0, 0), SHIFT_REPEAT(103),
  [371] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_depends_list_repeat1, 2, 0, 0),
  [373] = {.entry = {.count = 1, .reusable = true}}, SHIFT(149),
  [375] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_import_list, 2, 0, 0),
  [377] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_field_constraints, 1, 0, 0),
  [379] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_args, 2, 0, 0),
  [381] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_step_text, 1, 0, 0),
  [383] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_import_list, 1, 0, 0),
  [385] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_input_constraints_repeat1, 2, 0, 0),
  [387] = {.entry = {.count = 1, .reusable = true}}, SHIFT(69),
  [389] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_input_constraints_repeat1, 2, 0, 0), SHIFT_REPEAT(60),
  [392] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_test_args_repeat1, 2, 0, 0), SHIFT_REPEAT(44),
  [395] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_test_args_repeat1, 2, 0, 0),
  [397] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_list, 1, 0, 0),
  [399] = {.entry = {.count = 1, .reusable = true}}, SHIFT(166),
  [401] = {.entry = {.count = 1, .reusable = true}}, SHIFT(167),
  [403] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_constraints, 1, 0, 0),
  [405] = {.entry = {.count = 1, .reusable = true}}, SHIFT(83),
  [407] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_args, 1, 0, 0),
  [409] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_args, 2, 0, 0),
  [411] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_assertion, 4, 0, 16),
  [413] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_property_assertion, 2, 0, 5),
  [415] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_invariant_assertion, 2, 0, 5),
  [417] = {.entry = {.count = 1, .reusable = false}}, SHIFT(109),
  [419] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_header, 6, 0, 17),
  [421] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_property_header, 6, 0, 17),
  [423] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_arrow, 1, 0, 0),
  [425] = {.entry = {.count = 1, .reusable = false}}, SHIFT(215),
  [427] = {.entry = {.count = 1, .reusable = true}}, SHIFT(159),
  [429] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_reference, 3, 0, 0),
  [431] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_reference, 1, 0, 0),
  [433] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_condition_text, 1, 0, 0),
  [435] = {.entry = {.count = 1, .reusable = false}}, SHIFT(146),
  [437] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_state_prefix, 3, 0, 25),
  [439] = {.entry = {.count = 1, .reusable = false}}, SHIFT(184),
  [441] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_constraint_pair, 3, 0, 30),
  [443] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_invariant_header, 4, 0, 8),
  [445] = {.entry = {.count = 1, .reusable = false}}, SHIFT(196),
  [447] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_spec, 2, 0, 0),
  [449] = {.entry = {.count = 1, .reusable = true}}, SHIFT(20),
  [451] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [453] = {.entry = {.count = 1, .reusable = true}}, SHIFT(40),
  [455] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [457] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [459] = {.entry = {.count = 1, .reusable = true}}, SHIFT(62),
  [461] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [463] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [465] = {.entry = {.count = 1, .reusable = true}}, SHIFT(85),
  [467] = {.entry = {.count = 1, .reusable = true}}, SHIFT(192),
  [469] = {.entry = {.count = 1, .reusable = true}}, SHIFT(79),
  [471] = {.entry = {.count = 1, .reusable = true}}, SHIFT(217),
  [473] = {.entry = {.count = 1, .reusable = true}}, SHIFT(140),
  [475] = {.entry = {.count = 1, .reusable = true}}, SHIFT(195),
  [477] = {.entry = {.count = 1, .reusable = true}}, SHIFT(43),
  [479] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_call, 4, 0, 14),
  [481] = {.entry = {.count = 1, .reusable = true}}, SHIFT(198),
  [483] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [485] = {.entry = {.count = 1, .reusable = true}}, SHIFT(66),
  [487] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_bullet, 1, 0, 0),
  [489] = {.entry = {.count = 1, .reusable = true}}, SHIFT(153),
  [491] = {.entry = {.count = 1, .reusable = true}}, SHIFT(128),
  [493] = {.entry = {.count = 1, .reusable = true}}, SHIFT(218),
  [495] = {.entry = {.count = 1, .reusable = true}}, SHIFT(237),
  [497] = {.entry = {.count = 1, .reusable = true}}, SHIFT(246),
  [499] = {.entry = {.count = 1, .reusable = true}}, SHIFT(122),
  [501] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_description_text, 1, 0, 0),
  [503] = {.entry = {.count = 1, .reusable = true}}, SHIFT(219),
  [505] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [507] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [509] = {.entry = {.count = 1, .reusable = true}}, SHIFT(33),
  [511] = {.entry = {.count = 1, .reusable = true}}, SHIFT(30),
  [513] = {.entry = {.count = 1, .reusable = true}}, SHIFT(49),
  [515] = {.entry = {.count = 1, .reusable = true}}, SHIFT(31),
  [517] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_extends_clause, 2, 0, 7),
  [519] = {.entry = {.count = 1, .reusable = true}}, SHIFT(127),
  [521] = {.entry = {.count = 1, .reusable = true}}, SHIFT(137),
  [523] = {.entry = {.count = 1, .reusable = true}}, SHIFT(76),
  [525] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_returns_text, 1, 0, 0),
  [527] = {.entry = {.count = 1, .reusable = true}}, SHIFT(72),
  [529] = {.entry = {.count = 1, .reusable = true}}, SHIFT(222),
  [531] = {.entry = {.count = 1, .reusable = true}}, SHIFT(126),
  [533] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [535] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_text, 1, 0, 0),
  [537] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [539] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_spec, 1, 2, 0),
  [541] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_spec, 1, 1, 0),
  [543] = {.entry = {.count = 1, .reusable = true}}, SHIFT(64),
  [545] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [547] = {.entry = {.count = 1, .reusable = true}}, SHIFT(170),
  [549] = {.entry = {.count = 1, .reusable = true}}, SHIFT(226),
  [551] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_call, 3, 0, 14),
  [553] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [555] = {.entry = {.count = 1, .reusable = true}}, SHIFT(173),
  [557] = {.entry = {.count = 1, .reusable = true}}, SHIFT(241),
  [559] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 2, 0, 19),
  [561] = {.entry = {.count = 1, .reusable = true}}, SHIFT(220),
  [563] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_behavior_text, 1, 0, 0),
  [565] = {.entry = {.count = 1, .reusable = true}}, SHIFT(14),
  [567] = {.entry = {.count = 1, .reusable = true}}, SHIFT(165),
  [569] = {.entry = {.count = 1, .reusable = true}}, SHIFT(225),
  [571] = {.entry = {.count = 1, .reusable = true}}, SHIFT(174),
  [573] = {.entry = {.count = 1, .reusable = true}}, SHIFT(178),
  [575] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [577] = {.entry = {.count = 1, .reusable = true}}, SHIFT(130),
  [579] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [581] = {.entry = {.count = 1, .reusable = true}}, SHIFT(180),
  [583] = {.entry = {.count = 1, .reusable = true}}, SHIFT(131),
  [585] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_prefix, 3, 0, 0),
  [587] = {.entry = {.count = 1, .reusable = true}}, SHIFT(181),
  [589] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [591] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 3, 0, 23),
  [593] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_output_binding, 2, 0, 27),
  [595] = {.entry = {.count = 1, .reusable = true}}, SHIFT(68),
  [597] = {.entry = {.count = 1, .reusable = true}}, SHIFT(65),
  [599] = {.entry = {.count = 1, .reusable = true}}, SHIFT(224),
  [601] = {.entry = {.count = 1, .reusable = true}}, SHIFT(118),
  [603] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_call, 3, 0, 31),
  [605] = {.entry = {.count = 1, .reusable = true}}, SHIFT(239),
  [607] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_header, 4, 0, 9),
  [609] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 4, 0, 26),
  [611] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_call, 4, 0, 31),
  [613] = {.entry = {.count = 1, .reusable = true}}, SHIFT(50),
  [615] = {.entry = {.count = 1, .reusable = true}}, SHIFT(51),
  [617] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_target_name, 1, 0, 0),
  [619] = {.entry = {.count = 1, .reusable = true}}, SHIFT(52),
  [621] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_bullet, 1, 0, 0),
  [623] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arrow, 1, 0, 0),
  [625] = {.entry = {.count = 1, .reusable = true}}, SHIFT(150),
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
