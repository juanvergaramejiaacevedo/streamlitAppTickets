# Importamos las librerías necesarias
import streamlit as st  # Librería para crear aplicaciones web interactivas. Instalación: pip install streamlit
import pandas as pd  # Librería para manipulación y análisis de datos. Instalación: pip install pandas
from streamlit_cookies_controller import CookieController # Librería para manejar cookies en Streamlit. Instalación: pip install streamlit-cookies-controller
from dotenv import load_dotenv
from bd import query_to_df

#load_dotenv()

# Creamos una instancia de CookieController
# controller = CookieController()

# Validación simple de usuario y clave con un archivo csv

def validarUsuario(usuario,clave):    
    """Permite la validación de usuario y clave

    Args:
        usuario (str): usuario a validar
        clave (str): clave del usuario

    Returns:
        bool: True usuario valido, False usuario invalido
    """
    
    dfusuarios = query_to_df("SELECT * FROM viewinfousuarios;")

    # Filtramos el dataframe para buscar el usuario y la clave
    if len(dfusuarios[(dfusuarios['correo_electronico']==usuario) & (dfusuarios['numero_documento']==clave)])>0:
        # Si el usuario y la clave existen, retornamos True
        return True
    else:
        # Si el usuario o la clave no existen, retornamos False
        return False

# Generación de menú según el usuario y el rol se maneja desde el código
def generarMenu(usuario):
    """Genera el menú dependiendo del usuario y el rol

    Args:
        usuario (str): usuario utilizado para generar el menú
    """        
    with st.sidebar: # Creamos una barra lateral para el menú
        
        # Cargamos la tabla de usuarios
        dfusuarios = query_to_df("SELECT * FROM viewinfousuarios;")
        # Filtramos la tabla de usuarios por el usuario actual
        dfUsuario =dfusuarios[(dfusuarios['correo_electronico']==usuario)]
        # Cargamos el nombre del usuario
        nombre= dfUsuario['nombre_completo'].values[0]
        
        # Cargamos el rol
        rol= dfUsuario['nombre_rol'].values[0]
        #Mostramos el nombre del usuario
        st.write(f"Bienvenid@ **:blue-background[{nombre}]**") # Mostramos el nombre del usuario con formato
        st.caption(f"Rol: **:red-background[{rol}]**") # Mostramos el rol del usuario
        # Mostramos los enlaces de páginas
        st.page_link("inicio.py", label="Inicio", icon=":material/home:") # Enlace a la página de inicio
        st.subheader("Listado de Páginas") # Subtítulo para los tableros
        # Mostramos los enlaces a las páginas según el rol del usuario
        if rol in ['Administrador']:
            st.page_link("pages/paginaRegistroProyecto.py", label="Registro de Proyecto", icon=":material/domain_add:")      
        if rol in ['Administrador']:
            st.page_link("pages/paginaListadoProyectos.py", label="Listado de Proyectos", icon=":material/apartment:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaEdicionProyecto.py", label="Edición de Proyectos", icon=":material/edit_square:") 
        if rol in ['Administrador']:
            st.page_link("pages/paginaEliminacionProyecto.py", label="Eliminación de Proyectos", icon=":material/domain_disabled:")  
        if rol in ['Administrador']:
            st.page_link("pages/paginaRegistroAsuntoTicket.py", label="Registro de Categoría de Ticket", icon=":material/playlist_add:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaListadoAsuntosTickets.py", label="Listado de Categorías de Tickets", icon=":material/list:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaEdicionAsuntoTicket.py", label="Edición de Categorías de Tickets", icon=":material/edit_square:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaEliminacionAsuntoTicket.py", label="Eliminación de Categorías de Tickets", icon=":material/playlist_remove:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaRegistroUsuario.py", label="Registro de Usuario", icon=":material/person_add:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaListadoUsuarios.py", label="Listado de Usuarios", icon=":material/user_attributes:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaEdicionUsuario.py", label="Edición de Usuarios", icon=":material/edit_square:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaEliminacionUsuario.py", label="Eliminación de Usuarios", icon=":material/person_remove:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaRegistroTicket.py", label="Registro de Ticket", icon=":material/assignment_add:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaListadoTickets.py", label="Listado de Tickets", icon=":material/assignment:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaEliminacionTicket.py", label="Eliminación de Tickets", icon=":material/contract_delete:")
        if rol in ['Administrador', 'SoporteInterno', 'SoporteExterno']:
            st.page_link("pages/paginaCambioEstado.py", label="Atender Tickets", icon=":material/published_with_changes:")
        if rol in ['Administrador', 'Usuario', 'SoporteExterno', 'SoporteInterno']:
            st.page_link("pages/paginaDashboardMisTickets.py", label="Mis Tickets", icon=":material/search_insights:")
        if rol in ['Administrador', 'SoporteExterno', 'SoporteInterno']:
            st.page_link("pages/paginaDashboardTickets.py", label="Dashboard Tickets", icon=":material/analytics:")
        if rol in ['Administrador', 'SoporteExterno']:
            st.page_link("pages/paginaDashboardTicketsSopExt.py", label="Dashboard Tickets | (Soporte Externo)", icon=":material/analytics:")
        if rol in ['Administrador', 'SoporteInterno']:
            st.page_link("pages/paginaDashboardTicketsSopInt.py", label="Dashboard Tickets | (Soporte Interno)", icon=":material/analytics:")
        if rol in ['Administrador']:
            st.page_link("pages/paginaPruebaPwrBI.py", label="Dashboard | Power BI", icon=":material/analytics:")
            
        # Botón para cerrar la sesión
        btnSalir=st.button("Salir") # Creamos un botón para salir
        if btnSalir: # Si se presiona el botón
            st.session_state.clear() # Limpiamos las variables de sesión
            #st.session_state.clear()
            # controller.remove('correo_electronico')
            # Luego de borrar el Session State reiniciamos la app para mostrar la opción de usuario y clave
            st.rerun() # Reiniciamos la aplicación


# Validación de acceso a la página según los roles del usuario
def validarPagina(pagina,usuario):
    """Valida si el usuario tiene permiso para acceder a la página

    Args:
        pagina (str): página a validar
        usuario (str): usuario a validar

    Returns:
        bool: True si tiene permiso, False si no tiene permiso
    """
    # Cargamos la información de usuarios y roles
    dfusuarios = query_to_df("SELECT * FROM viewinfousuarios;")
    
    #data: dict = {
        #'pagina': ["inicio.py", "pages\paginaRegistroProyecto.py", "pages\paginaListadoProyectos.py", "pages\paginaEdicionProyecto.py", "pages\paginaEliminacionProyecto.py", "pages\paginaRegistroAsuntoTicket.py", "pages\paginaListadoAsuntosTickets.py", "pages\paginaEdicionAsuntoTicket.py", "pages\paginaEliminacionAsuntoTicket.py", "pages/paginaRegistroUsuario.py", "pages/paginaListadoUsuarios.py", "pages/paginaEdicionUsuario.py", "pages/paginaEliminacionUsuario.py", "pages/paginaRegistroTicket.py", "pages/paginaListadoTickets.py", "pages/paginaEliminacionTicket.py", "pages/paginaCambioEstado.py", "pages/paginaDashboardMisTickets.py", "pages/paginaDashboardTickets.py", "pages/paginaDashboardTicketsSopExt.py", "pages/paginaDashboardTicketsSopInt.py"],
        #'nombre': ["Inicio", "Registro de Proyectos", "Listado de Proyectos", "Edición de Proyectos", "Eliminación de Proyectos", "Registro de Categoría de Ticket", "Listado de Categorías de Tickets", "Edición de Categorías de Tickets", "Eliminación de Categorías de Tickets", "Registro de Usuario", "Listado de Usuarios", "Edición de Usuarios", "Eliminación de Usuarios", "Registro de Ticket", "Listado de Tickets", "Eliminación de Tickets", "Atender Tickets", "Mis Tickets", "Dashboard Tickets", "Dashboard Tickets | (Soporte Externo)", "Dashboard Tickets | (Soporte Interno)"],
        #'roles': ["ventas|compras|comercial|Administrador", "ventas|Administrador", "ventas|Administrador", "ventas|Administrador", "ventas|Administrador", "ventas|Administrador", "ventas|Administrador", "ventas|Administrador", "ventas|Administrador", "Administrador", "Administrador", "Administrador", "Administrador", "Administrador", "Administrador", "Administrador", "Administrador", "Administrador", "Administrador|SoporteExterno|SoporteInterno", "Administrador|SoporteExterno", "Administrador|SoporteInterno"],
        #'icono': ["home", "domain_add", "apartment", "edit_square", "domain_disabled", "playlist_add", "list", "edit_square", "playlist_remove", "person_add", "user_attributes", "edit_square", "person_remove", "assignment_add", "assignment", "contract_delete", "published_with_changes", "search_insights", "analytics", "analytics", "analytics"]
    #}
    
    #dfPaginas = pd.DataFrame(data)
    
    dfPaginas = query_to_df("SELECT * FROM info_paginas;")
    
    dfUsuario = dfusuarios[(dfusuarios['correo_electronico']==usuario)]

    rol = dfUsuario['nombre_rol'].values[0]
    dfPagina = dfPaginas[(dfPaginas['pagina'].str.contains(pagina))]
    
    # Validamos si el rol del usuario tiene acceso a la página
    if len(dfPagina)>0:
        if rol in dfPagina['roles'].values[0] or rol == "Administrador" or st.secrets.permisos.tipoPermiso=="rol":
            return True # El usuario tiene permiso
        else:
            return False # El usuario no tiene permiso
    else:
        return False # La página no existe en el archivo de permisos

# Generación de menú según el usuario y el rol se maneja desde un archivo csv
def generarMenuRoles(usuario):
    """Genera el menú dependiendo del usuario y el rol asociado a la página

    Args:
        usuario (str): usuario utilizado para generar el menú
    """        
    with st.sidebar: # Menú lateral
        # Cargamos la tabla de usuarios y páginas
        #dfusuarios = pd.read_csv('usuarios.csv')
        #dfPaginas = pd.read_csv('rol_paginas.csv')
        
        dfusuarios = query_to_df("SELECT * FROM viewinfousuarios;")
        dfPaginas = query_to_df("SELECT * FROM info_paginas ORDER BY id_pagina ASC;")

        # Filtramos la tabla de usuarios por el usuario actual
        dfUsuario =dfusuarios[(dfusuarios['correo_electronico']==usuario)]
        # Obtenemos el nombre y rol del usuario
        nombre = dfUsuario['nombre_completo'].values[0]
        rol = dfUsuario['nombre_rol'].values[0]
    
        #Mostramos el nombre del usuario
        st.write(f"Bienvenid@ **:blue-background[{nombre}]** ")
        st.caption(f"Rol: **:red-background[{rol}]**")
        # Mostramos los enlaces de páginas        
        st.subheader("Opciones")
        # Verificamos si se deben ocultar o deshabilitar las opciones del menú
        if st.secrets.permisos.ocultarOpciones=="True": # Verificamos el valor del secreto "ocultarOpciones"
            if rol!='Administrador': # Si el rol no es admin
                # Filtramos la tabla de páginas por el rol actual
                dfPaginas = dfPaginas[dfPaginas['roles'].apply(lambda roles_str: rol in roles_str.split('|'))]

            # Ocultamos las páginas que no tiene permiso
            for index, row in dfPaginas.iterrows():
                icono=row['icono']            
                st.page_link(row['pagina'], label=row['nombre'], icon=f":material/{icono}:")  # Mostramos la página  
        else: # Si no se ocultan las opciones
            # Deshabilitamo las páginas que no tiene permiso            
            for index, row in dfPaginas.iterrows():
                deshabilitarOpcion = True  # Valor por defecto para deshabilitar las opciones
                if rol in row["roles"] or rol == "Administrador": # Verificamos el rol
                    deshabilitarOpcion = False # Habilitamos la página si el usuario tiene permiso
                
                icono=row['icono']            
                # Mostramos el enlace de la página, deshabilitado o no según el permiso.
                st.page_link(row['pagina'], label=row['nombre'], icon=f":material/{icono}:",disabled=deshabilitarOpcion)         
        # Botón para cerrar la sesión
        btnSalir=st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            # controller.remove('correo_electronico')
            st.rerun()

# Generación de la ventana de login y carga de menú
def generarLogin(archivo):
    """Genera la ventana de login o muestra el menú si el login es valido
    """    
    
    # Obtenemos el usuario de la cookie
    # usuario = controller.get('correo_electronico')    
    # Validamos si el usuario ya fue ingresado
    # if usuario:
        # Si ya hay usuario en el cookie, lo asignamos al session state
        # st.session_state['correo_electronico'] = usuario
    # Validamos si el usuario ya fue ingresado    
    if 'correo_electronico' in st.session_state: # Verificamos si la variable usuario esta en el session state
        
        # Si ya hay usuario cargamos el menu
        if st.secrets.permisos.tipoPermiso=="rolpagina":
            generarMenuRoles(st.session_state['correo_electronico']) # Generamos el menú para la página
        else:
            generarMenu(st.session_state['correo_electronico']) # Generamos el menú del usuario       
        if validarPagina(archivo,st.session_state['correo_electronico'])==False: # Si el usuario existe, verificamos la página        
            st.error(f"No tiene permisos para acceder a esta página {archivo}",icon=":material/gpp_maybe:")
            st.stop() # Detenemos la ejecución de la página
    else: # Si no hay usuario
        # Cargamos el formulario de login       
        with st.form('frmLogin'): # Creamos un formulario de login
            parUsuario = st.text_input('Usuario (Correo electrónico)') # Creamos un campo de texto para usuario
            parPassword = st.text_input('Password (Nro. Documento)',type='password') # Creamos un campo para la clave de tipo password
            btnLogin=st.form_submit_button('Ingresar',type='primary') # Botón Ingresar
            if btnLogin: # Verificamos si se presiono el boton ingresar
                if validarUsuario(parUsuario,parPassword): # Verificamos si el usuario y la clave existen
                    st.session_state['correo_electronico'] =parUsuario # Asignamos la variable de usuario
                    # Set a cookie
                    # controller.set('correo_electronico', parUsuario)
                    # Si el usuario es correcto reiniciamos la app para que se cargue el menú
                    st.rerun() # Reiniciamos la aplicación
                else:
                    # Si el usuario es invalido, mostramos el mensaje de error
                    st.error("Usuario o clave inválidos",icon=":material/gpp_maybe:") # Mostramos un mensaje de error                    