import streamlit as st
import login as login
from bd import query_to_df, update_proyecto

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)
if 'correo_electronico' in st.session_state:

    st.subheader('Información | :orange[Edición de Proyectos]')
    
    df_Listado_Proyectos = query_to_df("SELECT * FROM info_proyecto WHERE activo = 'S';")

    nombres_proyectos = df_Listado_Proyectos["nombre_proyecto"].tolist()

    proyecto_seleccionado = st.selectbox("Selecciona un proyecto para editar:", nombres_proyectos)

    # Obtener el ID del proyecto seleccionado
    id_proyecto_seleccionado = df_Listado_Proyectos.loc[
        df_Listado_Proyectos["nombre_proyecto"] == proyecto_seleccionado, "id_proyecto"
    ].values[0]

    # Crear el formulario para edición
    with st.form(key="form_edicion_proyecto"):
        nuevo_nombre = st.text_input("Nuevo nombre del proyecto:", value=proyecto_seleccionado)
        submit_button = st.form_submit_button("Actualizar proyecto")

    if submit_button:
        # Actualizar el proyecto
        update_proyecto(int(id_proyecto_seleccionado), str(nuevo_nombre))
        st.success("Proyecto actualizado correctamente.")