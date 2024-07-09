import pandas as pd
import streamlit as st
import nltk
import matplotlib.pyplot as plt
import plotly.express as px
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from collections import Counter

# Fungsi untuk mengunduh resource NLTK secara senyap
def download_nltk_resources():
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)

# Panggil fungsi unduh NLTK resource di awal
download_nltk_resources()

# Daftar kata yang akan diganti atau dihapus
replace_words_negatif = {
    "yang": "",
    "nya": "",
    "kok": "",
    "sih": "",
    "romantic": "",
    "aja": "",
    "love": "",
    "toko": "",
    "doang": "",
    "midnight": "",
    "minggu": "",
    "kak": "",
    "beli": "",
    "puas": "",
    "enak": "",
    "pas": "",
    "suka": "",
    "pure": "",
    "jakarta": "",
    "kalo": "",
    "jam": "",
    "wangi": "",
    "puluh": "",
    "tiup": "",
    "langgan": "",
    "kena": "",
    "layan": "",
    "kemaren": "",
    "sesuai": "",
    "putih": "",
    "parfum": "",
    "tahan": "",
    "jalan": "",
    "angin": "",
    "cepat": "",
    "cepet": "",
    "kaya": "",
    "aroma": "",
    "tinggal": "",
    "buka": "",
    "sudah": "",
    "sampe": "",
    "barang": "",
    "menit": "",
    "express": "",
    "percaya": "",
    "make": "",
    "ekspektasi": "",
    "banget": "",
    "harga": "",
    "pake": "",
    "woody": "",
    "kotak": "",
    "moris": "",
    "jasa": "",
    "alfamart": "",
    "belanja": "",
    "kuat": "",
    "botol": "",
    "ongkos": "",
    "estimasi": "",
    "kaos": "",
    "leher": "",
    "pakai": "",
    "tutup": "",
    "delapan": "",
    "modal": "",
    "layak": "",
    "murah": "",
    "bijak": "",
    "iklan": "",
    "box": "",
    "kardus": "",
    "kembali": "",
    "harum": "",
    "metropolis": "",
    "kepala": "",
    "kualitas": "",
    "pesan": "",
    "semprot": "",
    "kirim": "",
    "massa": "",
    "hubung": "",
    "rumah": "",
    "nyata": "",
    "mudah": "",
    "sangat": "",
    "worth": "",
    "sengat": "",
    "baju": "",
    "ka": "",
    "ga": "tidak",
    "gak": "tidak",
    "tidakk": "tidak",
    "udah": "sudah",
    "cewe": "cewek",
    "cew": "cewek",
    "cowo": "cowok",
    "cow": "cowok",
}

replace_words_netral = {
    "ruang": "",
    "campur": "",
    "best": "",
    "ibu": "",
    "ga": "",
    "gak": "",
    "nya": "",
    "kalo": "",
    "ka": "",
    "kak": "",
    "bau": "",
    "borong": "",
    "bener": "",
    "yah": "",
}


replace_words_positif = {
    "harga": "",
    "ka": "",
    "kak": "",
    "biar": "",
    "segitu": "",
    "kelas": "",
    "estimasi": "",
    "pakai": "",
    "baju": "",
    "se": "",
    "nya": "",
    "emang": "",
    "biru": "",
    "pusing": "",
    "bismillah": "",
    "udah": "",
    "kepala": "",
    "tajam": "",
    "kirim": "",
    "sekolah": "",
    "belah": "",
    "anak": "",
    "bikin": "",
    "botol": "",
    "jodoh": "",
    "motif": "",
    "parfum": "",
    "beli": "",
    "varian": "",
    "breeze": "",
    "gak": "",
    "ocean": "",
    "keluarga": "",
    "metropolis": "",
    "woody": "",
    "morris": "",
    "pas": "",
    "orang": "",
    "langsung": "",
    "deh": "",
    "pake": "",
    "sih": "",
    "jalan": "",
    "pokok": "",
    "moris": "",
    "sesal": "",
    "sumpah": "",
    "artis": "",
    "asa": "",
    "asik": "",
}


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
                create_word_cloud(sentiment_text_cleaned, f'Word Cloud untuk Sentimen {sentiment}')
        else:
            st.error("File harus memiliki kolom 'Human'.")

if __name__ == "__main__":
    run()