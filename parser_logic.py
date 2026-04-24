#Kyle Bertrand
#Robert Huntington

# Parser
class Parser:
        def __init__(self, tokens):
            self.tokens = [] #list for <type,val>
            for tok in tokens:
                ttype = tok.split(",")[0].replace("<", "")
                tval = tok.split(",",1)[1][:-1] #remove only last > to handle <op,>>
                self.tokens.append((ttype, tval))
            self.inTokens = ("empty","empty")   # FIXED: was self.inTokens("empty","empty")
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
                lit_type = "float" if "." in self.inTokens[1] else "int"
                self.log("    child node(internal): " + lit_type)
                self.log("    " + lit_type + " has child node(token): " + self.inTokens[1])
                self.accept_tokens()
            else:
                self.log("    error: num expects int or float, got: " + self.inTokens[1])

        # BNF: multi -> num * multi | num
        def multi(self):
            self.log("\n  ---parent node multi, finding children nodes:")
            self.num()
            if self.inTokens[1] == "*":
                self.log("  child node(token): " + self.inTokens[1])
                self.accept_tokens()
                self.log("  child node(internal): multi")
                self.multi()
            else:
                self.log("  multi ends (no * found)")

        # BNF: math -> multi + math | multi
        def math(self):
            self.log("\n  ---parent node math, finding children nodes:")
            self.log("  child node(internal): multi")
            self.multi()
            if self.inTokens[1] == "+":
                self.log("\n  child node(token): " + self.inTokens[1])
                self.accept_tokens()
                self.log("  child node(internal): math")
                self.math()
            else:
                self.log("  math ends (no + found)")

        # BNF: exp -> type id = math
        def exp(self):
            self.log("\n---parent node exp, finding children nodes:")
            if self.inTokens[0] == "key":
                self.log("  ---parent node type, finding children nodes:")  # ← added
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
            if self.inTokens[0] == "id":    # FIXED: was self.inTokens0
                self.log("    child node(internal): id")
                self.log("    identifier has child node(token): " + self.inTokens[1])
                self.accept_tokens()
            self.log("    comparison_exp done")


        #BNF: if_exp -> if(comparison_exp):
        def if_exp(self):
            self.log("\n---parent node if_exp, finding children nodes:")
            self.log("  child node(token): " + self.inTokens[1])
            self.accept_tokens()

            if self.inTokens[1] == "(":
                self.log("  child node(token): " + self.inTokens[1])
                self.accept_tokens()

            self.log("  child node(internal): comparison_exp")
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
                lit_type = "float" if "." in self.inTokens[1] else "int"  # ← added
                self.log("    child node(internal): " + lit_type)  # ← changed
                self.log("    " + lit_type + " has child node(token): " + self.inTokens[1])
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