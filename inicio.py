import streamlit as st
import login as login

archivo = __file__.split("/")[-1]
login.generarLogin(archivo)

if 'correo_electronico' in st.session_state:
    st.header('Página :orange[principal]')
    #st.subheader('Información página principal')
    
    st.markdown("""
    # 🛠️ **:orange[Gestión Integral de Tickets]**
    Bienvenido a **Gestión Integral de Tickets**, la solución diseñada para **automatizar** y **optimizar** el registro y seguimiento de incidentes, solicitudes y actividades en tu organización. 🚀

    ### 📋 **Características principales**
    - **📂 Gestión centralizada:** Registro, edición y eliminación de tickets, usuarios, proyectos y asuntos de tickets de manera ágil y organizada.
    - **🔍 Interfaz intuitiva:** Navegación sencilla que facilita la consulta y administración de los datos, ideal para usuarios de cualquier nivel.
    - **📊 Dashboards interactivos:** Visualiza análisis y reportes en tiempo real mediante gráficos dinámicos para tomar decisiones informadas.

    ### 🎯 **Nuestro objetivo**
    Brindarte una experiencia **integrada y eficiente**, reduciendo el tiempo dedicado a tareas administrativas y permitiéndote concentrarte en resolver incidencias y mejorar la operación.

    #### 🌟 **¡Explora y gestiona tus tickets de forma inteligente!**
    """)
