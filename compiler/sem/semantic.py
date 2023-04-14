from synt.terminals import *
from lex.tokens import *


TERMINAL_COLOR = "\033[31m"
NONTERMINAL_COLOR = "\033[37m"
RESET_COLOR = "\033[0m"


def analyze_tree(node: Tag, var_dict: dict = {}, in_function: bool = False):
    class_name = node.__class__.__name__
    error = 0;

    if isinstance(node, Token):
        pass
    elif isinstance(node, NonTerminal):
        if node.parts:
            # D
            if class_name == "Declaration":
                type_node = node.parts[1]
                identifier_node = node.parts[0]
                var_name = identifier_node.data

                if var_name in var_dict:
                    if not error:
                        print(f"\033[91mError: ({type_node.data} {identifier_node.data}) has already been declared \033[0m")
                    return False
                else:
                    var_dict[var_name] = type_node.data

            #I->D=E;
            elif class_name == "Instruction":
                if len(node.parts) == 4 and isinstance(node.parts[3], Declaration) and isinstance(
                        node.parts[1], Expression) and node.parts[3].parts[1].data != "main":
                    decl_type = node.parts[3].parts[1].data
                    expr_type, error = get_expression_type(node.parts[1].parts[0], var_dict)

                    if decl_type != expr_type:
                        if not error:
                            print(
                                 f"\033[91mError: Type mismatch between declared type ({decl_type} {node.parts[3].parts[0].data}) and expression type")
                        return False

            # E->PreCall -> Identifier
            elif class_name == "Expression":
                if not in_function and isinstance(node.parts[0], PreCall):
                    identifier_node = node.parts[0].parts[0]
                    var_name = identifier_node.data

                    if var_name not in var_dict:
                        if not error:
                            print(f"\033[91mError: undeclared identifier ({var_name}) used in expression\033[0m")
                        return False

            elif class_name == "Function":
                in_function = True

            for child in reversed(node.parts):
                if not analyze_tree(child, var_dict, in_function):
                    return False

            if class_name == "Function":
                in_function = False

            #CoE->E==E
            if class_name == "CompExpression" and len(node.parts) == 3:
                left_exp = node.parts[0].parts[0]
                right_exp = node.parts[2].parts[0]
                operator = node.parts[1].data

                left_type, error = get_expression_type(left_exp, var_dict)
                right_type, error = get_expression_type(right_exp, var_dict)

                if left_type is None or right_type is None:
                    return False

                if operator in ["==", "!=", "<", "<=", ">", ">="]:
                    if left_type != right_type:
                        if not error:
                            print(f"\033[91mError: Type mismatch in comparison operator ({right_type} {operator} {left_type}) \033[0m")
                        return False
            #E->E+E
            if class_name == "Expression" and len(node.parts) == 3 and isinstance(node.parts[1], Arifm) and not isinstance(node.parts[0], Arifm):
                left_exp = node.parts[0].parts[0]
                right_exp = node.parts[2].parts[0]
                operator = node.parts[1].data

                left_type, error = get_expression_type(left_exp, var_dict)
                right_type, error = get_expression_type(right_exp, var_dict)

                if left_type is None or right_type is None:
                    return False

                if operator in ["+", "-", '*', "/"]:
                    if left_type != right_type:
                        if not error:
                            print(
                                f"\033[91mError: Type mismatch in arithmetic operator {operator} - {left_type} and {right_type}\033[0m")
                        return False

    return True


def get_expression_type(expression, var_dict):
    class_name = expression.__class__.__name__

    if class_name == "Const":
        const_type = expression.data

        if const_type.isnumeric():
            return "int", False
        elif const_type[0] in "\'":
             return "char", False

    elif class_name == "PreCall":
        identifier_node = expression.parts[0]
        var_name = identifier_node.data

        if var_name not in var_dict:
            print(f"\033[91mError Expresion: undeclared identifier ({var_name})\033[0m")
            return None, True

        return var_dict[var_name], False

    elif class_name == "Expression":
        types = [get_expression_type(child_expr, var_dict)[0] for child_expr in expression.parts]

        if None in types:
            return None, True

        if all(t == types[0] for t in types):
            return types[0], False
        else:
            print("\033[91mError Expresion: Type mismatch in nested expressions\033[0m")
            return None, True

    else:
        print(f"\033[91mError Expresion: Invalid node type {class_name}\033[0m")
        return None, True


