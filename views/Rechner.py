import streamlit as st
from functions.addition import hct_rechner
import matplotlib.pyplot as plt

st.title("Hämatokrit-Rechner")
st.write("Berechnet Hämatokrit (Hct) mit: **Hct (%) = RBC · MCV / 10**")

# Beispiel-Referenzbereiche (bitte mit euren Werten ersetzen!)
REF = {
    "weiblich": [(18, 120, 36.0, 46.0)],
    "männlich": [(18, 120, 41.0, 53.0)],
}

def get_ref(sex: str, age: int):
    for a_min, a_max, lo, hi in REF.get(sex, []):
        if a_min <= age <= a_max:
            return lo, hi
    return None, None

with st.form(key="hct_form_hematokrit"):  # <- Key geändert (eindeutig)
    sex = st.radio("Geschlecht", ["weiblich", "männlich"], horizontal=True)
    age = st.number_input("Alter [Jahre]", min_value=0, max_value=120, value=30, step=1)

    rbc = st.number_input("RBC [10¹²/L]", min_value=0.0, value=4.50, step=0.01, format="%.2f")
    mcv = st.number_input("MCV [fL]", min_value=0.0, value=90.0, step=0.1, format="%.1f")

    submitted = st.form_submit_button("Berechnen")

if submitted:
    if rbc <= 0 or mcv <= 0:
        st.error("Bitte gültige Werte eingeben: RBC und MCV müssen > 0 sein.")
        st.stop()  # wichtig, sonst rechnet er weiter

    hct_percent, hct_fraction = hct_rechner(rbc, mcv)

    col1, col2 = st.columns(2)
    col1.metric("Hämatokrit", f"{hct_percent:.1f} %")
    col2.metric("Hämatokrit (L/L)", f"{hct_fraction:.3f}")

    lo, hi = get_ref(sex, int(age))
    if lo is None:
        st.info(f"Kein Referenzbereich hinterlegt für {sex}, {int(age)} Jahre.")
    else:
        st.caption(f"Referenzbereich ({sex}, {int(age)} J.): {lo:.1f}–{hi:.1f} %")
        if hct_percent < lo:
            st.warning("Hct liegt unter dem Referenzbereich.")
        elif hct_percent > hi:
            st.warning("Hct liegt über dem Referenzbereich.")
        else:
            st.success("Hct liegt im Referenzbereich.")

if submitted:
    if rbc <= 0 or mcv <= 0:
        st.error("Bitte gültige Werte eingeben: RBC und MCV müssen > 0 sein.")
        st.stop()


    # ---- GRAFIK (auch innerhalb von submitted!) ----
    st.subheader("Einordnung")
    fig, ax = plt.subplots(figsize=(7, 1.6))

    xmin, xmax = 32.0, 55.0

    if lo is not None and hi is not None:
     ax.axvspan(lo, hi, alpha=0.2)

    ax.set_xlim(xmin, xmax)
    ax.set_xticks(range(32, 55, 2))
    ax.set_yticks([])
    ax.set_xlabel("Hct (%)")

    ax.axvline(hct_percent, linewidth=3)
    ax.text(
        hct_percent, 0.6, f"{hct_percent:.1f} %",
        transform=ax.get_xaxis_transform(),
        ha="left", va="center"
    )

    st.pyplot(fig)
    plt.close(fig)

st.markdown("Hämatokritwerte unter 32% sowie über 55% sind nicht mit dem Leben zu vereinbaren und werden nicht mehr in der Grafik angezeigt.")

    