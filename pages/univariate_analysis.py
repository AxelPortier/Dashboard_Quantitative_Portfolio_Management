import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import numpy as np

API_KEY = 'RQ87NAIKVT1WQVJ0' 
BASE_URL = 'https://www.alphavantage.co/query'


def get_stock_data(symbol, interval):
    """Récupère les données boursières intraday via AlphaVantage."""
    url = f'{BASE_URL}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}'
    try:
        r = requests.get(url)
        r.raise_for_status() # Lève une exception pour les codes d'état 4xx/5xx
        data = r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de requête API : {e}")
        return None
    except json.JSONDecodeError:
        st.error("Erreur de décodage JSON : Vérifiez la clé API ou le format de la réponse.")
        return None

    if "Error Message" in data:
        st.error(f"Erreur AlphaVantage : {data['Error Message']}")
        return None
    
    time_series_key = next(iter([k for k in data.keys() if 'Time Series' in k]), None)

    if time_series_key is None:
        st.error("Erreur : La clé de série temporelle n'a pas été trouvée. L'API a-t-elle retourné une erreur?")
        return None

    df_time_series = pd.DataFrame.from_dict(data[time_series_key], orient='index')

    new_columns = {col: col.split('. ')[1] for col in df_time_series.columns}
    df_time_series.rename(columns=new_columns, inplace=True)
    df_time_series.rename(columns={'close': 'Close'}, inplace=True) 

    df_time_series.index = pd.to_datetime(df_time_series.index)
    df_time_series = df_time_series.sort_index(ascending=True) # Trier chronologiquement

    price_columns = ['open', 'high', 'low', 'Close', 'volume']
    df_time_series[price_columns] = df_time_series[price_columns].apply(pd.to_numeric)
    
    symbol = data['Meta Data'].get('2. Symbol', 'Ticker Inconnu')
    interval_str = data['Meta Data'].get('4. Interval', 'Intervalle Inconnu')

    return df_time_series, symbol, interval_str


def univariate_analysis_page():
    """Fonction principale pour la page d'analyse d'actif unique."""
    st.title("📈 Univariate - Single Asset Analysis Module")
    st.markdown("---")

    st.sidebar.header("Paramètres d'Analyse")

    symbol = st.sidebar.text_input("Sélectionnez le Ticker", value="IBM").upper()

    interval = st.sidebar.selectbox("Sélectionnez l'Intervalle", 
                                    options=["5min", "15min", "30min", "60min"], 
                                    index=0)
    
    if st.sidebar.button('Lancer l\'Analyse'):

        with st.spinner(f'Récupération des données pour {symbol}...'):
            result = get_stock_data(symbol, interval)
        
        if result is not None:
            df_time_series, fetched_symbol, fetched_interval = result

            st.subheader(f"Série Temporelle : Prix de Clôture Intraday de {fetched_symbol}")

            fig, ax = plt.subplots(figsize=(12, 6))
            df_time_series['Close'].plot(ax=ax, linewidth=2, color='purple')

            ax.set_title(f"Prix de Clôture Intraday de {fetched_symbol} ({fetched_interval})", fontsize=16)
            ax.set_xlabel("Heure", fontsize=12)
            ax.set_ylabel("Prix de Clôture", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.6)
            fig.tight_layout()

            st.pyplot(fig)

            st.markdown("---")
            st.subheader("Statistiques Descriptives")
            st.dataframe(df_time_series['Close'].describe().to_frame())

            st.subheader("Aperçu des Données Brutes")
            st.dataframe(df_time_series[['open', 'high', 'low', 'Close', 'volume']].tail(10))

# --- Exécution ---
if __name__ == '__main__':
    univariate_analysis_page()