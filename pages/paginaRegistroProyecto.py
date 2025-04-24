import streamlit as st
import login as login
from bd import create_proyecto

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Formulario de Registro de Proyecto]')
    
    nombre_proyecto = st.text_input("Nombre del Proyecto")

    if st.button("Agregar Proyecto"):
        if nombre_proyecto:
            create_proyecto(nombre_proyecto)
            st.success("Proyecto agregado exitosamente.")
        else:
            st.error("Por favor ingrese el nombre del proyecto.")