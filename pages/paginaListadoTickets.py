import streamlit as st
import login as login
from bd import query_to_df

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)
if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Listado de Tickets]')
    
    df_Listado_Tickets = query_to_df("SELECT * FROM viewinfotickets;")
    
    st.markdown("""
    > ## Tabla con el Listado de Tickets       
    """)
    
    st.dataframe(df_Listado_Tickets)