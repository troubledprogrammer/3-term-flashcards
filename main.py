from settings import *
from card import Card

from random import randint

from parsers.default import parse


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
