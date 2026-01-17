/**
 * External scanner for NL (Natural Language Source)
 *
 * Handles literal block content with proper brace matching.
 * Literal blocks preserve all content exactly, including nested braces.
 */

#include "tree_sitter/parser.h"
#include <wctype.h>

enum TokenType {
  LITERAL_CONTENT,
};

void *tree_sitter_nl_external_scanner_create() { return NULL; }

void tree_sitter_nl_external_scanner_destroy(void *payload) {}

unsigned tree_sitter_nl_external_scanner_serialize(void *payload,
                                                    char *buffer) {
  return 0;
}

void tree_sitter_nl_external_scanner_deserialize(void *payload,
                                                  const char *buffer,
                                                  unsigned length) {}

/**
 * Scan literal block content.
 *
 * Matches everything from after the opening { until a } at the start of a line
 * AND brace depth returns to 0. This handles nested braces in code.
 */
static bool scan_literal_content(TSLexer *lexer) {
  bool has_content = false;
  int brace_depth = 1; // We're already inside the opening {

  while (lexer->lookahead) {
    // Check for closing brace at start of line (after optional whitespace)
    if (lexer->lookahead == '\n') {
      lexer->advance(lexer, false);
      has_content = true;

      // Skip leading whitespace on new line
      while (lexer->lookahead == ' ' || lexer->lookahead == '\t') {
        lexer->advance(lexer, false);
      }

      // Check if this line starts with a closing brace AND we're at depth 1
      // (meaning this close would bring us to depth 0 = end of literal)
      if (lexer->lookahead == '}' && brace_depth == 1) {
        // This is the end of the literal block
        // Don't consume the }, let the grammar handle it
        if (has_content) {
          lexer->result_symbol = LITERAL_CONTENT;
          return true;
        }
        return false;
      }
      continue;
    }

    // Track brace depth for nested content
    if (lexer->lookahead == '{') {
      brace_depth++;
    } else if (lexer->lookahead == '}') {
      brace_depth--;
    }

    lexer->advance(lexer, false);
    has_content = true;
  }

  // EOF reached
  if (has_content) {
    lexer->result_symbol = LITERAL_CONTENT;
    return true;
  }
  return false;
}

bool tree_sitter_nl_external_scanner_scan(void *payload, TSLexer *lexer,
                                           const bool *valid_symbols) {
  if (valid_symbols[LITERAL_CONTENT]) {
    return scan_literal_content(lexer);
  }
  return false;
}
