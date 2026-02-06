# 🏗️ Simulateur de Paie BTP - ACTERIM

Simulateur de calcul de paie pour le secteur du BTP avec gestion complète des cotisations, heures supplémentaires, indemnités de déplacement et facturation client.

## 🚀 Application en ligne

👉 **[Accéder au simulateur](https://acterim-simulateur-btp.streamlit.app)**

## 📋 Fonctionnalités

### ✅ Calculs de paie complets
- Heures normales et supplémentaires (25% et 50%)
- Cotisations salariales et patronales détaillées
- Net imposable et net à payer
- Retenue à la source (RAS)

### 🚗 Gestion des déplacements
- **Grand Déplacement** : Indemnités repas et découchés
- **Petit Déplacement** : Base de données par département
  - Taux horaires automatiques
  - Indemnités transport par zone
  - Prime trajet brut
  - Panier repas soumis

### 💰 Facturation client
- Calcul du coût intérimaire complet
- Marge cible configurable
- Taux horaire client


### 🔒 Sécurité
- Accès protégé par mot de passe pour les sections sensibles
- Cotisations salariales détaillées
- Charges patronales détaillées
- Facturation client

### ⚙️ Options avancées
- Mode Expert (saisie manuelle de tous les paramètres)
- Repas automatiques pour atteindre le net cible
- Gestion du logement (coût et participation salarié)
- Options IFM et ICCP

## 📊 Base de données Petit Déplacement

Le simulateur utilise une base de données Excel (`BASE_DE_DONNE_PD.xlsx`) contenant :

| Feuille | Contenu |
|---------|---------|
| **Taux_Horaires** | Taux par département et niveau (N1, N2, N3, N4) |
| **Transport** | Indemnités transport par département et zone (IA à IF) |
| **Trajet_Brut** | Prime trajet brut par département et zone |
| **Repas_Soumis** | Panier repas soumis par département |

## 🛠️ Technologies utilisées

- **Python 3.10+**
- **Streamlit** - Interface web interactive
- **Pandas** - Manipulation des données
- **OpenPyXL** - Lecture des fichiers Excel

## 📦 Installation locale

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/simulateur-btp-acterim.git
cd simulateur-btp-acterim
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
streamlit run simulateur_btp_v7.py
```

4. **Ouvrir dans le navigateur**
L'application s'ouvre automatiquement à l'adresse : `http://localhost:8501`

## 📁 Structure des fichiers

```
simulateur-btp-acterim/
├── simulateur_btp_v7.py          # Code principal
├── BASE_DE_DONNE_PD.xlsx         # Base de données départements
├── logo_acterim.png              # Logo de l'entreprise
├── requirements.txt              # Dépendances Python
└── README.md                     # Ce fichier
```

## ⚙️ Configuration

### Modifier le mot de passe

Pour des raisons de sécurité, il est recommandé d'utiliser les **Secrets** de Streamlit :

1. Sur Streamlit Cloud : Settings → Secrets
2. Ajouter :
```toml
mot_de_passe = "votre_nouveau_mot_de_passe"
```

3. Dans le code, remplacer par :
```python
MOT_DE_PASSE_CORRECT = st.secrets["mot_de_passe"]
```

### Mettre à jour les barèmes 2026

Les constantes sont définies en début de fichier :
```python
SMIC_LEGAL_2026 = 12.02
INDEMNITE_DECOUCHE_2026 = 51.60
INDEMNITE_REPAS_2026 = 21.40
```

## 📱 Compatibilité

✅ Desktop (Windows, Mac, Linux)
✅ Tablette
✅ Mobile (interface responsive)

## 🔄 Mises à jour

Les mises à jour sont automatiquement déployées dès qu'un fichier est modifié sur GitHub.

## 📞 Support

Pour toute question ou problème :
- 📧 Email : philippe.roger@acterim.fr
- 📝 Issues GitHub : Créer une issue sur ce repository

## 📄 Licence

© 2025 ACTÉRIM - Tous droits réservés

---

**Version** : 7.0
**Dernière mise à jour** : Janvier 2026
**Barème** : 2026
