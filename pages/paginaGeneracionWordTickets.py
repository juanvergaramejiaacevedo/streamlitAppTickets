import streamlit as st
import login as login
import datetime
import re
import time
import io
from docxtpl import DocxTemplate
from bd import query_to_df

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Registro de Observaciones de Tickets]')

    query_Tickets = """
        SELECT *
        FROM viewanalyticsword
        ORDER BY identificador DESC;
    """
        
    tickets_df = query_to_df(query_Tickets)
    numero_Ticket = tickets_df["identificador"].tolist()
        
    # Mostrar tabla editable
    st.title("📋 Explorador de Tickets")
            
    # Mostrar DataFrame con selección de fila
    selected = st.dataframe(tickets_df[["identificador", "fecha_creacion", "nombre_asunto", "descripcion_ticket", "nombre_usuario", "correo_usuario", "celular_usuario", "documento_usuario", "proyecto_usuario", "fecha_atencion", "observaciones_ticket", "nombre_tecnico", "correo_tecnico", "celular_tecnico", "documento_tecnico", "rol_atendido_por"]].sort_values(by="identificador", ascending=False), on_select="rerun", selection_mode=["single-row"], use_container_width=True)

        # Validar si hay selección
    if len(selected.selection.rows) > 0:
            
        indice_ticket = selected.selection.rows[0]  # Captura el índice del usuario seleccionado

        numero_Celular_Usuario = tickets_df.iloc[indice_ticket]["celular_usuario"]

        correo_Electronico_Usuario = tickets_df.iloc[indice_ticket]["correo_usuario"]

        st.markdown(f"### Indice del Ticket Seleccionado: {indice_ticket}")

        st.markdown(f"### Detalles del Ticket Seleccionado: #ID({tickets_df.iloc[indice_ticket]['identificador']})")

        var_Identificador_Ticket = tickets_df.iloc[indice_ticket]["identificador"]

        try:

            context = {
                "nombre_Usuario": tickets_df.iloc[indice_ticket]["nombre_usuario"],
                "correo_Usuario": tickets_df.iloc[indice_ticket]["correo_usuario"],
                "celular_Usuario": tickets_df.iloc[indice_ticket]["celular_usuario"],
                "documento_Usuario": tickets_df.iloc[indice_ticket]["documento_usuario"],
                "proyecto_Usuario": tickets_df.iloc[indice_ticket]["proyecto_usuario"],
                "nombre_Tecnico": tickets_df.iloc[indice_ticket]["nombre_tecnico"],
                "correo_Tecnico": tickets_df.iloc[indice_ticket]["correo_tecnico"],
                "celular_Tecnico": tickets_df.iloc[indice_ticket]["celular_tecnico"],
                "documento_Tecnico": tickets_df.iloc[indice_ticket]["documento_tecnico"],
                "rol_Tecnico": tickets_df.iloc[indice_ticket]["rol_atendido_por"],
                "nombre_Asunto": tickets_df.iloc[indice_ticket]["nombre_asunto"],
                "descripcion_Ticket": tickets_df.iloc[indice_ticket]["descripcion_ticket"],
                "fecha_Creacion": tickets_df.iloc[indice_ticket]["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S"),
                "fecha_Atencion": tickets_df.iloc[indice_ticket]["fecha_atencion"].strftime("%Y-%m-%d %H:%M:%S"),
                "observaciones_Ticket": tickets_df.iloc[indice_ticket]["observaciones_ticket"]
            }
                    
                    
            # Cargar la plantilla de Word y renderizarla con el contexto
            doc = DocxTemplate("templates/templateTicket.docx")
            doc.render(context)
                    
            # Guardar el documento en un buffer en memoria
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
                
            boton_Descargar = st.download_button(
                label="Descargar Documento",
                data=buffer,
                file_name="documentoAutomatizado.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

            st.link_button("Enviar WhatsApp", f"https://wa.me/57{numero_Celular_Usuario}")

            st.link_button("Enviar Email", f"mailto:{correo_Electronico_Usuario}")

            if boton_Descargar:
                st.success("Documento descargado exitosamente.")


            else:

                st.warning("Presione el botón para descargar el documento.")

        
        except Exception as e:
                
                st.error(f"Error al generar el documento: {e}")
        
    else:
            
        st.error("Por favor seleccione un Ticket.")