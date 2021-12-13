from utils import text_output_clear, text_output_write


#######################Running clips

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


def run_clips_chaining(environment, from_facts, facts, text_widget):
    text_output_clear(text_widget)
    environment.reset()
    environment.run()
    handle_user_response(environment, text_widget)
    for ff in from_facts:
        template = environment.find_template(fact2template(facts[ff]))
        template.assert_fact(data=facts[ff])
    while True:
        environment.run()
        end = handle_user_response(environment, text_widget)
        if not end:
            break


def handle_user_response(environment, text_widget):
    evaluation_str = "(find-fact ((?f ioproxy)) TRUE)"
    fact_value = environment.eval(evaluation_str)[0]
    messages = fact_value["messages"]
    answers = fact_value["answers"]

    for msg in messages:
        text_output_write(text_widget, msg + "\n\n")
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
