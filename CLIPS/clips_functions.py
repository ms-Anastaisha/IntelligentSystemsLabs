from pathlib import Path
import clips
import re
from utils import text_output_clear, text_output_write, read_file
import os

CLIPS_INIT = """(deftemplate ioproxy
    (slot fact-id)
    (multislot answers)
    (multislot messages)
    (slot reaction)
    (slot value)
    (slot restore)
)

(deffacts proxy-fact
    (ioproxy
        (fact-id 0112)
        (value none)
        (messages)
    )
)

(defrule clear-messages
    (declare (salience 90))
    ?clear-msg-flg <- (clearmessage)
    ?proxy <- (ioproxy)
    =>
    (modify ?proxy (messages))
    (retract ?clear-msg-flg)
)

(defrule set-output-and-halt
    (declare (salience 99))
    ?current-message <- (sendmessagehalt ?new-msg)
    ?proxy <- (ioproxy (messages $?msg-list))
    =>
    (modify ?proxy (messages ?new-msg))
    (retract ?current-message)
    (halt)
)

(defrule append-output-and-halt
    (declare (salience 99))
    ?current-message <- (appendmessagehalt $?new-msg)
    ?proxy <- (ioproxy (messages $?msg-list))
    =>
    (modify ?proxy (messages $?msg-list $?new-msg))
    (retract ?current-message)
    (halt)
)

(defrule set-output-and-proceed
    (declare (salience 99))
    ?current-message <- (sendmessage ?new-msg)
    ?proxy <- (ioproxy)
    =>
    (modify ?proxy (messages ?new-msg))
    (retract ?current-message)
)

(defrule append-output-and-proceed
    (declare (salience 99))
    ?current-message <- (appendmessage ?new-msg)
    ?proxy <- (ioproxy (messages $?msg-list))
    =>
    (modify ?proxy (messages $?msg-list ?new-msg))
    (retract ?current-message)
)

(deftemplate book
(slot data)
) 

(deftemplate plot
(slot data)
) 

(deftemplate author
(slot data)
) 

(deftemplate genre
(slot data)
) 

(deftemplate volume
(slot data)
) 

(deftemplate language
(slot data)
) 

(deftemplate school
(slot data)
) 

(deftemplate duration
(slot data)
) 

(deftemplate age
(slot data)
) 

(deftemplate mood
(slot data)
) 
"""


#####################Loading clips files
def load_clips_file(environment, filename, text_widget):
    if (len(list(environment.facts())) == 0 and
            len(list(environment.rules())) == 0 and
            len(list(environment.templates())) == 0 and
            len(list(environment.defined_facts())) == 0):
        environment.load(filename)
    else:
        handle_multiple_files(environment, filename)
    filetemp = 'temp.clp'
    environment.save(filetemp)
    text = read_file(filetemp)
    text_output_clear(text_widget)
    text_output_write(text_widget, text)
    os.remove(filetemp)
    environment.reset()


def handle_multiple_files(environment, filename):
    basename = Path(filename).stem
    with open(filename, encoding='utf-8-sig', errors='ignore') as f:
        construct_lines = []
        for line in f:
            if line == '\n':
                if len(construct_lines) == 0: continue
                construct = find_construct(environment, construct_lines)
                if construct is not None:
                    if not compare_constructs(construct_lines, construct):
                        rename_construct(construct_lines, basename)
                    else:
                        construct_lines = []
                        continue
                insert_construct(environment, construct_lines)
                construct_lines = []
            else:
                construct_lines.append(line)


def find_construct(environment, construct_lines):
    construct_type, construct_name = construct_lines[0].split()
    construct_type = construct_type[1:]
    try:
        if construct_type == 'deftemplate':
            return re.sub("MAIN::", "", str(environment.find_template(construct_name)))
        elif construct_type == 'deffacts':
            return re.sub("MAIN::", "", str(environment.find_defined_facts(construct_name)))
        elif construct_type == 'defrule':
            return re.sub("MAIN::", "", str(environment.find_rule(construct_name)))
    except Exception:
        return None


def compare_constructs(construct_lines, construct2):
    construct1 = re.sub("\n", "", " ".join(construct_lines))
    return "".join(construct1.split()) == "".join(construct2.split())


def rename_construct(construct_lines, postfix):
    construct_type, construct_name = construct_lines[0].split()
    construct_lines[0] = construct_type + " " + construct_name + postfix


def insert_construct(environment, construct_lines):
    construct = " ".join(construct_lines)
    environment.build(construct)


#####################Generating clips files
def fact2clips(fact: str) -> str:
    word = fact.split()[0]
    value_dict = {
        'книга': '(book (data "%s"))' % fact,
        'жанр': '(genre (data "%s"))' % fact,
        'в': '(plot (data "%s"))' % fact,
        'для': '(mood (data "%s"))' % fact,
        'автор': '(author (data "%s"))' % fact,
        'авторы': '(author (data "%s"))' % fact,
        'подходит': '(age (data "%s"))' % fact,
        'объем': '(volume (data "%s"))' % fact,
        'язык': '(language (data "%s"))' % fact,
        'входит': '(school (data "%s"))' % fact,
        'не': '(school (data "%s"))' % fact,
        'на': '(duration (data "%s"))' % fact
    }
    return value_dict[word]


def create_clips_file(facts: dict, final_facts: dict, rules: dict, output_file: str = "rules_clips.clp") -> None:
    merged_facts = {}
    merged_facts.update(facts)
    merged_facts.update(final_facts)
    clips_facts = {k: fact2clips(v) for k, v in merged_facts.items()}
    clips_lines = [CLIPS_INIT + "\n\n"]
    rule_cnt = 0
    for _, rule in rules.items():
        to_fact = rule[1]
        from_fact_set = rule[0]
        clips_lines.append("(defrule rule%d\n" % rule_cnt)
        rule_cnt += 1
        s = ""
        for fact in from_fact_set:
            s += facts[fact] + ", "
            clips_lines.append(clips_facts[fact] + "\n")
        s = s[:-2]
        s += " => " + merged_facts[to_fact]
        clips_lines.append("=>\n")
        clips_lines.append("(assert %s)\n" % clips_facts[to_fact])
        clips_lines.append('(assert (appendmessagehalt "%s"))\n)\n\n' % s)

    with open(output_file, 'w', encoding='utf-8-sig') as out:
        out.writelines(clips_lines)


#######################Running clips
def run_clips_chaining(clips, from_facts, facts, text_widget):
    text_output_clear(text_widget)
    clips.reset()
    clips.run()
    handle_user_response(clips, text_widget)
    for ff in from_facts:
        clips_fact = fact2clips(facts[ff])
        clips.eval("(assert %s})" % clips_fact)
    while True:
        clips.run()
        end = handle_user_response(clips, text_widget)
        if not end:
            break


def handle_user_response(clips, text_widget):
    evaluation_str = "(find-fact ((?f ioproxy)) TRUE)"
    fact_value = clips.eval(evaluation_str)[0]
    messages = fact_value["messages"]
    answers = fact_value["answers"]

    for msg in messages:
        text_output_write(text_widget, msg + "\n\n")
        if msg == "":
            if len(answers) == 0:
                clips.eval("(assert (clearmessage))")
            return False
    if len(messages) == 0:
        if len(answers) == 0:
            clips.eval("(assert (clearmessage))")
        return False

    if len(answers) == 0:
        clips.eval("(assert (clearmessage))")

    return True
