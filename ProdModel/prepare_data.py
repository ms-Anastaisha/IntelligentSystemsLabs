import pandas as pd


def add_explanations(facts_file: str, productions_file: str):
    facts = pd.read_csv(facts_file, sep=';')
    productions = pd.read_csv(productions_file, sep=';')
    interpretation_column = []
    facts_values = {}
    for i, row in facts.iterrows():
        facts_values[row["fact_id"]] = row["fact_name"]
    for i, row in productions.iterrows():
        from_facts = row["from_facts"].split(',')
        s = "Если "
        for fact in from_facts:
            s += facts_values[fact] + ', '
        s += "то " + facts_values[row["to_fact"]]
        interpretation_column.append(s)
    productions["interpretation"] = interpretation_column
    productions.to_csv(productions_file, index=False)


if __name__ == '__main__':
    add_explanations("./data/facts.txt",
                     "./data/productions.txt")
