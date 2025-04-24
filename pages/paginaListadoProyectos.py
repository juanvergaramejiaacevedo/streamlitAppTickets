import streamlit as st
import login as login
from bd import query_to_df

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)
#st.header('Página :orange[principal]')
if 'correo_electronico' in st.session_state:
    #st.header('Página :orange[principal]')
    st.subheader('Información | :orange[Listado de Proyectos]')
    
    df_Listado_Proyectos = query_to_df("SELECT * FROM info_proyecto WHERE activo = 'S';")
    
    st.markdown("""
    > ## Tabla con el Listado de Proyectos            
    """)
    
    st.dataframe(df_Listado_Proyectos)
    
    