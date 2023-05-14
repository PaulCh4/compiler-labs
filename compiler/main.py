from lex.lexer import parse_text
from synt.syntax import *

i = open("inputs/input0.txt", "r")
program = i.readlines()

tokens, error = parse_text(program)


def print_tree(node: Tag, indent: str = ""):
    class_name = node.__class__.__name__
    if isinstance(node, Token):
        print(f"{indent}|{TERMINAL_COLOR}{class_name}: {node.data}{RESET_COLOR}")
    elif isinstance(node, NonTerminal):
        if node.parts:
            print(f"{indent}|{NONTERMINAL_COLOR}{class_name}:{RESET_COLOR}")
            for child in node.parts:
                print_tree(child, indent + "  ")
        else:
            print(f"{indent}|{NONTERMINAL_COLOR}{class_name}{RESET_COLOR}")
            pass


if not error:
    grammar = loadGrammar()

    tree, error = build_tree(tokens, grammar)
    if not error:
        print('\n\n\n_________ root _________\n')
        for node in tree:
            print(node.__class__.__name__)
        print('\n\n\n_________ tree _________\n')
        print_tree(tree[0])

        tree[0].run()

        #2 списка отрицательных и положительных значений, соединить\\ отсортировать найти дубликаты


