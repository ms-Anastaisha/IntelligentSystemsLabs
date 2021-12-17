from typing import Tuple

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
(slot weight)
) 

(deftemplate plot
(slot data)
(slot weight)
) 

(deftemplate author
(slot data)
(slot weight)
) 

(deftemplate genre
(slot data)
(slot weight)
) 

(deftemplate volume
(slot data)
(slot weight)
) 
(deftemplate language
(slot data)
(slot weight)
) 

(deftemplate school
(slot data)
(slot weight)
) 

(deftemplate age
(slot data)
(slot weight)
) 

(deftemplate mood
(slot data)
(slot weight)
) 

(deftemplate duration
(slot data)
(slot weight)
) 
"""


#####################Generating clips files
def fact2clips(fact: str) -> str:
    word = fact.split()[0]
    value_dict = {
        'книга': '(book (data "%s") (weight ?book_w))' % fact,
        'жанр': '(genre (data "%s") (weight ?genre_w))' % fact,
        'в': '(plot (data "%s") (weight ?plot_w))' % fact,
        'для': '(mood (data "%s") (weight ?mood_w))' % fact,
        'автор': '(author (data "%s") (weight ?author_w))' % fact,
        'авторы': '(author (data "%s") (weight ?author_w))' % fact,
        'подходит': '(age (data "%s") (weight ?age_w))' % fact,
        'объем': '(volume (data "%s") (weight ?volume_w))' % fact,
        'язык': '(language (data "%s") (weight ?language_w))' % fact,
        'входит': '(school (data "%s") (weight ?school_w))' % fact,
        'не': '(school (data "%s") (weight ?school_w))' % fact,
        'на': '(duration (data "%s") (weight ?duration_w))' % fact
    }
    return value_dict[word]


def fact2weight(fact: str) -> str:
    word = fact.split()[0]
    value_dict = {
        'книга': '?book_w',
        'жанр': '?genre_w',
        'в': '?plot_w',
        'для': '?mood_w',
        'автор': '?author_w',
        'авторы': '?author_w',
        'подходит': '?age_w',
        'объем': '?volume_w',
        'язык': '?language_w',
        'входит': '?school_w',
        'не': '?school_w',
        'на': '?duration_w'
    }
    return value_dict[word]


def get_weight(from_set: set) -> Tuple[float, str]:
    from_words = [from_fact.split()[0] for from_fact in from_set]
    value_dict = {
        'жанр': 0.7,
        'в': 0.75,
        'для': 0.75,
        'автор': 0.8,
        'авторы': 0.8,
        'подходит': 0.65,
        'объем': 0.6,
        'язык': 0.6,
        'входит': 0.6,
        'не': 0.6,
        'на': 0.65
    }
    w = value_dict[from_words[0]] if len(from_words) == 1 else 0.9
    s = '(* %.1f %s)' % (w, " ".join([fact2weight(fact_word) for fact_word in from_words]))
    return w, s


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
            s += facts[fact] + ' ("%s"), ' % fact2weight(facts[fact])
            clips_lines.append(clips_facts[fact] + "\n")
            clips_lines.append('(test ( < 0.3 %s ))\n' % fact2weight(facts[fact]))

        s = s[:-2]
        s += " => " + merged_facts[to_fact]
        weight, weight_string = get_weight({facts[fact] for fact in from_fact_set})
        clips_lines.append('(test ( < 0.3 %s ))\n' % weight_string)
        clips_lines.append("=>\n")
        to_fact_weight = clips_facts[to_fact].replace(fact2weight(merged_facts[to_fact]), weight_string)
        clips_lines.append("(assert %s)\n" % to_fact_weight)
        s += '(" %s ")' % weight_string
        clips_lines.append('(assert (appendmessagehalt (str-cat " %s ")))\n)\n\n' % s)

    with open(output_file, 'w', encoding='utf-8-sig') as out:
        out.writelines(clips_lines)
