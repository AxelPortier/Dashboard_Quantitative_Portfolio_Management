import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
# IMPORTANT : J'ajoute cet import. Vous devez avoir un fichier 'univariate_analysis.py' 
# qui contient la fonction 'univariate_analysis_page()'
import univariate_analysis as ua 


# Configuration initiale de la page
st.set_page_config(layout="wide")

# --- Gestion de la Navigation (État de Session) ---
PAGES = {
    "dashboard": "📊 Dashboard Général",
    "univariate": "📈 Univariate - Single Asset Analysis",
    "multivariate": "🔗 Multivariate - Multi-Asset Portfolio",
}

if 'page' not in st.session_state:
    st.session_state['page'] = 'dashboard'

# --- 0. Injection CSS pour le style ---
# J'ajoute le CSS pour le bouton de navigation principal en bas de page
st.markdown("""
<style>
/* Style général des conteneurs de métriques */
div.st-emotion-cache-1r6r8vw { /* Cible le conteneur des colonnes */
    border: 1px solid #E0E0E0;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease-in-out;
    background-color: #FAFAFA;
}

/* Style au survol des cartes */
div.st-emotion-cache-1r6r8vw:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

/* Titre des métriques */
.st-emotion-cache-16idsd1 { /* Cible les titres des métriques */
    font-size: 1.1em;
    font-weight: 600;
    color: #333333;
}

/* Valeurs des métriques */
.st-emotion-cache-1bjpgya { /* Cible la valeur principale */
    font-size: 2.2em;
    font-weight: 700;
    color: #4CAF50; /* Couleur par défaut (vert) */
}

/* Bouton stylisé (pour Rafraîchir) */
div.stButton > button:first-child {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    transition: background-color 0.3s;
}

div.stButton > button:first-child:hover {
    background-color: #45A049;
}

/* Style spécifique pour le bouton de navigation principal (plus grand) */
.main-nav-button {
    background-color: #0077B6 !important; /* Bleu pour la navigation */
    color: white !important;
    font-size: 1.2em !important;
    padding: 15px 30px !important;
    border-radius: 12px !important;
    margin-top: 20px;
}
.main-nav-button:hover {
    background-color: #005A91 !important;
}

/* Réajuster le bouton stylisé pour le Rafraîchissement car il utilise la même classe */
div.st-emotion-cache-199v4c3 div.stButton button:first-child {
    background-color: #4CAF50;
}
</style>
""", unsafe_allow_html=True)


# --- 1. FONCTION D'AFFICHAGE DU DASHBOARD ---
def display_dashboard():
    """Contient tout le contenu de la page d'accueil."""
    
    st.title("📊 Dashboard Général : Vue d'Ensemble des Marchés")
    st.markdown("---")

    # --- 1. Contrôles Utilisateur (Filtrage et Actions) ---
    st.header("Actions & Filtrage")

    col_filter, col_action = st.columns([3, 1])

    with col_filter:
        # Simuler le choix de période d'analyse
        period = st.selectbox(
            "Sélectionner la période d'analyse pour les graphiques :",
            ['1 An', '6 Mois', '3 Mois', '1 Mois'],
            index=0,
            key='period_selector'
        )

    with col_action:
        # Bouton de rafraîchissement
        if st.button(f"Rafraîchir les Données ({datetime.now().strftime('%H:%M:%S')})"):
            st.experimental_rerun() # Rafraîchit l'application
        st.caption("Dernier rafraîchissement automatique à l'exécution.")


    st.markdown("---")


    # --- 2. Statistiques Rapides (Metrics stylisées) ---
    st.subheader("Statistiques Clés du Marché")
    col1, col2, col3 = st.columns(3)

    # Exemple de données simulées
    data_points = 252 # Environ 1 an de jours de trading
    dates = pd.date_range(end=pd.Timestamp.now(), periods=data_points, freq='B')
    sp_data = pd.DataFrame({
        'Prix S&P 500': np.cumsum(np.random.randn(data_points) * 0.5) + 3000
    }, index=dates)

    # Calcul simple de la variation sur la période
    if period == '6 Mois':
        data_filtered = sp_data.last('180D')
    elif period == '3 Mois':
        data_filtered = sp_data.last('90D')
    elif period == '1 Mois':
        data_filtered = sp_data.last('30D')
    else: # 1 An
        data_filtered = sp_data

    # Calcul de la variation en pourcentage sur la période sélectionnée
    start_price = data_filtered['Prix S&P 500'].iloc[0]
    end_price = data_filtered['Prix S&P 500'].iloc[-1]
    change = (end_price - start_price) / start_price * 100
    change_str = f"{change:.2f}%"

    # Affichage des métriques avec le style CSS injecté
    with col1:
        st.metric("S&P 500 (Clôture)", f"{end_price:.2f}", change_str)
    with col2:
        st.metric("Volatilité VIX", "15.30", "-1.2% (vs. J-1)")
    with col3:
        st.metric("Taux 10 ans US", "4.21%", "0.02% (vs. J-1)")

    st.markdown("---")


    # --- 3. Performance Récente du Marché (Graphique) ---
    st.header(f"Performance de l'Indice S&P 500 ({period})")

    # Utilisation de Matplotlib pour plus de contrôle
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data_filtered.index, data_filtered['Prix S&P 500'], label='S&P 500', color='#0077B6', linewidth=2) # Couleur plus professionnelle

    ax.set_title(f"Évolution du S&P 500 sur {period}", fontsize=14)
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel("Prix", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()

    # Affichage du graphique
    st.pyplot(fig)
    plt.close(fig) 

    st.markdown("---")

    # --- 4. Alertes et Informations Marché ---
    st.subheader("📢 Alertes et Nouvelles Marché")

    # Création d'une structure pour simuler des alertes
    alerts = [
        {"type": "⚠️ Risque", "message": "Forte augmentation de la Volatilité Implicite (VIX) de 15% cette semaine."},
        {"type": "✅ Opportunité", "message": "Le secteur Technologique (IT) a cassé sa résistance des 52 semaines : opportunité d'achat?"},
        {"type": "🛑 Économie", "message": "Les chiffres du Chômage sont plus mauvais qu'attendu, pression sur les taux de la Fed."},
    ]

    for alert in alerts:
        if alert['type'] == "⚠️ Risque":
            st.warning(f"{alert['type']}: {alert['message']}")
        elif alert['type'] == "✅ Opportunité":
            st.success(f"{alert['type']}: {alert['message']}")
        elif alert['type'] == "🛑 Économie":
            st.error(f"{alert['type']}: {alert['message']}")

    st.markdown("---")
    
    # --- BOUTON DE NAVIGATION DEMANDÉ ---
    # Nous utilisons une classe CSS personnalisée 'main-nav-button'
    st.markdown("<p style='font-size: 1.1em; font-weight: 500;'>Prêt pour l'analyse détaillée ?</p>", unsafe_allow_html=True)
    if st.button("Aller au Module d'Analyse Univariée 📈", key='nav_to_univariate', help="Cliquez pour analyser un actif individuel"):
        st.session_state['page'] = 'univariate'
        st.experimental_rerun()


# --- 2. FONCTION D'AFFICHAGE DE LA PAGE UNIVARIATE (NON DÉTAILLÉE ICI) ---
def display_univariate_module():
    """Appelle la fonction de la page Univariate (contenue dans univariate_analysis.py)."""
    # Si vous voulez un bouton Retour, vous pouvez l'ajouter ici
    if st.sidebar.button("◀ Retour au Dashboard", key='back_to_dashboard'):
        st.session_state['page'] = 'dashboard'
        st.experimental_rerun()
    
    ua.univariate_analysis_page()


# --- 3. FONCTION D'AFFICHAGE DE LA PAGE MULTIVARIATE (NON DÉTAILLÉE ICI) ---
def display_multivariate_module():
    """Affiche la page Multivariate."""
    st.title("🔗 Multivariate - Multi-Asset Portfolio Module")
    st.markdown("---")
    st.warning("Ce module est en cours de développement.")
    if st.button("◀ Retour au Dashboard", key='back_from_multi'):
        st.session_state['page'] = 'dashboard'
        st.experimental_rerun()


# --- 4. LOGIQUE DE ROUTAGE PRINCIPALE ---
# Cette logique détermine quelle fonction d'affichage est appelée
if st.session_state['page'] == 'dashboard':
    display_dashboard()
elif st.session_state['page'] == 'univariate':
    display_univariate_module()
elif st.session_state['page'] == 'multivariate':
    display_multivariate_module()

# La barre latérale de navigation manuelle (optionnelle si vous voulez deux menus)
st.sidebar.title("Navigation Manuelle")
selection = st.sidebar.radio("Pages", list(PAGES.values()), index=list(PAGES.keys()).index(st.session_state['page']), key='sidebar_nav')
if PAGES[st.session_state['page']] != selection:
    st.session_state['page'] = list(PAGES.keys())[list(PAGES.values()).index(selection)]
    st.experimental_rerun()