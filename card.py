from settings import *


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

        self.term_button: ctk.CTkButton = ctk.CTkButton(self, width=300, height=400, command=self.card_button_event,
                                                        textvariable=self.text, font=BUTTON_FONT)
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
