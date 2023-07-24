#ifndef SEALANG_H
#define SEALANG_H

#include "Python.h"

#include "clang/AST/OperationKinds.h"
#include "clang-c/Index.h"
#include "clang-c/CXString.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \brief Returns string representation of unary and binary operators
 */
CXString clang_Cursor_getOperatorString(CXCursor cursor);

/**
 * \brief Returns Opcode of binary operator
 */
clang::BinaryOperatorKind clang_Cursor_getBinaryOpcode(CXCursor cursor);

/**
 * \brief Returns Opcode of unary operator
 */
clang::UnaryOperatorKind clang_Cursor_getUnaryOpcode(CXCursor cursor);

/**
 * \brief Returns string representation of literal cursor (1.f, 1000L, etc)
 */
CXString clang_Cursor_getLiteralString(CXCursor cursor);

/**
 * \brief Returns for-loop init cursor [for(init;cond;inc)], or CXCursor_NoDeclFound if there is no decl,
 * or CXCursor_InvalidCode if C is not CXCursor_ForStmt
 */
// CXCursor clang_getForStmtInit(CXCursor C);

/**
 * \brief Returns for-loop condition cursor [for(init;cond;inc)], or CXCursor_NoDeclFound if there is no decl,
 * or CXCursor_InvalidCode if C is not CXCursor_ForStmt
 */
// CXCursor clang_getForStmtCond(CXCursor C);

/**
 * \brief Returns for-loop increment cursor [for(init;cond;inc)], or CXCursor_NoDeclFound if there is no decl,
 * or CXCursor_InvalidCode if C is not CXCursor_ForStmt
 */
// CXCursor clang_getForStmtInc(CXCursor C);

/**
 * \brief Returns for-loop body, or CXCursor_NoDeclFound if there is no decl,
 * or CXCursor_InvalidCode if C is not CXCursor_ForStmt
 */
// CXCursor clang_getForStmtBody(CXCursor C);


#ifdef __cplusplus
}
#endif

#endif