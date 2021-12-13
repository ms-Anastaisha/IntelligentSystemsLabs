from collections import defaultdict, deque
from tkinter import *
import re
import pandas as pd
from tkinter.font import Font

from backward_chaining import SolutionTree
from utils import parse_products, parse_facts


class ProdModel:
    def __init__(self, facts_file, products_file):
        ## tkinter configuration
        self.window = Tk()
        self.window.title("Продукционная модель - выбор книг")
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='book.png'))
        self.myFont = Font(family="Helvetica", size=14)
        self.window.resizable(False, False)

        ## init
        self.visible, self.facts, self.final_facts = parse_facts(facts_file)
        self.products = parse_products(products_file)

        ## control buttons
        self.button_forward = Button(self.window, text="Прямой вывод", command=self.init_forward, width=30,
                                     font=self.myFont)
        self.button_backward = Button(self.window, text="Обратный вывод", command=self.init_backward, width=30,
                                      font=self.myFont)
        self.button_forward.grid(column=0, row=0)
        self.button_backward.grid(column=1, row=0)

        ## texts outputs
        self.fact_text = Text(self.window, width=50, font=self.myFont)
        self.final_text = Text(self.window, width=50, font=self.myFont)
        self.result_text = Text(self.window, width=50, font=self.myFont)
        self.fact_text.grid(column=0, row=1)
        self.final_text.grid(column=1, row=1)
        self.result_text.grid(column=2, row=1)

        ## checkbuttons
        self.fact_checkbuttons = []
        self.fact_vars = []
        for fact, text in self.facts.items():
            if fact in self.visible:
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

    def forward_chaining(self, init_facts):
        reasoning = defaultdict(list)
        while True:
            suitable_products = []
            for pname, pbody in self.products.items():
                if pbody[0].issubset(init_facts):
                    if pbody[1] in init_facts: continue
                    suitable_products.append((pname, *pbody))
            if len(suitable_products) == 0:
                break
            suitable_products.sort(key=lambda value: len(value[1]), reverse=True)
            for p in suitable_products:
                if p[2] not in init_facts:
                    init_facts.add(p[2])
                    for f in p[1]:
                        reasoning[p[2]].extend(reasoning[f])
                    reasoning[p[2]].append(p[0])
        return reasoning

    def backward_chaining(self, init_facts, final):
        solutionTree = SolutionTree(init_facts, final, self.products)
        return solutionTree.resolve()

    def init_forward(self):
        init_facts = []
        for cb, var in zip(self.fact_checkbuttons, self.fact_vars):
            text = cb.cget("text")
            value = var.get()
            result = re.search(r"\(([A-Za-z0-9\-]+)\)", text).group(1)
            if value == 1:
                init_facts.append(result)
        reasoning = self.forward_chaining(set(init_facts))
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", END)
        for f in reasoning:
            if f in self.final_facts:
                s = ""
                reason = reasoning[f]
                for r in reason:
                    s += "%s \n и " % self.products[r][2]
                s = s[:-2]
                self.result_text.insert(INSERT, "%s\n" % s)
        self.result_text.configure(state="disabled")

    def init_backward(self):
        init_facts = []
        for cb, var in zip(self.fact_checkbuttons, self.fact_vars):
            text = cb.cget("text")
            value = var.get()
            result = re.search(r"\(([A-Za-z0-9\-]+)\)", text).group(1)
            if value == 1:
                init_facts.append(result)
        final_fact = ""
        for cb, var in zip(self.final_checkbuttons, self.final_vars):
            text = cb.cget("text")
            value = var.get()
            result = re.search(r"\(([A-Za-z0-9\-]+)\)", text).group(1)
            if value == 1:
                final_fact = result
                break
        answer = self.backward_chaining(set(init_facts), final_fact)
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", END)
        self.result_text.insert(INSERT, answer)
        self.result_text.configure(state="disabled")


if __name__ == '__main__':
    ProdModel('./data/facts.txt', './data/productions.txt')
    # print(prod_model.backward_chaining({"f-2","f-11", "f-5" }, "f-10"))
