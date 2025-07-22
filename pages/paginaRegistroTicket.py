import streamlit as st
import login as login
import re
from bd import query_to_df, create_ticket

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Registro de Ticket]')
    
    # Obtener el correo electrónico del usuario actual desde la sesión
    usuario_Actual = st.session_state['correo_electronico']

    query_Usuarios = """
        SELECT * 
        FROM info_usuario infusr 
        INNER JOIN tipos_documento tdc ON 
            tdc.id_tipo_documento = infusr.id_tipo_documento
        INNER JOIN info_proyecto infpry ON
            infpry.id_proyecto = infusr.id_proyecto
        INNER JOIN info_roles infrol ON
            infrol.id_rol = infusr.id_rol
        WHERE infusr.activo = 'S';
    """

    usuarios_df = query_to_df(query_Usuarios)

    # Obtener el ID del usuario actual basado en su correo electrónico
    id_usuario = usuarios_df.loc[
        usuarios_df["correo_electronico"] == usuario_Actual, "id_usuario"
    ].values[0]

    with st.form("formulario_ticket"):

        st.text_input("Correo electrónico:", value=usuario_Actual, disabled=True)

        # Seleccionar el asunto del ticket
        asuntos_tickets_df = query_to_df("SELECT * FROM asunto_ticket WHERE activo = 'S' ORDER BY asunto_ticket DESC;")
        
        descripciones_asuntos = asuntos_tickets_df["descripcion_asunto"].tolist()
        
        asunto_seleccionado = st.selectbox(
            "Selecciona el asunto del ticket:",
            descripciones_asuntos
        )

        id_asunto_ticket = asuntos_tickets_df.loc[
            asuntos_tickets_df["descripcion_asunto"] == asunto_seleccionado, "id_asunto_ticket"
        ].values[0]

        # Seleccionar la prioridad del ticket
        prioridades_ticket_df = query_to_df("SELECT * FROM prioridades_ticket WHERE activo = 'S';")
        
        descripciones_prioridades = prioridades_ticket_df["tipo_prioridad"].tolist()
        
        prioridad_seleccionada = st.selectbox(
            "Selecciona la prioridad del ticket:",
            descripciones_prioridades
        )
        
        id_prioridad_ticket = prioridades_ticket_df.loc[
            prioridades_ticket_df["tipo_prioridad"] == prioridad_seleccionada, "id_prioridad"
        ].values[0]

        # Campo para la descripción del ticket
        descripcion_ticket = st.text_area("Describe el problema o solicitud:", placeholder="Escribe aquí los detalles del ticket...")

        # Botón para registrar el ticket
        boton_Enviar = st.form_submit_button("Crear Ticket")
    
    if boton_Enviar:

        if descripcion_ticket.strip():

            st.success("✅ Ticket creado exitosamente.")

            create_ticket(int(id_usuario), int(id_asunto_ticket), descripcion_ticket, int(id_prioridad_ticket))

        else:
        
            st.error("❌ Por favor, proporciona una descripción para el ticket.")
