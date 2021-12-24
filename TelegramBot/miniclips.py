import clips
import pandas as pd


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


def fact2template(fact: str) -> str:
    word = fact.split()[0]
    value_dict = {
        'книга': 'book',
        'жанр': 'genre',
        'в': 'plot',
        'для': 'mood',
        'автор': 'author',
        'авторы': 'author',
        'подходит': 'age',
        'объем': 'volume',
        'язык': 'language',
        'входит': 'school',
        'не': 'school',
        'на': 'duration'
    }
    return value_dict[word]


class Miniclips:
    def __init__(self, facts_file, products_file, clips_filename):
        self.visible, self.facts, self.final_facts = parse_facts(facts_file)
        self.products = parse_products(products_file)
        self.environment = clips.Environment()
        self.environment.load(clips_filename)
        self.environment.reset()
        self.visible_facts2numbers = {}

        i = 1
        for fact, text in self.facts.items():
            if fact in self.visible:
                self.visible_facts2numbers[i] = (text, fact)
                i += 1

        self.message_result = ""

    def message(self):
        return "Укажите необходимые свойства через запятую(без пробелов):\n" + \
               "\n".join([str(i) + ':' + fact[0] for i, fact in self.visible_facts2numbers.items()])

    def proceed(self, msg):
        try:
            fact_nums = list(map(int, msg.split(',')))
        except Exception:
            return "Некорректный ввод"
        init_facts = []
        for i in fact_nums:
            if i not in fact_nums:
                return "Некорректный ввод"
            init_facts.append(self.visible_facts2numbers[i][1])
        self.message_result = ""
        return self._run_clips_chaining(init_facts)

    def _run_clips_chaining(self, from_facts):
        self.environment.reset()
        self.environment.run()
        self._handle_user_response(self.environment)
        for ff in from_facts:
            template = self.environment.find_template(fact2template(self.facts[ff]))
            template.assert_fact(data=self.facts[ff])
        while True:
            self.environment.run()
            end = self._handle_user_response(self.environment)
            if not end:
                return self.message_result + "Наберите \\return, чтобы выйти"

    def _handle_user_response(self, environment):
        evaluation_str = "(find-fact ((?f ioproxy)) TRUE)"
        fact_value = environment.eval(evaluation_str)[0]
        messages = fact_value["messages"]
        answers = fact_value["answers"]

        for msg in messages:
            msg = msg.replace("=>", "|")
            from_, to_ = msg.split("|")
            if "книга" in to_:
                self.message_result += to_ + "\n"
            if msg == "":
                if len(answers) == 0:
                    environment.eval("(assert (clearmessage))")
                return False
        if len(messages) == 0:
            if len(answers) == 0:
                environment.eval("(assert (clearmessage))")
            return False

        if len(answers) == 0:
            environment.eval("(assert (clearmessage))")

        return True
