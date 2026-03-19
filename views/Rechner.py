from unicodedata import category

import streamlit as st
from functions.addition import hct_rechner, get_ref
import matplotlib.pyplot as plt
import pytz
import pandas as pd
from utils.data_manager import DataManager  # --- NEW CODE: import data manager ---

st.title("Hämatokrit-Rechner")
st.write("Berechnet Hämatokrit (Hct) mit: **Hct (%) = RBC · MCV / 10**")

with st.form(key="hct_form_hematokrit"):
    sex = st.radio("Geschlecht", ["weiblich", "männlich"], horizontal=True)
    age = st.number_input("Alter [Jahre]", min_value=0, max_value=120, value=30, step=1)

    rbc = st.number_input("RBC [10¹²/L]", min_value=0.0, value=4.50, step=0.01, format="%.2f")
    mcv = st.number_input("MCV [fL]", min_value=0.0, value=90.0, step=0.1, format="%.1f")

    submitted = st.form_submit_button("Berechnen")

if submitted:
    if rbc <= 0 or mcv <= 0:
        st.error("Bitte gültige Werte eingeben: RBC und MCV müssen > 0 sein.")
        st.stop()

    result = hct_rechner(rbc, mcv)

    col1, col2 = st.columns(2)
    col1.metric("Hämatokrit", f"{result["hct_percent"]} %")
    col2.metric("Hämatokrit (L/L)", f"{result['hct_fraction']}")


    lo, hi = get_ref(sex, int(age))
    if lo is None:
        st.info(f"Kein Referenzbereich hinterlegt für {sex}, {int(age)} Jahre.")
    else:
        st.caption(f"Referenzbereich ({sex}, {int(age)} J.): {lo:.1f}–{hi:.1f} %")
        if result["hct_percent"] < lo:
            st.warning("Hct liegt unter dem Referenzbereich.")
        elif result["hct_percent"] > hi:
            st.warning("Hct liegt über dem Referenzbereich.")
        else:
            st.success("Hct liegt im Referenzbereich.")

    # ---- GRAFIK oder Warnung ----
    if result["hct_percent"] < 32 or result["hct_percent"] > 55:
        st.error("Achtung! Extremwert. Präanalytik und klinische Plausibilität kontrollieren.")
    else:
        st.subheader("Einordnung")
        fig, ax = plt.subplots(figsize=(10, 1.6))

        xmin, xmax = 32.0, 55.0

        if lo is not None and hi is not None:
            ax.axvspan(lo, hi, alpha=0.2)

        ax.set_xlim(xmin, xmax)
        ax.set_xticks(range(32, 55, 2))
        ax.set_yticks([])
        ax.set_xlabel("Hct (%)")

        ax.axvline(result["hct_percent"], linewidth=3)
        ax.text(
            result["hct_percent"], 0.6, f"{result['hct_percent']:.1f} %",
            transform=ax.get_xaxis_transform(),
            ha="left", va="center"
        )

        st.pyplot(fig)
        plt.close(fig)

    # --- NEW CODE to update history in session state and display it ---
    st.session_state['data_df'] = pd.concat([st.session_state['data_df'], pd.DataFrame([result])])

    # --- CODE UPDATE: save data to data manager ---
    data_manager = DataManager()
    data_manager.save_user_data(st.session_state['data_df'], 'data.csv')
    # --- END OF CODE UPDATE ---
        
# --- NEW CODE to display the history table ---
st.dataframe(st.session_state['data_df'])

# --- Balkendiagramm der gespeicherten Hct-Werte ---
if not st.session_state['data_df'].empty and "hct_percent" in st.session_state['data_df'].columns:
    st.subheader("Verlauf der gespeicherten Hämatokrit-Werte")

    chart_df = st.session_state['data_df'].copy().tail(10).reset_index(drop=True)
    chart_df["Messung"] = range(1, len(chart_df) + 1)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(chart_df["Messung"], chart_df["hct_percent"])

    ax.set_xlabel("Letzte Messungen")
    ax.set_ylabel("Hct (%)")
    ax.set_title("Letzte 10 gespeicherte Ergebnisse")
    ax.axhline(32, linestyle="--", linewidth=1)
    ax.axhline(55, linestyle="--", linewidth=1)

    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("Noch keine gespeicherten Ergebnisse vorhanden.")