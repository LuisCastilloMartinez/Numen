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
    
    