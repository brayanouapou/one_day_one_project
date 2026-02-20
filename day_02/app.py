import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta

# Configuration Pro
st.set_page_config(page_title="AI Fitness Analytics", layout="wide")

# --- MOTEUR DE CALCULS (DATA SCIENCE) ---
def process_data(df):
    if len(df) > 1:
        # Transformation temporelle pour le ML (nombre de jours depuis le début)
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        
        # Moyenne mobile sur 3 jours (Lissage)
        df['poids_smooth'] = df['poids'].rolling(window=3).mean()
        
        # Calcul du surplus calorique (base arbitraire de 2500 kcal pour ton gabarit de 1m97)
        df['surplus'] = df['calories'] - 2500
    return df

# --- CHARGEMENT ---
df = pd.read_csv("fitness_data.csv")
df['date'] = pd.to_datetime(df['date'], format='mixed')
df = process_data(df)

st.title("🚀 AI Fitness Analytics - Prise de Masse")

# --- SECTION 1 : SMART METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Poids Actuel", f"{df['poids'].iloc[-1]} kg", f"{round(df['poids'].iloc[-1] - df['poids'].iloc[-2], 2)} kg")
with col2:
    moy_cal = int(df['calories'].tail(7).mean())
    st.metric("Moyenne Cal (7j)", f"{moy_cal} kcal", delta=f"{moy_cal - 3500} vs cible")
with col3:
    gain_total = round(df['poids'].iloc[-1] - df['poids'].iloc[0], 2)
    st.metric("Gain Total", f"{gain_total} kg")
with col4:
    # Estimation de la masse grasse simplifiée ou autre indicateur
    st.metric("Statut", "En Masse" if moy_cal > 3000 else "Maintenance")

# --- SECTION 2 : VISUALISATION AVANCÉE ---
st.write("---")
tab1, tab2, tab3 = st.tabs(["📈 Analyse de Tendance", "🔗 Corrélations", "🔮 Prédiction IA"])

with tab1:
    # Graphique combinant Poids Réel et Poids Lissé
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['poids'], name="Poids Réel", mode='markers'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['poids_smooth'], name="Tendance (Moyenne Mobile)", line=dict(color='firebrick', width=4)))
    fig.update_layout(title="Lissage des variations de poids", xaxis_title="Date", yaxis_title="Kg")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Scatter plot pour voir l'impact des calories sur le poids
    fig_corr = px.scatter(df, x="calories", y="poids", color="seance_faite", 
                         trendline="ols", title="Relation Calories / Poids")
    st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    # --- MICRO MODÈLE DE MACHINE LEARNING ---
    if len(df) > 3:
        X = df[['days_since_start']].values
        y = df['poids'].values
        model = LinearRegression()
        model.fit(X, y)
        
        # Prédiction à 30 jours
        future_days = np.array([[df['days_since_start'].max() + 30]])
        pred_poids = model.predict(future_days)[0]
        
        st.subheader("Prédiction IA (Régression Linéaire)")
        st.write(f"Si tu continues sur cette lancée, ton poids estimé dans **30 jours** sera de :")
        st.header(f"🎯 {round(pred_poids, 2)} kg")
        
        st.info("Le modèle se base sur ta progression actuelle. Si tu augmentes tes calories (Biscoff/beurre de cacahuète), la pente changera !")
    else:
        st.warning("Pas assez de données pour lancer l'IA (minimum 4 jours requis).")