import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import json

# Configuration de la page
st.set_page_config(page_title="Tableau de bord", layout="wide")

# === Barre utilisateur personnalisée ===
st.markdown("""
    <style>
    .top-bar {
        position: fixed;
        top: 0;
        right: 0;
        width: 15%;
        height: 40px;
        background-color: #000000;
        display: flex;
        justify-content: flex-start;
        align-items: center;
        padding: 0 20px;
        z-index: 100;
        border-bottom: 1px solid #ddd;
    }

    .user-icon {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 500;
        font-family: Arial, sans-serif;
    }

    .user-icon img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        border: 1px solid #999;
    }

    .block-container {
        padding-top: 70px; /* Décale le contenu pour ne pas passer sous la barre */
    }
    </style>

    <div class="top-bar">
        <div class="user-icon">
            <span>👤 Utilisateur connecté</span>
            <img src="https://cdn-icons-png.flaticon.com/512/847/847969.png" alt="user">
        </div>
    </div>
""", unsafe_allow_html=True)



# === Barre latérale ===
st.sidebar.image("images/cst2.png", width=370)

# === Menu principal ===
main_section = st.sidebar.radio("Section principale", [
    "🏠 Tableau de bord",
    "➕ Ajouter une carte",
    "📊 KPI",
    "👥 Employés",
    "⚙️ Configurations"
])

# === Sous-sections (si "Tableau de bord") ===
sub_section = None
if main_section == "🏠 Tableau de bord":
    sub_section = st.sidebar.radio("Sous-section", ["📡 Dispositif", "🏭 Production de blister"])

# === Fonctions de chargement des données ===
@st.cache_data
def load_dispositif_data():
    return pd.DataFrame({
        "Nombre d'arrêts": [4],
        "Énergie (Wh)": [234.7],
        "Nb capteurs actifs": [7]
    })

@st.cache_data
def load_production_data():
    with open("production_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

@st.cache_data
def load_arret_details():
    data = {
        "Début arrêt": [
            "2025-06-03 08:15",
            "2025-06-08 14:30",
            "2025-06-15 09:00",
            "2025-06-25 11:45"
        ],
        "Fin arrêt": [
            "2025-06-03 09:00",
            "2025-06-08 15:10",
            "2025-06-15 09:45",
            "2025-06-25 12:15"
        ]
    }
    df = pd.DataFrame(data)
    df["Début arrêt"] = pd.to_datetime(df["Début arrêt"])
    df["Fin arrêt"] = pd.to_datetime(df["Fin arrêt"])
    df["Durée"] = df["Fin arrêt"] - df["Début arrêt"]
    df["Durée (min)"] = df["Durée"].dt.total_seconds() // 60
    return df

# === Carte stylisée ===
def custom_card(title, value, bg_color, text_color="#FFFFFF"):
    st.markdown(f"""
        <div style='
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 10px;
            background-color: {bg_color};
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        '>
            <h4 style='margin-bottom:5px; color:{text_color}'>{title}</h4>
            <h3 style='margin-top: 0px; color:{text_color}'>{value}</h3>
        </div>
    """, unsafe_allow_html=True)

# === Section : Ajouter une carte ===
if main_section == "➕ Ajouter une carte":
    st.title("➕ Ajouter une carte")
    st.info("Fonction à implémenter : formulaire ou ajout dynamique d'une nouvelle carte au dashboard.")

# === Section : KPI ===
elif main_section == "📊 KPI":
    st.title("📊 Indicateurs de performance")
    st.info("Affichage de KPI globaux (à définir selon besoins métier).")

# === Section : Employés ===
elif main_section == "👥 Employés":
    st.title("👥 Gestion des employés")
    st.info("Liste des utilisateurs, affectations et droits (à implémenter).")

# === Section : Configurations ===
elif main_section == "⚙️ Configurations":
    st.title("⚙️ Paramètres du système")
    st.info("Options de configuration et préférences générales.")

# === Sous-section : Dispositif ===
elif main_section == "🏠 Tableau de bord" and sub_section == "📡 Dispositif":
    st.title("📟 Dispositif")

    # st.sidebar.markdown("### 📅 Paramètres")
    st.sidebar.markdown("### 📅 Période personnalisée")

    start_date_input = st.sidebar.date_input("📅 Date de début", date(2025, 6, 1))
    start_time_input = st.sidebar.time_input("🕒 Heure de début", datetime.strptime("08:00", "%H:%M").time())

    end_date_input = st.sidebar.date_input("📅 Date de fin", date(2025, 7, 1))
    end_time_input = st.sidebar.time_input("🕒 Heure de fin", datetime.strptime("18:00", "%H:%M").time())

    start_datetime = datetime.combine(start_date_input, start_time_input)
    end_datetime = datetime.combine(end_date_input, end_time_input)

    df_dispositif = load_dispositif_data()
    data = df_dispositif.loc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        custom_card("📅 Début période", start_datetime.strftime("%Y-%m-%d %H:%M"), "#0000FF")
        custom_card("⚠️ Nombre d'arrêts", data["Nombre d'arrêts"], "#FF4500")

    with col2:
        custom_card("📆 Fin période", end_datetime.strftime("%Y-%m-%d %H:%M"), "#20B2AA")
        custom_card("⚡ Énergie consommée (Wh)", f"{data['Énergie (Wh)']} ", "#FFD700", "#000000")

    with col3:
        custom_card("🟢 Nb capteurs actifs", data["Nb capteurs actifs"], "#228B22")

    # === Détails des arrêts ===

    # === Graphe : Histogramme horizontal des durées des arrêts ===
    st.subheader("📊 Durées des arrêts (en minutes)")

    df_arrets = load_arret_details().copy()
    df_arrets["Arrêt #"] = ["Arrêt " + str(i + 1) for i in range(len(df_arrets))]

    fig = px.bar(
        df_arrets,
        x="Durée (min)",
        y="Arrêt #",
        orientation="h",
        text="Durée (min)",
        color="Durée (min)",
        color_continuous_scale="Blues",
        title="Durée de chaque arrêt (en minutes)",
        hover_data={
            "Durée (min)": True,
            "Début arrêt": True,
            "Fin arrêt": True,
            "Arrêt #": False  # Évite de le dupliquer dans le hover
        }
    )

    fig.update_layout(
        xaxis_title="Durée (minutes)",
        yaxis_title="Arrêts",
        yaxis=dict(autorange="reversed"),  # Arrêt 1 en haut
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)


# === Sous-section : Production de blister ===
elif main_section == "🏠 Tableau de bord" and sub_section == "🏭 Production de blister":
    st.title("🏭 Production de blister")

    df_production = load_production_data()
    df_production["Date"] = pd.to_datetime(df_production["Date"])

    granularity = st.selectbox("Afficher les données par :", ["Jour", "Heure"])

    if granularity == "Jour":
        df_grouped = df_production.groupby(df_production["Date"].dt.date).agg({
            "Quantité produite": "sum",
            "Quantité rejetée": "sum"
        }).reset_index().rename(columns={"Date": "Date temps"})
    else:
        df_grouped = df_production.groupby(df_production["Date"].dt.floor('H')).agg({
            "Quantité produite": "sum",
            "Quantité rejetée": "sum"
        }).reset_index().rename(columns={"Date": "Date temps"})

    df_grouped["Quantité brute"] = df_grouped["Quantité produite"] - df_grouped["Quantité rejetée"]

    total_produced = df_grouped["Quantité produite"].sum()
    total_rejected = df_grouped["Quantité rejetée"].sum()
    total_brute = df_grouped["Quantité brute"].sum()

    st.subheader("📦 Statistiques selon " + granularity.lower())

    col1, col2, col3 = st.columns(3)
    with col1:
        custom_card("📈 Quantité produite", f"{total_produced} unités", "#4682B4")
    with col2:
        custom_card("❌ Quantité rejetée", f"{total_rejected} unités", "#DC143C")
    with col3:
        custom_card("🧮 Quantité brute", f"{total_brute} unités", "#2E8B57")

    st.subheader("📊 Évolution des quantités")
    st.line_chart(
        df_grouped.set_index("Date temps")[["Quantité produite", "Quantité rejetée", "Quantité brute"]],
        use_container_width=True
    )

    with st.expander("📄 Voir les données regroupées"):
        st.dataframe(df_grouped, use_container_width=True)

    with st.expander("📁 Voir les données brutes"):
        st.dataframe(df_production, use_container_width=True)
