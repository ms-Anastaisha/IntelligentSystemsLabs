from collections import defaultdict, deque
from tkinter import *
import re
import clips


class ProdModel:
    def __init__(self, filename):
        self.window = Tk()
        self.window.title("Продукционная модель - выбор книг")
        self.facts = {}
        self.final_facts = {}
        self.products = {}
        self.parse_facts(filename)

        self.fact_text = Text(self.window)

        self.final_text = Text(self.window)
        self.result_text = Text(self.window)

        self.button_download = Button(self.window, text="Загрузить clips файл", command=self.download)
        self.button_chaining = Button(self.window, text="Вывод", command=self.clips_chaining)
        self.button_generate = Button(self.window, text="Сгенерировать clips файл", command=self.generate_clips)

        self.button_download.grid(column=1, row=1, sticky=NW)
        self.button_chaining.grid(column=1, row=1, sticky=W)
        self.button_generate.grid(column=1, row=1, sticky=SW)

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

    def parse_facts(self, filename):
        with open(filename, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip().split(';')
                if len(line) == 1: continue
                if line[0][0] == 'f':
                    if len(line) == 2:
                        self.facts[line[0]] = line[1]
                    else:
                        self.final_facts[line[0]] = line[1]
                else:
                    line[1] = line[1].split(',')
                    self.products[line[0]] = (set(line[1]), line[2])

    def download(self):
        pass

    def generate_clips(self):
        pass

    def clips_chaining(self):
        pass


if __name__ == '__main__':
    prod_model = ProdModel('C:/Users/Anastaisha/PycharmProjects/ProdModel/facts.txt')
    # print(prod_model.backward_chaining({"f-2","f-11", "f-5" }, "f-10"))
