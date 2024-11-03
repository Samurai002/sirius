import streamlit as st
import io
import PyPDF2
from PyPDF2 import PdfWriter
from g4f.client import Client

# Две функции сокращения текста: сильно и слабо


def summarization_strong(text):
    # Инициализация клиента
    client = Client()
    # Создание запроса для модели
    prompt = "Перескажи текст на русском языке, не пиши свое мнение, пиши только то что происходило в тексте, " \
             "используя не менее 300 слов: "
    # Вызов клиента
    response = client.chat.completions.create(
        # Вызов модели
        model="gpt-3.5-turbo",
        # Обращение к модели
        messages=[{"role": "user", "content": prompt + text}],
    )
    # Возвращение результата
    return response.choices[0].message.content


def summarization_little(text):
    # Инициализация клиента
    client = Client()
    # Создание запроса для модели
    prompt = "Перескажи текст на русском языке, не пиши свое мнение, пиши только то что происходило в тексте, " \
             "используя не менее 100 слов и не более 250 слов: "
    # Вызов клиента
    response = client.chat.completions.create(
        # Вызов модели
        model="gpt-3.5-turbo",
        # Обращение к модели
        messages=[{"role": "user", "content": prompt + text}],
    )
    # Возвращение результата
    return response.choices[0].message.content

# Функции создания тестов и ответов для них


def tests(text):
    # Инициализация клиента
    client = Client()
    # Создание запроса для модели
    prompt = "Представь что ты учитель, и задаешь своим ученикам вопросы по прочитанному тексту. " \
             "Нужно придумать 5 вопросов по этому тексту, кроме этих вопросов ничего больше не пиши в ответе: "
    # Вызов клиента
    response = client.chat.completions.create(
        # Вызов модели
        model="gpt-3.5-turbo",
        # Обращение к модели
        messages=[{"role": "user",
                   "content": prompt + text}],
    )
    # Возвращение результата
    return response.choices[0].message.content


def otvet(text, questions):
    # Инициализация клиента
    client = Client()
    # Вызов клиента
    response = client.chat.completions.create(
        # Вызов модели
        model="gpt-3.5-turbo",
        # Обращение к модели
        messages=[{"role": "user", "content": f"{questions} в тексте: {text}"}],
    )
    # Возвращение результата
    return response.choices[0].message.content

# Главная функция программы


def main():
    # Инициализация состояния сессии
    global pdf_reader, book_text
    if 'uploaded_books' not in st.session_state:
        st.session_state.uploaded_books = []
    # Инициализация списка загруженных книг, если он отсутствует в сессии
    if 'current_book' not in st.session_state:
        st.session_state.current_book = None
    # Инициализация выбранной книги значением None, если она отсутствует в сессии
    if 'page' not in st.session_state:
        st.session_state.page = 'main'
    # Инициализация страницы значением 'main', если она отсутствует в сессии
    if 'compression_level' not in st.session_state:
        st.session_state.compression_level = None
    # Инициализация уровня сжатия значением None, если он отсутствует в сессии
    # Главная страница
    if st.session_state.page == 'main':
        st.title("Прототип приложения для чтения книг")
        # Отображение заголовка на главной странице
        uploaded_file = st.file_uploader("Загрузите книгу", type=["pdf"])
        # Отображение элемента для загрузки книги в формате PDF

        if uploaded_file is not None:
            # Если файл был загружен пользователем
            if uploaded_file not in st.session_state.uploaded_books:
                # Проверка, что файл еще не был добавлен в список книг
                st.session_state.uploaded_books.append(uploaded_file)
            # Добавление файла в список загруженных книг в состоянии сессии
            st.success(f"Книга '{uploaded_file.name}' успешно загружена!")
    # Уведомление пользователя об успешной загрузке книги

    st.sidebar.button("Главная", on_click=lambda: st.session_state.update({'page': 'main'}))
    # Кнопка на боковой панели для перехода на главную страницу
    st.sidebar.button("Мой профиль", on_click=lambda: st.session_state.update({'page': 'profile'}))
    # Кнопка на боковой панели для перехода в профиль
    st.sidebar.button("Мои книги", on_click=lambda: st.session_state.update({'page': 'books'}))
    # Кнопка на боковой панели для перехода в список загруженный книг
    st.sidebar.button("Тестирование", on_click=lambda: st.session_state.update({'page': 'testing'}),
                      key='sidebar_testing_button')
    # Кнопка на боковой панели для перехода в раздел тестирования

    if st.session_state.page == 'books':
        # Страница "Мои книги"
        st.header("Мои книги")  # Отображение заголовка на текущей странице
        unique_books = list({book.name: book for book in st.session_state.uploaded_books}.values())
        for idx, book in enumerate(unique_books):
            # Проход по всем книгам для отображения кнопок с названиями книг
            if st.button(book.name, key=f"book_{idx}"):
                # Если кнопка с книгой, уст. книгу и перех. на страницу чтения
                st.session_state.current_book = book
                st.session_state.page = 'read'  # Переход на страницу чтения

    if st.session_state.page == 'read':
        if st.session_state.current_book is not None:
            # Проверка, если текущая книга не равна None
            st.header(st.session_state.current_book.name)
            # Отображение заголовка с названием текущей книги
            try:
                pdf_reader = PyPDF2.PdfReader(st.session_state.current_book)
                # Создание объекта для чтения PDF, выбранного в качестве книги
                book_text = ""
                # Инициализация пустой строки для хранения текста книги
                for page in pdf_reader.pages:
                    # Проход по всем страницам книги и извлечение текста
                    text = page.extract_text()
                    # Извлечение текста со страницы
                    if text:
                        # Если текст был извлечен, добавляем его в текст книги
                        book_text += text + ""
                st.text_area("Содержимое книги", value=book_text, height=800, max_chars=None, disabled=True)
                # Отображение содержимого книги в текстовом поле для просмотра
            except Exception as e:
                st.error(f"Ошибка при чтении файла: {e}")

            col1, col2 = st.columns(2)
            # Создание двух колонок для элементов управления

            if 'compress_text_clicked' not in st.session_state:
                st.session_state.compress_text_clicked = False

            if col1.button("Сжатие текста", key='compress_text'):
                st.session_state.compress_text_clicked = True

            if st.session_state.compress_text_clicked:
                compression_level = col1.selectbox("Выберите степень сжатия", ["Сильное", "Слабое"],
                                                   key='compression_level')
                if compression_level == "Слабое":
                    pdf_writer = PdfWriter()
                    # Создание PdfWriter для записи PDF
                    for page in pdf_reader.pages:
                        # Проход по страницам книги и добавление их в новый PDF
                        pdf_writer.add_page(page)

                    pdf_buffer = io.BytesIO()
                    # Создание буфера для хранения нового PDF
                    pdf_writer.write(pdf_buffer)
                    pdf_buffer.seek(0)

                    st.text_area("AI-помощник:", value=summarization_strong(book_text), max_chars=None, disabled=True,
                                 height=400)
                elif compression_level == "Сильное":
                    # Если выбран уровень сжатия "Сильное"
                    st.text_area("AI-помощник:", value=summarization_little(book_text), max_chars=None, disabled=True,
                                 height=400)

            if col2.button("Тестирование по тексту", key='text_testing'):
                st.session_state.update({'page': 'testing'})

    if st.session_state.page == 'testing':
        # Страница тестирования
        st.header("Тестирование")
        # Отображение заголовка на текущей странице
        if st.session_state.current_book is not None:
            try:
                pdf_reader = PyPDF2.PdfReader(st.session_state.current_book)
                # Создание объекта для чтения PDF, выбранного в книге
                book_text = ""
                # Инициализация строки для хранения текста
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    # Извлечение текста со страницы
                    if text:
                        # Если текст был извлечен, добавляем его в текст книги
                        book_text += text + ""
            except Exception as e:
                st.error(f"Ошибка при чтении файла: {e}")

        if len(st.session_state.uploaded_books) > 0:
            # Проверка, если есть загруженные книги
            selected_book = st.selectbox("Выберите книгу для тестирования",
                                         [book.name for book in st.session_state.uploaded_books],
                                         key='unique_testing_book_select')
            testik = tests(book_text)
            # Генерация теста на основе книги с испол. функции tests()
            if selected_book:
                # Если книга выбрана, отображение теста в текстовом поле
                st.text_area("AI-помощник:", value=testik, max_chars=None, disabled=True, height=300)

                # Добавление кнопки для отображения поля с ответами
                if st.button("Показать ответы", key='show_answers'):
                    # Если нажата кнопка "Показать ответы", отображаем ответы
                    st.text_area("AI-помощник:", value=otvet(book_text, testik), max_chars=None,
                                 disabled=True, height=300)

    if st.session_state.page == 'profile':
        # Страница профиля пользователя
        st.header("Мой профиль")  # Отображение заголовка на текущей странице
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False

        if not st.session_state.authenticated:
            # Проверка, если пользователь не аутентифицирован
            col1, col2 = st.columns(2)
            # Создание двух колонок для кнопок "Вход" и "Регистрация"
            if col1.button("Вход", key='login_button'):
                # Если нажата "Вход" в колонке устанав. состояние  True
                st.session_state.authenticated = True
            if col2.button("Регистрация", key='register_button'):
                # Если нажата "Регистрация" во колонке устанав. состояние True
                st.session_state.authenticated = True
        else:
            st.write("Тут будет профиль после авторизации")


if __name__ == "__main__":
    global pdf_reader, book_text
    main()
