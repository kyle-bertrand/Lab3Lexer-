import re

#Kyle Bertrand
#Robert Huntington

patterns = [
    ("whitespace", re.compile(r"")),
    ("String_literal", re.compile(r"")),
    ("Float_literal", re.compile(r"")),
    ("Int_literal", re.compile(r"")),
    ("Operator", re.compile(r"")),
    ("Seperator", re.compile(r"")),
    ("Keyword", re.compile(r"")),
    ("Identifier", re.compile(r""))
]

def CutOneLineTokens(line : str) -> list[str]:
    out = []
    s = line

    while s:
        matched = False

        for ttype, pat in patterns:
            m = pat.match(s)
            if not m:
                continue

            tok = m.group(0)

            if ttype != "whitespace": #ignore leading whitespace
                #rename for output
                type_map ={
                    "String_literal" : "lit",
                    "Float_literal": "lit",
                    "Int_literal": "lit",
                    "Operator": "op",
                    "Seperator": "sep",
                    "Keyword": "key",
                    "Identifier": "id",
                }
                out.append(f"<{type_map.get(ttype,ttype)},{tok}>")

            s =s[m.end():] #cut token off
            matched = True
            break

        if not matched:
            out.append(f"<unknown,{s[0]}>")
            s =s[1:]
    return out


#test lines
tests = [
        "int A1=5",
        "float BBB2 =1034.2",
        "float cresult = A1 +BBB2 * BBB2",
        "if (cresult >10):",
        'print("TinyPie ")',
]

for line in tests:
    out = CutOneLineTokens(line)
    print(f"Test input string: {line}")
    print(f"Output <type,token> list: {out}")
    print()