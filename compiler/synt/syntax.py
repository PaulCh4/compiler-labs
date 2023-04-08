from typing import List, Tuple, Dict

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
        parts = row.split()

        args = []
        for part in parts:
            if part not in ["=", "+"]:
                args.append(part)

        grammar.append(Rule(args[0], args[1:]))

    return grammar


def error_grammar_check(tokens, p):
    if len(tokens) >= 2:
        invalid_sequences = [(Type, If), (While, If), (For, If)]

        for seq in invalid_sequences:
            if p+1 < len(tokens) and isinstance(tokens[p], seq[0]) and isinstance(tokens[p+1], seq[1]):
                print(f"\033[91mError: invalid sequence {seq[0].__name__} + {seq[1].__name__}\033[0m")
                return True

        if p+1 < len(tokens) and isinstance(tokens[p], Identifier) and isinstance(tokens[p+1], Identifier):
            print(f"\033[91mError: unexpected token: {tokens[p+1].data}\033[0m")
            return True

        if p+1 < len(tokens) and isinstance(tokens[p], Type) and not isinstance(tokens[p+1], Identifier):
            print(f"\033[91mError: expected Identifier after Type\033[0m")
            return True

        open_parentheses = 0
        for t in tokens:
            if isinstance(t, POpen):
                open_parentheses += 1
            elif isinstance(t, PClose):
                open_parentheses -= 1
        if open_parentheses > 0:
            print("\033[91mError: unclosed curly bracket )\033[0m")
            return True

        open_parentheses = 0
        for t in tokens:
            if isinstance(t, BOpen):
                open_parentheses += 1
            elif isinstance(t, BClose):
                open_parentheses -= 1
        if open_parentheses > 0:
            print("\033[91mError: unclosed curly bracket }\033[0m")
            return True

    return False


def build_tree(tokens: List[Token], grammar: List[Rule]):
    stack = []
    p = 0
    print('\n\n\n_________ tokens _________\n')
    for i in range(len(tokens)):

        print(f"{NONTERMINAL_COLOR}{tokens[i].__class__.__name__}:{RESET_COLOR}")

        if error_grammar_check(tokens, p):
            return stack, 1
        stack.append(tokens[i])
        p += 1


        for rule in grammar:
            if len(stack) >= len(rule.parts) and all(stack[-len(rule.parts) + i].__class__.__name__ == word for i, word in enumerate(rule.parts)):

                class_name = rule.result
                if class_name in globals() and issubclass(globals()[class_name], NonTerminal):
                    nonterminal = globals()[class_name](rule.parts)
                else:
                    nonterminal = NonTerminal(rule.result, rule.parts)

                for _ in rule.parts:
                    nonterminal.parts.append(stack.pop())

                stack.append(nonterminal)

    return stack, 0


def print_tree(node: Tag, indent: str = ""):
    class_name = node.__class__.__name__
    if isinstance(node, Token):
        print(f"{indent}{TERMINAL_COLOR}|{class_name}: {node.data}{RESET_COLOR}")
        #print(f"{indent}{TERMINAL_COLOR}Terminal_{class_name}: {node.data}{RESET_COLOR}")
    elif isinstance(node, NonTerminal):
        if node.parts:
            print(f"{indent}|{NONTERMINAL_COLOR}{class_name}:{RESET_COLOR}")
            for child in reversed(node.parts):
                print_tree(child, indent + "  ")
        else:
            print(f"{indent}|{NONTERMINAL_COLOR}{class_name}{RESET_COLOR}")
            pass
