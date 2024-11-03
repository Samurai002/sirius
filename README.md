# Документация по работе с прототипом

**Описание функционала прототипа**:
> Приложение для чтения книг в формате PDF-файлов с использованием AI-помощника, способным:
> + Сокращать текст (Пользователь может регулировать силу сжатия)
> + Генерировать тесты по тексту

**Инструкция по запуску прототипа**: <br>
> Для работы программы вам необходимо установить Python версии от 3.8 и выше. <br>
> (Во избежания ошибок **ОБЯЗАТЕЛЬНО** при установке Python включить чекбокс “Добавить в PATH”)

> Необходимо скачать все файлы с github репозитория -->  Скопировать путь до директории, в которую были скачаны файлы --> Ввести в консоль (Win+R, далее cmd) команды: <br>
> 1. cd [скопированный путь до папки] <br>
> 2. pip install -r requirements.txt <br>
> 3. streamlit run prototype.py <br>

> Вас перекинет в браузер где и будет открыто приложение. <br>

***Примечание***: <br>
> Надпись "RUNNING" справа сверху означает выполнения функций приложения.  
> Если вы её видите, никакие кнопки не нажимать, дабы избежать поломок программы!

**Описание методов, используемых при разработке**: <br>
> Сокращение текста в прототипе реализовано с помощью абстрактивного подхода суммаризации текста. Для этогоо используется нейросетевая модель ChatGPT 3.5 Turbo, доступ к которой получен из библиотеки g4f (GPT for Free). Модель не подгружается на компьютер пользоваля, <br>
> что позволяет избавиться от нужны занимать место на диске при установке модели. Так же это обеспечивает независимость от характеристик устройства пользователя, ведь для локальной работы Большой Языковой Модели нужны большие мощности железа. <br>
>
> Для генерации тестов так же используется эта же нейросетевая модель, ведь на данный момент достойных аналогов такого подхода не существует.
>
> Графический интерфейс создан с помощью библиотеки StreamLit. В ней есть почти все нужные для реализации проекта инструменты, а освоение функционала проходит буквально за 20 минут. К сожалению, только к финальным дням разработки выяснилось, что некоторые полезные для <br>
> проекта вещи просто невозможно реализовать с помощью этой библиотеки, по этому в будущем планируется перейти на PyQT6. <br>
> **Её приемущества**:
>   + Низкий порог входа
>   + Большой простор для стилизации благодаря адаптации CSS стилей под систему QT - QSS
>   + Возможность создать красивое, удобное и быстрое графическое окружение

Краткий видео-гайд по установке и использованию прототипа вы можете найти <a href="https://drive.google.com/file/d/1R6ceU-7Zk7B0Y932so0tQcQdqH-VrR1h/view?usp=sharing">тут</a>
