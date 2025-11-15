import mysql.connector

#datos de la conexion
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Papacaliente12#",
    database="NUMEN"
)

# Ejecutar una consulta
cursor = conexion.cursor()
cursor.execute("SELECT * FROM usuarios;")

for fila in cursor:
    print(fila)

conexion.close()