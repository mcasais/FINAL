
import mysql.connector
import bcrypt
from mysql.connector import Error
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.graphics import Color, RoundedRectangle


def ejecutar_query(query, params=None):
    """
    Ejecuta una consulta en la base de datos.
    Si es una consulta SELECT, retorna los resultados.
    Para otras consultas, confirma los cambios y retorna True.
    """
    conexion = None
    cursor = None
    try:
        # Establecer conexión con la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="administrador",
            database="LIBRERIA"
        )
        cursor = conexion.cursor()

        # Ejecutar la consulta
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # toma los datos de la bbdd si es SELECT
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()

        # Si no es SELECT, modifica la base de datos (confrimación)(SCRUD)
        conexion.commit()
        return True

    except Error as err:
            #erorr en la conexion con las bbdd
            print(f"Error en la conexión o consulta: {err}")
            return None
    
    finally:
            # Cerrar el cursor y la conexión 
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

       
    """
    Recupera registros de una tabla según el valor de una columna.
    Devuelve los registros o None si no se encuentran coincidencias.
    """
def obtener_registros(tabla, id_columna, valor):

    try:
       
        conexion = mysql.connector.connect(
            host="localhost",            
            user="root",                 
            password="administrador",      
            database="LIBRERIA" 
        )
        cursor = conexion.cursor()

        # Consulta SQL toma datos de una tabla según el valor de una columna
        query = f"SELECT * FROM {tabla} WHERE {id_columna} = %s;"
        
        cursor.execute(query, (valor,))
        var = cursor.fetchall()  # Obtiene las filas

        cursor.close()
        conexion.close()

        return var if var else None  # Retorna None si no hay registros encontrados

    except mysql.connector.Error as err:
        print(f"Error en la conexión o consulta: {err}")
        return None

    """
    Obtiene un usuario de la tabla 'clientes' según el nombre de usuario.
    Devuelve la fila correspondiente o None si no existe.
    """
def get_user(usuario: str):
    usuario_db = obtener_registros('Clientes', 'Usuario', usuario)
    return usuario_db

def login(usr: str, pwd: str, tries: int = 0, max_tries: int = 3):
    """
    Verifica si el usuario puede iniciar sesión.
    Retorna un tuple: (bool, mensaje).
    """
    # Paso 0: Verificar si se excedió el número máximo de intentos
    if tries >= max_tries:
        return False, "Intentos superados. Inténtalo más tarde."

    # Paso 1: Recuperar usuario desde la base de datos
    usuario_db = get_user(usr)  # Implementa get_user para que devuelva la fila completa o None
    if not usuario_db:  # Usuario no existe en la base de datos
        return False, "Usuario o contraseña incorrectos"
    
    # Obtener la contraseña encriptada de la base de datos
    hashed_password = usuario_db[0][5]  

    # bcrypt.checkpw se usa para comparar la contraseña ingresada con la contraseña encriptada
    #la contraseña ingresada (pwd) es plana y la contraseña encriptada es en bytes, .encode la convierte para poder compararla
    #la almacenada en la base de datos es en forma de string
    if bcrypt.checkpw(pwd.encode('utf-8'), hashed_password.encode('utf-8')):
        return True, "Inicio de sesión exitoso"
    else:
        return False, "Usuario o contraseña incorrectos"

def get_user(username):
    return obtener_registros('Clientes', 'Usuario', username)

def get_user_by_email(mail):
    return obtener_registros('Clientes', 'Mail', mail)

def register(name: str, last_name: str, usr: str, mail: str, pwd1: str, pwd2: str):
    # Validar campos obligatorios
    if not all([name, last_name, usr, mail, pwd1, pwd2]):
        return False, 'Todos los campos son obligatorios'

    # Consulta si el usuario ya existe en la base de datos
    usuario_db = get_user(usr)  # Busca el usuario por nombre en la base de datos
    correo_db = get_user_by_email(mail)  # Busca el correo en la base de datos

    # Validaciones de los datos ingresado
    if usuario_db:
        return False, 'El nombre de usuario ya está en uso'

    if correo_db:
        return False, 'El correo electrónico ya está registrado'

    if pwd1 != pwd2:
        return False, 'Las contraseñas no coinciden'

    if len(pwd1) < 8:
        return False, 'La contraseña debe tener al menos 8 caracteres'

    if "@" not in mail or "." not in mail.split("@")[-1]:
        return False, 'El correo electrónico no tiene un formato válido'

    # Crear el usuario en la base de datos si todo es válido
    crear_usuario_en_bd(name, last_name, usr, mail, pwd1)

    return True, 'Usuario creado exitosamente'
import mysql.connector

def crear_usuario_en_bd(name, last_name, usr, mail, pwd1):
    try:
        hashed_password = bcrypt.hashpw(pwd1.encode('utf-8'), bcrypt.gensalt())
        conexion = mysql.connector.connect(
            host="localhost",            
            user="root",                 
            password="administrador",      
            database="LIBRERIA" 
        )
        cursor = conexion.cursor()

        # Query no es de tipo SELECT es de tipo INSERT
        query = """
        INSERT INTO clientes (nombre, apellido, usuario, mail, contraseña)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, last_name, usr, mail, hashed_password))
        
        # Confirmar los cambios
        conexion.commit()

        print("Usuario creado exitosamente")

    except mysql.connector.Error as err:
        print(f"Error en la conexión o consulta: {err}")
        return None

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def alquiler(titulo, autor, tiempo, main_widget):
    try:
        conexion = mysql.connector.connect(
            host="localhost",            
            user="root",                 
            password="administrador",      
            database="LIBRERIA" 
        )
        
        cursor = conexion.cursor(dictionary=True)

        # Realizar la consulta
        query = """
        SELECT * 
        FROM Libros
        WHERE 
            (titulo LIKE CONCAT('%', %s, '%') OR %s = '')
            AND 
            (autor LIKE CONCAT('%', %s, '%') OR %s = '')
            AND stock > 0;  -- Verifica que haya stock disponible
        """
    
        cursor.execute(query, (titulo, titulo, autor, autor),multi=True)
        resultados = cursor.fetchall()

        # Si hay resultados, validar si hay uno o más libros
        if resultados:
            if len(resultados) == 1:
                # Si hay solo un libro, cambiar a la pantalla TSHScreen
                main_widget.ids.error_label.text = f"Libro encontrado: {resultados[0]['titulo']}"
                main_widget.ids.error_label.color = (0, 1, 0, 1)  # Verde para éxito
                main_widget.manager.current = 'The Secret History'
            else:
                # Si hay más de uno, mostrar un Popup con las opciones
                libros = [libro['titulo'] for libro in resultados]
                # Crear el popup
                popup_content = BoxLayout(orientation='vertical')
                label = Label(text="Selecciona el libro correcto")
                popup_content.add_widget(label)

                # Crear botones para cada libro
                for libro in libros:
                    button = Button(text=libro)
                    button.bind(on_press=lambda btn, libro=libro: seleccion_libro(libro, main_widget, popup))
                    popup_content.add_widget(button)
                    
                popup = Popup(
                    title="Selecciona un libro",
                    content=popup_content,
                    size_hint=(0.8, 0.6),
                    auto_dismiss=False  # Para no cerrar automáticamente
                )

                with popup_content.canvas.before:
                    Color(0.9, 0.9, 0.9, 1)  # Color de fondo
                    RoundedRectangle(size=popup_content.size, pos=popup_content.pos, radius=[10]
                )
                popup.open()
        else:
            # Si no hay libros con esos criterios o sin stock
            main_widget.ids.error_label.text = "No se encontraron libros con esos criterios o no hay stock disponible."
            main_widget.ids.error_label.color = (1, 0, 0, 1)  # Rojo para error

        cursor.close()
        conexion.close()
    
    except mysql.connector.Error as e:
        main_widget.ids.error_label.text = f"Error al consultar la base de datos.\n{e}"
        main_widget.ids.error_label.color = (1, 0, 0, 1)  # Rojo para error


def seleccion_libro(libro, main_widget, popup):
    # Mostrar el libro seleccionado y cambiar a la pantalla TSHScreen
    main_widget.ids.error_label.text = f"Has seleccionado: {libro}"
    main_widget.ids.error_label.color = (0, 1, 0, 1)  # Verde para éxito
    main_widget.manager.current = 'The Secret History'
    
    # Cerrar el popup después de la selección
    popup.dismiss()

