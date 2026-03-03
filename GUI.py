from tkinter import *
from tkinter import messagebox
from main import CutOneLineTokens
import re

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
                Label(self.master, text="").grid(row=3, column=0, padx=10, sticky=E)
                self.line_entry = Entry(self.master, width=5, justify="center")
                self.line_entry.insert(0, "0")
                self.line_entry.config(state="readonly")
                self.line_entry.grid(row=3, column=1, sticky=W)

                #handle buttons
                Button(self.master, text="Next Line", command=self.next_line).grid(row=4, column=1, padx=10)
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

                tokens = self.lexer.cut_line_tokens(line)

                self.output_text.config(state=NORMAL)
                self.output_text.inset(END, f"Line {self.current_line+1}: {line}\n ")
                self.output.test.insert(END, f"{line}\n\n")
                self.output_test.config(state=DISABLED)

                self.current_line += 1
                self.line_var.set(str(self.current_line))


if __name__ == "__main__":
        root = Tk()
        app = LexerGUI(root)
        root.mainloop()

