import streamlit as st
import login as login
import datetime
import re
import time
from streamlit.runtime.fragment import fragment
from bd import query_to_df, create_observation_ticket, detalle_crear_observacion_ticket

archivo = __file__.split("\\")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Registro de Observaciones de Tickets]')

    usuario_Tickets = st.session_state["correo_electronico"]

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

    id_usuario = usuarios_df.loc[
        usuarios_df["correo_electronico"] == usuario_Tickets, "id_usuario"
    ].values[0]

    query_Tickets = f"""
        SELECT inftic.id_ticket AS identificador,
        infusr.nombre_completo AS nombre_usuario,
        infusr.numero_celular AS celular_usuario,
        infusr.correo_electronico AS correo_usuario,
        infusr.numero_documento AS documento_usuario,
        infpry.nombre_proyecto AS proyecto_usuario,
        asntic.descripcion_asunto,
        inftic.descripcion_ticket,
        inftic.fecha_creacion,
        inftic.fecha_atencion,
        inftic.estado,
        inftic.observaciones_respuesta AS observaciones_ticket,
        infusr2.nombre_completo AS nombre_tecnico,
        infusr2.correo_electronico AS correo_tecnico,
        infusr2.numero_celular AS celular_tecnico,
        infrol.nombre_rol AS rol_atendido_por
        FROM info_ticket inftic
        JOIN info_usuario infusr ON inftic.id_usuario = infusr.id_usuario
        LEFT JOIN info_usuario infusr2 ON inftic.id_usuario_asignado = infusr2.id_usuario
        LEFT JOIN info_roles infrol ON infusr2.id_rol = infrol.id_rol
        JOIN asunto_ticket asntic ON inftic.id_asunto_ticket = asntic.id_asunto_ticket
        JOIN info_proyecto infpry ON infusr.id_proyecto = infpry.id_proyecto
        WHERE inftic.activo = 'S' AND infusr2.correo_electronico = '{usuario_Tickets}'
        ORDER BY inftic.fecha_creacion DESC
    """

    #AND infusr2.correo_electronico = '{usuario_Tickets}'
        
    tickets_df = query_to_df(query_Tickets)

    numero_Ticket = tickets_df["identificador"].tolist()
        
    # Mostrar tabla editable
    st.title("📋 Explorador de Tickets")
            
    # Mostrar DataFrame con selección de fila
    selected = st.dataframe(tickets_df[["identificador", "fecha_creacion", "descripcion_asunto", "descripcion_ticket", "nombre_usuario", "correo_usuario", "celular_usuario", "documento_usuario", "proyecto_usuario", "fecha_atencion", "observaciones_ticket", "nombre_tecnico", "correo_tecnico", "celular_tecnico", "rol_atendido_por"]].sort_values(by="identificador", ascending=False), on_select="rerun", selection_mode=["single-row"], use_container_width=True)

    # Validar si hay selección
    if len(selected.selection.rows) > 0:
            
        indice_ticket = selected.selection.rows[0]  # Captura el índice del usuario seleccionado

        numero_Celular_Usuario = tickets_df.iloc[indice_ticket]["celular_usuario"]

        correo_Electronico_Usuario = tickets_df.iloc[indice_ticket]["correo_usuario"]

        var_Identificador_Ticket = tickets_df.iloc[indice_ticket]["identificador"]

        query_Observaciones = f"""
            SELECT obstk.id_ticket,
            obstk.id_observacion,
            infusr.nombre_completo AS nombre_usuario,
            infusr.correo_electronico,
            infrol.nombre_rol AS rol_usuario,
            obstk.fecha_observacion,
            obstk.contenido
            FROM observaciones_ticket obstk
            INNER JOIN info_usuario infusr ON obstk.id_usuario = infusr.id_usuario
            LEFT JOIN info_roles infrol ON infusr.id_rol = infrol.id_rol
            WHERE infusr.correo_electronico = '{usuario_Tickets}'
        """

        df_Observaciones = query_to_df(query_Observaciones)

        df_Observaciones = df_Observaciones[df_Observaciones["id_ticket"] == var_Identificador_Ticket]

        if not df_Observaciones.empty:

            st.success("Se encontraron observaciones para el Ticket Seleccionado.")
            
            for index, row in df_Observaciones.iterrows():
                st.markdown("---")
                #st.markdown(f"**Observación ID:** {row['id_observacion']}")
                st.markdown(f"**Nombre Usuario:** {row['nombre_usuario']}")
                #st.markdown(f"**Rol Usuario:** {row['rol_usuario']}")
                st.markdown(f"**Fecha:** {row['fecha_observacion']}")
                st.markdown(f"**Contenido:** {row['contenido']}")
                st.markdown("---")

            with st.form(key="formulario_observacion", clear_on_submit=True):
                contenido_observacion = st.text_area("Ingrese el contenido de la observación:")
                submit_button = st.form_submit_button("Agregar Observación")

                if submit_button and contenido_observacion:
                    try:
                        create_observation_ticket(id_ticket=int(var_Identificador_Ticket), id_usuario=int(id_usuario), contenido=contenido_observacion)
                        st.success("Observación registrada correctamente.")
                        detalle_crear_observacion_ticket(var_Identificador_Ticket=int(var_Identificador_Ticket), id_usuario=int(id_usuario), contenido_observacion=contenido_observacion)
                        time.sleep(5)
                        st.rerun(scope="app")
                    except Exception as e:
                        st.error(f"Error al registrar la observación: {e}. Por favor, inténtalo de nuevo.")

        else:

            st.warning("No se encontraron observaciones para el Ticket Seleccionado.")
                
            with st.form(key="formulario_observacion", clear_on_submit=True):
                contenido_observacion = st.text_area("Ingrese el contenido de la observación:")
                submit_button = st.form_submit_button("Agregar Observación")

                if submit_button and contenido_observacion:
                    try:
                        create_observation_ticket(id_ticket=int(var_Identificador_Ticket), id_usuario=int(id_usuario), contenido=contenido_observacion)
                        st.success("Observación registrada correctamente.")
                        detalle_crear_observacion_ticket(var_Identificador_Ticket=int(var_Identificador_Ticket), id_usuario=int(id_usuario), contenido_observacion=contenido_observacion)
                        time.sleep(5)
                        st.rerun(scope="app")
                    except Exception as e:
                        st.error(f"Error al registrar la observación: {e}. Por favor, inténtalo de nuevo.")

    else:
            
        st.error("Por favor seleccione un Ticket.")