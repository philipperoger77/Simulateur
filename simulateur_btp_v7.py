"""
╔════════════════════════════════════════════════════════════════════════════╗
║   ACTÉRIM - Simulateur de Paie BTP V7                                      ║
║   Base de données complète : Taux + Transport + Trajet + Repas Soumis     ║
║   Barème 2026 : SMIC 12.02€/h - Découché 51.60€ - Repas 21.40€            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import math
import base64
import pandas as pd
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
# CHARGEMENT DE LA BASE DE DONNÉES PETIT DÉPLACEMENT
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def charger_base_donnees_pd():
    """Charge les données Excel pour les Petits Déplacements"""
    try:
        # Chemin du fichier Excel (même dossier que le script)
        fichier_excel = Path(__file__).parent / "BASE_DE_DONNE_PD.xlsx"
        
        # Charger les 4 feuilles
        df_taux = pd.read_excel(fichier_excel, sheet_name='Taux_Horaires')
        df_transport = pd.read_excel(fichier_excel, sheet_name='Transport')
        df_trajet = pd.read_excel(fichier_excel, sheet_name='Trajet_Brut')
        df_repas = pd.read_excel(fichier_excel, sheet_name='Repas_Soumis')
        
        # Nettoyer : convertir Département en string et supprimer espaces
        for df in [df_taux, df_transport, df_trajet, df_repas]:
            df['Département'] = df['Département'].astype(str).str.strip()
        
        return df_taux, df_transport, df_trajet, df_repas
    except Exception as e:
        st.error(f"⚠️ Erreur chargement base PD : {e}")
        return None, None, None, None

# Charger les données
df_taux_horaires, df_transport_pd, df_trajet_brut_pd, df_repas_soumis_pd = charger_base_donnees_pd()

def lookup_taux_horaire(departement, niveau):
    """Récupère le taux horaire selon département et niveau"""
    if df_taux_horaires is None or not departement:
        return None
    
    ligne = df_taux_horaires[df_taux_horaires['Département'] == departement]
    if ligne.empty:
        return None
    
    return float(ligne[niveau].iloc[0])

def lookup_transport(departement, zone):
    """Récupère l'indemnité transport selon département et zone"""
    if df_transport_pd is None or not departement:
        return None
    
    ligne = df_transport_pd[df_transport_pd['Département'] == departement]
    if ligne.empty:
        return None
    
    # Convertir "Zone IA - 0 km à 4 km" en "Zone_IA"
    zone_col = "Zone_" + zone.split(" ")[1]  # Extrait "IA", "IB", etc.
    return float(ligne[zone_col].iloc[0])

def lookup_trajet_brut(departement, zone):
    """Récupère la prime trajet brut selon département et zone"""
    if df_trajet_brut_pd is None or not departement:
        return None
    
    ligne = df_trajet_brut_pd[df_trajet_brut_pd['Département'] == departement]
    if ligne.empty:
        return None
    
    # Convertir "Zone IA - 0 km à 4 km" en "Zone_IA"
    zone_col = "Zone_" + zone.split(" ")[1]  # Extrait "IA", "IB", etc.
    return float(ligne[zone_col].iloc[0])

def lookup_repas_soumis(departement):
    """Récupère le panier repas soumis selon département"""
    if df_repas_soumis_pd is None or not departement:
        return None
    
    ligne = df_repas_soumis_pd[df_repas_soumis_pd['Département'] == departement]
    if ligne.empty:
        return None
    
    return float(ligne['Panier soumis'].iloc[0])

# Configuration de la page
st.set_page_config(
    page_title="ACTÉRIM - Simulateur Paie BTP",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour charger le logo en base64
def get_logo_base64():
    try:
        logo_path = Path("logo_acterim.png")
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_base64()

# CSS personnalisé ACTÉRIM V2 avec couleurs turquoise
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Fond général moins blanc */
    .main {
        background-color: #F5F7FA;
    }
    
    /* Header ACTÉRIM avec logo */
    .acterim-header {
        background: linear-gradient(135deg, #202E3B 0%, #2a3f4f 100%);
        padding: 10px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .acterim-logo-img {
        max-height: 50px;
        width: auto;
    }
    
    /* Titres */
    h1, h2, h3 {
        color: #202E3B !important;
    }
    
    h2 {
        border-left: 4px solid #49c7cb;
        padding-left: 15px;
        margin-top: 30px !important;
        background: linear-gradient(90deg, #e6f9fa 0%, transparent 100%);
        padding: 10px 15px;
        border-radius: 5px;
    }
    
    /* Métriques - SANS flèches ni croix */
    [data-testid="stMetricValue"] {
        color: #202E3B !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricDelta"] {
        display: none !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #5a6c7d !important;
        font-weight: 600 !important;
    }
    
    /* Sliders avec couleurs turquoise */
    .stSlider > div > div > div > div {
        background-color: #49c7cb !important;
    }
    
    /* Expanders avec turquoise */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, #e6f9fa 0%, #f0fafb 100%);
        border-left: 4px solid #00a99f;
        font-weight: 600;
        color: #202E3B !important;
    }
    
    /* Sidebar fond clair */
    section[data-testid="stSidebar"] {
        background-color: #FAFBFC;
    }
    
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #202E3B !important;
        font-weight: 600 !important;
        border-left: 3px solid #49c7cb;
        padding-left: 10px;
    }
    
    /* Labels dans la sidebar */
    section[data-testid="stSidebar"] label {
        color: #202E3B !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #202E3B !important;
    }
    
    /* Checkboxes dans la sidebar */
    section[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
        color: #202E3B !important;
    }
    
    /* Input text dans la sidebar */
    section[data-testid="stSidebar"] input {
        color: #202E3B !important;
    }
    
    /* Badges turquoise */
    .badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 15px;
    }
    
    .badge-comptable {
        background: linear-gradient(135deg, #00a99f 0%, #49c7cb 100%);
        color: white;
    }
    
    .badge-tresorerie {
        background: linear-gradient(135deg, #F05534 0%, #ff6b4a 100%);
        color: white;
    }
    
    /* Cards */
    .result-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Info boxes turquoise */
    .stAlert {
        background: linear-gradient(135deg, #e6f9fa 0%, #f0fafb 100%);
        border-left: 4px solid #00a99f;
    }
    
    /* Formules de calcul */
    .formula-box {
        background: #f8f9fa;
        border-left: 3px solid #49c7cb;
        padding: 10px 15px;
        margin: 10px 0;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        color: #202E3B;
    }
</style>
""", unsafe_allow_html=True)

# Header avec logo ACTÉRIM
if logo_b64:
    st.markdown(f"""
    <div class="acterim-header">
        <img src="data:image/png;base64,{logo_b64}" class="acterim-logo-img" alt="ACTÉRIM Logo">
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="acterim-header">
        <div style="color: white; font-size: 36px; font-weight: 700;">Actérim - Simulateur Paie BTP</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("**Barème 2026** : SMIC 12.02€/h • Découché 51.60€ • Repas GD 21.40€ • Repas PD 10.40€ • PMSS 4005€")

# Mot de passe pour accès détails
st.markdown("---")
mot_de_passe = st.text_input("🔒 Mot de passe (pour détails)", type="password", help="Saisissez le mot de passe pour accéder aux détails des calculs")
acces_details = (mot_de_passe == "acterim")

# ═══════════════════════════════════════════════════════════════════════════
# FONCTION CALCUL RGDU
# ═══════════════════════════════════════════════════════════════════════════

def calculer_rgdu(brut_total, heures_travaillees, smic_horaire=12.02):
    """Calcule la Réduction Générale Des Cotisations patronales (RGDU)"""
    T_MIN = 0.0200
    T_MAX = 0.3981
    T_DELTA = 0.3781
    COEFF_PUISSANCE = 1.75
    
    trois_smic = 3 * smic_horaire * heures_travaillees
    
    if brut_total == 0:
        return 0, 0, 0, trois_smic
    
    step1 = trois_smic / brut_total
    step2 = step1 - 1
    step3 = step2 / 2
    step4 = math.pow(step3, COEFF_PUISSANCE)
    step5 = step4 * T_DELTA
    coeff = step5 + T_MIN
    
    coeff_max = min(coeff, T_MAX)
    
    rgdu_avant = coeff_max * brut_total
    rgdu_apres = rgdu_avant * 1.1
    
    return rgdu_avant, rgdu_apres, coeff_max, trois_smic

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR - PARAMÈTRES RÉORGANISÉS
# ═══════════════════════════════════════════════════════════════════════════

st.sidebar.header("⚙️ Paramètres")

with st.sidebar:
    # 1. TYPE DE DÉPLACEMENT (TOUT EN HAUT)
    st.subheader("🚗 Type de Déplacement")
    type_deplacement = st.radio(
        "Choisir le type",
        options=["Grand Déplacement", "Petit Déplacement"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Variables booléennes pour le reste du code
    grand_deplacement = (type_deplacement == "Grand Déplacement")
    petit_deplacement = (type_deplacement == "Petit Déplacement")
    
    # 2. OPTIONS
    st.markdown("---")
    st.subheader("📋 Options")
    col1, col2 = st.columns(2)
    with col1:
        payer_ifm = st.checkbox("IFM (10%)", value=True)
        payer_iccp = st.checkbox("ICCP (10%)", value=True)
    with col2:
        attestation_fiscale = st.checkbox("Attestation fiscale", value=True, 
                                         help="Si cochée : cotisation maladie 5.5%. Si décochée : CSG/CRDS")
        mode_expert = st.checkbox("🔧 Mode Expert", value=False,
                                 help="Options avancées : taux personnalisables, repas auto")
    
    # OPTIONS MODE EXPERT
    if mode_expert:
        st.markdown("**⚙️ Paramètres Mode Expert :**")
        
        repas_auto = st.checkbox("🍽️ Repas automatiques pour atteindre le net", value=False,
                                help="Calcule automatiquement les repas nécessaires pour atteindre le net promis")
        
        taux_accident = st.number_input("Taux accident du travail (%)", 0.0, 10.0, 3.0, 0.1) / 100
        
        reduction_hs_choix = st.radio(
            "Réduction HS patronale (€/h)",
            options=[0.5, 1.5],
            index=1,
            horizontal=True,
            help="0.5€/h ou 1.5€/h selon le cas"
        )
        reduction_hs_patronale_euro = reduction_hs_choix
    else:
        repas_auto = False
        taux_accident = 0.03
        reduction_hs_patronale_euro = 1.5
    
    # 3. PARAMÈTRES DÉPLACEMENT (si Petit Déplacement)
    if petit_deplacement:
        st.markdown("---")
        st.subheader("🗺️ Paramètres Déplacement")
        
        departement = st.text_input("Département (2 caractères)", value="", max_chars=2,
                                   help="Ex: 06 pour Alpes-Maritimes")
        
        zone_chantier = st.selectbox(
            "Zone Chantier",
            options=["Zone IA - 0 km à 4 km", 
                    "Zone IB - 4 km à 10km",
                    "Zone II - 10 km à 20 km",
                    "Zone III - 20 km à 30 km",
                    "Zone IV - 30 km à 40 km",
                    "Zone V - 40 à 50 km"]
        )
        
        niveau = st.selectbox(
            "Niveau",
            options=["N1P1", "N1P2", "N2", "N3P1", "N3P2", "N4P1", "N4P2"]
        )
    else:
        departement = ""
        zone_chantier = "Zone IA - 0 km à 4 km"
        niveau = "N1P1"
    
    # 4. TEMPS DE TRAVAIL
    st.markdown("---")
    st.subheader("⏰ Temps de travail")
    heures_semaine = st.slider("Heures travaillées", 35, 48, 41, 1)
    jours_travailles = st.number_input("Jours travaillés", 1, 7, 5, 1)
    
    # 5. RÉMUNÉRATION
    st.markdown("---")
    st.subheader("💰 Rémunération")
    
    # Taux brut : minimum automatique si PD, mais toujours modifiable
    if petit_deplacement and departement and niveau:
        taux_brut_auto = lookup_taux_horaire(departement, niveau)
        if taux_brut_auto:
            st.info(f"💡 Taux horaire min : **{taux_brut_auto:.2f}€/h** ({departement} - {niveau})")
            # Slider avec minimum = taux auto
            taux_brut = st.slider("Taux Horaire Brut (€/h)", taux_brut_auto, 25.0, taux_brut_auto, 0.01,
                                 help=f"Minimum conventionnel : {taux_brut_auto:.2f}€/h")
        else:
            st.warning(f"⚠️ Département {departement} introuvable, saisie manuelle")
            taux_brut = st.slider("Taux Horaire Brut (€/h)", 12.02, 25.0, 12.02, 0.01)
    else:
        taux_brut = st.slider("Taux Horaire Brut (€/h)", 12.02, 25.0, 12.02, 0.01, 
                             help="Minimum = SMIC 12.02€/h")
    
    taux_net = st.slider("Net €/h promis", 8.0, 20.0, 14.0, 0.5)
    prime_brute = st.number_input("Prime Brute Hebdomadaire (€)", 0.0, 10000.0, 0.0, 10.0)
    
    # Primes Repas et Trajet Brut (si Petit Déplacement) - Prime Repas MANUELLE, Trajet AUTO
    if petit_deplacement:
        # Prime Repas Brut AUTOMATIQUE
        st.write("**Prime Repas Brut (automatique)**")
        if departement:
            taux_prime_repas_auto = lookup_repas_soumis(departement)
            if taux_prime_repas_auto:
                st.info(f"💡 Panier soumis auto : **{taux_prime_repas_auto:.2f}€/jour** ({departement})")
                nb_prime_repas = st.number_input("Quantité", 0, 7, int(jours_travailles), 1, key="nb_prime_repas")
                taux_prime_repas = taux_prime_repas_auto
            else:
                st.warning(f"⚠️ Département {departement} introuvable, saisie manuelle")
                col_pr1, col_pr2 = st.columns([1, 1])
                with col_pr1:
                    nb_prime_repas = st.number_input("Quantité", 0, 7, 0, 1, key="nb_prime_repas")
                with col_pr2:
                    taux_prime_repas = st.number_input("€/jour", 0.0, 100.0, 0.0, 1.0, key="taux_prime_repas")
        else:
            st.warning("⚠️ Renseigner département pour calcul auto")
            col_pr1, col_pr2 = st.columns([1, 1])
            with col_pr1:
                nb_prime_repas = st.number_input("Quantité", 0, 7, 0, 1, key="nb_prime_repas")
            with col_pr2:
                taux_prime_repas = st.number_input("€/jour", 0.0, 100.0, 0.0, 1.0, key="taux_prime_repas")
        
        # Prime Trajet AUTOMATIQUE
        st.write("**Prime Trajet Brut (automatique)**")
        if departement and zone_chantier:
            taux_prime_trajet_auto = lookup_trajet_brut(departement, zone_chantier)
            if taux_prime_trajet_auto:
                st.info(f"💡 Prime trajet auto : **{taux_prime_trajet_auto:.2f}€/jour** ({departement} - {zone_chantier.split(' ')[1]})")
                nb_prime_trajet = st.number_input("Quantité", 0, 7, int(jours_travailles), 1, key="nb_prime_trajet")
                taux_prime_trajet = taux_prime_trajet_auto
            else:
                st.warning(f"⚠️ Données introuvables, saisie manuelle")
                col_pt1, col_pt2 = st.columns([1, 1])
                with col_pt1:
                    nb_prime_trajet = st.number_input("Quantité", 0, 7, 0, 1, key="nb_prime_trajet")
                with col_pt2:
                    taux_prime_trajet = st.number_input("€/jour", 0.0, 100.0, 0.0, 1.0, key="taux_prime_trajet")
        else:
            st.warning("⚠️ Renseigner département et zone pour calcul auto")
            col_pt1, col_pt2 = st.columns([1, 1])
            with col_pt1:
                nb_prime_trajet = st.number_input("Quantité", 0, 7, 0, 1, key="nb_prime_trajet")
            with col_pt2:
                taux_prime_trajet = st.number_input("€/jour", 0.0, 100.0, 0.0, 1.0, key="taux_prime_trajet")
    else:
        nb_prime_repas = 0
        taux_prime_repas = 0.0
        nb_prime_trajet = 0
        taux_prime_trajet = 0.0
    
    # 6. MAJORATIONS HEURES SUP
    st.markdown("---")
    st.subheader("📈 Majorations Heures Sup")
    st.caption("De la 36ème à la 43ème heure (8h max)")
    majo_sup_1 = st.slider("Majoration % (36h-43h)", 0, 100, 25, 5, key="majo1")
    
    st.caption("À partir de la 44ème heure")
    majo_sup_2 = st.slider("Majoration % (44h+)", 0, 100, 50, 5, key="majo2")
    
    # 7. INDEMNITÉS GD (si Grand Déplacement)
    st.markdown("---")
    if grand_deplacement:
        st.subheader("🍽️ Indemnités GD")
        
        st.write("**Repas**")
        col_r1, col_r2 = st.columns([1, 1])
        with col_r1:
            nb_repas_gd = st.number_input("Quantité", 0, 7, 0, 1, key="nb_repas_gd")
        with col_r2:
            taux_repas_gd = st.number_input("€/jour", 0.0, 100.0, 0.0, 1.0, key="taux_repas_gd")
        
        st.write("**Découché**")
        col_d1, col_d2 = st.columns([1, 1])
        with col_d1:
            nb_decouches_gd = st.number_input("Quantité", 0, 7, 0, 1, key="nb_decouches_gd")
        with col_d2:
            taux_decouche_gd = st.number_input("€/nuit", 0.0, 100.0, 0.0, 1.0, key="taux_decouche_gd")
    else:
        nb_repas_gd = 0
        taux_repas_gd = 0.0
        nb_decouches_gd = 0
        taux_decouche_gd = 0.0
    
    # 8. INDEMNITÉS PD (si Petit Déplacement)
    if petit_deplacement:
        st.subheader("🚶 Indemnités PD")
        
        st.write("**Repas (10.40€/jour fixe)**")
        nb_repas_pd = st.number_input("Quantité", 0, 7, 0, 1, key="nb_repas_pd")
        taux_repas_pd = 10.40
        
        # Transport AUTOMATIQUE
        st.write("**Transport (automatique)**")
        if departement and zone_chantier:
            taux_transport_auto = lookup_transport(departement, zone_chantier)
            if taux_transport_auto:
                st.info(f"💡 Transport auto : **{taux_transport_auto:.2f}€/jour** ({departement} - {zone_chantier.split(' ')[1]})")
                nb_transport_pd = st.number_input("Quantité", 0, 7, int(jours_travailles), 1, key="nb_transport_pd")
                taux_transport_pd = taux_transport_auto
            else:
                st.warning(f"⚠️ Données introuvables, saisie manuelle")
                col_tp1, col_tp2 = st.columns([1, 1])
                with col_tp1:
                    nb_transport_pd = st.number_input("Quantité", 0, 7, 0, 1, key="nb_transport_pd")
                with col_tp2:
                    taux_transport_pd = st.number_input("€/jour", 0.0, 100.0, 0.0, 1.0, key="taux_transport_pd")
        else:
            st.warning("⚠️ Renseigner département et zone pour calcul auto")
            col_tp1, col_tp2 = st.columns([1, 1])
            with col_tp1:
                nb_transport_pd = st.number_input("Quantité", 0, 7, 0, 1, key="nb_transport_pd")
            with col_tp2:
                taux_transport_pd = st.number_input("€/jour", 0.0, 100.0, 0.0, 1.0, key="taux_transport_pd")
    else:
        nb_repas_pd = 0
        taux_repas_pd = 10.40
        nb_transport_pd = 0
        taux_transport_pd = 0.0
    
    # 9. FRAIS LOGEMENT
    st.markdown("---")
    st.subheader("🏠 Frais logement")
    logement_hebdo = st.number_input("Logement hors paie €/sem", 0.0, 500.0, 0.0, 10.0)
    cout_logement_salarie = st.number_input("Participation salarié au logement (€/sem)", 0.0, 500.0, 0.0, 10.0)
    
    # 10. REFACTURATION
    st.markdown("---")
    st.subheader("💵 Refacturation")
    nb_refactu = st.number_input("Quantité à refacturer", 0.0, 100.0, 0.0, 1.0)
    taux_refactu = st.number_input("Taux unitaire refactu (€)", 0.0, 1000.0, 0.0, 10.0)
    
    # 11. MARGE
    st.markdown("---")
    st.subheader("📊 Marge cible")
    marge_pct = st.slider("Marge %", 10.0, 25.0, 17.0, 0.5)

# ═══════════════════════════════════════════════════════════════════════════
# CALCULS DÉTAILLÉS
# ═══════════════════════════════════════════════════════════════════════════

# Variables
h = heures_semaine
brut_h = taux_brut
net_h = taux_net
prime = prime_brute
jours = jours_travailles
log = logement_hebdo
cout_log_salarie = cout_logement_salarie
marge = marge_pct / 100
attest_fisc = attestation_fiscale
nb_refact = nb_refactu
taux_refact = taux_refactu

# Variables selon type de déplacement
if grand_deplacement:
    # Indemnités GD (nettes)
    total_repas = nb_repas_gd * taux_repas_gd
    total_decouche = nb_decouches_gd * taux_decouche_gd
    # Primes brutes PD = 0
    total_prime_repas_brut = 0.0
    total_prime_trajet_brut = 0.0
    # Indemnités PD = 0
    total_repas_pd = 0.0
    total_transport_pd = 0.0
else:  # petit_deplacement
    # Indemnités GD = 0
    total_repas = 0.0
    total_decouche = 0.0
    # Primes brutes PD (alimentent le brut)
    total_prime_repas_brut = nb_prime_repas * taux_prime_repas
    total_prime_trajet_brut = nb_prime_trajet * taux_prime_trajet
    # Indemnités PD (nettes)
    total_repas_pd = nb_repas_pd * taux_repas_pd
    total_transport_pd = nb_transport_pd * taux_transport_pd

# 1. BRUT TOTAL AVEC DOUBLE MAJORATION ET PRIMES BRUTES
h_normales = 35
h_sup_tranche1 = 0  # 36-43h à majo_sup_1%
h_sup_tranche2 = 0  # 44h+ à majo_sup_2%

if h > 35:
    if h <= 43:
        h_sup_tranche1 = h - 35
    else:
        h_sup_tranche1 = 8  # Max 8h pour la tranche 1
        h_sup_tranche2 = h - 43

brut_normales = h_normales * brut_h
brut_sup_t1 = h_sup_tranche1 * brut_h * (1 + majo_sup_1 / 100)
brut_sup_t2 = h_sup_tranche2 * brut_h * (1 + majo_sup_2 / 100)
brut_sup_total = brut_sup_t1 + brut_sup_t2

brut_base = brut_normales + brut_sup_total

# Ajout primes (hebdo + primes brutes PD)
brut_avant_ifm = brut_base + prime + total_prime_repas_brut + total_prime_trajet_brut
ifm = brut_avant_ifm * 0.10 if payer_ifm else 0.0
brut_majoré = brut_avant_ifm + ifm
iccp = brut_majoré * 0.10 if payer_iccp else 0.0
brut_total = brut_avant_ifm + ifm + iccp

# 3. CALCUL DU PLAFOND SÉCURITÉ SOCIALE
plafond_ss = (4005 / 30) * jours
tranche_a = min(brut_total, plafond_ss)
tranche_b = max(0, brut_total - plafond_ss)
est_au_dessus_plafond = brut_total > plafond_ss

# 4. COTISATIONS SALARIALES DÉTAILLÉES
part_patron_mutuelle = h_normales * 0.0874
part_patron_prevoyance = brut_total * 0.00449

# CSG sur heures sup (9.7%)
base_hs_csg = brut_sup_total * 0.9825
csg_hs = base_hs_csg * 0.097 if not attest_fisc else 0.0

# CSG 2.9% et 6.8% (base = brut HORS HS × 0.9825 + part patronale)
base_avant_abattement = brut_total - brut_sup_total
base_csg_abattue = base_avant_abattement * 0.9825
base_csg = base_csg_abattue + part_patron_mutuelle + part_patron_prevoyance

csg_deduct = base_csg * 0.068 if not attest_fisc else 0.0
csg_non_deduct = base_csg * 0.029 if not attest_fisc else 0.0

# Maladie
maladie = brut_total * 0.055 if attest_fisc else 0.0

# Cotisations avec logique Tranche A/B
if est_au_dessus_plafond:
    # TRANCHE A (limitée au plafond)
    ss_plaf = tranche_a * 0.069
    comp_incap_t1 = tranche_a * 0.004
    comp_t1 = tranche_a * 0.0401
    
    # TRANCHE B (au-dessus du plafond) - Nouvelles cotisations
    comp_incap_t2 = tranche_b * 0.00335
    comp_t2 = tranche_b * 0.0972
    cet = brut_total * 0.0014
else:
    # Brut sous le plafond - calcul normal
    ss_plaf = brut_total * 0.069
    comp_incap_t1 = brut_total * 0.004
    comp_t1 = brut_total * 0.0401
    
    # Pas de tranche B
    comp_incap_t2 = 0.0
    comp_t2 = 0.0
    cet = 0.0

# Cotisations communes (toujours sur brut total)
ss_deplaf = brut_total * 0.004
comp_sante = h_normales * 0.0874
reduction_hs = brut_sup_total * 0.1131

# TOTAL COTISATIONS SALARIALES
cotis_salar = (maladie + ss_plaf + ss_deplaf + comp_incap_t1 + comp_t1 + 
               comp_sante + csg_deduct + csg_non_deduct + csg_hs + 
               comp_incap_t2 + comp_t2 + cet) - reduction_hs

# 5. NET IMPOSABLE ET RETENUE À LA SOURCE
if attest_fisc:
    net_imposable = brut_total - cotis_salar - brut_sup_total + part_patron_mutuelle
else:
    # Réintégrer les CSG non déductibles (HS + 2.9%)
    net_imposable = brut_total - cotis_salar + part_patron_mutuelle + csg_hs + csg_non_deduct - brut_sup_total

base_pas = (net_imposable * 0.9) - (55 * jours)
retenue_source = max(0, base_pas * 0.12)

# 6. NET AVANT RÉGULARISATION et REPAS AUTO
net_avant_regul = brut_total - cotis_salar - retenue_source + total_repas + total_decouche + total_repas_pd + total_transport_pd - cout_log_salarie
net_cible = net_h * h
regul_initiale = max(0, net_cible - net_avant_regul)

# REPAS AUTOMATIQUES pour atteindre le net
nb_repas_auto = 0
montant_repas_auto = 0
taux_repas_auto = 0

if repas_auto and regul_initiale > 0:
    # Plafond selon attestation fiscale
    taux_max_repas = 21.40 if attest_fisc else 10.40
    
    # Nombre de repas = nombre de jours travaillés (toujours)
    nb_repas_auto = int(jours)
    
    # Taux unitaire = montant nécessaire / nb de jours (plafonné au taux max)
    taux_repas_auto = min(regul_initiale / nb_repas_auto, taux_max_repas)
    montant_repas_auto = nb_repas_auto * taux_repas_auto
    
    # Recalcul avec les repas auto
    total_repas_final = total_repas + montant_repas_auto
    net_avant_regul_final = brut_total - cotis_salar - retenue_source + total_repas_final + total_decouche + total_repas_pd + total_transport_pd - cout_log_salarie
    regul = max(0, net_cible - net_avant_regul_final)
else:
    total_repas_final = total_repas
    net_avant_regul_final = net_avant_regul
    regul = regul_initiale

# 7. CHARGES PATRONALES avec Tranches A/B et détails
charges_patron = {}

# Cotisations communes (sur brut total)
charges_patron['Secu-Maladie-Mat-Inv-Deces'] = {
    'base': brut_total,
    'taux': 0.13,
    'montant': brut_total * 0.13
}
charges_patron['Complementaire sante'] = {
    'base': h_normales,
    'taux': 0.0874,
    'montant': h_normales * 0.0874,
    'unite': '€/h'
}
charges_patron['Accidents du travail'] = {
    'base': brut_total,
    'taux': taux_accident,
    'montant': brut_total * taux_accident
}
charges_patron['Securite Sociale deplafonnee'] = {
    'base': brut_total,
    'taux': 0.0211,
    'montant': brut_total * 0.0211
}
charges_patron['Famille-Securite Sociale'] = {
    'base': brut_total,
    'taux': 0.0525,
    'montant': brut_total * 0.0525
}
charges_patron['Assurance chomage'] = {
    'base': brut_total,
    'taux': 0.0403,
    'montant': brut_total * 0.0403
}
charges_patron['Autres contributions'] = {
    'base': brut_total,
    'taux': 0.03766,
    'montant': brut_total * 0.03766
}
charges_patron['Cotisations statutaires'] = {
    'base': brut_total,
    'taux': 0.0015,
    'montant': brut_total * 0.0015
}

# Cotisations avec logique Tranche A/B
if est_au_dessus_plafond:
    # TRANCHE A
    charges_patron['Complementaire Incap-Inv-Deces T1'] = {
        'base': tranche_a,
        'taux': 0.00449,
        'montant': tranche_a * 0.00449,
        'tranche': 'A'
    }
    charges_patron['Securite Sociale plafonnee'] = {
        'base': tranche_a,
        'taux': 0.0855,
        'montant': tranche_a * 0.0855,
        'tranche': 'A'
    }
    charges_patron['Complementaire Tranche 1'] = {
        'base': tranche_a,
        'taux': 0.0601,
        'montant': tranche_a * 0.0601,
        'tranche': 'A'
    }
    
    # TRANCHE B (nouvelles lignes)
    charges_patron['Complementaire Incap-Inv-Deces T2'] = {
        'base': tranche_b,
        'taux': 0.00385,
        'montant': tranche_b * 0.00385,
        'tranche': 'B'
    }
    charges_patron['Complementaire Tranche 2'] = {
        'base': tranche_b,
        'taux': 0.1457,
        'montant': tranche_b * 0.1457,
        'tranche': 'B'
    }
    charges_patron['CET 1+2'] = {
        'base': brut_total,
        'taux': 0.0014,
        'montant': brut_total * 0.0014,
        'note': 'Si > plafond'
    }
else:
    # Brut sous le plafond - calcul normal
    charges_patron['Complementaire Incap-Inv-Deces T1'] = {
        'base': brut_total,
        'taux': 0.00449,
        'montant': brut_total * 0.00449
    }
    charges_patron['Securite Sociale plafonnee'] = {
        'base': brut_total,
        'taux': 0.0855,
        'montant': brut_total * 0.0855
    }
    charges_patron['Complementaire Tranche 1'] = {
        'base': brut_total,
        'taux': 0.0601,
        'montant': brut_total * 0.0601
    }

cotis_patron_brutes = sum([v['montant'] for v in charges_patron.values()])
reduction_patron_hs = (h_sup_tranche1 + h_sup_tranche2) * reduction_hs_patronale_euro

# 8. CALCUL RGDU
SMIC_LEGAL_2026 = 12.02
rgdu_avant, rgdu, coeff, trois_smic = calculer_rgdu(brut_total, h, SMIC_LEGAL_2026)
cotis_patron = cotis_patron_brutes - reduction_patron_hs - rgdu

# 9. COÛT TOTAL ET FACTURATION
cout_total_comptable = brut_total + cotis_patron + log + total_repas_final + total_decouche + total_repas_pd + total_transport_pd - cout_log_salarie
cout_total_tresorerie = cout_total_comptable + regul

ca_refactu = nb_refact * taux_refact

# CA HT : marge sur le coût TOTAL (intérimaire + refacturation)
cout_total_avec_refactu_comptable = cout_total_comptable + ca_refactu
ca_ht_comptable = cout_total_avec_refactu_comptable / (1 - marge)
taux_fact_comptable = ca_ht_comptable / h
marge_euro_comptable = ca_ht_comptable - cout_total_avec_refactu_comptable
coeff_comptable = taux_fact_comptable / brut_h

cout_total_avec_refactu_tresorerie = cout_total_tresorerie + ca_refactu
ca_ht_tresorerie = cout_total_avec_refactu_tresorerie / (1 - marge)
taux_fact_tresorerie = ca_ht_tresorerie / h
marge_euro_tresorerie = ca_ht_tresorerie - cout_total_avec_refactu_tresorerie
coeff_tresorerie = taux_fact_tresorerie / brut_h

# ═══════════════════════════════════════════════════════════════════════════
# AFFICHAGE DES RÉSULTATS DÉTAILLÉS
# ═══════════════════════════════════════════════════════════════════════════

st.header("📊 Résultats du Calcul")

# SALAIRE BRUT DÉTAILLÉ
with st.expander("💵 SALAIRE BRUT (Détails et formules)", expanded=True):
    st.markdown("### Décomposition des heures")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Heures normales", f"{h_normales}h")
        st.markdown(f'<div class="formula-box">{h_normales}h × {brut_h:.2f}€ = {brut_normales:.2f}€</div>', 
                   unsafe_allow_html=True)
    
    with col2:
        if h_sup_tranche1 > 0:
            st.metric("Heures sup 36-43h", f"{h_sup_tranche1}h (+{majo_sup_1}%)")
            st.markdown(f'<div class="formula-box">{h_sup_tranche1}h × {brut_h:.2f}€ × {1+majo_sup_1/100:.2f} = {brut_sup_t1:.2f}€</div>', 
                       unsafe_allow_html=True)
    
    with col3:
        if h_sup_tranche2 > 0:
            st.metric("Heures sup 44h+", f"{h_sup_tranche2}h (+{majo_sup_2}%)")
            st.markdown(f'<div class="formula-box">{h_sup_tranche2}h × {brut_h:.2f}€ × {1+majo_sup_2/100:.2f} = {brut_sup_t2:.2f}€</div>', 
                       unsafe_allow_html=True)
    
    st.markdown("### Majorations")
    col1, col2, col3 = st.columns(3)
    with col1:
        if prime > 0:
            st.metric("Prime brute hebdo", f"{prime:.2f} €")
    with col2:
        if ifm > 0:
            st.metric("IFM (10%)", f"{ifm:.2f} €")
            st.markdown(f'<div class="formula-box">{brut_avant_ifm:.2f}€ × 0.10 = {ifm:.2f}€</div>', 
                       unsafe_allow_html=True)
    with col3:
        if iccp > 0:
            st.metric("ICCP (10%)", f"{iccp:.2f} €")
            st.markdown(f'<div class="formula-box">{brut_majoré:.2f}€ × 0.10 = {iccp:.2f}€</div>', 
                       unsafe_allow_html=True)
    
    # Afficher les primes brutes PD si présentes
    if total_prime_repas_brut > 0 or total_prime_trajet_brut > 0:
        st.markdown("### Primes Brutes PD (soumises)")
        col1, col2 = st.columns(2)
        with col1:
            if total_prime_repas_brut > 0:
                st.metric("Prime Repas Brut", f"{total_prime_repas_brut:.2f} €")
                st.markdown(f'<div class="formula-box">{nb_prime_repas} × {taux_prime_repas:.2f}€ = {total_prime_repas_brut:.2f}€</div>', 
                           unsafe_allow_html=True)
        with col2:
            if total_prime_trajet_brut > 0:
                st.metric("Prime Trajet Brut", f"{total_prime_trajet_brut:.2f} €")
                st.markdown(f'<div class="formula-box">{nb_prime_trajet} × {taux_prime_trajet:.2f}€ = {total_prime_trajet_brut:.2f}€</div>', 
                           unsafe_allow_html=True)
    
    st.markdown("---")
    st.metric("**🎯 BRUT TOTAL IMPOSABLE**", f"**{brut_total:.2f} €**")

# COTISATIONS SALARIALES ULTRA DÉTAILLÉES
if acces_details:
    with st.expander("📉 COTISATIONS SALARIALES (Détails et formules)"):
    
        # Afficher le plafond SS
        st.info(f"💡 **Plafond Sécurité Sociale** : {plafond_ss:.2f} € (4005/30 × {jours} jours)")
        if est_au_dessus_plafond:
            st.warning(f"⚠️ **Brut > Plafond** → Tranches A ({tranche_a:.2f}€) et B ({tranche_b:.2f}€)")
    
        if attest_fisc:
            st.info("✅ **Attestation fiscale cochée** : Cotisation maladie Non Résident 5.5% (pas de CSG/CRDS)")
            st.write(f"**Maladie (5.5%)** : {maladie:.2f} €")
            st.markdown(f'<div class="formula-box">Base : {brut_total:.2f}€ × 0.055 = {maladie:.2f}€</div>', 
                       unsafe_allow_html=True)
        else:
            st.warning("❌ **Attestation fiscale décochée** : CSG/CRDS au lieu de maladie 5.5% Non Résident")
            st.markdown("### CSG/CRDS Détaillée")
        
            st.write(f"**CSG NON DÉDUCTIBLE sur heures sup (9.7%)** : {csg_hs:.2f} €")
            st.markdown(f'<div class="formula-box">Base HS : {brut_sup_total:.2f}€ × 98.25% = {base_hs_csg:.2f}€<br>CSG HS : {base_hs_csg:.2f}€ × 0.097 = {csg_hs:.2f}€</div>', 
                       unsafe_allow_html=True)
        
            st.write(f"**CSG NON DÉDUCTIBLE (2.9%)** : {csg_non_deduct:.2f} €")
            st.markdown(f'<div class="formula-box">Base avant abattement : {base_avant_abattement:.2f}€ (brut - HS)<br>Base abattue : {base_avant_abattement:.2f}€ × 98.25% = {base_csg_abattue:.2f}€<br>+ Part patronale mutuelle : {part_patron_mutuelle:.2f}€<br>+ Part patronale prévoyance : {part_patron_prevoyance:.2f}€<br>Base finale : {base_csg:.2f}€<br>CSG 2.9% : {base_csg:.2f}€ × 0.029 = {csg_non_deduct:.2f}€</div>', 
                       unsafe_allow_html=True)
        
            st.write(f"**CSG DÉDUCTIBLE (6.8%)** : {csg_deduct:.2f} €")
            st.markdown(f'<div class="formula-box">CSG 6.8% : {base_csg:.2f}€ × 0.068 = {csg_deduct:.2f}€<br>⚠️ Diminue le net imposable</div>', 
                       unsafe_allow_html=True)
    
        st.markdown("### Cotisations sociales")
    
        if est_au_dessus_plafond:
            st.markdown("**Tranche A (plafonnée) :**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"• SS plafonnée (6.9%) : {ss_plaf:.2f} €")
                st.markdown(f'<div class="formula-box">Tranche A : {tranche_a:.2f}€ × 0.069 = {ss_plaf:.2f}€</div>', 
                           unsafe_allow_html=True)
                st.write(f"• Comp. Incap T1 (0.4%) : {comp_incap_t1:.2f} €")
                st.markdown(f'<div class="formula-box">Tranche A : {tranche_a:.2f}€ × 0.004 = {comp_incap_t1:.2f}€</div>', 
                           unsafe_allow_html=True)
            with col2:
                st.write(f"• Complémentaire T1 (4.01%) : {comp_t1:.2f} €")
                st.markdown(f'<div class="formula-box">Tranche A : {tranche_a:.2f}€ × 0.0401 = {comp_t1:.2f}€</div>', 
                           unsafe_allow_html=True)
        
            st.markdown("**Tranche B (déplafonnée) :**")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"• Comp. Incap T2 (0.335%) : {comp_incap_t2:.2f} €")
                st.markdown(f'<div class="formula-box">Tranche B : {tranche_b:.2f}€ × 0.00335 = {comp_incap_t2:.2f}€</div>', 
                           unsafe_allow_html=True)
            with col2:
                st.write(f"• Complémentaire T2 (9.72%) : {comp_t2:.2f} €")
                st.markdown(f'<div class="formula-box">Tranche B : {tranche_b:.2f}€ × 0.0972 = {comp_t2:.2f}€</div>', 
                           unsafe_allow_html=True)
        
            st.write(f"• **CET 1+2 (0.14%)** : {cet:.2f} €")
            st.markdown(f'<div class="formula-box">Brut total : {brut_total:.2f}€ × 0.0014 = {cet:.2f}€</div>', 
                       unsafe_allow_html=True)
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"• SS plafonnée (6.9%) : {ss_plaf:.2f} €")
                st.markdown(f'<div class="formula-box">Base : {brut_total:.2f}€ × 0.069 = {ss_plaf:.2f}€</div>', 
                           unsafe_allow_html=True)
                st.write(f"• Comp. Incap T1 (0.4%) : {comp_incap_t1:.2f} €")
                st.markdown(f'<div class="formula-box">Base : {brut_total:.2f}€ × 0.004 = {comp_incap_t1:.2f}€</div>', 
                           unsafe_allow_html=True)
            with col2:
                st.write(f"• Complémentaire T1 (4.01%) : {comp_t1:.2f} €")
                st.markdown(f'<div class="formula-box">Base : {brut_total:.2f}€ × 0.0401 = {comp_t1:.2f}€</div>', 
                           unsafe_allow_html=True)
    
        st.markdown("**Cotisations communes :**")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"• SS déplafonnée (0.4%) : {ss_deplaf:.2f} €")
            st.write(f"• Complémentaire santé : {comp_sante:.2f} €")
        with col2:
            st.write(f"• ❌ Réduction HS (11.31%) : -{reduction_hs:.2f} €")
    
        st.markdown(f'<div class="formula-box">Réduction HS : {brut_sup_total:.2f}€ × 0.1131 = {reduction_hs:.2f}€</div>', 
                   unsafe_allow_html=True)
        
        st.markdown("---")
        st.metric("**TOTAL COTISATIONS SALARIALES**", f"**{cotis_salar:.2f} €**")
else:
    st.info("🔒 Saisissez le mot de passe pour accéder aux détails des cotisations salariales")

# NET À PAYER DÉTAILLÉ
with st.expander("💰 NET À PAYER (Détails et formules)", expanded=True):
    st.markdown("### Calcul du net")
    
    # Afficher d'abord le détail du net fiscal
    st.markdown("**Détail du NET FISCAL (Net imposable) :**")
    if attest_fisc:
        st.markdown(f"""
        <div class="formula-box">
        • Brut total : {brut_total:.2f} €<br>
        • - Cotisations salariales : -{cotis_salar:.2f} €<br>
        • - Heures sup : -{brut_sup_total:.2f} €<br>
        • + Part patronale mutuelle : +{part_patron_mutuelle:.2f} €<br>
        <strong>= NET FISCAL : {net_imposable:.2f} €</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="formula-box">
        • Brut total : {brut_total:.2f} €<br>
        • - Cotisations salariales : -{cotis_salar:.2f} €<br>
        • + Part patronale mutuelle : +{part_patron_mutuelle:.2f} €<br>
        • + CSG HS non déductible (réintégrée) : +{csg_hs:.2f} €<br>
        • + CSG 2.9% non déductible (réintégrée) : +{csg_non_deduct:.2f} €<br>
        • - Heures sup : -{brut_sup_total:.2f} €<br>
        <strong>= NET FISCAL : {net_imposable:.2f} €</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("**Calcul de la Retenue À la Source (RAS) :**")
    st.markdown(f'<div class="formula-box">Base RAS : ({net_imposable:.2f}€ × 0.9) - (55 × {jours}) = {base_pas:.2f}€<br>Retenue : {base_pas:.2f}€ × 0.12 = {retenue_source:.2f}€</div>', 
               unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Calcul du net à payer :**")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(f"Brut total : **{brut_total:.2f} €**")
        st.write(f"❌ Cotisations salariales : **-{cotis_salar:.2f} €**")
        st.write(f"❌ Retenue à la source : **-{retenue_source:.2f} €**")
        if total_repas > 0:
            st.write(f"✅ Indemnités repas : **+{total_repas:.2f} €**")
        if total_decouche > 0:
            st.write(f"✅ Indemnités découchés : **+{total_decouche:.2f} €**")
        if cout_log_salarie > 0:
            st.write(f"❌ Participation salarié : **-{cout_log_salarie:.2f} €**")
    
    with col2:
        pass
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Net avant régularisation", f"{net_avant_regul_final:.2f} €")
    with col2:
        st.metric("Net cible garanti", f"{net_cible:.2f} €", help=f"{net_h:.2f}€/h × {h}h")
    with col3:
        st.metric("**Régularisation / Avance**", f"**+{regul:.2f} €**")

# CHARGES PATRONALES DÉTAILLÉES
if acces_details:
    with st.expander("🏢 CHARGES PATRONALES (Base + Taux + Montant)"):
        st.markdown("### Charges patronales détaillées")
    
                # Afficher chaque charge avec base, taux et montant
        for key, data in charges_patron.items():
            if isinstance(data, dict):  # ← indenté d'un niveau par rapport au for
                base = data['base']
                taux = data['taux'] * 100
                montant = data['montant']
                
                # Affichage avec note si tranche
                note = ""
                if 'tranche' in data:
                    note = f" [{data['tranche']}]"
                elif 'note' in data:
                    note = f" ({data['note']})"
                elif 'unite' in data:
                    note = f" ({data['unite']})"
                
                st.write(f"**{key}{note}** : {montant:.2f} €")
                st.markdown(f'<div class="formula-box">Base : {base:.2f}€ × {taux:.2f}% = {montant:.2f}€</div>', 
                           unsafe_allow_html=True)
    
        st.markdown("---")
        st.write(f"**Total brut** : {cotis_patron_brutes:.2f} €")
    
        st.markdown("### Réductions")
        st.write(f"❌ Réduction HS patronale : -{reduction_patron_hs:.2f} €")
        st.markdown(f'<div class="formula-box">{h_sup_tranche1 + h_sup_tranche2}h HS × {reduction_hs_patronale_euro:.2f}€ = {reduction_patron_hs:.2f}€</div>', 
               unsafe_allow_html=True)
    
        st.write(f"❌ RGDU (après ×1.1) : -{rgdu:.2f} €")
        st.markdown(f'<div class="formula-box">3 SMIC : 3 × {SMIC_LEGAL_2026}€ × {h}h = {trois_smic:.2f}€<br>Coefficient : {coeff:.4f} ({coeff*100:.2f}%)<br>RGDU avant ×1.1 : {rgdu_avant:.2f}€<br>RGDU après ×1.1 : {rgdu:.2f}€</div>', 
                   unsafe_allow_html=True)
        
        st.markdown("---")
        st.metric("**CHARGES PATRONALES NETTES**", f"**{cotis_patron:.2f} €**")
else:
        st.info("🔒 Saisissez le mot de passe pour accéder aux détails des charges patronales")

    # FACTURATION CLIENT
st.markdown("---")
if acces_details:
    with st.expander("💼 FACTURATION CLIENT", expanded=True):
        # MODE PRINCIPAL (ex-comptable)
        st.markdown('<div class="badge badge-comptable">💰 FACTURATION CLIENT</div>', unsafe_allow_html=True)

        st.write("**Composition du coût intérimaire :**")
        st.write(f"• Brut total : {brut_total:.2f} €")
        st.write(f"• Charges patronales : {cotis_patron:.2f} €")
        st.write(f"• Logement : {log:.2f} €")
        st.write(f"• Indemnités repas (manuels) : {total_repas:.2f} €")
        if repas_auto and nb_repas_auto > 0:
            st.write(f"• 🍽️ Repas automatiques : {montant_repas_auto:.2f} € ({nb_repas_auto} × {taux_repas_auto:.2f}€)")
        st.write(f"• Indemnités découchés : {total_decouche:.2f} €")
        if total_repas_pd > 0:
            st.write(f"• 🚶 Indemnités Repas PD : {total_repas_pd:.2f} €")
        if total_transport_pd > 0:
            st.write(f"• 🚶 Indemnités Transport PD : {total_transport_pd:.2f} €")
        if cout_log_salarie > 0:
            st.write(f"• ❌ Participation salarié : -{cout_log_salarie:.2f} €")

        st.markdown("---")
        st.metric("**Coût total intérimaire**", f"**{cout_total_comptable:.2f} €**")
        if ca_refactu > 0:
            st.write(f"✅ Coût refacturation : +{ca_refactu:.2f} € ({nb_refact:.1f} × {taux_refact:.2f}€)")
            st.metric("**Coût TOTAL**", f"**{cout_total_avec_refactu_comptable:.2f} €**")

        st.write(f"Marge cible ({marge_pct:.1f}%) : {marge_euro_comptable:.2f} €")

        st.markdown("---")
        st.metric("**CA HT NÉCESSAIRE**", f"**{ca_ht_comptable:.2f} €**")
        st.metric("**Taux facturation client**", f"**{taux_fact_comptable:.2f} €/h**")

        # MODE TRÉSORERIE (caché dans expander)
        if regul > 0 and not repas_auto:
            with st.expander("💸 Facturation avec avance non récupérable"):
                st.write("**Composition du coût :**")
                st.write(f"• Coût total intérimaire : {cout_total_comptable:.2f} €")
                st.write(f"• ✅ Avance non récupérable : +{regul:.2f} €")
            
                st.markdown("---")
                st.metric("**Coût total avec avance**", f"**{cout_total_tresorerie:.2f} €**")
                if ca_refactu > 0:
                    st.write(f"✅ Coût refacturation : +{ca_refactu:.2f} €")
                    st.metric("**Coût TOTAL**", f"**{cout_total_avec_refactu_tresorerie:.2f} €**")
            
                st.write(f"Marge cible ({marge_pct:.1f}%) : {marge_euro_tresorerie:.2f} €")
            
                st.markdown("---")
                st.metric("**CA HT NÉCESSAIRE**", f"**{ca_ht_tresorerie:.2f} €**")
                st.metric("**Taux facturation client**", f"**{taux_fact_tresorerie:.2f} €/h**")
else:
    st.info("🔒 Saisissez le mot de passe pour accéder aux détails de la facturation client")

# RÉSUMÉ ET WARNINGS
st.markdown("---")
if acces_details:
    with st.expander("📋 RÉSUMÉ", expanded=True):
        # Infos générales
        resume_text = f"""
**Options payées :**
- IFM : {"✅ Oui" if payer_ifm else "❌ Non"}
- ICCP : {"✅ Oui" if payer_iccp else "❌ Non"}

**Facturation :**
- CA HT : {ca_ht_comptable:.2f} €
- Marge : {marge_euro_comptable:.2f} € ({marge_pct:.1f}%)
- Taux horaire : {taux_fact_comptable:.2f} €/h
"""
        st.info(resume_text)

        # Warnings conditionnels
        if repas_auto and nb_repas_auto > 0:
            st.warning(f"""
    ⚠️ **Repas automatiques activés**
    
    {nb_repas_auto} repas à {taux_repas_auto:.2f}€ ont été déclenchés pour vous permettre d'atteindre le net promis ({net_cible:.2f}€).
    
    Vous pouvez désactiver cette option dans les paramètres.
    """)

        if not repas_auto and regul > 0:
            st.warning(f"""
    ⚠️ **Avance nécessaire**
    
    Une avance de {regul:.2f}€ est nécessaire pour atteindre le net promis ({net_cible:.2f}€).
    
    Options :
    - Activer les repas automatiques pour couvrir cette avance
    - Consulter le mode "Facturation avec avance non récupérable" ci-dessus
    """)
else:
    st.info("🔒 Saisissez le mot de passe pour accéder au résumé détaillé")


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #5a6c7d; padding: 20px;">
    <p style="margin: 0;">
        <strong style="color: #202E3B;">Actérim</strong> - Simulateur de Paie BTP V7
    </p>
    <p style="margin: 5px 0 0 0; font-size: 12px;">
        Version Streamlit - Barème 2026
    </p>
</div>
""", unsafe_allow_html=True)
