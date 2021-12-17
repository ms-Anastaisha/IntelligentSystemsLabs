from utils import text_output_clear, text_output_write
import pyttsx3
import re


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


def run_clips_chaining(environment, from_facts, from_weights, facts, text_widget, window):
    engine = pyttsx3.init()
    text_output_clear(text_widget)
    environment.reset()
    environment.run()
    handle_user_response(environment, text_widget, window, engine)
    for ff, fw in zip(from_facts, from_weights):
        template = environment.find_template(fact2template(facts[ff]))
        template.assert_fact(data=facts[ff],
                             weight=fw)
    while True:
        environment.run()
        end = handle_user_response(environment, text_widget, window, engine)
        if not end:
            break


def handle_user_response(environment, text_widget, window, speech_engine):
    evaluation_str = "(find-fact ((?f ioproxy)) TRUE)"
    fact_value = environment.eval(evaluation_str)[0]
    messages = fact_value["messages"]
    answers = fact_value["answers"]

    for msg in messages:
        text_output_write(text_widget, msg + "\n\n")
        window.update()
        say_msg = re.sub("\(0\.\d+\)", "", msg.replace("=>", "следовательно"))
        speech_engine.say(say_msg)
        speech_engine.runAndWait()
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
