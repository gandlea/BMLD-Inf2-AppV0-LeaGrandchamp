import streamlit as st
import pandas as pd

# --- NEW CODE: initialize empty data frame if not already present ---
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = pd.DataFrame()
# --- END OF NEW CODE ---

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/Rechner.py", title="Rechner", icon=":material/info:")

pg = st.navigation([pg_home, pg_second])
pg.run()
