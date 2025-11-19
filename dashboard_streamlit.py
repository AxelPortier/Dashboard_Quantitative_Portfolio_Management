import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import pandas as pd

# --- 1. FONCTION PRINCIPALE STREAMLIT ---
def sp500_app():
    st.title("📈 Cours de Clôture du S&P 500 (15 Ans)")
    st.markdown("Affichage du prix de l'indice S&P 500 via yfinance.")

    # --- 1. Définition des Paramètres ---
    TICKER = "^GSPC"
    
    # Calcul de la date de début (il y a 15 ans)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=15 * 365) 

    # --- 2. Téléchargement des Données avec yfinance ---
    st.info(f"Tentative de téléchargement des données pour {TICKER} de {start_date} à {end_date}...")
    
    try:
        # Télécharger l'historique des prix (seulement la colonne 'Close' nous intéresse)
        # Utilisation de st.cache_data pour éviter de re-télécharger à chaque interaction
        @st.cache_data
        def download_data(ticker, start, end):
             return yf.download(ticker, start=start, end=end)
             
        sp500_data = download_data(TICKER, start_date, end_date)
        
        if sp500_data.empty:
            st.error(f"Erreur: Aucune donnée trouvée pour le ticker {TICKER}.")
            return
        
        # Isoler la colonne des prix de clôture
        close_prices = sp500_data['Close']
        
    except Exception as e:
        st.error(f"Une erreur est survenue lors du téléchargement: {e}")
        return

    # --- 3. Création et Affichage du Graphique avec Matplotlib ---
    
    # Crée une figure Matplotlib
    fig, ax = plt.subplots(figsize=(14, 7))
    close_prices.plot(ax=ax, color='blue', linewidth=1.5)

    # Définir le titre et les labels Matplotlib
    ax.set_title(f"Cours de Clôture du S&P 500 ({TICKER}) sur les 15 Dernières Années", fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Prix de Clôture (USD)", fontsize=12)

    # Ajouter une grille
    ax.grid(True, linestyle='--', alpha=0.7)

    # Afficher la figure Matplotlib dans Streamlit
    st.pyplot(fig)
    
    st.subheader("Aperçu des Données Récentes")
    st.dataframe(sp500_data.tail())


if __name__ == "__main__":
    # La fonction est appelée pour démarrer l'application
    sp500_app()