import pyparsing as pp

pragma = "#pragma" + pp.Word(pp.alphanums + "(" + ")" + " ")
forstart = "for (" + pp.Word(pp.alphanums + "=-+*/; ") + ")"
forinput = "{" + pp.Word(pp.alphanums + "\n" + " ") + "}"

forall = pp.Combine(pragma + pp.Word("\n" + "\t" + " ") + forstart + forinput)

text = """#pragma unk tnk (f i 3)
    for (i = 3; i++ ){
        a3
        b3
    }
"""
print(forall.parse_string(text))
