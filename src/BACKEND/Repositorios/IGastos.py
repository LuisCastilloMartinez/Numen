from src.DATABASE.Conexion import Conexion
import datetime

class ConexionGastos:

    # ==============================
    # INSERTAR GASTO (ID auto generado)
    # ==============================
    @staticmethod
    def Insertar(id_usuario, id_ingresos, monto, tipo, descripcion, fecha=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos.")
                return None

            cursor = conn.cursor()

            # Si no se proporciona fecha, se toma la fecha actual
            if fecha is None:
                fecha = datetime.datetime.now()

            sql = """
            INSERT INTO gastos
            (id_usuario, id_ingresos, monto, fecha, tipo, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            valores = (id_usuario, id_ingresos, monto, fecha, tipo, descripcion)
            cursor.execute(sql, valores)
            conn.commit()

            # Obtener el ID generado automáticamente
            nuevo_id = cursor.lastrowid
            print(f"Gasto insertado correctamente con ID {nuevo_id}.")
            return nuevo_id

        except Exception as e:
            print("Error al insertar gasto:", e)
            return None

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # ==============================
    # ACTUALIZAR GASTO
    # ==============================
    @staticmethod
    def Actualizar(id_gastos, id_usuario=None, id_ingresos=None, monto=None, tipo=None, descripcion=None, fecha=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexion a la base de datos")
                return False

            cursor = conn.cursor()

            sql = "UPDATE gastos SET "
            valores = []

            if id_usuario is not None:
                sql += "id_usuario = %s, "
                valores.append(id_usuario)
            if id_ingresos is not None:
                sql += "id_ingresos = %s, "
                valores.append(id_ingresos)
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

            # Eliminar la última coma
            sql = sql.rstrip(", ")
            sql += " WHERE id_gastos = %s"
            valores.append(id_gastos)

            cursor.execute(sql, tuple(valores))
            conn.commit()

            print(f"Gasto con ID {id_gastos} actualizado correctamente.")
            return True

        except Exception as e:
            print("Error al actualizar gasto:", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # ELIMINAR GASTO
    # ==============================
    @staticmethod
    def Eliminar(id_gastos):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexion a la base de datos")
                return False

            cursor = conn.cursor()
            sql = "DELETE FROM gastos WHERE id_gastos = %s"
            cursor.execute(sql, (id_gastos,))
            conn.commit()

            print(f"Gasto con ID {id_gastos} eliminado correctamente.")
            return True

        except Exception as e:
            print("Error al eliminar gasto:", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # MOSTRAR GASTOS
    # ==============================
    @staticmethod
    def Mostrar(id_usuario=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexion a la base de datos")
                return []

            cursor = conn.cursor()

            sql = "SELECT id_gastos, id_usuario, id_ingresos, monto, fecha, tipo, descripcion FROM gastos"
            valores = ()

            if id_usuario is not None:
                sql += " WHERE id_usuario = %s"
                valores = (id_usuario,)

            cursor.execute(sql, valores)
            gastos = cursor.fetchall()

            # Convertir a lista de diccionarios
            lista_gastos = []
            for gasto in gastos:
                lista_gastos.append({
                    "id_gastos": gasto[0],
                    "id_usuario": gasto[1],
                    "id_ingresos": gasto[2],
                    "monto": gasto[3],
                    "fecha": gasto[4],
                    "tipo": gasto[5],
                    "descripcion": gasto[6]
                })

            return lista_gastos

        except Exception as e:
            print("Error al mostrar gastos:", e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
