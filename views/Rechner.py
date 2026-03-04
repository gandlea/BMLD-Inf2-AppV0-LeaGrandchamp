import streamlit as st
from functions.addition import hct_rechner

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