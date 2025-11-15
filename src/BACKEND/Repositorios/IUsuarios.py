from src.BACKEND.Entidades.Usuarios import Usuarios
from src.DATABASE.Conexion import Conexion
import bcrypt

class ConexionEntidades:

    # ==============================
    # INSERTAR USUARIO
    # ==============================
    @staticmethod
    def Insertar(nombre, ocupacion, meta_mensual, email, password, foto):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos.")
                return

            cursor = conn.cursor()

            # Hashear la contraseña antes de guardar
            password_hash = ConexionEntidades.hashear_contraseña(password)

            sql = """
            INSERT INTO usuarios
            (nombre, ocupacion, meta_mensual, email, password_hash, foto)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            valores = (nombre, ocupacion, meta_mensual, email, password_hash, foto)
            cursor.execute(sql, valores)
            conn.commit()

            print("Usuario insertado correctamente.")

        except Exception as e:
            print("Error al insertar usuario:", e)

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # ==============================
    # ACTUALIZAR USUARIO
    # ==============================
    @staticmethod
    def Actualizar_Usuario(nombre, ocupacion, meta_mensual, email, password=None, foto=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexion a la base de datos")
                return

            cursor = conn.cursor()

            # Si viene contraseña nueva, se hashea
            if password is not None:
                password_hash = ConexionEntidades.hashear_contraseña(password)
            else:
                password_hash = None

            sql = "UPDATE usuarios SET "
            valores = []

            if ocupacion is not None:
                sql += "ocupacion = %s, "
                valores.append(ocupacion)
            if meta_mensual is not None:
                sql += "meta_mensual = %s, "
                valores.append(meta_mensual)
            if password_hash is not None:
                sql += "password_hash = %s, "
                valores.append(password_hash)
            if foto is not None:
                sql += "foto = %s, "
                valores.append(foto)

            # Eliminar la última coma
            sql = sql.rstrip(", ")
            sql += " WHERE email = %s"
            valores.append(email)

            cursor.execute(sql, tuple(valores))
            conn.commit()

            print(f"Usuario {nombre} actualizado correctamente.")

        except Exception as e:
            print("Error al actualizar usuario:", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # ELIMINAR USUARIO
    # ==============================
    @staticmethod
    def Eliminar_Usuario(email):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexion a la base de datos")
                return

            cursor = conn.cursor()
            sql = "DELETE FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            conn.commit()

            print(f"Usuario con email {email} eliminado correctamente.")

        except Exception as e:
            print("Error al eliminar usuario:", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # MOSTRAR USUARIOS
    # ==============================
    @staticmethod
    def Mostrar_Usuarios():
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexion a la base de datos")
                return

            cursor = conn.cursor()
            sql = "SELECT nombre, ocupacion, meta_mensual, email, foto FROM usuarios"
            cursor.execute(sql)
            usuarios = cursor.fetchall()

            for usuario in usuarios:
                print("Nombre:", usuario[0])
                print("Ocupación:", usuario[1])
                print("Meta mensual:", usuario[2])
                print("Email:", usuario[3])
                print("Foto:", usuario[4])
                print("---------------------------")

        except Exception as e:
            print("Error al mostrar usuarios:", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # HASH CONTRASEÑA
    # ==============================
    @staticmethod
    def hashear_contraseña(password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password_bytes, salt)
        return hash

    # ==============================
    # LOGIN
    # ==============================
    @staticmethod
    def Login(email, password):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexion a la base de datos")
                return False

            cursor = conn.cursor()
            sql = "SELECT password_hash FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            resultado = cursor.fetchone()

            if resultado is None:
                print("Usuario no encontrado.")
                return False

            password_hash = resultado[0]
            # bcrypt requiere bytes
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                print("Login exitoso.")
                return True
            else:
                print("Contraseña incorrecta.")
                return False

        except Exception as e:
            print("Error en login:", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
