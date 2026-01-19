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
#define STATE_COUNT 246
#define LARGE_STATE_COUNT 2
#define SYMBOL_COUNT 168
#define ALIAS_COUNT 0
#define TOKEN_COUNT 77
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
  sym_step_text = 38,
  aux_sym_returns_section_token1 = 39,
  aux_sym_depends_section_token1 = 40,
  aux_sym_edge_cases_section_token1 = 41,
  anon_sym_ATtype = 42,
  anon_sym_LBRACE = 43,
  anon_sym_extends = 44,
  sym_type_name = 45,
  anon_sym_RBRACE = 46,
  anon_sym_ATtest = 47,
  anon_sym_EQ_EQ = 48,
  anon_sym_ATinvariant = 49,
  anon_sym_ATproperty = 50,
  sym_expression_text = 51,
  anon_sym_ATliteral = 52,
  anon_sym_QMARK = 53,
  anon_sym_number = 54,
  anon_sym_string = 55,
  anon_sym_boolean = 56,
  anon_sym_void = 57,
  anon_sym_any = 58,
  anon_sym_list = 59,
  anon_sym_of = 60,
  anon_sym_map = 61,
  anon_sym_to = 62,
  sym_number = 63,
  aux_sym_quoted_string_token1 = 64,
  aux_sym_quoted_string_token2 = 65,
  anon_sym_true = 66,
  anon_sym_false = 67,
  anon_sym_True = 68,
  anon_sym_False = 69,
  anon_sym_u2022 = 70,
  anon_sym_DASH = 71,
  anon_sym_STAR = 72,
  anon_sym_u2192 = 73,
  anon_sym_DASH_GT = 74,
  sym__newline = 75,
  sym_literal_content = 76,
  sym_source_file = 77,
  sym_directive = 78,
  sym_module_directive = 79,
  sym_version_directive = 80,
  sym_target_directive = 81,
  sym_imports_directive = 82,
  sym_target_name = 83,
  sym_import_list = 84,
  sym_anlu_block = 85,
  sym_anlu_header = 86,
  sym_purpose_section = 87,
  sym_description_text = 88,
  sym_inputs_section = 89,
  sym_input_item = 90,
  sym_input_constraints = 91,
  sym_guards_section = 92,
  sym_guard_item = 93,
  sym_guard_text = 94,
  sym_error_spec = 95,
  sym_error_call = 96,
  sym_error_args = 97,
  sym_error_text = 98,
  sym_logic_section = 99,
  sym_logic_item = 100,
  sym_logic_step = 101,
  sym_state_prefix = 102,
  sym_condition_prefix = 103,
  sym_condition_text = 104,
  sym_condition_token = 105,
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
  [243] = 176,
  [244] = 142,
  [245] = 245,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(207);
      ADVANCE_MAP(
        '\n', 343,
        '\r', 1,
        '"', 6,
        '#', 211,
        '\'', 18,
        '(', 239,
        ')', 240,
        '*', 340,
        ',', 221,
        '-', 339,
        '.', 242,
        ':', 231,
        '=', 288,
        '?', 316,
        '@', 65,
        'E', 160,
        'F', 30,
        'L', 179,
        'P', 195,
        'R', 163,
        'T', 111,
        '[', 222,
        ']', 224,
        'a', 84,
        'b', 99,
        'e', 152,
        'f', 38,
        'l', 67,
        'm', 31,
        'n', 97,
        'o', 61,
        'p', 155,
        'r', 29,
        's', 141,
        't', 93,
        'v', 95,
        '{', 304,
        '}', 307,
        0x2022, 338,
        0x2192, 341,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(0);
      if (('+' <= lookahead && lookahead <= '/')) ADVANCE(291);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(164);
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(196);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(170);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(289);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(243);
      END_STATE();
    case 1:
      if (lookahead == '\n') ADVANCE(343);
      END_STATE();
    case 2:
      ADVANCE_MAP(
        '\n', 343,
        '\r', 1,
        '"', 6,
        '#', 211,
        '\'', 18,
        ')', 240,
        '-', 28,
        'F', 249,
        'T', 271,
        'f', 251,
        't', 274,
        0x2192, 341,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(326);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 3:
      ADVANCE_MAP(
        '"', 6,
        '#', 211,
        '\'', 18,
        ')', 240,
        '*', 340,
        '-', 339,
        '}', 307,
        0x2022, 338,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(3);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 4:
      if (lookahead == '"') ADVANCE(6);
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '\'') ADVANCE(18);
      if (lookahead == '-') ADVANCE(201);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(4);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(326);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 5:
      if (lookahead == '"') ADVANCE(6);
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '\'') ADVANCE(18);
      if (lookahead == 'o') ADVANCE(269);
      if (lookahead == 'r') ADVANCE(258);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(5);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 6:
      if (lookahead == '"') ADVANCE(328);
      if (lookahead != 0) ADVANCE(6);
      END_STATE();
    case 7:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == '[') ADVANCE(222);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(7);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(225);
      END_STATE();
    case 8:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == 'a') ADVANCE(265);
      if (lookahead == 'n') ADVANCE(267);
      if (lookahead == 'o') ADVANCE(272);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(8);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(289);
      if (lookahead == '(' ||
          lookahead == ')' ||
          lookahead == '[' ||
          lookahead == ']') ADVANCE(290);
      if (lookahead == '*' ||
          lookahead == '+' ||
          lookahead == '-' ||
          lookahead == '/') ADVANCE(291);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(286);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 9:
      if (lookahead == '#') ADVANCE(211);
      if (lookahead == 'a') ADVANCE(265);
      if (lookahead == 'n') ADVANCE(267);
      if (lookahead == 'o') ADVANCE(272);
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(9);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(283);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(289);
      if (lookahead == '(' ||
          lookahead == ')' ||
          lookahead == '[' ||
          lookahead == ']') ADVANCE(290);
      if (lookahead == '*' ||
          lookahead == '+' ||
          lookahead == '-' ||
          lookahead == '/') ADVANCE(291);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(286);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 10:
      ADVANCE_MAP(
        '#', 211,
        'a', 89,
        'b', 99,
        'l', 66,
        'm', 31,
        'n', 146,
        's', 141,
        'v', 95,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(10);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(19);
      if (('A' <= lookahead && lookahead <= 'Z')) ADVANCE(306);
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
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(244);
      END_STATE();
    case 13:
      if (lookahead == '#') ADVANCE(209);
      if (lookahead == '-') ADVANCE(199);
      if (lookahead == '[') ADVANCE(223);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(13);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(298);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(299);
      END_STATE();
    case 14:
      if (lookahead == '#') ADVANCE(209);
      if (lookahead == '-') ADVANCE(199);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(14);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(298);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(299);
      END_STATE();
    case 15:
      if (lookahead == '#') ADVANCE(209);
      if (lookahead == '-') ADVANCE(199);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(15);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(299);
      END_STATE();
    case 16:
      if (lookahead == '#') ADVANCE(208);
      if (lookahead == '}') ADVANCE(307);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(313);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n') ADVANCE(314);
      END_STATE();
    case 17:
      if (lookahead == '#') ADVANCE(210);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(237);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(238);
      END_STATE();
    case 18:
      if (lookahead == '\'') ADVANCE(329);
      if (lookahead != 0) ADVANCE(18);
      END_STATE();
    case 19:
      if (lookahead == '.') ADVANCE(203);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(19);
      END_STATE();
    case 20:
      if (lookahead == ':') ADVANCE(241);
      END_STATE();
    case 21:
      if (lookahead == ':') ADVANCE(236);
      END_STATE();
    case 22:
      if (lookahead == ':') ADVANCE(230);
      END_STATE();
    case 23:
      if (lookahead == ':') ADVANCE(226);
      END_STATE();
    case 24:
      if (lookahead == ':') ADVANCE(300);
      END_STATE();
    case 25:
      if (lookahead == ':') ADVANCE(301);
      END_STATE();
    case 26:
      if (lookahead == ':') ADVANCE(302);
      END_STATE();
    case 27:
      if (lookahead == '=') ADVANCE(309);
      END_STATE();
    case 28:
      if (lookahead == '>') ADVANCE(342);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(326);
      END_STATE();
    case 29:
      if (lookahead == 'E') ADVANCE(194);
      if (lookahead == 'e') ADVANCE(110);
      if (lookahead == 'u') ADVANCE(128);
      END_STATE();
    case 30:
      if (lookahead == 'a') ADVANCE(78);
      END_STATE();
    case 31:
      if (lookahead == 'a') ADVANCE(104);
      END_STATE();
    case 32:
      if (lookahead == 'a') ADVANCE(112);
      if (lookahead == 'e') ADVANCE(129);
      if (lookahead == 'y') ADVANCE(107);
      END_STATE();
    case 33:
      if (lookahead == 'a') ADVANCE(76);
      END_STATE();
    case 34:
      if (lookahead == 'a') ADVANCE(77);
      END_STATE();
    case 35:
      if (lookahead == 'a') ADVANCE(86);
      END_STATE();
    case 36:
      if (lookahead == 'a') ADVANCE(91);
      END_STATE();
    case 37:
      if (lookahead == 'a') ADVANCE(117);
      END_STATE();
    case 38:
      if (lookahead == 'a') ADVANCE(81);
      END_STATE();
    case 39:
      if (lookahead == 'b') ADVANCE(58);
      END_STATE();
    case 40:
      if (lookahead == 'c') ADVANCE(118);
      END_STATE();
    case 41:
      if (lookahead == 'd') ADVANCE(292);
      if (lookahead == 'y') ADVANCE(321);
      END_STATE();
    case 42:
      if (lookahead == 'd') ADVANCE(320);
      END_STATE();
    case 43:
      if (lookahead == 'd') ADVANCE(232);
      END_STATE();
    case 44:
      if (lookahead == 'd') ADVANCE(150);
      END_STATE();
    case 45:
      if (lookahead == 'd') ADVANCE(124);
      END_STATE();
    case 46:
      if (lookahead == 'e') ADVANCE(334);
      END_STATE();
    case 47:
      if (lookahead == 'e') ADVANCE(330);
      END_STATE();
    case 48:
      if (lookahead == 'e') ADVANCE(303);
      END_STATE();
    case 49:
      if (lookahead == 'e') ADVANCE(336);
      END_STATE();
    case 50:
      if (lookahead == 'e') ADVANCE(332);
      END_STATE();
    case 51:
      if (lookahead == 'e') ADVANCE(212);
      END_STATE();
    case 52:
      if (lookahead == 'e') ADVANCE(90);
      END_STATE();
    case 53:
      if (lookahead == 'e') ADVANCE(35);
      END_STATE();
    case 54:
      if (lookahead == 'e') ADVANCE(114);
      END_STATE();
    case 55:
      if (lookahead == 'e') ADVANCE(123);
      END_STATE();
    case 56:
      if (lookahead == 'e') ADVANCE(43);
      END_STATE();
    case 57:
      if (lookahead == 'e') ADVANCE(122);
      END_STATE();
    case 58:
      if (lookahead == 'e') ADVANCE(113);
      END_STATE();
    case 59:
      if (lookahead == 'e') ADVANCE(137);
      END_STATE();
    case 60:
      if (lookahead == 'e') ADVANCE(120);
      END_STATE();
    case 61:
      if (lookahead == 'f') ADVANCE(323);
      if (lookahead == 'p') ADVANCE(142);
      if (lookahead == 'r') ADVANCE(294);
      END_STATE();
    case 62:
      if (lookahead == 'g') ADVANCE(318);
      END_STATE();
    case 63:
      if (lookahead == 'g') ADVANCE(59);
      END_STATE();
    case 64:
      if (lookahead == 'h') ADVANCE(101);
      END_STATE();
    case 65:
      if (lookahead == 'i') ADVANCE(83);
      if (lookahead == 'l') ADVANCE(71);
      if (lookahead == 'm') ADVANCE(94);
      if (lookahead == 'p') ADVANCE(116);
      if (lookahead == 't') ADVANCE(32);
      if (lookahead == 'v') ADVANCE(54);
      END_STATE();
    case 66:
      if (lookahead == 'i') ADVANCE(126);
      END_STATE();
    case 67:
      if (lookahead == 'i') ADVANCE(126);
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(171);
      END_STATE();
    case 68:
      if (lookahead == 'i') ADVANCE(42);
      END_STATE();
    case 69:
      if (lookahead == 'i') ADVANCE(88);
      END_STATE();
    case 70:
      if (lookahead == 'i') ADVANCE(108);
      END_STATE();
    case 71:
      if (lookahead == 'i') ADVANCE(145);
      END_STATE();
    case 72:
      if (lookahead == 'i') ADVANCE(98);
      END_STATE();
    case 73:
      if (lookahead == 'i') ADVANCE(121);
      END_STATE();
    case 74:
      if (lookahead == 'i') ADVANCE(103);
      END_STATE();
    case 75:
      if (lookahead == 'i') ADVANCE(36);
      END_STATE();
    case 76:
      if (lookahead == 'l') ADVANCE(315);
      END_STATE();
    case 77:
      if (lookahead == 'l') ADVANCE(234);
      END_STATE();
    case 78:
      if (lookahead == 'l') ADVANCE(127);
      END_STATE();
    case 79:
      if (lookahead == 'l') ADVANCE(53);
      END_STATE();
    case 80:
      if (lookahead == 'l') ADVANCE(51);
      END_STATE();
    case 81:
      if (lookahead == 'l') ADVANCE(130);
      END_STATE();
    case 82:
      if (lookahead == 'm') ADVANCE(39);
      END_STATE();
    case 83:
      if (lookahead == 'm') ADVANCE(106);
      if (lookahead == 'n') ADVANCE(151);
      END_STATE();
    case 84:
      if (lookahead == 'n') ADVANCE(41);
      END_STATE();
    case 85:
      if (lookahead == 'n') ADVANCE(218);
      END_STATE();
    case 86:
      if (lookahead == 'n') ADVANCE(319);
      END_STATE();
    case 87:
      if (lookahead == 'n') ADVANCE(213);
      END_STATE();
    case 88:
      if (lookahead == 'n') ADVANCE(62);
      END_STATE();
    case 89:
      if (lookahead == 'n') ADVANCE(153);
      END_STATE();
    case 90:
      if (lookahead == 'n') ADVANCE(45);
      END_STATE();
    case 91:
      if (lookahead == 'n') ADVANCE(139);
      END_STATE();
    case 92:
      if (lookahead == 'n') ADVANCE(34);
      END_STATE();
    case 93:
      if (lookahead == 'o') ADVANCE(325);
      if (lookahead == 'r') ADVANCE(148);
      if (lookahead == 'y') ADVANCE(105);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(165);
      END_STATE();
    case 94:
      if (lookahead == 'o') ADVANCE(44);
      END_STATE();
    case 95:
      if (lookahead == 'o') ADVANCE(68);
      END_STATE();
    case 96:
      if (lookahead == 'o') ADVANCE(79);
      END_STATE();
    case 97:
      if (lookahead == 'o') ADVANCE(132);
      if (lookahead == 'u') ADVANCE(82);
      END_STATE();
    case 98:
      if (lookahead == 'o') ADVANCE(92);
      END_STATE();
    case 99:
      if (lookahead == 'o') ADVANCE(96);
      END_STATE();
    case 100:
      if (lookahead == 'o') ADVANCE(109);
      END_STATE();
    case 101:
      if (lookahead == 'o') ADVANCE(85);
      END_STATE();
    case 102:
      if (lookahead == 'o') ADVANCE(119);
      END_STATE();
    case 103:
      if (lookahead == 'o') ADVANCE(87);
      END_STATE();
    case 104:
      if (lookahead == 'p') ADVANCE(324);
      END_STATE();
    case 105:
      if (lookahead == 'p') ADVANCE(55);
      END_STATE();
    case 106:
      if (lookahead == 'p') ADVANCE(102);
      END_STATE();
    case 107:
      if (lookahead == 'p') ADVANCE(48);
      END_STATE();
    case 108:
      if (lookahead == 'p') ADVANCE(140);
      END_STATE();
    case 109:
      if (lookahead == 'p') ADVANCE(60);
      END_STATE();
    case 110:
      if (lookahead == 'q') ADVANCE(149);
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(198);
      END_STATE();
    case 111:
      if (lookahead == 'r') ADVANCE(147);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(165);
      END_STATE();
    case 112:
      if (lookahead == 'r') ADVANCE(63);
      END_STATE();
    case 113:
      if (lookahead == 'r') ADVANCE(317);
      END_STATE();
    case 114:
      if (lookahead == 'r') ADVANCE(131);
      END_STATE();
    case 115:
      if (lookahead == 'r') ADVANCE(69);
      END_STATE();
    case 116:
      if (lookahead == 'r') ADVANCE(100);
      END_STATE();
    case 117:
      if (lookahead == 'r') ADVANCE(75);
      END_STATE();
    case 118:
      if (lookahead == 'r') ADVANCE(70);
      END_STATE();
    case 119:
      if (lookahead == 'r') ADVANCE(144);
      END_STATE();
    case 120:
      if (lookahead == 'r') ADVANCE(138);
      END_STATE();
    case 121:
      if (lookahead == 'r') ADVANCE(56);
      END_STATE();
    case 122:
      if (lookahead == 'r') ADVANCE(33);
      END_STATE();
    case 123:
      if (lookahead == 's') ADVANCE(40);
      END_STATE();
    case 124:
      if (lookahead == 's') ADVANCE(305);
      END_STATE();
    case 125:
      if (lookahead == 's') ADVANCE(215);
      END_STATE();
    case 126:
      if (lookahead == 's') ADVANCE(134);
      END_STATE();
    case 127:
      if (lookahead == 's') ADVANCE(49);
      END_STATE();
    case 128:
      if (lookahead == 's') ADVANCE(135);
      END_STATE();
    case 129:
      if (lookahead == 's') ADVANCE(136);
      END_STATE();
    case 130:
      if (lookahead == 's') ADVANCE(50);
      END_STATE();
    case 131:
      if (lookahead == 's') ADVANCE(74);
      END_STATE();
    case 132:
      if (lookahead == 't') ADVANCE(296);
      END_STATE();
    case 133:
      if (lookahead == 't') ADVANCE(64);
      END_STATE();
    case 134:
      if (lookahead == 't') ADVANCE(322);
      END_STATE();
    case 135:
      if (lookahead == 't') ADVANCE(220);
      END_STATE();
    case 136:
      if (lookahead == 't') ADVANCE(308);
      END_STATE();
    case 137:
      if (lookahead == 't') ADVANCE(214);
      END_STATE();
    case 138:
      if (lookahead == 't') ADVANCE(154);
      END_STATE();
    case 139:
      if (lookahead == 't') ADVANCE(311);
      END_STATE();
    case 140:
      if (lookahead == 't') ADVANCE(219);
      END_STATE();
    case 141:
      if (lookahead == 't') ADVANCE(115);
      END_STATE();
    case 142:
      if (lookahead == 't') ADVANCE(72);
      END_STATE();
    case 143:
      if (lookahead == 't') ADVANCE(52);
      END_STATE();
    case 144:
      if (lookahead == 't') ADVANCE(125);
      END_STATE();
    case 145:
      if (lookahead == 't') ADVANCE(57);
      END_STATE();
    case 146:
      if (lookahead == 'u') ADVANCE(82);
      END_STATE();
    case 147:
      if (lookahead == 'u') ADVANCE(46);
      END_STATE();
    case 148:
      if (lookahead == 'u') ADVANCE(47);
      END_STATE();
    case 149:
      if (lookahead == 'u') ADVANCE(73);
      END_STATE();
    case 150:
      if (lookahead == 'u') ADVANCE(80);
      END_STATE();
    case 151:
      if (lookahead == 'v') ADVANCE(37);
      END_STATE();
    case 152:
      if (lookahead == 'x') ADVANCE(143);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(172);
      END_STATE();
    case 153:
      if (lookahead == 'y') ADVANCE(321);
      END_STATE();
    case 154:
      if (lookahead == 'y') ADVANCE(312);
      END_STATE();
    case 155:
      if (lookahead == 'y') ADVANCE(133);
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(184);
      END_STATE();
    case 156:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(183);
      END_STATE();
    case 157:
      if (lookahead == 'A' ||
          lookahead == 'a') ADVANCE(191);
      END_STATE();
    case 158:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(20);
      END_STATE();
    case 159:
      if (lookahead == 'C' ||
          lookahead == 'c') ADVANCE(157);
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') ADVANCE(159);
      END_STATE();
    case 160:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(172);
      END_STATE();
    case 161:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(186);
      END_STATE();
    case 162:
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(190);
      END_STATE();
    case 163:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(194);
      END_STATE();
    case 164:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(182);
      END_STATE();
    case 165:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(174);
      END_STATE();
    case 166:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(200);
      END_STATE();
    case 167:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(177);
      END_STATE();
    case 168:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(23);
      END_STATE();
    case 169:
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(192);
      END_STATE();
    case 170:
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(245);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(181);
      END_STATE();
    case 171:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(173);
      END_STATE();
    case 172:
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(166);
      END_STATE();
    case 173:
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(158);
      END_STATE();
    case 174:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(247);
      END_STATE();
    case 175:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(181);
      END_STATE();
    case 176:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(188);
      END_STATE();
    case 177:
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(162);
      END_STATE();
    case 178:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(189);
      END_STATE();
    case 179:
      if (lookahead == 'O' ||
          lookahead == 'o') ADVANCE(171);
      END_STATE();
    case 180:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(178);
      END_STATE();
    case 181:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(197);
      END_STATE();
    case 182:
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(167);
      END_STATE();
    case 183:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(161);
      END_STATE();
    case 184:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(180);
      END_STATE();
    case 185:
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(176);
      END_STATE();
    case 186:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(21);
      END_STATE();
    case 187:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(22);
      END_STATE();
    case 188:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(24);
      END_STATE();
    case 189:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(168);
      END_STATE();
    case 190:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(25);
      END_STATE();
    case 191:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(169);
      END_STATE();
    case 192:
      if (lookahead == 'S' ||
          lookahead == 's') ADVANCE(26);
      END_STATE();
    case 193:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(187);
      END_STATE();
    case 194:
      if (lookahead == 'T' ||
          lookahead == 't') ADVANCE(198);
      END_STATE();
    case 195:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(184);
      END_STATE();
    case 196:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(156);
      END_STATE();
    case 197:
      if (lookahead == 'U' ||
          lookahead == 'u') ADVANCE(193);
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
          lookahead != 0x2192) ADVANCE(299);
      END_STATE();
    case 200:
      if (('\t' <= lookahead && lookahead <= '\r') ||
          lookahead == ' ') ADVANCE(159);
      END_STATE();
    case 201:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(326);
      END_STATE();
    case 202:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(327);
      END_STATE();
    case 203:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(216);
      END_STATE();
    case 204:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(217);
      END_STATE();
    case 205:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(287);
      END_STATE();
    case 206:
      if (eof) ADVANCE(207);
      ADVANCE_MAP(
        '\n', 343,
        '\r', 1,
        '#', 211,
        '(', 239,
        ')', 240,
        '*', 340,
        ',', 221,
        '-', 339,
        ':', 231,
        '=', 27,
        '@', 65,
        '[', 222,
        ']', 224,
        '{', 304,
        0x2022, 338,
      );
      if (lookahead == '\t' ||
          lookahead == ' ') SKIP(206);
      if (lookahead == 'D' ||
          lookahead == 'd') ADVANCE(164);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(160);
      if (lookahead == 'G' ||
          lookahead == 'g') ADVANCE(196);
      if (lookahead == 'I' ||
          lookahead == 'i') ADVANCE(175);
      if (lookahead == 'L' ||
          lookahead == 'l') ADVANCE(179);
      if (lookahead == 'P' ||
          lookahead == 'p') ADVANCE(195);
      if (lookahead == 'R' ||
          lookahead == 'r') ADVANCE(163);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(243);
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
          lookahead != 0x2192) ADVANCE(299);
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
      ACCEPT_TOKEN(anon_sym_COLON);
      END_STATE();
    case 232:
      ACCEPT_TOKEN(anon_sym_required);
      END_STATE();
    case 233:
      ACCEPT_TOKEN(anon_sym_required);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 234:
      ACCEPT_TOKEN(anon_sym_optional);
      END_STATE();
    case 235:
      ACCEPT_TOKEN(anon_sym_optional);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 236:
      ACCEPT_TOKEN(aux_sym_guards_section_token1);
      END_STATE();
    case 237:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead == '#') ADVANCE(210);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(237);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(238);
      END_STATE();
    case 238:
      ACCEPT_TOKEN(aux_sym_guard_text_token1);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '-' &&
          lookahead != 0x2192) ADVANCE(238);
      END_STATE();
    case 239:
      ACCEPT_TOKEN(anon_sym_LPAREN);
      END_STATE();
    case 240:
      ACCEPT_TOKEN(anon_sym_RPAREN);
      END_STATE();
    case 241:
      ACCEPT_TOKEN(aux_sym_logic_section_token1);
      END_STATE();
    case 242:
      ACCEPT_TOKEN(anon_sym_DOT);
      END_STATE();
    case 243:
      ACCEPT_TOKEN(sym_step_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(243);
      END_STATE();
    case 244:
      ACCEPT_TOKEN(sym_state_name);
      if (lookahead == '-' ||
          ('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(244);
      END_STATE();
    case 245:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token1);
      END_STATE();
    case 246:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token1);
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(199);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(299);
      END_STATE();
    case 247:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token2);
      END_STATE();
    case 248:
      ACCEPT_TOKEN(aux_sym_condition_prefix_token2);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 249:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(262);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 250:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(263);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 251:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'a') ADVANCE(264);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('b' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 252:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'd') ADVANCE(293);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 253:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'd') ADVANCE(233);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 254:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(335);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 255:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(331);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 256:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(337);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 257:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(333);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 258:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(270);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 259:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'e') ADVANCE(253);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 260:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'i') ADVANCE(268);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 261:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'i') ADVANCE(273);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 262:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(275);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 263:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(235);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 264:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'l') ADVANCE(276);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 265:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'n') ADVANCE(252);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 266:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'n') ADVANCE(250);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 267:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'o') ADVANCE(277);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 268:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'o') ADVANCE(266);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 269:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'p') ADVANCE(278);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 270:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'q') ADVANCE(281);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 271:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(279);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 272:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(295);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 273:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(259);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 274:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'r') ADVANCE(280);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 275:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 's') ADVANCE(256);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 276:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 's') ADVANCE(257);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 277:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 't') ADVANCE(297);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 278:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 't') ADVANCE(260);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 279:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(254);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 280:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(255);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 281:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'u') ADVANCE(261);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 282:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(284);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 283:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'H' ||
          lookahead == 'h') ADVANCE(282);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 284:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (lookahead == 'N' ||
          lookahead == 'n') ADVANCE(248);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 285:
      ACCEPT_TOKEN(aux_sym_condition_token_token1);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 286:
      ACCEPT_TOKEN(aux_sym_condition_token_token2);
      if (lookahead == '.') ADVANCE(205);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(286);
      END_STATE();
    case 287:
      ACCEPT_TOKEN(aux_sym_condition_token_token2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(287);
      END_STATE();
    case 288:
      ACCEPT_TOKEN(aux_sym_condition_token_token3);
      if (lookahead == '=') ADVANCE(310);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(289);
      END_STATE();
    case 289:
      ACCEPT_TOKEN(aux_sym_condition_token_token3);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(289);
      END_STATE();
    case 290:
      ACCEPT_TOKEN(aux_sym_condition_token_token4);
      END_STATE();
    case 291:
      ACCEPT_TOKEN(aux_sym_condition_token_token5);
      END_STATE();
    case 292:
      ACCEPT_TOKEN(anon_sym_and);
      END_STATE();
    case 293:
      ACCEPT_TOKEN(anon_sym_and);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 294:
      ACCEPT_TOKEN(anon_sym_or);
      END_STATE();
    case 295:
      ACCEPT_TOKEN(anon_sym_or);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 296:
      ACCEPT_TOKEN(anon_sym_not);
      END_STATE();
    case 297:
      ACCEPT_TOKEN(anon_sym_not);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 298:
      ACCEPT_TOKEN(sym_step_text);
      if (lookahead == 'F' ||
          lookahead == 'f') ADVANCE(246);
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(199);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(299);
      END_STATE();
    case 299:
      ACCEPT_TOKEN(sym_step_text);
      if (lookahead == '\t' ||
          lookahead == ' ' ||
          lookahead == '-') ADVANCE(199);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != 0x2192) ADVANCE(299);
      END_STATE();
    case 300:
      ACCEPT_TOKEN(aux_sym_returns_section_token1);
      END_STATE();
    case 301:
      ACCEPT_TOKEN(aux_sym_depends_section_token1);
      END_STATE();
    case 302:
      ACCEPT_TOKEN(aux_sym_edge_cases_section_token1);
      END_STATE();
    case 303:
      ACCEPT_TOKEN(anon_sym_ATtype);
      END_STATE();
    case 304:
      ACCEPT_TOKEN(anon_sym_LBRACE);
      END_STATE();
    case 305:
      ACCEPT_TOKEN(anon_sym_extends);
      END_STATE();
    case 306:
      ACCEPT_TOKEN(sym_type_name);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(306);
      END_STATE();
    case 307:
      ACCEPT_TOKEN(anon_sym_RBRACE);
      END_STATE();
    case 308:
      ACCEPT_TOKEN(anon_sym_ATtest);
      END_STATE();
    case 309:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      END_STATE();
    case 310:
      ACCEPT_TOKEN(anon_sym_EQ_EQ);
      if (lookahead == '!' ||
          ('<' <= lookahead && lookahead <= '>')) ADVANCE(289);
      END_STATE();
    case 311:
      ACCEPT_TOKEN(anon_sym_ATinvariant);
      END_STATE();
    case 312:
      ACCEPT_TOKEN(anon_sym_ATproperty);
      END_STATE();
    case 313:
      ACCEPT_TOKEN(sym_expression_text);
      if (lookahead == '#') ADVANCE(208);
      if (lookahead == '\t' ||
          lookahead == ' ') ADVANCE(313);
      if (lookahead != 0 &&
          lookahead != '\t' &&
          lookahead != '\n' &&
          lookahead != '}') ADVANCE(314);
      END_STATE();
    case 314:
      ACCEPT_TOKEN(sym_expression_text);
      if (lookahead != 0 &&
          lookahead != '\n' &&
          lookahead != '}') ADVANCE(314);
      END_STATE();
    case 315:
      ACCEPT_TOKEN(anon_sym_ATliteral);
      END_STATE();
    case 316:
      ACCEPT_TOKEN(anon_sym_QMARK);
      END_STATE();
    case 317:
      ACCEPT_TOKEN(anon_sym_number);
      END_STATE();
    case 318:
      ACCEPT_TOKEN(anon_sym_string);
      END_STATE();
    case 319:
      ACCEPT_TOKEN(anon_sym_boolean);
      END_STATE();
    case 320:
      ACCEPT_TOKEN(anon_sym_void);
      END_STATE();
    case 321:
      ACCEPT_TOKEN(anon_sym_any);
      END_STATE();
    case 322:
      ACCEPT_TOKEN(anon_sym_list);
      END_STATE();
    case 323:
      ACCEPT_TOKEN(anon_sym_of);
      END_STATE();
    case 324:
      ACCEPT_TOKEN(anon_sym_map);
      END_STATE();
    case 325:
      ACCEPT_TOKEN(anon_sym_to);
      END_STATE();
    case 326:
      ACCEPT_TOKEN(sym_number);
      if (lookahead == '.') ADVANCE(202);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(326);
      END_STATE();
    case 327:
      ACCEPT_TOKEN(sym_number);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(327);
      END_STATE();
    case 328:
      ACCEPT_TOKEN(aux_sym_quoted_string_token1);
      END_STATE();
    case 329:
      ACCEPT_TOKEN(aux_sym_quoted_string_token2);
      END_STATE();
    case 330:
      ACCEPT_TOKEN(anon_sym_true);
      END_STATE();
    case 331:
      ACCEPT_TOKEN(anon_sym_true);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 332:
      ACCEPT_TOKEN(anon_sym_false);
      END_STATE();
    case 333:
      ACCEPT_TOKEN(anon_sym_false);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 334:
      ACCEPT_TOKEN(anon_sym_True);
      END_STATE();
    case 335:
      ACCEPT_TOKEN(anon_sym_True);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 336:
      ACCEPT_TOKEN(anon_sym_False);
      END_STATE();
    case 337:
      ACCEPT_TOKEN(anon_sym_False);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(285);
      END_STATE();
    case 338:
      ACCEPT_TOKEN(anon_sym_u2022);
      END_STATE();
    case 339:
      ACCEPT_TOKEN(anon_sym_DASH);
      END_STATE();
    case 340:
      ACCEPT_TOKEN(anon_sym_STAR);
      END_STATE();
    case 341:
      ACCEPT_TOKEN(anon_sym_u2192);
      END_STATE();
    case 342:
      ACCEPT_TOKEN(anon_sym_DASH_GT);
      END_STATE();
    case 343:
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
  [25] = {.lex_state = 2},
  [26] = {.lex_state = 10},
  [27] = {.lex_state = 10},
  [28] = {.lex_state = 10},
  [29] = {.lex_state = 10},
  [30] = {.lex_state = 10},
  [31] = {.lex_state = 10},
  [32] = {.lex_state = 206},
  [33] = {.lex_state = 206},
  [34] = {.lex_state = 206},
  [35] = {.lex_state = 206},
  [36] = {.lex_state = 206},
  [37] = {.lex_state = 206},
  [38] = {.lex_state = 206},
  [39] = {.lex_state = 206},
  [40] = {.lex_state = 206},
  [41] = {.lex_state = 206},
  [42] = {.lex_state = 206},
  [43] = {.lex_state = 206},
  [44] = {.lex_state = 2},
  [45] = {.lex_state = 206},
  [46] = {.lex_state = 206},
  [47] = {.lex_state = 206},
  [48] = {.lex_state = 206},
  [49] = {.lex_state = 206},
  [50] = {.lex_state = 206},
  [51] = {.lex_state = 2},
  [52] = {.lex_state = 206},
  [53] = {.lex_state = 8},
  [54] = {.lex_state = 9},
  [55] = {.lex_state = 9},
  [56] = {.lex_state = 3},
  [57] = {.lex_state = 3},
  [58] = {.lex_state = 3},
  [59] = {.lex_state = 9},
  [60] = {.lex_state = 5},
  [61] = {.lex_state = 3},
  [62] = {.lex_state = 3},
  [63] = {.lex_state = 3},
  [64] = {.lex_state = 206},
  [65] = {.lex_state = 206},
  [66] = {.lex_state = 206},
  [67] = {.lex_state = 206},
  [68] = {.lex_state = 11},
  [69] = {.lex_state = 13},
  [70] = {.lex_state = 4},
  [71] = {.lex_state = 3},
  [72] = {.lex_state = 3},
  [73] = {.lex_state = 16},
  [74] = {.lex_state = 3},
  [75] = {.lex_state = 3},
  [76] = {.lex_state = 16},
  [77] = {.lex_state = 2},
  [78] = {.lex_state = 3},
  [79] = {.lex_state = 16},
  [80] = {.lex_state = 3},
  [81] = {.lex_state = 16},
  [82] = {.lex_state = 3},
  [83] = {.lex_state = 2},
  [84] = {.lex_state = 2},
  [85] = {.lex_state = 3},
  [86] = {.lex_state = 0},
  [87] = {.lex_state = 0},
  [88] = {.lex_state = 16},
  [89] = {.lex_state = 0},
  [90] = {.lex_state = 0},
  [91] = {.lex_state = 16},
  [92] = {.lex_state = 0},
  [93] = {.lex_state = 0},
  [94] = {.lex_state = 0},
  [95] = {.lex_state = 0},
  [96] = {.lex_state = 2},
  [97] = {.lex_state = 7},
  [98] = {.lex_state = 0},
  [99] = {.lex_state = 206},
  [100] = {.lex_state = 0},
  [101] = {.lex_state = 3},
  [102] = {.lex_state = 7},
  [103] = {.lex_state = 0},
  [104] = {.lex_state = 0},
  [105] = {.lex_state = 206},
  [106] = {.lex_state = 206},
  [107] = {.lex_state = 206},
  [108] = {.lex_state = 206},
  [109] = {.lex_state = 2},
  [110] = {.lex_state = 0},
  [111] = {.lex_state = 2},
  [112] = {.lex_state = 0},
  [113] = {.lex_state = 0},
  [114] = {.lex_state = 206},
  [115] = {.lex_state = 14},
  [116] = {.lex_state = 0},
  [117] = {.lex_state = 0},
  [118] = {.lex_state = 0},
  [119] = {.lex_state = 206},
  [120] = {.lex_state = 0},
  [121] = {.lex_state = 0},
  [122] = {.lex_state = 0},
  [123] = {.lex_state = 206},
  [124] = {.lex_state = 206},
  [125] = {.lex_state = 11},
  [126] = {.lex_state = 206},
  [127] = {.lex_state = 17},
  [128] = {.lex_state = 16},
  [129] = {.lex_state = 0},
  [130] = {.lex_state = 0},
  [131] = {.lex_state = 0},
  [132] = {.lex_state = 0},
  [133] = {.lex_state = 16},
  [134] = {.lex_state = 2},
  [135] = {.lex_state = 3},
  [136] = {.lex_state = 3},
  [137] = {.lex_state = 3},
  [138] = {.lex_state = 0},
  [139] = {.lex_state = 3},
  [140] = {.lex_state = 3},
  [141] = {.lex_state = 16},
  [142] = {.lex_state = 11},
  [143] = {.lex_state = 11},
  [144] = {.lex_state = 3},
  [145] = {.lex_state = 0},
  [146] = {.lex_state = 16},
  [147] = {.lex_state = 206},
  [148] = {.lex_state = 3},
  [149] = {.lex_state = 3},
  [150] = {.lex_state = 0},
  [151] = {.lex_state = 17},
  [152] = {.lex_state = 14},
  [153] = {.lex_state = 11},
  [154] = {.lex_state = 0},
  [155] = {.lex_state = 0},
  [156] = {.lex_state = 0},
  [157] = {.lex_state = 0},
  [158] = {.lex_state = 206},
  [159] = {.lex_state = 0},
  [160] = {.lex_state = 10},
  [161] = {.lex_state = 206},
  [162] = {.lex_state = 0},
  [163] = {.lex_state = 0},
  [164] = {.lex_state = 0},
  [165] = {.lex_state = 0},
  [166] = {.lex_state = 0},
  [167] = {.lex_state = 0},
  [168] = {.lex_state = 0},
  [169] = {.lex_state = 0},
  [170] = {.lex_state = 0},
  [171] = {.lex_state = 10},
  [172] = {.lex_state = 0},
  [173] = {.lex_state = 206},
  [174] = {.lex_state = 0},
  [175] = {.lex_state = 0},
  [176] = {.lex_state = 3},
  [177] = {.lex_state = 10},
  [178] = {.lex_state = 206},
  [179] = {.lex_state = 0},
  [180] = {.lex_state = 0},
  [181] = {.lex_state = 206},
  [182] = {.lex_state = 12},
  [183] = {.lex_state = 0},
  [184] = {.lex_state = 0},
  [185] = {.lex_state = 0},
  [186] = {.lex_state = 0},
  [187] = {.lex_state = 15},
  [188] = {.lex_state = 0},
  [189] = {.lex_state = 206},
  [190] = {.lex_state = 0},
  [191] = {.lex_state = 206},
  [192] = {.lex_state = 0},
  [193] = {.lex_state = 0},
  [194] = {.lex_state = 0},
  [195] = {.lex_state = 0, .external_lex_state = 1},
  [196] = {.lex_state = 0},
  [197] = {.lex_state = 0, .external_lex_state = 1},
  [198] = {.lex_state = 0},
  [199] = {.lex_state = 10},
  [200] = {.lex_state = 0},
  [201] = {.lex_state = 0},
  [202] = {.lex_state = 0},
  [203] = {.lex_state = 7},
  [204] = {.lex_state = 206},
  [205] = {.lex_state = 206},
  [206] = {.lex_state = 0},
  [207] = {.lex_state = 0},
  [208] = {.lex_state = 0},
  [209] = {.lex_state = 0},
  [210] = {.lex_state = 0},
  [211] = {.lex_state = 7},
  [212] = {.lex_state = 0},
  [213] = {.lex_state = 15},
  [214] = {.lex_state = 0},
  [215] = {.lex_state = 0},
  [216] = {.lex_state = 0},
  [217] = {.lex_state = 206},
  [218] = {.lex_state = 206},
  [219] = {.lex_state = 0},
  [220] = {.lex_state = 0},
  [221] = {.lex_state = 7},
  [222] = {.lex_state = 0},
  [223] = {.lex_state = 0},
  [224] = {.lex_state = 0},
  [225] = {.lex_state = 15},
  [226] = {.lex_state = 7},
  [227] = {.lex_state = 0},
  [228] = {.lex_state = 0},
  [229] = {.lex_state = 0},
  [230] = {.lex_state = 0},
  [231] = {.lex_state = 0},
  [232] = {.lex_state = 206},
  [233] = {.lex_state = 0},
  [234] = {.lex_state = 0},
  [235] = {.lex_state = 206},
  [236] = {.lex_state = 0},
  [237] = {.lex_state = 0},
  [238] = {.lex_state = 0},
  [239] = {.lex_state = 0},
  [240] = {.lex_state = 0},
  [241] = {.lex_state = 0},
  [242] = {.lex_state = 206},
  [243] = {.lex_state = 17},
  [244] = {.lex_state = 3},
  [245] = {.lex_state = 0},
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
    [sym_source_file] = STATE(224),
    [sym_directive] = STATE(3),
    [sym_module_directive] = STATE(37),
    [sym_version_directive] = STATE(37),
    [sym_target_directive] = STATE(37),
    [sym_imports_directive] = STATE(37),
    [sym_anlu_block] = STATE(3),
    [sym_anlu_header] = STATE(5),
    [sym_type_block] = STATE(3),
    [sym_type_header] = STATE(56),
    [sym_test_block] = STATE(3),
    [sym_test_header] = STATE(63),
    [sym_invariant_block] = STATE(3),
    [sym_invariant_header] = STATE(79),
    [sym_property_block] = STATE(3),
    [sym_property_header] = STATE(81),
    [sym_literal_block] = STATE(3),
    [sym_literal_header] = STATE(197),
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
    STATE(5), 1,
      sym_anlu_header,
    STATE(56), 1,
      sym_type_header,
    STATE(63), 1,
      sym_test_header,
    STATE(79), 1,
      sym_invariant_header,
    STATE(81), 1,
      sym_property_header,
    STATE(197), 1,
      sym_literal_header,
    STATE(37), 4,
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
    STATE(5), 1,
      sym_anlu_header,
    STATE(56), 1,
      sym_type_header,
    STATE(63), 1,
      sym_test_header,
    STATE(79), 1,
      sym_invariant_header,
    STATE(81), 1,
      sym_property_header,
    STATE(197), 1,
      sym_literal_header,
    STATE(37), 4,
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
    ACTIONS(73), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(76), 1,
      aux_sym_guards_section_token1,
    ACTIONS(79), 1,
      aux_sym_logic_section_token1,
    ACTIONS(82), 1,
      aux_sym_returns_section_token1,
    ACTIONS(85), 1,
      aux_sym_depends_section_token1,
    ACTIONS(88), 1,
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
    ACTIONS(93), 1,
      aux_sym_purpose_section_token1,
    ACTIONS(95), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(97), 1,
      aux_sym_guards_section_token1,
    ACTIONS(99), 1,
      aux_sym_logic_section_token1,
    ACTIONS(101), 1,
      aux_sym_returns_section_token1,
    ACTIONS(103), 1,
      aux_sym_depends_section_token1,
    ACTIONS(105), 1,
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
    ACTIONS(91), 12,
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
    ACTIONS(93), 1,
      aux_sym_purpose_section_token1,
    ACTIONS(95), 1,
      aux_sym_inputs_section_token1,
    ACTIONS(97), 1,
      aux_sym_guards_section_token1,
    ACTIONS(99), 1,
      aux_sym_logic_section_token1,
    ACTIONS(101), 1,
      aux_sym_returns_section_token1,
    ACTIONS(103), 1,
      aux_sym_depends_section_token1,
    ACTIONS(105), 1,
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
    ACTIONS(107), 12,
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
    STATE(151), 1,
      sym_bullet,
    STATE(12), 2,
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
    STATE(148), 1,
      sym_bullet,
    STATE(9), 2,
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
    STATE(148), 1,
      sym_bullet,
    STATE(9), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(119), 3,
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
    STATE(127), 1,
      sym_bullet,
    STATE(11), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
    ACTIONS(122), 19,
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
    STATE(127), 1,
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
    STATE(151), 1,
      sym_bullet,
    STATE(12), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
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
    STATE(18), 2,
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
  [605] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(142), 22,
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
  [633] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(144), 22,
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
  [661] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(148), 1,
      sym_step_number,
    STATE(18), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
    ACTIONS(146), 19,
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
    STATE(191), 1,
      sym_test_args,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(105), 3,
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
    STATE(89), 1,
      sym_type_spec,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(104), 5,
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
    STATE(87), 1,
      sym_type_spec,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(104), 5,
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
    STATE(94), 1,
      sym_type_spec,
    ACTIONS(175), 5,
      anon_sym_number,
      anon_sym_string,
      anon_sym_boolean,
      anon_sym_void,
      anon_sym_any,
    STATE(104), 5,
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
    STATE(86), 5,
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
    STATE(190), 5,
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
    STATE(95), 5,
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
  [1196] = 2,
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
  [1214] = 2,
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
  [1232] = 2,
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
  [1250] = 2,
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
  [1268] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(165), 1,
      aux_sym_condition_token_token1,
    ACTIONS(167), 1,
      sym_number,
    STATE(147), 1,
      sym_test_value,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(105), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(171), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
  [1296] = 2,
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
  [1314] = 2,
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
  [1332] = 2,
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
  [1350] = 2,
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
  [1368] = 2,
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
  [1386] = 2,
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
  [1404] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(165), 1,
      aux_sym_condition_token_token1,
    ACTIONS(167), 1,
      sym_number,
    STATE(188), 1,
      sym_test_value,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(105), 3,
      sym_quoted_string,
      sym_boolean,
      sym_identifier,
    ACTIONS(171), 4,
      anon_sym_true,
      anon_sym_false,
      anon_sym_True,
      anon_sym_False,
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
    STATE(207), 1,
      sym_condition_text,
    STATE(54), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(219), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(221), 4,
      aux_sym_condition_token_token2,
      aux_sym_condition_token_token3,
      aux_sym_condition_token_token4,
      aux_sym_condition_token_token5,
  [1473] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(223), 1,
      aux_sym_condition_prefix_token2,
    STATE(55), 2,
      sym_condition_token,
      aux_sym_condition_text_repeat1,
    ACTIONS(219), 4,
      aux_sym_condition_token_token1,
      anon_sym_and,
      anon_sym_or,
      anon_sym_not,
    ACTIONS(221), 4,
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
    STATE(47), 1,
      sym_type_close,
    STATE(135), 1,
      sym_bullet,
    STATE(192), 1,
      sym_identifier,
    STATE(57), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(115), 3,
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
    STATE(50), 1,
      sym_type_close,
    STATE(135), 1,
      sym_bullet,
    STATE(192), 1,
      sym_identifier,
    STATE(58), 2,
      sym_type_field,
      aux_sym_type_block_repeat1,
    ACTIONS(115), 3,
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
    STATE(135), 1,
      sym_bullet,
    STATE(192), 1,
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
    STATE(116), 1,
      sym_identifier,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    ACTIONS(249), 2,
      anon_sym_required,
      anon_sym_optional,
    STATE(145), 2,
      sym_constraint_pair,
      sym_quoted_string,
  [1639] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(251), 1,
      anon_sym_RBRACE,
    STATE(33), 1,
      sym_test_close,
    STATE(217), 1,
      sym_test_call,
    STATE(242), 1,
      sym_identifier,
    STATE(71), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1662] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(253), 1,
      anon_sym_RPAREN,
    STATE(235), 1,
      sym_error_args,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(123), 2,
      sym_quoted_string,
      sym_identifier,
  [1683] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(251), 1,
      anon_sym_RBRACE,
    STATE(41), 1,
      sym_test_close,
    STATE(217), 1,
      sym_test_call,
    STATE(242), 1,
      sym_identifier,
    STATE(61), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1706] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(255), 6,
      anon_sym_COMMA,
      anon_sym_COLON,
      anon_sym_LPAREN,
      anon_sym_RPAREN,
      anon_sym_LBRACE,
      sym__newline,
  [1718] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(148), 1,
      sym_bullet,
    STATE(8), 2,
      sym_input_item,
      aux_sym_inputs_section_repeat1,
    ACTIONS(115), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1734] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(151), 1,
      sym_bullet,
    STATE(7), 2,
      sym_guard_item,
      aux_sym_guards_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1750] = 4,
    ACTIONS(3), 1,
      sym_comment,
    STATE(127), 1,
      sym_bullet,
    STATE(10), 2,
      sym_edge_case_item,
      aux_sym_edge_cases_section_repeat1,
    ACTIONS(111), 3,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1766] = 7,
    ACTIONS(165), 1,
      aux_sym_condition_token_token1,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(259), 1,
      aux_sym_description_text_token1,
    STATE(201), 1,
      sym_error_spec,
    STATE(202), 1,
      sym_error_call,
    STATE(204), 1,
      sym_identifier,
    STATE(245), 1,
      sym_error_text,
  [1788] = 7,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(261), 1,
      anon_sym_LBRACK,
    ACTIONS(263), 1,
      aux_sym_condition_prefix_token1,
    ACTIONS(265), 1,
      sym_step_text,
    STATE(115), 1,
      sym_state_prefix,
    STATE(185), 1,
      sym_logic_step,
    STATE(187), 1,
      sym_condition_prefix,
  [1810] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(267), 1,
      sym_number,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(154), 2,
      sym_quoted_string,
      sym_identifier,
  [1828] = 6,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(269), 1,
      aux_sym_condition_token_token1,
    ACTIONS(272), 1,
      anon_sym_RBRACE,
    STATE(217), 1,
      sym_test_call,
    STATE(242), 1,
      sym_identifier,
    STATE(71), 2,
      sym_test_assertion,
      aux_sym_test_block_repeat1,
  [1848] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(274), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1859] = 5,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(276), 1,
      anon_sym_RBRACE,
    ACTIONS(278), 1,
      sym_expression_text,
    STATE(43), 1,
      sym_invariant_close,
    STATE(91), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [1876] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(280), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1887] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(282), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1898] = 5,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(284), 1,
      anon_sym_RBRACE,
    ACTIONS(286), 1,
      sym_expression_text,
    STATE(34), 1,
      sym_property_close,
    STATE(88), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [1915] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(290), 1,
      sym__newline,
    STATE(149), 1,
      sym_arrow,
    STATE(209), 1,
      sym_output_binding,
    ACTIONS(288), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [1932] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(292), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1943] = 5,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(276), 1,
      anon_sym_RBRACE,
    ACTIONS(278), 1,
      sym_expression_text,
    STATE(45), 1,
      sym_invariant_close,
    STATE(73), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [1960] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(294), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1971] = 5,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(284), 1,
      anon_sym_RBRACE,
    ACTIONS(286), 1,
      sym_expression_text,
    STATE(49), 1,
      sym_property_close,
    STATE(76), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [1988] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(296), 5,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
      anon_sym_u2022,
      anon_sym_DASH,
      anon_sym_STAR,
  [1999] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(298), 1,
      sym__newline,
    STATE(149), 1,
      sym_arrow,
    STATE(228), 1,
      sym_output_binding,
    ACTIONS(288), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2016] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(300), 1,
      sym__newline,
    STATE(149), 1,
      sym_arrow,
    STATE(237), 1,
      sym_output_binding,
    ACTIONS(288), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2033] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    ACTIONS(169), 2,
      aux_sym_quoted_string_token1,
      aux_sym_quoted_string_token2,
    STATE(126), 2,
      sym_quoted_string,
      sym_identifier,
  [2048] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(302), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2058] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(304), 1,
      anon_sym_COMMA,
    ACTIONS(306), 1,
      sym__newline,
    STATE(98), 1,
      aux_sym_input_constraints_repeat1,
    STATE(220), 1,
      sym_input_constraints,
  [2074] = 4,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(308), 1,
      anon_sym_RBRACE,
    ACTIONS(310), 1,
      sym_expression_text,
    STATE(88), 2,
      sym_property_assertion,
      aux_sym_property_block_repeat1,
  [2088] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(304), 1,
      anon_sym_COMMA,
    ACTIONS(313), 1,
      sym__newline,
    STATE(113), 1,
      aux_sym_input_constraints_repeat1,
    STATE(196), 1,
      sym_field_constraints,
  [2104] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(315), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2114] = 4,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(317), 1,
      anon_sym_RBRACE,
    ACTIONS(319), 1,
      sym_expression_text,
    STATE(91), 2,
      sym_invariant_assertion,
      aux_sym_invariant_block_repeat1,
  [2128] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(322), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2138] = 3,
    ACTIONS(3), 1,
      sym_comment,
    STATE(163), 1,
      sym_target_name,
    ACTIONS(324), 3,
      anon_sym_python,
      anon_sym_typescript,
      anon_sym_rust,
  [2150] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(304), 1,
      anon_sym_COMMA,
    ACTIONS(326), 1,
      sym__newline,
    STATE(113), 1,
      aux_sym_input_constraints_repeat1,
    STATE(168), 1,
      sym_field_constraints,
  [2166] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(328), 4,
      anon_sym_COMMA,
      anon_sym_QMARK,
      anon_sym_to,
      sym__newline,
  [2176] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(332), 1,
      sym__newline,
    STATE(68), 1,
      sym_arrow,
    ACTIONS(330), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2190] = 5,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(334), 1,
      anon_sym_LBRACK,
    ACTIONS(336), 1,
      sym_anlu_identifier,
    STATE(121), 1,
      sym_anlu_reference,
    STATE(216), 1,
      sym_depends_list,
  [2206] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(304), 1,
      anon_sym_COMMA,
    ACTIONS(338), 1,
      sym__newline,
    STATE(117), 1,
      aux_sym_input_constraints_repeat1,
  [2219] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(340), 1,
      anon_sym_COMMA,
    ACTIONS(343), 1,
      anon_sym_RPAREN,
    STATE(99), 1,
      aux_sym_error_args_repeat1,
  [2232] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(345), 1,
      anon_sym_COMMA,
    ACTIONS(348), 1,
      sym__newline,
    STATE(100), 1,
      aux_sym_import_list_repeat1,
  [2245] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(118), 1,
      sym_identifier,
    STATE(193), 1,
      sym_import_list,
  [2258] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(334), 1,
      anon_sym_LBRACK,
    ACTIONS(336), 1,
      sym_anlu_identifier,
    STATE(132), 1,
      sym_anlu_reference,
  [2271] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(350), 1,
      anon_sym_COMMA,
    ACTIONS(352), 1,
      sym__newline,
    STATE(110), 1,
      aux_sym_depends_list_repeat1,
  [2284] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(356), 1,
      anon_sym_QMARK,
    ACTIONS(354), 2,
      anon_sym_COMMA,
      sym__newline,
  [2295] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(358), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2304] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(360), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2313] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(362), 3,
      anon_sym_COMMA,
      anon_sym_RPAREN,
      sym__newline,
  [2322] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(364), 1,
      anon_sym_COMMA,
    ACTIONS(366), 1,
      anon_sym_RPAREN,
    STATE(114), 1,
      aux_sym_test_args_repeat1,
  [2335] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(368), 3,
      anon_sym_u2192,
      anon_sym_DASH_GT,
      sym__newline,
  [2344] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(370), 1,
      anon_sym_COMMA,
    ACTIONS(373), 1,
      sym__newline,
    STATE(110), 1,
      aux_sym_depends_list_repeat1,
  [2357] = 3,
    ACTIONS(3), 1,
      sym_comment,
    STATE(143), 1,
      sym_arrow,
    ACTIONS(330), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2368] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(375), 1,
      anon_sym_COMMA,
    ACTIONS(377), 1,
      sym__newline,
    STATE(100), 1,
      aux_sym_import_list_repeat1,
  [2381] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(304), 1,
      anon_sym_COMMA,
    ACTIONS(379), 1,
      sym__newline,
    STATE(117), 1,
      aux_sym_input_constraints_repeat1,
  [2394] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(364), 1,
      anon_sym_COMMA,
    ACTIONS(381), 1,
      anon_sym_RPAREN,
    STATE(119), 1,
      aux_sym_test_args_repeat1,
  [2407] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(263), 1,
      aux_sym_condition_prefix_token1,
    ACTIONS(383), 1,
      sym_step_text,
    STATE(213), 1,
      sym_condition_prefix,
  [2420] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(387), 1,
      anon_sym_COLON,
    ACTIONS(385), 2,
      anon_sym_COMMA,
      sym__newline,
  [2431] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(385), 1,
      sym__newline,
    ACTIONS(389), 1,
      anon_sym_COMMA,
    STATE(117), 1,
      aux_sym_input_constraints_repeat1,
  [2444] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(375), 1,
      anon_sym_COMMA,
    ACTIONS(392), 1,
      sym__newline,
    STATE(112), 1,
      aux_sym_import_list_repeat1,
  [2457] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(394), 1,
      anon_sym_COMMA,
    ACTIONS(397), 1,
      anon_sym_RPAREN,
    STATE(119), 1,
      aux_sym_test_args_repeat1,
  [2470] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(138), 1,
      sym_step_number,
    STATE(14), 2,
      sym_logic_item,
      aux_sym_logic_section_repeat1,
  [2481] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(350), 1,
      anon_sym_COMMA,
    ACTIONS(399), 1,
      sym__newline,
    STATE(103), 1,
      aux_sym_depends_list_repeat1,
  [2494] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(401), 1,
      anon_sym_LBRACE,
    ACTIONS(403), 1,
      anon_sym_extends,
    STATE(174), 1,
      sym_extends_clause,
  [2507] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(405), 1,
      anon_sym_COMMA,
    ACTIONS(407), 1,
      anon_sym_RPAREN,
    STATE(124), 1,
      aux_sym_error_args_repeat1,
  [2520] = 4,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(405), 1,
      anon_sym_COMMA,
    ACTIONS(409), 1,
      anon_sym_RPAREN,
    STATE(99), 1,
      aux_sym_error_args_repeat1,
  [2533] = 3,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(411), 1,
      aux_sym_description_text_token1,
    STATE(208), 1,
      sym_returns_text,
  [2543] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(343), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [2551] = 3,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(413), 1,
      aux_sym_guard_text_token1,
    STATE(111), 1,
      sym_edge_condition_text,
  [2561] = 2,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(415), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2569] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(417), 1,
      anon_sym_RBRACE,
    STATE(36), 1,
      sym_literal_close,
  [2579] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(348), 2,
      anon_sym_COMMA,
      sym__newline,
  [2587] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(419), 2,
      anon_sym_COMMA,
      sym__newline,
  [2595] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(373), 2,
      anon_sym_COMMA,
      sym__newline,
  [2603] = 2,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(421), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2611] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(423), 2,
      anon_sym_u2192,
      anon_sym_DASH_GT,
  [2619] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(223), 1,
      sym_identifier,
  [2629] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(130), 1,
      sym_identifier,
  [2639] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(241), 1,
      sym_identifier,
  [2649] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(425), 2,
      anon_sym_COMMA,
      sym__newline,
  [2657] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(427), 2,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
  [2665] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(429), 2,
      aux_sym_condition_token_token1,
      anon_sym_RBRACE,
  [2673] = 2,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(431), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2681] = 2,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(433), 2,
      aux_sym_description_text_token1,
      aux_sym_condition_token_token1,
  [2689] = 3,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(435), 1,
      aux_sym_description_text_token1,
    STATE(215), 1,
      sym_edge_behavior_text,
  [2699] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(229), 1,
      sym_identifier,
  [2709] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(385), 2,
      anon_sym_COMMA,
      sym__newline,
  [2717] = 2,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(437), 2,
      anon_sym_RBRACE,
      sym_expression_text,
  [2725] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(397), 2,
      anon_sym_COMMA,
      anon_sym_RPAREN,
  [2733] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(219), 1,
      sym_identifier,
  [2743] = 3,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(233), 1,
      aux_sym_condition_token_token1,
    STATE(227), 1,
      sym_identifier,
  [2753] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(439), 2,
      anon_sym_COMMA,
      sym__newline,
  [2761] = 3,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(441), 1,
      aux_sym_guard_text_token1,
    STATE(96), 1,
      sym_guard_text,
  [2771] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(443), 2,
      aux_sym_condition_prefix_token1,
      sym_step_text,
  [2779] = 3,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(445), 1,
      aux_sym_description_text_token1,
    STATE(155), 1,
      sym_description_text,
  [2789] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(447), 2,
      anon_sym_COMMA,
      sym__newline,
  [2797] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(449), 1,
      sym__newline,
  [2804] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(451), 1,
      sym__newline,
  [2811] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(453), 1,
      sym__newline,
  [2818] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(455), 1,
      anon_sym_RBRACK,
  [2825] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(457), 1,
      sym__newline,
  [2832] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(459), 1,
      sym_type_name,
  [2839] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(461), 1,
      anon_sym_LBRACK,
  [2846] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(463), 1,
      anon_sym_of,
  [2853] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(465), 1,
      sym__newline,
  [2860] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(467), 1,
      anon_sym_of,
  [2867] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(469), 1,
      sym__newline,
  [2874] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(471), 1,
      sym__newline,
  [2881] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(473), 1,
      sym__newline,
  [2888] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(475), 1,
      sym__newline,
  [2895] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(477), 1,
      anon_sym_LBRACE,
  [2902] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(479), 1,
      sym__newline,
  [2909] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(481), 1,
      sym_type_name,
  [2916] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(483), 1,
      sym__newline,
  [2923] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(485), 1,
      anon_sym_EQ_EQ,
  [2930] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(487), 1,
      anon_sym_LBRACE,
  [2937] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(489), 1,
      sym__newline,
  [2944] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(491), 1,
      aux_sym_condition_token_token1,
  [2951] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(493), 1,
      sym_version_string,
  [2958] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(495), 1,
      anon_sym_RBRACK,
  [2965] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(497), 1,
      sym__newline,
  [2972] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(499), 1,
      sym__newline,
  [2979] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(501), 1,
      anon_sym_RBRACK,
  [2986] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(503), 1,
      sym_state_name,
  [2993] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(505), 1,
      sym__newline,
  [3000] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(507), 1,
      sym__newline,
  [3007] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(509), 1,
      sym__newline,
  [3014] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(511), 1,
      anon_sym_LBRACE,
  [3021] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(383), 1,
      sym_step_text,
  [3028] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(513), 1,
      sym__newline,
  [3035] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(515), 1,
      anon_sym_EQ_EQ,
  [3042] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(517), 1,
      anon_sym_to,
  [3049] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(519), 1,
      anon_sym_RPAREN,
  [3056] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(521), 1,
      anon_sym_COLON,
  [3063] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(523), 1,
      sym__newline,
  [3070] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(525), 1,
      anon_sym_LBRACE,
  [3077] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(527), 1,
      sym_literal_content,
  [3084] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(529), 1,
      sym__newline,
  [3091] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(531), 1,
      sym_literal_content,
  [3098] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(533), 1,
      sym__newline,
  [3105] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(535), 1,
      sym_type_name,
  [3112] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(537), 1,
      sym__newline,
  [3119] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(539), 1,
      sym__newline,
  [3126] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(541), 1,
      sym__newline,
  [3133] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(543), 1,
      sym_anlu_identifier,
  [3140] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(545), 1,
      anon_sym_LPAREN,
  [3147] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(547), 1,
      anon_sym_RBRACK,
  [3154] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(549), 1,
      sym__newline,
  [3161] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(551), 1,
      aux_sym_condition_prefix_token2,
  [3168] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(553), 1,
      sym__newline,
  [3175] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(555), 1,
      sym__newline,
  [3182] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(557), 1,
      sym__newline,
  [3189] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(559), 1,
      sym_anlu_identifier,
  [3196] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(561), 1,
      sym__newline,
  [3203] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(563), 1,
      sym_step_text,
  [3210] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(565), 1,
      sym__newline,
  [3217] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(567), 1,
      sym__newline,
  [3224] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(569), 1,
      sym__newline,
  [3231] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(571), 1,
      anon_sym_EQ_EQ,
  [3238] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(573), 1,
      anon_sym_RBRACK,
  [3245] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(575), 1,
      anon_sym_COLON,
  [3252] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(577), 1,
      sym__newline,
  [3259] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(579), 1,
      sym_anlu_identifier,
  [3266] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(581), 1,
      anon_sym_LBRACE,
  [3273] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(583), 1,
      anon_sym_COLON,
  [3280] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(585), 1,
      ts_builtin_sym_end,
  [3287] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(587), 1,
      sym_step_text,
  [3294] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(589), 1,
      sym_anlu_identifier,
  [3301] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(591), 1,
      sym__newline,
  [3308] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(593), 1,
      sym__newline,
  [3315] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(595), 1,
      anon_sym_LBRACE,
  [3322] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(597), 1,
      sym__newline,
  [3329] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(599), 1,
      sym__newline,
  [3336] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(601), 1,
      anon_sym_LBRACK,
  [3343] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(603), 1,
      sym__newline,
  [3350] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(605), 1,
      sym__newline,
  [3357] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(607), 1,
      anon_sym_RPAREN,
  [3364] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(609), 1,
      sym__newline,
  [3371] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(611), 1,
      sym__newline,
  [3378] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(613), 1,
      sym__newline,
  [3385] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(615), 1,
      sym__newline,
  [3392] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(617), 1,
      anon_sym_DOT,
  [3399] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(619), 1,
      sym__newline,
  [3406] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(621), 1,
      anon_sym_LPAREN,
  [3413] = 2,
    ACTIONS(257), 1,
      sym_comment,
    ACTIONS(623), 1,
      aux_sym_guard_text_token1,
  [3420] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(625), 1,
      aux_sym_condition_token_token1,
  [3427] = 2,
    ACTIONS(3), 1,
      sym_comment,
    ACTIONS(627), 1,
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
  [SMALL_STATE(16)] = 605,
  [SMALL_STATE(17)] = 633,
  [SMALL_STATE(18)] = 661,
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
  [SMALL_STATE(41)] = 1214,
  [SMALL_STATE(42)] = 1232,
  [SMALL_STATE(43)] = 1250,
  [SMALL_STATE(44)] = 1268,
  [SMALL_STATE(45)] = 1296,
  [SMALL_STATE(46)] = 1314,
  [SMALL_STATE(47)] = 1332,
  [SMALL_STATE(48)] = 1350,
  [SMALL_STATE(49)] = 1368,
  [SMALL_STATE(50)] = 1386,
  [SMALL_STATE(51)] = 1404,
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
  [SMALL_STATE(63)] = 1683,
  [SMALL_STATE(64)] = 1706,
  [SMALL_STATE(65)] = 1718,
  [SMALL_STATE(66)] = 1734,
  [SMALL_STATE(67)] = 1750,
  [SMALL_STATE(68)] = 1766,
  [SMALL_STATE(69)] = 1788,
  [SMALL_STATE(70)] = 1810,
  [SMALL_STATE(71)] = 1828,
  [SMALL_STATE(72)] = 1848,
  [SMALL_STATE(73)] = 1859,
  [SMALL_STATE(74)] = 1876,
  [SMALL_STATE(75)] = 1887,
  [SMALL_STATE(76)] = 1898,
  [SMALL_STATE(77)] = 1915,
  [SMALL_STATE(78)] = 1932,
  [SMALL_STATE(79)] = 1943,
  [SMALL_STATE(80)] = 1960,
  [SMALL_STATE(81)] = 1971,
  [SMALL_STATE(82)] = 1988,
  [SMALL_STATE(83)] = 1999,
  [SMALL_STATE(84)] = 2016,
  [SMALL_STATE(85)] = 2033,
  [SMALL_STATE(86)] = 2048,
  [SMALL_STATE(87)] = 2058,
  [SMALL_STATE(88)] = 2074,
  [SMALL_STATE(89)] = 2088,
  [SMALL_STATE(90)] = 2104,
  [SMALL_STATE(91)] = 2114,
  [SMALL_STATE(92)] = 2128,
  [SMALL_STATE(93)] = 2138,
  [SMALL_STATE(94)] = 2150,
  [SMALL_STATE(95)] = 2166,
  [SMALL_STATE(96)] = 2176,
  [SMALL_STATE(97)] = 2190,
  [SMALL_STATE(98)] = 2206,
  [SMALL_STATE(99)] = 2219,
  [SMALL_STATE(100)] = 2232,
  [SMALL_STATE(101)] = 2245,
  [SMALL_STATE(102)] = 2258,
  [SMALL_STATE(103)] = 2271,
  [SMALL_STATE(104)] = 2284,
  [SMALL_STATE(105)] = 2295,
  [SMALL_STATE(106)] = 2304,
  [SMALL_STATE(107)] = 2313,
  [SMALL_STATE(108)] = 2322,
  [SMALL_STATE(109)] = 2335,
  [SMALL_STATE(110)] = 2344,
  [SMALL_STATE(111)] = 2357,
  [SMALL_STATE(112)] = 2368,
  [SMALL_STATE(113)] = 2381,
  [SMALL_STATE(114)] = 2394,
  [SMALL_STATE(115)] = 2407,
  [SMALL_STATE(116)] = 2420,
  [SMALL_STATE(117)] = 2431,
  [SMALL_STATE(118)] = 2444,
  [SMALL_STATE(119)] = 2457,
  [SMALL_STATE(120)] = 2470,
  [SMALL_STATE(121)] = 2481,
  [SMALL_STATE(122)] = 2494,
  [SMALL_STATE(123)] = 2507,
  [SMALL_STATE(124)] = 2520,
  [SMALL_STATE(125)] = 2533,
  [SMALL_STATE(126)] = 2543,
  [SMALL_STATE(127)] = 2551,
  [SMALL_STATE(128)] = 2561,
  [SMALL_STATE(129)] = 2569,
  [SMALL_STATE(130)] = 2579,
  [SMALL_STATE(131)] = 2587,
  [SMALL_STATE(132)] = 2595,
  [SMALL_STATE(133)] = 2603,
  [SMALL_STATE(134)] = 2611,
  [SMALL_STATE(135)] = 2619,
  [SMALL_STATE(136)] = 2629,
  [SMALL_STATE(137)] = 2639,
  [SMALL_STATE(138)] = 2649,
  [SMALL_STATE(139)] = 2657,
  [SMALL_STATE(140)] = 2665,
  [SMALL_STATE(141)] = 2673,
  [SMALL_STATE(142)] = 2681,
  [SMALL_STATE(143)] = 2689,
  [SMALL_STATE(144)] = 2699,
  [SMALL_STATE(145)] = 2709,
  [SMALL_STATE(146)] = 2717,
  [SMALL_STATE(147)] = 2725,
  [SMALL_STATE(148)] = 2733,
  [SMALL_STATE(149)] = 2743,
  [SMALL_STATE(150)] = 2753,
  [SMALL_STATE(151)] = 2761,
  [SMALL_STATE(152)] = 2771,
  [SMALL_STATE(153)] = 2779,
  [SMALL_STATE(154)] = 2789,
  [SMALL_STATE(155)] = 2797,
  [SMALL_STATE(156)] = 2804,
  [SMALL_STATE(157)] = 2811,
  [SMALL_STATE(158)] = 2818,
  [SMALL_STATE(159)] = 2825,
  [SMALL_STATE(160)] = 2832,
  [SMALL_STATE(161)] = 2839,
  [SMALL_STATE(162)] = 2846,
  [SMALL_STATE(163)] = 2853,
  [SMALL_STATE(164)] = 2860,
  [SMALL_STATE(165)] = 2867,
  [SMALL_STATE(166)] = 2874,
  [SMALL_STATE(167)] = 2881,
  [SMALL_STATE(168)] = 2888,
  [SMALL_STATE(169)] = 2895,
  [SMALL_STATE(170)] = 2902,
  [SMALL_STATE(171)] = 2909,
  [SMALL_STATE(172)] = 2916,
  [SMALL_STATE(173)] = 2923,
  [SMALL_STATE(174)] = 2930,
  [SMALL_STATE(175)] = 2937,
  [SMALL_STATE(176)] = 2944,
  [SMALL_STATE(177)] = 2951,
  [SMALL_STATE(178)] = 2958,
  [SMALL_STATE(179)] = 2965,
  [SMALL_STATE(180)] = 2972,
  [SMALL_STATE(181)] = 2979,
  [SMALL_STATE(182)] = 2986,
  [SMALL_STATE(183)] = 2993,
  [SMALL_STATE(184)] = 3000,
  [SMALL_STATE(185)] = 3007,
  [SMALL_STATE(186)] = 3014,
  [SMALL_STATE(187)] = 3021,
  [SMALL_STATE(188)] = 3028,
  [SMALL_STATE(189)] = 3035,
  [SMALL_STATE(190)] = 3042,
  [SMALL_STATE(191)] = 3049,
  [SMALL_STATE(192)] = 3056,
  [SMALL_STATE(193)] = 3063,
  [SMALL_STATE(194)] = 3070,
  [SMALL_STATE(195)] = 3077,
  [SMALL_STATE(196)] = 3084,
  [SMALL_STATE(197)] = 3091,
  [SMALL_STATE(198)] = 3098,
  [SMALL_STATE(199)] = 3105,
  [SMALL_STATE(200)] = 3112,
  [SMALL_STATE(201)] = 3119,
  [SMALL_STATE(202)] = 3126,
  [SMALL_STATE(203)] = 3133,
  [SMALL_STATE(204)] = 3140,
  [SMALL_STATE(205)] = 3147,
  [SMALL_STATE(206)] = 3154,
  [SMALL_STATE(207)] = 3161,
  [SMALL_STATE(208)] = 3168,
  [SMALL_STATE(209)] = 3175,
  [SMALL_STATE(210)] = 3182,
  [SMALL_STATE(211)] = 3189,
  [SMALL_STATE(212)] = 3196,
  [SMALL_STATE(213)] = 3203,
  [SMALL_STATE(214)] = 3210,
  [SMALL_STATE(215)] = 3217,
  [SMALL_STATE(216)] = 3224,
  [SMALL_STATE(217)] = 3231,
  [SMALL_STATE(218)] = 3238,
  [SMALL_STATE(219)] = 3245,
  [SMALL_STATE(220)] = 3252,
  [SMALL_STATE(221)] = 3259,
  [SMALL_STATE(222)] = 3266,
  [SMALL_STATE(223)] = 3273,
  [SMALL_STATE(224)] = 3280,
  [SMALL_STATE(225)] = 3287,
  [SMALL_STATE(226)] = 3294,
  [SMALL_STATE(227)] = 3301,
  [SMALL_STATE(228)] = 3308,
  [SMALL_STATE(229)] = 3315,
  [SMALL_STATE(230)] = 3322,
  [SMALL_STATE(231)] = 3329,
  [SMALL_STATE(232)] = 3336,
  [SMALL_STATE(233)] = 3343,
  [SMALL_STATE(234)] = 3350,
  [SMALL_STATE(235)] = 3357,
  [SMALL_STATE(236)] = 3364,
  [SMALL_STATE(237)] = 3371,
  [SMALL_STATE(238)] = 3378,
  [SMALL_STATE(239)] = 3385,
  [SMALL_STATE(240)] = 3392,
  [SMALL_STATE(241)] = 3399,
  [SMALL_STATE(242)] = 3406,
  [SMALL_STATE(243)] = 3413,
  [SMALL_STATE(244)] = 3420,
  [SMALL_STATE(245)] = 3427,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, SHIFT_EXTRA(),
  [5] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 0, 0, 0),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(137),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(177),
  [11] = {.entry = {.count = 1, .reusable = true}}, SHIFT(93),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(101),
  [15] = {.entry = {.count = 1, .reusable = true}}, SHIFT(203),
  [17] = {.entry = {.count = 1, .reusable = true}}, SHIFT(160),
  [19] = {.entry = {.count = 1, .reusable = true}}, SHIFT(161),
  [21] = {.entry = {.count = 1, .reusable = true}}, SHIFT(199),
  [23] = {.entry = {.count = 1, .reusable = true}}, SHIFT(232),
  [25] = {.entry = {.count = 1, .reusable = true}}, SHIFT(144),
  [27] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [29] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0),
  [31] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(137),
  [34] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(177),
  [37] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(93),
  [40] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(101),
  [43] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(203),
  [46] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(160),
  [49] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(161),
  [52] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(199),
  [55] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(232),
  [58] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(144),
  [61] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_source_file_repeat1, 2, 0, 0), SHIFT_REPEAT(2),
  [64] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_source_file, 1, 0, 0),
  [66] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [68] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0),
  [70] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(153),
  [73] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(231),
  [76] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(233),
  [79] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(239),
  [82] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(125),
  [85] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(97),
  [88] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_anlu_block_repeat1, 2, 0, 0), SHIFT_REPEAT(236),
  [91] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_block, 1, 0, 0),
  [93] = {.entry = {.count = 1, .reusable = true}}, SHIFT(153),
  [95] = {.entry = {.count = 1, .reusable = true}}, SHIFT(231),
  [97] = {.entry = {.count = 1, .reusable = true}}, SHIFT(233),
  [99] = {.entry = {.count = 1, .reusable = true}}, SHIFT(239),
  [101] = {.entry = {.count = 1, .reusable = true}}, SHIFT(125),
  [103] = {.entry = {.count = 1, .reusable = true}}, SHIFT(97),
  [105] = {.entry = {.count = 1, .reusable = true}}, SHIFT(236),
  [107] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_block, 2, 0, 0),
  [109] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guards_section, 3, 0, 11),
  [111] = {.entry = {.count = 1, .reusable = true}}, SHIFT(243),
  [113] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_inputs_section, 3, 0, 11),
  [115] = {.entry = {.count = 1, .reusable = true}}, SHIFT(176),
  [117] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_inputs_section_repeat1, 2, 0, 0),
  [119] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_inputs_section_repeat1, 2, 0, 0), SHIFT_REPEAT(176),
  [122] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_cases_section, 3, 0, 11),
  [124] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_edge_cases_section_repeat1, 2, 0, 0),
  [126] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_edge_cases_section_repeat1, 2, 0, 0), SHIFT_REPEAT(243),
  [129] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_guards_section_repeat1, 2, 0, 0),
  [131] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_guards_section_repeat1, 2, 0, 0), SHIFT_REPEAT(243),
  [134] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_case_item, 5, 0, 28),
  [136] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_section, 3, 0, 11),
  [138] = {.entry = {.count = 1, .reusable = true}}, SHIFT(240),
  [140] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_item, 3, 0, 18),
  [142] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_item, 6, 0, 21),
  [144] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_item, 5, 0, 21),
  [146] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_logic_section_repeat1, 2, 0, 0),
  [148] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_logic_section_repeat1, 2, 0, 0), SHIFT_REPEAT(240),
  [151] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_item, 5, 0, 24),
  [153] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_item, 4, 0, 22),
  [155] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_returns_section, 3, 0, 12),
  [157] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_header, 4, 0, 1),
  [159] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_purpose_section, 3, 0, 10),
  [161] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_section, 3, 0, 13),
  [163] = {.entry = {.count = 1, .reusable = true}}, SHIFT(189),
  [165] = {.entry = {.count = 1, .reusable = false}}, SHIFT(64),
  [167] = {.entry = {.count = 1, .reusable = true}}, SHIFT(105),
  [169] = {.entry = {.count = 1, .reusable = true}}, SHIFT(106),
  [171] = {.entry = {.count = 1, .reusable = false}}, SHIFT(107),
  [173] = {.entry = {.count = 1, .reusable = true}}, SHIFT(90),
  [175] = {.entry = {.count = 1, .reusable = true}}, SHIFT(92),
  [177] = {.entry = {.count = 1, .reusable = true}}, SHIFT(162),
  [179] = {.entry = {.count = 1, .reusable = true}}, SHIFT(164),
  [181] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_close, 2, 0, 0),
  [183] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_block, 3, 0, 0),
  [185] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_block, 3, 0, 0),
  [187] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_module_directive, 3, 0, 1),
  [189] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_block, 3, 0, 6),
  [191] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_directive, 1, 0, 0),
  [193] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_version_directive, 3, 0, 2),
  [195] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_target_directive, 3, 0, 3),
  [197] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_imports_directive, 3, 0, 4),
  [199] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_block, 2, 0, 0),
  [201] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_close, 2, 0, 0),
  [203] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_block, 3, 0, 0),
  [205] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_invariant_block, 2, 0, 0),
  [207] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_close, 2, 0, 0),
  [209] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_block, 2, 0, 0),
  [211] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_close, 2, 0, 0),
  [213] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_block, 2, 0, 0),
  [215] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_block, 3, 0, 0),
  [217] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_property_close, 2, 0, 0),
  [219] = {.entry = {.count = 1, .reusable = false}}, SHIFT(59),
  [221] = {.entry = {.count = 1, .reusable = true}}, SHIFT(59),
  [223] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_text, 1, 0, 0),
  [225] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0),
  [227] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0), SHIFT_REPEAT(59),
  [230] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_condition_text_repeat1, 2, 0, 0), SHIFT_REPEAT(59),
  [233] = {.entry = {.count = 1, .reusable = true}}, SHIFT(64),
  [235] = {.entry = {.count = 1, .reusable = true}}, SHIFT(230),
  [237] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0), SHIFT_REPEAT(64),
  [240] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0),
  [242] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_type_block_repeat1, 2, 0, 0), SHIFT_REPEAT(176),
  [245] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_token, 1, 0, 0),
  [247] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_condition_token, 1, 0, 0),
  [249] = {.entry = {.count = 1, .reusable = false}}, SHIFT(145),
  [251] = {.entry = {.count = 1, .reusable = true}}, SHIFT(198),
  [253] = {.entry = {.count = 1, .reusable = true}}, SHIFT(234),
  [255] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_identifier, 1, 0, 0),
  [257] = {.entry = {.count = 1, .reusable = false}}, SHIFT_EXTRA(),
  [259] = {.entry = {.count = 1, .reusable = false}}, SHIFT(200),
  [261] = {.entry = {.count = 1, .reusable = false}}, SHIFT(182),
  [263] = {.entry = {.count = 1, .reusable = false}}, SHIFT(53),
  [265] = {.entry = {.count = 1, .reusable = false}}, SHIFT(77),
  [267] = {.entry = {.count = 1, .reusable = true}}, SHIFT(154),
  [269] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_test_block_repeat1, 2, 0, 0), SHIFT_REPEAT(64),
  [272] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_test_block_repeat1, 2, 0, 0),
  [274] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_header, 5, 0, 1),
  [276] = {.entry = {.count = 1, .reusable = false}}, SHIFT(170),
  [278] = {.entry = {.count = 1, .reusable = false}}, SHIFT(159),
  [280] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_header, 4, 0, 1),
  [282] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 4, 0, 15),
  [284] = {.entry = {.count = 1, .reusable = false}}, SHIFT(165),
  [286] = {.entry = {.count = 1, .reusable = false}}, SHIFT(172),
  [288] = {.entry = {.count = 1, .reusable = true}}, SHIFT(244),
  [290] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 1, 0, 19),
  [292] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 5, 0, 15),
  [294] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 6, 0, 21),
  [296] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_field, 5, 0, 21),
  [298] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 2, 0, 23),
  [300] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 3, 0, 27),
  [302] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_list_type, 3, 0, 20),
  [304] = {.entry = {.count = 1, .reusable = true}}, SHIFT(60),
  [306] = {.entry = {.count = 1, .reusable = true}}, SHIFT(17),
  [308] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_property_block_repeat1, 2, 0, 0),
  [310] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_property_block_repeat1, 2, 0, 0), SHIFT_REPEAT(172),
  [313] = {.entry = {.count = 1, .reusable = true}}, SHIFT(82),
  [315] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_custom_type, 1, 0, 0),
  [317] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_invariant_block_repeat1, 2, 0, 0),
  [319] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_invariant_block_repeat1, 2, 0, 0), SHIFT_REPEAT(159),
  [322] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_primitive_type, 1, 0, 0),
  [324] = {.entry = {.count = 1, .reusable = true}}, SHIFT(157),
  [326] = {.entry = {.count = 1, .reusable = true}}, SHIFT(75),
  [328] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_map_type, 5, 0, 29),
  [330] = {.entry = {.count = 1, .reusable = true}}, SHIFT(142),
  [332] = {.entry = {.count = 1, .reusable = true}}, SHIFT(15),
  [334] = {.entry = {.count = 1, .reusable = true}}, SHIFT(211),
  [336] = {.entry = {.count = 1, .reusable = true}}, SHIFT(150),
  [338] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_input_constraints, 1, 0, 0),
  [340] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_error_args_repeat1, 2, 0, 0), SHIFT_REPEAT(85),
  [343] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_error_args_repeat1, 2, 0, 0),
  [345] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_import_list_repeat1, 2, 0, 0), SHIFT_REPEAT(136),
  [348] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_import_list_repeat1, 2, 0, 0),
  [350] = {.entry = {.count = 1, .reusable = true}}, SHIFT(102),
  [352] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_list, 2, 0, 0),
  [354] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_spec, 1, 0, 0),
  [356] = {.entry = {.count = 1, .reusable = true}}, SHIFT(138),
  [358] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_value, 1, 0, 0),
  [360] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_quoted_string, 1, 0, 0),
  [362] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_boolean, 1, 0, 0),
  [364] = {.entry = {.count = 1, .reusable = true}}, SHIFT(44),
  [366] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_args, 1, 0, 0),
  [368] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_guard_text, 1, 0, 0),
  [370] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_depends_list_repeat1, 2, 0, 0), SHIFT_REPEAT(102),
  [373] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_depends_list_repeat1, 2, 0, 0),
  [375] = {.entry = {.count = 1, .reusable = true}}, SHIFT(136),
  [377] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_import_list, 2, 0, 0),
  [379] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_field_constraints, 1, 0, 0),
  [381] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_args, 2, 0, 0),
  [383] = {.entry = {.count = 1, .reusable = false}}, SHIFT(83),
  [385] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_input_constraints_repeat1, 2, 0, 0),
  [387] = {.entry = {.count = 1, .reusable = true}}, SHIFT(70),
  [389] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_input_constraints_repeat1, 2, 0, 0), SHIFT_REPEAT(60),
  [392] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_import_list, 1, 0, 0),
  [394] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_test_args_repeat1, 2, 0, 0), SHIFT_REPEAT(44),
  [397] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_test_args_repeat1, 2, 0, 0),
  [399] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_depends_list, 1, 0, 0),
  [401] = {.entry = {.count = 1, .reusable = true}}, SHIFT(167),
  [403] = {.entry = {.count = 1, .reusable = true}}, SHIFT(171),
  [405] = {.entry = {.count = 1, .reusable = true}}, SHIFT(85),
  [407] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_args, 1, 0, 0),
  [409] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_args, 2, 0, 0),
  [411] = {.entry = {.count = 1, .reusable = false}}, SHIFT(206),
  [413] = {.entry = {.count = 1, .reusable = false}}, SHIFT(134),
  [415] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_property_assertion, 2, 0, 5),
  [417] = {.entry = {.count = 1, .reusable = true}}, SHIFT(179),
  [419] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_reference, 3, 0, 0),
  [421] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_invariant_assertion, 2, 0, 5),
  [423] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_condition_text, 1, 0, 0),
  [425] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_type_spec, 2, 0, 0),
  [427] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_assertion, 4, 0, 16),
  [429] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_header, 6, 0, 17),
  [431] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_property_header, 6, 0, 17),
  [433] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_arrow, 1, 0, 0),
  [435] = {.entry = {.count = 1, .reusable = false}}, SHIFT(214),
  [437] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_invariant_header, 4, 0, 8),
  [439] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_anlu_reference, 1, 0, 0),
  [441] = {.entry = {.count = 1, .reusable = false}}, SHIFT(109),
  [443] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_state_prefix, 3, 0, 25),
  [445] = {.entry = {.count = 1, .reusable = false}}, SHIFT(184),
  [447] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_constraint_pair, 3, 0, 30),
  [449] = {.entry = {.count = 1, .reusable = true}}, SHIFT(23),
  [451] = {.entry = {.count = 1, .reusable = true}}, SHIFT(38),
  [453] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_target_name, 1, 0, 0),
  [455] = {.entry = {.count = 1, .reusable = true}}, SHIFT(131),
  [457] = {.entry = {.count = 1, .reusable = true}}, SHIFT(133),
  [459] = {.entry = {.count = 1, .reusable = true}}, SHIFT(122),
  [461] = {.entry = {.count = 1, .reusable = true}}, SHIFT(221),
  [463] = {.entry = {.count = 1, .reusable = true}}, SHIFT(29),
  [465] = {.entry = {.count = 1, .reusable = true}}, SHIFT(39),
  [467] = {.entry = {.count = 1, .reusable = true}}, SHIFT(30),
  [469] = {.entry = {.count = 1, .reusable = true}}, SHIFT(52),
  [471] = {.entry = {.count = 1, .reusable = true}}, SHIFT(22),
  [473] = {.entry = {.count = 1, .reusable = true}}, SHIFT(74),
  [475] = {.entry = {.count = 1, .reusable = true}}, SHIFT(78),
  [477] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_extends_clause, 2, 0, 7),
  [479] = {.entry = {.count = 1, .reusable = true}}, SHIFT(42),
  [481] = {.entry = {.count = 1, .reusable = true}}, SHIFT(169),
  [483] = {.entry = {.count = 1, .reusable = true}}, SHIFT(128),
  [485] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_call, 4, 0, 14),
  [487] = {.entry = {.count = 1, .reusable = true}}, SHIFT(175),
  [489] = {.entry = {.count = 1, .reusable = true}}, SHIFT(72),
  [491] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_bullet, 1, 0, 0),
  [493] = {.entry = {.count = 1, .reusable = true}}, SHIFT(156),
  [495] = {.entry = {.count = 1, .reusable = true}}, SHIFT(186),
  [497] = {.entry = {.count = 1, .reusable = true}}, SHIFT(32),
  [499] = {.entry = {.count = 1, .reusable = true}}, SHIFT(146),
  [501] = {.entry = {.count = 1, .reusable = true}}, SHIFT(194),
  [503] = {.entry = {.count = 1, .reusable = true}}, SHIFT(205),
  [505] = {.entry = {.count = 1, .reusable = true}}, SHIFT(195),
  [507] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_description_text, 1, 0, 0),
  [509] = {.entry = {.count = 1, .reusable = true}}, SHIFT(20),
  [511] = {.entry = {.count = 1, .reusable = true}}, SHIFT(210),
  [513] = {.entry = {.count = 1, .reusable = true}}, SHIFT(139),
  [515] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_test_call, 3, 0, 14),
  [517] = {.entry = {.count = 1, .reusable = true}}, SHIFT(31),
  [519] = {.entry = {.count = 1, .reusable = true}}, SHIFT(173),
  [521] = {.entry = {.count = 1, .reusable = true}}, SHIFT(28),
  [523] = {.entry = {.count = 1, .reusable = true}}, SHIFT(40),
  [525] = {.entry = {.count = 1, .reusable = true}}, SHIFT(212),
  [527] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_literal_header, 4, 0, 9),
  [529] = {.entry = {.count = 1, .reusable = true}}, SHIFT(80),
  [531] = {.entry = {.count = 1, .reusable = true}}, SHIFT(129),
  [533] = {.entry = {.count = 1, .reusable = true}}, SHIFT(48),
  [535] = {.entry = {.count = 1, .reusable = true}}, SHIFT(222),
  [537] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_text, 1, 0, 0),
  [539] = {.entry = {.count = 1, .reusable = true}}, SHIFT(19),
  [541] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_spec, 1, 2, 0),
  [543] = {.entry = {.count = 1, .reusable = true}}, SHIFT(218),
  [545] = {.entry = {.count = 1, .reusable = true}}, SHIFT(62),
  [547] = {.entry = {.count = 1, .reusable = true}}, SHIFT(152),
  [549] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_returns_text, 1, 0, 0),
  [551] = {.entry = {.count = 1, .reusable = true}}, SHIFT(225),
  [553] = {.entry = {.count = 1, .reusable = true}}, SHIFT(21),
  [555] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 2, 0, 19),
  [557] = {.entry = {.count = 1, .reusable = true}}, SHIFT(140),
  [559] = {.entry = {.count = 1, .reusable = true}}, SHIFT(158),
  [561] = {.entry = {.count = 1, .reusable = true}}, SHIFT(141),
  [563] = {.entry = {.count = 1, .reusable = false}}, SHIFT(84),
  [565] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_edge_behavior_text, 1, 0, 0),
  [567] = {.entry = {.count = 1, .reusable = true}}, SHIFT(13),
  [569] = {.entry = {.count = 1, .reusable = true}}, SHIFT(24),
  [571] = {.entry = {.count = 1, .reusable = true}}, SHIFT(51),
  [573] = {.entry = {.count = 1, .reusable = true}}, SHIFT(166),
  [575] = {.entry = {.count = 1, .reusable = true}}, SHIFT(27),
  [577] = {.entry = {.count = 1, .reusable = true}}, SHIFT(16),
  [579] = {.entry = {.count = 1, .reusable = true}}, SHIFT(178),
  [581] = {.entry = {.count = 1, .reusable = true}}, SHIFT(180),
  [583] = {.entry = {.count = 1, .reusable = true}}, SHIFT(26),
  [585] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
  [587] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_condition_prefix, 3, 0, 0),
  [589] = {.entry = {.count = 1, .reusable = true}}, SHIFT(181),
  [591] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_output_binding, 2, 0, 26),
  [593] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 3, 0, 23),
  [595] = {.entry = {.count = 1, .reusable = true}}, SHIFT(183),
  [597] = {.entry = {.count = 1, .reusable = true}}, SHIFT(46),
  [599] = {.entry = {.count = 1, .reusable = true}}, SHIFT(65),
  [601] = {.entry = {.count = 1, .reusable = true}}, SHIFT(226),
  [603] = {.entry = {.count = 1, .reusable = true}}, SHIFT(66),
  [605] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_call, 3, 0, 31),
  [607] = {.entry = {.count = 1, .reusable = true}}, SHIFT(238),
  [609] = {.entry = {.count = 1, .reusable = true}}, SHIFT(67),
  [611] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_logic_step, 4, 0, 27),
  [613] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_call, 4, 0, 31),
  [615] = {.entry = {.count = 1, .reusable = true}}, SHIFT(120),
  [617] = {.entry = {.count = 1, .reusable = true}}, SHIFT(69),
  [619] = {.entry = {.count = 1, .reusable = true}}, SHIFT(35),
  [621] = {.entry = {.count = 1, .reusable = true}}, SHIFT(25),
  [623] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_bullet, 1, 0, 0),
  [625] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_arrow, 1, 0, 0),
  [627] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_error_spec, 1, 1, 0),
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
