class Tag:
    pass


class Terminal(Tag):
    def __init__(self, token):
        self.token = token


class NonTerminal:
    def __init__(self, result, parts=None):
        # self.result = result
        self.parts = parts if parts is not None else []
        # self.token = None


class Expression(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self) -> any:
        pass  # todo метод возвращает результат выражения - константу


class Declaration(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self):
        pass  # todo метод объявляет переменную


class Instruction(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self):
        pass  # todo смотрит свои части и вызывает их методы run()


class PreCall(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class InstructionSet(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self):
        for part in self.parts:
            part.run()


class CompExpression(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self) -> bool:
        pass  # todo посчитать значение


class CaseLine(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self, value):
        pass  # todo сравнить значение и если совпадает, то выполнить


class Cases(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self, value):
        for part in self.parts:
            part.run()

#    .    .    .    .    .    .    .    .    .    .    .    .
class Method(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class Function(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class Assignment(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)