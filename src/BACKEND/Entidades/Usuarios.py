from dataclasses import dataclass
import bcrypt

@dataclass
class Usuarios:
    id_usuarios: int
    nombre: str
    ocupacion: str
    meta_mensual: float
    fecha_registro: str
    email: str
    password: str
    
    @staticmethod
    def hashear_contraseña(password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password_bytes, salt)
        return hash
    
    @staticmethod
    def verificar_contraseña(password, hash_guardado):
        return bcrypt.checkpw(password.encode('utf-8'), hash_guardado)

    @staticmethod
    def imagen_a_bytes(ruta_imagen):
        with open(ruta_imagen, 'rb') as archivo:
            datos_binarios = archivo.read()
        return datos_binarios