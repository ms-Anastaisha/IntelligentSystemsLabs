import clips


def load_clips_file(clips, clips_text, file_name, loaded):
    clips.clear()
    s = clips_text + "\n" + loaded
    clips.load(s)
    clips.reset()
    return s



def create_clips_file(facts: dict, rules: dict, output_file: str ="rules_clips.clp") -> None:
    clips_facts = {k: fact2clips(v) for k, v in facts.items()}
    clips_lines = []
    rule_cnt = 0
    for _, rule in rules.items():
        to_fact =  rule[1]
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


def run_clips_chaining(clips, from_facts, facts, text_box):
    text_box.clear() ### ????
    clips.reset()
    clips.run()
    handle_user_response(clips, text_box)
    for ff in from_facts:
        clips_fact = fact2clips(facts[ff])
        clips.eval("(assert %s})" % clips_fact)
    while True:
        clips.run()
        end = handle_user_response(clips, text_box)
        if not end:
            break


def handle_user_response(clips, text_box):
    evaluation_str = "(find-fact ((?f ioproxy)) TRUE)"
    fact_value = clips.eval(evaluation_str)[0]
    messages = fact_value["messages"]
    answers = fact_value["answers"]

    for msg in messages:
        text_box.text += msg + "\n\n"
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