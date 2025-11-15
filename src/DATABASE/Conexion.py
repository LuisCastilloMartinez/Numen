import mysql.connector

class Conexion:

    @staticmethod
    def obtener_conexion():
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Papacaliente12#",
                database="NUMEN"
            )

            print("Conexión exitosa")
            return conexion
        
        except mysql.connector.Error as error:
            print(f"Error al conectarse a la base de datos: {error}")
            return None

if __name__ == "__main__":
    Conexion.obtener_conexion()
