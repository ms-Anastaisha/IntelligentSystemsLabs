from tkinter import *
import re
from tkinter.font import Font
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
import clips
from clips_loading import load_clips_file
from clips_generating import create_clips_file
from clips_chaining import run_clips_chaining
from utils import parse_products, parse_facts, text_output_write, read_file, text_output_clear

filetypes = [("clips files", '*.clp')]


class ExpertSystemCoeff:
    def __init__(self, facts_file, products_file):
        ## tkinter configuration
        self.window = Tk()
        self.window.title("Экспертная система - выбор книг")
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='book.png'))
        self.myFont = Font(family='Helvetica', size=14)
        self.window.resizable(False, False)
        self.status_label = Label(text="", font=self.myFont)
        self.status_label.grid(row=2, columnspan=3, column=0)

        ## clips
        self.environment = clips.Environment()

        ## inits
        self.visible, self.facts, self.final_facts = parse_facts(facts_file)
        self.products = parse_products(products_file)

        ## texts outputs
        self.fact_text = Text(self.window, width=50, font=self.myFont)
        self.file_text = Text(self.window, width=50, font=self.myFont)
        self.result_text = Text(self.window, width=50, font=self.myFont)
        self.fact_text.grid(column=0, row=1)
        self.result_text.grid(column=2, row=1)
        self.file_text.grid(column=1, row=1)

        ## control buttons
        self.button_download = Button(self.window, text="Загрузить clips файл", command=self.download, width=23,
                                      font=self.myFont)
        self.button_chaining = Button(self.window, text="Clips Вывод", command=self.clips_chaining, width=23,
                                      font=self.myFont)
        self.button_generate = Button(self.window, text="Сгенерировать clips файл", command=self.generate_clips,
                                      width=23, font=self.myFont)
        self.button_clear_files = Button(self.window, text="Очистить Clips файлы", command=self.clips_files_clear,
                                         width=23, font=self.myFont)
        self.button_download.grid(column=0, row=0, sticky=NE, padx=7)
        self.button_chaining.grid(column=1, row=0, sticky=NE, padx=7)
        self.button_clear_files.grid(column=1, row=0, sticky=NW, padx=7)
        self.button_generate.grid(column=0, row=0, sticky=NW, padx=7)

        ## checkbuttons
        self.fact_checkbuttons = []
        self.fact_vars = []
        for fact, text in self.facts.items():
            if fact in self.visible:
                var = IntVar(value=0)
                cb = Checkbutton(self.fact_text, text="%s(%s)" % (text, fact),
                                 variable=var, onvalue=1, offvalue=0, font=self.myFont)
                self.fact_text.window_create("end", window=cb)
                self.fact_text.insert("end", "\n")
                self.fact_checkbuttons.append(cb)
                self.fact_vars.append(var)

        self.fact_text.configure(state="disabled")
        self.result_text.configure(state="disabled")
        self.button_chaining.configure(state="disabled")
        self.window.mainloop()

    def _get_init_facts(self):
        init_facts = []
        for cb, var in zip(self.fact_checkbuttons, self.fact_vars):
            text = cb.cget("text")
            value = var.get()
            result = re.search(r"\(([A-Za-z0-9\-]+)\)", text).group(1)
            if value == 1:
                init_facts.append(result)
        return init_facts

    def download(self):
        filename = fd.askopenfilename(filetypes=filetypes)
        load_clips_file(self.environment, filename, self.file_text)
        self.button_chaining.configure(state="normal")
        self.status_label.config(text="Файл загружен", fg="#00f")

    def generate_clips(self):
        filename_for_generated = sd.askstring("Имя файла", "Введите имя файла:",
                                              parent=self.window)
        create_clips_file(self.facts, self.final_facts, self.products, filename_for_generated)
        self.status_label.config(text="Файл сгенерирован", fg="#00f")

    def clips_chaining(self):
        init_facts = self._get_init_facts()
        run_clips_chaining(self.environment, init_facts, self.facts, self.result_text)
        self.status_label.config(text="Вывод окончен", fg="#00f")

    def clips_files_clear(self):
        self.environment.clear()
        text_output_clear(self.file_text)
        self.button_chaining.configure(state="disabled")
        self.status_label.config(text="Файлы очищены", fg="#00f")


if __name__ == '__main__':
    ExpertSystemCoeff('data/facts.txt', 'data/productions.txt')
