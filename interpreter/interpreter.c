#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "interpreter.h"

void initEnvironment(Environment* env) {
    env->entries = NULL;
}

void defineVariable(Environment* env, char* name, Token value) {
    EnvEntry* entry = (EnvEntry*)malloc(sizeof(EnvEntry));
    entry->name = name;
    entry->value = value;
    entry->next = env->entries;
    env->entries = entry;
}

Token getVariable(Environment* env, char* name) {
    for (EnvEntry* entry = env->entries; entry != NULL; entry = entry->next) {
        if (strcmp(entry->name, name) == 0) {
            return entry->value;
        }
    }
    Token errorToken;
    errorToken.type = TOKEN_ERROR;
    errorToken.start = "Variable not defined.";
    errorToken.length = strlen("Variable not defined.");
    errorToken.line = -1;
    return errorToken;
}

void initInterpreter(Interpreter* interpreter, Environment* env) {
    interpreter->environment = env;
}

static void interpretExpression(Interpreter* interpreter, Expr* expr) {
    switch (expr->type) {
        case EXPR_LITERAL:
            printf("Literal: %.*s\n", expr->value.length, expr->value.start);
            break;
        case EXPR_BINARY:
            interpretExpression(interpreter, expr->left);
            interpretExpression(interpreter, expr->right);
            printf("Binary Operator: %.*s\n", expr->operator.length, expr->operator.start);
            break;
        case EXPR_UNARY:
            interpretExpression(interpreter, expr->right);
            printf("Unary Operator: %.*s\n", expr->operator.length, expr->operator.start);
            break;
        default:
            break;
    }
}

void interpret(Interpreter* interpreter, Expr* expression) {
    interpretExpression(interpreter, expression);
}
