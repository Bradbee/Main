#include <stdlib.h>
#include <stdio.h>
#include "parser.h"

void initParser(Parser* parser, Lexer* lexer) {
    parser->lexer = lexer;
    parser->hadError = false;
    parser->panicMode = false;
    advance(parser); // Initialize the first token
}

static void advance(Parser* parser) {
    parser->previous = parser->current;
    parser->current = scanToken(parser->lexer);
}

static bool check(Parser* parser, TokenType type) {
    return parser->current.type == type;
}

static bool match(Parser* parser, TokenType type) {
    if (!check(parser, type)) return false;
    advance(parser);
    return true;
}

static Expr* expression(Parser* parser);
static Expr* equality(Parser* parser);
static Expr* comparison(Parser* parser);
static Expr* term(Parser* parser);
static Expr* factor(Parser* parser);
static Expr* unary(Parser* parser);
static Expr* primary(Parser* parser);

Expr* parse(Parser* parser) {
    return expression(parser);
}

static Expr* expression(Parser* parser) {
    return equality(parser);
}

static Expr* equality(Parser* parser) {
    Expr* expr = comparison(parser);

    while (match(parser, TOKEN_BANG_EQUAL) || match(parser, TOKEN_EQUAL_EQUAL)) {
        Token operator = parser->previous;
        Expr* right = comparison(parser);
        expr = (Expr*)malloc(sizeof(Expr));
        expr->type = EXPR_BINARY;
        expr->left = expr;
        expr->right = right;
        expr->operator = operator;
    }

    return expr;
}

static Expr* comparison(Parser* parser) {
    Expr* expr = term(parser);

    while (match(parser, TOKEN_GREATER) || match(parser, TOKEN_GREATER_EQUAL) ||
           match(parser, TOKEN_LESS) || match(parser, TOKEN_LESS_EQUAL)) {
        Token operator = parser->previous;
        Expr* right = term(parser);
        expr = (Expr*)malloc(sizeof(Expr));
        expr->type = EXPR_BINARY;
        expr->left = expr;
        expr->right = right;
        expr->operator = operator;
    }

    return expr;
}

static Expr* term(Parser* parser) {
    Expr* expr = factor(parser);

    while (match(parser, TOKEN_MINUS) || match(parser, TOKEN_PLUS)) {
        Token operator = parser->previous;
        Expr* right = factor(parser);
        expr = (Expr*)malloc(sizeof(Expr));
        expr->type = EXPR_BINARY;
        expr->left = expr;
        expr->right = right;
        expr->operator = operator;
    }

    return expr;
}

static Expr* factor(Parser* parser) {
    Expr* expr = unary(parser);

    while (match(parser, TOKEN_SLASH) || match(parser, TOKEN_STAR)) {
        Token operator = parser->previous;
        Expr* right = unary(parser);
        expr = (Expr*)malloc(sizeof(Expr));
        expr->type = EXPR_BINARY;
        expr->left = expr;
        expr->right = right;
        expr->operator = operator;
    }

    return expr;
}

static Expr* unary(Parser* parser) {
    if (match(parser, TOKEN_BANG) || match(parser, TOKEN_MINUS)) {
        Token operator = parser->previous;
        Expr* right = unary(parser);
        Expr* expr = (Expr*)malloc(sizeof(Expr));
        expr->type = EXPR_UNARY;
        expr->operator = operator;
        expr->right = right;
        return expr;
    }

    return primary(parser);
}

static Expr* primary(Parser* parser) {
    if (match(parser, TOKEN_FALSE)) return literal(parser, false);
    if (match(parser, TOKEN_TRUE)) return literal(parser, true);
    if (match(parser, TOKEN_NIL)) return literal(parser, NULL);

    if (match(parser, TOKEN_NUMBER) || match(parser, TOKEN_STRING)) {
        Expr* expr = (Expr*)malloc(sizeof(Expr));
        expr->type = EXPR_LITERAL;
        expr->value = parser->previous;
        return expr;
    }

    if (match(parser, TOKEN_LEFT_PAREN)) {
        Expr* expr = expression(parser);
        consume(parser, TOKEN_RIGHT_PAREN, "Expect ')' after expression.");
        return expr;
    }

    // Error handling
    return NULL;
}

static Expr* literal(Parser* parser, Token value) {
    Expr* expr = (Expr*)malloc(sizeof(Expr));
    expr->type = EXPR_LITERAL;
    expr->value = value;
    return expr;
}

static void consume(Parser* parser, TokenType type, const char* message) {
    if (check(parser, type)) {
        advance(parser);
        return;
    }

    // Error handling
}
