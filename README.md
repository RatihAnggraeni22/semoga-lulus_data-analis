# Submission Belajar Analisis Data dengan Python

## Deskripsi

Menganalisis data pada Bike Sharing Dataset dengan tujuan untuk memahami berapa banyak dan sedikit penyewaan sepeda didasarkan pada waktu dan musim.

## Struktur Direktori

- **/data**: Direktori ini berisi data csv yang digunakan .
- **/dashboard**: Direktori ini berisi dashboard.py yang digunakan untuk menampilkan informasi hasil analisis data.
- **notebook.ipynb**: File ini yang digunakan untuk melakukan analisis data.
- **requirements.txt**: Berisi informasi terkait library apa saja yang digunakan.
- **url.txt**: Public link url dashboard

## Setup Anaconda
```shell
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter
```

## Setup Project
```shell
mkdir proyek_analisis_data
cd proyek_analisis_data
jupyter-notebook .
```

## Setup Dahboard 
```shell
pip install streamlit
```

## Run steamlit app
```shell
streamlit run dashboard.py
```