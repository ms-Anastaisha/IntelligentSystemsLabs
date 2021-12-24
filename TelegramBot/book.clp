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
(author (data "автор Джоан Ролинг"))
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Гарри Поттер и философский Камень")))
(assert (appendmessagehalt "автор Джоан Ролинг, жанр фэнтези, объем от 300 до 600 страниц => книга Гарри Поттер и философский Камень"))
)

(defrule rule1
(author (data "автор Джоан Ролинг"))
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Гарри Поттер и Тайная комната")))
(assert (appendmessagehalt "автор Джоан Ролинг, жанр фэнтези, объем от 300 до 600 страниц => книга Гарри Поттер и Тайная комната"))
)

(defrule rule2
(author (data "автор Джоан Ролинг"))
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Гарри Поттер и узник Азкабана")))
(assert (appendmessagehalt "автор Джоан Ролинг, жанр фэнтези, объем от 300 до 600 страниц => книга Гарри Поттер и узник Азкабана"))
)

(defrule rule3
(author (data "автор Джоан Ролинг"))
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Гарри Поттер и Кубок Огня")))
(assert (appendmessagehalt "автор Джоан Ролинг, жанр фэнтези, объем от 300 до 600 страниц => книга Гарри Поттер и Кубок Огня"))
)

(defrule rule4
(author (data "автор Джоан Ролинг"))
(genre (data "жанр фэнтези"))
(volume (data "объем от 600 страниц"))
=>
(assert (book (data "книга Гарри Поттер и Орден Феникса")))
(assert (appendmessagehalt "автор Джоан Ролинг, жанр фэнтези, объем от 600 страниц => книга Гарри Поттер и Орден Феникса"))
)

(defrule rule5
(author (data "автор Джоан Ролинг"))
(genre (data "жанр фэнтези"))
(volume (data "объем от 600 страниц"))
=>
(assert (book (data "книга Гарри Поттер и Принц-Полукровка")))
(assert (appendmessagehalt "автор Джоан Ролинг, жанр фэнтези, объем от 600 страниц => книга Гарри Поттер и Принц-Полукровка"))
)

(defrule rule6
(author (data "автор Джоан Ролинг"))
(genre (data "жанр фэнтези"))
(volume (data "объем от 600 страниц"))
=>
(assert (book (data "книга Гарри Поттер и Дары Смерти")))
(assert (appendmessagehalt "автор Джоан Ролинг, жанр фэнтези, объем от 600 страниц => книга Гарри Поттер и Дары Смерти"))
)

(defrule rule7
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
(author (data "автор Лев Толстой"))
=>
(assert (book (data "книга Анна Каренина")))
(assert (appendmessagehalt "объем от 600 страниц, жанр реализм, автор Лев Толстой => книга Анна Каренина"))
)

(defrule rule8
(genre (data "жанр исторический"))
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
(author (data "автор Лев Толстой"))
=>
(assert (book (data "книга Война и мир")))
(assert (appendmessagehalt "жанр исторический, объем от 600 страниц, жанр реализм, автор Лев Толстой => книга Война и мир"))
)

(defrule rule9
(author (data "автор Иван Тургенев"))
(genre (data "жанр реализм"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Отцы и дети")))
(assert (appendmessagehalt "автор Иван Тургенев, жанр реализм, объем от 300 до 600 страниц => книга Отцы и дети"))
)

(defrule rule10
(genre (data "жанр антиутопия"))
(volume (data "объем от 600 страниц"))
(author (data "автор Айн Рэнд"))
=>
(assert (book (data "книга Атлант расправил плечи")))
(assert (appendmessagehalt "жанр антиутопия, объем от 600 страниц, автор Айн Рэнд => книга Атлант расправил плечи"))
)

(defrule rule11
(author (data "автор Джек Лондон"))
(volume (data "объем от 300 до 600 страниц"))
(genre (data "жанр драма"))
=>
(assert (book (data "книга Мартин Иден")))
(assert (appendmessagehalt "автор Джек Лондон, объем от 300 до 600 страниц, жанр драма => книга Мартин Иден"))
)

(defrule rule12
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
(author (data "автор Теодор Драйзер"))
=>
(assert (book (data "книга Финансист")))
(assert (appendmessagehalt "объем от 600 страниц, жанр реализм, автор Теодор Драйзер => книга Финансист"))
)

(defrule rule13
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
(author (data "автор Теодор Драйзер"))
=>
(assert (book (data "книга Гений")))
(assert (appendmessagehalt "объем от 600 страниц, жанр реализм, автор Теодор Драйзер => книга Гений"))
)

(defrule rule14
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
(author (data "автор Теодор Драйзер"))
=>
(assert (book (data "книга Стоик")))
(assert (appendmessagehalt "объем от 600 страниц, жанр реализм, автор Теодор Драйзер => книга Стоик"))
)

(defrule rule15
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
(author (data "автор Теодор Драйзер"))
=>
(assert (book (data "книга Американская трагедия")))
(assert (appendmessagehalt "объем от 600 страниц, жанр реализм, автор Теодор Драйзер => книга Американская трагедия"))
)

(defrule rule16
(genre (data "жанр фэнтези"))
(author (data "автор Терри Пратчетт"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Санта-Хрякус")))
(assert (appendmessagehalt "жанр фэнтези, автор Терри Пратчетт, объем от 300 до 600 страниц => книга Санта-Хрякус"))
)

(defrule rule17
(genre (data "жанр реализм"))
(volume (data "объем от 300 до 600 страниц"))
(author (data "автор О.Генри"))
=>
(assert (book (data "книга Дары волхвов")))
(assert (appendmessagehalt "жанр реализм, объем от 300 до 600 страниц, автор О.Генри => книга Дары волхвов"))
)

(defrule rule18
(author (data "автор Чарльз Диккенс"))
(volume (data "объем от 100 до 300 страниц"))
(genre (data "жанр сказка"))
=>
(assert (book (data "книга Рождественская песнь")))
(assert (appendmessagehalt "автор Чарльз Диккенс, объем от 100 до 300 страниц, жанр сказка => книга Рождественская песнь"))
)

(defrule rule19
(genre (data "жанр антиутопия"))
(volume (data "объем от 100 до 300 страниц"))
(genre (data "жанр фантастика"))
(author (data "автор Энтони Бёрджесс"))
=>
(assert (book (data "книга Заводной апельсин")))
(assert (appendmessagehalt "жанр антиутопия, объем от 100 до 300 страниц, жанр фантастика, автор Энтони Бёрджесс => книга Заводной апельсин"))
)

(defrule rule20
(volume (data "объем от 100 до 300 страниц"))
(author (data "автор Евгений Замятин"))
(genre (data "жанр антиутопия"))
=>
(assert (book (data "книга Мы")))
(assert (appendmessagehalt "объем от 100 до 300 страниц, автор Евгений Замятин, жанр антиутопия => книга Мы"))
)

(defrule rule21
(genre (data "жанр фантастика"))
(volume (data "объем от 100 до 300 страниц"))
(genre (data "жанр антиутопия"))
(author (data "автор Рэй Брэдбери"))
=>
(assert (book (data "книга 451 градус по Фаренгейту")))
(assert (appendmessagehalt "жанр фантастика, объем от 100 до 300 страниц, жанр антиутопия, автор Рэй Брэдбери => книга 451 градус по Фаренгейту"))
)

(defrule rule22
(genre (data "жанр фантастика"))
(author (data "автор Олдос Хаксли"))
(genre (data "жанр антиутопия"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга О дивный новый мир")))
(assert (appendmessagehalt "жанр фантастика, автор Олдос Хаксли, жанр антиутопия, объем от 300 до 600 страниц => книга О дивный новый мир"))
)

(defrule rule23
(genre (data "жанр антиутопия"))
(author (data "автор Джордж Оруэлл"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Скотный двор")))
(assert (appendmessagehalt "жанр антиутопия, автор Джордж Оруэлл, объем от 300 до 600 страниц => книга Скотный двор"))
)

(defrule rule24
(genre (data "жанр антиутопия"))
(author (data "автор Джордж Оруэлл"))
(volume (data "объем от 300 до 600 страниц"))
(genre (data "жанр фантастика"))
=>
(assert (book (data "книга 1984")))
(assert (appendmessagehalt "жанр антиутопия, автор Джордж Оруэлл, объем от 300 до 600 страниц, жанр фантастика => книга 1984"))
)

(defrule rule25
(genre (data "жанр фэнтези"))
(author (data "автор Терри Пратчетт"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Цвет волшебства")))
(assert (appendmessagehalt "жанр фэнтези, автор Терри Пратчетт, объем от 300 до 600 страниц => книга Цвет волшебства"))
)

(defrule rule26
(genre (data "жанр фэнтези"))
(author (data "автор Терри Пратчетт"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Стража! Стража!")))
(assert (appendmessagehalt "жанр фэнтези, автор Терри Пратчетт, объем от 300 до 600 страниц => книга Стража! Стража!"))
)

(defrule rule27
(genre (data "жанр фэнтези"))
(author (data "автор Терри Пратчетт"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Вещие сестрички")))
(assert (appendmessagehalt "жанр фэнтези, автор Терри Пратчетт, объем от 300 до 600 страниц => книга Вещие сестрички"))
)

(defrule rule28
(volume (data "объем от 100 до 300 страниц"))
(genre (data "жанр фантастика"))
(author (data "автор Айзек Азимов"))
=>
(assert (book (data "книга Я робот")))
(assert (appendmessagehalt "объем от 100 до 300 страниц, жанр фантастика, автор Айзек Азимов => книга Я робот"))
)

(defrule rule29
(volume (data "объем от 100 до 300 страниц"))
(author (data "автор Дуглас Адамс"))
(genre (data "жанр фантастика"))
(genre (data "жанр юмор"))
=>
(assert (book (data "книга Автостопом по галактике")))
(assert (appendmessagehalt "объем от 100 до 300 страниц, автор Дуглас Адамс, жанр фантастика, жанр юмор => книга Автостопом по галактике"))
)

(defrule rule30
(genre (data "жанр детектив"))
(author (data "автор Артур Конан Дойл"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Рассказы о Шерлоке Холмсе")))
(assert (appendmessagehalt "жанр детектив, автор Артур Конан Дойл, объем от 300 до 600 страниц => книга Рассказы о Шерлоке Холмсе"))
)

(defrule rule31
(genre (data "жанр детектив"))
(author (data "автор Агата Кристи"))
(volume (data "объем от 100 до 300 страниц"))
=>
(assert (book (data "книга Убийство в «Восточном экспрессе»")))
(assert (appendmessagehalt "жанр детектив, автор Агата Кристи, объем от 100 до 300 страниц => книга Убийство в «Восточном экспрессе»"))
)

(defrule rule32
(genre (data "жанр детектив"))
(author (data "автор Агата Кристи"))
(volume (data "объем от 100 до 300 страниц"))
=>
(assert (book (data "книга Десять негритят")))
(assert (appendmessagehalt "жанр детектив, автор Агата Кристи, объем от 100 до 300 страниц => книга Десять негритят"))
)

(defrule rule33
(genre (data "жанр детектив"))
(author (data "автор Агата Кристи"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Убийство Роджера Экройда")))
(assert (appendmessagehalt "жанр детектив, автор Агата Кристи, объем от 300 до 600 страниц => книга Убийство Роджера Экройда"))
)

(defrule rule34
(volume (data "объем от 300 до 600 страниц"))
(genre (data "жанр приключения"))
(genre (data "жанр юмор"))
(author (data "авторы Илья Ильф и Евгений Петров"))
=>
(assert (book (data "книга Двенадцать стульев")))
(assert (appendmessagehalt "объем от 300 до 600 страниц, жанр приключения, жанр юмор, авторы Илья Ильф и Евгений Петров => книга Двенадцать стульев"))
)

(defrule rule35
(volume (data "объем от 100 до 300 страниц"))
(genre (data "жанр юмор"))
(author (data "автор Пелам Вудхаус"))
=>
(assert (book (data "книга Дживс и феодальная верность")))
(assert (appendmessagehalt "объем от 100 до 300 страниц, жанр юмор, автор Пелам Вудхаус => книга Дживс и феодальная верность"))
)

(defrule rule36
(volume (data "объем от 100 до 300 страниц"))
(author (data "автор Джером К. Джером"))
(genre (data "жанр юмор"))
=>
(assert (book (data "книга Трое в одной лодке, не считая собаки")))
(assert (appendmessagehalt "объем от 100 до 300 страниц, автор Джером К. Джером, жанр юмор => книга Трое в одной лодке, не считая собаки"))
)

(defrule rule37
(author (data "автор Иван Тургенев"))
(genre (data "жанр реализм"))
(volume (data "объем до 100 страниц"))
=>
(assert (book (data "книга Муму")))
(assert (appendmessagehalt "автор Иван Тургенев, жанр реализм, объем до 100 страниц => книга Муму"))
)

(defrule rule38
(author (data "автор Федор Достоевский"))
(volume (data "объем от 600 страниц"))
(genre (data "жанр реализм"))
=>
(assert (book (data "книга Преступление и наказание")))
(assert (appendmessagehalt "автор Федор Достоевский, объем от 600 страниц, жанр реализм => книга Преступление и наказание"))
)

(defrule rule39
(volume (data "объем от 300 до 600 страниц"))
(genre (data "жанр реализм"))
(author (data "автор Александр Пушкин"))
=>
(assert (book (data "книга Евгений Онегин")))
(assert (appendmessagehalt "объем от 300 до 600 страниц, жанр реализм, автор Александр Пушкин => книга Евгений Онегин"))
)

(defrule rule40
(genre (data "жанр реализм"))
(volume (data "объем от 300 до 600 страниц"))
(author (data "автор Михаил Лермонтов"))
=>
(assert (book (data "книга Герой нашего времени")))
(assert (appendmessagehalt "жанр реализм, объем от 300 до 600 страниц, автор Михаил Лермонтов => книга Герой нашего времени"))
)

(defrule rule41
(author (data "автор Николай Гоголь"))
(genre (data "жанр реализм"))
(volume (data "объем от 300 до 600 страниц"))
=>
(assert (book (data "книга Мертвые души")))
(assert (appendmessagehalt "автор Николай Гоголь, жанр реализм, объем от 300 до 600 страниц => книга Мертвые души"))
)

(defrule rule42
(volume (data "объем от 100 до 300 страниц"))
(author (data "автор Николай Гоголь"))
(genre (data "жанр юмор"))
=>
(assert (book (data "книга Ревизор")))
(assert (appendmessagehalt "объем от 100 до 300 страниц, автор Николай Гоголь, жанр юмор => книга Ревизор"))
)

(defrule rule43
(genre (data "жанр сказка"))
(volume (data "объем до 100 страниц"))
(author (data "автор Сергей Аксаков"))
=>
(assert (book (data "книга Аленький цветочек")))
(assert (appendmessagehalt "жанр сказка, объем до 100 страниц, автор Сергей Аксаков => книга Аленький цветочек"))
)

(defrule rule44
(author (data "автор Ганс Христиан Андерсен"))
(volume (data "объем до 100 страниц"))
(genre (data "жанр сказка"))
=>
(assert (book (data "книга Снежная королева")))
(assert (appendmessagehalt "автор Ганс Христиан Андерсен, объем до 100 страниц, жанр сказка => книга Снежная королева"))
)

(defrule rule45
(author (data "автор Ганс Христиан Андерсен"))
(volume (data "объем до 100 страниц"))
(genre (data "жанр сказка"))
=>
(assert (book (data "книга Дюймовочка")))
(assert (appendmessagehalt "автор Ганс Христиан Андерсен, объем до 100 страниц, жанр сказка => книга Дюймовочка"))
)

(defrule rule46
(genre (data "жанр фэнтези"))
(volume (data "объем от 600 страниц"))
(author (data "автор Джон Р. Р. Толкин"))
=>
(assert (book (data "книга Властелин колец")))
(assert (appendmessagehalt "жанр фэнтези, объем от 600 страниц, автор Джон Р. Р. Толкин => книга Властелин колец"))
)

(defrule rule47
(genre (data "жанр фэнтези"))
(volume (data "объем от 300 до 600 страниц"))
(author (data "автор Джон Р. Р. Толкин"))
=>
(assert (book (data "книга Хоббит, или Туда и обратно")))
(assert (appendmessagehalt "жанр фэнтези, объем от 300 до 600 страниц, автор Джон Р. Р. Толкин => книга Хоббит, или Туда и обратно"))
)

(defrule rule48
(duration (data "на вечер"))
=>
(assert (volume (data "объем до 100 страниц")))
(assert (appendmessagehalt "на вечер => объем до 100 страниц"))
)

(defrule rule49
(duration (data "на пару-тройку дней"))
=>
(assert (volume (data "объем от 300 до 600 страниц")))
(assert (appendmessagehalt "на пару-тройку дней => объем от 300 до 600 страниц"))
)

(defrule rule50
(duration (data "на много дней"))
=>
(assert (volume (data "объем от 600 страниц")))
(assert (appendmessagehalt "на много дней => объем от 600 страниц"))
)

(defrule rule51
(duration (data "на вечер"))
=>
(assert (volume (data "объем от 100 до 300 страниц")))
(assert (appendmessagehalt "на вечер => объем от 100 до 300 страниц"))
)

(defrule rule52
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Джоан Ролинг")))
(assert (appendmessagehalt "язык оригинала английский => автор Джоан Ролинг"))
)

(defrule rule53
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Терри Пратчетт")))
(assert (appendmessagehalt "язык оригинала английский => автор Терри Пратчетт"))
)

(defrule rule54
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Айзек Азимов")))
(assert (appendmessagehalt "язык оригинала английский => автор Айзек Азимов"))
)

(defrule rule55
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Теодор Драйзер")))
(assert (appendmessagehalt "язык оригинала английский => автор Теодор Драйзер"))
)

(defrule rule56
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Айн Рэнд")))
(assert (appendmessagehalt "язык оригинала английский => автор Айн Рэнд"))
)

(defrule rule57
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Джек Лондон")))
(assert (appendmessagehalt "язык оригинала английский => автор Джек Лондон"))
)

(defrule rule58
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Дуглас Адамс")))
(assert (appendmessagehalt "язык оригинала английский => автор Дуглас Адамс"))
)

(defrule rule59
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Джордж Оруэлл")))
(assert (appendmessagehalt "язык оригинала английский => автор Джордж Оруэлл"))
)

(defrule rule60
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Рэй Брэдбери")))
(assert (appendmessagehalt "язык оригинала английский => автор Рэй Брэдбери"))
)

(defrule rule61
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Энтони Бёрджесс")))
(assert (appendmessagehalt "язык оригинала английский => автор Энтони Бёрджесс"))
)

(defrule rule62
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Чарльз Диккенс")))
(assert (appendmessagehalt "язык оригинала английский => автор Чарльз Диккенс"))
)

(defrule rule63
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор О.Генри")))
(assert (appendmessagehalt "язык оригинала английский => автор О.Генри"))
)

(defrule rule64
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Олдос Хаксли")))
(assert (appendmessagehalt "язык оригинала английский => автор Олдос Хаксли"))
)

(defrule rule65
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Артур Конан Дойл")))
(assert (appendmessagehalt "язык оригинала английский => автор Артур Конан Дойл"))
)

(defrule rule66
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Агата Кристи")))
(assert (appendmessagehalt "язык оригинала английский => автор Агата Кристи"))
)

(defrule rule67
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Пелам Вудхаус")))
(assert (appendmessagehalt "язык оригинала английский => автор Пелам Вудхаус"))
)

(defrule rule68
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Джером К. Джером")))
(assert (appendmessagehalt "язык оригинала английский => автор Джером К. Джером"))
)

(defrule rule69
(language (data "язык оригинала английский"))
=>
(assert (author (data "автор Джон Р. Р. Толкин")))
(assert (appendmessagehalt "язык оригинала английский => автор Джон Р. Р. Толкин"))
)

(defrule rule70
(language (data "язык оригинала датский"))
=>
(assert (author (data "автор Ганс Христиан Андерсен")))
(assert (appendmessagehalt "язык оригинала датский => автор Ганс Христиан Андерсен"))
)

(defrule rule71
(language (data "язык оригинала русский"))
=>
(assert (author (data "автор Лев Толстой")))
(assert (appendmessagehalt "язык оригинала русский => автор Лев Толстой"))
)

(defrule rule72
(language (data "язык оригинала русский"))
=>
(assert (author (data "автор Иван Тургенев")))
(assert (appendmessagehalt "язык оригинала русский => автор Иван Тургенев"))
)

(defrule rule73
(language (data "язык оригинала русский"))
=>
(assert (author (data "автор Евгений Замятин")))
(assert (appendmessagehalt "язык оригинала русский => автор Евгений Замятин"))
)

(defrule rule74
(language (data "язык оригинала русский"))
=>
(assert (author (data "авторы Илья Ильф и Евгений Петров")))
(assert (appendmessagehalt "язык оригинала русский => авторы Илья Ильф и Евгений Петров"))
)

(defrule rule75
(language (data "язык оригинала русский"))
=>
(assert (author (data "автор Федор Достоевский")))
(assert (appendmessagehalt "язык оригинала русский => автор Федор Достоевский"))
)

(defrule rule76
(language (data "язык оригинала русский"))
=>
(assert (author (data "автор Александр Пушкин")))
(assert (appendmessagehalt "язык оригинала русский => автор Александр Пушкин"))
)

(defrule rule77
(language (data "язык оригинала русский"))
=>
(assert (author (data "автор Михаил Лермонтов")))
(assert (appendmessagehalt "язык оригинала русский => автор Михаил Лермонтов"))
)

(defrule rule78
(language (data "язык оригинала русский"))
=>
(assert (author (data "автор Николай Гоголь")))
(assert (appendmessagehalt "язык оригинала русский => автор Николай Гоголь"))
)

(defrule rule79
(language (data "язык оригинала русский"))
=>
(assert (author (data "автор Сергей Аксаков")))
(assert (appendmessagehalt "язык оригинала русский => автор Сергей Аксаков"))
)

(defrule rule80
(age (data "подходит для ребенка"))
=>
(assert (volume (data "объем до 100 страниц")))
(assert (appendmessagehalt "подходит для ребенка => объем до 100 страниц"))
)

(defrule rule81
(age (data "подходит для ребенка"))
=>
(assert (genre (data "жанр сказка")))
(assert (appendmessagehalt "подходит для ребенка => жанр сказка"))
)

(defrule rule82
(age (data "подходит для ребенка"))
=>
(assert (genre (data "жанр приключения")))
(assert (appendmessagehalt "подходит для ребенка => жанр приключения"))
)

(defrule rule83
(age (data "подходит для ребенка"))
=>
(assert (genre (data "жанр фэнтези")))
(assert (appendmessagehalt "подходит для ребенка => жанр фэнтези"))
)

(defrule rule84
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр юмор")))
(assert (appendmessagehalt "подходит для взрослого => жанр юмор"))
)

(defrule rule85
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр фэнтези")))
(assert (appendmessagehalt "подходит для взрослого => жанр фэнтези"))
)

(defrule rule86
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр приключения")))
(assert (appendmessagehalt "подходит для взрослого => жанр приключения"))
)

(defrule rule87
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр антиутопия")))
(assert (appendmessagehalt "подходит для взрослого => жанр антиутопия"))
)

(defrule rule88
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр реализм")))
(assert (appendmessagehalt "подходит для взрослого => жанр реализм"))
)

(defrule rule89
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр исторический")))
(assert (appendmessagehalt "подходит для взрослого => жанр исторический"))
)

(defrule rule90
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр драма")))
(assert (appendmessagehalt "подходит для взрослого => жанр драма"))
)

(defrule rule91
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр фантастика")))
(assert (appendmessagehalt "подходит для взрослого => жанр фантастика"))
)

(defrule rule92
(age (data "подходит для взрослого"))
=>
(assert (genre (data "жанр детектив")))
(assert (appendmessagehalt "подходит для взрослого => жанр детектив"))
)

(defrule rule93
(school (data "входит в школьную программу"))
=>
(assert (author (data "автор Лев Толстой")))
(assert (appendmessagehalt "входит в школьную программу => автор Лев Толстой"))
)

(defrule rule94
(school (data "входит в школьную программу"))
=>
(assert (author (data "автор Иван Тургенев")))
(assert (appendmessagehalt "входит в школьную программу => автор Иван Тургенев"))
)

(defrule rule95
(school (data "входит в школьную программу"))
=>
(assert (author (data "автор Федор Достоевский")))
(assert (appendmessagehalt "входит в школьную программу => автор Федор Достоевский"))
)

(defrule rule96
(school (data "входит в школьную программу"))
=>
(assert (author (data "автор Александр Пушкин")))
(assert (appendmessagehalt "входит в школьную программу => автор Александр Пушкин"))
)

(defrule rule97
(school (data "входит в школьную программу"))
=>
(assert (author (data "автор Михаил Лермонтов")))
(assert (appendmessagehalt "входит в школьную программу => автор Михаил Лермонтов"))
)

(defrule rule98
(school (data "входит в школьную программу"))
=>
(assert (author (data "автор Николай Гоголь")))
(assert (appendmessagehalt "входит в школьную программу => автор Николай Гоголь"))
)

(defrule rule99
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Джоан Ролинг")))
(assert (appendmessagehalt "не входит в школьную программу => автор Джоан Ролинг"))
)

(defrule rule100
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Терри Пратчетт")))
(assert (appendmessagehalt "не входит в школьную программу => автор Терри Пратчетт"))
)

(defrule rule101
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Айзек Азимов")))
(assert (appendmessagehalt "не входит в школьную программу => автор Айзек Азимов"))
)

(defrule rule102
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Теодор Драйзер")))
(assert (appendmessagehalt "не входит в школьную программу => автор Теодор Драйзер"))
)

(defrule rule103
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Айн Рэнд")))
(assert (appendmessagehalt "не входит в школьную программу => автор Айн Рэнд"))
)

(defrule rule104
(age (data "подходит для ребенка"))
=>
(assert (volume (data "объем от 100 до 300 страниц")))
(assert (appendmessagehalt "подходит для ребенка => объем от 100 до 300 страниц"))
)

(defrule rule105
(age (data "подходит для взрослого"))
=>
(assert (volume (data "объем от 100 до 300 страниц")))
(assert (appendmessagehalt "подходит для взрослого => объем от 100 до 300 страниц"))
)

(defrule rule106
(age (data "подходит для взрослого"))
=>
(assert (volume (data "объем от 300 до 600 страниц")))
(assert (appendmessagehalt "подходит для взрослого => объем от 300 до 600 страниц"))
)

(defrule rule107
(age (data "подходит для взрослого"))
=>
(assert (volume (data "объем от 600 страниц")))
(assert (appendmessagehalt "подходит для взрослого => объем от 600 страниц"))
)

(defrule rule108
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Айн Рэнд")))
(assert (appendmessagehalt "не входит в школьную программу => автор Айн Рэнд"))
)

(defrule rule109
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Джек Лондон")))
(assert (appendmessagehalt "не входит в школьную программу => автор Джек Лондон"))
)

(defrule rule110
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Дуглас Адамс")))
(assert (appendmessagehalt "не входит в школьную программу => автор Дуглас Адамс"))
)

(defrule rule111
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Джордж Оруэлл")))
(assert (appendmessagehalt "не входит в школьную программу => автор Джордж Оруэлл"))
)

(defrule rule112
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Рэй Брэдбери")))
(assert (appendmessagehalt "не входит в школьную программу => автор Рэй Брэдбери"))
)

(defrule rule113
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Энтони Бёрджесс")))
(assert (appendmessagehalt "не входит в школьную программу => автор Энтони Бёрджесс"))
)

(defrule rule114
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Чарльз Диккенс")))
(assert (appendmessagehalt "не входит в школьную программу => автор Чарльз Диккенс"))
)

(defrule rule115
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор О.Генри")))
(assert (appendmessagehalt "не входит в школьную программу => автор О.Генри"))
)

(defrule rule116
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Олдос Хаксли")))
(assert (appendmessagehalt "не входит в школьную программу => автор Олдос Хаксли"))
)

(defrule rule117
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Евгений Замятин")))
(assert (appendmessagehalt "не входит в школьную программу => автор Евгений Замятин"))
)

(defrule rule118
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Артур Конан Дойл")))
(assert (appendmessagehalt "не входит в школьную программу => автор Артур Конан Дойл"))
)

(defrule rule119
(school (data "не входит в школьную программу"))
=>
(assert (author (data "авторы Илья Ильф и Евгений Петров")))
(assert (appendmessagehalt "не входит в школьную программу => авторы Илья Ильф и Евгений Петров"))
)

(defrule rule120
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Пелам Вудхаус")))
(assert (appendmessagehalt "не входит в школьную программу => автор Пелам Вудхаус"))
)

(defrule rule121
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Джером К. Джером")))
(assert (appendmessagehalt "не входит в школьную программу => автор Джером К. Джером"))
)

(defrule rule122
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Федор Достоевский")))
(assert (appendmessagehalt "не входит в школьную программу => автор Федор Достоевский"))
)

(defrule rule123
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Сергей Аксаков")))
(assert (appendmessagehalt "не входит в школьную программу => автор Сергей Аксаков"))
)

(defrule rule124
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Ганс Христиан Андерсен")))
(assert (appendmessagehalt "не входит в школьную программу => автор Ганс Христиан Андерсен"))
)

(defrule rule125
(school (data "не входит в школьную программу"))
=>
(assert (author (data "автор Джон Р. Р. Толкин")))
(assert (appendmessagehalt "не входит в школьную программу => автор Джон Р. Р. Толкин"))
)

(defrule rule126
(plot (data "в тексте есть восстание"))
=>
(assert (genre (data "жанр антиутопия")))
(assert (appendmessagehalt "в тексте есть восстание => жанр антиутопия"))
)

(defrule rule127
(plot (data "в тексте есть магия"))
=>
(assert (genre (data "жанр фэнтези")))
(assert (appendmessagehalt "в тексте есть магия => жанр фэнтези"))
)

(defrule rule128
(plot (data "в тексте есть расслоение общества"))
=>
(assert (genre (data "жанр антиутопия")))
(assert (appendmessagehalt "в тексте есть расслоение общества => жанр антиутопия"))
)

(defrule rule129
(plot (data "в тексте есть расслоение общества"))
=>
(assert (genre (data "жанр реализм")))
(assert (appendmessagehalt "в тексте есть расслоение общества => жанр реализм"))
)

(defrule rule130
(plot (data "в тексте есть расслоение общества"))
=>
(assert (genre (data "жанр драма")))
(assert (appendmessagehalt "в тексте есть расслоение общества => жанр драма"))
)

(defrule rule131
(plot (data "в тексте есть предательство"))
=>
(assert (genre (data "жанр драма")))
(assert (appendmessagehalt "в тексте есть предательство => жанр драма"))
)

(defrule rule132
(plot (data "в тексте есть предательство"))
=>
(assert (genre (data "жанр реализм")))
(assert (appendmessagehalt "в тексте есть предательство => жанр реализм"))
)

(defrule rule133
(plot (data "в тексте есть убийство"))
=>
(assert (genre (data "жанр детектив")))
(assert (appendmessagehalt "в тексте есть убийство => жанр детектив"))
)

(defrule rule134
(plot (data "в тексте есть убийство"))
=>
(assert (genre (data "жанр исторический")))
(assert (appendmessagehalt "в тексте есть убийство => жанр исторический"))
)

(defrule rule135
(plot (data "в тексте есть убийство"))
=>
(assert (genre (data "жанр реализм")))
(assert (appendmessagehalt "в тексте есть убийство => жанр реализм"))
)

(defrule rule136
(plot (data "в тексте есть убийство"))
=>
(assert (genre (data "жанр драма")))
(assert (appendmessagehalt "в тексте есть убийство => жанр драма"))
)

(defrule rule137
(plot (data "в тексте есть роботы"))
=>
(assert (genre (data "жанр фантастика")))
(assert (appendmessagehalt "в тексте есть роботы => жанр фантастика"))
)

(defrule rule138
(plot (data "в тексте есть животные"))
=>
(assert (genre (data "жанр реализм")))
(assert (appendmessagehalt "в тексте есть животные => жанр реализм"))
)

(defrule rule139
(plot (data "в тексте есть животные"))
=>
(assert (genre (data "жанр фэнтези")))
(assert (appendmessagehalt "в тексте есть животные => жанр фэнтези"))
)

(defrule rule140
(plot (data "в тексте есть животные"))
=>
(assert (genre (data "жанр сказка")))
(assert (appendmessagehalt "в тексте есть животные => жанр сказка"))
)

(defrule rule141
(mood (data "для хорошего настроения"))
=>
(assert (genre (data "жанр фэнтези")))
(assert (appendmessagehalt "для хорошего настроения => жанр фэнтези"))
)

(defrule rule142
(mood (data "для хорошего настроения"))
=>
(assert (genre (data "жанр юмор")))
(assert (appendmessagehalt "для хорошего настроения => жанр юмор"))
)

(defrule rule143
(mood (data "для хорошего настроения"))
=>
(assert (genre (data "жанр приключения")))
(assert (appendmessagehalt "для хорошего настроения => жанр приключения"))
)

(defrule rule144
(mood (data "для хорошего настроения"))
=>
(assert (genre (data "жанр сказка")))
(assert (appendmessagehalt "для хорошего настроения => жанр сказка"))
)

(defrule rule145
(mood (data "для отвратительного настроения"))
=>
(assert (genre (data "жанр исторический")))
(assert (appendmessagehalt "для отвратительного настроения => жанр исторический"))
)

(defrule rule146
(mood (data "для отвратительного настроения"))
=>
(assert (genre (data "жанр драма")))
(assert (appendmessagehalt "для отвратительного настроения => жанр драма"))
)

(defrule rule147
(mood (data "для новогоднего настроения"))
=>
(assert (genre (data "жанр сказка")))
(assert (appendmessagehalt "для новогоднего настроения => жанр сказка"))
)

(defrule rule148
(mood (data "для новогоднего настроения"))
=>
(assert (genre (data "жанр фэнтези")))
(assert (appendmessagehalt "для новогоднего настроения => жанр фэнтези"))
)

(defrule rule149
(mood (data "для настроения подумать"))
=>
(assert (genre (data "жанр реализм")))
(assert (appendmessagehalt "для настроения подумать => жанр реализм"))
)

(defrule rule150
(mood (data "для настроения подумать"))
=>
(assert (genre (data "жанр антиутопия")))
(assert (appendmessagehalt "для настроения подумать => жанр антиутопия"))
)

(defrule rule151
(mood (data "для настроения подумать"))
=>
(assert (genre (data "жанр драма")))
(assert (appendmessagehalt "для настроения подумать => жанр драма"))
)

(defrule rule152
(mood (data "для того, чтобы погрустить"))
=>
(assert (genre (data "жанр драма")))
(assert (appendmessagehalt "для того, чтобы погрустить => жанр драма"))
)

(defrule rule153
(mood (data "для того, чтобы погрустить"))
=>
(assert (genre (data "жанр реализм")))
(assert (appendmessagehalt "для того, чтобы погрустить => жанр реализм"))
)

(defrule rule154
(mood (data "для того, чтобы погрустить"))
=>
(assert (genre (data "жанр антиутопия")))
(assert (appendmessagehalt "для того, чтобы погрустить => жанр антиутопия"))
)

(defrule rule155
(mood (data "для настроения подумать"))
=>
(assert (genre (data "жанр драма")))
(assert (appendmessagehalt "для настроения подумать => жанр драма"))
)

(defrule rule156
(mood (data "для хорошего настроения"))
=>
(assert (genre (data "жанр фантастика")))
(assert (appendmessagehalt "для хорошего настроения => жанр фантастика"))
)

(defrule rule157
(mood (data "для того, чтобы погрустить"))
=>
(assert (genre (data "жанр исторический")))
(assert (appendmessagehalt "для того, чтобы погрустить => жанр исторический"))
)

(defrule rule158
(mood (data "для того, чтобы уснуть"))
=>
(assert (genre (data "жанр исторический")))
(assert (appendmessagehalt "для того, чтобы уснуть => жанр исторический"))
)

(defrule rule159
(mood (data "для того, чтобы уснуть"))
=>
(assert (genre (data "жанр реализм")))
(assert (appendmessagehalt "для того, чтобы уснуть => жанр реализм"))
)

(defrule rule160
(mood (data "для настроения подумать"))
=>
(assert (genre (data "жанр детектив")))
(assert (appendmessagehalt "для настроения подумать => жанр детектив"))
)

(defrule rule161
(mood (data "для того, чтобы уснуть"))
=>
(assert (volume (data "объем от 600 страниц")))
(assert (appendmessagehalt "для того, чтобы уснуть => объем от 600 страниц"))
)

(defrule rule162
(mood (data "для того, чтобы расслабиться"))
=>
(assert (genre (data "жанр фэнтези")))
(assert (appendmessagehalt "для того, чтобы расслабиться => жанр фэнтези"))
)

(defrule rule163
(mood (data "для того, чтобы расслабиться"))
=>
(assert (genre (data "жанр приключения")))
(assert (appendmessagehalt "для того, чтобы расслабиться => жанр приключения"))
)

(defrule rule164
(mood (data "для того, чтобы расслабиться"))
=>
(assert (genre (data "жанр сказка")))
(assert (appendmessagehalt "для того, чтобы расслабиться => жанр сказка"))
)

(defrule rule165
(mood (data "для того, чтобы расслабиться"))
=>
(assert (genre (data "жанр фантастика")))
(assert (appendmessagehalt "для того, чтобы расслабиться => жанр фантастика"))
)

(defrule rule166
(mood (data "для того, чтобы расслабиться"))
=>
(assert (volume (data "объем до 100 страниц")))
(assert (appendmessagehalt "для того, чтобы расслабиться => объем до 100 страниц"))
)

(defrule rule167
(mood (data "для того, чтобы расслабиться"))
=>
(assert (volume (data "объем от 100 до 300 страниц")))
(assert (appendmessagehalt "для того, чтобы расслабиться => объем от 100 до 300 страниц"))
)

