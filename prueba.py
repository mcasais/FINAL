import pymysql

# Variables de conexión
host = "localhost"
puerto = 3306
username = "root"
passw = "administrador"
bd = "LIBRERIA"

# Crear la base de datos si no existe
try:
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='administrador')
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS LIBRERIA")
        connection.commit()
    finally:
        connection.close()
except pymysql.MySQLError as e:
    print(f"Error al conectar a MySQL: {e}")

# Crear las tablas
try:
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='administrador', database='LIBRERIA')
    try:
        with connection.cursor() as cursor:
            # Tabla Clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Clientes (
                    ID_Cliente INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                    Nombre VARCHAR(50) NOT NULL,
                    Apellido VARCHAR(50) NOT NULL,
                    Usuario VARCHAR(50) NOT NULL UNIQUE,
                    Mail VARCHAR(50) NOT NULL UNIQUE,
                    Contraseña LONGTEXT NOT NULL
                )
            """)

            # Tabla Alquileres
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Alquileres (
                    ID_Alquiler INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                    ID_libro VARCHAR(50) NOT NULL,
                    DNI_Cliente INT NOT NULL,
                    Fecha_retiro DATE NOT NULL,
                    Fecha_devolución DATE NOT NULL
                )
            """)

            # Tabla Libros
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Libros (
                    ID_Libro INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                    Titulo VARCHAR(100) NOT NULL,
                    Autor VARCHAR(50) NOT NULL,
                    Genero VARCHAR(50) NOT NULL,
                    Fecha_Publicacion VARCHAR(50) NOT NULL,
                    Editorial VARCHAR(50) NOT NULL,
                    Descripción VARCHAR(300),
                    Precio INT NOT NULL,
                    Stock INT NOT NULL       
                )
                           
            """)

        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error al crear las tablas: {e}")
    finally:
        connection.close()
except pymysql.MySQLError as e:
    print(f"Error al conectar a MySQL: {e}")
