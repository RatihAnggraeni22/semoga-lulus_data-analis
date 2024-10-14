import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.ticker import FuncFormatter

# Mengatur gaya seaborn
sns.set(style='dark')

# Memuat data
day_df = pd.read_csv('dashboard/day_clean.csv')
hours_df = pd.read_csv('dashboard/hour_clean.csv')

# Mengonversi kolom tanggal menjadi datetime
for df in [day_df, hours_df]:
    df['dteday'] = pd.to_datetime(df['dteday'])

# Pemilihan Tanggal di Sidebar
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Menyaring DataFrame berdasarkan tanggal yang dipilih
main_df_day = day_df.query(f'dteday >= "{start_date}" and dteday <= "{end_date}"')
main_df_hour = hours_df.query(f'dteday >= "{start_date}" and dteday <= "{end_date}"')

# Agregasi Data
hour_count_df = main_df_hour.groupby("hours").agg({"count_cr": "sum"}).reset_index()
day_df_count_2011 = main_df_day.query('dteday >= "2011-01-01" and dteday <= "2012-12-31"')
reg_df = main_df_day.groupby("dteday").agg({"registered": "sum"}).reset_index().rename(columns={"registered": "register_sum"})
cas_df = main_df_day.groupby("dteday").agg({"casual": "sum"}).reset_index().rename(columns={"casual": "casual_sum"})
sum_order_items_df = hour_count_df.sort_values(by="hours", ascending=False).reset_index()
season_df = main_df_hour.groupby("season").count_cr.sum().reset_index()

# Visualisasi Dashboard
st.header('Bike Sharing')
st.subheader('Daily Sharing')

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    formatted_orders = f"{total_orders:,}".replace(",", ".")
    st.metric("Total Sharing Bike", value=formatted_orders)

st.subheader("Pada jam berapa jumlah penyewaan sepeda tertinggi terjadi, dan di jam berapa jumlah penyewaan sepeda paling rendah dalam satu hari?")

# Plot untuk penyewaan sepeda berdasarkan jam
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Penyewaan terbanyak
sns.barplot()

from matplotlib.ticker import FuncFormatter

# Misalkan day_df adalah DataFrame yang sudah ada
# Mengatur warna yang berbeda
colors = ["#FF5733", "#FFC300", "#33FF57", "#C70039", "#900C3F"]  # Warna yang bervariasi

# Membuat subplot dengan ukuran (20, 10)
fig, ax = plt.subplots(figsize=(20, 10))

# Menghitung jumlah penyewaan per musim
top_seasons = (
    day_df.groupby(by="season", observed=True)["count_cr"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .head(10)
)

# Buat barplot untuk y="count" dan x="season"
sns.barplot(
    x="season",
    y="count_cr",
    data=top_seasons,  # Menggunakan data yang sudah diolah
    ax=ax,
    palette=colors,
    hue="season",  # Menetapkan hue ke "season" untuk menghindari peringatan
    dodge=True,   # Memisahkan bar berdasarkan musim
    legend=False   # Menghilangkan legend
)

# Mengatur format sumbu y untuk menampilkan angka dalam ribu dan juta
def format_func(value, tick_number):
    if value >= 1_000_000:
        return f'{value / 1_000_000:.1f} juta'
    elif value >= 1_000:
        return f'{value / 1_000:.0f} ribu'
    else:
        return int(value)

ax.yaxis.set_major_formatter(FuncFormatter(format_func))

# Mengatur judul, label y dan x, serta tick params untuk subplot tersebut
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Musim", loc="center", fontsize=50)
ax.set_ylabel("Jumlah Penyewaan", fontsize=30)
ax.set_xlabel("Musim", fontsize=30)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

st.pyplot(fig)


st.subheader("Pada jam berapa jumlah penyewaan sepeda tertinggi terjadi, dan di jam berapa jumlah penyewaan sepeda paling rendah dalam satu hari?")

# Grouping berdasarkan jam dan menghitung jumlah penyewaan
sum_order_items_df = hours_df.groupby("hours")["count_cr"].sum().sort_values(ascending=False).reset_index()
# Membuat bar chart untuk melihat perbedaan penyewaan sepeda berdasarkan jam
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Membuat barplot untuk penyewa sepeda terbanyak 
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), 
            hue="hours", palette=["#FF6F61", "#FFC300", "#FF6F61", "#BFBFBF", "#FF6F61"], 
            ax=ax[0], legend=False)

# Mengatur label dan judul untuk subplot pertama
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan jumlah penyewaan terbanyak", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Membuat barplot untuk penyewa sepeda terdikit 
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="count_cr", ascending=True).head(5), 
            hue="hours", palette=["#FFC300", "#BFBFBF", "#BFBFBF", "#FF6F61", "#FFC300"], 
            ax=ax[1], legend=False)

# Mengatur label dan judul untuk subplot kedua
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)", fontsize=30)
ax[1].set_title("Jam dengan jumlah penyewaan paling sedikit", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)