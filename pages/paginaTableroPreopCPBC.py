import streamlit as st
import login as login
import streamlit.components.v1 as components
from streamlit.components.v1 import html

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Tablero de Power BI - App Preoperacionales Control Pérdidas Bolívar Centro e ISVIMED]')
    
    components.html("""
        <iframe title="dashboard_CPBC_ISV_VF" width="1750" height="1060" src="https://app.powerbi.com/view?r=eyJrIjoiZDBlMzA3ZWYtODQyNy00MGE3LTg0NzUtMzU1NmFlNmU0MWRkIiwidCI6ImZhMWU5YjAwLTAwOGEtNDEyZC1iYzcxLWFlNTI4MDg2YTg1MiJ9&pageName=652e28b69898452bab3e" frameborder="0" allowFullScreen="true"></iframe>
    """, height=1060)