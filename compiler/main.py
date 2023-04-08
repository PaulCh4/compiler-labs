from lex.lexer import parse_text
from synt.syntax import *
from lex.tokens import *

i = open("input.txt", "r")
program = i.readlines()

tokens, error = parse_text(program)

if not error:
    grammar = loadGrammar()

    tree, error = build_tree(tokens, grammar)
    if not error:
        print('\n\n\n_________ root _________\n')
        for node in tree:
            print(node.__class__.__name__)
        print('\n\n\n_________ tree _________\n')
        print_tree(tree[0])






