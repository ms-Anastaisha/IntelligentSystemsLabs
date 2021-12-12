from pathlib import Path
import clips
import re
from utils import text_output_clear, text_output_write


def load_clips_file(environment, filename):
    if (len(list(environment.facts())) == 0 and
            len(list(environment.rules())) == 0 and
            len(list(environment.templates())) == 0 and
            len(list(environment.defined_facts())) == 0):
        environment.load(filename)
    else:
        handle_multiple_files(environment, filename)
    environment.reset()


def handle_multiple_files(environment, filename):
    basename = Path(filename).stem
    with open(filename, encoding='utf-8-sig', errors='ignore') as f:
        construct_lines = []
        for line in f:
            if line == '\n':
                if len(construct_lines) == 0: continue
                construct = find_construct(environment, construct_lines)
                if construct is None: continue
                if not compare_constructs(construct_lines, construct):
                    rename_construct(construct_lines, basename)
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
    return " ".join(re.sub("\n", "", construct_lines)) == construct2


def rename_construct(construct_lines, postfix):
    construct_type, construct_name = construct_lines[0].split()
    construct_lines[0] = construct_type + " " + construct_name + postfix


def insert_construct(environment, construct_lines):
    # construct_type, construct_name = construct_lines[0].split()
    # construct_type = construct_type[1:]
    construct = "".join(construct_lines)
    environment.build(construct)

def create_clips_file(facts: dict, rules: dict, output_file: str = "rules_clips.clp") -> None:
    clips_facts = {k: fact2clips(v) for k, v in facts.items()}
    clips_lines = []
    rule_cnt = 0
    for _, rule in rules.items():
        to_fact = rule[1]
        from_fact_set = rule[0]
        clips_lines.append("(defrule rule%d\n" % rule_cnt)
        rule_cnt += 1
        s = ""
        for fact in from_fact_set:
            s += facts[fact] + ", "
            clips_lines.appned(clips_facts[fact] + "\n")
        s = s[:-2]
        s += " => " + facts[to_fact]
        clips_lines.append("=>\n")
        clips_lines.append("(assert %s)\n" % clips_facts[to_fact])
        clips_lines.append('(assert (appendmessagehalt "%s"))\n)\n\n' % s)

    with open(output_file, 'w') as out:
        out.writelines(clips_lines)


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


def fact2clips(fact: str) -> str:
    words = fact.split()
    if words[0] == 'книга':
        return "(book (data %s))" % " ".join(words[1:])
    elif words[0] == 'жанр':
        return "(genre (data %s))" % " ".join(words[1:])
    elif words[0] == 'в':
        return "(plot (data %s))" % fact
    elif words[0] == 'для':
        return "(mood (data %s))" % fact
    elif words[0] == 'автор':
        return "(author (data %s))" % " ".join(words[1:])
    elif words[0] == 'подходит':
        return "(age (data %s))" % fact
    elif words[0] == 'объем':
        return "(volume (data %s))" % fact
    elif words[0] == 'язык':
        return "(language (data %s))" % fact
    elif words[0] == 'входит' or words[0] == 'не':
        return "(school (data %s))" % fact
