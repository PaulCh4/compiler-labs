from typing import List

from synt.terminals import *
from lex.tokens import *

TERMINAL_COLOR = "\033[36m"
NONTERMINAL_COLOR = "\033[37m"
RESET_COLOR = "\033[0m"


class Rule:
    def __init__(self, result, parts):
        self.result = result
        self.parts = parts


def loadGrammar() -> list:
    file = open("synt/grammar.txt", "r")
    raw = file.readlines()

    grammar = []
    for row in raw:
        row = row.strip()
        row = row.split('//')[0]
        if row == "":
            continue
        parts = row.split()

        args = []
        for part in parts:
            if part not in ["=", "+", "-x-", "-?-", "---", "-!-"]:
                args.append(part)

        grammar.append(Rule(args[0], args[1:]))

    return grammar


def build_tree(tokens: List[Token], grammar: List[Rule]):
    stack = []
    print('\n\n\n_________ tokens _________\n')
    for i in range(len(tokens)):
        nextToken = tokens[-i-1]
        print(f"{NONTERMINAL_COLOR}{nextToken.__class__.__name__}:{RESET_COLOR}")
        stack.append(nextToken)

        flag = True
        while flag:
            flag = False
            for rule in grammar:
                if len(stack) >= len(rule.parts) and all(
                        stack[-j-1].__class__.__name__
                        ==
                        word for j, word in enumerate(rule.parts)
                ):
                    if rule == grammar[15]:
                        if (i < len(tokens)-1) and (isinstance(tokens[-i-2], Type)):
                            break
                    if rule.result == "FunctionCall":
                        if (i < len(tokens)-1) and (isinstance(tokens[-i-2], Type)):
                            break
                    if (i < len(tokens)-1) and \
                            (isinstance(nextToken, Identifier)) and \
                            (isinstance(tokens[-i-2], SBClose)):
                        break

                    class_name = rule.result
                    parts = []
                    for j in range(len(rule.parts)):
                        parts.append(stack.pop())
                    nonterminal = globals()[class_name](parts)

                    stack.append(nonterminal)
                    flag = True
                    break

        print(*stack)

    return stack, 0

