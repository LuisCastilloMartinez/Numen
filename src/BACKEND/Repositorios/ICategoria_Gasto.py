from src.DATABASE.Conexion import Conexion

class ConexionCategorias:

    # ==============================
    # INSERTAR CATEGORIA
    # ==============================
    @staticmethod
    def Insertar(id_categoria=None, nombre=None, tipo_sugerido=None, icono=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos.")
                return False

            cursor = conn.cursor()
            sql = """
            INSERT INTO categorias
            (id_categoria, nombre, tipo_sugerido, icono)
            VALUES (%s, %s, %s, %s)
            """
            valores = (id_categoria, nombre, tipo_sugerido, icono)
            cursor.execute(sql, valores)
            conn.commit()

            print("Categoría insertada correctamente.")
            return True

        except Exception as e:
            print("Error al insertar categoría:", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # ACTUALIZAR CATEGORIA
    # ==============================
    @staticmethod
    def Actualizar(id_categoria, nombre=None, tipo_sugerido=None, icono=None):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos.")
                return False

            cursor = conn.cursor()
            sql = "UPDATE categorias SET "
            valores = []

            if nombre is not None:
                sql += "nombre = %s, "
                valores.append(nombre)
            if tipo_sugerido is not None:
                sql += "tipo_sugerido = %s, "
                valores.append(tipo_sugerido)
            if icono is not None:
                sql += "icono = %s, "
                valores.append(icono)

            if not valores:
                print("No hay campos para actualizar.")
                return False

            sql = sql.rstrip(", ")
            sql += " WHERE id_categoria = %s"
            valores.append(id_categoria)

            cursor.execute(sql, tuple(valores))
            conn.commit()

            print(f"Categoría con ID {id_categoria} actualizada correctamente.")
            return True

        except Exception as e:
            print("Error al actualizar categoría:", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # ELIMINAR CATEGORIA
    # ==============================
    @staticmethod
    def Eliminar(id_categoria):
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos")
                return False

            cursor = conn.cursor()
            sql = "DELETE FROM categorias WHERE id_categoria = %s"
            cursor.execute(sql, (id_categoria,))
            conn.commit()

            print(f"Categoría con ID {id_categoria} eliminada correctamente.")
            return True

        except Exception as e:
            print("Error al eliminar categoría:", e)
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==============================
    # MOSTRAR CATEGORIAS
    # ==============================
    @staticmethod
    def Mostrar():
        try:
            conn = Conexion.obtener_conexion()
            if conn is None:
                print("No hay conexión a la base de datos")
                return []

            cursor = conn.cursor()
            sql = "SELECT id_categoria, nombre, tipo_sugerido, icono FROM categorias"
            cursor.execute(sql)
            categorias = cursor.fetchall()

            # Devolver lista de diccionarios
            lista_categorias = []
            for cat in categorias:
                lista_categorias.append({
                    "id_categoria": cat[0],
                    "nombre": cat[1],
                    "tipo_sugerido": cat[2],
                    "icono": cat[3]
                })

            return lista_categorias

        except Exception as e:
            print("Error al mostrar categorías:", e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
 