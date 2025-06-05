import streamlit as st
import login as login
import datetime
from datetime import datetime
import re
from bd import query_to_df, detalle_ticket, update_estado_ticket, detalle_cambio_estado_ticket

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Cambio de Estado de Ticket]')
    
    # Obtener usuarios
    
    query_Tickets = """
        SELECT * 
        FROM viewinfocambioestadotickets
        ORDER BY identificador DESC;
    """
    
    tickets_df = query_to_df(query_Tickets)

    #id_usuario = st.session_state.get("id_usuario", None)
    #if id_usuario is not None:
        #tickets_df = tickets_df[tickets_df["id_usuario_asignado"] == id_usuario]

    #numero_Ticket = tickets_df["identificador"].tolist()
    
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
    
    usuario_soporte = st.session_state["correo_electronico"]

    # Obtener el ID del usuario seleccionado
    id_usuario_soporte_actual = usuarios_df.loc[
        usuarios_df["correo_electronico"] == usuario_soporte, "id_usuario"
    ].values[0]

    tickets_df = tickets_df[tickets_df["id_usuario_asignado"] == id_usuario_soporte_actual]

    numero_Ticket = tickets_df["identificador"].tolist()
    
    st.markdown(f"""> ### Usuario Soporte: {usuario_soporte} | ID Usuario: {id_usuario_soporte_actual}""")
    
    # Markdown para Mencionar que es la Cabecera del DataFrame
    #st.markdown("""> ## Listado de Tickets""")
    
    # Mostrar tabla
    #st.dataframe(tickets_df[["nombre_completo", "correo_electronico", "nombre_proyecto", "descripcion_asunto", "descripcion_ticket"]], use_container_width=True)

    # Mostrar tabla editable
    st.title("📋 Explorador de Tickets")
    st.markdown("""> ## Selecciona un ticket y haz clic en 'Ver Detalle' para ver más información.""")
        
    # Mostrar DataFrame con selección de fila
    selected = st.dataframe(tickets_df[["identificador", "fecha_creacion", "numero_celular", "nombre_completo", "nombre_proyecto", "descripcion_asunto", "descripcion_ticket"]].sort_values(by="identificador", ascending=False), on_select="rerun", selection_mode=["single-row"], use_container_width=True)

    # Validar si hay selección
    if len(selected.selection.rows) > 0:
        
        indice_ticket = selected.selection.rows[0]  # Captura el índice del usuario seleccionado

        # Botón para ver detalles del usuario seleccionado
        if st.button(f"🔍 Ver detalle de #ID({tickets_df.iloc[indice_ticket]['identificador']}) - Asunto: ({tickets_df.iloc[indice_ticket]['descripcion_asunto']})"):
            
            # Llamar a la función de detalles
            detalle_ticket(dataFrame=tickets_df, indice_ticket=indice_ticket)
            
        st.markdown("""> ### Por favor digite las observaciones de la solución del ticket.""")
        
        observiones_Respuesta_Ticket = st.text_input(label="s", label_visibility="hidden", placeholder="Digite las observaciones...", max_chars=1000)
        
        if len(observiones_Respuesta_Ticket) > 0:
            
            if st.button(f"✅ Cambiar de Estado el Ticket #ID({tickets_df.iloc[indice_ticket]['identificador']}) - Asunto: ({tickets_df.iloc[indice_ticket]['descripcion_asunto']})"):
                
                update_estado_ticket(
                    id_ticket=int(tickets_df.iloc[indice_ticket]["identificador"]),
                    nuevo_estado="Resuelto",
                    fecha_soporte=datetime.now(),
                    observaciones_respuesta=observiones_Respuesta_Ticket,
                    id_usuario_soporte=int(id_usuario_soporte_actual)
                )
                
                detalle_cambio_estado_ticket(dataFrame=tickets_df, indice_ticket=indice_ticket)
                    
                #st.switch_page("inicio.py")
                
        else:
            
            st.error("Por favor describa las observaciones de respuesta del Ticket.")
    
    else:
        
        st.error("Por favor seleccione un Ticket.")

    #ticket_Seleccionado = st.selectbox("Seleccione un Ticket:", numero_Ticket)
    
    