import streamlit as st
import login as login
import datetime
from datetime import datetime
import re
from bd import query_to_df, detalle_ticket, update_asignar_ticket

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Asignación de Tickets]')
    
    # Obtener usuarios
    
    query_Tickets = """
        SELECT * 
        FROM info_ticket
        ORDER BY id_ticket DESC;
    """
    
    tickets_df = query_to_df(query_Tickets)
    numero_Ticket = tickets_df["id_ticket"].tolist()
    
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

    obtener_Usuarios_Soporte = usuarios_df.loc[
        usuarios_df["id_rol"].isin([3, 4]), ["id_usuario", "nombre_completo"]
    ].sort_values(by="nombre_completo", ascending=True)

    nombres_usuarios = obtener_Usuarios_Soporte["nombre_completo"].tolist()
    
    usuario_soporte = st.session_state["correo_electronico"]

    # Obtener el ID del usuario seleccionado
    id_usuario_soporte_actual = usuarios_df.loc[
        usuarios_df["correo_electronico"] == usuario_soporte, "id_usuario"
    ].values[0]
    
    # Mostrar tabla editable
    st.title("📋 Explorador de Tickets")
    st.markdown("""> ## Selecciona un ticket y haz clic en 'Ver Detalle' para ver más información.""")
        
    # Mostrar DataFrame con selección de fila
    selected = st.dataframe(tickets_df[["identificador", "fecha_creacion", "nombre_completo", "nombre_proyecto", "descripcion_asunto", "descripcion_ticket"]].sort_values(by="identificador", ascending=False), on_select="rerun", selection_mode=["single-row"], use_container_width=True)

    # Validar si hay selección
    if len(selected.selection.rows) > 0:
        
        indice_ticket = selected.selection.rows[0]  # Captura el índice del usuario seleccionado

        # Botón para ver detalles del usuario seleccionado
        if st.button(f"🔍 Ver detalle de #ID({tickets_df.iloc[indice_ticket]['identificador']}) - Asunto: ({tickets_df.iloc[indice_ticket]['descripcion_asunto']})"):
            
            # Llamar a la función de detalles
            detalle_ticket(dataFrame=tickets_df, indice_ticket=indice_ticket)
            
        st.markdown("""> ### Por favor seleccione el usuario al que va a asignarle el ticket.""")

        usuario_Soporte_Seleccionado = st.selectbox("Seleccione un usuario para asignar:", nombres_usuarios)
        
        # Obtener el ID del asunto seleccionado
        id_Usuario_Soporte_Seleccionado = usuarios_df.loc[
            usuarios_df["nombre_completo"] == usuario_Soporte_Seleccionado, "id_usuario"
        ].values[0]

        #observiones_Respuesta_Ticket = st.text_input(label="s", label_visibility="hidden", placeholder="Digite las observaciones...", max_chars=1000)
        
        if usuario_Soporte_Seleccionado:

            print("hola")

            if st.button(f"✅ Asignar Ticket #ID({tickets_df.iloc[indice_ticket]['identificador']}) - A: ({usuario_Soporte_Seleccionado})"):
                
                update_asignar_ticket(
                    id_ticket=int(tickets_df.iloc[indice_ticket]["identificador"]),
                    id_usuario_soporte=int(id_Usuario_Soporte_Seleccionado)
                )

                st.success(f"El Ticket #ID{int(tickets_df.iloc[indice_ticket]["identificador"])} ha sido asignado a: {usuario_Soporte_Seleccionado} correctamente.")
                
        else:
            
            st.error("Por favor describa las observaciones de respuesta del Ticket.")
    
    else:
        
        st.error("Por favor seleccione un Ticket.")