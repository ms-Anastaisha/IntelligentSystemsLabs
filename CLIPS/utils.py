import pandas as pd
from tkinter import *


def parse_products(filename):
    products = {}
    data = pd.read_csv(filename)
    for _, row in data.iterrows():
        from_facts_set = set(row.loc["from_facts"].split(','))
        products[row["rule_id"]] = (from_facts_set, row["to_fact"], row["interpretation"])
    return products


def parse_facts(filename):
    visible, facts, final_facts = set(), {}, {}
    data = pd.read_csv(filename, sep=';')
    for _, row in data.iterrows():
        if row["status"] == "f":
            final_facts[row["fact_id"]] = row["fact_name"]
            continue
        elif row["status"] != "i":
            visible.add(row["fact_id"])
        facts[row["fact_id"]] = row["fact_name"]
    return visible, facts, final_facts


def text_output_clear(text_widget):
    text_widget.configure(state="normal")
    text_widget.delete(1.0, END)
    text_widget.configure(state="disabled")


def text_output_write(text_widget, text):
    text_widget.configure(state="normal")
    text_widget.insert(INSERT, "%s" % text)
    text_widget.configure(state="disabled")

def read_file(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        text = "\n".join(lines)
    return text



