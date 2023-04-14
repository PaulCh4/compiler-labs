class Tag:
    pass


class Terminal(Tag):
    def __init__(self, token):
        self.token = token


class NonTerminal:
    def __init__(self, result, parts=None):
        #self.result = result
        self.parts = parts if parts is not None else []
        #self.token = None


class Expression(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class Declaration(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class Instruction(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class PreCall(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class InstructionSet(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class CompExpression(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class CaseLine(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class Cases(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


# TODO----------------------
class Method(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class Function(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class Assignment(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)