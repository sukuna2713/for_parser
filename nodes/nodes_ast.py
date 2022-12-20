from .nodes_nodes import PragmaState, Condition, For, ForWhole, NestedState, Program, Others


class AstGenerator(object):
    def __init__(self):
        self.symbol_table = {}

    def make_pragma(self, tokens):
        state = tokens.asList()
        return PragmaState(state[1:])

    def make_condition(self, tokens):
        state = tokens.asList()
        return Condition(state[1:-1])

    def make_for(self, tokens):
        tokens = tokens.asList()
        start = tokens[0]
        end = tokens[2]
        condition = tokens[1][1]
        body = tokens[1][2]
        return For(condition, body, start, end)

    def make_for_whole(self, tokens):
        tokens = tokens.asList()
        pragma = [token for token in tokens if isinstance(token, PragmaState)]
        for_state = [token for token in tokens if isinstance(token, For)]
        if len(pragma) > 0:
            #print("for with pragma")
            return ForWhole(pragma[0], for_state[0], True)
        else:
            #print("for without pragma")
            return ForWhole(None, for_state[0], False)

    def make_nested(self, tokens):
        tokens = tokens.asList()
        return NestedState(tokens)

    def make_others(self, tokens):
        tokens = tokens.asList()
        return Others(tokens)

    def make_program(self, tokens):
        tokens = tokens.asList()
        return Program(tokens)
