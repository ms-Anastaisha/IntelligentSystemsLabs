from collections import defaultdict, deque
from tkinter import *
import re
import pandas as pd


class ProductNode:
    def __init__(self, product, factNode):
        self.node = product
        self.childFactNodes = []
        self.parentFactNode = factNode

    @property
    def resolved(self):
        return len(self.childFactNodes) > 0 and all([node.resolved for node in self.childFactNodes])


class FactNode:
    def __init__(self, fact):
        self.node = fact
        self.childProductNodes = []
        self.parentProductNodes = []
        self.reasoning = []
        self.resFlag = False

    @property
    def resolved(self):
        return self.resFlag or (
                len(self.childProductNodes) > 0 and any([node.resolved for node in self.childProductNodes]))


class SolutionTree:
    def __init__(self, init_facts, final_fact, products):
        self.root = FactNode(final_fact)
        self.products = products
        self.init_facts = init_facts

    def resolve(self):
        treeFacts = {self.root}
        while len(treeFacts) > 0:
            fact = treeFacts.pop()
            for pname, pbody in self.products.items():
                if pbody[1] == fact.node:
                    productNode = ProductNode(pname, fact)
                    fact.childProductNodes.append(productNode)
                    for f in pbody[0]:
                        fnode = FactNode(f)
                        productNode.childFactNodes.append(fnode)
                        if f not in self.init_facts:
                            treeFacts.add(fnode)
                        else:
                            fnode.resFlag = True
        if self.root.resolved:
            return self._answer()
        return "unresolved"

    def _answer(self):
        answer = ""
        treeFacts = [self.root]
        while len(treeFacts) > 0:
            fact = treeFacts.pop(0)
            answer += fact.node + ' <= '
            if len(fact.childProductNodes) == 0:
                answer += "initial\n"
            else:
                for product in fact.childProductNodes:
                    if product.resolved:
                        for i in range(len(product.childFactNodes)):
                            answer += product.childFactNodes[i].node
                            treeFacts.append(product.childFactNodes[i])
                            if i < len(product.childFactNodes) - 1:
                                answer += ','
                        answer += '(' + product.node + ')\n'
                        break

        return answer


class ProdModel:
    def __init__(self, facts_file, products_file):
        self.window = Tk()
        self.window.title("Продукционная модель - выбор книг")

        ## init
        self.visible = set()
        self.facts = {}
        self.final_facts = {}
        self.products = {}
        self._parse_facts(facts_file)
        self._parse_products(products_file)

        ## control buttons
        self.button_forward = Button(self.window, text="Прямой вывод", command=self.init_forward)
        self.button_backward = Button(self.window, text="Обратный вывод", command=self.init_backward)
        self.button_forward.grid(column=1, row=1, sticky=NW)
        self.button_backward.grid(column=1, row=1, sticky=W)

        ## texts outputs
        self.fact_text = Text(self.window)
        self.final_text = Text(self.window)
        self.result_text = Text(self.window)
        self.fact_text.grid(column=0, row=0)
        self.final_text.grid(column=0, row=1)
        self.result_text.grid(column=1, row=0)

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

        print(self.facts)
        print(self.final_facts)
        print(len(self.visible))

    # with open(filename, 'r', encoding='utf8') as f:
    #     for line in f:
    #         line = line.strip().split(';')
    #         if len(line) == 1: continue
    #         if line[0][0] == 'f':
    #             if len(line) == 2:
    #                 self.facts[line[0]] = line[1]
    #             else:
    #                 self.final_facts[line[0]] = line[1]
    #         else:
    #             line[1] = line[1].split(',')
    #             self.products[line[0]] = (set(line[1]), line[2])

    def _parse_products(self, filename):
        ...

    def forward_chaining(self, init_facts):
        reasoning = defaultdict(list)
        while True:
            suitable_products = []
            for pname, pbody in self.products.items():
                if pbody[0].issubset(init_facts):
                    if len(init_facts) > 1 and len(pbody) == 1:
                        continue
                    if pbody[1] in init_facts: continue
                    suitable_products.append((pname, *pbody))
            if len(suitable_products) == 0:
                break
            suitable_products.sort(key=lambda value: len(value[1]), reverse=True)
            for p in suitable_products:
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
                self.result_text.insert(INSERT, "%s(%s)\n" % (self.final_facts[f], f))
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
    prod_model = ProdModel('./data/facts.txt', './data/productions.txt')
    # print(prod_model.backward_chaining({"f-2","f-11", "f-5" }, "f-10"))
