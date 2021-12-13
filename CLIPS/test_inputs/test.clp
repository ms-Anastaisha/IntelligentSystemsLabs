(deftemplate ioproxy
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


(defrule rule0
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
(author (data "автор Джоан Ролинг"))
=>
(assert (book (data "книга Гарри Поттер и философский Камень")))
(assert (appendmessagehalt "жанр фэнтези, объем от 300 до 600 страниц, автор Джоан Ролинг => книга Гарри Поттер и философский Камень"))
)

(defrule rule1
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
(author (data "автор Джоан Ролинг"))
=>
(assert (book (data "книга Гарри Поттер и Тайная комната")))
(assert (appendmessagehalt "жанр фэнтези, объем от 300 до 600 страниц, автор Джоан Ролинг => книга Гарри Поттер и Тайная комната"))
)

(defrule rule2
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
(author (data "автор Джоан Ролинг"))
=>
(assert (book (data "книга Гарри Поттер и узник Азкабана")))
(assert (appendmessagehalt "жанр фэнтези, объем от 300 до 600 страниц, автор Джоан Ролинг => книга Гарри Поттер и узник Азкабана"))
)

(defrule rule3
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
(author (data "автор Джоан Ролинг"))
=>
(assert (book (data "книга Гарри Поттер и Кубок Огня")))
(assert (appendmessagehalt "жанр фэнтези, объем от 300 до 600 страниц, автор Джоан Ролинг => книга Гарри Поттер и Кубок Огня"))
)

(defrule rule4
(genre (data "жанр фэнтези"))
(volume (data "объем от 600 страниц"))
(author (data "автор Джоан Ролинг"))
=>
(assert (book (data "книга Гарри Поттер и Орден Феникса")))
(assert (appendmessagehalt "жанр фэнтези, объем от 600 страниц, автор Джоан Ролинг => книга Гарри Поттер и Орден Феникса"))
)

(defrule rule5
(genre (data "жанр фэнтези"))
(volume (data "объем от 600 страниц"))
(author (data "автор Джоан Ролинг"))
=>
(assert (book (data "книга Гарри Поттер и Принц-Полукровка")))
(assert (appendmessagehalt "жанр фэнтези, объем от 600 страниц, автор Джоан Ролинг => книга Гарри Поттер и Принц-Полукровка"))
)

(defrule rule6
(genre (data "жанр фэнтези"))
(volume (data "объем от 600 страниц"))
(author (data "автор Джоан Ролинг"))
=>
(assert (book (data "книга Гарри Поттер и Дары Смерти")))
(assert (appendmessagehalt "жанр фэнтези, объем от 600 страниц, автор Джоан Ролинг => книга Гарри Поттер и Дары Смерти"))
)

(defrule rule7
(author (data "автор Лев Толстой"))
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
=>
(assert (book (data "книга Анна Каренина")))
(assert (appendmessagehalt "автор Лев Толстой, объем от 600 страниц, жанр реализм => книга Анна Каренина"))
)

(defrule rule8
(genre (data "жанр исторический"))
(author (data "автор Лев Толстой"))
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
=>
(assert (book (data "книга Война и мир")))
(assert (appendmessagehalt "жанр исторический, автор Лев Толстой, объем от 600 страниц, жанр реализм => книга Война и мир"))
)
