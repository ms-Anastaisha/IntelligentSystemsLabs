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
        '??????????': '(book (data "%s") (weight ?book_w))' % fact,
        '????????': '(genre (data "%s") (weight ?genre_w))' % fact,
        '??': '(plot (data "%s") (weight ?plot_w))' % fact,
        '??????': '(mood (data "%s") (weight ?mood_w))' % fact,
        '??????????': '(author (data "%s") (weight ?author_w))' % fact,
        '????????????': '(author (data "%s") (weight ?author_w))' % fact,
        '????????????????': '(age (data "%s") (weight ?age_w))' % fact,
        '??????????': '(volume (data "%s") (weight ?volume_w))' % fact,
        '????????': '(language (data "%s") (weight ?language_w))' % fact,
        '????????????': '(school (data "%s") (weight ?school_w))' % fact,
        '????': '(school (data "%s") (weight ?school_w))' % fact,
        '????': '(duration (data "%s") (weight ?duration_w))' % fact
    }
    return value_dict[word]


def fact2weight(fact: str) -> str:
    word = fact.split()[0]
    value_dict = {
        '??????????': '?book_w',
        '????????': '?genre_w',
        '??': '?plot_w',
        '??????': '?mood_w',
        '??????????': '?author_w',
        '????????????': '?author_w',
        '????????????????': '?age_w',
        '??????????': '?volume_w',
        '????????': '?language_w',
        '????????????': '?school_w',
        '????': '?school_w',
        '????': '?duration_w'
    }
    return value_dict[word]


def get_weight(from_set: set) -> Tuple[float, str]:
    from_words = [from_fact.split()[0] for from_fact in from_set]
    value_dict = {
        '????????': 0.7,
        '??': 0.75,
        '??????': 0.75,
        '??????????': 0.8,
        '????????????': 0.8,
        '????????????????': 0.65,
        '??????????': 0.6,
        '????????': 0.6,
        '????????????': 0.6,
        '????': 0.6,
        '????': 0.65
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
