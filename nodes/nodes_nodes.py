from typing import cast
from .nodes_base import ASTNode
import re

space = " "


class Statement(ASTNode):
    pass


class PragmaState(Statement):
    _fields = ('state',)

    def __init__(self, statement: list) -> None:
        self.state = statement

    def __str__(self) -> str:
        return "#pragma " + " ".join(map(str, self.state))

    def dumps(self, indent=0) -> str:
        return f"{space * indent}" + self.__str__()


class Condition(Statement):
    _fields = ('state',)

    def __init__(self, statement: list) -> None:
        self.state = statement

    def __str__(self) -> str:
        statestr = " ".join([state.__str__() for state in self.state])
        return f"({statestr})"

    def dumps(self, indent=0) -> str:
        return f"{space * indent}" + self.__str__()


class For(Statement):
    _fields = ('condition', 'body', 'start', 'end')

    def __init__(self, condition, body, start, end) -> None:
        self.condition = condition
        self.body = body
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return "is For"

    def location(self) -> tuple[int, int]:
        return (self.start, self.end)

    def dumps(self, indent=0) -> str:
        indentstr = f"{space * indent}"
        if isinstance(self.body, NestedState):
            return f"{indentstr}for {self.condition.dumps()}\n{(indent - 2) * space + self.body.dumps(indent)}"
        else:
            return f"{indentstr}for {self.condition.dumps()} {self.body.dumps()}"


class ForWhole(Statement):
    _fields = ('pragma', 'for_main', 'label')
    # 指示文ありのときlabel=True,なしのときfalse

    def __init__(self, pragma, for_main, label=False) -> None:
        self.pragma = pragma
        self.for_main = for_main
        self.label = label


class NestedState(ASTNode):
    _fields = ('statements',)

    def __init__(self, statements) -> None:
        self.statements = statements

    def __str__(self) -> str:
        return "{\n" + "\n".join([state.__str__() for state in self.statements]) + "\n}"

    def dumps(self, indent=0) -> str:
        indentstr = f"{space * indent}"
        states = "\n".join([state.dumps(indent + 2)
                           for state in self.statements])
        return indentstr + "{\n" + states + "\n" + indentstr + "}"


class Others(ASTNode):
    _fields = ('ids',)

    def __init__(self, ids) -> None:
        self.ids = ids

    def __str__(self) -> str:
        return " ".join([id.__str__() for id in self.ids])

    def dumps(self, indent=0) -> str:
        p = re.compile('(;)')
        # compiled
        stred = f"{space * indent}" + self.__str__()
        compiled = p.sub('\\1\n', stred)
        p = re.compile('(\n)')
        compiled = p.sub(f'\\1{space*(indent - 1)}', compiled)
        return compiled


class Program(ASTNode):
    _fields = ('statements',)

    def __init__(self, statements) -> None:
        self.statements = statements

    def __str__(self) -> str:
        return "\n".join([state.__str__() for state in self.statements])

    def dumps(self, indent=0) -> str:
        return "\n".join([state.dumps(indent + 2)
                          for state in self.statements])
