import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import heapq
# Функция суммаризации текста


def summarize_text(text, num_sentences=None):
    # Токенизация текста на предложения
    sentences = sent_tokenize(text, language=language)
    # Токенизация текста на слова и удаление стоп-слов
    words = word_tokenize(text.lower(), language=language)
    stop_words = set(stopwords.words(language))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    # Подсчет частоты слов
    word_freq = defaultdict(int)
    for word in words:
        word_freq[word] += 1
    # Определение значимости каждого предложения
    sentence_scores = defaultdict(int)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower(), language=language):
            if word in word_freq:
                sentence_scores[i] += word_freq[word]
    # Выбор предложений для суммаризации
    if num_sentences:
        best_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
        best_sentences = sorted(best_sentences)
        summary = ' '.join([sentences[i] for i in best_sentences])
        return summary
# Основная функция Streamlit


def main():
    st.title("Приложение для сжатия текста с AI-ассистентом")
    st.write("Введите текст, выберите уровень сжатия и получите результат!")
    # Поле ввода текста
    user_text = st.text_area("Введите текст для сжатия:")
    # Выбор уровня сжатия
    compression_level = st.selectbox("Выберите уровень сжатия:", ["Сильное сжатие", "Слабое сжатие"])
    num_sentences = None
    if compression_level == "Сильное сжатие":
        num_sentences = 2
    elif compression_level == "Слабое сжатие":
        num_sentences = 5
    # Кнопка для выполнения сжатия
    if st.button("Сжать текст"):
        if user_text:
            st.subheader("Результат сжатия:")
            st.write(summarize_text(user_text, num_sentences))
        else:
            st.warning("Пожалуйста, введите текст для сжатия.")


if __name__ == "__main__":
    language = 'russian'
    nltk.download('punkt_tab')
    nltk.download('punkt')
    nltk.download('stopwords')
    main()
