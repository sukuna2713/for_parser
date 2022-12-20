from __future__ import annotations
import pyparsing as pp
from nodes.nodes_ast import AstGenerator
from nodes.nodes_nodes import For, ForWhole, NestedState
import re
import json

ast = AstGenerator()

# 予約語の定義
(PRAGMA, FOR) = map(pp.CaselessKeyword, "#pragma, for".replace(",", "").split())

keyword = pp.MatchFirst((PRAGMA, FOR))
# pragmaでもforでも無い文はidentifierということにする
ident = ~keyword + pp.Word(pp.alphas + pp.alphanums +
                           "_;:+-*/\"'<>%|^~!#[],._=")

# 条件式
condition = "(" + (ident)[1, ...] + ")"

condition.add_parse_action(ast.make_condition)


# 文
statement = pp.Forward()

# #pragma による指示文
pragma_statement = PRAGMA + ... + pp.lineEnd()

pragma_statement.add_parse_action(ast.make_pragma)

# for文
for_body = pp.Group(statement)
for_statement = "for" + condition + for_body
for_statement = pp.Located(for_statement)

for_statement.add_parse_action(ast.make_for)

for_whole = pp.ZeroOrMore(pragma_statement) + for_statement

for_whole.add_parse_action(ast.make_for_whole)

# 他の文
other_statement = (ident)[1, ...]

other_statement.add_parse_action(ast.make_others)

one_state = condition | other_statement

# {}によってネストされた文
nested_statement = "{" + (statement)[1, ...] + "}"
nested_statement.add_parse_action(ast.make_nested)

statement <<= (for_whole | nested_statement | one_state)

program = pp.OneOrMore(statement)
program.add_parse_action(ast.make_program)


class ForGetter:
    def __init__(self, source: str) -> None:
        self.source = source

    def get_text(self, start: int, end: int) -> str:
        return self.source[start:end]

    def scan_source(self) -> list[tuple[For, bool]]:
        result = for_whole.scanString(self.source)
        reslist = list(result)
        forlist: list[tuple[For, bool]] = []
        for res, i, j in reslist:
            for item in res.as_list():
                forlist += self.get_for(item)
        return forlist

    def get_for(self, res) -> list[tuple[For, bool]]:
        forlist: list[tuple[For, bool]] = []
        if isinstance(res, For):
            forlist.append((res, False))
            for body in res.body:
                forlist += self.get_for(body)
        elif isinstance(res, ForWhole):
            for_state = res.for_main
            forlist.append((for_state, res.label))
            for body in for_state.body:
                forlist += self.get_for(body)
        elif isinstance(res, NestedState):
            for state in res.statements:
                forlist += self.get_for(state)
        return forlist

    def remove_pragma(self, text: str) -> str:
        return re.sub('.*?#pragma.*?\n', '', text, re.S)

    def to_input_string(self, forlist: list[tuple[For, bool]]) -> str:
        input_string = ''
        for forstate, label in forlist:
            start, end = forstate.location()
            input_string += f"===original=== start:{start}, end:{end}, ispragma: {label}\n"
            gotten = self.get_text(start, end)
            input_string += self.remove_pragma(gotten) + '\n'
        return input_string

    def to_json(self, forstate: tuple[For, bool], index: int) -> str:
        state, target = forstate
        start, end = state.location()
        gotten = self.get_text(start, end)
        func = self.remove_pragma(gotten)
        targetnum = 1 if target else 0
        resdict = {
            "project": "test",
            "commit_id": "kari",
            "target": targetnum,
            "func": func,
            "index": index
        }
        return json.dumps(resdict)


"""
# test
path = "sample1.c"
with open(path, 'r') as f:
    text = f.read()

getter = ForGetter(text)
forlist = getter.scan_source()
print(len(forlist))
# print(getter.to_input_string(forlist))
for ind, fo in enumerate(forlist):
    print(getter.to_json(fo, ind))
"""
