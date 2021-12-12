from collections import defaultdict, deque
from tkinter import *
import re
import clips
import pandas as pd


class ExpertSystem:
    def __init__(self, facts_file, products_file):
        self.window = Tk()
        self.window.title("Экспертная система - выбор книг")
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='book.png'))

        ## inits
        self.visible = set()
        self.facts = {}
        self.final_facts = {}
        self.products = {}
        self._parse_facts(facts_file)
        self._parse_products(products_file)

        ## texts outputs
        self.fact_text = Text(self.window)
        self.final_text = Text(self.window)
        self.result_text = Text(self.window)
        self.fact_text.grid(column=0, row=0)
        self.final_text.grid(column=0, row=1)
        self.result_text.grid(column=1, row=0)

        ## control buttons
        self.button_download = Button(self.window, text="Загрузить clips файл", command=self.download)
        self.button_chaining = Button(self.window, text="Вывод", command=self.clips_chaining)
        self.button_generate = Button(self.window, text="Сгенерировать clips файл", command=self.generate_clips)
        self.button_download.grid(column=1, row=1, sticky=NW)
        self.button_chaining.grid(column=1, row=1, sticky=W)
        self.button_generate.grid(column=1, row=1, sticky=SW)

        ## checkbuttons
        self.fact_checkbuttons = []
        self.fact_vars = []
        for fact, text in self.facts.items():
            var = IntVar(value=0)
            cb = Checkbutton(self.fact_text, text="%s(%s)" % (text, fact),
                             variable=var, onvalue=1, offvalue=0)
            self.fact_text.window_create("end", window=cb)
            self.fact_text.insert("end", "\n")
            self.fact_checkbuttons.append(cb)
            self.fact_vars.append(var)

        self.final_checkbuttons = []
        self.final_vars = []
        for fact, text in self.final_facts.items():
            var = IntVar(value=0)
            cb = Checkbutton(self.final_text, text="%s(%s)" % (text, fact),
                             variable=var, onvalue=1, offvalue=0)
            self.final_text.window_create("end", window=cb)
            self.final_text.insert("end", "\n")
            self.final_checkbuttons.append(cb)
            self.final_vars.append(var)

        self.fact_text.configure(state="disabled")
        self.final_text.configure(state="disabled")
        self.result_text.configure(state="disabled")

        self.window.mainloop()

    def _parse_facts(self, filename):
        data = pd.read_csv(filename, sep=';')
        for _, row in data.iterrows():
            if row["status"] == "f":
                self.final_facts[row["fact_id"]] = row["fact_name"]
                continue
            elif row["status"] != "i":
                self.visible.add(row["fact_id"])
            self.facts[row["fact_id"]] = row["fact_name"]

    def _parse_products(self, filename):
        data = pd.read_csv(filename)
        for _, row in data.iterrows():
            from_facts_set = set(row.loc["from_facts"].split(','))
            self.products[row["rule_id"]] = (from_facts_set, row["to_fact"], row["interpretation"])

    def download(self):
        pass

    def generate_clips(self):
        pass

    def clips_chaining(self):
        pass


if __name__ == '__main__':
    ExpertSystem('data/facts.txt', 'data/productions.txt')
