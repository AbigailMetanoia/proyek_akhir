import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Judul Dashboard
st.title('Analisis E-Commerce Public Dataset ')
st.subheader('Oleh Abigail Metanoia Melody')
st.write(
    """
    - **Nama:** Abigail Metanoia Melody
    - **Email:** abigailmetanoia17@gmail.com
    - **ID Dicoding:** m200d4kx3142
    """
)


#Isi Dashboard meliputi menampilkan grafik hasil analisis data.

#Visualisasi 1
st.header('Grafik Jumlah Produk yang Dibeli')
st.subheader(
    """
    Visualisasi data berikut akan menjawab pertanyaan bisnis yang ditentukan yakni \"Kategori produk apa yang paling diminati oleh konsumen?\"
    """
)
#Membaca dataset yang sudah diolah
df = pd.read_csv("main_data.csv")

# Kode Grafik Jumlah Produk yang Dibeli
product_counts = df.groupby('product_category_name_english').size().reset_index(name='product_count')

# Ambil 5 kategori produk teratas
top_5_categories = product_counts.nlargest(5, 'product_count')

# Palet warna yang berbeda untuk setiap bar
colors = sns.color_palette('husl', n_colors=len(top_5_categories))

# Visualisasikan data
fig, ax = plt.subplots(figsize=(15, 6))
bars = ax.bar(x=top_5_categories['product_category_name_english'], height=top_5_categories['product_count'], color=colors)


# Tampilkan grafik menggunakan Streamlit
st.pyplot(fig)

#Tabel Rangking
product_counts.columns = ['Rangking','Nama Kategori Produk', 'Jumlah Produk yang Dibeli']

# Urutkan data berdasarkan jumlah produk yang dibeli dalam urutan menurun
product_counts = product_counts.sort_values(by='Jumlah Produk yang Dibeli', ascending=False)

product_counts['Ranking'] = range(1, len(product_counts) + 1)
product_counts = product_counts[['Ranking', 'Nama Kategori Produk', 'Jumlah Produk yang Dibeli']]

# Tampilkan tabel 
st.table(product_counts)

#Kesimpulan
st.subheader(
    """
    Kesimpulan yang bisa diambil adalah kategori yang paling diminati konsumen adalah **bed_bath_table**.
    """
)

#Visualisasi 2
st.header('Grafik Rata-rata Nilai Review untuk Setiap Produk')
st.subheader(
    """
    Visualisasi data berikut akan menjawab pertanyaan bisnis yang ditentukan yakni \"Apakah kategori produk yang sering diminati konsumen memiliki review yang baik?\"
    """
)

# Kode Grafik Rata-rata Nilai Review untuk Setiap Produk
# Hitung rata-rata nilai review untuk setiap produk
avg_review = df.groupby('product_category_name_english')['review_score'].mean().reset_index()

# Visualisasikan data
# Ambil 5 kategori produk teratas
top_5_categories = avg_review.nlargest(5, 'review_score')

# Visualisasikan data
fig, ax = plt.subplots(figsize=(15, 8))
bars = ax.bar(x=top_5_categories['product_category_name_english'], height=top_5_categories['review_score'])

# Berikan warna yang berbeda untuk setiap kategori
colors = ['blue', 'green', 'red', 'purple', 'orange']
for bar, color in zip(bars, colors):
    bar.set_color(color)

plt.xticks(rotation=90)
ax.set_xlabel('Nama Kategori Produk')
ax.set_ylabel('Rata-rata Review')
ax.set_title('Review dari 5 Kategori Produk Teratas')

# Tampilkan grafik menggunakan Streamlit
st.pyplot(fig)


#Tabel 
avg_review.columns = ['Nama Kategori Produk', 'Rata-rata Review']

# Urutkan data berdasarkan rata-rata review dalam urutan menurun
avg_review = avg_review.sort_values(by='Rata-rata Review', ascending=False)

# Ambil 5 top kategori produk teratas
top_5_avg_review = avg_review.head(5)

# Tambahkan kolom rangking
top_5_avg_review['Ranking'] = range(1, len(top_5_avg_review) + 1)

# Tambahkan kolom kategori rata-rata review
top_5_avg_review['Kategori Rata-rata Review'] = pd.cut(top_5_avg_review['Rata-rata Review'], bins=[0, 2, 3, 4, 5], labels=['Sangat Buruk', 'Buruk', 'Baik', 'Sangat Baik'], right=False)

#Kesimpulan
st.subheader(
    """
    Kesimpulan yang bisa diambil adalah kategori yang paling diminati konsumen yakni **bed_bath_table** memiliki **review yang baik** dari konsumen.
    """
)
