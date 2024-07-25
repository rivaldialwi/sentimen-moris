import pandas as pd
import streamlit as st
import nltk
import matplotlib.pyplot as plt
import plotly.express as px
from replace_words import replace_words_negatif, replace_words_netral, replace_words_positif
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from collections import Counter
from create_pdf import create_pdf

# Fungsi untuk mengunduh resource NLTK secara senyap
def download_nltk_resources():
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

# Panggil fungsi unduh NLTK resource di awal
download_nltk_resources()

# Fungsi untuk mengganti atau menghapus kata-kata tertentu dalam teks
def replace_and_remove_words(text, replace_words):
    words = text.split()
    replaced_words = [replace_words.get(word, word) for word in words]
    return " ".join(replaced_words)

# Fungsi untuk membuat word cloud
def create_word_cloud(text, title):
    wordcloud = WordCloud(width=300, height=200, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title)
    st.pyplot(fig)

# Fungsi untuk membersihkan teks
def clean_text(text, replace_words):
    stop_words = set(stopwords.words('indonesian'))
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    text = text.lower()  # Case folding
    words = word_tokenize(text)  # Tokenizing
    cleaned_words = [word for word in words if word not in stop_words]  # Stopword removal
    stemmed_words = [stemmer.stem(word) for word in cleaned_words]  # Stemming
    replaced_text = replace_and_remove_words(" ".join(stemmed_words), replace_words)  # Replace and remove words
    return replaced_text

# Fungsi untuk menghitung kemunculan kata-kata tertentu
def count_specific_words(text, words_to_count):
    word_list = text.split()
    word_counts = Counter(word_list)
    specific_word_counts = {word: word_counts[word] for word in words_to_count}
    sorted_word_counts = dict(sorted(specific_word_counts.items(), key=lambda item: item[1], reverse=True))
    return sorted_word_counts

# Fungsi untuk menjalankan Website
def run():
    st.title("Website Analisis Sentimen Moris Indonesia")

    st.header("Unggah file untuk Grafik dan Word Cloud Sentimen")
    uploaded_excel = st.file_uploader("Unggah file Excel", type=["xlsx"], key="file_uploader_analysis")

    if uploaded_excel is not None:
        # Baca file Excel
        df_excel = pd.read_excel(uploaded_excel)
        
        # Periksa apakah kolom 'Human' ada di file yang diunggah
        if 'Human' in df_excel.columns:
            # Periksa apakah kolom 'Human' kosong
            if df_excel['Human'].isnull().all():
                st.error("Kolom 'Human' tidak boleh kosong.")
            else:
                # Hitung kemunculan setiap sentimen
                sentiment_counts = df_excel['Human'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']
                
                # Buat diagram batang menggunakan Plotly
                color_discrete_map = {
                    'Negatif': 'red',
                    'Netral': 'gray',
                    'Positif': 'green'
                }

                fig = px.bar(sentiment_counts, x='Sentiment', y='Count', color='Sentiment',
                             labels={'Sentiment': 'Sentimen', 'Count': 'Jumlah'},
                             title='Distribusi Sentimen',
                             text='Count',
                             color_discrete_map=color_discrete_map)
                
                fig.update_traces(texttemplate='%{text}', textposition='outside')
                fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                
                st.plotly_chart(fig)
                
                # Kata-kata yang ingin dihitung kemunculannya
                words_to_count = ["metropolis", "freedom", "vintage", "advent", "creative", "independent", "woody", "aquatic", "oud", "amber"]

                all_sentiments_text_cleaned = ""

                # Hasilkan kata untuk setiap sentimen
                sentiments = df_excel['Human'].unique()
                for sentiment in sentiments:
                    sentiment_text = " ".join(df_excel[df_excel['Human'] == sentiment]['Text'])
                    
                    # Pilih daftar kata yang akan diganti atau dihapus berdasarkan sentimen
                    if sentiment == 'Negatif':
                        replace_words = replace_words_negatif
                    elif sentiment == 'Netral':
                        replace_words = replace_words_netral
                    elif sentiment == 'Positif':
                        replace_words = replace_words_positif
                    else:
                        replace_words = {}

                    sentiment_text_cleaned = clean_text(sentiment_text, replace_words)
                    all_sentiments_text_cleaned += " " + sentiment_text_cleaned
                    create_word_cloud(sentiment_text_cleaned, f'Word Cloud untuk Sentimen {sentiment}')
                
                # Hitung kemunculan kata-kata tertentu dari semua teks yang telah dibersihkan
                word_counts = count_specific_words(all_sentiments_text_cleaned, words_to_count)
                word_counts_df = pd.DataFrame(word_counts.items(), columns=['Kata', 'Jumlah'])
                
                st.subheader("Produk Terpopuler")
                st.dataframe(word_counts_df)

                # Tombol untuk mengunduh tabel sebagai PDF
                pdf_data = create_pdf(word_counts_df)
                st.download_button(
                    label="Unduh PDF",
                    data=pdf_data,
                    file_name="Produk Terpopuler.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("File harus memiliki kolom 'Human'.")

if __name__ == "__main__":
    run()