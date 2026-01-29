import streamlit as st
import login as login
import streamlit.components.v1 as components
from streamlit.components.v1 import html

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Tablero de Power BI - SGI-GH Q+]')
    
    components.html("""
        <iframe title="dashboard_EX_VF" width="1750" height="1060" src="https://app.powerbi.com/reportEmbed?reportId=02599841-3188-48ad-8c94-00f2a351212f&autoAuth=true&ctid=fa1e9b00-008a-412d-bc71-ae528086a852" frameborder="0" allowFullScreen="true"></iframe>
    """, height=1060)