import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import os

st.set_page_config(page_title="Bike Sharing Insight", page_icon="🚲", layout="wide")

sns.set_theme(style='ticks')

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "hour.csv")
    df = pd.read_csv(csv_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    df['weather_label'] = df['weathersit'].map({
        1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan', 4: 'Hujan Lebat'
    })
    df['day_type'] = df['workingday'].map({
        0: 'Hari Libur/Weekend', 1: 'Hari Kerja'
    })
    df['temp_category'] = pd.cut(df['temp'], bins=[0, 0.3, 0.6, 1.0], labels=['Dingin', 'Sedang', 'Panas'])
    return df

df = load_data()

with st.sidebar:
    st.title("🚲 Bike Control")
    
    min_date, max_date = df["dteday"].min(), df["dteday"].max()
    date_range = st.date_input("Rentang Waktu:", min_value=min_date, max_value=max_date, value=[min_date, max_date])
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.stop()

    weather_filter = st.multiselect("Kondisi Cuaca:", options=df['weather_label'].unique(), default=df['weather_label'].unique())

main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date)) & (df['weather_label'].isin(weather_filter))]

st.title('🚲 Bike Sharing Analysis Dashboard')
st.markdown(f"Periode Analisis: **{start_date}** s/d **{end_date}**")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rental", f"{main_df.cnt.sum():,}")
with col2:
    st.metric("Registered", f"{main_df.registered.sum():,}", delta=f"{int(main_df.registered.sum()/main_df.cnt.sum()*100)}%")
with col3:
    st.metric("Casual", f"{main_df.casual.sum():,}")

st.markdown("---")

tab1, tab2 = st.tabs(["Tren Perilaku", "Kondisi Lingkungan"])

with tab1:
    st.subheader("Kasual vs Terdaftar (Rata-rata)")
    user_behavior_df = main_df.groupby('day_type', observed=True)[['casual', 'registered']].mean().reset_index()
    labels = user_behavior_df['day_type']
    x = np.arange(len(labels))
    width = 0.35

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    rects1 = ax1.bar(x - width/2, user_behavior_df['casual'], width, label='Kasual', color='#FF8A65')
    rects2 = ax1.bar(x + width/2, user_behavior_df['registered'], width, label='Terdaftar', color='#0097A7')
    ax1.set_ylabel('Rata-rata Rental')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend()
    st.pyplot(fig1)

    st.subheader("Distribusi Jam: Kerja vs Libur")
    hourly_behavior = main_df.groupby(['day_type', 'hr'], observed=True)[['casual', 'registered']].mean().reset_index()
    
    fig2, axes2 = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
    for i, dtype in enumerate(['Hari Kerja', 'Hari Libur/Weekend']):
        data = hourly_behavior[hourly_behavior['day_type'] == dtype]
        axes2[i].plot(data['hr'], data['casual'], label='Kasual', color='#FF8A65', linewidth=2, marker='o')
        axes2[i].plot(data['hr'], data['registered'], label='Terdaftar', color='#0097A7', linewidth=2, marker='o')
        axes2[i].set_title(dtype)
        axes2[i].set_xlabel("Jam")
        axes2[i].legend()
    st.pyplot(fig2)

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Pengaruh Cuaca")
        weather_df = main_df.groupby("weather_label", observed=True)["cnt"].mean().sort_values(ascending=False)
        fig3, ax3 = plt.subplots()
        weather_df.plot(kind="bar", color='#B2CEFE', ax=ax3)
        ax3.set_ylabel("Rata-rata")
        st.pyplot(fig3)

    with col_b:
        st.subheader("Pengaruh Suhu")
        temp_df = main_df.groupby('temp_category', observed=True)['cnt'].mean().reset_index()
        fig4, ax4 = plt.subplots()
        sns.barplot(x='cnt', y='temp_category', data=temp_df, palette='coolwarm', ax=ax4)
        ax4.set_xlabel("Rata-rata Rental")
        st.pyplot(fig4)

st.markdown("---")
st.caption('Copyright © 2026 - Data Analysis Project by Salsabil Salwa Putri Maharani')
