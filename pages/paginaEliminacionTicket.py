import streamlit as st
import login as login
from bd import query_to_df, delete_ticket

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)
if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Eliminación de Ticket]')

    # Obtener listado de tickets activos
    df_Listado_Tickets = query_to_df("""
        SELECT inftic.id_ticket,
        inftic.descripcion_ticket,
        inftic.fecha_creacion,
        inftic.estado,
        infusr.nombre_completo,
        infusr.correo_electronico,
        asntic.descripcion_asunto
        FROM info_ticket inftic
        INNER JOIN info_usuario infusr ON
            inftic.id_usuario = infusr.id_usuario
        INNER JOIN asunto_ticket asntic ON
            inftic.id_asunto_ticket = asntic.id_asunto_ticket
        WHERE inftic.activo = 'S';
    """)
    
    ids_tickets = df_Listado_Tickets["id_ticket"].tolist()

    # Seleccionar ticket
    id_ticket_seleccionado = st.selectbox("Selecciona un ticket:", ids_tickets)

    # Obtener detalles del ticket seleccionado
    ticket_detalle = df_Listado_Tickets.loc[
        df_Listado_Tickets["id_ticket"] == id_ticket_seleccionado
    ]

    # Botón para ver detalle del ticket (usando un expander como "modal")
    with st.expander("🔍 Ver detalle del ticket"):
        st.write(f"**:red[ID del Ticket]:** {ticket_detalle['id_ticket'].values[0]}")
        st.write(f"**:red[Creador]:** {ticket_detalle['nombre_completo'].values[0]} ({ticket_detalle['correo_electronico'].values[0]})")
        st.write(f"**:red[Descripción Ticket]:** {ticket_detalle['descripcion_ticket'].values[0]}")
        st.write(f"**:red[Descripción Asunto]:** {ticket_detalle['descripcion_asunto'].values[0]}")
        st.write(f"**:red[Fecha de Creación]:** {ticket_detalle['fecha_creacion'].values[0]}")
        st.write(f"**:red[Estado]:** {ticket_detalle['estado'].values[0]}")
        # Agrega otros detalles que quieras mostrar

    # Botón para eliminar el ticket
    if st.button("Eliminar ticket"):
        delete_ticket(int(id_ticket_seleccionado))
        st.success(f"El ticket '{id_ticket_seleccionado}' ha sido eliminado correctamente.")