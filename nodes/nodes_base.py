class ASTNode(object):
    _fields: tuple = ()

    def __repr__(self):
        field = ', '.join(["%s=%s" % (field, getattr(self, field))
                          for field in self._fields])
        return f"{self.__class__.__name__}({field})"

    # インデント付きで表示
    def _p(self, v, indent):
        SPACER = " "
        print(f"{SPACER * indent}{v}")

    def indented(self, value, indent=0):
        SPACER = " "
        return f"{SPACER * indent}{value}\n"

    # 文字列化
    def __str__(self) -> str:
        return f"{self.__class__.__name__}: default!"

    def dumps(self, indent=0) -> str:
        dumped = ""
        for field in self._fields:
            value = getattr(self, field)
            if isinstance(value, list):
                for value2 in value:
                    if isinstance(value2, ASTNode):
                        dumped += value2.dumps(indent + 2)
                    else:
                        dumped += ""
                        #dumped += self.indented(value2, indent + 2)
            else:
                if value:
                    if isinstance(value, ASTNode):
                        dumped += value.__str__()
                        dumped += value.dumps(indent + 2)
                    elif isinstance(value[0], ASTNode):
                        dumped += value[0].__str__()
                        dumped += value[0].dumps(indent + 2)
                    else:
                        dumped += ""
                        #dumped += self.indented(value, indent + 2)
        return dumped
