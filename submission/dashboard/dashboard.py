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

#Membaca dataset yang sudah diolah
# Baca data dari file CSV
product_df = pd.read_csv("https://raw.githubusercontent.com/AbigailMetanoia/proyek_akhir/main/submission/data/order_items_dataset.csv")
category_translation_df = pd.read_csv("https://raw.githubusercontent.com/AbigailMetanoia/proyek_akhir/main/submission/data/product_category_name_translation.csv")
orders_df = pd.read_csv("https://raw.githubusercontent.com/AbigailMetanoia/proyek_akhir/main/submission/data/order_items_dataset.csv")
order_reviews_df = pd.read_csv("https://raw.githubusercontent.com/AbigailMetanoia/proyek_akhir/main/submission/data/order_reviews_dataset.csv")

# Gabungkan product_df dengan category_translation_df agar mengetahui nama masing-masing product
merged_product_df = pd.merge(left=product_df,
                            right=category_translation_df,
                            how="inner",
                            left_on="product_category_name",
                            right_on="product_category_name")

# Gabungkan dengan tabel produk dengan order agar mengatuhi produk mana yang di order konsumen
final_df = pd.merge(left=merged_product_df,
                    right=orders_df,
                    how="inner",
                    left_on="product_id",
                    right_on="product_id")

# Gabungkan kembali tabel dengan order review, agar mengetahui review masing-masing produk yang dipesan
df = pd.merge(left=final_df,
                    right=order_reviews_df,
                    how="inner",
                    left_on="order_id",
                    right_on="order_id")

#Bersihkan data
for column in df.columns:
    if df[column].dtype == 'object':
        df[column].fillna(0, inplace=True)  # Mengisi dengan 0 untuk kolom non-numerik
    else:
        df[column].fillna(df[column].mean(), inplace=True)

#Isi Dashboard meliputi menampilkan grafik hasil analisis data.

#Visualisasi 1
st.header('Grafik Jumlah Produk yang Dibeli')
st.subheader(
    """
    \"Kategori produk apa yang paling diminati oleh konsumen?\"
    """
)

# Kode Grafik Jumlah Produk yang Dibeli
product_counts = df.groupby('product_category_name_english').size().reset_index(name='product_count')

top_5_categories = product_counts.nlargest(5, 'product_count')

# Palet warna yang berbeda untuk setiap bar
colors = sns.color_palette('husl', n_colors=len(top_5_categories))

# Visualisasikan data
fig, ax = plt.subplots(figsize=(15, 6))
bars = ax.bar(x=top_5_categories['product_category_name_english'], height=top_5_categories['product_count'], color=colors)


# Tampilkan grafik menggunakan Streamlit
st.pyplot(fig)


#Tabel Rangking Jumlah Produk Tertinggi
top_5_products = product_counts.nlargest(5, 'product_count')
top_5_products['Ranking'] = range(1, 6)
top_5_products = top_5_products.reset_index(drop=True)

top_5_products.columns = ['Nama Kategori Produk', 'Jumlah Produk yang Dibeli', 'Rangking']
# Tampilkan tabel 
st.table(top_5_products)

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
    \"Apakah kategori produk yang sering diminati konsumen memiliki review yang baik?\"
    """
)

# Kode Grafik Rata-rata Nilai Review untuk Setiap Produk
# Hitung rata-rata nilai review untuk setiap produk
avg_review = df.groupby('product_category_name_english')['review_score'].mean().reset_index()

# Visualisasikan data
# Ambil 5 kategori produk teratas
top_5_categories = avg_review.nlargest(5, 'review_score')

# Ambil data untuk kategori produk "bed_bath_table"
bed_bath_table_category = avg_review[avg_review['product_category_name_english'] == 'bed_bath_table']

# Gabungkan data 5 kategori teratas dengan data "bed_bath_table"
categories_to_plot = pd.concat([top_5_categories, bed_bath_table_category])

# Urutkan kembali data berdasarkan nilai review
categories_to_plot = categories_to_plot.sort_values(by='review_score', ascending=False)

# Visualisasikan data
fig, ax = plt.subplots(figsize=(15, 8))
bars = ax.bar(x=categories_to_plot['product_category_name_english'], height=categories_to_plot['review_score'])

# Berikan warna yang berbeda untuk setiap kategori
colors = ['blue', 'green', 'gray', 'purple', 'orange'] + ['red'] 
for bar, color in zip(bars, colors):
    bar.set_color(color)

ax.set_xlabel('Nama Kategori Produk')
ax.set_ylabel('Rata-rata Review')
ax.set_title('Review dari 5 Kategori Produk Teratas')

# Tampilkan grafik menggunakan Streamlit
st.pyplot(fig)

# Penjelasan kategori review
penjelasan_review = """
Asumsi Kategori Rata-Rata Review:
- Sangat Baik: Nilai rata-rata review antara 4 - 5. 
- Baik: Nilai rata-rata review antara 3 - 4.
- Buruk: Nilai rata-rata review antara 2 - 3.
- Sangat Buruk: Nilai rata-rata review antara 0 - 2.
"""

# Tampilkan penjelasan kategori review di Streamlit
st.subheader(penjelasan_review)

#Tabel Rangking Rata-rata Review terbaik
categories_to_plot.reset_index(drop=True, inplace=True)
categories_to_plot = categories_to_plot.sort_values(by='review_score', ascending=False)
categories_to_plot['Ranking'] = range(1, len(categories_to_plot) + 1)
categories_to_plot['Kategori Review'] = pd.cut(categories_to_plot['review_score'], bins=[0, 2.5, 3.5, 4.5, 5], labels=['Sangat Buruk', 'Buruk', 'Baik', 'Sangat Baik'], right=False)
st.table(categories_to_plot)

#Kesimpulan
st.subheader(
    """
    Kesimpulan yang bisa diambil adalah kategori yang paling diminati konsumen yakni \"bed_bath_table\" memiliki review yang \"BAIK\" dari konsumen.
    """
)
