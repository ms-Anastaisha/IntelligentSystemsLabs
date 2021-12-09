import clips


def load_clips_file():
    ...


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


def run_clips_chaining():
    ...


def handle_user_response():
    ...


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
