#ifndef PARSER_H
#define PARSER_H

#include "lexer.h"

typedef enum {
    EXPR_BINARY,
    EXPR_UNARY,
    EXPR_LITERAL,
    EXPR_GROUPING,
    EXPR_VARIABLE,
    EXPR_ASSIGNMENT,
    EXPR_LOGICAL,
    EXPR_CALL,
    EXPR_FUNCTION,
    EXPR_CLASS,
    EXPR_GET,
    EXPR_SET,
    EXPR_THIS,
    EXPR_SUPER,
} ExprType;

typedef struct Expr {
    ExprType type;
    struct Expr* left;
    struct Expr* right;
    Token operator;
    Token value;
} Expr;

typedef struct {
    Lexer* lexer;
    Token current;
    Token previous;
    bool hadError;
    bool panicMode;
} Parser;

void initParser(Parser* parser, Lexer* lexer);
Expr* parse(Parser* parser);

#endif
