from typing import Union, Any

from lex.tokens import *

def checkIgnore(line, p) -> int:
    if line[p:p + 6] == "public" and (p + 6 >= len(line) or not line[p + 6].isalnum()):
        return 6
    if line[p:p + 9] == "protected" and (p + 9 >= len(line) or not line[p + 9].isalnum()):
        return 9
    if line[p:p + 7] == "private" and (p + 7 >= len(line) or not line[p + 7].isalnum()):
        return 7
    if line[p:p + 6] == "static" and (p + 6 >= len(line) or not line[p + 6].isalnum()):
        return 6
    return 0


# def checkConstant(line, p):
#     if line[p:p + 4] == "true" and (p + 4 >= len(line) or not line[p + 4].isalnum()):
#         return 4, 0
#     if line[p:p + 5] == "false" and (p + 5 >= len(line) or not line[p + 5].isalnum()):
#         return 5, 0
#     if line[p].isdigit():
#         z = p
#         e = 0
#         while p < len(line) and line[z].isalnum():
#             z += 1
#             if z + 1 < len(line) and line[z + 1].isalpha() and line[z + 1] not in " ;{}()+-/*":
#                 e = 1
#         if e == 0:
#             return z - p, 0
#         else:
#             return z - p, 10000
#
#     if line[p] == '\'':
#         if line[p + 1] == '\'':
#             return 2, 0
#         else:
#             if line[p:p + 3] == "\'\\\'":
#                 return 4, 0
#             else:
#                 return 3, 0
#
#     if line[p] == '\"':
#         z = p + 1
#         while line[z] != '\"' or line[z - 1] == '\\':
#             z += 1
#             if z + 1 == len(line):
#                 return z - p + 1, 10002
#         if '\\' in line[p + 1:z - p + 1] and not "\\n" in line[p + 1:z - p + 1]:  # "\n"
#             return z - p + 1, 10001
#         return z - p + 1, 0
#
#     return 0, 0
def checkConstant(line, p):
    if line[p:p + 4] == "true" and (p + 4 >= len(line) or not line[p + 4].isalnum()):
        return 4, 0, True
    if line[p:p + 5] == "false" and (p + 5 >= len(line) or not line[p + 5].isalnum()):
        return 5, 0, False
    if line[p].isdigit() or line[p] == '-':
        z = p
        e = 0
        while z < len(line) and (line[z].isalnum() or line[z] == '.' or line[z] == 'j' or line[z] == '-'):
            if line[z] == 'j':
                e = 1
            if line[z] == '-' and z > p:
                break
            z += 1
        if e == 0:
            return z - p, 0, int(line[p:z])
        else:
            return z - p, 10000, -1

    if line[p] == '\'':
        if line[p + 1] == '\'':
            return 2, 0, ''
        else:
            if line[p:p + 3] == "\'\\\'":
                return 4, 0, "\'\\\'"
            else:
                return 3, 0, line[p:p + 3]

    if line[p] == '\"':
        z = p + 1
        while line[z] != '\"' or line[z - 1] == '\\':
            z += 1
            if z + 1 == len(line):
                return z - p + 1, 10002, -1
        if '\\' in line[p + 1:z - p + 1] and not "\\n" in line[p + 1:z - p + 1]:  # "\n"
            return z - p + 1, 10001, -1
        return z - p + 1, 0, line[p:z+1]

    return 0, 0, -1

def checkType(line, p) -> int:
    if line[p:p + 4] == "bool" and (p + 4 >= len(line) or not line[p + 4].isalnum()):
        return 4
    if line[p:p + 4] == "char" and (p + 4 >= len(line) or not line[p + 4].isalnum()):
        return 4
    if line[p:p + 4] == "void" and (p + 4 >= len(line) or not line[p + 4].isalnum()):
        return 4
    if line[p:p + 6] == "String" and (p + 6 >= len(line) or not line[p + 6].isalnum()):
        return 6
    if line[p:p + 3] == "int" and (p + 3 >= len(line) or not line[p + 3].isalnum()):
        return 3
    return 0


def checkVar(line, p) -> int:
    if line[p].isalpha():
        z = p
        while p+1 < len(line) and p < len(line) and line[z].isalnum():
            z += 1
        return z - p
    return 0


def parseLine(line):
    p = 0
    res = []
    while p < len(line):
        if line[p] == ' ':
            p += 1
            continue
        if line[p] == '\n':
            p += 1
            continue
        x = checkIgnore(line, p)
        if x > 0:
            p += x
            continue

        if line[p] == '{':
            res.append(BOpen())
            p += 1
            continue
        if line[p] == '}':
            res.append(BClose())
            p += 1
            continue
        if line[p] == '(':
            res.append(POpen())
            p += 1
            continue
        if line[p] == ')':
            res.append(PClose())
            p += 1
            continue
        if line[p] == '[':
            res.append(SBOpen())
            p += 1
            continue
        if line[p] == ']':
            res.append(SBClose())
            p += 1
            continue
        if line[p] == ';':
            res.append(Semicolon())
            p += 1
            continue
        if line[p] == '.':
            res.append(Dot())
            p += 1
            continue
        if line[p:p + 2] in ["==", "<=", ">="]:
            res.append(Comp(line[p:p + 2]))
            p += 2
            continue
        if line[p] in ['>', '<']:
            res.append(Comp(line[p]))
            p += 1
            continue
        if line[p] == '=':
            res.append(SetOp())
            p += 1
            continue


        if line[p:p + 5] == "while" and (p + 5 >= len(line) or not line[p + 5].isalnum()):
            res.append(While())
            p += 5
            continue
        if line[p:p + 3] == "for" and (p + 3 >= len(line) or not line[p + 3].isalnum()):
            res.append(For())
            p += 3
            continue
        if line[p:p + 3] == "new" and (p + 3 >= len(line) or not line[p + 3].isalnum()):
            res.append(New())
            p += 3
            continue
        if line[p:p + 2] == "do" and (p + 2 >= len(line) or not line[p + 2].isalnum()):
            res.append(Do())
            p += 2
            continue
        if line[p:p + 2] == "if" and (p + 2 >= len(line) or not line[p + 2].isalnum()):
            res.append(If())
            p += 2
            continue
        if line[p:p + 4] == "else" and (p + 4 >= len(line) or not line[p + 4].isalnum()):
            res.append(Else())
            p += 4
            continue
        if line[p:p + 6] == "switch" and (p + 6 >= len(line) or not line[p + 6].isalnum()):
            res.append(Switch())
            p += 6
            continue
        if line[p:p + 4] == "case" and (p + 4 >= len(line) or not line[p + 4].isalnum()):
            res.append(Case())
            p += 4

        x, e, value = checkConstant(line, p)
        if x > 0:
            if e == 10000 and not Token.error:
                print(f"\033[91mERROR bad identifier {line[p:p + x]}\033[0m")
                Token.error = 1
                return res, 1
            elif e == 10001 and not Token.error:
                print(f"\033[91mERROR unrecognized excape sequence {line[p:p + x]}\033[0m")
                Token.error = 1
                return res, 1
            elif e == 10002 and not Token.error:
                print(f"\033[91mERROR unterminated string literal {line[p:p + x]}\033[0m")
                Token.error = 1
                return res, 1
            else:
                res.append(Const(value))
            p += x
        if line[p] in ['+', '-', '*', '/', '%']:
            res.append(Arifm(line[p]))
            p += 1
            continue

        x = checkType(line, p)
        if x > 0:
            res.append(Type(line[p:p + x]))
            p += x
            continue
        x = checkVar(line, p)
        if x > 0:
            res.append(Identifier(line[p:p + x]))
            p += x
            continue
        if line[p] not in [';', '+', '-', '*', '/', '(', ')', ' ', '=', '[ ', ']', '{', '}']:
            if not Token.error:
                print(f"\033[91mERROR unexpected char {line[p]}\033[0m")
                Token.error = 1
                return res, 1
    return res, 0

def parse_text(program):
    tokens = []

    for row in program:
        row_tokens, error = parseLine(row)
        if error:
            return tokens, error
        tokens.extend(row_tokens)

    return tokens, 0

    # print_toke_table()
    # if not Token.error:
    #    variables = set()
    #    key_words = set()
    #    operators = set()
    #    constants = set()
    #
    #    table_data = []
    #    for i, token in enumerate(tokens):
    #        table_data.append([i, token.__class__.__name__, token.data])
    #
    #    for i, token in enumerate(tokens):
    #        if isinstance(token, Identifier) and tokens[i - 1].data in ["int", "void", "char"]:
    #            variables.add(token.data + " - type " + tokens[i - 1].data)
    #        elif token.data in ["if", "else", "for", "while", "do", "switch", "case", "final", "println"]:
    #            key_words.add(token.data)
    #        elif token.data in ["+", "-", "=", "==", ">=", "<=", "<", ">"]:
    #            operators.add(token.data)
    #        elif isinstance(token, Const) or isinstance(token, Identifier) and not any(token.data.startswith(var.split()[0]) for var in variables):
    #            if token.data.isdigit():
    #                constants.add(token.data + " - int constant")
    #            if token.data in ["true", "false"]:
    #                constants.add(token.data + " - bool constant")
    #            if token.data[0] == '\'':
    #                constants.add(token.data + " - char constant")
    #            if token.data[0] == '\"':
    #                constants.add(token.data + " - string constant")
    #
    #    headers = ["#", "Token type", "Token data"]
    #    print("\nVariables:")
    #    print(tabulate(enumerate(variables), headers=['#', 'Variable name', '']))
    #    print("\nKey words:")
    #    print(tabulate(enumerate(key_words), headers=['#', 'Key word name']))
    #    print("\nOperators:")
    #    print(tabulate(enumerate(operators), headers=['#', 'Operator name']))
    #    print("\nConstants:")
    #    print(tabulate(enumerate(constants), headers=['#', 'Constant name']))