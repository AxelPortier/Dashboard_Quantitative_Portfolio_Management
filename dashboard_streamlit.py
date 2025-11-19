import streamlit as st

# Remplacez ceci par le message ou la variable que vous voulez vérifier
message_a_afficher = "Le pipeline est prêt ! Les objets entraînés sont chargés."
valeur_a_verifier = 42 # Remplacez par une variable de votre choix (ex: pls_final.n_components)

# Fonction principale de l'application Streamlit
def main_minimal():
    st.title("Test de Démarrage Streamlit")
    
    st.markdown("---")
    
    # Afficher le message principal
    st.header("Statut : Succès du Chargement")
    st.success(message_a_afficher)
    
    # Afficher une variable spécifique
    st.write(f"Variable de test/vérification : **{valeur_a_verifier}**")

if __name__ == '__main__':
    main_minimal()