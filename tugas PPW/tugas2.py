# Import library yang diperlukan
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load data dari file CSV
file_path = 'berita_kompas.csv'  # Pastikan Anda mengganti path ini dengan lokasi file Anda
df = pd.read_csv(file_path)

# Periksa beberapa baris pertama untuk memastikan data sudah benar
print(df.head())

# Asumsikan bahwa kolom 'isi' adalah kolom yang akan digunakan
# Pastikan bahwa kolom ini ada dalam dataset
if 'isi' in df.columns:
    documents = df['isi'].fillna('').tolist()  # Mengambil teks dari kolom 'isi' dan mengatasi missing values
    
    # Inisialisasi TfidfVectorizer
    vectorizer = TfidfVectorizer()
    
    # Menghitung TF-IDF
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Mendapatkan fitur (kata-kata unik dari seluruh dokumen)
    feature_names = vectorizer.get_feature_names_out()
    
    # Menampilkan hasil TF-IDF dalam bentuk matriks
    tfidf_matrix_array = tfidf_matrix.toarray()
    
    # Menampilkan hasil
    print("Fitur (Kata-kata unik):")
    print(feature_names)
    
    print("\nMatriks TF-IDF:")
    print(tfidf_matrix_array)
    
    # Jika ingin tampilkan dalam bentuk data frame
    df_tfidf = pd.DataFrame(tfidf_matrix_array, columns=feature_names)
    print("\nMatriks TF-IDF dalam bentuk DataFrame:")
    print(df_tfidf)
    
    # Simpan hasil TF-IDF ke dalam file CSV
    output_file = 'tfidf_output.csv'  # Nama file output
    df_tfidf.to_csv(output_file, index=False)
    print(f"Hasil TF-IDF telah disimpan ke dalam file: {output_file}")
    
else:
    print("Kolom 'isi' tidak ditemukan dalam dataset.")
