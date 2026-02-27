import re

#Kyle Bertrand
#Robert Huntington

patterns = [
    ("whitespace", re.compile(r"^\s+")),
    ("String_literal", re.compile(r'^"[^"\n]*"')),
    ("Float_literal", re.compile(r"^\d+\.\d+")),
    ("Int_literal", re.compile(r"^\d+")),
    ("Operator", re.compile(r"^[+=>*]")),
    ("Seperator", re.compile(r"^[():;]")),
    ("Keyword", re.compile(r"^(if|else|int|float)\b")),
    ("Identifier", re.compile(r"^[A-Za-z_][A-Za-z0-9_]*"))
]

def CutOneLineTokens(line : str) -> list[str]:
    out_list = [] #list that will hold output
    s = line #remaining text

    while s: #loop until string s is empty
        matched = False

        for ttype, pat in patterns:
            moutput = pat.match(s)
            if not moutput:
                continue #run through all pattern options, make sure the patterns all start with ^

            tok = moutput.group(0) #extract token if match found

            if ttype != "whitespace": #ignore whitespaces so the output doesn't add them

                #rename patterns for output
                type_map ={
                    "String_literal" : "lit",
                    "Float_literal": "lit",
                    "Int_literal": "lit",
                    "Operator": "op",
                    "Seperator": "sep",
                    "Keyword": "key",
                    "Identifier": "id",
                }
                out_list.append(f"<{type_map.get(ttype,ttype)},{tok}>")

            s =s[moutput.end():] #s assigns to right after match for next
            matched = True
            break #stop checking patterns b/c found next token

        # keeps loop from getting stuck on unknown characters
        if not matched:
            out_list.append(f"<unknown,{s[0]}>")
            s =s[1:]
    return out_list



#test lines
tests = [
        "int A1=5",
        "float BBB2 =1034.2",
        "float cresult = A1 +BBB2 * BBB2",
        "if (cresult >10):",
        'print("TinyPie ")',
]

for line in tests:
    out_list = CutOneLineTokens(line)
    print(f"Test input string: {line}")
    print(f"Output <type,token> list: {out_list}")
    print()


# thing from GUIexample
if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()