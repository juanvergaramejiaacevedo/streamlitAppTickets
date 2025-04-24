import streamlit as st
import login as login
from bd import query_to_df, delete_proyecto

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)
if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Eliminación de Proyectos]')

    df_Listado_Proyectos = query_to_df("SELECT * FROM info_proyecto WHERE activo = 'S';")

    nombres_proyectos = df_Listado_Proyectos["nombre_proyecto"].tolist()

    proyecto_seleccionado = st.selectbox("Selecciona un proyecto para eliminar:", nombres_proyectos)

    # Obtener el ID del proyecto seleccionado
    id_proyecto_seleccionado = df_Listado_Proyectos.loc[
        df_Listado_Proyectos["nombre_proyecto"] == proyecto_seleccionado, "id_proyecto"
    ].values[0]

    if st.button("Eliminar proyecto"):
        delete_proyecto(int(id_proyecto_seleccionado))
        st.success(f"El proyecto '{proyecto_seleccionado}' ha sido eliminado correctamente.")