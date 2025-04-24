import streamlit as st
import login as login
import re
import plotly.express as px
from bd import query_to_df, get_tickets_analytics_sopint

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    
    st.subheader('Información | :orange[Dashboard - Tickets (Soporte Interno)]')
    
    tickets_df = get_tickets_analytics_sopint()
    if tickets_df.empty:
        st.info("No hay tickets registrados.")
    else:
        st.dataframe(tickets_df)
        
        # Agregación de datos: Conteo de tickets por estado
        conteo_proyecto = tickets_df.groupby("nombre_proyecto").size().reset_index(name="count")
        
        # Agregación de datos: Conteo de tickets por categoría
        conteo_categorias = tickets_df.groupby("descripcion_asunto").size().reset_index(name="count")
        
        # Agregación de datos: Conteo de tickets por estado
        conteo_estado = tickets_df.groupby("estado").size().reset_index(name="count")
        
        # Agrupar datos por Proyecto, Categoría y Estado
        conteo_agrupacion_multiple = tickets_df.groupby(["nombre_proyecto", "descripcion_asunto", "estado"]).size().reset_index(name="count")

        # Gráfico de barras: Número de tickets por categoría
        fig_bar = px.bar(
            conteo_proyecto,
            x="count",
            y="nombre_proyecto",
            title="Número de Tickets por Nombre de Proyecto",
            labels={"count": "Cantidad de Tickets", "nombre_proyecto": "Nombre de Proyecto"}
        )

        # Gráfico de pastel: Distribución porcentual de tickets por categoría
        fig_pie = px.pie(
            conteo_categorias,
            names="descripcion_asunto",
            values="count",
            title="Distribución de Tickets por Descripción del Asunto"
        )
        
        # Gráfico de barras: Número de tickets por estado
        fig_bar_estado = px.bar(
            conteo_estado,
            x="count",
            y="estado",
            title="Número de Tickets por Estado",
            labels={"count": "Cantidad de Tickets", "estado": "Estado del Ticket"}
        )
        
        # Crear el gráfico de barras con facetas por Estado
        fig_agrupacion_multiple = px.bar(
            conteo_agrupacion_multiple,
            x="nombre_proyecto",
            y="count",
            color="descripcion_asunto",
            facet_col="estado",      # Separa cada Estado en una faceta distinta
            barmode="group",         # Coloca las barras lado a lado para ver la comparación
            title="Tickets agrupados por Proyecto, Descripción y Estado",
            labels={"count": "Cantidad de Tickets"}
        )

        # Distribuir gráficos en columnas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_pie, use_container_width=True)
        with col3:
            st.plotly_chart(fig_bar_estado, use_container_width=True)

        # Mostrar el gráfico de dispersión en toda la anchura
        st.plotly_chart(fig_agrupacion_multiple, use_container_width=True)