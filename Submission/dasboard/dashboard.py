#Library---------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
#----------------------------------------------------------
day_df = pd.read_csv("main_data.csv") 
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

st.header('Bike Sharing Dashboard')

#Pertanyaan 1----------------------------------------------
st.subheader('Jumlah sewa sepeda dalam 1 tahun')
col1, col2 = st.columns(2)
 
with col1:
    total_user = main_df.registered.sum()
    st.metric("Jumlah Registered User", value=total_user)
 
with col2:
    total_user = main_df.casual.sum()
    st.metric("Jumlah Casual User", value=total_user)

mnth_name = {
    1: 'Januari',
    2: 'Februari',
    3: 'Maret',
    4: 'April',
    5: 'Mei',
    6: 'Juni',
    7: 'Juli',
    8: 'Agustus',
    9: 'September',
    10: 'Oktober',
    11: 'November',
    12: 'Desember'
}
day_df['mnth_name'] = day_df['mnth'].map(mnth_name)

registered_df = day_df.groupby(by="mnth_name").registered.sum().reset_index()
registered_df.rename(columns={"registered": "user_count"}, inplace=True)
registered_df['user_type'] = 'Registered'

casual_df = day_df.groupby(by="mnth_name").casual.sum().reset_index()
casual_df.rename(columns={"casual": "user_count"}, inplace=True)
casual_df['user_type'] = 'Casual'

ordered_months = [
    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
]
registered_df['mnth_name'] = pd.Categorical(registered_df['mnth_name'], categories=ordered_months, ordered=True)
casual_df['mnth_name'] = pd.Categorical(casual_df['mnth_name'], categories=ordered_months, ordered=True)

registered_df = registered_df.sort_values('mnth_name')
casual_df = casual_df.sort_values('mnth_name')
#Visualisasi 1---------------------------------------------
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 6))
sns.barplot(
    y="user_count",
    x="mnth_name",
    data=registered_df,
    color="blue", 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Registered User by Month", loc="center", fontsize=18)
ax[0].tick_params(axis='x', labelsize=12, rotation=45)

sns.barplot(
    y="user_count",
    x="mnth_name",
    data=casual_df,
    color="orange", 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Casual User by Month", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=12, rotation=45)
st.pyplot(fig)
#Visualisasi 2------------------------------------------------------------
combined_df = pd.concat([registered_df, casual_df])
combined_df['mnth_name'] = pd.Categorical(combined_df['mnth_name'], categories=ordered_months, ordered=True)
combined_df = combined_df.sort_values('mnth_name')

st.subheader("Perbandingan Jumlah Registered User dan Casual User Berdasarkan Bulan")

plt.figure(figsize=(15, 6))
sns.barplot(
    x="mnth_name",
    y="user_count",
    hue="user_type",
    data=combined_df,
    palette='bright' 
)
plt.title("Perbandingan Jumlah Registered User dan Casual User berdasarkan Bulan", loc="center", fontsize=15)
plt.ylabel("Jumlah User")
plt.xlabel("Bulan")
plt.tick_params(axis='x', labelsize=12)
plt.legend(title="Tipe User")
st.pyplot(plt)
#Pertanyaan 2------------------------------------------------
agg_df = day_df.groupby(by="mnth").agg({
    "temp": ["min", "max", "mean"],
    "hum": ["min", "max", "mean"],
    "windspeed": ["min", "max", "mean"]
})

agg_df.columns = ['Temp Min', 'Temp Max', 'Temp Mean', 'Hum Min', 'Hum Max', 'Hum Mean', 'Wind Speed Min', 'Wind Speed Max', 'Wind Speed Mean']
agg_df.reset_index(inplace=True)

agg_df['mnth_name'] = agg_df['mnth'].map(mnth_name)
agg_df['mnth_name'] = pd.Categorical(agg_df['mnth_name'], categories=ordered_months, ordered=True)
agg_df = agg_df.sort_values('mnth_name')

st.subheader("Persebaran suhu, kelembapan dan windspeed dalam 1 tahun")


plt.figure(figsize=(14, 8))

plt.subplot(3, 1, 1)
sns.barplot(x='mnth_name', y='Temp Mean', data=agg_df, color='blue', label='Suhu Rata-rata')
plt.title('Suhu Rata-rata per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Suhu (°C)')
plt.xticks(rotation=45)
plt.legend()

plt.subplot(3, 1, 2)
sns.barplot(x='mnth_name', y='Hum Mean', data=agg_df, color='green', label='Kelembapan Rata-rata')
plt.title('Kelembapan Rata-rata per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Kelembapan (%)')
plt.xticks(rotation=45)
plt.legend()

plt.subplot(3, 1, 3)
sns.barplot(x='mnth_name', y='Wind Speed Mean', data=agg_df, color='orange', label='Kecepatan Angin Rata-rata')
plt.title('Kecepatan Angin Rata-rata per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Kecepatan Angin (m/s)')
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
st.pyplot(plt)
#Pertanyaan 3-----------------------------------------------
st.subheader("Hubungan Cuaca dan Jumlah Penyewa Sepeda dalam tiap musim")

season_name = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}
day_df['season_name'] = day_df['season'].map(season_name)
weather_season_df = day_df.groupby(by=["season_name", "weathersit"]).cnt.sum().reset_index()

ordered_season = [
    'Spring', 'Summer', 'Fall', 'Winter']
weather_season_df['season_name'] = pd.Categorical(weather_season_df['season_name'], categories=ordered_season, ordered=True)
weather_season_df = weather_season_df.sort_values('season_name')

plt.figure(figsize=(20, 8))
sns.barplot(
    x="season_name",
    y="cnt",
    hue="weathersit",
    data=weather_season_df,
    palette="bright", 
    order=ordered_season  
)
plt.title("Hubungan antara Cuaca dan Jumlah Penyewa Sepeda berdasarkan Musim", fontsize=16)
plt.xlabel("Musim", fontsize=14)
plt.ylabel("Jumlah Penyewa Sepeda", fontsize=14)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.legend(title="Kategori Cuaca") 
plt.tight_layout() 
st.pyplot(plt)

st.caption('Copyright (c) Wahyu 2025')