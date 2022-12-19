import pyparsing as pp

pp.ParserElement.set_default_whitespace_chars(" \t")

# 予約語の定義
(PRAGMA, FOR) = map(pp.CaselessKeyword, "#pragma, for".replace(",", "").split())
keyword = pp.MatchFirst((PRAGMA, FOR))

# あったりなかったりする空白
whiteOrNothing = pp.ZeroOrMore(pp.Literal(" "))

# あったりなかったりする改行
clOrNothing = pp.ZeroOrMore(pp.Literal("\n"))

# 文の定義
expression = pp.Forward()

# OpenMP指示文の定義
openmp = PRAGMA + ... + pp.lineEnd()

# 条件式部分の定義
condition = pp.nestedExpr("(", ")")

# 鉤括弧部分の定義
nested_expr = pp.originalTextFor(pp.nestedExpr("{", "}", expression))

forone = FOR + whiteOrNothing + condition + whiteOrNothing + nested_expr

# 追加アクションとしてクラス変換を登録する


class PragmaState(object):
    def __init__(self, tokens) -> None:
        tokens = tokens.asList()
        self.statement = tokens[1:]

    def __str__(self) -> str:
        stred = "#pragma " + "".join(map(str, self.statement))
        return stred


class ConditionState(object):
    def __init__(self, tokens) -> None:
        self.statement = tokens[0]

    def __str__(self) -> str:
        stred = "(" + " ".join(map(str, self.statement)) + ")"
        return stred


class NestedExprState(object):
    def __init__(self, tokens) -> None:
        self.statement = tokens[1]
        print(self.__str__())

    def __str__(self) -> str:
        stred = "{\n" + "\n".join(map(str, self.statement)) + "\n}"
        return stred


class ForState(object):
    def __init__(self, tokens) -> None:
        tokens = tokens.asList()
        self.statement = tokens[1:]

    def __str__(self) -> str:
        stred = "for" + " ".join([i.__str__() for i in self.statement])
        return stred


class ForallState(object):
    def __init__(self, tokens) -> None:
        self.statement = tokens.asList()

    def __str__(self) -> str:
        stred = "".join([i.__str__() for i in self.statement])
        return stred


openmp.setParseAction(PragmaState)
condition.setParseAction(ConditionState)
nested_expr.setParseAction(NestedExprState)
forone.setParseAction(ForState)

token = ~keyword + ... + pp.LineEnd()

forall = (pp.ZeroOrMore(openmp) + forone)
forall.setParseAction(ForallState)

expression <<= forall | nested_expr | token

program = pp.ZeroOrMore(forall | expression)("program")

text = """{gewi}"""
result = program.parseString(text).dump()
print(result)
