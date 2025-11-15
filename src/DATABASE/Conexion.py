import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Papacaliente12#",
    database="NUMEN"
)

cursor = conexion.cursor()

cursor.execute("SELECT DATABASE();")
print("Base usada desde Python:", cursor.fetchone())

cursor.execute("SHOW TABLES;")
print("Tablas en esta base desde Python:")
for t in cursor.fetchall():
    print(t)

cursor.execute("SELECT COUNT(*) FROM usuarios2;")
print("Registros en usuarios2:", cursor.fetchone())

cursor.execute("SELECT * FROM usuarios2;")
print("\nContenido de usuarios2:")
for fila in cursor.fetchall():
    print(fila)

conexion.close()
