from lex.tokens import *

variables = {}  # [type, value]


class Tag:
    pass


class Terminal(Tag):
    def __init__(self, token):
        self.token = token


class NonTerminal:
    def __init__(self, parts=None):
        self.parts = parts if parts is not None else []

    def __str__(self):
        return f"{self.__class__.__name__}"


class Expression(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self) -> any:
        if isinstance(self.parts[0], Const):
            return self.parts[0].data
        if len(self.parts) == 3:
            #try:
                if isinstance(self.parts[1], Arifm):
                    if self.parts[1].data == "+":
                        return self.parts[0].run() + self.parts[2].run()
                    if self.parts[1].data == "-":
                        return self.parts[0].run() - self.parts[2].run()
                    if self.parts[1].data == "*":
                        return self.parts[0].run() * self.parts[2].run()
                    if self.parts[1].data == "/":
                        return self.parts[0].run() / self.parts[2].run()
                    if self.parts[1].data == "%":
                        return self.parts[0].run() % self.parts[2].run()
                if isinstance(self.parts[1], Comp):
                    if self.parts[1].data == "==":
                        return self.parts[0].run() == self.parts[2].run()
                    if self.parts[1].data == "<=":
                        return self.parts[0].run() <= self.parts[2].run()
                    if self.parts[1].data == ">=":
                        return self.parts[0].run() >= self.parts[2].run()
                    if self.parts[1].data == ">":
                        return self.parts[0].run() > self.parts[2].run()
                    if self.parts[1].data == "<":
                        return self.parts[0].run() < self.parts[2].run()
            #except :
            #    print(f"\033[91mERROR Expressions types doesn't match\033[0m")
            #    return -1
        if isinstance(self.parts[0], Identifier):
            if variables[self.parts[0].data] is None:
                print(f"\033[91mERROR Variable wasn't defined\033[0m")
                return -1
            else:
                return variables[self.parts[0].data][1]
        if isinstance(self.parts[0], POpen):
            return self.parts[1].run()


class Declaration(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self) -> str:
        if len(self.parts) == 2:
            variables[self.parts[1].data] = [self.parts[0].data, None]
            return self.parts[1].data
        else:
            variables[self.parts[3].data] = [self.parts[0].data + "[]", None]
            return self.parts[3].data


class Instruction(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self):
        if isinstance(self.parts[0], Declaration) and isinstance(self.parts[1], Semicolon):
            self.parts[0].run()
            return
        if isinstance(self.parts[0], Declaration) and isinstance(self.parts[1], SetOp) and isinstance(self.parts[2], Expression):
            ind = self.parts[0].run()
            variables[ind][1] = self.parts[2].run()
            return
        if len(self.parts) == 8 and isinstance(self.parts[2], New):
            ind = self.parts[0].run()
            variables[ind][1] = []
            return
        if isinstance(self.parts[0], Do):
            self.parts[2].run()
            while self.parts[5].run():
                self.parts[2].run()
            return
        if isinstance(self.parts[0], Expression):
            if self.parts[1].data == "+":
                variables[self.parts[0].parts[0].data][1] = variables[self.parts[0].parts[0].data][1] + 1
                return
            if self.parts[1].data == "-":
                variables[self.parts[0].parts[0].data][1] = variables[self.parts[0].parts[0].data][1] - 1
                return
            print(f"\033[91mERROR Wrong attempt to inc or dec\033[0m")
            return
        if isinstance(self.parts[0], For):
            self.parts[2].run()
            while self.parts[3].run():
                self.parts[8].run()
                self.parts[4].run()
            return
        if isinstance(self.parts[0], FunctionCall):
            self.parts[0].run()
            return
        if len(self.parts) == 4 and isinstance(self.parts[1], SetOp):
            variables[self.parts[0].data][1] = self.parts[2].run()
            return
        if isinstance(self.parts[0], If):
            if self.parts[1].run():
                self.parts[3].run()
            else:
                if len(self.parts) > 5:
                    self.parts[7].run()
            return
        if isinstance(self.parts[0], Switch):
            self.parts[3].run(self.parts[1].run())
            return
        if isinstance(self.parts[0], While):
            while self.parts[1].run():
                self.parts[3].run()


class PreCall(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)


class InstructionSet(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self):
        for part in self.parts:
            part.run()


class CaseLine(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self, value):
        if value == self.parts[1].run():
            self.parts[3].run()


class Cases(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self, value):
        for part in self.parts:
            part.run(value)


#    .    .    .    .    .    .    .    .    .    .    .    .
class Method(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self):
        self.parts[4].run()


class FunctionCall(NonTerminal):
    def __init__(self, parts):
        super().__init__(parts)

    def run(self) -> any:
        if self.parts[0].data == "println" and isinstance(self.parts[1], Expression):
            print(self.parts[1].run())
        pass  # todo
