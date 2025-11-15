from src.DATABASE.Conexion import Conexion
import datetime

class ConexionIngresos:

    # ==============================
    # INSERTAR INGRESO
    # ==============================
    @staticmethod
    def Insertar(id_usuario, monto, tipo=None, descripcion=None, fecha=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos.")
                return None

            cursor = conn.cursor()

            # Fecha por defecto si no se pasa
            if fecha is None:
                fecha = datetime.datetime.now()

            sql = """
            INSERT INTO ingresos
            (id_usuario, monto, fecha, tipo, descripcion)
            VALUES (%s, %s, %s, %s, %s)
            """

            valores = (id_usuario, monto, fecha, tipo, descripcion)
            cursor.execute(sql, valores)
            conn.commit()

            # Obtener el ID generado automáticamente
            nuevo_id = cursor.lastrowid
            print(f"Ingreso insertado correctamente con ID {nuevo_id}.")
            return nuevo_id

        except Exception as e:
            print("Error al insertar ingreso:", e)
            return None

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # ==============================
    # ACTUALIZAR INGRESO
    # ==============================
    @staticmethod
    def Actualizar(id_ingreso, id_usuario=None, monto=None, tipo=None, descripcion=None, fecha=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos")
                return False

            cursor = conn.cursor()

            sql = "UPDATE ingresos SET "
            valores = []

            if id_usuario is not None:
                sql += "id_usuario = %s, "
                valores.append(id_usuario)
            if monto is not None:
                sql += "monto = %s, "
                valores.append(monto)
            if tipo is not None:
                sql += "tipo = %s, "
                valores.append(tipo)
            if descripcion is not None:
                sql += "descripcion = %s, "
                valores.append(descripcion)
            if fecha is not None:
                sql += "fecha = %s, "
                valores.append(fecha)

            if not valores:
                print("No hay campos para actualizar.")
                return False

            # Eliminar la última coma y agregar WHERE
            sql = sql.rstrip(", ")
            sql += " WHERE id_ingreso = %s"
            valores.append(id_ingreso)

            cursor.execute(sql, tuple(valores))
            conn.commit()

            print(f"Ingreso con ID {id_ingreso} actualizado correctamente.")
            return True

        except Exception as e:
            print("Error al actualizar ingreso:", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # ELIMINAR INGRESO
    # ==============================
    @staticmethod
    def Eliminar(id_ingreso):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos")
                return False

            cursor = conn.cursor()
            sql = "DELETE FROM ingresos WHERE id_ingreso = %s"
            cursor.execute(sql, (id_ingreso,))
            conn.commit()

            print(f"Ingreso con ID {id_ingreso} eliminado correctamente.")
            return True

        except Exception as e:
            print("Error al eliminar ingreso:", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # MOSTRAR INGRESOS
    # ==============================
    @staticmethod
    def Mostrar(id_usuario=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos")
                return []

            cursor = conn.cursor()

            sql = "SELECT id_ingreso, id_usuario, monto, fecha, tipo, descripcion FROM ingresos"
            valores = ()

            if id_usuario is not None:
                sql += " WHERE id_usuario = %s"
                valores = (id_usuario,)

            cursor.execute(sql, valores)
            ingresos = cursor.fetchall()

            # Convertir a lista de diccionarios
            lista_ingresos = []
            for ingreso in ingresos:
                lista_ingresos.append({
                    "id_ingreso": ingreso[0],
                    "id_usuario": ingreso[1],
                    "monto": ingreso[2],
                    "fecha": ingreso[3],
                    "tipo": ingreso[4],
                    "descripcion": ingreso[5]
                })

            return lista_ingresos

        except Exception as e:
            print("Error al mostrar ingresos:", e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
