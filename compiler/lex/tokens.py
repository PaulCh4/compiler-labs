class Token:
    data = ""
    error = 0

    def __str__(self):
        return f"{self.data}"

class Identifier(Token):
    def __init__(self, op):
        self.data = op


class Type(Token):
    def __init__(self, op):
        self.data = op


class Const(Token):
    def __init__(self, op):
        self.data = op
        #self.type = type


class If(Token):
    def __init__(self):
        self.data = "if"

class Else(Token):
    def __init__(self):
        self.data = "else"


class Switch(Token):
    def __init__(self):
        self.data = "switch"


class Case(Token):
    def __init__(self):
        self.data = "case"


class While(Token):
    def __init__(self):
        self.data = "while"


class For(Token):
    def __init__(self):
        self.data = "for"


class Do(Token):
    def __init__(self):
        self.data = "do"


class Arifm(Token):
    def __init__(self, op):
        self.data = op


class SetOp(Token):
    def __init__(self):
        self.data = "="


class Comp(Token):
    def __init__(self, op):
        self.data = op


#{
class BOpen(Token):
    def __init__(self):
        self.data = "{"

#}
class BClose(Token):
    def __init__(self):
        self.data = "}"


#(
class POpen(Token):
    def __init__(self):
        self.data = "("

#)
class PClose(Token):
    def __init__(self):
        self.data = ")"


#[
class SBOpen(Token):
    def __init__(self):
        self.data = "["

#]
class SBClose(Token):
    def __init__(self):
        self.data = "]"


class Semicolon(Token):
    def __init__(self):
        self.data = ";"

class Dot(Token):
    def __init__(self):
        self.data = "."

class New(Token):
    def __init__(self):
        self.data = "new"
