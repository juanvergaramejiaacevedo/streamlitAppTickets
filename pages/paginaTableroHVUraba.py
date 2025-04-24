import streamlit as st
import login as login
import streamlit.components.v1 as components
from streamlit.components.v1 import html

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Tablero de Power BI - HV Urabá]')
    
    components.html("""
        <iframe title="ensayo hv URABA" width="1750" height="1060" src="https://app.powerbi.com/view?r=eyJrIjoiYmI1MWZjMzMtODg5NC00ODdiLWFjZDktY2JhZTAxOGEzNTc1IiwidCI6ImZhMWU5YjAwLTAwOGEtNDEyZC1iYzcxLWFlNTI4MDg2YTg1MiJ9" frameborder="0" allowFullScreen="true"></iframe>
    """, height=1060)