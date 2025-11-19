import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json 
import numpy as np # Import nécessaire pour le code de conversion
import requests
import pandas as pd

# Fonction principale de l'application Streamlit
def main_minimal():
    st.title("Test de Démarrage Streamlit")
    
    st.markdown("---")


    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=RQ87NAIKVT1WQVJ0'
    r = requests.get(url)
    data = r.json()

    time_series_key = next(iter([k for k in data.keys() if 'Time Series' in k]), None)

    if time_series_key is None:
        print("Erreur: La clé de série temporelle ('Time Series (Xmin)') n'a pas été trouvée dans le dictionnaire.")
        exit()

    # 1.1. Inverser la structure du dictionnaire pour créer le DataFrame
    df_time_series = pd.DataFrame.from_dict(data[time_series_key], orient='index')

    # 1.2. Nettoyer et renommer les colonnes
    # Suppression des préfixes numériques (ex: '1. open' -> 'open')
    new_columns = {col: col.split('. ')[1] for col in df_time_series.columns}
    df_time_series.rename(columns=new_columns, inplace=True)
    df_time_series.rename(columns={'close': 'Close'}, inplace=True) 

    # 1.3. Nettoyer l'index (dates) et le trier
    df_time_series.index = pd.to_datetime(df_time_series.index)
    df_time_series = df_time_series.sort_index(ascending=True) # Trier chronologiquement

    # 1.4. Convertir les colonnes de prix (qui sont des chaînes de caractères) en nombres
    price_columns = ['open', 'high', 'low', 'Close', 'volume']
    df_time_series[price_columns] = df_time_series[price_columns].apply(pd.to_numeric)

    # ... (votre logique de téléchargement et de conversion df_time_series) ...

    # --- 2. Affichage du Graphique ---

    # Extraire les métadonnées pour le titre
    symbol = data['Meta Data'].get('2. Symbol', 'Ticker Inconnu')
    interval = data['Meta Data'].get('4. Interval', 'Intervalle Inconnu')

    # Créer la figure et l'objet Axes Matplotlib (TRÈS IMPORTANT)
    fig, ax = plt.subplots(figsize=(12, 6))

    # Tracer le prix de clôture en utilisant l'objet Axes
    df_time_series['Close'].plot(ax=ax, linewidth=2, color='purple')

    # Définir le titre et les labels Matplotlib
    ax.set_title(f"Prix de Clôture Intraday de {symbol} ({interval})", fontsize=16)
    ax.set_xlabel("Heure", fontsize=12)
    ax.set_ylabel("Prix de Clôture", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    fig.tight_layout()

    # Ligne de code critique : Remplacer plt.show() par st.pyplot()
    st.pyplot(fig) # <--- CORRECTION

    st.subheader("Aperçu des Données (API)")
    st.dataframe(df_time_series[['open', 'high', 'low', 'Close', 'volume']].tail())

if __name__ == '__main__':
    main_minimal()