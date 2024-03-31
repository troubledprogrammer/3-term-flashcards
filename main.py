import tkinter as tk
import customtkinter as ctk

from random import randint

from parsers.default import parse

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

BUTTON_FONT = ('wasy10', 40)


class Card(ctk.CTkFrame):
    WRAP_LENGTH = 7

    def __init__(self, master):
        self.shown: bool = False
        self.default_shown: tk.BooleanVar = tk.BooleanVar(value=True)
        self.text: tk.StringVar = tk.StringVar(value="<No term>")
        super().__init__(master, corner_radius=0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=8)
        self.grid_columnconfigure(0, weight=1)

        self.shown_toggle: ctk.CTkSwitch = ctk.CTkSwitch(self, width=300, text="", variable=self.default_shown)
        self.shown_toggle.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.term_button: ctk.CTkButton = ctk.CTkButton(self, width=300, height=400, command=self.card_button_event, textvariable=self.text, font=BUTTON_FONT)
        self.term_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.terms = []
        self.current_term = 0

    def add_term(self, term: str) -> None:
        # self.terms.append(term)
        # wrap term
        res: list[str] = []

        term: list[str] = term.split(" ")
        temp: str = ""

        while term:
            temp += term.pop(0)
            l: int = len(term[0]) + 1 if term else 0
            if len(temp) + l > self.WRAP_LENGTH:
                res.append(temp)
                temp = ""
            else:
                temp += " "
        res.append(temp)

        self.terms.append("\n".join(res))

    def next_term(self, next_term: int = None):
        if not next_term:
            self.current_term += 1
            self.current_term %= len(self.terms)

        else:
            self.current_term = next_term

        if self.default_shown.get():
            self.show()
        else:
            self.hide()

    def card_button_event(self) -> None:
        if not self.shown:
            self.show()
        else:
            self.hide()

    def show(self) -> None:
        self.shown = True
        try:
            self.text.set(self.terms[self.current_term])
        except IndexError:
            self.text.set("<No term>")

    def hide(self) -> None:
        self.shown = False
        self.text.set("")
        # self.text.set("click\nto\nreveal")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # get terms
        with open("sets/set.txt", "r", encoding="utf8") as f:
            contents: str = f.read()
        terms: list[list[str]] = parse(contents)
        self.num_terms: int = len(terms)

        # configure window
        self.title("Better quizlet.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)

        # add cards
        self.card_1: Card = Card(self)
        self.card_1.grid(row=1, column=0, sticky="nsew")

        self.card_2: Card = Card(self)
        self.card_2.grid(row=1, column=1, sticky="nsew")

        self.card_3: Card = Card(self)
        self.card_3.grid(row=1, column=2, sticky="nsew")

        self.cards: list[Card] = [self.card_1, self.card_2, self.card_3]

        # add terms to cards
        for term in terms:
            for t, c in zip(term, self.cards):
                c.add_term(t)

        # display terms
        for c in self.cards:
            c.show()

        # next term button
        self.next_button: ctk.CTkButton = ctk.CTkButton(self, height=20, command=self.next_term, text="Next", font=BUTTON_FONT)
        self.next_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def next_term(self) -> None:
        rand_term: int = randint(0, self.num_terms - 1)
        for c in self.cards:
            c.next_term(rand_term)


if __name__ == "__main__":
    app: App = App()
    app.mainloop()
