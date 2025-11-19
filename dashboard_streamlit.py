import yfinance as yf
import matplotlib.pyplot as plt
import datetime

# --- 1. Définition des Paramètres ---
# Ticker pour l'indice S&P 500 (généralement ^GSPC ou ^SPX)
TICKER = "^GSPC"
# Calcul de la date de début (il y a 15 ans à partir d'aujourd'hui)
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=15 * 365) 

# --- 2. Téléchargement des Données avec yfinance ---
print(f"Téléchargement des données pour {TICKER} de {start_date} à {end_date}...")
try:
    # Télécharger l'historique des prix (seulement la colonne 'Close' nous intéresse)
    sp500_data = yf.download(TICKER, start=start_date, end=end_date)
    
    if sp500_data.empty:
        print(f"Erreur: Aucune donnée trouvée pour le ticker {TICKER}.")
    
    # Isoler la colonne des prix de clôture
    close_prices = sp500_data['Close']
    
except Exception as e:
    print(f"Une erreur est survenue lors du téléchargement: {e}")
    exit()

# --- 3. Affichage du Graphique avec Matplotlib ---
plt.figure(figsize=(14, 7)) # Définir la taille du graphique
close_prices.plot(color='blue', linewidth=1.5)

# Définir le titre et les labels
plt.title(f"Cours de Clôture du S&P 500 ({TICKER}) sur les 15 Dernières Années", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Prix de Clôture (USD)", fontsize=12)

# Ajouter une grille pour la lisibilité
plt.grid(True, linestyle='--', alpha=0.7)


plt.show()