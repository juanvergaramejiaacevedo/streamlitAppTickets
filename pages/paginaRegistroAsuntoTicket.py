import streamlit as st
import login as login
from bd import create_asunto_ticket

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Formulario de Registro de Categoría de Tickets]')
    
    descripcion_asunto = st.text_input("Nombre de la Categoría")

    if st.button("Agregar Categoría"):
        if descripcion_asunto:
            create_asunto_ticket(descripcion_asunto)
            st.success("Categoría agregada exitosamente.")
        else:
            st.error("Por favor ingrese el nombre de la categoría.")