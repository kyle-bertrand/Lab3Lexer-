import re
from tkinter import *

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
                self.title_label.place(row = 0, column = 0, columnspan = 2, pady=10)