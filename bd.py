import pandas as pd
import os
import streamlit as st
import datetime as dt
import psycopg2
from sqlalchemy import create_engine, text
from configparser import ConfigParser

DB_USERNAME=st.secrets.database.DB_USERNAME
DB_PASSWORD=st.secrets.database.DB_PASSWORD
DB_URL=st.secrets.database.DB_URL
DB_PORT=st.secrets.database.DB_PORT
DB_NAME=st.secrets.database.DB_NAME

# Definición de la función para obtener la cadena de conexión a la base de datos
def get_engine():
    return create_engine(f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}:{int(DB_PORT)}/{DB_NAME}')

# Función para ejecutar consultas y devolver resultados en un DataFrame usando SQLAlchemy
def query_to_df(query, params=None):
    engine = get_engine()
    # Utilizamos un bloque "with" para asegurar el cierre de la conexión
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params=params)
    return df

def execute_query(query, params=None):
    engine = get_engine()
    # Usamos engine.begin() para manejar la transacción automáticamente
    with engine.begin() as connection:
        # La función text() es necesaria para construir una consulta SQL al estilo SQLAlchemy.
        connection.execute(text(query), params or {})
        
        
# Funciones CRUD para las tablas

# CRUD para proyectos
def get_proyectos():
    return query_to_df("SELECT * FROM info_proyecto WHERE activo = 'S';")
    
def create_proyecto(nombre_proyecto):
    query = "INSERT INTO info_proyecto (nombre_proyecto) VALUES (:nombre_proyecto)"
    execute_query(query, {"nombre_proyecto": nombre_proyecto})

def update_proyecto(id_proyecto, nuevo_nombre):
    query = "UPDATE info_proyecto SET nombre_proyecto = :nuevo_nombre WHERE id_proyecto = :id_proyecto"
    execute_query(query, {"nuevo_nombre": nuevo_nombre, "id_proyecto": id_proyecto})

def delete_proyecto(id_proyecto):
    query = "UPDATE info_proyecto SET activo = 'N' WHERE id_proyecto = :id_proyecto"
    execute_query(query, {"id_proyecto": id_proyecto})



# CRUD para usuarios
def get_usuarios():
    return query_to_df("SELECT * FROM info_usuario WHERE activo='S';")

def create_usuario(nombre_completo, numero_celular, correo_electronico, numero_documento, id_tipo_documento, id_proyecto, id_rol):
    query = "INSERT INTO info_usuario (nombre_completo, numero_celular, correo_electronico, numero_documento, id_tipo_documento, id_proyecto, id_rol) VALUES (:nombre_completo, :numero_celular, :correo_electronico, :numero_documento, :id_tipo_documento, :id_proyecto, :id_rol)"
    execute_query(query,{"nombre_completo": nombre_completo, "numero_celular": numero_celular, "correo_electronico": correo_electronico, "numero_documento": numero_documento, "id_tipo_documento": id_tipo_documento, "id_proyecto": id_proyecto, "id_rol": id_rol})

def update_usuario(id_usuario, nuevo_nombre_completo, nuevo_numero_celular, nuevo_correo_electronico, nuevo_numero_documento, nuevo_id_tipo_documento, nuevo_id_proyecto, nuevo_id_rol):
    query= "UPDATE info_usuario SET nombre_completo = :nuevo_nombre_completo, numero_celular = :nuevo_numero_celular, correo_electronico = :nuevo_correo_electronico, numero_documento = :nuevo_numero_documento, id_tipo_documento = :nuevo_id_tipo_documento, id_proyecto = :nuevo_id_proyecto, id_rol = :nuevo_id_rol WHERE id_usuario = :id_usuario"
    execute_query(query, {"nuevo_nombre_completo": nuevo_nombre_completo, "nuevo_numero_celular": nuevo_numero_celular, "nuevo_correo_electronico": nuevo_correo_electronico, "nuevo_numero_documento": nuevo_numero_documento, "nuevo_id_tipo_documento": nuevo_id_tipo_documento, "nuevo_id_proyecto": nuevo_id_proyecto, "nuevo_id_rol": nuevo_id_rol, "id_usuario": id_usuario})

def delete_usuario(id_usuario):
    query = "UPDATE info_usuario SET activo = 'N' WHERE id_usuario = :id_usuario"
    execute_query(query, {"id_usuario": id_usuario})



# CRUD para asuntos de tickets
def get_asuntos():
    return query_to_df("SELECT * FROM asunto_ticket WHERE activo = 'S';")

def create_asunto_ticket(descripcion_asunto):
    query = "INSERT INTO asunto_ticket (descripcion_asunto) VALUES (:descripcion_asunto)"
    execute_query(query, {"descripcion_asunto": descripcion_asunto})

def update_asunto_ticket(id_asunto_ticket, nueva_descripcion):
    query = "UPDATE asunto_ticket SET descripcion_asunto = :nueva_descripcion WHERE id_asunto_ticket = :id_asunto_ticket"
    execute_query(query, {"nueva_descripcion": nueva_descripcion, "id_asunto_ticket": id_asunto_ticket})

def delete_asunto_ticket(id_asunto_ticket):
    query = "UPDATE asunto_ticket SET activo = 'N' WHERE id_asunto_ticket = :id_asunto_ticket"
    execute_query(query, {"id_asunto_ticket": id_asunto_ticket})



# CRUD para tickets
def get_tickets():
    return query_to_df("SELECT * FROM info_ticket")

def create_ticket(id_usuario, id_asunto_ticket, descripcion_ticket):
    query = "INSERT INTO info_ticket (id_usuario, id_asunto_ticket, descripcion_ticket) VALUES (:id_usuario, :id_asunto_ticket, :descripcion_ticket)"
    execute_query(query,{"id_usuario": id_usuario, "id_asunto_ticket": id_asunto_ticket, "descripcion_ticket": descripcion_ticket})

#def update_ticket(id_ticket, id_usuario, id_proyecto, id_asunto_ticket, descripcion_ticket, estado):
#    execute_query("UPDATE info_ticket SET id_usuario = %s, id_proyecto = %s, id_asunto_ticket = %s, descripcion_ticket = %s, estado = %s WHERE id_ticket = %s", 
#                  (id_usuario, id_proyecto, id_asunto_ticket, descripcion_ticket, estado, id_ticket))

def update_asignar_ticket(id_ticket, id_usuario_asignado):
    query = """UPDATE info_ticket 
    SET id_usuario_asignado = :id_usuario_asignado 
    WHERE id_ticket = :id_ticket
    """
    execute_query(query, {
        "id_usuario_asignado": id_usuario_asignado, 
        "id_ticket": id_ticket
    })

def update_estado_ticket(id_ticket, nuevo_estado, fecha_soporte, observaciones_respuesta, id_usuario_soporte):
    query = """
    UPDATE info_ticket
    SET estado = :nuevo_estado, fecha_atencion = :fecha_soporte, observaciones_respuesta = :observaciones_respuesta, id_usuario_soporte = :id_usuario_soporte
    WHERE id_ticket = :id_ticket
    """
    execute_query(query, {
        "nuevo_estado": nuevo_estado,
        "fecha_soporte": fecha_soporte,
        "observaciones_respuesta": observaciones_respuesta,
        "id_usuario_soporte": id_usuario_soporte,
        "id_ticket": id_ticket
    })

def delete_ticket(id_ticket):
    query = "UPDATE info_ticket SET activo = 'N' WHERE id_ticket = :id_ticket"
    execute_query(query, {"id_ticket": id_ticket})
    
    
    
def get_tickets_analytics():
    return query_to_df("""
    SELECT * 
    FROM viewinfotickets inftks
    """)
    
    
def get_tickets_analytics_sopint():
    return query_to_df("""
    SELECT * 
    FROM viewinfotickets inftks
    WHERE inftks.rol_atendido_por = 'SoporteInterno'
    """)
    

def get_tickets_analytics_sopext():
    return query_to_df("""
    SELECT * 
    FROM viewinfotickets inftks
    WHERE inftks.rol_atendido_por = 'SoporteExterno'
    """)
    
    
# Definición del diálogo usando el decorador @st.dialog
@st.dialog("Detalle del Ticket", width="large")
def detalle_ticket(dataFrame: pd.DataFrame, indice_ticket: int):
    """Función que recibe como parámetros el DataFrame y el Índice del Ticket para luego mostrarlos en un modal.

    Args:
        dataFrame (pd.DataFrame): Parámetro con el DataFrame que contiene el listado de Usuarios.
        indice_ticket (int): Parámetro con el índice del dato seleccionado en específico.
    """
    ticket_detalle = dataFrame.iloc[indice_ticket]
    st.write(f"**:blue[Fecha de Creación]:** {ticket_detalle['fecha_creacion']}")
    st.write(f"**:blue[Nombre Creador]:** {ticket_detalle['nombre_completo']}")
    st.write(f"**:blue[Correo Electrónico]:** {ticket_detalle['correo_electronico']}")
    st.write(f"**:blue[Número de Celular]:** {ticket_detalle['numero_celular']}")
    st.write(f"**:blue[Número de Documento]:** {ticket_detalle['numero_documento']}")
    st.write(f"**:blue[Nombre del Proyecto]:** {ticket_detalle['nombre_proyecto']}")
    st.write(f"**:blue[Asunto del Ticket]:** {ticket_detalle['descripcion_asunto']}")
    st.write(f"**:blue[Observaciones]:** {ticket_detalle['descripcion_ticket']}")


# Definición del diálogo usando el decorador @st.dialog
@st.dialog("Cambio de Estado del Ticket", width="large")
def detalle_cambio_estado_ticket(dataFrame: pd.DataFrame, indice_ticket: int):
    """Función que recibe como parámetros el DataFrame y el Índice del Ticket para luego mostrarlos en un modal.

    Args:
        dataFrame (pd.DataFrame): Parámetro con el DataFrame que contiene el listado de Usuarios.
        indice_ticket (int): Parámetro con el índice del dato seleccionado en específico.
    """
    ticket_detalle = dataFrame.iloc[indice_ticket]
    st.success("Se ha cambiado correctamente el estado.")
    
    st.write(f"**:blue[Fecha de Creación]:** {ticket_detalle['fecha_creacion']}")
    st.write(f"**:blue[Nombre Creador]:** {ticket_detalle['nombre_completo']}")
    st.write(f"**:blue[Correo Electrónico]:** {ticket_detalle['correo_electronico']}")
    st.write(f"**:blue[Número de Celular]:** {ticket_detalle['numero_celular']}")
    st.write(f"**:blue[Número de Documento]:** {ticket_detalle['numero_documento']}")
    st.write(f"**:blue[Nombre del Proyecto]:** {ticket_detalle['nombre_proyecto']}")
    st.write(f"**:blue[Asunto del Ticket]:** {ticket_detalle['descripcion_asunto']}")
    st.write(f"**:blue[Observaciones]:** {ticket_detalle['descripcion_ticket']}")