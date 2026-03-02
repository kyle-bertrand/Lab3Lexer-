from tkinter import *
from tkinter import messagebox

class LexerGUI:
        def __init__(self, root):
                self.master = root
                self.master.title("Lexer GUI")
                self.master.geometry("900x600")

                #variables
                self.lines = []
                self.current_line = 0

                #title
                self.title_label = Label(self.master, text="Tinypie Lexer GUI", font=("Arial", 12, "bold"))
                self.title_label.grid(row = 0, column = 0, columnspan = 2, pady=10)

                #source code label
                self.src_label = Label(self.master, text="Source Code Input:", font=("Arial", 12, "bold"))
                self.src_label.grid(row = 1, column = 1, padx=10, sticky = W)

                #output label
                self.output_label = Label(self.master, text="Lexical Analyzed Output:", font=("Arial", 12, "bold"))
                self.output_label.grid(row=1, column=1, padx=10, sticky=W)

                #input text
                self.src_text = Text(self.master, width=60, height=20)
                self.src_text.grid(row=2, column=0, padx=10)

                #output text
                #handle buttons


        #def next_line(self):

root = Tk()
app = LexerGUI(root)
root.mainloop()

