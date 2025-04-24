import streamlit as st
import login as login
from bd import query_to_df, update_asunto_ticket

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)
if 'correo_electronico' in st.session_state:

    st.subheader('Información | :orange[Edición de Categoría de Ticket]')
    
    df_Listado_AsuntosTickets = query_to_df("SELECT * FROM asunto_ticket WHERE activo = 'S';")

    nombres_asuntos = df_Listado_AsuntosTickets["descripcion_asunto"].tolist()

    asunto_seleccionado = st.selectbox("Selecciona una categoría para editar:", nombres_asuntos)

    # Obtener el ID de la categoría seleccionada
    id_asunto_seleccionado = df_Listado_AsuntosTickets.loc[
        df_Listado_AsuntosTickets["descripcion_asunto"] == asunto_seleccionado, "id_asunto_ticket"
    ].values[0]

    # Crear el formulario para edición
    with st.form(key="form_edicion_asunto_ticket"):
        nuevo_nombre = st.text_input("Nuevo nombre de la categoría:", value=asunto_seleccionado)
        submit_button = st.form_submit_button("Actualizar categoría")

    if submit_button:
        # Actualizar la categoría
        update_asunto_ticket(int(id_asunto_seleccionado), str(nuevo_nombre))
        st.success("Categoría actualizada correctamente.")