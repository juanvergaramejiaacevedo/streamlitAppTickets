import streamlit as st
import login as login
from bd import query_to_df, delete_asunto_ticket

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)
if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Eliminación de Categoría de Ticket]')

    df_Listado_AsuntosTickets = query_to_df("SELECT * FROM asunto_ticket WHERE activo = 'S';")

    nombres_asuntos = df_Listado_AsuntosTickets["descripcion_asunto"].tolist()

    asunto_seleccionado = st.selectbox("Selecciona una categoría para eliminar:", nombres_asuntos)

    # Obtener el ID del asunto seleccionado
    id_asunto_seleccionado = df_Listado_AsuntosTickets.loc[
        df_Listado_AsuntosTickets["descripcion_asunto"] == asunto_seleccionado, "id_asunto_ticket"
    ].values[0]

    if st.button("Eliminar categoría"):
        delete_asunto_ticket(int(id_asunto_seleccionado))
        st.success(f"La categoría '{asunto_seleccionado}' ha sido eliminada correctamente.")