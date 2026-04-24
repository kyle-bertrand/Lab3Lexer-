from tkinter import *
from tkinter import messagebox
import re
import parser_logic

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

                #rename patterns for output
                type_map = {
                    "String_literal" : "lit",
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

# GUI
class LexerGUI:
        def __init__(self, root):
                self.master = root
                self.master.title("Lexer GUI")
                self.master.geometry("1600x900")

                #variables
                self.lines = []
                self.current_line = 0

                #title
                self.title_label = Label(self.master, text="Lexer and Parser for TinyPie", font=("Arial", 16, "bold"))
                self.title_label.grid(row = 0, column = 0, columnspan = 2, pady=10)

                #source code label
                self.src_label = Label(self.master, text="Source Code Input:", font=("Arial", 12, "bold"))
                self.src_label.grid(row = 1, column = 0, padx=10, sticky = W)

                #output label
                self.output_label = Label(self.master, text="Lexical Analyzed Output:", font=("Arial", 12, "bold"))
                self.output_label.grid(row=1, column=1, padx=10, sticky=W)

                #parser output label
                self.parser_label = Label(self.master, text="Parser Output:", font=("Arial", 12, "bold"))
                self.parser_label.grid(row=1, column=2, padx=10, sticky=W)

                # input text — no scrollbar, fixed smaller size
                self.src_text = Text(self.master, width=55, height=20)
                self.src_text.grid(row=2, column=0, padx=10, pady=5, sticky=N)

                # output text — no scrollbar, fixed smaller size
                self.output_text = Text(self.master, width=55, height=20, state=DISABLED)
                self.output_text.grid(row=2, column=1, padx=10, pady=5, sticky=N)

                # parser output text — scrollbar only here, tallest box
                parser_frame = Frame(self.master)
                parser_frame.grid(row=2, column=2, padx=10, pady=5, sticky=N)
                parser_scroll = Scrollbar(parser_frame)
                parser_scroll.pack(side=RIGHT, fill=Y)
                self.parser_text = Text(parser_frame, width=70, height=40, state=DISABLED,
                                        font=("Courier", 11), yscrollcommand=parser_scroll.set)
                self.parser_text.pack(side=LEFT, fill=BOTH, expand=True)
                parser_scroll.config(command=self.parser_text.yview)

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
                self.output_text.insert(END, "\n".join(tokens) + "\n\n")
                self.output_text.config(state=DISABLED)

                output_lines = parser_logic.parser(tokens, self.current_line + 1)
                parser_out = "\n".join(output_lines)

                self.parser_text.config(state=NORMAL)
                self.parser_text.insert(END, f"####Parse tree for line {self.current_line+1}####\n")
                self.parser_text.insert(END, parser_out)
                self.parser_text.insert(END, "\n\n")
                self.parser_text.config(state=DISABLED)

                self.current_line += 1
                self.line_entry.config(state='normal')
                self.line_entry.delete(0, END)
                self.line_entry.insert(0, str(self.current_line))
                self.line_entry.config(state='readonly')


if __name__ == "__main__":
        root = Tk()
        app = LexerGUI(root)
        root.mainloop()