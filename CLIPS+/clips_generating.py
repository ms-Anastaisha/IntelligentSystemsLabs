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
