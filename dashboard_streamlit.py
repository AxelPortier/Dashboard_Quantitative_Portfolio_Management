import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration initiale de la page
st.set_page_config(layout="wide")

# --- Contenu du Tableau de Bord Général ---

st.title("📊 Dashboard Général : Vue d'Ensemble des Marchés")
st.markdown("---")

st.header("Indices Clés (Exemple : S&P 500)")

st.info("Utilisez le menu déroulant à gauche (géré automatiquement par Streamlit) pour naviguer vers le module d'Analyse Univariée.")

# Exemple de données simulées pour un graphique
data_points = 100
dates = pd.date_range(end=pd.Timestamp.now(), periods=data_points, freq='D')
# Nécessite np.random.randn
sp_data = pd.DataFrame({
    'Prix S&P 500': np.cumsum(np.random.randn(data_points) * 0.5) + 3000
}, index=dates)

st.subheader("Performance Récente du Marché")
st.line_chart(sp_data)

st.subheader("Statistiques Rapides")
col1, col2, col3 = st.columns(3)
# Assurez-vous d'utiliser np.random.randn si vous n'avez pas de données réelles
col1.metric("S&P 500 Aujourd'hui", f"{sp_data['Prix S&P 500'].iloc[-1]:.2f}", "0.45%")
col2.metric("Volatilité VIX", "15.30", "-1.2%")
col3.metric("Taux 10 ans US", "4.21%", "0.02%")

st.markdown("---")