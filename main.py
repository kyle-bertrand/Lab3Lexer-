
from tkinter import *
from tkinter import messagebox
import re

#Kyle Bertrand
#Robert Huntington

#lexer engine
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

                # rename patterns for output
                type_map = {
                    "String_literal": "lit",
                    "Float_literal": "lit",
                    "Int_literal": "lit",
                    "Operator": "op",
                    "Seperator": "sep",
                    "Keyword": "key",
                    "Identifier": "id",
                }

                out_list.append(f"<{type_map.get(ttype,ttype)},{tok}>")

            s = s[moutput.end():] #s assigns to right after match for next
            matched = True
            break #stop checking patterns b/c found next token

        # keeps loop from getting stuck on unknown characters
        if not matched:
            out_list.append(f"<unknown,{s[0]}>")
            s = s[1:]
    return out_list

#Parser
class Parser:
        def __init__(self, tokens):
            self.tokens = [] #list for <type,val>
            for tok in tokens:
                ttype = tok.split(",")[0].replace("<", "")
                tval = tok.split(",",1)[1][:-1] #remove only last > to handle <op,>>
                self.tokens.append((ttype, tval))
            self.inTokens("empty","empty")
            self.output = [] #lines for parse tree

        def accept_tokens(self):
            self.output.append("  accepting token from list: " + self.inTokens[1])
            if self.tokens:
                self.inTokens = self.tokens.pop(0)
            else:
                self.inTokens = ("empty","empty")

        def log(self,msg):
            self.output.append(msg)

        # BNF: num -> int | float
        def num(self):
            self.log("\n  ---parent node num, finding children nodes:")
            if self.inTokens[0] == "lit":
                self.log("    child node(internal): lit")
                self.log("    lit has child node(token): " + self.inTokens[1])
                self.accept_tokens()
            else:
                self.log("    error: num expects int or float, got: " + self.inTokens[1])

        # BNF: multi -> num * multi | num
        def multi(self):
            self.log("\n  ---parent node multi, finding children nodes:")
            self.num()
            if self.inTokens[1] == "*":
                self.log("    child node(token): " + self.inTokens[1])
                self.accept_tokens()
                self.log("    child node(internal): multi")
                self.multi()
            else:
                self.log("    multi ends (no * found)")

        # BNF: math -> multi + math | multi
        def math(self):
            self.log("\n  ---parent node math, finding children nodes:")
            self.log("  child node(internal): multi")
            self.multi()
            if self.inTokens[1] == "+":
                self.log("\n  child node(token): " + self.inTokens[1])
                self.accept_tokens()
                self.log("    child node(internal): math")
                self.math()
            else:
                self.log("    math ends (no + found)")

        # BNF: exp -> type id = math
        def exp(self):
            self.log("\n---parent node exp, finding children nodes:")
            if self.inTokens[0] == "key":
                self.log("  child node(internal): type")
                self.log("    type has child node(token): " + self.inTokens[1])
                self.accept_tokens()
            else:
                self.log("  error: expected type keyword, got: " + self.inTokens[1])
                return

            if self.inTokens[0] == "id":
                self.log("  child node(internal): id")
                self.log("    identifier has child node(token): " + self.inTokens[1])
                self.accept_tokens()
            else:
                self.log("  error: expected identifier, got: " + self.inTokens[1])
                return

            if self.inTokens[1] == "=":
                self.log("  child node(token): " + self.inTokens[1])
                self.accept_tokens()
            else:
                self.log("  error: expected =, got: " + self.inTokens[1])
                return

            self.log("  child node(internal): math")
            self.math()

        #BNF: comparison_exp -> identifier > identifier
        def comparison_exp(self):
            self.log("\n  ---parent node comparison_exp, finding children nodes:")
            if self.inTokens[0] == "id":
                self.log("    child node(internal): id")
                self.log("    identifier has child node(token): " + self.inTokens[1])
                self.accept_tokens()
            if self.inTokens[1] == ">":
                self.log("    child node(token): " + self.inTokens[1])
                self.accept_tokens()
            if self.inTokens0 == "id":
                self.log("    child node(internal): id")
                self.log("    identifier has child node(token): " + self.inTokens[1])
                self.accept_tokens()
            self.log("    comparison_exp done")


        #BNF: if_exp -> if(comparison_exp):
        def if_exp(self):
            self.log("\n  ---parent node if_exp, finding children nodes:")
            self.log("    child node(token): " + self.inTokens[1])
            self.accept_tokens()

            if self.inTokens[1] == "(":
                self.log("    child node(token): " + self.inTokens[1])
                self.accept_tokens()

            self.log("    child node(internal): comparison_exp")
            self.comparison_exp()

            if self.inTokens[1] == ")":
                self.log("  child node(token): " + self.inTokens[1])
                self.accept_tokens()

            if self.inTokens[1] == ":":
                self.log("  child node(token): " + self.inTokens[1])
                self.accept_tokens()

            self.log("  if_exp done")

        # BNF: print_exp -> print ( lit ) ;
        def print_exp(self):
            self.log("\n---parent node print_exp, finding children nodes:")
            self.log("  child node(token): " + self.inTokens[1])
            self.accept_tokens()  # consume print

            if self.inTokens[1] == "(":
                self.log("  child node(token): " + self.inTokens[1])
                self.accept_tokens()

            if self.inTokens[0] == "lit":
                self.log("  child node(internal): lit")
                self.log("    lit has child node(token): " + self.inTokens[1])
                self.accept_tokens()

            if self.inTokens[1] == ")":
                self.log("  child node(token): " + self.inTokens[1])
                self.accept_tokens()

            if self.inTokens[1] == ";":
                self.log("  child node(token): " + self.inTokens[1])
                self.accept_tokens()

            self.log("  print_exp done")


def parser(tokens, line_number):
    p = Parser(tokens)

    # pop first token to start, just like main() in PyLab parser
    if len(p.tokens) > 0:
        p.inTokens = p.tokens.pop(0)
    else:
        p.inTokens = ("empty", "empty")

    # call the right parse function based on line number
    if line_number == 1 or line_number == 2:
        p.exp()
    elif line_number == 3:
        p.if_exp()
    elif line_number == 4:
        p.print_exp()

    return p.output


# GUI
class LexerGUI:
        def __init__(self, root):
                self.master = root
                self.master.title("Lexer GUI")
                self.master.geometry("900x600")

                #variables
                self.lines = []
                self.current_line = 0

                #title
                self.title_label = Label(self.master)
                self.title_label.grid(row = 0, column = 0, columnspan = 2, pady=10)

                #source code label
                self.src_label = Label(self.master, text="Source Code Input:", font=("Arial", 12, "bold"))
                self.src_label.grid(row = 1, column = 0, padx=10, sticky = W)

                #output label
                self.output_label = Label(self.master, text="Lexical Analyzed Output:", font=("Arial", 12, "bold"))
                self.output_label.grid(row=1, column=1, padx=10, sticky=W)

                #input text
                self.src_text = Text(self.master, width=60, height=20)
                self.src_text.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

                #output text
                self.output_text = Text(self.master, width=60, height=20, state=DISABLED)
                self.output_text.grid(row=2, column=1, padx=10)

                #current line label
                Label(self.master, text="Current Line:").grid(row=3, column=0, padx=10, sticky=E)
                self.line_entry = Entry(self.master, width=5, justify="center")
                self.line_entry.insert(0, "0")
                self.line_entry.config(state="readonly")
                self.line_entry.grid(row=3, column=1, sticky=W)

                #handle buttons
                Button(self.master, text="Next Line", command=self.next_line).grid(row=4, column=0, padx=10)
                Button(self.master, text="Quit", command=self.master.quit).grid(row=4, column=1, padx=10)

        def next_line(self):
                if self.current_line == 0:
                        text = self.src_text.get("1.0", "end-1c")
                        if not text.strip():
                                messagebox.showerror("Error", "Please enter code.")
                                return
                        self.lines = text.splitlines()

                if self.current_line >= len(self.lines):
                        messagebox.showinfo("Done", "All lines processed.")
                        return

                line = self.lines[self.current_line]

                tokens = CutOneLineTokens(line)

                self.output_text.config(state=NORMAL)
                self.output_text.insert(END, f"Line {self.current_line+1}: {line}\n ")
                # EDITED: format tokens without quotes around each token
                self.output_text.insert(END, f"[{', '.join(tokens)}]\n\n")
                self.output_text.config(state=DISABLED)

                self.current_line += 1
                self.line_entry.config(state='normal')
                self.line_entry.delete(0, END)
                self.line_entry.insert(0, str(self.current_line))
                self.line_entry.config(state='readonly')


if __name__ == "__main__":
        root = Tk()
        app = LexerGUI(root)
        root.mainloop()