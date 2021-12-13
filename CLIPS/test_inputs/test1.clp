(deftemplate mood
(slot data)
)

(deftemplate moodsfdd
(slot data)
(slot title)
)


(defrule rule0
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
(author (data "автор Джоан Ролинг3423642"))
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
